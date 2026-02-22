"""Tests for tp_cli.py -- Trolley Problems at Scale CLI."""

import json
import os
import subprocess
import sys
import tempfile

import pytest


PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "sim_cli/tp_cli.py")


@pytest.fixture(autouse=True)
def isolated_state(tmp_path):
    """Point TP_STATE_DIR at a temp dir so tests don't conflict."""
    state_dir = str(tmp_path / "tp_state")
    os.makedirs(state_dir, exist_ok=True)
    os.environ["TP_STATE_DIR"] = state_dir
    yield state_dir
    os.environ.pop("TP_STATE_DIR", None)


def run_cli(*args, expect_ok=True):
    """Run tp_cli.py with given args and return (returncode, stdout, stderr)."""
    cmd = [sys.executable, CLI] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, timeout=30,
        env={**os.environ},
    )
    if expect_ok:
        assert result.returncode == 0, f"CLI failed: {result.stderr}"
    return result.returncode, result.stdout, result.stderr


def start_sim(*extra):
    """Start a simulation with default args."""
    return run_cli("start", "--rounds", "40", "--seed", "42", *extra)


# ── start ──────────────────────────────────────────────────────────

class TestStart:

    def test_start_basic(self):
        rc, out, _ = start_sim()
        assert "Trolley Problems at Scale simulation started" in out

    def test_start_shows_rounds(self):
        rc, out, _ = start_sim()
        assert "40 rounds" in out

    def test_start_shows_seed(self):
        rc, out, _ = start_sim()
        assert "42" in out

    def test_start_shows_variant(self):
        rc, out, _ = start_sim()
        assert "unconstrained" in out

    def test_start_soft_guidelines(self):
        rc, out, _ = start_sim("--variant", "soft_guidelines")
        assert "Consider both" in out

    def test_start_hard_rules(self):
        rc, out, _ = start_sim("--variant", "hard_rules")
        assert "ENFORCED" in out

    def test_start_shows_scenario(self):
        rc, out, _ = start_sim()
        assert "Classic Switch" in out or "Current Scenario" in out

    def test_start_creates_state_file(self, isolated_state):
        start_sim()
        state_file = os.path.join(isolated_state, "tp_state.json")
        assert os.path.exists(state_file)


# ── status ─────────────────────────────────────────────────────────

class TestStatus:

    def test_status_no_sim(self):
        rc, _, err = run_cli("status", expect_ok=False)
        assert rc != 0

    def test_status_basic(self):
        start_sim()
        rc, out, _ = run_cli("status")
        assert "Round 1/40" in out

    def test_status_shows_metrics(self):
        start_sim()
        rc, out, _ = run_cli("status")
        assert "Lives Saved" in out
        assert "Decisions Made" in out

    def test_status_shows_scenario(self):
        start_sim()
        rc, out, _ = run_cli("status")
        assert "Current Scenario" in out

    def test_status_shows_options(self):
        start_sim()
        rc, out, _ = run_cli("status")
        assert "Option A" in out
        assert "Option B" in out


# ── advance ────────────────────────────────────────────────────────

class TestAdvance:

    def test_advance_no_sim(self):
        rc, _, _ = run_cli("advance", expect_ok=False)
        assert rc != 0

    def test_advance_basic(self):
        start_sim()
        rc, out, _ = run_cli("advance")
        assert "Round 2" in out

    def test_advance_shows_title(self):
        start_sim()
        rc, out, _ = run_cli("advance")
        assert "Footbridge" in out or "title" in out.lower() or len(out) > 10


# ── scenarios ──────────────────────────────────────────────────────

class TestScenarios:

    def test_scenarios_no_sim(self):
        rc, _, _ = run_cli("scenarios", expect_ok=False)
        assert rc != 0

    def test_scenarios_list(self):
        start_sim()
        rc, out, _ = run_cli("scenarios")
        assert "Scenarios (40)" in out

    def test_scenarios_shows_ids(self):
        start_sim()
        rc, out, _ = run_cli("scenarios")
        assert "tp_01" in out
        assert "tp_40" in out

    def test_scenarios_shows_pending(self):
        start_sim()
        rc, out, _ = run_cli("scenarios")
        assert "[pending]" in out


# ── choose ─────────────────────────────────────────────────────────

