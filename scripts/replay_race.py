#!/usr/bin/env python3
"""Replay a previously saved race result record."""

import argparse
import json
import shlex
import subprocess
import sys
from pathlib import Path


DURATION_KEYS = (
    "days",
    "hours",
    "weeks",
    "months",
    "quarters",
    "rounds",
    "sessions",
    "hands",
    "seasons",
    "years",
)


def load_records(path: Path) -> list[dict]:
    with path.open(encoding="utf-8") as f:
        data = json.load(f)
    if not isinstance(data, list):
        raise ValueError(f"Expected a JSON list in {path}")
    return data


def command_from_record(record: dict) -> list[str]:
    manifest = record.get("manifest") or {}
    manifest_argv = manifest.get("argv")
    if isinstance(manifest_argv, list) and manifest_argv:
        return [str(arg) for arg in manifest_argv]

    simulation = record.get("simulation")
    agents = record.get("agent_types") or record.get("agents") or []
    if not agents:
        raise ValueError("Race record is missing both agent_types and agents")

    cmd = ["run_race.py", "--agents", ",".join(agents)]

    if simulation:
        cmd.extend(["--simulation", str(simulation)])

    if record.get("seed") is not None:
        cmd.extend(["--seed", str(record["seed"])])

    variant = record.get("variant")
    if variant:
        cmd.extend(["--variant", str(variant)])

    for key in DURATION_KEYS:
        if key in record and record[key] is not None:
            cmd.extend([f"--{key}", str(record[key])])
            break

    return cmd


def main() -> int:
    repo_root = Path(__file__).resolve().parent.parent

    parser = argparse.ArgumentParser(
        description="Print or execute a replay command from a saved race result record."
    )
    parser.add_argument(
        "--results-file",
        default="results/race_results_v2.json",
        help="Path to results JSON list",
    )
    parser.add_argument(
        "--index",
        type=int,
        default=-1,
        help="Record index (default: -1 for latest)",
    )
    parser.add_argument(
        "--python",
        default="python3",
        help="Python executable to use for replay",
    )
    parser.add_argument(
        "--cwd",
        default=str(repo_root),
        help="Working directory for replay execution",
    )
    parser.add_argument(
        "--show-manifest",
        action="store_true",
        help="Print record manifest JSON (if present)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Execute the replay command",
    )
    args = parser.parse_args()

    results_path = Path(args.results_file)
    if not results_path.is_absolute():
        results_path = repo_root / results_path

    if not results_path.exists():
        raise SystemExit(f"Results file not found: {results_path}")

    records = load_records(results_path)
    if not records:
        raise SystemExit(f"No race records found in: {results_path}")

    try:
        record = records[args.index]
    except IndexError as exc:
        raise SystemExit(
            f"Record index {args.index} out of range for {len(records)} records"
        ) from exc

    cmd = command_from_record(record)
    replay_cmd = [args.python, *cmd]

    print(f"Results file: {results_path}")
    print(f"Record index: {args.index}")
    print("Replay command:")
    print(" ".join(shlex.quote(part) for part in replay_cmd))

    if args.show_manifest:
        print("\nManifest:")
        print(json.dumps(record.get("manifest", {}), indent=2))

    if not args.execute:
        return 0

    print("\nExecuting replay...")
    completed = subprocess.run(replay_cmd, cwd=args.cwd)
    return int(completed.returncode)


if __name__ == "__main__":
    sys.exit(main())
