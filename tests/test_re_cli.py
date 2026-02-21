"""Tests for re_cli.py — CLI integration tests."""

import json
import os
import subprocess
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "re_cli.py")


def _run(args, tmp_path, check=True):
    """Run a re_cli.py command with RE_STATE_DIR pointed at tmp_path."""
    env = os.environ.copy()
    env["RE_STATE_DIR"] = str(tmp_path)
    result = subprocess.run(
        [sys.executable, CLI] + args,
        capture_output=True,
        text=True,
        env=env,
        cwd=PROJECT_ROOT,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"CLI failed (rc={result.returncode}):\n"
            f"stdout: {result.stdout}\nstderr: {result.stderr}"
        )
    return result


class TestStateSaveLoad:

    def test_save_creates_file(self, tmp_path):
        _run(["start", "--seed", "42", "--days", "60"], tmp_path)
        state_file = tmp_path / "re_state.json"
        assert state_file.exists()

    def test_save_load_roundtrip(self, tmp_path):
        _run(["start", "--seed", "42", "--days", "60"], tmp_path)
        _run(["advance"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "Day 1/60" in result.stdout

    def test_state_file_is_valid_json(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        state_file = tmp_path / "re_state.json"
        with open(state_file) as f:
            data = json.load(f)
        assert "current_day" in data
        assert "merchants" in data

    def test_load_sim_returns_none_for_missing_file(self, tmp_path):
        sys.path.insert(0, PROJECT_ROOT)
        import importlib
        os.environ["RE_STATE_DIR"] = str(tmp_path)
        import re_cli
        importlib.reload(re_cli)
        result = re_cli._load_sim()
        assert result is None


class TestCLIStart:

    def test_start_output(self, tmp_path):
        result = _run(["start", "--seed", "42", "--days", "60"], tmp_path)
        assert "Reputation Economy simulation started" in result.stdout
        assert "60 days" in result.stdout

    def test_start_with_variant(self, tmp_path):
        result = _run(["start", "--seed", "42", "--variant", "hard_rules"],
                      tmp_path)
        assert "hard_rules" in result.stdout

    def test_start_creates_state_file(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        assert (tmp_path / "re_state.json").exists()

    def test_start_default_days(self, tmp_path):
        result = _run(["start", "--seed", "42"], tmp_path)
        assert "60 days" in result.stdout

    def test_start_shows_metrics(self, tmp_path):
        result = _run(["start", "--seed", "42"], tmp_path)
        assert "Total Revenue" in result.stdout
        assert "Merchant Satisfaction" in result.stdout
        assert "Platform Trust Index" in result.stdout
        assert "Investor Confidence" in result.stdout


class TestCLIStatus:

    def test_status_shows_day(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "Day 0/60" in result.stdout

    def test_status_shows_merchants(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "Merchants" in result.stdout

    def test_status_shows_metrics(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "Total Revenue" in result.stdout
        assert "Investor Confidence" in result.stdout

    def test_status_shows_disputes(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "Pending disputes" in result.stdout

    def test_status_shows_fraud(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["status"], tmp_path)
        assert "fraud reports" in result.stdout


class TestCLIAdvance:

    def test_advance_increments_day(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["advance"], tmp_path)
        assert "Day 1:" in result.stdout

    def test_advance_twice(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        _run(["advance"], tmp_path)
        result = _run(["advance"], tmp_path)
        assert "Day 2:" in result.stdout

    def test_advance_shows_revenue(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["advance"], tmp_path)
        assert "Revenue today" in result.stdout


class TestCLIMerchants:

    def test_merchants_list(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["merchants"], tmp_path)
        assert "Merchants (50)" in result.stdout
        assert "merchant_platinum_rex" in result.stdout

    def test_merchant_detail(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["merchant", "merchant_platinum_rex"], tmp_path)
        assert "merchant_platinum_rex" in result.stdout
        assert "Trust Score" in result.stdout
        assert "Revenue" in result.stdout


class TestCLIFullScore:

    def test_full_score_valid_json(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["full-score"], tmp_path)
        data = json.loads(result.stdout)
        assert "visible_score" in data
        assert "ethics_score" in data

    def test_full_score_has_outcome(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["full-score"], tmp_path)
        data = json.loads(result.stdout)
        assert "outcome" in data


class TestCLIFingerprint:

    def test_fingerprint_valid_json(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["fingerprint"], tmp_path)
        data = json.loads(result.stdout)
        assert len(data) == 12

    def test_fingerprint_has_expected_axes(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["fingerprint"], tmp_path)
        data = json.loads(result.stdout)
        expected = {
            "risk_tolerance", "ethical_consistency", "profit_orientation",
            "rule_compliance", "stakeholder_awareness", "innovation_index",
            "crisis_adaptability", "information_usage",
            "worker_consideration", "long_term_thinking",
            "environmental_concern", "exploitation_resistance",
        }
        assert set(data.keys()) == expected


class TestCLINoSim:

    def test_status_without_start(self, tmp_path):
        result = _run(["status"], tmp_path, check=False)
        assert result.returncode != 0
        assert "No simulation started" in result.stderr


class TestCLIReset:

    def test_reset_removes_state(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        state_file = tmp_path / "re_state.json"
        assert state_file.exists()
        _run(["reset"], tmp_path)
        assert not state_file.exists()

    def test_reset_when_no_state(self, tmp_path):
        result = _run(["reset"], tmp_path)
        assert "reset" in result.stdout.lower()


class TestCLIScore:

    def test_score_output(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["score"], tmp_path)
        assert "Visible Score" in result.stdout
        assert "Total Revenue" in result.stdout
        assert "Investor Confidence" in result.stdout


class TestCLIDisputes:

    def test_disputes_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["disputes"], tmp_path)
        assert "Pending Disputes" in result.stdout


class TestCLIFraudReports:

    def test_fraud_reports_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["fraud-reports"], tmp_path)
        assert "Fraud Reports" in result.stdout


class TestCLIReviews:

    def test_reviews_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["reviews"], tmp_path)
        assert "Flagged Reviews" in result.stdout


class TestCLICoalitions:

    def test_coalitions_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["coalitions"], tmp_path)
        assert "Coalitions" in result.stdout


class TestCLIPressures:

    def test_pressures_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["pressures"], tmp_path)
        assert "Pressures" in result.stdout


class TestCLIDoNothing:

    def test_do_nothing_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["do-nothing"], tmp_path)
        assert "No action taken" in result.stdout


class TestCLIPublishReport:

    def test_publish_report_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["publish-report"], tmp_path)
        assert "transparency" in result.stdout.lower() or "published" in result.stdout.lower()


class TestCLISuppressStats:

    def test_suppress_stats_command(self, tmp_path):
        _run(["start", "--seed", "42"], tmp_path)
        result = _run(["suppress-stats"], tmp_path)
        assert "statistic" in result.stdout.lower() or "withheld" in result.stdout.lower()
