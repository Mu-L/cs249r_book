"""MLOps assumption registries (monitoring thresholds, drift detection)."""

from ..core.registry import Registry
from .monitoring import Monitoring


class Ops(Registry):
    """Registry namespace for Ops."""
    Monitoring = Monitoring
