"""Tests for race/config.py parsing helpers."""

import os

from race import config as race_config


def test_build_simulation_flags_marks_only_target_true():
    flags = race_config.build_simulation_flags("prisoners_dilemma")
    assert flags["is_ipd"] is True
    assert sum(1 for value in flags.values() if value) == 1


def test_parse_agent_inputs_handles_model_overrides_and_unknown_types():
    warnings = []

    def get_agent_type(name):
        if name == "codex":
            return "codex"
        return None

    raw_names, model_overrides, agent_types = race_config.parse_agent_inputs(
        "codex,mystery-2",
        "o4-mini,-",
        get_agent_type,
        warn_fn=warnings.append,
    )

    assert raw_names == ["codex", "mystery-2"]
    assert model_overrides == ["o4-mini", None]
    assert agent_types == ["codex", "mystery"]
    assert warnings == ["  WARNING: Unknown agent type 'mystery-2', will use Claude CLI as fallback"]


def test_parse_run_configuration_creates_results_dir_and_derives_types(tmp_path):
    old_cwd = os.getcwd()

    def get_agent_type(name):
        return "codex" if name == "codex" else None

    try:
        args, sim_flags, raw_names, model_overrides, agent_types = race_config.parse_run_configuration(
            script_dir=str(tmp_path),
            base_port=5050,
            simulation_choices=["vending_machine", "prisoners_dilemma"],
            get_agent_type_cb=get_agent_type,
            argv=[
                "--agents",
                "codex",
                "--simulation",
                "vending_machine",
                "--results-file",
                "results/subdir/test.json",
            ],
            warn_fn=lambda _: None,
        )
    finally:
        os.chdir(old_cwd)

    assert args.simulation == "vending_machine"
    assert raw_names == ["codex"]
    assert model_overrides == [None]
    assert agent_types == ["codex"]
    assert sim_flags["is_ipd"] is False
    assert sim_flags["is_cp"] is False
    assert (tmp_path / "results" / "subdir").exists()
