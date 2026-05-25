# LEGO Cell Contract

Inline `{python}` cells in MLSysBook chapters follow a **LEGO** pattern: a small
class computes scenario values once, exports formatted `*_str` fields, and prose
references them with `` `{python} Class.field_str` ``.

This document defines how to author and review LEGO cells. It complements the
fmt/notation audit lane (`book/tools/audit/fmt/README.md`) and pre-commit checks
(`lego-dead-code`, `./book/binder check math --scope canonical`).

## Core rule

**One cell ≈ one narrative anchor** — a callout, table, or tight paragraph
cluster. Place the cell **immediately above** the first `{python}` reference that
uses its exports.

## Cell contract

Each LEGO cell should include:

1. **Header comment** — Context (section/callout ID), Goal, Show, How, Imports,
   Exports (only fields used nearby).
2. **Class name** — Scenario-specific (`Gpt4ClusterMtbf`), not generic (`Calc`).
3. **Four blocks** (when applicable): LOAD → EXECUTE → GUARD → OUTPUT.
4. **Exports** — Formatted strings (`*_str`) via `fmt()`, `fmt_int()`, or
   `fmt_sci()`; units belong in prose or suffix kwargs, not duplicated in every
   export name.

Example shape:

````markdown
```{python}
#| echo: false
# ┌── LEGO ───────────────────────────────────────────────
# │ Goal: A100 ridge point for the latency callout below.
# │ Exports: A100RidgeExample.ridge_str
class A100RidgeExample:
    ridge = Hardware.Cloud.A100.ridge_fp16
    ridge_str = fmt_int(round(ridge.magnitude), commas=False)
```

The A100 ridge is `{python} A100RidgeExample.ridge_str` FLOP/byte.
````

## Do

- Keep **≤ 5–8 exports** per cell when possible.
- Use **registry paths** for shared specs — `Hardware.Cloud.H100`, `Models.Vision.ResNet50`,
  `Systems.Reliability.Gpu.mttf_hours`, `Literature.Training.MfuHigh`, and
  `mlsysim.physics.calc_*` for architecture formulas. Reserve `mlsysim.core.constants`
  for physics/units only (`HOURS_PER_DAY`, `BYTES_FP16`, latency stack).
- Put `#| echo: false` as the **first line** after ` ```{python}` (required by
  `book-check-code`).
- Use **`fmt_int(round(x))`** for computed integers; **`precision=0`** only when
  the value is already integer-like at the source.

## Don't

- **Mega-classes** — one class whose exports appear in multiple distant sections
  or unrelated callouts (anti-pattern: `TrainingDimensions` spanning forward-pass
  prose and a wave-quantization table hundreds of lines apart).
- **Cross-cell reads** — a later cell referencing `OtherClass.some_str` without
  redefining inputs in the same cell (hidden exec-order dependency).
- **Duplicate classes** — two cells for the same story (e.g. separate table and
  prose calcs for one latency budget); merge or split by narrative beat, not by
  output type.
- **Kitchen-sink exports** — header lists ten fields used once each across the
  chapter; split by callout instead.

## Review checklist

When editing or auditing a chapter:

| Check | Question |
|-------|----------|
| Locality | Is the cell within ~50–100 lines of the first ref? |
| Span | Do all exports appear in the same callout / `##` section? |
| Coupling | Does any other cell read this class's attributes? |
| Dead code | Does `lego-dead-code` report unused exports? |
| Fmt | Do prose preview + canonical audit pass (`fmt/` workflow)? |

## Migration (existing chapters)

Do **not** big-bang refactor large chapters. When a file is already open for
copyedit, fact-check, or fmt audit:

1. Split the mega-class at callout boundaries.
2. Rename classes to match the narrative beat.
3. Inline duplicated constants from `mlsysim` where it reduces drift.
4. Re-run `fmt/audit_prose.py` and `./book/binder check math --scope canonical` on that chapter.

Future optional lints (`lego-locality`, `lego-span`, `lego-cross-ref`) may
automate the checklist; until then, apply this contract in review.

## Related

- `book/tools/audit/fmt/README.md` — spurious `.0` / fmt precision workflow
- `./book/binder check math --scope canonical` — static fmt and suffix lint
- `./book/binder check refs --scope inline-python` — chapter exec validation
- `book/tools/audit/book_check_registry_sources.py` — legacy alias / constant import gate
- `mlsysim/tests/test_constants_allowlist.py` — CI lock on `constants.py` surface
