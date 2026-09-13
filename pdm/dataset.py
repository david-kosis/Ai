"""Deterministic synthetic datasets for PDM benchmarks."""

from dataclasses import dataclass
import random


@dataclass(frozen=True)
class Row:
    country: str
    year: int
    temperature: float
    rainfall: float
    population: int


def generate_rows(n: int, seed: int = 42) -> list[Row]:
    """Generate reproducible rows without external dependencies."""
    rng = random.Random(seed)
    countries = ("Nigeria", "Ghana", "Kenya", "Egypt", "Canada", "India")
    return [
        Row(
            country=rng.choice(countries),
            year=rng.randint(2000, 2025),
            temperature=round(rng.uniform(18.0, 38.0), 3),
            rainfall=round(rng.uniform(0.0, 3000.0), 2),
            population=rng.randint(100_000, 10_000_000),
        )
        for _ in range(n)
    ]
