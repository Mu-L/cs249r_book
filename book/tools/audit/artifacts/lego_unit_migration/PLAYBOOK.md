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

## Lessons

- (updated per chapter)
