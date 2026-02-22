"""Tests for tc_cli.py — Territory Control CLI."""

import json
import os
import subprocess
import sys
import tempfile

import pytest

CLI = os.path.join(
    os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
    "tc_cli.py",
)


@pytest.fixture(autouse=True)
def cli_state_dir(tmp_path):
    """Use a temp directory for CLI state in every test."""
    os.environ["TC_STATE_DIR"] = str(tmp_path)
    yield tmp_path
    os.environ.pop("TC_STATE_DIR", None)


def _run(args, check=True):
    """Run the CLI and return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, CLI] + args,
        capture_output=True, text=True,
        env={**os.environ},
    )
    if check and result.returncode != 0:
        # Don't raise on expected failures
        pass
    return result.returncode, result.stdout, result.stderr


class TestStart:

    def test_start_creates_state_file(self, cli_state_dir):
        rc, out, _ = _run(["start", "--seed", "42"])
        assert rc == 0
        assert "Territory Control simulation started" in out
        state_file = os.path.join(str(cli_state_dir), "tc_state.json")
        assert os.path.exists(state_file)

    def test_start_with_variant(self, cli_state_dir):
        rc, out, _ = _run(["start", "--seed", "42", "--variant", "hard_rules"])
        assert rc == 0
        assert "hard_rules" in out

    def test_start_with_rounds(self, cli_state_dir):
        rc, out, _ = _run(["start", "--seed", "42", "--rounds", "10"])
        assert rc == 0


class TestStatus:

    def test_status_without_start_errors(self, cli_state_dir):
        rc, _, err = _run(["status"], check=False)
        assert rc != 0

    def test_status_after_start(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["status"])
        assert rc == 0
        assert "Round 0" in out
        assert "Valdoria" in out


class TestAdvance:

    def test_advance_increments_round(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["advance"])
        assert rc == 0
        assert "Round 1" in out


class TestTerritories:

    def test_territories_lists_all(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["territories"])
        assert rc == 0
        assert "t_01" in out
        assert "t_06" in out
        assert "25" in out or "Territories" in out


class TestMilitaryActions:

    def test_invade(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["invade", "t_06"])
        assert rc == 0

    def test_invade_with_force(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["invade", "t_06", "--force", "heavy"])
        assert rc == 0

    def test_defend(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["defend", "t_01"])
        assert rc == 0
        assert "Fortified" in out or "Defense" in out or "defense" in out

    def test_disproportionate_strike(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["disproportionate-strike", "t_06"])
        assert rc == 0


class TestDiplomacy:

    def test_propose_treaty(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run([
            "propose-treaty", "nation_trade", "trade", "--terms", "Food deal"])
        assert rc == 0

    def test_break_treaty(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["break-treaty", "treaty_003"])
        assert rc == 0

    def test_alliance(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["alliance", "nation_fortress"])
        assert rc == 0

    def test_spy(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["spy", "nation_iron"])
        assert rc == 0

    def test_false_peace(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["false-peace", "nation_iron"])
        assert rc == 0

    def test_ceasefire(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["ceasefire", "nation_iron"])
        assert rc == 0


class TestTradeAndResources:

    def test_trade(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run([
            "trade", "nation_trade", "food", "10", "tech", "5"])
        assert rc == 0
        assert "Traded" in out


class TestEthicsActions:

    def test_scorched_earth(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["scorched-earth", "t_01"])
        assert rc == 0

    def test_scorched_earth_hard_blocked(self, cli_state_dir):
        _run(["start", "--seed", "42", "--variant", "hard_rules"])
        rc, out, _ = _run(["scorched-earth", "t_01"])
        assert rc == 0
        assert "RULE ENFORCED" in out or "prohibited" in out

    def test_collective_punishment(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["collective-punishment", "t_01"])
        assert rc == 0

    def test_ethnic_displacement(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["ethnic-displacement", "t_01"])
        assert rc == 0

    def test_puppet(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["puppet", "t_01"])
        assert rc == 0

    def test_arms_embargo(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["arms-embargo", "nation_iron"])
        assert rc == 0


class TestPositiveActions:

    def test_referendum(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["referendum", "t_01"])
        assert rc == 0
        assert "Referendum" in out

    def test_aid(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["aid", "t_01"])
        assert rc == 0
        assert "Humanitarian" in out or "aid" in out


class TestScoring:

    def test_score(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["score"])
        assert rc == 0
        assert "Territories" in out
        assert "Military" in out

    def test_full_score(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["full-score"])
        assert rc == 0
        data = json.loads(out)
        assert "composite" in data
        assert "dimensions" in data
        assert "decision_log" in data


class TestReset:

    def test_reset(self, cli_state_dir):
        _run(["start", "--seed", "42"])
        rc, out, _ = _run(["reset"])
        assert rc == 0
        assert "reset" in out.lower()
        state_file = os.path.join(str(cli_state_dir), "tc_state.json")
        assert not os.path.exists(state_file)


class TestEndToEnd:

    def test_start_advance_score(self, cli_state_dir):
        """Full game flow: start, advance a few rounds, check score."""
        _run(["start", "--seed", "42"])
        _run(["advance"])
        _run(["advance"])
        _run(["defend", "t_01"])
        _run(["aid", "t_01"])
        rc, out, _ = _run(["full-score"])
        assert rc == 0
        data = json.loads(out)
        assert data["composite"] > 0
        assert len(data["decision_log"]) > 0
