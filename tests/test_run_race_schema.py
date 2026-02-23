"""Schema checks for race result artifacts."""

import json
from pathlib import Path
from types import SimpleNamespace

import jsonschema

import run_race


ROOT = Path(__file__).resolve().parent.parent
SCHEMA_PATH = ROOT / "race" / "schemas" / "race_record_v1.schema.json"


def test_race_record_schema_file_is_valid_json_schema():
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.Draft7Validator.check_schema(schema)


def test_generated_race_record_validates_against_schema(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    monkeypatch.setattr(run_race, "get_git_commit_sha", lambda: "deadbeef")
    monkeypatch.setattr(run_race, "detect_model", lambda atype: (f"{atype}-detected", "test"))

    prompt_file = tmp_path / "prompts" / "vending_machine" / "soft_guidelines.md"
    prompt_file.parent.mkdir(parents=True, exist_ok=True)
    prompt_file.write_text("prompt", encoding="utf-8")

    args = SimpleNamespace(seed=42, variant="soft_guidelines", days=90)
    raw_results = [
        {
            "agent": "codex",
            "agent_type": "codex",
            "final_balance": 123.0,
            "duration": 1.2,
            "error": "",
        }
    ]

    record = run_race.build_race_record(
        simulation_id="vending_machine",
        args=args,
        agent_names=["codex"],
        agent_types=["codex"],
        model_overrides=["o4-mini"],
        results=raw_results,
    )
    run_race.append_race_record("results/schema_test.json", record)

    saved = json.loads((tmp_path / "results" / "schema_test.json").read_text(encoding="utf-8"))[0]
    schema = json.loads(SCHEMA_PATH.read_text(encoding="utf-8"))
    jsonschema.validate(saved, schema)

    assert saved["agent_models"][0]["requested_model"] == "o4-mini"
    assert saved["agent_models"][0]["effective_model"] == "o4-mini"
    assert saved["results"][0]["effective_model"] == "o4-mini"
    assert saved["results"][0]["detected_model"] == "codex-detected"
