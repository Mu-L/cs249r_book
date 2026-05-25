# scripts/

Utility scripts for auditing and maintaining the ML Systems textbook.

## Active scripts

| Script | Purpose |
|--------|---------|
| `figure_audit.py` | Multimodal figure audit via Gemini CLI (compares rendered images against QMD source prose, captions, alt-text). |
| `exec_analysis.py` | Execution analysis helper for mlsysim scenarios. |
| `exec_single.py` | Single-scenario execution runner. |
| `audit_blocks.py` | Audits code block structure across chapters. |
| `check_lego_vars.py` | Validates LEGO cell variable exports match inline refs. |
| `cross-references/` | Cross-reference audit tooling (see `cross-references/README.md`). |

## Prerequisites

- `figure_audit.py` requires the `gemini` CLI installed and authenticated.
- The figure audit assumes the rendered HTML book is available at `https://harvard-edge.github.io/cs249r_book_dev/`.

## Usage

Run from the repository root:

```bash
python3 scripts/figure_audit.py
python3 scripts/check_lego_vars.py
python3 scripts/cross-references/audit_crossrefs.py
```
