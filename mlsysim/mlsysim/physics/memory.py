"""Model and activation memory accounting."""

from __future__ import annotations

import math

import pint

from mlsysim.core.constants import ureg, MB

from ._units import _ensure_unit


def model_memory(params, bytes_per_param, unit=MB):
    """Model memory footprint in the requested unit (default MB)."""
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
    """Transformer activation memory (Korthikanti et al., 2023)."""
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
    """Checkpoint size for mixed-precision Adam training."""
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
    """KV cache memory for autoregressive inference."""
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
    """PagedAttention KV cache size and internal fragmentation (Kwon et al., 2023)."""
    bpe = _ensure_unit(bytes_per_elem, ureg.byte, "bytes_per_elem")
    padded_seq_len = math.ceil(seq_len / page_size_tokens) * page_size_tokens
    internal_frag = max(0, padded_seq_len - seq_len)
    frag_pct = internal_frag / padded_seq_len if padded_seq_len > 0 else 0.0
    size = (
        2 * n_layers * n_heads * head_dim * padded_seq_len * batch_size * bpe
    ).to(ureg.byte)
    return size, frag_pct
