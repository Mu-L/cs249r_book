"""Scenarios: real-world case studies and workload reference statistics.

This registry is the home for the book's recurring real-world reference figures —
illustrative scale anchors (Gmail volume, Waymo sensor rate) and case-study model
metrics (the TinyML anomaly detector). Every value carries sourced() provenance.

Note: *evaluatable* scenario bundles (workload + system + SLA, with .evaluate())
live in the Scenario model in core/scenarios.py. This registry is the
reference-statistics counterpart — sourced numbers the prose cites, not things to run.
"""
from ..core.provenance import sourced, sourced_qty
from ..core.registry import Registry
from ..core import provenance_catalog as pc
from ..core.units import ureg, TB

_hour = ureg.hour


class Workloads(Registry):
    """Illustrative real-world workload scale anchors (order-of-magnitude intuition)."""

    GmailEmailsPerDay = sourced(
        121e9, pc.BOOK_WORKLOAD_SCALE,
        name="Gmail emails per day", description="Approximate daily Gmail volume.")
    GoogleSearchesPerDay = sourced(
        8.5e9, pc.BOOK_WORKLOAD_SCALE,
        name="Google searches per day", description="Approximate daily Google search volume.")
    WaymoDataPerHourLow = sourced_qty(
        1 * TB / _hour, pc.BOOK_WORKLOAD_SCALE,
        name="Waymo sensor data rate (low)", description="Lower-bound AV sensor data generation rate.")
    WaymoDataPerHourHigh = sourced_qty(
        19 * TB / _hour, pc.BOOK_WORKLOAD_SCALE,
        name="Waymo sensor data rate (high)", description="Upper-bound AV sensor data generation rate.")


class AnomalyModel(Registry):
    """TinyML anomaly-detection case study (benchmarking example)."""

    Latency = sourced_qty(
        10.4 * ureg.ms, pc.BOOK_ANOMALY_CASE,
        name="Anomaly model latency", description="Inference latency of the TinyML anomaly detector.")
    Auc = sourced(
        0.86, pc.BOOK_ANOMALY_CASE,
        name="Anomaly model AUC", description="Area under the ROC curve for the TinyML anomaly detector.")
    Energy = sourced_qty(
        516 * ureg.microjoule, pc.BOOK_ANOMALY_CASE,
        name="Anomaly model energy", description="Per-inference energy of the TinyML anomaly detector.")


class Scenarios(Registry):
    """Registry namespace for real-world case studies and workload statistics."""

    Workloads = Workloads
    AnomalyModel = AnomalyModel
