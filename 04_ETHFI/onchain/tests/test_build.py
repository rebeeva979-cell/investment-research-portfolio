"""Unit tests for the committed ETHFI build outputs (stdlib only)."""
from __future__ import annotations

import csv
import json
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
DATA = HERE / "data"
RAW = HERE / "raw"


def metrics() -> dict[str, float]:
    out = {}
    with (DATA / "ethfi_metrics.csv").open(encoding="utf-8", newline="") as fh:
        for r in csv.DictReader(fh):
            try:
                out[r["metric"]] = float(r["value"])
            except ValueError:
                pass
    return out


def metric_text(name: str) -> str:
    with (DATA / "ethfi_metrics.csv").open(encoding="utf-8", newline="") as fh:
        return {r["metric"]: r["value"] for r in csv.DictReader(fh)}[name]


class SupplyAndConcentration(unittest.TestCase):
    def setUp(self) -> None:
        self.m = metrics()

    def test_supply_reconciles_to_genesis(self) -> None:
        self.assertAlmostEqual(self.m["circulating_supply"], 998_535_999, places=0)
        self.assertAlmostEqual(self.m["burned_supply"], 1_464_001, places=0)
        self.assertAlmostEqual(
            self.m["circulating_supply"] + self.m["burned_supply"], 1_000_000_000, places=0
        )

    def test_concentration_is_ordered(self) -> None:
        values = [self.m[k] for k in (
            "top1_holder_share", "top5_holder_share", "top10_holder_share", "top20_holder_share"
        )]
        self.assertEqual(values, sorted(values))
        self.assertAlmostEqual(self.m["top10_holder_share"], 62.19, places=1)
        self.assertGreater(self.m["eoa_gini"], 0.7)

    def test_burn_is_not_a_dead_address(self) -> None:
        supply = json.loads((RAW / "rpc_supply.json").read_text())
        self.assertAlmostEqual(supply["total_supply_ethfi"], 998_535_999, places=0)


class Buyback(unittest.TestCase):
    def setUp(self) -> None:
        self.m = metrics()

    def test_buyback_totals(self) -> None:
        self.assertAlmostEqual(self.m["buyback_ethfi"], 2_542_499, delta=2)
        self.assertEqual(int(self.m["buyback_txs"]), 566)
        self.assertAlmostEqual(self.m["buyback_avg_price"], 0.6472, places=3)

    def test_buyback_vs_revenue_and_spot(self) -> None:
        self.assertAlmostEqual(self.m["buyback_30d_pct_revenue"], 17.3, places=1)
        self.assertAlmostEqual(self.m["buyback_mark_vs_spot_pct"], -27.9, places=1)
        self.assertGreater(self.m["buyback_avg_price"], self.m["price"])

    def test_daily_buybacks_sum_to_total(self) -> None:
        with (DATA / "ethfi_buybacks_daily.csv").open(encoding="utf-8", newline="") as fh:
            rows = list(csv.DictReader(fh))
        total = sum(float(r["ethfi_bought"]) for r in rows)
        self.assertAlmostEqual(total, self.m["buyback_ethfi"], delta=2)


class Economics(unittest.TestCase):
    def setUp(self) -> None:
        self.m = metrics()

    def test_holders_revenue_is_zero_recently(self) -> None:
        self.assertEqual(self.m["holders_revenue_30d"], 0)
        self.assertEqual(metric_text("holders_revenue_last_nonzero"), "2026-04-01")

    def test_valuation_multiples(self) -> None:
        self.assertAlmostEqual(self.m["mcap_revenue"], 10.73, places=1)
        self.assertAlmostEqual(self.m["mcap_tvl"], 0.125, places=2)
        self.assertAlmostEqual(self.m["tvl_drawdown_from_peak"], -70.86, places=1)

    def test_scenarios_are_sensitivity_not_targets(self) -> None:
        with (DATA / "ethfi_valuation_scenarios.csv").open(encoding="utf-8", newline="") as fh:
            rows = {r["scenario"]: r for r in csv.DictReader(fh)}
        self.assertEqual(list(rows), ["Bear", "Base", "Bull"])
        for row in rows.values():
            self.assertAlmostEqual(
                float(row["implied_mcap_usd"]),
                float(row["revenue_run_rate_usd"]) * float(row["multiple_x"]),
                delta=1,
            )
        self.assertLess(float(rows["Bear"]["implied_price_usd"]), float(rows["Bull"]["implied_price_usd"]))


if __name__ == "__main__":
    unittest.main(verbosity=2)
