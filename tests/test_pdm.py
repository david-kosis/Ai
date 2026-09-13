import unittest

from pdm.dataset import generate_rows
from pdm.operations import average, select
from pdm.planner import choose_plan


class PDMTests(unittest.TestCase):
    def test_dataset_is_deterministic(self):
        self.assertEqual(generate_rows(5), generate_rows(5))

    def test_filter(self):
        rows = generate_rows(100)
        matched = select(rows, country="Nigeria", min_year=2020)
        self.assertTrue(all(r.country == "Nigeria" and r.year >= 2020 for r in matched))

    def test_average(self):
        self.assertEqual(average([1.0, 2.0, 3.0]), 2.0)

    def test_planner_prefers_aggregate_for_large_reduction(self):
        plan = choose_plan(raw_bytes=6_400_000, matched_rows=10_000)
        self.assertEqual(plan.strategy, "aggregate_pushdown")


if __name__ == "__main__":
    unittest.main()
