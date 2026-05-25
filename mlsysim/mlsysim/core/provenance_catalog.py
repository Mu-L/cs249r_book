"""Shared provenance records (stable ids, single definition)."""

from __future__ import annotations

from .provenance import Provenance, ProvenanceKind

IEA_WEO_2023 = Provenance(
    id="prov:iea-weo-2023-carbon",
    kind=ProvenanceKind.INDUSTRY_REPORT,
    ref="IEA World Energy Outlook 2023 (rounded gCO2/kWh)",
    url="https://www.iea.org/reports/world-energy-outlook-2023",
    verified="2025-03-06",
)

UPTIME_PUE_2022 = Provenance(
    id="prov:uptime-pue-survey-2022",
    kind=ProvenanceKind.INDUSTRY_REPORT,
    ref="Uptime Institute Global Data Center Survey 2022",
    verified="2025-03-06",
)

BOOK_CLUSTER_TIERS = Provenance(
    id="prov:book-cluster-tier-convention",
    kind=ProvenanceKind.CONVENTION,
    ref="MLSysBook editorial cluster tiers (256 / 2k / 8k / 100k GPUs)",
    verified="2025-03-06",
)

RELIABILITY_MTTF_LITERATURE = Provenance(
    id="prov:reliability-mttf-literature",
    kind=ProvenanceKind.LITERATURE,
    ref=(
        "Kokolis et al. (2025, HPCA); Zu et al. (2024, NSDI); "
        "Barroso et al. (2019) — order-of-magnitude steady-state MTTF"
    ),
    url="https://doi.org/10.1109/hpca61900.2025.00096",
    verified="2025-03-06",
)

BOOK_ILLUSTRATIVE_IOWA_CARBON = Provenance(
    id="prov:book-illustrative-iowa-carbon",
    kind=ProvenanceKind.ILLUSTRATIVE,
    ref="MLSysBook illustrative high-carbon US grid contrast (not IEA country average)",
    verified="2025-03-06",
)
