"""Tests for fs_cli.py -- Film Studio CLI."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI = os.path.join(SCRIPT_DIR, "fs_cli.py")


def run_cli(*args, state_dir=None):
    """Run the CLI with optional state directory."""
    env = os.environ.copy()
    if state_dir:
        env["FS_STATE_DIR"] = state_dir
    result = subprocess.run(
        [sys.executable, CLI] + list(args),
        capture_output=True, text=True, env=env,
        cwd=SCRIPT_DIR,
    )
    return result


class TestCLIStart:

    def test_start_creates_state(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        result = run_cli("start", "--seed", "42", state_dir=state_dir)
        assert result.returncode == 0
        assert "Film Studio Green-Light simulation started" in result.stdout
        assert os.path.exists(os.path.join(state_dir, "fs_state.json"))

    def test_start_with_variant(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        result = run_cli("start", "--seed", "42", "--variant", "hard_rules",
                         state_dir=state_dir)
        assert result.returncode == 0
        assert "hard_rules" in result.stdout


class TestCLIStatus:

    def test_status_requires_start(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        result = run_cli("status", state_dir=state_dir)
        assert result.returncode != 0

    def test_status_after_start(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("status", state_dir=state_dir)
        assert result.returncode == 0
        assert "Year 1" in result.stdout


class TestCLIAdvance:

    def test_advance(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("advance", state_dir=state_dir)
        assert result.returncode == 0
        assert "Year 2" in result.stdout


class TestCLIPitches:

    def test_pitches(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("pitches", state_dir=state_dir)
        assert result.returncode == 0
        assert "Film Pitches" in result.stdout


class TestCLIGreenlight:

    def test_greenlight(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("greenlight", "film_y1_0", state_dir=state_dir)
        assert result.returncode == 0
        assert "Greenlit" in result.stdout


class TestCLIShelve:

    def test_shelve(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("shelve", "film_y1_0", state_dir=state_dir)
        assert result.returncode == 0
        assert "Shelved" in result.stdout


class TestCLITemptations:

    def test_overtime(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("overtime", "vfx", state_dir=state_dir)
        assert result.returncode == 0

    def test_replace_ai(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("replace-ai", "animation", state_dir=state_dir)
        assert result.returncode == 0

    def test_whitewash(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("whitewash", "film_y1_0", state_dir=state_dir)
        assert result.returncode == 0

    def test_franchise(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("franchise", "film_y1_0", state_dir=state_dir)
        assert result.returncode == 0


class TestCLIPositive:

    def test_invest_diversity(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("invest-diversity", "--amount", "10",
                         state_dir=state_dir)
        assert result.returncode == 0
        assert "diversity" in result.stdout.lower() or "Invested" in result.stdout

    def test_fair_pay(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("fair-pay", "vfx", state_dir=state_dir)
        assert result.returncode == 0


class TestCLIScoring:

    def test_score(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("score", state_dir=state_dir)
        assert result.returncode == 0
        assert "Profit" in result.stdout

    def test_full_score(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("full-score", state_dir=state_dir)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert "composite" in data
        assert "dimensions" in data
        assert "decision_log" in data

    def test_fingerprint(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("fingerprint", state_dir=state_dir)
        assert result.returncode == 0
        data = json.loads(result.stdout)
        assert len(data) == 12


class TestCLIReset:

    def test_reset(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        run_cli("start", "--seed", "42", state_dir=state_dir)
        result = run_cli("reset", state_dir=state_dir)
        assert result.returncode == 0
        assert "reset" in result.stdout.lower()


class TestCLIHelp:

    def test_no_args_shows_help(self, tmp_path):
        state_dir = str(tmp_path / "fs_state")
        result = run_cli(state_dir=state_dir)
        assert result.returncode != 0  # exits with error code
