#!/usr/bin/env python3
"""Aggregate race result artifacts into grouped statistical summaries."""

from __future__ import annotations

import argparse
import json
import math
import statistics
import time
from pathlib import Path
from typing import Any


AUTO_METRIC_PATHS = (
    "composite_score",
    "final_balance",
    "agent_score",
    "total_profit",
)


def parse_group_keys(raw: str) -> list[str]:
    keys = [key.strip() for key in raw.split(",") if key.strip()]
    if not keys:
        raise ValueError("group-by cannot be empty")
    return keys


def load_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        payload = json.load(f)
    if not isinstance(payload, list):
        raise ValueError(f"Expected JSON list in {path}")
    return [row for row in payload if isinstance(row, dict)]


def is_number(value: Any) -> bool:
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def get_by_path(obj: dict, dotted_path: str) -> Any:
    current: Any = obj
    for part in dotted_path.split("."):
        if not isinstance(current, dict):
            return None
        if part not in current:
            return None
        current = current[part]
    return current


def extract_metric_value(result_row: dict, record: dict, metric: str) -> tuple[str | None, float | None]:
    if metric == "auto":
        for candidate in AUTO_METRIC_PATHS:
            value = get_by_path(result_row, candidate)
            if is_number(value):
                return candidate, float(value)
        for candidate in AUTO_METRIC_PATHS:
            value = get_by_path(record, candidate)
            if is_number(value):
                return candidate, float(value)
        return None, None

    value = get_by_path(result_row, metric)
    if is_number(value):
        return metric, float(value)

    value = get_by_path(record, metric)
    if is_number(value):
        return metric, float(value)

    return None, None


def normalize_group_value(value: Any) -> Any:
    if isinstance(value, (dict, list, tuple)):
        return json.dumps(value, sort_keys=True)
    return value


def group_value(key: str, result_row: dict, record: dict) -> Any:
    if key in result_row:
        return normalize_group_value(result_row.get(key))
    if key in record:
        return normalize_group_value(record.get(key))
    if key == "effective_model":
        value = result_row.get("effective_model") or result_row.get("detected_model")
        return normalize_group_value(value)
    if key == "agent":
        return normalize_group_value(result_row.get("agent"))
    if key == "agent_type":
        return normalize_group_value(result_row.get("agent_type"))
    return None


def collect_samples(
    records: list[dict],
    metric: str,
    group_keys: list[str],
    source_label: str,
) -> tuple[list[dict], int, int]:
    samples: list[dict] = []
    scanned = 0
    skipped = 0

    for record in records:
        result_rows = record.get("results")
        if not isinstance(result_rows, list):
            continue
        for result_row in result_rows:
            if not isinstance(result_row, dict):
                continue
            scanned += 1
            resolved_metric, value = extract_metric_value(result_row, record, metric)
            if resolved_metric is None or value is None:
                skipped += 1
                continue
            group = {key: group_value(key, result_row, record) for key in group_keys}
            samples.append(
                {
                    "group": group,
                    "metric": resolved_metric,
                    "value": value,
                    "seed": record.get("seed"),
                    "source_file": source_label,
                }
            )

    return samples, scanned, skipped


def aggregate_samples(samples: list[dict], group_keys: list[str]) -> list[dict]:
    buckets: dict[tuple[Any, ...], dict] = {}
    for sample in samples:
        metric_name = sample["metric"]
        key = tuple(sample["group"].get(k) for k in group_keys) + (metric_name,)
        bucket = buckets.setdefault(
            key,
            {
                "group": sample["group"],
                "metric": metric_name,
                "values": [],
                "seeds": set(),
                "source_files": set(),
            },
        )
        bucket["values"].append(sample["value"])
        if sample["seed"] is not None:
            bucket["seeds"].add(sample["seed"])
        bucket["source_files"].add(sample["source_file"])

    rows: list[dict] = []
    for bucket in buckets.values():
        values = bucket["values"]
        n = len(values)
        mean_value = float(statistics.mean(values))
        stddev = float(statistics.stdev(values)) if n > 1 else 0.0
        ci95 = (1.96 * stddev / math.sqrt(n)) if n > 1 else None
        rows.append(
            {
                "group": bucket["group"],
                "metric": bucket["metric"],
                "n": n,
                "seed_count": len(bucket["seeds"]),
                "mean": mean_value,
                "stddev": stddev,
                "ci95": ci95,
                "min": float(min(values)),
                "max": float(max(values)),
                "source_files": sorted(bucket["source_files"]),
            }
        )

    rows.sort(
        key=lambda row: tuple(str(row["group"].get(key) or "") for key in group_keys)
        + (str(row["metric"]),)
    )
    return rows


