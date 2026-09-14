import unittest

from pdm.network_benchmark import run


class NetworkBenchmarkTests(unittest.TestCase):
    def test_tcp_strategies_preserve_result(self):
        result = run(2_000, "Nigeria", 2020)
        self.assertTrue(result["correct"])

    def test_pushdown_reduces_payload(self):
        result = run(2_000, "Nigeria", 2020)
        measurements = {m["strategy"]: m for m in result["measurements"]}
        self.assertLess(
            measurements["aggregate_pushdown"]["payload_bytes"],
            measurements["raw_transfer"]["payload_bytes"],
        )

    def test_wire_bytes_include_frame_header(self):
        result = run(100, "Nigeria", 2020)
        for measurement in result["measurements"]:
            self.assertEqual(measurement["wire_bytes"], measurement["payload_bytes"] + 8)


if __name__ == "__main__":
    unittest.main()
