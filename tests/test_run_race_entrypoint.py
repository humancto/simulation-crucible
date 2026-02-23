"""Thin-entrypoint wiring tests for run_race.py."""

import run_race


def test_main_delegates_to_orchestrator(monkeypatch):
    captured = {}

    def fake_run_main(**kwargs):
        captured.update(kwargs)

    monkeypatch.setattr(run_race.race_orchestrator, "run_main", fake_run_main)

    run_race.main()

    assert captured["script_dir"] == run_race.SCRIPT_DIR
    assert captured["base_port"] == run_race.BASE_PORT
    assert captured["agent_defs"] == run_race.AGENT_DEFS
    assert captured["run_preflight_cb"] == run_race._run_preflight
    assert captured["build_race_record_cb"] == run_race.build_race_record
    assert captured["append_race_record_cb"] == run_race.append_race_record
