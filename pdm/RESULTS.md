# PDM experiment results

## First real TCP experiment

A 100,000-row deterministic workload was sent through a real localhost TCP producer/consumer boundary. The query selected `country = Nigeria` and `year >= 2020`, producing 3,966 matching rows. Ten transfer runs were collected per strategy and median latency was used.

| Strategy | Payload | Wire bytes | Median latency |
|---|---:|---:|---:|
| Raw transfer | 3,383,263 B | 3,383,271 B | 5.768 ms |
| Filter pushdown | 140,157 B | 140,165 B | 0.243 ms |
| Projection pushdown | 27,345 B | 27,353 B | 0.132 ms |
| Aggregate pushdown | 24 B | 32 B | 0.107 ms |

The aggregate result matched the other strategies. Relative to raw transfer, the aggregate payload was reduced by **99.999291%** in this workload.

These are experimental localhost results, not cloud benchmarks. The first important result is that the cost of moving irrelevant data is large even in a simple controlled setup.

## What this does and does not prove

**It supports:** operation-aware data movement can drastically reduce bytes crossing a boundary for selective analytical workloads.

**It does not prove:** PDM is novel, that it beats production databases, or that the same percentages will occur over a real network. Existing systems already implement forms of predicate pushdown, projection pruning, aggregation pushdown and computational storage.

## Next experiment: find the boundary where PDM actually matters

Run a selectivity sweep from approximately 0%, 1%, 5%, 10%, 25%, 50%, 75% and 100% matching rows. Repeat with controlled latency/bandwidth conditions and compare PDM's planner prediction against measured transfer and execution cost. The goal is to identify workloads where an adaptive movement decision provides a measurable advantage over a fixed pushdown strategy.

## Reproducibility

Raw measurements are stored in `results/tcp_baseline_100k.json`. The benchmark implementation is `network_benchmark.py`.

## Research standard

No novelty or performance claim should be made from this experiment alone. Every claim must identify workload, baseline, environment, dataset size, repetition count and statistical method.
