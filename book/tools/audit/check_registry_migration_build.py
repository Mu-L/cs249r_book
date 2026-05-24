#!/usr/bin/env python3
"""Run end-to-end gates for the constants → registry migration build."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[3]
YAML_DIR = REPO_ROOT / "book/tools/audits/mlsysim_constants"


def _run(label: str, cmd: list[str], cwd: Path | None = None) -> None:
    print(f"\n== {label} ==")
    proc = subprocess.run(cmd, cwd=cwd or REPO_ROOT, text=True)
    if proc.returncode != 0:
        raise SystemExit(proc.returncode)


def _count_should_change() -> int:
    import yaml

    total = 0
    for path in YAML_DIR.glob("*.yaml"):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        for cell in data.get("python_cells") or []:
            for entry in cell.get("constants") or []:
                if entry.get("should_change") is True:
                    total += 1
    return total


def main() -> int:
    py = sys.executable
    _run(
        "mlsysim pytest (registry gates)",
        [py, "-m", "pytest", "tests/test_constants_allowlist.py",
         "tests/test_no_legacy_constant_refs.py", "tests/test_appendix_constants.py", "-q"],
        cwd=REPO_ROOT / "mlsysim",
    )
    _run("book registry source scan", [py, "book/tools/audit/book_check_registry_sources.py"])
    _run("appendix LEGO verify", [py, "book/tools/audit/generate_appendix_constants.py", "--verify"])
    _run("paper anchor validation", [py, "paper/scripts/validate_anchors.py"], cwd=REPO_ROOT / "mlsysim")

    pending = _count_should_change()
    print(f"\n== audit YAML should_change=true count: {pending} ==")
    if pending:
        print("Run: python3 book/tools/audit/refresh_mlsysim_constants_yamls.py --finalize")
        return 1

    print("\nRegistry migration build: ALL GATES GREEN")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
