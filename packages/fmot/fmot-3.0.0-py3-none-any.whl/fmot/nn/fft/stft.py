import torch
from torch import nn, Tensor
from fmot.nn.sequencer import Sequencer
from fmot.nn.atomics import Identity
from fmot.nn.signal_processing import TuningEpsilon
from fmot.nn.super_structures import SuperStructure
from .fft import RFFT, IRFFT
from fmot.precisions import int16, Precision
from typing import *

ISTFT_AUTO_FACTOR = 0.0005
STFT_AUTO_FACTOR = 1 / 128


class _ReciprocalErrorCorrection(nn.Module):
    """Simple method to improve initial estimate of reciprocal.

    Main goal: make x * xinv closer to 1, useful to use this method
    with invertible normalizing factors
    """

    def forward(self, x, xinv):
        one_approx_v0 = x * xinv
        xinv1 = 2 * xinv - (one_approx_v0) * xinv
        return x, xinv1


class InvertibleNormalizingFactor(nn.Module):
    def __init__(self, clamp_min=0.02):
        super().__init__()
        self.clamp_min = clamp_min
        self.error_corrector = _ReciprocalErrorCorrection()

    def forward(self, x):
        norm = torch.mean(torch.abs(x), dim=-1, keepdim=True)
        norm = torch.clamp(norm, min=self.clamp_min, max=None)
        # norm = self.tuneps(norm)
        inorm = 1 / norm

        # want norm * inorm as close as we can get to 1 to avoid gain fluctuation
        # problems. Two iterations of reciprical error correction
        norm, inorm = self.error_corrector(norm, inorm)

        return norm, inorm


class Mul(nn.Module):
    def forward(self, x, y):
        return x * y


class Cat(nn.Module):
    """Utility; exists so that STFTBUffCell can be a SuperStructure"""

    def __init__(self, dim):
        super().__init__()
        self.dim = dim

    def forward(self, x: List[Tensor]) -> Tensor:
        return torch.cat(x, self.dim)


