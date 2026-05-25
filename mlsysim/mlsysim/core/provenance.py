"""Pedagogical provenance for book-aligned constants."""

from __future__ import annotations

from typing import Optional

# How a constant should be interpreted in the textbook appendix.
SOURCE_DATASHEET = "datasheet"
SOURCE_LITERATURE = "literature"
SOURCE_INDUSTRY_REPORT = "industry_report"
SOURCE_CONVENTION = "convention"
SOURCE_ILLUSTRATIVE = "illustrative"


class TraceableConstant(float):
    """
    A float that carries citation metadata for the MLSysBook assumptions appendix.

    Behaves as a plain float in arithmetic; exposes ``citation``, ``bib_keys``,
    ``source_type``, ``url``, and ``last_verified`` for rendering and audits.
    """

    def __new__(
        cls,
        value,
        name: str,
        description: str,
        citation: str,
        url: Optional[str] = None,
        *,
        source_type: str = SOURCE_LITERATURE,
        bib_keys: Optional[str] = None,
        last_verified: Optional[str] = None,
    ):
        obj = super().__new__(cls, value)
        obj.name = name
        obj.description = description
        obj.citation = citation
        obj.url = url
        obj.source_type = source_type
        obj.bib_keys = bib_keys
        obj.last_verified = last_verified
        return obj

    def render_markdown(self) -> str:
        """Render as a markdown block for lab / appendix integration."""
        lines = [
            f"**Assumption: {self.name}** = `{float(self)}`",
            "",
            f"_{self.description}_",
            "",
            f"> **Source type:** {self.source_type}",
        ]
        if self.bib_keys:
            lines.append(f"> **BibTeX keys:** `{self.bib_keys}`")
        if self.url:
            lines.append(f"> **Reference:** [{self.citation}]({self.url})")
        else:
            lines.append(f"> **Reference:** {self.citation}")
        if self.last_verified:
            lines.append(f"> **Last verified:** {self.last_verified}")
        return "\n".join(lines)


# Shared fleet-reliability provenance (order-of-magnitude MTTF tiers).
_RELIABILITY_BIB_KEYS = "kokolis2025; zu2024tpuv4; barroso2019"
_RELIABILITY_CITATION = "Kokolis et al. (2025); Zu et al. (2024); Barroso et al. (2019)"
_RELIABILITY_URL = "https://doi.org/10.1109/hpca61900.2025.00096"
_RELIABILITY_VERIFIED = "2025-03-06"


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
        citation=_RELIABILITY_CITATION,
        url=_RELIABILITY_URL,
        source_type=SOURCE_LITERATURE,
        bib_keys=_RELIABILITY_BIB_KEYS,
        last_verified=_RELIABILITY_VERIFIED,
    )
