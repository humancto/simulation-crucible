"""Tests for scripts/replay_race.py."""

import json
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
REPLAY_SCRIPT = ROOT / "scripts" / "replay_race.py"


def run_replay(args):
    completed = subprocess.run(
        [sys.executable, str(REPLAY_SCRIPT), *args],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return completed.returncode, completed.stdout, completed.stderr


def test_replay_uses_manifest_argv_when_present(tmp_path):
    results_file = tmp_path / "results.json"
    payload = [
        {
            "manifest": {
                "schema_version": "race_manifest_v1",
                "argv": ["run_race.py", "--agents", "claude,codex", "--seed", "42"],
            }
        }
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    code, stdout, stderr = run_replay(["--results-file", str(results_file)])

    assert code == 0, stderr
    assert "Replay command:" in stdout
    assert "python3 run_race.py --agents claude,codex --seed 42" in stdout


def test_replay_falls_back_to_record_fields_without_manifest(tmp_path):
    results_file = tmp_path / "results.json"
    payload = [
        {
            "simulation": "prisoners_dilemma",
            "agent_types": ["claude", "codex"],
            "seed": 7,
            "variant": "hard_rules",
            "rounds": 100,
        }
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    code, stdout, stderr = run_replay(["--results-file", str(results_file)])

    assert code == 0, stderr
    assert "--simulation prisoners_dilemma" in stdout
    assert "--agents claude,codex" in stdout
    assert "--seed 7" in stdout
    assert "--variant hard_rules" in stdout
    assert "--rounds 100" in stdout


def test_replay_skips_none_seed_and_duration_values(tmp_path):
    results_file = tmp_path / "results.json"
    payload = [
        {
            "simulation": "news_editor",
            "agent_types": ["codex"],
            "seed": None,
            "variant": "soft_guidelines",
            "hours": None,
        }
    ]
    results_file.write_text(json.dumps(payload), encoding="utf-8")

    code, stdout, stderr = run_replay(["--results-file", str(results_file)])

    assert code == 0, stderr
    assert "--seed" not in stdout
    assert "--hours" not in stdout
