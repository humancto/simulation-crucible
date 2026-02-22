"""Tests for tn_cli.py -- state save/load roundtrip and subprocess integration."""

import json
import os
import subprocess
import sys

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(PROJECT_ROOT, "sim_cli/tn_cli.py")


@pytest.fixture
def state_dir(tmp_path):
    """Temporary state directory for CLI tests."""
    d = tmp_path / "tn_state"
    d.mkdir()
    return str(d)


def run_cli(args, state_dir, check=True):
    """Run tn_cli.py with given args and state directory."""
    env = os.environ.copy()
    env["TN_STATE_DIR"] = state_dir
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
        run_cli(["start", "--seed", "42", "--rounds", "10"], state_dir)
        state_file = os.path.join(state_dir, "tn_state.json")
        assert os.path.exists(state_file)

    def test_start_output(self, state_dir):
        result = run_cli(["start", "--seed", "42"], state_dir)
        assert "Trade Negotiation" in result.stdout
        assert "Reputation" in result.stdout


class TestCLIStatus:
    def test_status(self, state_dir):
        run_cli(["start", "--seed", "42", "--rounds", "10"], state_dir)
        result = run_cli(["status"], state_dir)
        assert "Round" in result.stdout
        assert "Deal Value" in result.stdout or "Reputation" in result.stdout

    def test_status_no_sim(self, state_dir):
        result = run_cli(["status"], state_dir, check=False)
        assert result.returncode != 0


class TestCLIAdvance:
    def test_advance(self, state_dir):
        run_cli(["start", "--seed", "42", "--rounds", "10"], state_dir)
        result = run_cli(["advance"], state_dir)
        assert "Round 1" in result.stdout


class TestCLIStatePersistence:
    def test_state_roundtrip(self, state_dir):
        run_cli(["start", "--seed", "42", "--rounds", "10"], state_dir)
        run_cli(["advance"], state_dir)
        run_cli(["advance"], state_dir)

        # Load and verify state
        state_file = os.path.join(state_dir, "tn_state.json")
        with open(state_file) as f:
            data = json.load(f)
        assert data["current_round"] == 2
        assert data["seed"] == 42

    def test_actions_persist(self, state_dir):
        run_cli(["start", "--seed", "42", "--rounds", "10"], state_dir)
        run_cli(["offer-fair-terms", "partner_05"], state_dir)

        state_file = os.path.join(state_dir, "tn_state.json")
        with open(state_file) as f:
            data = json.load(f)
        assert len(data["decision_log"]) >= 1


class TestCLIActions:
    def test_partners(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["partners"], state_dir)
        assert "partner_01" in result.stdout or "Nortania" in result.stdout

    def test_offer_fair_terms(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["offer-fair-terms", "partner_06"], state_dir)
        assert "Trust" in result.stdout or "trust" in result.stdout

    def test_exploit_weakness(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["exploit-weakness", "partner_05"], state_dir)
        assert "Exploit" in result.stdout or "Deal Value" in result.stdout

    def test_score(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["score"], state_dir)
        assert "Reputation" in result.stdout or "Deal Value" in result.stdout

    def test_full_score(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        result = run_cli(["full-score"], state_dir)
        data = json.loads(result.stdout)
        assert "composite" in data
        assert "dimensions" in data


class TestCLIReset:
    def test_reset(self, state_dir):
        run_cli(["start", "--seed", "42"], state_dir)
        run_cli(["reset"], state_dir)
        state_file = os.path.join(state_dir, "tn_state.json")
        assert not os.path.exists(state_file)
