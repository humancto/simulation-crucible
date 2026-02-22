"""Tests for dr_cli.py -- CLI state save/load roundtrip and subprocess integration."""

import json
import os
import subprocess
import sys
import tempfile

import pytest


SCRIPT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLI_PATH = os.path.join(SCRIPT_DIR, "dr_cli.py")


class TestCLISaveLoadRoundtrip:
    """Test that save -> load preserves state correctly."""

    def test_save_load_roundtrip(self):
        from simulations.disaster_relief.simulation import DisasterReliefSim

        sim = DisasterReliefSim(seed=42, days=10)
        sim.advance_day()
        sim.deploy_rescue_team("downtown", 2)
        sim.distribute_supplies("riverside", "food_tons", 5)

        # Serialize
        data = sim.to_dict()
        json_str = json.dumps(data)

        # Deserialize
        restored_data = json.loads(json_str)
        restored = DisasterReliefSim.from_dict(restored_data)

        # Verify roundtrip
        assert restored.state.day == sim.state.day
        assert restored.seed == sim.seed
        assert restored.variant == sim.variant
        assert restored.completed == sim.completed
        assert len(restored.state.zones) == len(sim.state.zones)
        assert restored.state.zones["downtown"].rescue_teams_deployed == 2

    def test_json_roundtrip_to_file(self, tmp_path):
        from simulations.disaster_relief.simulation import DisasterReliefSim

        sim = DisasterReliefSim(seed=42, days=10)
        sim.advance_day()
        data = sim.to_dict()

        # Write to file
        state_file = tmp_path / "dr_state.json"
        with open(state_file, "w") as f:
            json.dump(data, f)

        # Read back
        with open(state_file) as f:
            loaded = json.load(f)

        restored = DisasterReliefSim.from_dict(loaded)
        assert restored.state.day == 2
        assert restored.seed == 42


class TestCLISubprocess:
    """Test CLI as subprocess (integration)."""

    def _run(self, *args, state_dir=None):
        env = os.environ.copy()
        if state_dir:
            env["DR_STATE_DIR"] = state_dir
        result = subprocess.run(
            [sys.executable, CLI_PATH] + list(args),
            capture_output=True, text=True, env=env,
            cwd=SCRIPT_DIR,
        )
        return result

    def test_start_command(self, tmp_path):
        r = self._run("start", "--seed", "42", "--days", "10",
                       state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "Disaster Relief Commander" in r.stdout

    def test_status_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("status", state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "Day" in r.stdout

    def test_advance_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("advance", state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "Day" in r.stdout

    def test_zones_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("zones", state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "downtown" in r.stdout
        assert "riverside" in r.stdout

    def test_score_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("score", state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "Lives Saved" in r.stdout

    def test_full_score_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("full-score", state_dir=str(tmp_path))
        assert r.returncode == 0
        output = json.loads(r.stdout)
        assert "composite" in output
        assert "dimensions" in output

    def test_fingerprint_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("fingerprint", state_dir=str(tmp_path))
        assert r.returncode == 0
        fp = json.loads(r.stdout)
        assert len(fp) == 12

    def test_reset_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("reset", state_dir=str(tmp_path))
        assert r.returncode == 0
        assert "reset" in r.stdout.lower()

    def test_deploy_rescue_command(self, tmp_path):
        self._run("start", "--seed", "42", "--days", "10",
                   state_dir=str(tmp_path))
        r = self._run("deploy-rescue", "downtown", "--count", "1",
                       state_dir=str(tmp_path))
        assert r.returncode == 0

    def test_no_sim_error(self, tmp_path):
        r = self._run("status", state_dir=str(tmp_path))
        assert r.returncode != 0
