# mlsysim/__init__.py
"""
mlsysim: Machine Learning Systems Infrastructure and Modeling Platform
"""

__version__ = "0.1.2"

from . import core
from . import hardware
from . import models
from . import datasets
from . import platforms
from . import infra
from . import systems
from . import sim
from . import physics

# AUTHORITATIVE API ENTRY POINTS
from .core.engine import Engine
from .core.scenarios import Scenario, Scenarios, Applications
from .hardware.registry import Hardware
from .models.registry import Models
from .platforms.registry import Platforms
from .datasets.registry import Datasets
from .systems.registry import Systems
from .infra.registry import Infrastructure

# AUTHORITATIVE SOLVERS
from .core.solver import (
    SingleNodeModel,
    DistributedModel,
    ReliabilityModel,
    SustainabilityModel,
    EconomicsModel,
    ServingModel,
    TrainingMemoryModel,
    ServingCapacityModel,
    DataModel,
    PlacementOptimizer,
)

# AUTHORITATIVE MEASUREMENT (UNITS)
from .core.constants import (
    ureg, Q_,
    # Common units
    byte, bit, second, ms, US, NS, hour, day, count,
    KB, MB, GB, TB, PB,
    Gbps,
    BYTES_FP32, BYTES_FP16, BYTES_INT8, BYTES_INT4, BYTES_INT32, BYTES_ADAM_STATE,
    flop, MFLOPs, GFLOPs, TFLOPs, PFLOPs, EFLOPs, ZFLOPs,
    watt, milliwatt, kilowatt,
    joule,
    # Common scaling constants
    THOUSAND, MILLION, BILLION, TRILLION,
    param, Kparam, Mparam, Bparam, Tparam,
    HOURS_PER_DAY,
)
from .core.defaults import CLOUD_ELECTRICITY_PER_KWH

GPT3_TRAINING_DAYS_REF = Models.Language.GPT3.training_days_ref
GPT3_TRAINING_ACCELERATORS_REF = Models.Language.GPT3.training_accelerators_ref

# AUTHORITATIVE FORMATTING
from .core.formulas import *
from .fmt import fmt, fmt_int, check, MarkdownStr

def plot_evaluation_scorecard(*args, **kwargs):
    """Render a system evaluation scorecard."""
    from .viz.plots import plot_evaluation_scorecard as _plot_evaluation_scorecard
    return _plot_evaluation_scorecard(*args, **kwargs)

def plot_roofline(*args, **kwargs):
    """Render a Roofline plot."""
    from .viz.plots import plot_roofline as _plot_roofline
    return _plot_roofline(*args, **kwargs)

__all__ = [
    # Core API
    "Engine", "Hardware", "Models", "Datasets", "Platforms", "Systems", "Infrastructure",
    "Scenario", "Scenarios", "Applications",
    "fmt", "fmt_int", "check", "MarkdownStr",
    # Solvers
    "SingleNodeModel", "DistributedModel", "ReliabilityModel",
    "SustainabilityModel", "EconomicsModel", "ServingModel",
    "TrainingMemoryModel", "ServingCapacityModel", "DataModel",
    "PlacementOptimizer",
    # Units
    "ureg", "Q_",
    "byte", "bit", "second", "ms", "US", "NS", "hour", "day", "count",
    "KB", "MB", "GB", "TB", "PB",
    "Gbps",
    "BYTES_FP32", "BYTES_FP16", "BYTES_INT8", "BYTES_INT4", "BYTES_INT32", "BYTES_ADAM_STATE",
    "flop", "MFLOPs", "GFLOPs", "TFLOPs", "PFLOPs", "EFLOPs", "ZFLOPs",
    "watt", "milliwatt", "kilowatt",
    "joule",
    "THOUSAND", "MILLION", "BILLION", "TRILLION",
    "param", "Kparam", "Mparam", "Bparam", "Tparam",
    "GPT3_TRAINING_DAYS_REF", "GPT3_TRAINING_ACCELERATORS_REF", "CLOUD_ELECTRICITY_PER_KWH",
    "HOURS_PER_DAY",
    # Viz
    "viz", "plot_evaluation_scorecard", "plot_roofline",
    # Internal Namespaces
    "core", "hardware", "models", "infra", "systems", "sim", "physics",
]
