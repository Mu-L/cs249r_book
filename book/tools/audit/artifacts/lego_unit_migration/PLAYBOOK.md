# LEGO Unit Migration Playbook

## Standard cell shape

```python
from mlsysim.core.constants import ureg
from mlsysim.fmt import fmt_qty, check

energy = 66 * ureg.millijoule
time = 1000 * ureg.millisecond
power = energy / time
check(power.to(ureg.mW).magnitude > 50, "pipeline power ~60–70 mW")
energy_str = fmt_qty(energy, ureg.millijoule, precision=0, commas=False)
time_str = fmt_qty(time, ureg.millisecond, precision=0, commas=False)
power_str = fmt_qty(power, ureg.mW, precision=0, commas=False)
```

Prose: `` `{python} Class.energy_str` / `{python} Class.time_str` = `{python} Class.power_str` `` — no trailing unit.

## Parallel workers (no JOURNAL/PLAYBOOK edits)

1. Gate one chapter; write only under `chapters/`:
   - `vol1_<name>.md` — gate log
   - `vol1_<name>_llm.json` — LLM report
   - `vol1_<name>.status.yaml` — sign-off record
2. Append lessons to `chapters/_lessons_pending.md` (one line each).
3. Commit **only** the chapter `.qmd` (+ optional `chapters/*` artifacts in same commit).
4. Maintainer runs `python3 book/tools/audit/sync_lego_journal.py` to refresh `JOURNAL.md`.

Multiple chapters can run in parallel; no file locks on shared journal.

## Lessons

- (batch-merged from `chapters/_lessons_pending.md`)
