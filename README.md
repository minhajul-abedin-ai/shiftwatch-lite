# ShiftWatch Lite

**Dependency-free distribution drift monitoring for numeric machine-learning data.** Compare training/reference samples with new data using Population Stability Index (PSI) and Jensen–Shannon divergence (JSD).

[![Tests](https://github.com/minhajul-abedin-ai/shiftwatch-lite/actions/workflows/tests.yml/badge.svg)](https://github.com/minhajul-abedin-ai/shiftwatch-lite/actions/workflows/tests.yml)

## Features
- Reference-quantile binning with deterministic handling of ties
- PSI and Jensen–Shannon divergence (in nats)
- JSON output suitable for ML monitoring pipelines
- Standard-library-only Python package and CLI
- Synthetic electricity-demand CSV example and unit tests

## Quick start

Requires Python 3.10+; **no external dependencies**.

```bash
git clone https://github.com/minhajul-abedin-ai/shiftwatch-lite.git
cd shiftwatch-lite
python -m shiftwatch examples/reference.csv examples/current.csv --column demand --bins 4
python -m unittest discover -s tests -v
```

Python API:
```python
from shiftwatch import drift_report
report = drift_report([10, 11, 12, 13], [11, 13, 15, 17], n_bins=3)
print(report["psi"], report["js_divergence_nats"])
```

## Method and limitations
Reference quantile edges are fixed before evaluating the current sample. Repeated edges are deduplicated; values outside the reference range fall in the first/last bin. Probabilities use small smoothing to avoid log(0). JSD lies between 0 and ln(2).

**These are descriptive statistics, not statistical significance tests or proof of model degradation.** No universal alert threshold is valid across datasets. This initial version handles finite numeric values only; it does not implement streaming storage, missing-value imputation, categorical features or conformal prediction.

## Research connection
Distribution-shift monitoring is relevant to electricity-demand forecasting and model reliability. The included demand data is **synthetic**, not a published research result. This utility does not reproduce or claim results from any manuscript.

## Project structure
- `shiftwatch/`: package and CLI
- `tests/`: six unit tests
- `examples/`: synthetic CSV examples
- `.github/workflows/tests.yml`: GitHub Actions CI

## License
MIT. Contributions and reproducible bug reports are welcome.
