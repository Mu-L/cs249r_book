"""Pedagogical provenance for book-aligned constants."""

from __future__ import annotations

from typing import Optional


class TraceableConstant(float):
    """
    A float that carries a human-readable source string for the textbook.

    Behaves as a plain float in arithmetic. The book appendix uses Quarto
    ``@citekey`` references separately; ``source`` here is for package audits
    and labs (paper title, datasheet name, URL, or "book convention").
    """

    def __new__(
        cls,
        value,
        name: str,
        description: str,
        source: str,
        url: Optional[str] = None,
    ):
        obj = super().__new__(cls, value)
        obj.name = name
        obj.description = description
        obj.source = source
        obj.url = url
        return obj

    def render_markdown(self) -> str:
        """Render as a markdown block for lab / appendix integration."""
        lines = [
            f"**Assumption: {self.name}** = `{float(self)}`",
            "",
            f"_{self.description}_",
            "",
        ]
        if self.url:
            lines.append(f"> **Source:** [{self.source}]({self.url})")
        else:
            lines.append(f"> **Source:** {self.source}")
        return "\n".join(lines)


_RELIABILITY_SOURCE = (
    "Kokolis et al. (2025, HPCA); Zu et al. (2024, NSDI); "
    "Barroso et al. (2019) — order-of-magnitude steady-state MTTF"
)
_RELIABILITY_URL = "https://doi.org/10.1109/hpca61900.2025.00096"


def fleet_mttf_hours(
    hours: float,
    *,
    component: str,
    failure_mode: str = "",
) -> TraceableConstant:
    """MTTF anchor aligned with appendix_reliability @tbl-component-fit."""
    desc = f"Steady-state MTTF for {component} in continuous datacenter operation."
    if failure_mode:
        desc += f" Typical mode: {failure_mode}."
    return TraceableConstant(
        hours,
        name=f"{component} MTTF (hours)",
        description=desc,
        source=_RELIABILITY_SOURCE,
        url=_RELIABILITY_URL,
    )
