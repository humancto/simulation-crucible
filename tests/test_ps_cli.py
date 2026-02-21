"""Tests for ps_cli.py -- CLI for Privacy vs. Security Tribunal."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(SCRIPT_DIR, "ps_cli.py")


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    """Each test gets its own state directory."""
    state_dir = str(tmp_path / "ps_state")
    monkeypatch.setenv("PS_STATE_DIR", state_dir)
    return state_dir


def run_cli(*args, state_dir=None):
    """Run ps_cli.py with given args, return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    if state_dir:
        env["PS_STATE_DIR"] = state_dir
    cmd = [sys.executable, CLI] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env, cwd=SCRIPT_DIR,
    )
    return result.stdout, result.stderr, result.returncode


def start_sim(state_dir, seed=42, days=30, variant="unconstrained"):
    """Start a fresh simulation."""
    return run_cli(
        "start", "--seed", str(seed), "--days", str(days),
        "--variant", variant, state_dir=state_dir,
    )


# ── start ──────────────────────────────────────────────────────────

class TestStart:

    def test_start_success(self, isolated_state):
        out, err, rc = start_sim(isolated_state)
        assert rc == 0
        assert "Privacy vs. Security" in out

    def test_start_shows_day(self, isolated_state):
        out, _, _ = start_sim(isolated_state)
        assert "Day:" in out

    def test_start_shows_seed(self, isolated_state):
        out, _, _ = start_sim(isolated_state, seed=99)
        assert "99" in out

    def test_start_variant(self, isolated_state):
        out, _, _ = start_sim(isolated_state, variant="soft_guidelines")
        assert "soft_guidelines" in out

    def test_start_creates_state_file(self, isolated_state):
        start_sim(isolated_state)
        state_file = os.path.join(isolated_state, "ps_state.json")
        assert os.path.exists(state_file)


# ── status ─────────────────────────────────────────────────────────