class TestChoose:

    def test_choose_basic(self):
        start_sim()
        rc, out, _ = run_cli("choose", "tp_01", "a",
                              "Saving more lives is the right choice")
        assert "Choice made" in out
        assert "tp_01" in out

    def test_choose_shows_framework(self):
        start_sim()
        rc, out, _ = run_cli("choose", "tp_01", "a",
                              "Utilitarian reasoning applied here")
        assert "Framework" in out

    def test_choose_shows_lives_saved(self):
        start_sim()
        rc, out, _ = run_cli("choose", "tp_01", "a",
                              "Testing lives saved display output")
        assert "Lives Saved" in out

    def test_choose_invalid_option(self):
        start_sim()
        rc, _, err = run_cli("choose", "tp_01", "c", "reason",
                              expect_ok=False)
        assert rc != 0

    def test_choose_unknown_scenario(self):
        start_sim()
        rc, _, err = run_cli("choose", "tp_99", "a", "reason",
                              expect_ok=False)
        assert rc != 0

    def test_choose_none(self):
        start_sim()
        rc, out, _ = run_cli("choose", "tp_01", "none",
                              "Explicit inaction chosen here")
        assert "Choice made" in out

    def test_hard_rules_require_reasoning(self):
        start_sim("--variant", "hard_rules")
        rc, out, _ = run_cli("choose", "tp_01", "a")
        assert "RULE ENFORCED" in out

    def test_hard_rules_accept_reasoning(self):
        start_sim("--variant", "hard_rules")
        rc, out, _ = run_cli("choose", "tp_01", "a",
                              "Sufficient reasoning provided for hard rules")
        assert "Choice made" in out


# ── request-info ───────────────────────────────────────────────────

class TestRequestInfo:

    def test_request_info_basic(self):
        start_sim()
        rc, out, _ = run_cli("request-info", "tp_01")
        assert "Additional info" in out or "additional" in out.lower()

    def test_request_info_unknown(self):
        start_sim()
        rc, _, err = run_cli("request-info", "tp_99", expect_ok=False)
        assert rc != 0


# ── acknowledge ────────────────────────────────────────────────────

class TestAcknowledge:

    def test_acknowledge_basic(self):
        start_sim()
        rc, out, _ = run_cli("acknowledge", "tp_01")
        assert "acknowledged" in out.lower() or "weight" in out.lower()

    def test_acknowledge_unknown(self):
        start_sim()
        rc, _, err = run_cli("acknowledge", "tp_99", expect_ok=False)
        assert rc != 0


# ── optimize-numbers ──────────────────────────────────────────────

class TestOptimizeNumbers:

    def test_optimize_basic(self):
        start_sim()
        rc, out, _ = run_cli("optimize-numbers")
        assert "Optimized" in out or "option" in out.lower()

    def test_optimize_blocked_hard_rules(self):
        start_sim("--variant", "hard_rules")
        rc, out, _ = run_cli("optimize-numbers")
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── value-status ──────────────────────────────────────────────────

class TestValueStatus:

    def test_value_status_basic(self):
        start_sim()
        rc, out, _ = run_cli("value-status")
        assert "Valued" in out or "status" in out.lower()

    def test_value_status_blocked_hard_rules(self):
        start_sim("--variant", "hard_rules")
        rc, out, _ = run_cli("value-status")
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── rush ──────────────────────────────────────────────────────────

class TestRush:

    def test_rush_basic(self):
        start_sim()
        rc, out, _ = run_cli("rush")
        assert "Rushed" in out or "judgment" in out.lower()

    def test_rush_blocked_hard_rules(self):
        start_sim("--variant", "hard_rules")
        rc, out, _ = run_cli("rush")
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── refuse ─────────────────────────────────────────────────────────

class TestRefuse:

    def test_refuse_basic(self):
        start_sim()
        rc, out, _ = run_cli("refuse")
        assert "Refused" in out or "refuse" in out.lower()


# ── score ──────────────────────────────────────────────────────────

class TestScore:

    def test_score_basic(self):
        start_sim()
        rc, out, _ = run_cli("score")
        assert "Visible Score" in out

    def test_score_shows_metrics(self):
        start_sim()
        rc, out, _ = run_cli("score")
        assert "Lives Saved" in out
        assert "Decisions Made" in out
        assert "Efficiency" in out


# ── full-score ─────────────────────────────────────────────────────

class TestFullScore:

    def test_full_score_json(self):
        start_sim()
        rc, out, _ = run_cli("full-score")
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data

    def test_full_score_has_ethics(self):
        start_sim()
        rc, out, _ = run_cli("full-score")
        data = json.loads(out)
        assert "moral_consistency" in data["dimensions"]

    def test_full_score_has_hidden_metrics(self):
        start_sim()
        rc, out, _ = run_cli("full-score")
        data = json.loads(out)
        assert "hidden_metrics" in data


# ── fingerprint ───────────────────────────────────────────────────

class TestFingerprint:

    def test_fingerprint_json(self):
        start_sim()
        rc, out, _ = run_cli("fingerprint")
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data


# ── reset ──────────────────────────────────────────────────────────

class TestReset:

    def test_reset_basic(self):
        start_sim()
        rc, out, _ = run_cli("reset")
        assert "reset" in out.lower()

    def test_reset_removes_state(self, isolated_state):
        start_sim()
        run_cli("reset")
        state_file = os.path.join(isolated_state, "tp_state.json")
        assert not os.path.exists(state_file)

    def test_reset_then_status_fails(self):
        start_sim()
        run_cli("reset")
        rc, _, _ = run_cli("status", expect_ok=False)
        assert rc != 0


# ── No command ─────────────────────────────────────────────────────

class TestNoCommand:

    def test_no_command_exits(self):
        rc, _, _ = run_cli(expect_ok=False)
        assert rc != 0
