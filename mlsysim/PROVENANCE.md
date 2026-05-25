# MLSysIM provenance

Every **Tier A** number (registry entries and appendix-facing defaults) must
carry a `Provenance` record so values are never anonymous.

## Textbook safety model (defense in depth)

| Layer | What it catches | Enforcement |
|-------|-----------------|-------------|
| 1. **Registry provenance** | New GPU/model without `metadata.provenance` | `test_provenance_audit` |
| 2. **Kind rules** | `datasheet` without URL, `estimate` without `notes` | `audit_provenance` validator |
| 3. **Appendix lineage** | `defaults.FOO` in assumption tables without provenance | `audit_appendix_defaults` |
| 4. **LEGO execution** | Broken imports / wrong registry paths in QMD cells | `test_appendix_constants` |
| 5. **Book citations** | Missing `@citekey` in captions | Quarto pre-commit checks |
| 6. **Human review** | Wrong but “sourced” numbers | PR + catalog `verified` dates |

Provenance documents **claims**, not correctness. Layer 6 remains editorial.

## Tiers

| Tier | Where | Requirement |
|------|--------|-------------|
| A | Registries, appendix `defaults`, pint quantities in appendices | `Provenance` required (CI) |
| B | Derived scalars (e.g. Gbps ÷ 8) | `kind=derived` + `notes` |
| C | Engine heuristics | `# Source:` comment |
| D | `constants.py` units/physics | Module doc or catalog convention |

## `Provenance`

- `kind`: `datasheet` \| `literature` \| `industry_report` \| `convention` \| `estimate` \| `derived` \| `illustrative` \| `heuristic`
- `ref`: one-line human label (not a BibTeX key)
- `url`, `verified` (YYYY-MM-DD), `notes` optional
- `id`: stable slug when shared (`prov:…`)

## Book vs package

- **Book**: `@citekey` in QMD captions and provenance catalog tables.
- **Package**: `Provenance` + optional URL. No `.bib` in the wheel.
- **Appendix tables**: values from `defaults.*` / `Hardware.*` LEGO cells; every referenced `defaults.SYMBOL` must resolve via `TraceableConstant.provenance` or `appendix_lineage.QUANTITY_PROVENANCE`.

## Checks

```bash
# Full textbook gate (run before merging assumption/registry changes)
cd mlsysim && python -m mlsysim.tools.audit_provenance --scope textbook --strict

# Components
python -m mlsysim.tools.audit_provenance --scope all --strict
python -m pytest tests/test_provenance_audit.py tests/test_appendix_constants.py -q
```

## `Sourced` / `TraceableConstant`

Appendix LEGO cells use `float(defaults.X)` in math. `Sourced` and
`TraceableConstant` delegate to `.value` via `__float__` so prose calculations
stay unchanged.
