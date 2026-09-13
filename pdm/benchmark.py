"""Reproducible first benchmark for PDM."""

import argparse
from .dataset import generate_rows
from .operations import select, project_temperature, average
from .planner import choose_plan


def run(n: int, country: str, min_year: int) -> dict:
    rows = generate_rows(n)
    matched = select(rows, country=country, min_year=min_year)
    values = project_temperature(matched)
    result = average(values)
    raw_bytes = n * 64
    plan = choose_plan(raw_bytes, len(matched))
    return {
        "rows": n,
        "matched_rows": len(matched),
        "result": round(result, 6),
        "raw_bytes": raw_bytes,
        "planned_strategy": plan.strategy,
        "estimated_bytes_moved": plan.estimated_bytes_moved,
        "estimated_compute_units": plan.estimated_compute_units,
        "estimated_score": round(plan.estimated_score, 4),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the PDM baseline benchmark")
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--country", default="Nigeria")
    parser.add_argument("--min-year", type=int, default=2020)
    args = parser.parse_args()
    for key, value in run(args.rows, args.country, args.min_year).items():
        print(f"{key}: {value}")


if __name__ == "__main__":
    main()
