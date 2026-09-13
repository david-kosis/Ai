"""Simple transparent cost model for the first PDM benchmark."""

from dataclasses import dataclass


@dataclass(frozen=True)
class StrategyCost:
    name: str
    bytes_moved: int
    compute_units: float
    score: float


def score(bytes_moved: int, compute_units: float, transfer_weight: float = 1.0, compute_weight: float = 0.01) -> float:
    return bytes_moved * transfer_weight + compute_units * compute_weight