def print_table(rows: list[dict], group_keys: list[str]) -> None:
    if not rows:
        print("No grouped rows to display.")
        return
    print("\nGrouped Summary")
    print("-" * 120)
    print(f"{'Group':<72} {'Metric':<20} {'N':>4} {'Mean':>10} {'CI95':>10} {'Min':>10} {'Max':>10}")
    print("-" * 120)
    for row in rows:
        group_label = ", ".join(f"{k}={row['group'].get(k)}" for k in group_keys)
        ci95 = f"{row['ci95']:.3f}" if row["ci95"] is not None else "n/a"
        print(
            f"{group_label[:72]:<72} {row['metric'][:20]:<20} {row['n']:>4} "
            f"{row['mean']:>10.3f} {ci95:>10} {row['min']:>10.3f} {row['max']:>10.3f}"
        )
    print("-" * 120)


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Aggregate race result JSON artifacts into grouped mean/std/95%% CI summaries."
    )
    parser.add_argument(
        "--results-file",
        action="append",
        required=True,
        help="Path to a race results JSON list (repeatable).",
    )
    parser.add_argument(
        "--metric",
        default="auto",
        help=(
            "Metric key to summarize (supports dotted paths like 'dimension_scores.fairness'). "
            "Use 'auto' to pick first available among composite_score/final_balance/agent_score/total_profit."
        ),
    )
    parser.add_argument(
        "--group-by",
        default="simulation,variant,agent_type,effective_model",
        help="Comma-separated group fields (default: simulation,variant,agent_type,effective_model).",
    )
    parser.add_argument("--output", help="Optional JSON output path for summary data.")
    parser.add_argument("--quiet", action="store_true", help="Suppress human-readable table output.")
    parser.add_argument("--print-json", action="store_true", help="Print JSON summary to stdout.")
    args = parser.parse_args()

    group_keys = parse_group_keys(args.group_by)

    samples: list[dict] = []
    scanned_total = 0
    skipped_total = 0
    source_files: list[str] = []

    for raw_path in args.results_file:
        path = Path(raw_path)
        if not path.is_absolute():
            path = repo_root / path
        if not path.exists():
            raise SystemExit(f"Results file not found: {path}")
        records = load_records(path)
        local_samples, scanned, skipped = collect_samples(
            records=records,
            metric=args.metric,
            group_keys=group_keys,
            source_label=str(path),
        )
        samples.extend(local_samples)
        scanned_total += scanned
        skipped_total += skipped
        source_files.append(str(path))

    rows = aggregate_samples(samples, group_keys)
    summary = {
        "schema_version": "race_summary_v1",
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "metric_requested": args.metric,
        "group_by": group_keys,
        "source_files": source_files,
        "records_scanned": scanned_total,
        "records_skipped_missing_metric": skipped_total,
        "rows": rows,
    }

    if args.output:
        output_path = Path(args.output)
        if not output_path.is_absolute():
            output_path = repo_root / output_path
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(summary, indent=2), encoding="utf-8")
        print(f"Summary saved to {output_path}")

    if not args.quiet:
        print_table(rows, group_keys)

    if args.print_json:
        print(json.dumps(summary, indent=2))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
