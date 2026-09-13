"""Baseline operations used by the PDM strategy simulator."""

from .dataset import Row


def select(rows: list[Row], country: str | None = None, min_year: int | None = None) -> list[Row]:
    return [
        row for row in rows
        if (country is None or row.country == country)
        and (min_year is None or row.year >= min_year)
    ]


def project_temperature(rows: list[Row]) -> list[float]:
    return [row.temperature for row in rows]


def average(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty sequence")
    return sum(values) / len(values)
