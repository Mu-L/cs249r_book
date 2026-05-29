"""Native-only bootstrap for Marimo co-labs (not part of the mlsysim wheel).

WASM bootstrap (micropip.install) is handled inline in each lab's Cell 0
because marimo's html-wasm export bundles only the notebook .py file —
bootstrap.py is not available in the Pyodide virtual filesystem.
"""

from __future__ import annotations

import sys
from pathlib import Path


def _repo_root(lab_file: str) -> Path:
    return Path(lab_file).resolve().parents[2]


def native_bootstrap(lab_file: str) -> None:
    """Add repo root to sys.path for editable/local mlsysim imports."""
    if sys.platform == "emscripten" or "mlsysim" in sys.modules:
        return
    root = str(_repo_root(lab_file))
    if root not in sys.path:
        sys.path.insert(0, root)