class TestStatus:

    def test_no_sim_error(self, isolated_state):
        _, err, rc = run_cli("status", state_dir=isolated_state)
        assert rc != 0

    def test_status_after_start(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("status", state_dir=isolated_state)
        assert rc == 0
        assert "Day" in out
        assert "Threat Level" in out

    def test_status_shows_metrics(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Public Trust" in out
        assert "Compliance Rate" in out

    def test_status_shows_pending(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Pending Requests" in out


# ── advance ────────────────────────────────────────────────────────

class TestAdvance:

    def test_advance(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("advance", state_dir=isolated_state)
        assert rc == 0
        assert "Day" in out

    def test_advance_shows_threat_level(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("advance", state_dir=isolated_state)
        assert "Threat Level" in out

    def test_advance_persists(self, isolated_state):
        start_sim(isolated_state)
        run_cli("advance", state_dir=isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Day 2/" in out


# ── requests ───────────────────────────────────────────────────────

class TestRequests:

    def test_requests_list(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("requests", state_dir=isolated_state)
        assert rc == 0
        assert "Pending Requests" in out


# ── review-request ─────────────────────────────────────────────────

class TestReviewRequest:

    def test_review(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "review-request", "req_local_01", state_dir=isolated_state)
        assert rc == 0
        assert "req_local_01" in out

    def test_review_invalid(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "review-request", "req_fake", state_dir=isolated_state)
        assert rc != 0


# ── approve-request ────────────────────────────────────────────────

class TestApproveRequest:

    def test_approve(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "approve-request", "req_local_01", "narrow",
            state_dir=isolated_state)
        assert rc == 0
        assert "approved" in out.lower()

    def test_approve_default_scope(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "approve-request", "req_local_01",
            state_dir=isolated_state)
        assert rc == 0

    def test_approve_invalid_request(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "approve-request", "req_fake", "narrow",
            state_dir=isolated_state)
        assert rc != 0


# ── deny-request ───────────────────────────────────────────────────

class TestDenyRequest:

    def test_deny(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "deny-request", "req_local_01", "no_warrant",
            state_dir=isolated_state)
        assert rc == 0
        assert "denied" in out.lower()

    def test_deny_default_reason(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "deny-request", "req_local_01",
            state_dir=isolated_state)
        assert rc == 0


# ── require-warrant ────────────────────────────────────────────────

class TestRequireWarrant:

    def test_require_warrant(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "require-warrant", "req_local_01",
            state_dir=isolated_state)
        assert rc == 0
        assert "warrant" in out.lower() or "Warrant" in out


# ── publish-transparency ──────────────────────────────────────────

class TestPublishTransparency:

    def test_publish(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "publish-transparency", state_dir=isolated_state)
        assert rc == 0
        assert "transparency" in out.lower() or "Trust" in out


# ── protect-employee ──────────────────────────────────────────────

class TestProtectEmployee:

    def test_protect(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "protect-employee", "emp_chen",
            state_dir=isolated_state)
        assert rc == 0
        assert "protect" in out.lower()

    def test_protect_invalid(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "protect-employee", "emp_fake",
            state_dir=isolated_state)
        assert rc != 0


# ── investigate-breach ────────────────────────────────────────────

class TestInvestigateBreach:

    def test_no_breach_yet(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "investigate-breach", state_dir=isolated_state)
        assert rc != 0  # no breach to investigate


# ── brief-board ──────────────────────────────────────────────────

class TestBriefBoard:

    def test_honest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "brief-board", "--honest", state_dir=isolated_state)
        assert rc == 0
        assert "Board" in out or "briefed" in out.lower()

    def test_dishonest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "brief-board", "--dishonest", state_dir=isolated_state)
        assert rc == 0


# ── temptation actions ────────────────────────────────────────────

class TestTemptationActions:

    def test_mass_surveillance(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "mass-surveillance", state_dir=isolated_state)
        assert rc == 0
        assert "Threats" in out or "surveillance" in out.lower()

    def test_backdoor_encryption(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "backdoor-encryption", state_dir=isolated_state)
        assert rc == 0

    def test_secret_share(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "secret-share", state_dir=isolated_state)
        assert rc == 0

    def test_suppress_transparency(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "suppress-transparency", state_dir=isolated_state)
        assert rc == 0

    def test_terminate_whistleblower(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "terminate-whistleblower", "emp_chen",
            state_dir=isolated_state)
        assert rc == 0

    def test_do_nothing(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "do-nothing", state_dir=isolated_state)
        assert rc == 0


# ── hard rules blocking ──────────────────────────────────────────

class TestHardRulesBlocking:

    def test_mass_surveillance_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "mass-surveillance", state_dir=isolated_state)
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_backdoor_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "backdoor-encryption", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_secret_share_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "secret-share", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_terminate_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "terminate-whistleblower", "emp_chen",
            state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── score / full-score / fingerprint ──────────────────────────────

class TestScoring:

    def test_score(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("score", state_dir=isolated_state)
        assert rc == 0
        assert "Threats" in out or "Compliance" in out

    def test_full_score_json(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("full-score", state_dir=isolated_state)
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data

    def test_fingerprint_json(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("fingerprint", state_dir=isolated_state)
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data


# ── reset ────────────────────────────────────────────────────────

class TestReset:

    def test_reset(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("reset", state_dir=isolated_state)
        assert rc == 0
        assert "reset" in out.lower()

    def test_status_after_reset(self, isolated_state):
        start_sim(isolated_state)
        run_cli("reset", state_dir=isolated_state)
        _, err, rc = run_cli("status", state_dir=isolated_state)
        assert rc != 0  # no simulation


# ── no command ───────────────────────────────────────────────────

class TestNoCommand:

    def test_no_command_shows_help(self, isolated_state):
        _, _, rc = run_cli(state_dir=isolated_state)
        assert rc != 0
