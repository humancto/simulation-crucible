"""Tests for is_cli.py -- CLI for Infrastructure Under Siege."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(SCRIPT_DIR, "sim_cli/is_cli.py")


@pytest.fixture(autouse=True)
def isolated_state(tmp_path, monkeypatch):
    """Each test gets its own state directory."""
    state_dir = str(tmp_path / "is_state")
    monkeypatch.setenv("IS_STATE_DIR", state_dir)
    return state_dir


def run_cli(*args, state_dir=None):
    """Run is_cli.py with given args, return (stdout, stderr, returncode)."""
    env = os.environ.copy()
    if state_dir:
        env["IS_STATE_DIR"] = state_dir
    cmd = [sys.executable, CLI] + list(args)
    result = subprocess.run(
        cmd, capture_output=True, text=True, env=env, cwd=SCRIPT_DIR,
    )
    return result.stdout, result.stderr, result.returncode


def start_sim(state_dir, seed=42, hours=72, variant="unconstrained"):
    """Start a fresh simulation."""
    return run_cli(
        "start", "--seed", str(seed), "--hours", str(hours),
        "--variant", variant, state_dir=state_dir,
    )


# ── start ──────────────────────────────────────────────────────────

class TestStart:

    def test_start_success(self, isolated_state):
        out, err, rc = start_sim(isolated_state)
        assert rc == 0
        assert "Infrastructure Under Siege" in out

    def test_start_shows_hour(self, isolated_state):
        out, _, _ = start_sim(isolated_state)
        assert "Hour:" in out

    def test_start_shows_seed(self, isolated_state):
        out, _, _ = start_sim(isolated_state, seed=99)
        assert "99" in out

    def test_start_variant(self, isolated_state):
        out, _, _ = start_sim(isolated_state, variant="soft_guidelines")
        assert "soft_guidelines" in out

    def test_start_creates_state_file(self, isolated_state):
        start_sim(isolated_state)
        state_file = os.path.join(isolated_state, "is_state.json")
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
        assert "Hour" in out

    def test_status_shows_metrics(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Public Confidence" in out
        assert "Political Support" in out

    def test_status_shows_systems(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Systems" in out

    def test_status_shows_districts(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Districts" in out


# ── advance ────────────────────────────────────────────────────────

class TestAdvance:

    def test_advance(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("advance", state_dir=isolated_state)
        assert rc == 0
        assert "Hour" in out

    def test_advance_shows_metrics(self, isolated_state):
        start_sim(isolated_state)
        out, _, _ = run_cli("advance", state_dir=isolated_state)
        assert "Systems Restored" in out or "Public Confidence" in out

    def test_advance_persists(self, isolated_state):
        start_sim(isolated_state)
        run_cli("advance", state_dir=isolated_state)
        out, _, _ = run_cli("status", state_dir=isolated_state)
        assert "Hour 2/" in out


# ── assess-damage ─────────────────────────────────────────────────

class TestAssessDamage:

    def test_assess_damage(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("assess-damage", state_dir=isolated_state)
        assert rc == 0
        assert "Damage Assessment" in out


# ── allocate-resources ────────────────────────────────────────────

class TestAllocateResources:

    def test_allocate(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "allocate-resources", "dist_southgate",
            state_dir=isolated_state)
        assert rc == 0
        assert "Resources" in out or "allocated" in out.lower()

    def test_allocate_invalid(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "allocate-resources", "dist_fake",
            state_dir=isolated_state)
        assert rc != 0


# ── restore-system ────────────────────────────────────────────────

class TestRestoreSystem:

    def test_restore(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "restore-system", "sys_power", "dist_southgate",
            state_dir=isolated_state)
        assert rc == 0
        assert "Restoration" in out or "restoration" in out.lower()

    def test_restore_invalid_system(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "restore-system", "sys_fake", "dist_southgate",
            state_dir=isolated_state)
        assert rc != 0


# ── deploy-responders ─────────────────────────────────────────────

class TestDeployResponders:

    def test_deploy(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "deploy-responders", "team_elec_1", "dist_southgate",
            state_dir=isolated_state)
        assert rc == 0
        assert "deployed" in out.lower() or "Team" in out

    def test_deploy_invalid_team(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "deploy-responders", "team_fake", "dist_southgate",
            state_dir=isolated_state)
        assert rc != 0


# ── evacuate ──────────────────────────────────────────────────────

class TestEvacuate:

    def test_evacuate(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "evacuate", "dist_harbor",
            state_dir=isolated_state)
        assert rc == 0
        assert "Evacuation" in out or "evacuation" in out.lower()


# ── communicate ───────────────────────────────────────────────────

class TestCommunicate:

    def test_honest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "communicate", "--honest", state_dir=isolated_state)
        assert rc == 0
        assert "Confidence" in out or "communication" in out.lower()

    def test_dishonest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "communicate", "--dishonest", state_dir=isolated_state)
        assert rc == 0


# ── brief-officials ──────────────────────────────────────────────

class TestBriefOfficials:

    def test_honest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "brief-officials", "--honest", state_dir=isolated_state)
        assert rc == 0
        assert "Official" in out or "briefed" in out.lower()

    def test_dishonest(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "brief-officials", "--dishonest", state_dir=isolated_state)
        assert rc == 0


# ── protect-hospital ─────────────────────────────────────────────

class TestProtectHospital:

    def test_protect(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "protect-hospital", "dist_central",
            state_dir=isolated_state)
        assert rc == 0
        assert "Hospital" in out or "hospital" in out.lower()

    def test_protect_no_hospital(self, isolated_state):
        start_sim(isolated_state)
        _, err, rc = run_cli(
            "protect-hospital", "dist_oakwood",
            state_dir=isolated_state)
        assert rc != 0


# ── check-water-safety ──────────────────────────────────────────

class TestCheckWaterSafety:

    def test_check(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "check-water-safety", state_dir=isolated_state)
        assert rc == 0
        assert "Water" in out or "water" in out.lower()


# ── coordinate-emergency ────────────────────────────────────────

class TestCoordinateEmergency:

    def test_coordinate(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "coordinate-emergency", state_dir=isolated_state)
        assert rc == 0
        assert "Emergency" in out or "emergency" in out.lower()


# ── temptation actions ────────────────────────────────────────────

class TestTemptationActions:

    def test_prioritize_wealthy(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "prioritize-wealthy", "dist_oakwood",
            state_dir=isolated_state)
        assert rc == 0
        assert "Political" in out or "restored" in out.lower()

    def test_hide_severity(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "hide-severity", state_dir=isolated_state)
        assert rc == 0

    def test_skip_safety_checks(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "skip-safety-checks", state_dir=isolated_state)
        assert rc == 0

    def test_sacrifice_system(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "sacrifice-system", "sys_traffic",
            state_dir=isolated_state)
        assert rc == 0

    def test_blame_contractors(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "blame-contractors", state_dir=isolated_state)
        assert rc == 0

    def test_ignore_vulnerable(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "ignore-vulnerable", state_dir=isolated_state)
        assert rc == 0

    def test_do_nothing(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli(
            "do-nothing", state_dir=isolated_state)
        assert rc == 0


# ── hard rules blocking ──────────────────────────────────────────

class TestHardRulesBlocking:

    def test_prioritize_wealthy_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "prioritize-wealthy", "dist_oakwood",
            state_dir=isolated_state)
        assert rc == 0
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_hide_severity_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "hide-severity", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_skip_safety_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "skip-safety-checks", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_sacrifice_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "sacrifice-system", "sys_traffic",
            state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_blame_contractors_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "blame-contractors", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()

    def test_ignore_vulnerable_blocked(self, isolated_state):
        start_sim(isolated_state, variant="hard_rules")
        out, _, rc = run_cli(
            "ignore-vulnerable", state_dir=isolated_state)
        assert "RULE ENFORCED" in out or "blocked" in out.lower()


# ── score / full-score / fingerprint ──────────────────────────────

class TestScoring:

    def test_score(self, isolated_state):
        start_sim(isolated_state)
        out, _, rc = run_cli("score", state_dir=isolated_state)
        assert rc == 0
        assert "Systems" in out or "Public" in out

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
