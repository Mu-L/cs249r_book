"""Model and activation memory accounting."""

from __future__ import annotations

import math
import pint

from mlsysim.core.constants import ureg, MB

from ._units import _ensure_unit


def model_memory(params, bytes_per_param, unit=MB):
    """
    Calculates the memory footprint to store model weights in a requested unit.

    Parameters
    ----------
    params : Quantity or int
        Total number of parameters in the model.
    bytes_per_param : Quantity or int
        Size of each parameter in bytes (e.g., 2 bytes for FP16).
    unit : pint.Unit, optional
        The desired output unit (defaults to MB).

    Returns
    -------
    float
        The calculated memory footprint magnitude in the requested unit.
    """
    if isinstance(params, ureg.Quantity):
        try:
            param_count = params.to(ureg.count).magnitude
        except pint.DimensionalityError:
            raise pint.DimensionalityError(
                params.units,
                ureg.count,
                extra_msg=(
                    f" in model_memory() — params must be in param/count units, "
                    f"got {params.units}"
                ),
            )
    else:
        param_count = params

    if isinstance(bytes_per_param, ureg.Quantity):
        try:
            bpp = bytes_per_param.to(ureg.byte).magnitude
        except pint.DimensionalityError:
            raise pint.DimensionalityError(
                bytes_per_param.units,
                ureg.byte,
                extra_msg=(
                    f" in model_memory() — bytes_per_param must be byte units, "
                    f"got {bytes_per_param.units}"
                ),
            )
    else:
        bpp = bytes_per_param

    total_bytes = param_count * bpp * ureg.byte
    return total_bytes.to(unit).magnitude


def calc_activation_memory(
    n_layers,
    seq_len,
    batch_size,
    hidden_dim,
    n_heads=None,
    precision_bytes=1,
    strategy="selective",
):
    """
    Estimates the activation memory required for a Transformer model during training.

    This implements the analytical bounds from Korthikanti et al. (2023). Memory
    consumption depends heavily on the activation recomputation (checkpointing) strategy.

    Parameters
    ----------
    n_layers : int
        Number of transformer layers per device (after pipeline parallelism).
    seq_len : int
        Sequence length.
    batch_size : int
        Microbatch size per device.
    hidden_dim : int
        Hidden dimension of the model.
    n_heads : int, optional
        Number of attention heads (reserved for future exact attention estimates).
    precision_bytes : float, optional
        Bytes per activation element (defaults to 1).
    strategy : str, optional
        Recomputation strategy: 'none' (34x), 'selective' (10x), or 'full' (2x).
        Defaults to 'selective'.

    Returns
    -------
    Quantity
        The total estimated activation memory in bytes.
    """
    del n_heads  # reserved for future head-aware estimates
    s, b, h = seq_len, batch_size, hidden_dim
    if strategy == "full":
        bytes_per_layer = 2 * s * b * h * precision_bytes
    elif strategy == "selective":
        bytes_per_layer = 10 * s * b * h * precision_bytes
    else:
        bytes_per_layer = 34 * s * b * h * precision_bytes
    return (n_layers * bytes_per_layer) * ureg.byte


def calc_checkpoint_size(n_params, bytes_per_param=14):
    """
    Calculates the total storage size required for a training checkpoint.

    Parameters
    ----------
    n_params : Quantity
        Total number of parameters in the model.
    bytes_per_param : Quantity or int, optional
        Bytes required per parameter for optimizer state + weights.
        For mixed-precision Adam, this is typically 14 bytes (FP32 master weights,
        FP32 momentum, FP32 variance, FP16 parameters). Defaults to 14.

    Returns
    -------
    Quantity
        Total checkpoint size in bytes.
    """
    bpp = _ensure_unit(bytes_per_param, ureg.byte, "bytes_per_param")
    return (n_params * bpp).to(ureg.byte)


def calc_kv_cache_size(
    n_layers,
    n_heads,
    head_dim,
    seq_len,
    batch_size,
    bytes_per_elem=2,
    kv_precision_bytes=None,
):
    """
    Calculates the KV cache memory size for autoregressive inference.

    The KV cache stores Key and Value tensors for all previous tokens to avoid
    recomputing them. The size is strictly: 2 * L * H * d * S * B * precision.

    Parameters
    ----------
    n_layers : int
        Number of transformer layers.
    n_heads : int
        Number of Key/Value attention heads (accounts for MQA/GQA).
    head_dim : int
        Dimension of a single attention head.
    seq_len : int
        Total sequence length (context + generated tokens).
    batch_size : int
        Number of parallel requests.
    bytes_per_elem : Quantity or int, optional
        Numerical precision of the cache (defaults to 2 for FP16/BF16).
    kv_precision_bytes : Quantity or int, optional
        Override for specific KV cache quantization (e.g., INT8 KV cache).

    Returns
    -------
    Quantity
        Total KV cache size in bytes.
    """
    effective_bpe = kv_precision_bytes if kv_precision_bytes is not None else bytes_per_elem
    bpe = _ensure_unit(
        effective_bpe,
        ureg.byte,
        "kv_precision_bytes" if kv_precision_bytes is not None else "bytes_per_elem",
    )
    return (2 * n_layers * n_heads * head_dim * seq_len * batch_size * bpe).to(ureg.byte)


def calc_paged_kv_cache_size(
    n_layers,
    n_heads,
    head_dim,
    seq_len,
    batch_size,
    page_size_tokens=16,
    bytes_per_elem=2,
):
    """
    Calculates KV cache size accounting for PagedAttention fragmentation.

    PagedAttention (Kwon et al., 2023) allocates KV cache in fixed-size blocks
    (pages). This eliminates external fragmentation but introduces internal
    fragmentation in the final allocated page.

    Parameters
    ----------
    n_layers : int
        Number of transformer layers.
    n_heads : int
        Number of Key/Value attention heads.
    head_dim : int
        Dimension of a single attention head.
    seq_len : int
        Current sequence length.
    batch_size : int
        Number of parallel requests.
    page_size_tokens : int, optional
        Number of tokens per allocated page block (defaults to 16).
    bytes_per_elem : Quantity or int, optional
        Numerical precision (defaults to 2).

    Returns
    -------
    tuple
        A 2-tuple containing:
        - size (Quantity): Total allocated KV cache size in bytes.
        - frag_pct (float): Internal memory fragmentation (0.0 to 1.0).
    """
    bpe = _ensure_unit(bytes_per_elem, ureg.byte, "bytes_per_elem")
    padded_seq_len = math.ceil(seq_len / page_size_tokens) * page_size_tokens
    internal_frag = max(0, padded_seq_len - seq_len)
    frag_pct = internal_frag / padded_seq_len if padded_seq_len > 0 else 0.0
    size = (
        2 * n_layers * n_heads * head_dim * padded_seq_len * batch_size * bpe
    ).to(ureg.byte)
    return size, frag_pct
