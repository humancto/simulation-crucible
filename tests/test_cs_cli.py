"""Tests for cs_cli.py — state save/load roundtrip and subprocess integration."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "cs_cli.py")


@pytest.fixture
def state_dir(tmp_path):
    """Temporary state directory for CLI tests."""
    d = tmp_path / "cs_state"
    d.mkdir()
    return str(d)


def run_cli(args, state_dir, check=True):
    """Run cs_cli.py with given args and state directory."""
    env = os.environ.copy()
    env["CS_STATE_DIR"] = state_dir
    result = subprocess.run(
        [sys.executable, CLI] + args,
        capture_output=True, text=True, env=env,
        cwd=PROJECT_ROOT,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"CLI failed: {result.stderr}\nstdout: {result.stdout}")
    return result


class TestCLIStart:
    def test_start_creates_state(self, state_dir):
        run_cli(["start", "--seed", "42", "--years", "10"], state_dir)
        state_file = os.path.join(state_dir, "cs_state.json")
        assert os.path.exists(state_file)

    def test_start_output(self, state_dir):
        result = run_cli(["start", "--seed", "42"], state_dir)
        assert "Colony Ship" in result.stdout
        assert "Population" in result.stdout or "10,000" in result.stdout or "10000" in result.stdout


class TestCLIStatus:
    def test_status(self, state_dir):
        run_cli(["start", "--seed", "42", "--years", "10"], state_dir)
        result = run_cli(["status"], state_dir)
        assert "Year" in result.stdout
        assert "Population" in result.stdout or "Food" in result.stdout

    def test_status_no_sim(self, state_dir):
        result = run_cli(["status"], state_dir, check=False)
        assert result.returncode != 0


class TestCLIAdvance:
    def test_advance(self, state_dir):
        run_cli(["start", "--seed", "42", "--years", "10"], state_dir)
        result = run_cli(["advance"], state_dir)
        assert "Year 1" in result.stdout


class TestCLIStatePersistence:
    def test_state_roundtrip(self, state_dir):
        run_cli(["start", "--seed", "42", "--years", "10"], state_dir)
        run_cli(["advance"], state_dir)
        run_cli(["advance"], state_dir)

        # Load and verify state
        state_file = os.path.join(state_dir, "cs_state.json")
        with open(state_file) as f:
            data = json.load(f)
        assert data["current_year"] == 2
        assert data["seed"] == 42

    def test_actions_persist(self, state_dir):
        run_cli(["start", "--seed", "42", "--years", "10"], state_dir)
        run_cli(["election"], state_dir)

        state_file = os.path.join(state_dir, "cs_state.json")
        with open(state_file) as f:
            data = json.load(f)
        assert data["elections_held"] == 1


class TestCLIActions:
    def test_allocate_rations(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["allocate-rations", "--group", "elder",
                          "--level", "generous"], state_dir)
        assert "generous" in result.stdout.lower() or "elder" in result.stdout.lower()

    def test_maintain(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        run_cli(["advance"], state_dir)
        result = run_cli(["maintain", "--system", "Hydroponics Bay"], state_dir)
        assert "maintained" in result.stdout.lower() or "Hydroponics" in result.stdout

    def test_score(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["score"], state_dir)
        assert "Survival" in result.stdout or "survival" in result.stdout


class TestCLIReset:
    def test_reset(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        run_cli(["reset"], state_dir)
        state_file = os.path.join(state_dir, "cs_state.json")
        assert not os.path.exists(state_file)
