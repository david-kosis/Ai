# PDM Engine

The first implementation will be a local simulator. Keep the core independent from cloud providers and specialized hardware so benchmark results are reproducible.

## Planned modules

- `dataset.py` — deterministic synthetic data
- `operations.py` — filters, projection, aggregation, compression
- `cost_model.py` — transfer/compute/memory estimates
- `planner.py` — strategy selection
- `benchmark.py` — comparable experiments
- `cli.py` — command-line entry point

No external service is required for the first milestone.
