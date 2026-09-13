"""First adaptive planner: choose a valid execution strategy by estimated cost."""

from dataclasses import dataclass
from .cost_model import score


@dataclass(frozen=True)
class Plan:
    strategy: str
    estimated_bytes_moved: int
    estimated_compute_units: float
    estimated_score: float


def choose_plan(raw_bytes: int, matched_rows: int, row_bytes: int = 64) -> Plan:
    """Choose between raw transfer, filter pushdown, and aggregate pushdown.

    This is intentionally deterministic and explainable. A later milestone can
    replace the hand-written cost model with learned workload predictions.
    """
    candidates = [
        Plan("raw_transfer", raw_bytes, 0.0, score(raw_bytes, 0.0)),
        Plan("filter_pushdown", matched_rows * row_bytes, matched_rows * 0.5,
             score(matched_rows * row_bytes, matched_rows * 0.5)),
        Plan("aggregate_pushdown", 16, matched_rows * 1.0,
             score(16, matched_rows * 1.0)),
    ]
    return min(candidates, key=lambda p: p.estimated_score)
