#!/usr/bin/env python3
"""Validate flow-polish worker YAML reports."""

from __future__ import annotations

import sys
from argparse import ArgumentParser
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover - environment guard
    raise SystemExit("PyYAML is required to validate flow-polish reports.") from exc


ROOT = Path(__file__).resolve().parents[4]
REPORT_DIR = Path(__file__).resolve().parent / "reports"
BOOK_DIR = ROOT / "book" / "quarto"
REQUIRED_TOP_LEVEL = {
    "schema_version",
    "report_kind",
    "qmd_path",
    "worker_id",
    "worker_status",
    "audit_scope",
    "checks",
    "edits",
    "residual_issues",
    "notes",
}
REQUIRED_SCOPE = {"assigned_file_only", "full_file_read", "allowed_edit_scope"}
REQUIRED_CHECKS = {
    "paragraph_flow",
    "section_transitions",
    "callout_leadins",
    "adjacent_callouts",
    "repeated_callout_titles",
    "italicized_transitions",
    "technical_meaning_preserved",
}
CHECK_STATUSES = {"pass", "fixed", "not_applicable", "needs_review"}
WORKER_STATUSES = {"edited", "reviewed_no_change", "blocked"}


def load_yaml(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        data = yaml.safe_load(handle)
    if not isinstance(data, dict):
        raise ValueError("top-level YAML value must be a mapping")
    return data


def validate_report(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        data = load_yaml(path)
    except Exception as exc:  # noqa: BLE001 - report validator should collect format errors
        return [f"{path}: {exc}"]

    missing = REQUIRED_TOP_LEVEL - data.keys()
    extra = data.keys() - REQUIRED_TOP_LEVEL
    if missing:
        errors.append(f"{path}: missing top-level fields: {', '.join(sorted(missing))}")
    if extra:
        errors.append(f"{path}: unknown top-level fields: {', '.join(sorted(extra))}")

    if data.get("schema_version") != 1:
        errors.append(f"{path}: schema_version must be 1")
    if data.get("report_kind") != "flow_polish_worker_report":
        errors.append(f"{path}: report_kind must be flow_polish_worker_report")
    if data.get("worker_status") not in WORKER_STATUSES:
        errors.append(f"{path}: worker_status must be one of {sorted(WORKER_STATUSES)}")

    qmd_path = data.get("qmd_path")
    if not isinstance(qmd_path, str) or not qmd_path.endswith(".qmd"):
        errors.append(f"{path}: qmd_path must be a repo-relative .qmd path")
    elif not (ROOT / qmd_path).exists():
        errors.append(f"{path}: qmd_path does not exist: {qmd_path}")

    scope = data.get("audit_scope")
    if not isinstance(scope, dict):
        errors.append(f"{path}: audit_scope must be a mapping")
    else:
        missing_scope = REQUIRED_SCOPE - scope.keys()
        extra_scope = scope.keys() - REQUIRED_SCOPE
        if missing_scope:
            errors.append(f"{path}: missing audit_scope fields: {', '.join(sorted(missing_scope))}")
        if extra_scope:
            errors.append(f"{path}: unknown audit_scope fields: {', '.join(sorted(extra_scope))}")
        if scope.get("assigned_file_only") is not True:
            errors.append(f"{path}: audit_scope.assigned_file_only must be true")
        if scope.get("full_file_read") is not True:
            errors.append(f"{path}: audit_scope.full_file_read must be true")

    checks = data.get("checks")
    if not isinstance(checks, dict):
        errors.append(f"{path}: checks must be a mapping")
    else:
        missing_checks = REQUIRED_CHECKS - checks.keys()
        extra_checks = checks.keys() - REQUIRED_CHECKS
        if missing_checks:
            errors.append(f"{path}: missing checks: {', '.join(sorted(missing_checks))}")
        if extra_checks:
            errors.append(f"{path}: unknown checks: {', '.join(sorted(extra_checks))}")
        for check_name, check in checks.items():
            if not isinstance(check, dict):
                errors.append(f"{path}: checks.{check_name} must be a mapping")
                continue
            if set(check.keys()) != {"status", "notes"}:
                errors.append(f"{path}: checks.{check_name} must contain only status and notes")
            if check.get("status") not in CHECK_STATUSES:
                errors.append(f"{path}: checks.{check_name}.status invalid: {check.get('status')!r}")
            if not isinstance(check.get("notes"), str):
                errors.append(f"{path}: checks.{check_name}.notes must be a string")

    for list_name in ("edits", "residual_issues"):
        value = data.get(list_name)
        if not isinstance(value, list):
            errors.append(f"{path}: {list_name} must be a sequence")
            continue
        for index, item in enumerate(value):
            if not isinstance(item, dict):
                errors.append(f"{path}: {list_name}[{index}] must be a mapping")

    if not isinstance(data.get("notes"), str):
        errors.append(f"{path}: notes must be a string")

    return errors


def expected_qmd_paths() -> set[str]:
    expected: set[str] = set()
    configs = [
        ("config/_quarto-pdf-vol1.yml", "book/quarto/index-vol1.qmd"),
        ("config/_quarto-pdf-vol2.yml", "book/quarto/index-vol2.qmd"),
    ]
    for config_path, index_path in configs:
        data = load_yaml(BOOK_DIR / config_path)
        book = data.get("book", {})
        for section_name in ("chapters", "appendices"):
            for rel_path in book.get(section_name, []):
                if rel_path == "index.qmd":
                    expected.add(index_path)
                elif isinstance(rel_path, str) and rel_path.endswith(".qmd"):
                    expected.add(f"book/quarto/{rel_path}")
    return expected


def main() -> int:
    parser = ArgumentParser(description=__doc__)
    parser.add_argument(
        "--require-all",
        action="store_true",
        help="also require one report for every QMD listed in the Volume I/II PDF configs",
    )
    args = parser.parse_args()

    report_paths = sorted(REPORT_DIR.glob("*.yml"))
    errors: list[str] = []
    reported_qmd_paths: dict[str, Path] = {}
    for report_path in report_paths:
        errors.extend(validate_report(report_path))
        try:
            data = load_yaml(report_path)
        except Exception:
            continue
        qmd_path = data.get("qmd_path")
        if isinstance(qmd_path, str):
            if qmd_path in reported_qmd_paths:
                errors.append(
                    f"{report_path}: duplicate qmd_path already reported by {reported_qmd_paths[qmd_path]}"
                )
            reported_qmd_paths[qmd_path] = report_path

    if args.require_all:
        expected = expected_qmd_paths()
        missing_reports = expected - reported_qmd_paths.keys()
        unexpected_reports = reported_qmd_paths.keys() - expected
        if missing_reports:
            errors.append(
                "missing reports for expected QMD paths:\n"
                + "\n".join(f"  - {path}" for path in sorted(missing_reports))
            )
        if unexpected_reports:
            errors.append(
                "reports exist for QMD paths outside the configured book order:\n"
                + "\n".join(f"  - {path}" for path in sorted(unexpected_reports))
            )

    if errors:
        print("\n".join(errors), file=sys.stderr)
        return 1

    suffix = " with complete configured-book coverage" if args.require_all else ""
    print(f"Validated {len(report_paths)} flow-polish report(s){suffix}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
