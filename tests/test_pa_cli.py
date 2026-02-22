"""Tests for the Post-Apocalyptic CLI (state save/load roundtrip, subprocess)."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

CLI_PATH = os.path.join(PROJECT_ROOT, "pa_cli.py")


@pytest.fixture
def state_dir(tmp_path):
    """Provide a temporary state directory."""
    return str(tmp_path / "pa_state")


def _run(args, state_dir, check=True):
    """Run pa_cli.py as a subprocess."""
    env = os.environ.copy()
    env["PA_STATE_DIR"] = state_dir
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
        result = _run(["start", "--seed", "42", "--years", "5"], state_dir)
        assert "simulation started" in result.stdout.lower()

    def test_status_after_start(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["status"], state_dir)
        assert "Year 1" in result.stdout
        assert "New Dawn" in result.stdout

    def test_status_without_start(self, state_dir):
        result = _run(["status"], state_dir, check=False)
        assert result.returncode != 0


class TestCLIAdvance:
    def test_advance(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["advance"], state_dir)
        assert "Advanced to year" in result.stdout


class TestCLIStatePersistence:
    def test_state_roundtrip(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        _run(["advance"], state_dir)
        _run(["advance"], state_dir)
        result = _run(["status"], state_dir)
        assert "Year 3" in result.stdout

    def test_score(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["score"], state_dir)
        assert "population" in result.stdout.lower()

    def test_full_score(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["full-score"], state_dir)
        assert "composite" in result.stdout.lower()


class TestCLIActions:
    def test_build(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["build", "farm"], state_dir)
        assert "success" in result.stdout.lower()

    def test_set_governance(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["set-governance", "democracy"], state_dir)
        assert "democracy" in result.stdout.lower()

    def test_population(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["population"], state_dir)
        assert "farmer" in result.stdout.lower()

    def test_factions(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["factions"], state_dir)
        assert "iron guard" in result.stdout.lower()

    def test_neighbors(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        result = _run(["neighbors"], state_dir)
        assert "haven" in result.stdout.lower()


class TestCLIReset:
    def test_reset(self, state_dir):
        _run(["start", "--seed", "42", "--years", "5"], state_dir)
        _run(["reset"], state_dir)
        result = _run(["status"], state_dir, check=False)
        assert result.returncode != 0
