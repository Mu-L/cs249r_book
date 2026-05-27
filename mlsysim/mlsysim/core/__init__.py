# mlsysim.core — Constants and Analytical Solvers

from . import constants
from . import config
from . import evaluation
from .constants import ureg, Q_

# Lazy re-exports: avoid triggering sibling imports during mlsysim.__init__
# partial initialization (circular import on Python <3.12).
def __getattr__(name):
    _lazy = {
        "Hardware": "..hardware.registry",
        "Models": "..models.registry",
        "Platforms": "..platforms.registry",
        "Systems": "..systems.registry",
        "Infrastructure": "..infra.registry",
    }
    if name in _lazy:
        import importlib
        mod = importlib.import_module(_lazy[name], __name__)
        val = getattr(mod, name)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

from .scenarios import Scenario, Scenarios, Applications, Fleet
from .resolver_factory import ResolverFactory
from .results import *
from .pipeline import Pipeline, CompositionError
from .walls import Domain, Wall, wall, walls_for_resolver, walls_in_domain, taxonomy
from . import calibration
