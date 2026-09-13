# Precision Data Movement (PDM)

> An experimental data-plane engine for reducing unnecessary movement between storage, memory, network, and compute.

## Vision

PDM explores a simple question: **what is the smallest amount of information that must move for a computation to complete correctly?**

Instead of treating storage, networking, and compute as independent layers, PDM models them as one execution path and chooses among operations such as filtering, projection, aggregation, compression, caching, local computation, and raw transfer.

## Current status

🚧 Research prototype — early stage.

This repository is intentionally starting with a simulator and benchmark harness before any cloud or hardware integration.

## First milestone

Build a reproducible benchmark comparing:

1. raw data transfer;
2. filter/project before transfer;
3. aggregate before transfer;
4. compressed transfer;
5. an adaptive controller that selects the cheapest valid strategy.

### Metrics

- bytes transferred
- execution latency
- CPU time
- memory use
- estimated energy/cost
- correctness

## Architecture

```text
Application / Query
        |
        v
+----------------------+
| PDM Planner           |
| cost + workload model |
+----------+-----------+
           |
     +-----+-----+----------------+
     |           |                |
   Storage     Network          Compute
     |           |                |
     +-----------+----------------+
                 |
              Result
```

## Research rule

PDM is not claimed to be novel or patented. The project must be benchmarked against existing approaches and the technical contribution clearly defined before making novelty claims.

## Roadmap

- [x] Define research problem
- [ ] Build deterministic dataset generator
- [ ] Implement baseline transfer engine
- [ ] Implement predicate/projection pushdown
- [ ] Implement aggregation pushdown
- [ ] Implement cost model
- [ ] Implement adaptive planner
- [ ] Build benchmark suite
- [ ] Compare against baselines
- [ ] Identify measurable technical contribution
- [ ] Explore cloud/disaggregated deployment

## License

TBD during the research phase.
