"""CI gate: appendix assumption-table LEGO cells resolve against live registries."""

from __future__ import annotations

import importlib.util
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
GENERATOR = REPO_ROOT / "book/tools/audit/generate_appendix_constants.py"


def _load_generator():
    spec = importlib.util.spec_from_file_location("generate_appendix_constants", GENERATOR)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod


def test_appendix_lego_cells_verify():
    mod = _load_generator()
    results = mod.verify_all()
    assert results, "no appendix LEGO cells found"
    failed = [r for r in results if not r.ok]
    assert not failed, "\n".join(
        f"{r.path.name}:{r.label or r.class_name}: {r.error}" for r in failed
    )


def test_interconnect_registry_spec_resolves():
    mod = _load_generator()
    errors = mod.verify_interconnect_spec()
    assert not errors, "\n".join(errors)


def test_generate_appendix_constants_cli_verify():
    proc = subprocess.run(
        [sys.executable, str(GENERATOR), "--verify"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    assert proc.returncode == 0, proc.stdout + proc.stderr
