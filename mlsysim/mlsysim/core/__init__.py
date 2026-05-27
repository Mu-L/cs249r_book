# mlsysim.core — Constants and Analytical Solvers

from . import constants
from . import config
from . import evaluation
from .constants import ureg, Q_

# Sibling registries available via lazy __getattr__ to avoid circular
# imports on Python <3.12 (core importing siblings during mlsysim init).
def __getattr__(name):
    _lazy = {
        "Hardware": ("mlsysim.hardware.registry", "Hardware"),
        "Models": ("mlsysim.models.registry", "Models"),
        "Platforms": ("mlsysim.platforms.registry", "Platforms"),
        "Systems": ("mlsysim.systems.registry", "Systems"),
        "Infrastructure": ("mlsysim.infra.registry", "Infrastructure"),
    }
    if name in _lazy:
        import importlib
        mod_path, attr = _lazy[name]
        mod = importlib.import_module(mod_path)
        val = getattr(mod, attr)
        globals()[name] = val
        return val
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

from .scenarios import Scenario, Scenarios, Applications, Fleet
from .resolver_factory import ResolverFactory
from .results import *
from .pipeline import Pipeline, CompositionError
from .walls import Domain, Wall, wall, walls_for_resolver, walls_in_domain, taxonomy
from . import calibration
