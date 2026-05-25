# MLSysIM provenance

Every **Tier A** number (registry entries and appendix-facing defaults) must
carry a `Provenance` record so values are never anonymous.

## Tiers

| Tier | Where | Requirement |
|------|--------|-------------|
| A | `hardware/registry.py`, `models/registry.py`, appendix `defaults` | `Provenance` required (CI) |
| B | Derived scalars (e.g. Gbps ÷ 8) | `kind=derived` + `notes` |
| C | Engine heuristics | `# Source:` comment |
| D | `constants.py` units/physics | Module doc or catalog convention |

## `Provenance`

- `kind`: `datasheet` \| `literature` \| `industry_report` \| `convention` \| `estimate` \| `derived` \| `illustrative` \| `heuristic`
- `ref`: one-line human label (not a BibTeX key)
- `url`, `verified` (YYYY-MM-DD), `notes` optional
- `id`: stable slug when shared across constants (`prov:…`)

## Book vs package

- **Book**: `@citekey` in QMD captions and provenance catalog tables.
- **Package**: `Provenance` + optional URL for audits and labs. No `.bib` in the wheel.

## Checks

```bash
python -m mlsysim.tools.audit_provenance                      # traceable defaults (CI-safe)
python -m mlsysim.tools.audit_provenance --scope cloud        # Cloud hardware gaps
python -m mlsysim.tools.audit_provenance --scope all          # full gap report
python -m mlsysim.tools.audit_provenance --scope defaults --strict  # fail CI
```

## `Sourced` / `TraceableConstant`

Appendix LEGO cells use `float(defaults.X)` in math. `Sourced` and
`TraceableConstant` delegate to `.value` via `__float__` so prose calculations
stay unchanged.
