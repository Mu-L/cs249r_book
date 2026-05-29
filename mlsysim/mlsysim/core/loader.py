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


def _instantiate(raw: dict, *, model_cls, type_map, tech_root):
    """Validate one entry dict into its pydantic model.

    Polymorphic schemas (e.g. the ``Workload`` family) carry a ``__type__``
    tag selecting the concrete class from ``type_map``; uniform schemas omit it
    and use ``model_cls``.
    """
    raw = dict(raw)
    type_name = raw.pop("__type__", None)
    if type_name is not None:
        if not type_map or type_name not in type_map:
            raise ValueError(f"unknown __type__ {type_name!r} (type_map keys: {sorted(type_map or [])})")
        cls = type_map[type_name]
    else:
        cls = model_cls
    if cls is None:
        raise ValueError("no model class: supply model_cls or a __type__ in the data")
    return cls(**_resolve(raw, tech_root))


def _build(entries: dict, *, name: str, doc: str, model_cls, type_map, tech_root) -> type:
    attrs: dict[str, Any] = {"__doc__": doc}
    for key, raw in entries.items():
        attrs[key] = _instantiate(raw, model_cls=model_cls, type_map=type_map, tech_root=tech_root)
    return type(name, (Registry,), attrs)


def load_registry(data_dir, model_cls=None, *, name: str, doc: str = "",
                  tech_root: Any = None, type_map: dict | None = None) -> type:
    """Build a ``Registry`` subclass from one-entry-per-file YAML in ``data_dir``.

    Each ``*.yaml`` becomes one validated instance, exposed as a class attribute
    named by the file's ``__key__`` field (falling back to the file stem). Files
    are read sorted; ``Registry.list()`` and attribute access are
    order-independent, so this matches the former definition order. Used for
    per-chip hardware data.
    """
    data_dir = Path(data_dir)
    entries: dict[str, Any] = {}
    for yaml_file in sorted(data_dir.glob("*.yaml")):
        raw = yaml.safe_load(yaml_file.read_text(encoding="utf-8"))
        entries[raw.pop("__key__", yaml_file.stem)] = raw
    return _build(entries, name=name, doc=doc, model_cls=model_cls, type_map=type_map, tech_root=tech_root)


def load_collection(yaml_file, model_cls=None, *, name: str, doc: str = "",
                    tech_root: Any = None, type_map: dict | None = None) -> type:
    """Build a ``Registry`` subclass from a single per-category YAML file.

    The file is a mapping ``{attr_name: entry_dict}``; each entry validates into
    ``model_cls`` (or its ``__type__`` from ``type_map`` for polymorphic
    schemas). Used for per-category model data, where the cohesive set is more
    useful read together than split across files.
    """
    raw = yaml.safe_load(Path(yaml_file).read_text(encoding="utf-8"))
    return _build(raw, name=name, doc=doc, model_cls=model_cls, type_map=type_map, tech_root=tech_root)
