"""Tests for run_race result-file persistence helpers."""

import json
from types import SimpleNamespace

import run_race


def test_append_race_record_creates_new_file(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    monkeypatch.setattr(run_race, "get_git_commit_sha", lambda: "deadbeef")
    monkeypatch.setattr(run_race, "detect_model", lambda atype: (f"{atype}-model", "test"))
    prompt_file = tmp_path / "prompts" / "vending_machine" / "soft_guidelines.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text("test prompt", encoding="utf-8")
    record = {
        "simulation": "vending_machine",
        "seed": 42,
        "agents": ["claude"],
        "agent_types": ["claude"],
        "results": [],
    }

    run_race.append_race_record("results/test_results.json", record)

    out_file = tmp_path / "results" / "test_results.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert len(data) == 1
    assert data[0]["simulation"] == "vending_machine"
    assert "manifest" in data[0]
    manifest = data[0]["manifest"]
    assert manifest["schema_version"] == "race_manifest_v1"
    assert manifest["git_commit_sha"] == "deadbeef"
    assert manifest["simulation_id"] == "vending_machine"
    assert manifest["seed"] == 42
    assert manifest["detected_models"]["claude"]["model"] == "claude-model"
    assert manifest["prompt"]["path"] == "prompts/vending_machine/soft_guidelines.md"
    assert len(manifest["prompt"]["sha256"]) == 64


def test_append_race_record_appends_to_existing_json(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    monkeypatch.setattr(run_race, "get_git_commit_sha", lambda: "deadbeef")
    monkeypatch.setattr(run_race, "detect_model", lambda atype: (f"{atype}-model", "test"))
    out_file = tmp_path / "results" / "test_results.json"
    out_file.parent.mkdir(parents=True)
    out_file.write_text(json.dumps([{"simulation": "a"}]))

    run_race.append_race_record("results/test_results.json", {"simulation": "b"})
    data = json.loads(out_file.read_text())
    assert data[0] == {"simulation": "a"}
    assert data[1]["simulation"] == "b"
    assert data[1]["manifest"]["schema_version"] == "race_manifest_v1"


def test_append_race_record_recovers_from_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    monkeypatch.setattr(run_race, "get_git_commit_sha", lambda: "deadbeef")
    monkeypatch.setattr(run_race, "detect_model", lambda atype: (f"{atype}-model", "test"))
    out_file = tmp_path / "results" / "test_results.json"
    out_file.parent.mkdir(parents=True)
    out_file.write_text("{invalid json")

    run_race.append_race_record("results/test_results.json", {"simulation": "fresh"})
    data = json.loads(out_file.read_text())
    assert data[0]["simulation"] == "fresh"
    assert data[0]["manifest"]["schema_version"] == "race_manifest_v1"


def test_build_race_record_adds_model_metadata_to_record_and_results(monkeypatch):
    monkeypatch.setattr(run_race, "detect_model", lambda atype: (f"{atype}-detected", "test"))
    args = SimpleNamespace(seed=7, variant="hard_rules", days=12)
    raw_results = [{"agent": "codex", "agent_type": "codex", "final_balance": 99}]

    record = run_race.build_race_record(
        simulation_id="vending_machine",
        args=args,
        agent_names=["codex"],
        agent_types=["codex"],
        model_overrides=["o4-mini"],
        results=raw_results,
    )

    assert record["simulation"] == "vending_machine"
    assert record["days"] == 12
    assert record["agent_models"][0]["requested_model"] == "o4-mini"
    assert record["agent_models"][0]["effective_model"] == "o4-mini"
    assert record["results"][0]["effective_model"] == "o4-mini"
    assert record["results"][0]["detected_model"] == "codex-detected"
