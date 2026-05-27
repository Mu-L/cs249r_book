# mlsysim/__init__.py
"""
mlsysim: Machine Learning Systems Infrastructure and Modeling Platform
"""

__version__ = "0.1.2"

from . import core
from . import hardware
from . import models
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
from .systems.registry import Systems
from .infra.registry import Infrastructure
from .literature.registry import Literature
from .ops import Ops, Monitoring
from .core import calibration

# datasets.registry.Datasets is imported eagerly (needed for star import).
# The `datasets` MODULE import is lazy via __getattr__ to break a circular
# import chain on Python <3.12.
from .datasets.registry import Datasets

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

# AUTHORITATIVE MEASUREMENT (units + physics-only constants)
from .core.constants import *  # noqa: F401,F403

# AUTHORITATIVE PHYSICS FORMULAS
from .physics import *  # noqa: F401,F403

# AUTHORITATIVE FORMATTING
from .fmt import fmt, fmt_int, fmt_qty, check, MarkdownStr


def plot_evaluation_scorecard(*args, **kwargs):
    """Render a system evaluation scorecard."""
    from .viz.plots import plot_evaluation_scorecard as _plot_evaluation_scorecard
    return _plot_evaluation_scorecard(*args, **kwargs)


def __getattr__(name):
    """Lazy imports for modules that cause circular imports on Python <3.12."""
    if name == "datasets":
        from . import datasets as _datasets
        globals()["datasets"] = _datasets
        return _datasets
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


def plot_roofline(*args, **kwargs):
    """Render a Roofline plot."""
    from .viz.plots import plot_roofline as _plot_roofline
    return _plot_roofline(*args, **kwargs)


__all__ = sorted(name for name in globals() if not name.startswith("_"))
