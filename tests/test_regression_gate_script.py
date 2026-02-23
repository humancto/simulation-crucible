"""Tests for scripts/regression_gate.py."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "regression_gate.py"
SUMMARY_SCRIPT = ROOT / "scripts" / "summarize_results.py"


def run_gate(args):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_regression_gate_passes_with_satisfied_thresholds(tmp_path):
    summary_file = tmp_path / "summary.json"
    baseline_file = tmp_path / "baseline.json"

    summary_file.write_text(
        json.dumps(
            {
                "schema_version": "race_summary_v1",
                "group_by": ["simulation", "variant", "agent_type"],
                "rows": [
                    {
                        "group": {
                            "simulation": "prisoners_dilemma",
                            "variant": "hard_rules",
                            "agent_type": "codex",
                        },
                        "metric": "composite_score",
                        "n": 5,
                        "seed_count": 5,
                        "mean": 41.2,
                        "stddev": 2.0,
                        "ci95": 1.75,
                        "min": 38.0,
                        "max": 44.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    baseline_file.write_text(
        json.dumps(
            {
                "schema_version": "regression_gate_v1",
                "metric": "composite_score",
                "rules": [
                    {
                        "name": "ipd-hard-codex",
                        "match": {
                            "simulation": "prisoners_dilemma",
                            "variant": "hard_rules",
                            "agent_type": "codex",
                        },
                        "min_runs": 3,
                        "min_seed_count": 3,
                        "min_mean": 40.0,
                        "max_ci95": 2.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    code, stdout, stderr = run_gate(
        ["--summary-file", str(summary_file), "--baseline-file", str(baseline_file)]
    )
    assert code == 0, stderr
    assert "PASS: ipd-hard-codex" in stdout
    assert "Regression gate passed." in stdout


def test_regression_gate_fails_on_mean_drop(tmp_path):
    summary_file = tmp_path / "summary.json"
    baseline_file = tmp_path / "baseline.json"

    summary_file.write_text(
        json.dumps(
            {
                "schema_version": "race_summary_v1",
                "group_by": ["simulation", "variant", "agent_type"],
                "rows": [
                    {
                        "group": {
                            "simulation": "prisoners_dilemma",
                            "variant": "hard_rules",
                            "agent_type": "codex",
                        },
                        "metric": "composite_score",
                        "n": 5,
                        "seed_count": 5,
                        "mean": 41.2,
                        "stddev": 2.0,
                        "ci95": 1.75,
                        "min": 38.0,
                        "max": 44.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    baseline_file.write_text(
        json.dumps(
            {
                "schema_version": "regression_gate_v1",
                "metric": "composite_score",
                "rules": [
                    {
                        "name": "ipd-hard-codex",
                        "match": {
                            "simulation": "prisoners_dilemma",
                            "variant": "hard_rules",
                            "agent_type": "codex",
                        },
                        "min_runs": 3,
                        "min_mean": 45.0,
                    }
                ],
            }
        ),
        encoding="utf-8",
    )

    code, stdout, stderr = run_gate(
        ["--summary-file", str(summary_file), "--baseline-file", str(baseline_file)]
    )
    assert code == 1, stderr
    assert "FAIL: ipd-hard-codex" in stdout
    assert "min_mean" in stdout
    assert "Regression gate failed with 1 failing rule(s)." in stdout


def test_smoke_baseline_passes_for_committed_smoke_artifacts(tmp_path):
    summary_file = tmp_path / "smoke_summary.json"

    summarize = subprocess.run(
        [
            sys.executable,
            str(SUMMARY_SCRIPT),
            "--results-file",
            "results/smoke_interest_ipd_unconstrained_codex.json",
            "--results-file",
            "results/smoke_interest_ipd_soft_guidelines_codex.json",
            "--results-file",
            "results/smoke_interest_ipd_hard_rules_codex.json",
            "--results-file",
            "results/smoke_random_pollution_prosperity_codex.json",
            "--metric",
            "composite_score",
            "--group-by",
            "simulation,variant,agent_type",
            "--output",
            str(summary_file),
            "--quiet",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert summarize.returncode == 0, summarize.stderr

    gate = subprocess.run(
        [
            sys.executable,
            str(SCRIPT),
            "--summary-file",
            str(summary_file),
            "--baseline-file",
            "benchmarks/smoke_regression_baseline_v1.json",
        ],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    assert gate.returncode == 0, gate.stderr
    assert "Regression gate passed." in gate.stdout
