#!/usr/bin/env python3
"""Fail fast when grouped benchmark summaries regress past configured thresholds."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any


def load_json(path: Path) -> Any:
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def matches_group(row: dict, match: dict) -> bool:
    group = row.get("group") or {}
    for key, expected in match.items():
        if group.get(key) != expected:
            return False
    return True


def rule_name(rule: dict) -> str:
    if isinstance(rule.get("name"), str) and rule["name"].strip():
        return rule["name"].strip()
    return json.dumps(rule.get("match", {}), sort_keys=True)


def evaluate_row_against_rule(row: dict, rule: dict, baseline_metric: str | None) -> list[str]:
    failures: list[str] = []

    row_metric = row.get("metric")
    expected_metric = rule.get("metric") or baseline_metric
    if expected_metric is not None and row_metric != expected_metric:
        failures.append(f"metric mismatch (expected {expected_metric}, got {row_metric})")

    min_runs = rule.get("min_runs")
    if isinstance(min_runs, int) and row.get("n", 0) < min_runs:
        failures.append(f"n={row.get('n')} < min_runs={min_runs}")

    min_seed_count = rule.get("min_seed_count")
    if isinstance(min_seed_count, int):
        seed_count = row.get("seed_count")
        if seed_count is None or seed_count < min_seed_count:
            failures.append(f"seed_count={seed_count} < min_seed_count={min_seed_count}")

    mean_value = row.get("mean")
    if isinstance(rule.get("min_mean"), (int, float)):
        if not isinstance(mean_value, (int, float)) or mean_value < float(rule["min_mean"]):
            failures.append(f"mean={mean_value} < min_mean={rule['min_mean']}")
    if isinstance(rule.get("max_mean"), (int, float)):
        if not isinstance(mean_value, (int, float)) or mean_value > float(rule["max_mean"]):
            failures.append(f"mean={mean_value} > max_mean={rule['max_mean']}")

    stddev = row.get("stddev")
    if isinstance(rule.get("max_stddev"), (int, float)):
        if not isinstance(stddev, (int, float)) or stddev > float(rule["max_stddev"]):
            failures.append(f"stddev={stddev} > max_stddev={rule['max_stddev']}")

    ci95 = row.get("ci95")
    if isinstance(rule.get("max_ci95"), (int, float)):
        if not isinstance(ci95, (int, float)):
            failures.append(f"ci95={ci95} missing for max_ci95={rule['max_ci95']}")
        elif ci95 > float(rule["max_ci95"]):
            failures.append(f"ci95={ci95} > max_ci95={rule['max_ci95']}")

    if bool(rule.get("require_ci95")) and ci95 is None:
        failures.append("ci95 missing but require_ci95=true")

    return failures


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Apply baseline threshold rules to a grouped summary JSON."
    )
    parser.add_argument(
        "--summary-file",
        required=True,
        help="Summary JSON produced by scripts/summarize_results.py",
    )
    parser.add_argument(
        "--baseline-file",
        required=True,
        help="Baseline rule JSON (schema: regression_gate_v1).",
    )
    args = parser.parse_args()

    summary_path = Path(args.summary_file)
    if not summary_path.is_absolute():
        summary_path = repo_root / summary_path
    baseline_path = Path(args.baseline_file)
    if not baseline_path.is_absolute():
        baseline_path = repo_root / baseline_path

    if not summary_path.exists():
        raise SystemExit(f"Summary file not found: {summary_path}")
    if not baseline_path.exists():
        raise SystemExit(f"Baseline file not found: {baseline_path}")

    summary = load_json(summary_path)
    baseline = load_json(baseline_path)

    rows = summary.get("rows")
    if not isinstance(rows, list):
        raise SystemExit(f"Invalid summary schema in {summary_path}: rows must be a list")

    rules = baseline.get("rules")
    if not isinstance(rules, list) or not rules:
        raise SystemExit(f"Invalid baseline schema in {baseline_path}: rules must be a non-empty list")

    baseline_metric = baseline.get("metric")
    total_failures = 0
    for rule in rules:
        if not isinstance(rule, dict):
            total_failures += 1
            print("FAIL: invalid rule entry (expected object)")
            continue
        if not isinstance(rule.get("match"), dict) or not rule["match"]:
            total_failures += 1
            print(f"FAIL: rule {rule_name(rule)} missing non-empty match block")
            continue

        matching_rows = [row for row in rows if isinstance(row, dict) and matches_group(row, rule["match"])]
        if not matching_rows:
            total_failures += 1
            print(f"FAIL: {rule_name(rule)} -> no summary row matched {rule['match']}")
            continue

        allow_multiple = bool(rule.get("allow_multiple"))
        if len(matching_rows) > 1 and not allow_multiple:
            total_failures += 1
            print(
                f"FAIL: {rule_name(rule)} -> matched {len(matching_rows)} rows; "
                "set allow_multiple=true or tighten match keys"
            )
            continue

        rule_failed = False
        for row in matching_rows:
            failures = evaluate_row_against_rule(row, rule, baseline_metric=baseline_metric)
            if failures:
                rule_failed = True
                group = row.get("group")
                print(f"FAIL: {rule_name(rule)} -> group={group}")
                for message in failures:
                    print(f"  - {message}")
        if rule_failed:
            total_failures += 1
        else:
            print(f"PASS: {rule_name(rule)}")

    if total_failures:
        print(f"\nRegression gate failed with {total_failures} failing rule(s).")
        return 1

    print("\nRegression gate passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
