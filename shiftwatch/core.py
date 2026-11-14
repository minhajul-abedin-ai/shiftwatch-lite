"""Distribution drift monitoring with fixed reference quantile bins.

Metrics are descriptive and are not statistical hypothesis tests.
"""
import math
from bisect import bisect_right


def _clean(values):
    if not isinstance(values, (list, tuple)):
        values = list(values)
    out = []
    for x in values:
        if isinstance(x, bool) or not isinstance(x, (int, float)):
            raise ValueError('All observations must be finite numeric values (excluding booleans)')
        try:
            numeric = float(x)
        except (OverflowError, ValueError):
            raise ValueError('All observations must be finite numeric values (excluding booleans)') from None
        if not math.isfinite(numeric):
            raise ValueError('All observations must be finite numeric values (excluding booleans)')
        out.append(numeric)
    if not out:
        raise ValueError('At least one observation is required')
    return out


def _bins(reference, n_bins):
    if not isinstance(n_bins, int) or isinstance(n_bins, bool) or n_bins < 2:
        raise ValueError('n_bins must be an integer >= 2')
    sorted_ref = sorted(reference)
    edges = []
    for i in range(1, n_bins):
        pos = i * (len(sorted_ref) - 1) / n_bins
        low = int(pos)
        frac = pos - low
        edge = sorted_ref[low] * (1-frac) + sorted_ref[min(low+1, len(sorted_ref)-1)] * frac
        if not edges or edge > edges[-1]:
            edges.append(edge)
    return edges


def _distribution(values, edges):
    counts = [0] * (len(edges) + 1)
    for v in values:
        counts[bisect_right(edges, v)] += 1
    return [c / len(values) for c in counts]


def _smooth(probabilities, epsilon):
    if not 0 < epsilon < 1:
        raise ValueError('epsilon must be between 0 and 1')
    total = sum(p + epsilon for p in probabilities)
    return [(p + epsilon) / total for p in probabilities]


def psi(reference_probs, current_probs, epsilon=1e-6):
    """Population stability index using smoothed, normalized probabilities."""
    if len(reference_probs) != len(current_probs) or not reference_probs:
        raise ValueError('Probability vectors must have the same nonzero length')
    if any(not math.isfinite(p) or p < 0 for p in [*reference_probs, *current_probs]):
        raise ValueError('Probabilities must be finite and nonnegative')
    if sum(reference_probs) <= 0 or sum(current_probs) <= 0:
        raise ValueError('Each probability vector must have positive mass')
    a = _smooth([p/sum(reference_probs) for p in reference_probs], epsilon)
    b = _smooth([p/sum(current_probs) for p in current_probs], epsilon)
    return sum((x-y) * math.log(x/y) for x, y in zip(a,b))


def js_divergence(reference_probs, current_probs, epsilon=1e-6):
    """Jensen-Shannon divergence in nats (bounded by ln(2))."""
    if len(reference_probs) != len(current_probs) or not reference_probs:
        raise ValueError('Probability vectors must have the same nonzero length')
    if any(not math.isfinite(p) or p < 0 for p in [*reference_probs, *current_probs]):
        raise ValueError('Probabilities must be finite and nonnegative')
    if sum(reference_probs) <= 0 or sum(current_probs) <= 0:
        raise ValueError('Each probability vector must have positive mass')
    a = _smooth([p/sum(reference_probs) for p in reference_probs], epsilon)
    b = _smooth([p/sum(current_probs) for p in current_probs], epsilon)
    m = [(x+y)/2 for x,y in zip(a,b)]
    return sum((x*math.log(x/z)+y*math.log(y/z))/2 for x,y,z in zip(a,b,m))


def drift_report(reference, current, n_bins=10, epsilon=1e-6):
    """Compare numeric samples using reference-derived bin edges."""
    ref = _clean(reference)
    cur = _clean(current)
    edges = _bins(ref, n_bins)
    a = _distribution(ref, edges)
    b = _distribution(cur, edges)
    return {'reference_count':len(ref), 'current_count':len(cur),
            'requested_bins':n_bins, 'effective_bins':len(a), 'bin_edges':edges,
            'reference_proportions':a, 'current_proportions':b,
            'psi':psi(a,b,epsilon), 'js_divergence_nats':js_divergence(a,b,epsilon),
            'note':'Descriptive metrics only; thresholds require domain-specific validation.'}