class _STFTBuffCell(SuperStructure):
    """Handles the data orchestration inside of STFT Buffer (with arb. kernel size)"""

    def __init__(self):
        super().__init__()
        self.cat = Cat(-1)

    @torch.jit.export
    def forward(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        y_t = self.cat(state + [x_t])
        state = state[1:] + [x_t]
        return y_t, state


class STFTBuffer(Sequencer):
    """Manages the internal buffer of an STFT and concatenates inputs with past inputs
    to fill the window-size.

    window_size must be an integer multiple of hop_size."""

    def __init__(self, window_size: int, hop_size: int):
        k = window_size / hop_size
        assert k % 1 == 0, "window_size must be an integer multiple of hop_size"
        k = int(k)

        super().__init__(state_shapes=[[hop_size]] * (k - 1), batch_dim=0, seq_dim=1)
        self.cell = _STFTBuffCell()

    @torch.jit.export
    def step(self, x_t: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        return self.cell(x_t, state)


class WindowMul(nn.Module):
    def __init__(self, window):
        super().__init__()
        self.window = nn.Parameter(window, requires_grad=False)

    def forward(self, x):
        return x * self.window


class ConstantMul(nn.Module):
    def __init__(self, cnst: float):
        super().__init__()
        self.cnst = cnst

    def forward(self, x):
        return self.cnst * x


class ZeroCatter(nn.Module):
    def __init__(self, n):
        super().__init__()
        self.zeros = nn.Parameter(torch.zeros(n), requires_grad=False)

    def forward(self, x):
        return torch.cat([x, self.zeros], -1)


class STFT(SuperStructure):
    """Short-Time Fourier Transform

    Arguments:
        n_fft (int): size of FFT, in samples
        hop_size (int): hop size, in samples
        window_size (int, optional): window size, in samples. If ``None``, defaults to ``n_fft``. Default :attr:`None`
        window_fn (Tensor, optional): Optional window function. Should be a 1D of length ``n_fft``. Default :attr:`None`
        n_stages (int | "auto", optional): number of power-of-2 decomposition stages. ``n_stages = 0`` yields a
            dense matrix implementation of the DFT. Default is "auto", in which case the function :attr:`auto_n_stages`
            is called to find the optimal number of decomposition stages.
        weight_precision (int | Precision, optional): precision to use for FFT weights. Valid options
            are :attr:`8` / :attr:`fmot.precisions.int8` to specify int8 weights, or :attr:`16` / :attr:`fmot.precisions.int16` to
            specify int16 weights. Default is :attr:`fmot.precisions.int16`,
            which yields the best quantized accuracy at the cost of 2x higher memory overhead and computatate cost.
        norm_min (float | "auto" | None, optional): Internal normalizing factor, used to improve fidelity when input signals dynamic
            range varies widely. Before taking the IFFT, the complex signal is normalized by dividing by
            :attr:`max(l1_norm(x), norm_min)`. After taking the IFFT, the waveform is multiplied by the inverse factor.
            Options:
                - :attr:`None`: no normalization is performed.
                - :attr:`"auto"`: norm_min is set to `0.01`, to automatically scale this value
                    based on the magnitude of the STFT components (which changes depending on the IFFT size)
                - :attr:`float`: if a float value is provided, this is used directly to set the norm_min value.
            Default: :attr:`"auto"`.


    .. note::

        Compared to the PyTorch builtin, the input must be reshaped into non-overlapping hops,
        and the output is returned as two separate tensors containing the real
        and imaginary parts. We do not automatically convert :attr:`torch.stft` into :attr:`fmot.nn.STFT`.

        **Comparison with torch.stft**

        .. code:: python

            import torch
            import fmot

            hop_length = 128
            window_length = 256
            window_fn = torch.hann_window(window_length)

            x = torch.randn(8, 16000)

            # using built-in torch.stft
            y_torch = torch.stft(x, n_fft=window_length, hop_length=hop_length,
                window_fn=window_fn, return_complex=True)
            re_torch = y_torch.real
            im_torch = y_torch.imag

            # using fmot.nn.STFT
            stft = fmot.nn.STFT(n_fft=window_length, hop_size=hop_length, n_stages="auto",
                window_fn=window_fn)
            # input needs to be reshaped into non-overlapping hops
            x_reshaped = x.reshape(8, 125, 128)
            re_fmot, im_fmot = stft(x_reshape)

    """

    report_supported = True

    def __init__(
        self,
        n_fft: int,
        hop_size: int,
        window_size: int = None,
        window_fn: Tensor = None,
        n_stages: Union[int, Literal["auto"]] = "auto",
        weight_precision: Union[Literal[8, 16], Precision] = int16,
        norm_min: Optional[Union[float, Literal["auto"]]] = "auto",
    ):
        super().__init__()
        self.n_fft = n_fft
        self.hop_size = hop_size
        if window_size is None:
            window_size = n_fft
        self.window_size = window_size
        self.n_stages = n_stages

        if window_fn is not None:
            self.window_mul = WindowMul(window_fn)
        else:
            self.window_mul = None

        if window_size < n_fft:
            self.catter = ZeroCatter(n_fft - window_size)
        elif window_size > n_fft:
            raise ValueError("window_size cannot exceed n_fft")
        else:
            self.catter = None

        self.buffer = STFTBuffer(window_size, hop_size)
        self.rfft = RFFT(n_fft, n_stages, weight_precision)

        if norm_min is not None:
            if norm_min == "auto":
                norm_min = STFT_AUTO_FACTOR

            if not isinstance(norm_min, (int, float)):
                raise ValueError(
                    f'Expected norm_min to be a float or "auto", got {norm_min}'
                )

            self.normalizer = InvertibleNormalizingFactor(norm_min)
            self.mul_inorm = Mul()
            self.mul_norm = Mul()
        else:
            self.normalizer = None

    def forward(self, x: Tensor) -> Tuple[Tensor, Tensor]:
        # concatenate with previous frames
        x_stack, __ = self.buffer(x)

        # optionally apply window_fn:
        if self.window_mul is not None:
            x_stack = self.window_mul(x_stack)

        # compute L1 norm and its inverse
        if self.normalizer is not None:
            norm, inorm = self.normalizer(x_stack)
            x_stack = self.mul_inorm(x_stack, inorm)

        # optionally pad with zeros:
        if self.catter is not None:
            x_stack = self.catter(x_stack)

        # apply the RFFT
        re_out, im_out = self.rfft(x_stack)

        # apply the norm
        if self.normalizer is not None:
            re_out = self.mul_norm(re_out, norm)
            im_out = self.mul_norm(im_out, norm)

        return re_out, im_out


@torch.no_grad()
def check_50pct_cola(window: Tensor) -> Tuple[bool, Union[float, Tensor]]:
    """Checks a window-function for the COLA (Constant Overlap Add)
    condition for 50% overlap.

    If COLA is satisfied, returns (True, c), where c is a scalar float
    given by the 50%-overlap-sum of the window function.

    If COLA is not satisfied, returns (False, woverlap), where woverlap
    is a tensor given by the 50%-overlap-sum of the window function.
    """

    N = len(window)
    assert N % 2 == 0, "Window function must be even-lengthed"

    w_left = window[: N // 2]
    w_right = window[N // 2 :]

    woverlap = w_left + w_right

    assert torch.all(
        woverlap != 0
    ), "Window function does not satisfy the NOLA (nonzero overlap add) constraint"

    c = woverlap[0]

    if torch.all((woverlap - c).abs() / torch.max(woverlap) < 1e-6):
        return True, c.item()
    else:
        return False, woverlap


class SynthesisWindow(nn.Module):
    """Convert an analysis window into a synthesis window,
    assuming 50% overlap.
    """

    def __init__(self, analysis_window: torch.Tensor):
        super().__init__()
        wa, wb = analysis_window.chunk(2, 0)
        den = wa**2 + wb**2
        assert torch.all(den > 0), "Window function must satisfy the COLA constraint"
        den = torch.cat([den, den])
        self.window = nn.Parameter(analysis_window / den, requires_grad=False)

    def forward(self, x):
        return self.window * x


class _OverlapAdd50pct(Sequencer):
    def __init__(self, hop_size: int):
        super().__init__([[hop_size]], 0, 1)

    @torch.jit.export
    def step(self, x: Tensor, state: List[Tensor]) -> Tuple[Tensor, List[Tensor]]:
        x_curr, x_next = torch.chunk(x, 2, -1)
        (s_curr,) = state
        x = x_curr + s_curr
        return x, [x_next]


class OverlapAdd50Pct(nn.Module):
    """50% Overlap-Add Decoding. Takes overlapping waveforms and performs
    overlap-add, multiplying by a constant or time-varying factor if a window-function
    is used.
    """

    report_supported = True

    def __init__(self, hop_size: int, window: Tensor = None):
        super().__init__()
        if window is not None:
            self.synthesis_window = SynthesisWindow(window)

        else:
            self.synthesis_window = ConstantMul(0.5)
        self.ola = _OverlapAdd50pct(hop_size)

    def forward(self, x):
        x = self.synthesis_window(x)
        y, __ = self.ola(x)
        return y


class ISTFT(SuperStructure):
    """Inverse Short-Time Fourier Transform

    Arguments:
        n_fft (int): size of FFT, in samples
        hop_size (int): hop size, in samples
        window_size (int): window size, in samples. If ``None``, defaults to ``n_fft``
        window_fn (Tensor): Optional window function. Should be a 1D of length ``n_fft``
        n_stages (int | "auto", optional): number of power-of-2 decomposition stages. ``n_stages = 0`` yields a
            dense matrix implementation of the DFT. Default is "auto", in which case the function :attr:`auto_n_stages`
            is called to find the optimal number of decomposition stages.
        weight_precision (int | Precision, optional): precision to use for FFT weights. Valid options
            are :attr:`8` / :attr:`fmot.precisions.int8` to specify int8 weights, or :attr:`16` / :attr:`fmot.precisions.int16` to
            specify int16 weights. Default is :attr:`fmot.precisions.int16`,
            which yields the best quantized accuracy at the cost of 2x higher memory overhead and computatate cost.
        norm_min (float | "auto" | None, optional): Internal normalizing factor, used to improve fidelity when input signals dynamic
            range varies widely. Before taking the IFFT, the complex signal is normalized by dividing by
            :attr:`max(l1_norm(x), norm_min)`. After taking the IFFT, the waveform is multiplied by the inverse factor.
            Options:
                - :attr:`None`: no normalization is performed.
                - :attr:`"auto"`: norm_min is set to `0.01 * n_fft`, to automatically scale this value
                    based on the magnitude of the STFT components (which changes depending on the IFFT size)
                - :attr:`float`: if a float value is provided, this is used directly to set the norm_min value.
            Default: :attr:`"auto"`.

    .. warning:

        Presently, restricted to the 50% overlap case where ``n_fft == window_size == 2*hop_size``
    """

    report_supported = True

    def __init__(
        self,
        n_fft: int,
        hop_size: int,
        window_size: int = None,
        window_fn: Tensor = None,
        n_stages: Union[int, Literal["auto"]] = "auto",
        weight_precision: Union[Literal[8, 16], Precision] = int16,
        norm_min: Optional[Union[float, Literal["auto"]]] = "auto",
    ):
        super().__init__()
        self.n_fft = n_fft
        self.hop_size = hop_size
        if window_size is None:
            window_size = n_fft

        assert window_size == n_fft, "window_size != n_fft not yet supported in ISTFT"
        assert (
            window_size == 2 * hop_size
        ), r"ISTFT with overlap other than 50% not yet supported in ISTFT"

        self.irfft = IRFFT(n_fft, n_stages, weight_precision)
        self.ola = OverlapAdd50Pct(hop_size, window=window_fn)

        if norm_min is not None:
            if norm_min == "auto":
                norm_min = ISTFT_AUTO_FACTOR * n_fft

            if not isinstance(norm_min, (float, int)):
                raise ValueError(
                    f'Expected norm_min to be a float or "auto", got {norm_min}'
                )

            self.normalizer = InvertibleNormalizingFactor(clamp_min=norm_min)
            self.cat = Cat(dim=-1)
            self.mul_norm = Mul()
            self.mul_inorm = Mul()
        else:
            self.normalizer = None

    def forward(self, re: Tensor, im: Tensor) -> Tensor:
        """Compute the ISTFT given tensors holding the real and imaginary spectral components.

        Arguments:
            re (Tensor): real-part of the STFT to invert, shape ``(batch, N, n_fft//2 + 1)``
            im (Tensor): imaginary-part of the STFT to invert, shape ``(batch, N, n_fft//2 + 1)``

        Returns:
            Tensor, real-valued inversion of the input STFT, with overlap-add inversion.
            shape: (batch, N, hop_size)
        """
        if self.normalizer is not None:
            norm, inorm = self.normalizer(self.cat([re, im]))
            re = self.mul_inorm(re, inorm)
            im = self.mul_inorm(im, inorm)

        winsig = self.irfft(re, im)
        if self.normalizer is not None:
            winsig = self.mul_norm(winsig, norm)
        olasig = self.ola(winsig)
        return olasig
