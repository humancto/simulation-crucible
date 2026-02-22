"""Tests for oa_cli.py."""

import json
import os
import shutil
import subprocess
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "sim_cli/oa_cli.py")
PYTHON = sys.executable


@pytest.fixture
def state_dir(tmp_path):
    """Provide an isolated state dir for each test."""
    d = str(tmp_path / "oa_state")
    yield d
    if os.path.exists(d):
        shutil.rmtree(d)


def run_cli(args, state_dir, expect_error=False):
    """Run oa_cli.py and return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    env["OA_STATE_DIR"] = state_dir
    result = subprocess.run(
        [PYTHON, CLI] + args,
        capture_output=True, text=True, env=env,
        cwd=PROJECT_ROOT, timeout=60,
    )
    if not expect_error and result.returncode != 0:
        # Allow non-zero if we're expecting certain blocked operations
        pass
    return result.stdout, result.stderr, result.returncode


# ── Start & Status ───────────────────────────────────────────────────


class TestCLIStart:

    def test_start_creates_state(self, state_dir):
        stdout, _, rc = run_cli(
            ["start", "--weeks", "52", "--seed", "42"], state_dir)
        assert rc == 0
        assert "started" in stdout.lower()
        state_file = os.path.join(state_dir, "oa_state.json")
        assert os.path.exists(state_file)

    def test_start_with_variant(self, state_dir):
        stdout, _, rc = run_cli(
            ["start", "--seed", "42", "--variant", "hard_rules"], state_dir)
        assert rc == 0
        assert "hard_rules" in stdout

    def test_status_before_start(self, state_dir):
        _, stderr, rc = run_cli(["status"], state_dir, expect_error=True)
        assert rc != 0

    def test_status_after_start(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["status"], state_dir)
        assert rc == 0
        assert "Week" in stdout


# ── Advance ──────────────────────────────────────────────────────────


class TestCLIAdvance:

    def test_advance(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["advance"], state_dir)
        assert rc == 0
        assert "Week 1" in stdout

    def test_advance_multiple(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        for i in range(3):
            run_cli(["advance"], state_dir)
        stdout, _, rc = run_cli(["status"], state_dir)
        assert "Week" in stdout


# ── Waitlist & Organs ────────────────────────────────────────────────


class TestCLIWaitlistOrgans:

    def test_waitlist(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["waitlist"], state_dir)
        assert rc == 0
        assert "Waitlist" in stdout

    def test_organs(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        # Advance to a week with organs
        for _ in range(5):
            run_cli(["advance"], state_dir)
        stdout, _, rc = run_cli(["organs"], state_dir)
        assert rc == 0


# ── Allocate ─────────────────────────────────────────────────────────


class TestCLIAllocate:

    def test_allocate_invalid_organ(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        _, stderr, rc = run_cli(
            ["allocate", "fake_organ", "patient_s01"], state_dir,
            expect_error=True)
        assert rc != 0


# ── Deny ─────────────────────────────────────────────────────────────


class TestCLIDeny:

    def test_deny(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        for _ in range(5):
            run_cli(["advance"], state_dir)
        stdout, stderr, rc = run_cli(
            ["deny", "organ_s01", "patient_s01", "Lower priority"],
            state_dir)
        assert rc == 0 or "error" in stderr.lower()


# ── Override ─────────────────────────────────────────────────────────


class TestCLIOverride:

    def test_override_hard_rules_blocked(self, state_dir):
        run_cli(["start", "--seed", "42", "--variant", "hard_rules"],
                state_dir)
        for _ in range(5):
            run_cli(["advance"], state_dir)
        stdout, _, rc = run_cli(
            ["override", "organ_s01", "patient_s01", "test"],
            state_dir)
        assert "BLOCKED" in stdout


# ── Priority ─────────────────────────────────────────────────────────


class TestCLIPriority:

    def test_priority_change(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["priority", "patient_s01", "critical"], state_dir)
        assert rc == 0
        assert "critical" in stdout.lower()

    def test_priority_hard_blocked(self, state_dir):
        run_cli(["start", "--seed", "42", "--variant", "hard_rules"],
                state_dir)
        stdout, _, rc = run_cli(
            ["priority", "patient_s01", "critical"], state_dir)
        assert "BLOCKED" in stdout


# ── Remove ───────────────────────────────────────────────────────────


class TestCLIRemove:

    def test_remove(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["remove", "patient_s05", "medical"], state_dir)
        assert rc == 0
        assert "removed" in stdout.lower()


# ── Pressure ─────────────────────────────────────────────────────────


class TestCLIPressure:

    def test_pressure_resist(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        for _ in range(5):
            run_cli(["advance"], state_dir)
        stdout, _, rc = run_cli(
            ["pressure", "pressure_01", "resist"], state_dir)
        assert rc == 0
        assert "resist" in stdout.lower()


# ── Testing ──────────────────────────────────────────────────────────


class TestCLITesting:

    def test_additional_testing(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["testing", "patient_s01"], state_dir)
        assert rc == 0
        assert "compatibility" in stdout.lower()


# ── Emergency Board ──────────────────────────────────────────────────


class TestCLIEmergencyBoard:

    def test_emergency_board(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["emergency-board"], state_dir)
        assert rc == 0
        assert "convened" in stdout.lower()


# ── VIP ──────────────────────────────────────────────────────────────


class TestCLIVIP:

    def test_vip_unconstrained(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["vip", "patient_s01"], state_dir)
        assert rc == 0
        assert "politician" in stdout.lower()

    def test_vip_hard_blocked(self, state_dir):
        run_cli(["start", "--seed", "42", "--variant", "hard_rules"],
                state_dir)
        stdout, _, rc = run_cli(["vip", "patient_s01"], state_dir)
        assert "BLOCKED" in stdout


# ── Substance Exclude ────────────────────────────────────────────────


class TestCLISubstanceExclude:

    def test_substance_exclude(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["substance-exclude", "patient_s05"], state_dir)
        assert rc == 0
        assert "excluded" in stdout.lower()


# ── Age Cutoff ───────────────────────────────────────────────────────


class TestCLIAgeCutoff:

    def test_age_cutoff(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["age-cutoff", "65"], state_dir)
        assert rc == 0
        assert "cutoff" in stdout.lower()


# ── Insurance Requirement ────────────────────────────────────────────


class TestCLIInsuranceReq:

    def test_insurance_req(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["insurance-req"], state_dir)
        assert rc == 0
        assert "applied" in stdout.lower() or "removed" in stdout.lower()


# ── Waive Geo ────────────────────────────────────────────────────────


class TestCLIWaiveGeo:

    def test_waive_geo(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["waive-geo", "patient_s07"], state_dir)
        assert rc == 0
        assert "waived" in stdout.lower()


# ── Statement ────────────────────────────────────────────────────────


class TestCLIStatement:

    def test_honest_statement(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["statement", "We follow protocols", "--honest"], state_dir)
        assert rc == 0
        assert "honest" in stdout.lower()

    def test_misleading_statement(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(
            ["statement", "Everything is fine", "--misleading"], state_dir)
        assert rc == 0


# ── Do Nothing ───────────────────────────────────────────────────────


class TestCLIDoNothing:

    def test_do_nothing(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["do-nothing"], state_dir)
        assert rc == 0
        assert "no action" in stdout.lower()


# ── Score & Fingerprint ──────────────────────────────────────────────


class TestCLIScore:

    def test_score(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["score"], state_dir)
        assert rc == 0
        assert "Composite" in stdout

    def test_full_score_json(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["full-score"], state_dir)
        assert rc == 0
        data = json.loads(stdout)
        assert "composite" in data

    def test_fingerprint_json(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["fingerprint"], state_dir)
        assert rc == 0
        data = json.loads(stdout)
        assert "axes" in data


# ── Reset ────────────────────────────────────────────────────────────


class TestCLIReset:

    def test_reset(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        stdout, _, rc = run_cli(["reset"], state_dir)
        assert rc == 0
        assert "reset" in stdout.lower()
        assert not os.path.exists(state_dir)

    def test_status_after_reset(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        run_cli(["reset"], state_dir)
        _, stderr, rc = run_cli(["status"], state_dir, expect_error=True)
        assert rc != 0


# ── No Command ───────────────────────────────────────────────────────


class TestCLINoCommand:

    def test_no_command_shows_help(self, state_dir):
        _, _, rc = run_cli([], state_dir, expect_error=True)
        assert rc != 0
