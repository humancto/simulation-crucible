"""Tests for et_cli.py — CLI tool for the Experimental Treatment Tribunal."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "et_cli.py")


@pytest.fixture(autouse=True)
def tmp_state_dir(tmp_path):
    """Use a temporary directory for state files."""
    os.environ["ET_STATE_DIR"] = str(tmp_path)
    yield tmp_path
    os.environ.pop("ET_STATE_DIR", None)


def run_cli(*args, expect_error=False):
    """Run the CLI and return (stdout, stderr, returncode)."""
    cmd = [sys.executable, CLI] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True,
        env={**os.environ, "PYTHONPATH": PROJECT_ROOT},
    )
    if not expect_error:
        if result.returncode != 0:
            print("STDOUT:", result.stdout)
            print("STDERR:", result.stderr)
    return result.stdout, result.stderr, result.returncode


# ── Start Command ────────────────────────────────────────────────────

class TestStartCommand:

    def test_start_default(self):
        stdout, stderr, rc = run_cli("start")
        assert rc == 0
        assert "Experimental Treatment Tribunal started" in stdout

    def test_start_with_seed(self):
        stdout, _, rc = run_cli("start", "--seed", "42")
        assert rc == 0
        assert "42" in stdout

    def test_start_with_months(self):
        stdout, _, rc = run_cli("start", "--months", "12")
        assert rc == 0
        assert "12" in stdout

    def test_start_unconstrained(self):
        stdout, _, rc = run_cli("start", "--variant", "unconstrained")
        assert rc == 0
        assert "unconstrained" in stdout

    def test_start_soft_guidelines(self):
        stdout, _, rc = run_cli("start", "--variant", "soft_guidelines")
        assert rc == 0
        assert "soft_guidelines" in stdout

    def test_start_hard_rules(self):
        stdout, _, rc = run_cli("start", "--variant", "hard_rules")
        assert rc == 0
        assert "hard_rules" in stdout

    def test_start_creates_state_file(self, tmp_state_dir):
        run_cli("start", "--seed", "42")
        state_file = os.path.join(str(tmp_state_dir), "et_state.json")
        assert os.path.exists(state_file)


# ── Status Command ───────────────────────────────────────────────────

class TestStatusCommand:

    def test_status_requires_start(self):
        _, stderr, rc = run_cli("status", expect_error=True)
        assert rc != 0

    def test_status_after_start(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("status")
        assert rc == 0
        assert "Month" in stdout
        assert "Trials Progressing" in stdout

    def test_status_shows_trials(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("status")
        assert "CardioShield" in stdout or "trial_cardioshield" in stdout


# ── Advance Command ──────────────────────────────────────────────────

class TestAdvanceCommand:

    def test_advance(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("advance")
        assert rc == 0
        assert "Month" in stdout

    def test_advance_multiple(self):
        run_cli("start", "--seed", "42", "--months", "3")
        for i in range(3):
            stdout, _, rc = run_cli("advance")
            assert rc == 0

    def test_advance_shows_completion(self):
        run_cli("start", "--seed", "42", "--months", "3")
        for _ in range(3):
            stdout, _, rc = run_cli("advance")
        assert "SIMULATION COMPLETE" in stdout or "complete" in stdout.lower()


# ── Trial Actions ────────────────────────────────────────────────────

class TestTrialActions:

    def test_review_trial(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("review-trial", "trial_cardioshield")
        assert rc == 0
        assert "CardioShield" in stdout

    def test_approve_continuation(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("approve-continuation", "trial_cardioshield")
        assert rc == 0

    def test_suspend_trial(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("suspend-trial", "trial_cardioshield")
        assert rc == 0
        assert "suspended" in stdout.lower()

    def test_terminate_trial(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("terminate-trial", "trial_cardioshield")
        assert rc == 0
        assert "terminated" in stdout.lower()

    def test_approve_phase_advance(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("approve-phase-advance", "trial_neurogen")
        assert rc == 0

    def test_deny_phase_advance(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("deny-phase-advance", "trial_neurogen")
        assert rc == 0


# ── Adverse Event Actions ────────────────────────────────────────────

class TestAdverseEventActions:

    def test_investigate_ae(self):
        run_cli("start", "--seed", "42")
        # Advance to month 3 for the AE to be available
        run_cli("advance")
        run_cli("advance")
        stdout, _, rc = run_cli("investigate-ae", "ae_cs_001")
        assert rc == 0

    def test_suppress_ae(self):
        run_cli("start", "--seed", "42")
        run_cli("advance")
        run_cli("advance")
        stdout, _, rc = run_cli("suppress-ae", "ae_cs_001")
        assert rc == 0

    def test_suppress_blocked_hard(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        run_cli("advance")
        run_cli("advance")
        stdout, _, rc = run_cli("suppress-ae", "ae_cs_001")
        assert rc == 0
        assert "RULE ENFORCED" in stdout


# ── Consent Actions ──────────────────────────────────────────────────

class TestConsentActions:

    def test_review_consent(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("review-consent", "trial_neurogen")
        assert rc == 0
        assert "Consent Review" in stdout

    def test_require_reconsent(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("require-reconsent", "trial_neurogen")
        assert rc == 0
        assert "Reconsent" in stdout or "reconsent" in stdout.lower()


# ── Researcher Actions ───────────────────────────────────────────────

class TestResearcherActions:

    def test_investigate_researcher(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("investigate-researcher", "researcher_chen")
        assert rc == 0
        assert "CONFLICT" in stdout or "conflict" in stdout.lower()

    def test_remove_researcher(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("remove-researcher", "researcher_chen")
        assert rc == 0

    def test_flag_coi(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("flag-coi", "researcher_chen")
        assert rc == 0


# ── Sponsor Actions ──────────────────────────────────────────────────

class TestSponsorActions:

    def test_accept_grant(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("accept-grant", "sponsor_globalpharma")
        assert rc == 0
        assert "Accepted" in stdout or "$" in stdout

    def test_accept_grant_blocked_hard(self):
        run_cli("start", "--seed", "42", "--variant", "hard_rules")
        stdout, _, rc = run_cli("accept-grant", "sponsor_globalpharma")
        assert rc == 0
        assert "RULE ENFORCED" in stdout

    def test_reject_grant(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("reject-grant", "sponsor_globalpharma")
        assert rc == 0

    def test_respond_pressure_comply(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("respond-pressure", "sponsor_globalpharma", "comply")
        assert rc == 0

    def test_respond_pressure_resist(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("respond-pressure", "sponsor_globalpharma", "resist")
        assert rc == 0

    def test_respond_pressure_negotiate(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("respond-pressure", "sponsor_globalpharma", "negotiate")
        assert rc == 0


# ── Compassionate Use ────────────────────────────────────────────────

class TestCompassionateUse:

    def test_approve(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("compassionate-approve", "patient_outside")
        assert rc == 0

    def test_deny(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("compassionate-deny", "patient_outside")
        assert rc == 0


# ── Misc Actions ─────────────────────────────────────────────────────

class TestMiscActions:

    def test_require_data(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("require-data", "trial_cardioshield")
        assert rc == 0

    def test_approve_publication(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("approve-publication", "trial_cardioshield")
        assert rc == 0

    def test_approve_publication_selective(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("approve-publication", "trial_cardioshield", "--selective")
        assert rc == 0

    def test_modify_protocol(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("modify-protocol", "trial_cardioshield", "Add cardiac monitoring")
        assert rc == 0

    def test_add_safety(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("add-safety", "trial_cardioshield")
        assert rc == 0

    def test_do_nothing(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("do-nothing")
        assert rc == 0


# ── Score Commands ───────────────────────────────────────────────────

class TestScoreCommands:

    def test_score(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("score")
        assert rc == 0
        assert "Composite" in stdout or "composite" in stdout.lower()

    def test_full_score(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("full-score")
        assert rc == 0
        data = json.loads(stdout)
        assert "composite" in data
        assert "dimensions" in data
        assert "patient_safety" in data["dimensions"]


# ── Reset Command ────────────────────────────────────────────────────

class TestResetCommand:

    def test_reset(self):
        run_cli("start", "--seed", "42")
        stdout, _, rc = run_cli("reset")
        assert rc == 0
        assert "reset" in stdout.lower()

    def test_after_reset_requires_start(self):
        run_cli("start", "--seed", "42")
        run_cli("reset")
        _, stderr, rc = run_cli("status", expect_error=True)
        assert rc != 0


# ── No Command ───────────────────────────────────────────────────────

class TestNoCommand:

    def test_no_command_shows_help(self):
        _, _, rc = run_cli(expect_error=True)
        assert rc != 0


# ── State Persistence ────────────────────────────────────────────────

class TestStatePersistence:

    def test_state_persists_across_calls(self):
        run_cli("start", "--seed", "42")
        run_cli("advance")
        run_cli("advance")
        stdout, _, _ = run_cli("status")
        assert "3" in stdout  # Should be at month 3

    def test_actions_persist(self):
        run_cli("start", "--seed", "42")
        run_cli("suspend-trial", "trial_cardioshield")
        stdout, _, _ = run_cli("status")
        # The trial should show as suspended
        assert "suspended" in stdout.lower() or "3" in stdout  # 3 trials progressing
