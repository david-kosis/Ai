"""Run a small parameter sweep and save reproducible PDM results."""

import argparse
import csv
from .benchmark import run


def main() -> None:
    parser = argparse.ArgumentParser(description="Run a PDM experiment sweep")
    parser.add_argument("--output", default="pdm/results.csv")
    parser.add_argument("--sizes", default="1000,10000,100000")
    args = parser.parse_args()

    rows = []
    for size in (int(x) for x in args.sizes.split(",")):
        result = run(size, "Nigeria", 2020)
        for measurement in result["measurements"]:
            rows.append({
                "rows": size,
                "strategy": measurement["strategy"],
                "matched_rows": measurement["matched_rows"],
                "bytes_moved": measurement["bytes_moved"],
                "elapsed_ms": measurement["elapsed_ms"],
                "result": measurement["result"],
                "correct": result["correct"],
                "selected_strategy": result["selected_strategy"],
            })

    with open(args.output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=rows[0].keys())
        writer.writeheader()
        writer.writerows(rows)
    print(f"wrote {len(rows)} measurements to {args.output}")


if __name__ == "__main__":
    main()
