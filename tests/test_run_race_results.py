"""Tests for run_race result-file persistence helpers."""

import json
from pathlib import Path

import run_race


def test_append_race_record_creates_new_file(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    record = {"simulation": "vending_machine", "seed": 42, "results": []}

    run_race.append_race_record("results/test_results.json", record)

    out_file = tmp_path / "results" / "test_results.json"
    assert out_file.exists()
    data = json.loads(out_file.read_text())
    assert data == [record]


def test_append_race_record_appends_to_existing_json(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    out_file = tmp_path / "results" / "test_results.json"
    out_file.parent.mkdir(parents=True)
    out_file.write_text(json.dumps([{"simulation": "a"}]))

    run_race.append_race_record("results/test_results.json", {"simulation": "b"})
    data = json.loads(out_file.read_text())
    assert data == [{"simulation": "a"}, {"simulation": "b"}]


def test_append_race_record_recovers_from_invalid_json(tmp_path, monkeypatch):
    monkeypatch.setattr(run_race, "SCRIPT_DIR", str(tmp_path))
    out_file = tmp_path / "results" / "test_results.json"
    out_file.parent.mkdir(parents=True)
    out_file.write_text("{invalid json")

    run_race.append_race_record("results/test_results.json", {"simulation": "fresh"})
    data = json.loads(out_file.read_text())
    assert data == [{"simulation": "fresh"}]
