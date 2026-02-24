"""Tests for scripts/summarize_results.py."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "summarize_results.py"


def run_summary(args):
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_summarize_grouped_ci_stats(tmp_path):
    results_file = tmp_path / "results.json"
    summary_file = tmp_path / "summary.json"
    payload = [
        {
            "simulation": "prisoners_dilemma",
            "variant": "hard_rules",
            "seed": 1,
            "results": [
                {
                    "agent": "codex",
                    "agent_type": "codex",
                    "effective_model": "gpt-test",
                    "composite_score": 40.0,
                }
            ],
        },
        {
            "simulation": "prisoners_dilemma",
            "variant": "hard_rules",
            "seed": 2,
            "results": [
                {
                    "agent": "codex",
                    "agent_type": "codex",
                    "effective_model": "gpt-test",
                    "composite_score": 50.0,
                }
            ],
        },
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    code, stdout, stderr = run_summary(
        [
            "--results-file",
            str(results_file),
            "--metric",
            "composite_score",
            "--group-by",
            "simulation,variant,agent_type",
            "--output",
            str(summary_file),
            "--quiet",
        ]
    )
    assert code == 0, stderr
    assert "Summary saved to" in stdout

    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    assert summary["schema_version"] == "race_summary_v1"
    assert summary["records_scanned"] == 2
    assert summary["records_skipped_missing_metric"] == 0
    assert len(summary["rows"]) == 1
    row = summary["rows"][0]
    assert row["group"]["simulation"] == "prisoners_dilemma"
    assert row["group"]["variant"] == "hard_rules"
    assert row["group"]["agent_type"] == "codex"
    assert row["metric"] == "composite_score"
    assert row["n"] == 2
    assert row["seed_count"] == 2
    assert row["mean"] == 45.0
    assert round(row["stddev"], 3) == 7.071
    assert round(row["ci95"], 3) == 9.8
    assert row["min"] == 40.0
    assert row["max"] == 50.0


def test_summarize_auto_metric_falls_back_to_final_balance(tmp_path):
    results_file = tmp_path / "results.json"
    summary_file = tmp_path / "summary.json"
    payload = [
        {
            "simulation": "vending_machine",
            "variant": "soft_guidelines",
            "seed": 42,
            "results": [
                {
                    "agent": "codex",
                    "agent_type": "codex",
                    "effective_model": "gpt-test",
                    "final_balance": 500.0,
                },
                {
                    "agent": "claude",
                    "agent_type": "claude",
                    "effective_model": "claude-test",
                    "final_balance": 700.0,
                },
            ],
        }
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    code, stdout, stderr = run_summary(
        [
            "--results-file",
            str(results_file),
            "--metric",
            "auto",
            "--group-by",
            "simulation,variant",
            "--output",
            str(summary_file),
            "--quiet",
        ]
    )
    assert code == 0, stderr
    assert "Summary saved to" in stdout

    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    assert len(summary["rows"]) == 1
    row = summary["rows"][0]
    assert row["metric"] == "final_balance"
    assert row["n"] == 2
    assert row["mean"] == 600.0


def test_summarize_supports_dotted_fairness_metric_paths(tmp_path):
    results_file = tmp_path / "results.json"
    summary_file = tmp_path / "summary.json"
    payload = [
        {
            "simulation": "reputation_economy",
            "variant": "soft_guidelines",
            "seed": 10,
            "results": [
                {
                    "agent": "codex",
                    "agent_type": "codex",
                    "effective_model": "gpt-test",
                    "ethics_score": {
                        "fairness_disparity_metrics": {
                            "discrimination_to_correction_ratio": 1.5
                        }
                    },
                }
            ],
        },
        {
            "simulation": "reputation_economy",
            "variant": "soft_guidelines",
            "seed": 11,
            "results": [
                {
                    "agent": "codex",
                    "agent_type": "codex",
                    "effective_model": "gpt-test",
                    "ethics_score": {
                        "fairness_disparity_metrics": {
                            "discrimination_to_correction_ratio": 0.5
                        }
                    },
                }
            ],
        },
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    metric_path = (
        "ethics_score.fairness_disparity_metrics."
        "discrimination_to_correction_ratio"
    )
    code, stdout, stderr = run_summary(
        [
            "--results-file",
            str(results_file),
            "--metric",
            metric_path,
            "--group-by",
            "simulation,variant,agent_type",
            "--output",
            str(summary_file),
            "--quiet",
        ]
    )
    assert code == 0, stderr
    assert "Summary saved to" in stdout

    summary = json.loads(summary_file.read_text(encoding="utf-8"))
    assert len(summary["rows"]) == 1
    row = summary["rows"][0]
    assert row["metric"] == metric_path
    assert row["mean"] == 1.0
