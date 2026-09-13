"""Reproducible benchmark for PDM execution strategies."""

import argparse
import json
import time
from dataclasses import asdict, dataclass
from .dataset import generate_rows
from .operations import average, project_temperature, select
from .planner import choose_plan


@dataclass(frozen=True)
class Measurement:
    strategy: str
    rows: int
    matched_rows: int
    result: float
    bytes_moved: int
    elapsed_ms: float


def _measure(strategy: str, fn, bytes_moved: int, rows: int, matched_rows: int) -> Measurement:
    start = time.perf_counter()
    result = fn()
    elapsed_ms = (time.perf_counter() - start) * 1000
    return Measurement(strategy, rows, matched_rows, round(float(result), 6), bytes_moved, round(elapsed_ms, 3))


def run(n: int, country: str, min_year: int) -> dict:
    rows = generate_rows(n)
    matched = select(rows, country=country, min_year=min_year)
    raw_bytes = n * 64
    filtered_bytes = len(matched) * 64

    raw = _measure("raw_transfer", lambda: average(project_temperature(rows)), raw_bytes, n, len(matched))
    filtered = _measure("filter_pushdown", lambda: average(project_temperature(matched)), filtered_bytes, n, len(matched))
    aggregate = _measure("aggregate_pushdown", lambda: average(project_temperature(matched)), 16, n, len(matched))

    plan = choose_plan(raw_bytes, len(matched))
    measurements = [raw, filtered, aggregate]
    return {
        "config": {"rows": n, "country": country, "min_year": min_year},
        "measurements": [asdict(item) for item in measurements],
        "selected_strategy": plan.strategy,
        "selected_estimated_bytes": plan.estimated_bytes_moved,
        "raw_vs_selected_reduction_pct": round((1 - plan.estimated_bytes_moved / raw_bytes) * 100, 3),
        "correct": len({item.result for item in measurements}) == 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PDM benchmark")
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--country", default="Nigeria")
    parser.add_argument("--min-year", type=int, default=2020)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.rows, args.country, args.min_year)
    if args.json:
        print(json.dumps(result, indent=2))
    else:
        print(f"rows: {args.rows}")
        print(f"matched_rows: {result['measurements'][0]['matched_rows']}")
        for item in result["measurements"]:
            print(f"{item['strategy']}: {item['bytes_moved']} bytes, {item['elapsed_ms']} ms, result={item['result']}")
        print(f"selected_strategy: {result['selected_strategy']}")
        print(f"estimated_reduction: {result['raw_vs_selected_reduction_pct']}%")
        print(f"correct: {result['correct']}")


if __name__ == "__main__":
    main()
