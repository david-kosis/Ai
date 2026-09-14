# PDM Engine

Precision Data Movement is now moving from a pure simulator toward a measurable producer/consumer data path.

## Modules

- `dataset.py` — deterministic synthetic data
- `operations.py` — filters, projection, aggregation
- `cost_model.py` — transfer/compute estimates
- `planner.py` — strategy selection
- `benchmark.py` — local simulated benchmark
- `network_benchmark.py` — real localhost TCP benchmark
- `transport.py` — length-prefixed TCP framing
- `experiment.py` — reproducible parameter sweep
- `cli.py` — command-line entry point

## Real-boundary experiment

Run from the repository root:

```bash
python -m pdm.network_benchmark --rows 10000 --country Nigeria --min-year 2020 --json
```

The benchmark creates a producer and consumer connected through a real TCP socket on localhost. It compares raw transfer, filter pushdown, projection pushdown, and aggregate pushdown while checking that every strategy returns the same result.

### What the numbers mean

- `payload_bytes`: application payload received by the consumer.
- `wire_bytes`: payload plus the benchmark's 8-byte frame header.
- `elapsed_ms`: client-side localhost transfer/receive time.
- `correct`: all strategies produced the same rounded result.

This is a controlled local experiment, **not** a claim about cloud/network performance. The next step is to repeat it across different selectivities and transport conditions, then compare the measured results with PDM's planner predictions.
