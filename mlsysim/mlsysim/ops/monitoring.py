"""MLOps monitoring thresholds (drift, stability)."""

from ..core.registry import Registry


class Monitoring(Registry):
    MemoryBitErrorRatePerBit = 1e-17
    KsTestCoefficient = 1.36
    PsiWarnThreshold = 0.10
    PsiReviewThreshold = 0.20
    PsiCriticalThreshold = 0.25
