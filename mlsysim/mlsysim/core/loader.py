"""YAML data-layer loader.

Leaf reference data (hardware chips, models, datasets, …) lives as YAML and is
loaded + validated against a pydantic schema at import, then assembled into a
``Registry`` subclass whose consumer API is identical to the former
hand-written Python registry (``Hardware.Cloud.H100.memory.bandwidth`` etc.).

Two encodings are handled before pydantic validation:

* **Unit-bearing strings** (``"3.35 TB/s"``, ``"80 GiB"``) are parsed by pint —
  this is already handled by the ``Quantity`` validator in ``core/types.py``,
  so the loader passes strings straight through.
* **``@tech:`` references** (``"@tech:Interconnect.NVLink.latency"``) preserve
  the instance→tech-class single source of truth: the value lives once in
  ``Hardware.Tech`` and instances point at it rather than copying it. The loader
  resolves these against ``tech_root`` into the live Quantity object.

See ``.claude/rules/mlsysim.md`` → *Storage format*.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any
import yaml

from .registry import Registry

_TECH_PREFIX = "@tech:"


def _resolve(node: Any, tech_root: Any) -> Any:
    """Recursively resolve ``@tech:`` reference markers against ``tech_root``."""
    if isinstance(node, dict):
        return {k: _resolve(v, tech_root) for k, v in node.items()}
    if isinstance(node, list):
        return [_resolve(v, tech_root) for v in node]
    if isinstance(node, str) and node.startswith(_TECH_PREFIX):
        if tech_root is None:
            raise ValueError(f"{node!r} found but no tech_root supplied to load_registry")
        obj = tech_root
        for part in node[len(_TECH_PREFIX):].split("."):
            obj = getattr(obj, part)
        return obj
    return node


def load_registry(data_dir, model_cls, *, name: str, doc: str = "", tech_root: Any = None) -> type:
    """Build a ``Registry`` subclass from the ``*.yaml`` files in ``data_dir``.

    Each file becomes one validated ``model_cls`` instance, exposed as a class
    attribute named by the file's ``__key__`` field (falling back to the file
    stem). Files are read in sorted order; ``Registry.list()`` and attribute
    access are order-independent, so this matches the former definition order.
    """
    data_dir = Path(data_dir)
    attrs: dict[str, Any] = {"__doc__": doc}
    for yaml_file in sorted(data_dir.glob("*.yaml")):
        raw = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        key = raw.pop("__key__", yaml_file.stem)
        attrs[key] = model_cls(**_resolve(raw, tech_root))
    return type(name, (Registry,), attrs)
