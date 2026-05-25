"""Shared WASM/native bootstrap for Marimo co-labs (not part of the mlsysim wheel)."""

from __future__ import annotations

import sys
from pathlib import Path

_RUNTIME_PACKAGES = ("pydantic", "pint", "plotly", "pandas")


def _repo_root(lab_file: str) -> Path:
    return Path(lab_file).resolve().parents[2]


def wheel_relpath(lab_file: str) -> str:
    """Micropip wheel URL relative to labs/volN/."""
    try:
        import tomllib
    except ImportError:
        import tomli as tomllib

    version = tomllib.load(
        open(_repo_root(lab_file) / "mlsysim" / "pyproject.toml", "rb")
    )["project"]["version"]
    return f"../../wheels/mlsysim-{version}-py3-none-any.whl"


def native_bootstrap(lab_file: str) -> None:
    """Add repo root to sys.path for editable/local mlsysim imports."""
    if sys.platform == "emscripten" or "mlsysim" in sys.modules:
        return
    root = str(_repo_root(lab_file))
    if root not in sys.path:
        sys.path.insert(0, root)


async def setup_lab(lab_file: str) -> None:
    """Install runtime deps on WASM; ensure repo root is on sys.path natively."""
    if sys.platform == "emscripten":
        import micropip

        await micropip.install(list(_RUNTIME_PACKAGES), keep_going=False)
        await micropip.install(wheel_relpath(lab_file), keep_going=False)
    else:
        native_bootstrap(lab_file)
