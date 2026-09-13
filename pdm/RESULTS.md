# PDM experiment protocol

## Goal

Measure whether moving computation toward the data can reduce the amount of information that must cross a storage/compute boundary while preserving the exact result.

## Strategies

- `raw_transfer`: transfer every row needed for the final calculation.
- `filter_pushdown`: apply the predicate before the transfer.
- `aggregate_pushdown`: compute the final aggregate at the data source and transfer only the aggregate state.
- `adaptive`: use the PDM planner to select a strategy from estimated transfer and compute costs.

## Important limitation

The current prototype is a **simulation**, not a distributed storage benchmark. `bytes_moved` represents the modeled payload crossing the boundary; it is not a measurement of real network traffic. Timing is local Python execution time and must not be interpreted as cloud performance.

## Next experiment

Add a real producer/consumer boundary with a local TCP transport. Measure serialized payload bytes, wall-clock latency, CPU time and correctness. Then compare against the simulated estimates.

## Research standard

No novelty or performance claim should be made from the simulator alone. Every claim must identify the workload, baseline, hardware/software environment, dataset size, and statistical method used.
