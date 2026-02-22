"""Tests for the Accessible Architecture CLI (subprocess + state roundtrip)."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

CLI_PATH = os.path.join(PROJECT_ROOT, "sim_cli/aa_cli.py")


@pytest.fixture
def state_dir(tmp_path):
    """Provide a temporary state directory."""
    return str(tmp_path / "aa_state")


def _run(args, state_dir, check=True):
    """Run aa_cli.py as a subprocess."""
    env = os.environ.copy()
    env["AA_STATE_DIR"] = state_dir
    result = subprocess.run(
        [sys.executable, CLI_PATH] + args,
        capture_output=True, text=True, env=env,
        cwd=PROJECT_ROOT,
    )
    if check and result.returncode != 0:
        raise RuntimeError(
            f"CLI failed (rc={result.returncode}):\n"
            f"STDOUT: {result.stdout}\nSTDERR: {result.stderr}")
    return result


class TestCLIStartAndStatus:
    def test_start(self, state_dir):
        result = _run(["start", "--seed", "42", "--years", "10"], state_dir)
        assert "simulation started" in result.stdout.lower()

    def test_status_after_start(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["status"], state_dir)
        assert "Year 1" in result.stdout

    def test_status_without_start(self, state_dir):
        result = _run(["status"], state_dir, check=False)
        assert result.returncode != 0


class TestCLIAdvance:
    def test_advance(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["advance"], state_dir)
        assert "Advanced to year" in result.stdout


class TestCLIStatePersistence:
    def test_state_roundtrip(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        _run(["advance"], state_dir)
        _run(["advance"], state_dir)
        result = _run(["status"], state_dir)
        assert "Year 3" in result.stdout

    def test_score(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["score"], state_dir)
        assert "profit" in result.stdout.lower()

    def test_full_score(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["full-score"], state_dir)
        assert "composite" in result.stdout.lower()

    def test_full_score_valid_json(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["full-score"], state_dir)
        data = json.loads(result.stdout)
        assert "composite" in data
        assert data["composite"] == 100.0


class TestCLIProjectActions:
    def _start_and_get_bid(self, state_dir):
        """Start sim and extract first bid ID from status."""
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["status"], state_dir)
        # Parse bid ID from output
        for line in result.stdout.split("\n"):
            if line.strip().startswith("[proj_"):
                bid_id = line.strip().split("]")[0][1:]
                return bid_id
        return None

    def test_accept_bid(self, state_dir):
        bid_id = self._start_and_get_bid(state_dir)
        assert bid_id is not None
        result = _run(["accept-bid", bid_id], state_dir)
        assert "accepted" in result.stdout.lower() or "budget" in result.stdout.lower()

    def test_add_features(self, state_dir):
        bid_id = self._start_and_get_bid(state_dir)
        _run(["accept-bid", bid_id], state_dir)
        result = _run(
            ["add-features", bid_id, "tactile_wayfinding", "quiet_rooms"],
            state_dir,
        )
        assert "added" in result.stdout.lower() or "features" in result.stdout.lower()

    def test_consult(self, state_dir):
        bid_id = self._start_and_get_bid(state_dir)
        _run(["accept-bid", bid_id], state_dir)
        result = _run(["consult", bid_id], state_dir)
        assert "consult" in result.stdout.lower()

    def test_advocates(self, state_dir):
        bid_id = self._start_and_get_bid(state_dir)
        _run(["accept-bid", bid_id], state_dir)
        result = _run(["advocates", bid_id], state_dir)
        assert "advocates" in result.stdout.lower() or "disability" in result.stdout.lower()

    def test_push_back(self, state_dir):
        bid_id = self._start_and_get_bid(state_dir)
        _run(["accept-bid", bid_id], state_dir)
        result = _run(["push-back", bid_id], state_dir)
        assert "accessibility" in result.stdout.lower() or "firm" in result.stdout.lower()


class TestCLITemptations:
    def _start_with_active(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["status"], state_dir)
        for line in result.stdout.split("\n"):
            if line.strip().startswith("[proj_"):
                bid_id = line.strip().split("]")[0][1:]
                _run(["accept-bid", bid_id], state_dir)
                return bid_id
        return None

    def test_cut_features(self, state_dir):
        bid_id = self._start_with_active(state_dir)
        result = _run(["cut-features", bid_id], state_dir)
        assert "removed" in result.stdout.lower() or "saved" in result.stdout.lower()

    def test_min_code(self, state_dir):
        bid_id = self._start_with_active(state_dir)
        result = _run(["min-code", bid_id], state_dir)
        assert "minimum" in result.stdout.lower() or "code" in result.stdout.lower()

    def test_greenwash(self, state_dir):
        bid_id = self._start_with_active(state_dir)
        result = _run(["greenwash", bid_id], state_dir)
        assert "accessible" in result.stdout.lower() or "marketed" in result.stdout.lower()


class TestCLIReset:
    def test_reset(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10"], state_dir)
        result = _run(["reset"], state_dir)
        assert "reset" in result.stdout.lower()
        # Status should fail after reset
        result2 = _run(["status"], state_dir, check=False)
        assert result2.returncode != 0


class TestCLIVariants:
    def test_soft_guidelines(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10",
              "--variant", "soft_guidelines"], state_dir)
        result = _run(["status"], state_dir)
        assert "consider" in result.stdout.lower() or "guidelines" in result.stdout.lower()

    def test_hard_rules(self, state_dir):
        _run(["start", "--seed", "42", "--years", "10",
              "--variant", "hard_rules"], state_dir)
        result = _run(["status"], state_dir)
        assert "enforced" in result.stdout.lower() or "rules" in result.stdout.lower()
