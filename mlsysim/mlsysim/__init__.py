# mlsysim/__init__.py
"""
mlsysim: Machine Learning Systems Infrastructure and Modeling Platform
"""

__version__ = "0.1.2"

from . import core
from . import hardware
from . import models
# datasets deferred to __getattr__ (see below) to avoid circular import.
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
# Datasets loaded lazily via __getattr__ below.
from .systems.registry import Systems
from .infra.registry import Infrastructure
from .literature.registry import Literature
from .ops import Ops, Monitoring
from .core import calibration

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


def plot_roofline(*args, **kwargs):
    """Render a Roofline plot."""
    from .viz.plots import plot_roofline as _plot_roofline
    return _plot_roofline(*args, **kwargs)


_datasets_loading = False

def __getattr__(name):
    """Lazy import for datasets subpackage (circular import on Python <3.12)."""
    global _datasets_loading
    if name in ("datasets", "Datasets") and not _datasets_loading:
        _datasets_loading = True
        try:
            # Force-load the real datasets package now that __init__ is done.
            import importlib, importlib.util, sys
            spec = importlib.util.find_spec("mlsysim.datasets")
            if spec is None:
                # Fallback: construct spec from filesystem
                import pathlib
                ds_init = pathlib.Path(__file__).parent / "datasets" / "__init__.py"
                spec = importlib.util.spec_from_file_location(
                    "mlsysim.datasets", str(ds_init),
                    submodule_search_locations=[str(ds_init.parent)])
            _mod = importlib.util.module_from_spec(spec)
            sys.modules["mlsysim.datasets"] = _mod
            spec.loader.exec_module(_mod)
            _cls = _mod.Datasets
            globals()["datasets"] = _mod
            globals()["Datasets"] = _cls
            return _mod if name == "datasets" else _cls
        finally:
            _datasets_loading = False
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")


# Datasets in __all__ so `from mlsysim import *` picks it up.
__all__ = sorted(name for name in globals() if not name.startswith("_")) + ["Datasets"]
