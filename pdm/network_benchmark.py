"""Measure real localhost TCP transfer for competing PDM strategies."""

import argparse
import json
import socket
import threading
import time
from dataclasses import asdict, dataclass

from .dataset import Row, generate_rows
from .operations import average, project_temperature, select
from .transport import receive_frame, send_frame


@dataclass(frozen=True)
class NetworkMeasurement:
    strategy: str
    payload_bytes: int
    wire_bytes: int
    elapsed_ms: float
    result: float


def _encode_rows(rows: list[Row]) -> bytes:
    # Compact deterministic text format. Field names are omitted deliberately so
    # this benchmark measures payload size rather than a schema-heavy format.
    lines = [f"{r.country}\t{r.year}\t{r.temperature}\t{r.rainfall}\t{r.population}" for r in rows]
    return ("\n".join(lines) + "\n").encode("utf-8")


def _decode_rows(payload: bytes) -> list[Row]:
    rows = []
    for line in payload.decode("utf-8").splitlines():
        country, year, temperature, rainfall, population = line.split("\t")
        rows.append(Row(country, int(year), float(temperature), float(rainfall), int(population)))
    return rows


def _encode_values(values: list[float]) -> bytes:
    return ("\n".join(str(v) for v in values) + "\n").encode("ascii")


def _encode_aggregate(values: list[float]) -> bytes:
    return f"{sum(values):.17g}\t{len(values)}\n".encode("ascii")


def _server(payload: bytes, ready: threading.Event, port_box: list[int]) -> None:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server.bind(("127.0.0.1", 0))
        server.listen(1)
        server.settimeout(10)
        port_box.append(server.getsockname()[1])
        ready.set()
        connection, _ = server.accept()
        with connection:
            connection.sendall(len(payload).to_bytes(8, "big"))
            connection.sendall(payload)


def _roundtrip(payload: bytes, decode) -> tuple[object, int, int, float]:
    ready = threading.Event()
    port_box: list[int] = []
    thread = threading.Thread(target=_server, args=(payload, ready, port_box), daemon=True)
    thread.start()
    ready.wait(2)
    if not port_box:
        raise RuntimeError("TCP server did not start")
    start = time.perf_counter()
    # The client uses the same framed protocol as send_frame, but the server
    # sends the frame so the benchmark measures a real producer -> consumer path.
    with socket.create_connection(("127.0.0.1", port_box[0]), timeout=10) as sock:
        data = receive_frame(sock)
    elapsed_ms = (time.perf_counter() - start) * 1000
    thread.join(timeout=2)
    return decode(data), len(data), len(data) + 8, elapsed_ms


def run(n: int = 100_000, country: str = "Nigeria", min_year: int = 2020) -> dict:
    rows = generate_rows(n)
    matched = select(rows, country=country, min_year=min_year)
    raw_payload = _encode_rows(rows)
    filtered_payload = _encode_rows(matched)
    values = project_temperature(matched)
    value_payload = _encode_values(values)
    aggregate_payload = _encode_aggregate(values)

    measurements = []
    decoded_rows, payload_bytes, wire_bytes, elapsed = _roundtrip(raw_payload, _decode_rows)
    raw_result = average(project_temperature(select(decoded_rows, country=country, min_year=min_year)))
    measurements.append(NetworkMeasurement("raw_transfer", payload_bytes, wire_bytes, round(elapsed, 3), round(raw_result, 6)))

    decoded_filtered, payload_bytes, wire_bytes, elapsed = _roundtrip(filtered_payload, _decode_rows)
    filtered_result = average(project_temperature(decoded_filtered))
    measurements.append(NetworkMeasurement("filter_pushdown", payload_bytes, wire_bytes, round(elapsed, 3), round(filtered_result, 6)))

    decoded_values, payload_bytes, wire_bytes, elapsed = _roundtrip(value_payload, lambda p: [float(x) for x in p.decode("ascii").splitlines()])
    value_result = average(decoded_values)
    measurements.append(NetworkMeasurement("projection_pushdown", payload_bytes, wire_bytes, round(elapsed, 3), round(value_result, 6)))

    (total, count), payload_bytes, wire_bytes, elapsed = _roundtrip(
        aggregate_payload,
        lambda p: (float(p.decode("ascii").split("\t")[0]), int(p.decode("ascii").split("\t")[1])),
    )
    aggregate_result = total / count
    measurements.append(NetworkMeasurement("aggregate_pushdown", payload_bytes, wire_bytes, round(elapsed, 3), round(aggregate_result, 6)))

    raw = measurements[0].payload_bytes
    selected = min(measurements, key=lambda item: item.payload_bytes)
    return {
        "config": {"rows": n, "country": country, "min_year": min_year},
        "matched_rows": len(matched),
        "measurements": [asdict(item) for item in measurements],
        "smallest_payload_strategy": selected.strategy,
        "payload_reduction_pct": round((1 - selected.payload_bytes / raw) * 100, 3),
        "correct": len({item.result for item in measurements}) == 1,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the real TCP PDM benchmark")
    parser.add_argument("--rows", type=int, default=100_000)
    parser.add_argument("--country", default="Nigeria")
    parser.add_argument("--min-year", type=int, default=2020)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    result = run(args.rows, args.country, args.min_year)
    print(json.dumps(result, indent=2) if args.json else result)
