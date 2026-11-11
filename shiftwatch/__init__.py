"""Dependency-free drift monitoring for numeric streams."""
from .core import drift_report, psi, js_divergence
__all__ = ['drift_report', 'psi', 'js_divergence']
