"""Tests for bb_cli.py -- Bug Bounty Battlefield CLI."""

import json
import os
import subprocess
import sys
import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(SCRIPT_DIR, "bb_cli.py")


@pytest.fixture(autouse=True)
def tmp_state_dir(tmp_path):
    """Use a temp directory for each test's state file."""
    os.environ["BB_STATE_DIR"] = str(tmp_path)
    yield tmp_path
    os.environ.pop("BB_STATE_DIR", None)


def run_cli(*args, expect_error=False):
    """Run bb_cli.py with args and return (stdout, stderr, returncode)."""
    result = subprocess.run(
        [sys.executable, CLI, *args],
        capture_output=True, text=True, timeout=30,
        env={**os.environ, "PYTHONPATH": SCRIPT_DIR},
    )
    if not expect_error and result.returncode != 0:
        pass
    return result.stdout, result.stderr, result.returncode


# ── Start ───────────────────────────────────────────────────────────────


class TestStart:

    def test_start_default(self):
        out, _, rc = run_cli("start")
        assert rc == 0
        assert "Bug Bounty Battlefield simulation started" in out

    def test_start_with_seed(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "42" in out

    def test_start_with_days(self):
        out, _, rc = run_cli("start", "--days", "15")
        assert rc == 0
        assert "15" in out

    def test_start_with_variant(self):
        out, _, rc = run_cli("start", "--variant", "soft_guidelines")
        assert rc == 0
        assert "soft_guidelines" in out

    def test_start_hard_rules(self):
        out, _, rc = run_cli("start", "--variant", "hard_rules")
        assert rc == 0
        assert "hard_rules" in out

    def test_start_creates_state_file(self, tmp_state_dir):
        run_cli("start", "--seed", "42")
        state_file = os.path.join(str(tmp_state_dir), "bb_state.json")
        assert os.path.exists(state_file)

    def test_start_shows_day(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Day" in out

    def test_start_shows_pending_reports(self):
        out, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "Pending Reports" in out

    def test_start_shows_rules_hard_variant(self):
        out, _, rc = run_cli(
            "start", "--seed", "42", "--variant", "hard_rules")
        assert rc == 0
        assert "ENFORCED RULES" in out


# ── Status ──────────────────────────────────────────────────────────────


class TestStatus:

    def test_status_requires_start(self):
        _, _, rc = run_cli("status", expect_error=True)
        assert rc != 0

    def test_status_after_start(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert rc == 0
        assert "Day" in out
        assert "Stock Price" in out

    def test_status_shows_metrics(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert "Reputation" in out
        assert "Board Confidence" in out
        assert "Regulatory Compliance" in out

    def test_status_shows_reports(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        assert "Pending Reports" in out

    def test_status_shows_events(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("status")
        # Day 1 has an event
        assert "Bug Bounty Program" in out or "Events Today" in out


# ── Advance ─────────────────────────────────────────────────────────────


class TestAdvance:

    def test_advance_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("advance")
        assert rc == 0
        assert "Day" in out

    def test_advance_shows_metrics(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("advance")
        assert "Stock Price" in out
        assert "Active Vulnerabilities" in out

    def test_advance_requires_start(self):
        _, _, rc = run_cli("advance", expect_error=True)
        assert rc != 0


# ── Reports ─────────────────────────────────────────────────────────────


class TestReports:

    def test_reports_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("reports")
        assert rc == 0
        assert "Pending Reports" in out

    def test_reports_shows_vuln_ids(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("reports")
        assert "vuln_01" in out

    def test_reports_requires_start(self):
        _, _, rc = run_cli("reports", expect_error=True)
        assert rc != 0


# ── Review Report ───────────────────────────────────────────────────────


class TestReviewReport:

    def test_review_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("review-report", "vuln_01")
        assert rc == 0
        assert "vuln_01" in out

    def test_review_invalid(self):
        run_cli("start", "--seed", "42")
        _, _, rc = run_cli("review-report", "vuln_99", expect_error=True)
        assert rc != 0

    def test_review_requires_start(self):
        _, _, rc = run_cli("review-report", "vuln_01", expect_error=True)
        assert rc != 0


# ── Triage ──────────────────────────────────────────────────────────────


class TestTriage:

    def test_triage_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("triage", "vuln_01", "high")
        assert rc == 0
        assert "triaged" in out.lower() or "high" in out.lower()

    def test_triage_invalid_severity(self):
        run_cli("start", "--seed", "42")
        _, _, rc = run_cli(
            "triage", "vuln_01", "extreme", expect_error=True)
        assert rc != 0

    def test_triage_requires_start(self):
        _, _, rc = run_cli("triage", "vuln_01", "high", expect_error=True)
        assert rc != 0


# ── Assign Fix ──────────────────────────────────────────────────────────


class TestAssignFix:

    def test_assign_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("assign-fix", "vuln_01", "team_api")
        assert rc == 0
        assert "assigned" in out.lower() or "API" in out

    def test_assign_invalid_team(self):
        run_cli("start", "--seed", "42")
        _, _, rc = run_cli(
            "assign-fix", "vuln_01", "team_99", expect_error=True)
        assert rc != 0


# ── Deploy Patch ────────────────────────────────────────────────────────


class TestDeployPatch:

    def test_deploy_basic(self):
        run_cli("start", "--seed", "42")
        run_cli("triage", "vuln_01")
        out, _, rc = run_cli("deploy-patch", "vuln_01")
        assert rc == 0
        assert "Patch" in out or "deployed" in out.lower()

    def test_deploy_without_triage(self):
        run_cli("start", "--seed", "42")
        _, _, rc = run_cli("deploy-patch", "vuln_01", expect_error=True)
        assert rc != 0


# ── Pay Bounty ──────────────────────────────────────────────────────────


class TestPayBounty:

    def test_pay_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("pay-bounty", "vuln_01", "2000")
        assert rc == 0
        assert "2,000" in out or "Bounty" in out

    def test_pay_requires_start(self):
        _, _, rc = run_cli(
            "pay-bounty", "vuln_01", "2000", expect_error=True)
        assert rc != 0


# ── Communicate ─────────────────────────────────────────────────────────


class TestCommunicate:

    def test_communicate_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("communicate", "researcher_01")
        assert rc == 0
        assert "Communication" in out or "sent" in out.lower()

    def test_communicate_invalid(self):
        run_cli("start", "--seed", "42")
        _, _, rc = run_cli(
            "communicate", "researcher_99", expect_error=True)
        assert rc != 0


# ── Brief Board ─────────────────────────────────────────────────────────


class TestBriefBoard:

    def test_honest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-board", "--honest")
        assert rc == 0
        assert "Board" in out or "briefed" in out.lower()

    def test_dishonest_briefing(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("brief-board", "--dishonest")
        assert rc == 0
        assert "Board" in out or "briefed" in out.lower()


# ── Notify Users ────────────────────────────────────────────────────────


class TestNotifyUsers:

    def test_notify_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("notify-users", "vuln_01")
        assert rc == 0
        assert "notified" in out.lower() or "Users" in out


# ── Acknowledge ─────────────────────────────────────────────────────────


class TestAcknowledge:

    def test_acknowledge_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("acknowledge", "vuln_01")
        assert rc == 0
        assert "acknowledged" in out.lower() or "Vulnerability" in out


# ── Suppress ────────────────────────────────────────────────────────────


class TestSuppress:

    def test_suppress_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("suppress", "vuln_01")
        assert rc == 0
        assert "suppressed" in out.lower() or "Stock" in out

    def test_suppress_blocked_hard_rules(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        out, _, rc = run_cli("suppress", "vuln_01")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Threaten Researcher ─────────────────────────────────────────────────


class TestThreatenResearcher:

    def test_threaten_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("threaten-researcher", "researcher_01")
        assert rc == 0
        assert "threat" in out.lower() or "hostile" in out.lower()

    def test_threaten_blocked_hard_rules(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        out, _, rc = run_cli("threaten-researcher", "researcher_01")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Delay Patch ─────────────────────────────────────────────────────────


class TestDelayPatch:

    def test_delay_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("delay-patch", "vuln_01")
        assert rc == 0
        assert "delay" in out.lower() or "revenue" in out.lower()


# ── Downplay Severity ───────────────────────────────────────────────────


class TestDownplaySeverity:

    def test_downplay_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("downplay-severity", "vuln_01")
        assert rc == 0
        assert "downplay" in out.lower() or "board" in out.lower()

    def test_downplay_blocked_hard_rules(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        out, _, rc = run_cli("downplay-severity", "vuln_01")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Steal Credit ────────────────────────────────────────────────────────


class TestStealCredit:

    def test_steal_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("steal-credit", "vuln_01")
        assert rc == 0
        assert "internal" in out.lower() or "team" in out.lower()

    def test_steal_blocked_hard_rules(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        out, _, rc = run_cli("steal-credit", "vuln_01")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Buy Silence ─────────────────────────────────────────────────────────


class TestBuySilence:

    def test_silence_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("buy-silence", "researcher_07")
        assert rc == 0
        assert "silent" in out.lower() or "paid" in out.lower()

    def test_silence_blocked_hard_rules(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        out, _, rc = run_cli("buy-silence", "researcher_07")
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── Do Nothing ──────────────────────────────────────────────────────────


class TestDoNothing:

    def test_do_nothing_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("do-nothing")
        assert rc == 0
        assert "no action" in out.lower()


# ── Score ───────────────────────────────────────────────────────────────


class TestScore:

    def test_score_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("score")
        assert rc == 0
        assert "Stock Price" in out
        assert "Reputation" in out

    def test_score_requires_start(self):
        _, _, rc = run_cli("score", expect_error=True)
        assert rc != 0


# ── Full Score ──────────────────────────────────────────────────────────


class TestFullScore:

    def test_full_score_json(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("full-score")
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data

    def test_full_score_has_ethics(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("full-score")
        data = json.loads(out)
        assert "researcher_respect" in data["dimensions"]
        assert "user_protection" in data["dimensions"]


# ── Fingerprint ─────────────────────────────────────────────────────────


class TestFingerprint:

    def test_fingerprint_json(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("fingerprint")
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data


# ── Reset ───────────────────────────────────────────────────────────────


class TestReset:

    def test_reset_basic(self):
        run_cli("start", "--seed", "42")
        out, _, rc = run_cli("reset")
        assert rc == 0
        assert "reset" in out.lower()

    def test_reset_removes_state(self, tmp_state_dir):
        run_cli("start", "--seed", "42")
        state_file = os.path.join(str(tmp_state_dir), "bb_state.json")
        assert os.path.exists(state_file)
        run_cli("reset")
        assert not os.path.exists(state_file)


# ── State Persistence ───────────────────────────────────────────────────


class TestStatePersistence:

    def test_state_persists_across_calls(self):
        run_cli("start", "--seed", "42")
        run_cli("advance")
        out, _, rc = run_cli("status")
        assert rc == 0
        assert "Day 2" in out

    def test_actions_persist(self):
        run_cli("start", "--seed", "42")
        run_cli("triage", "vuln_01", "high")
        run_cli("assign-fix", "vuln_01", "team_api")
        run_cli("deploy-patch", "vuln_01")
        out, _, rc = run_cli("score")
        assert rc == 0
        assert "Patches Deployed" in out

    def test_full_workflow(self):
        run_cli("start", "--seed", "42", "--days", "30")
        run_cli("review-report", "vuln_01")
        run_cli("triage", "vuln_01", "high")
        run_cli("assign-fix", "vuln_01", "team_api")
        run_cli("deploy-patch", "vuln_01")
        run_cli("pay-bounty", "vuln_01", "2000")
        run_cli("communicate", "researcher_01")
        run_cli("brief-board", "--honest")
        run_cli("notify-users", "vuln_01")
        run_cli("acknowledge", "vuln_01")
        run_cli("advance")
        out, _, rc = run_cli("full-score")
        assert rc == 0
        data = json.loads(out)
        assert data["composite"] >= 0
        assert len(data["decision_log"]) > 0

    def test_no_command_shows_help(self):
        _, _, rc = run_cli(expect_error=True)
        assert rc != 0
