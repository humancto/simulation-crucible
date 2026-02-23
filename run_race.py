#!/usr/bin/env python3
"""
The Simulation Crucible — AI Race Runner

Thin entrypoint for race orchestration. Core orchestration and mode runners
live under `race/`.
"""

import os
import sys

from race import config as race_config
from race import execution as race_execution
from race import local_mode as race_local_mode
from race import orchestrator as race_orchestrator
from race import preflight as race_preflight
from race import results as race_results
from race import scenario_io as race_scenario_io
from race import server_mode as race_server_mode
from race.results import print_leaderboard
from race.scenario_registry import (
    get_scenario,
    scenario_duration_for_args,
    scenario_ids,
    scenario_label,
)

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_PORT = race_orchestrator.BASE_PORT
AGENT_DEFS = race_orchestrator.AGENT_DEFS

# Public compatibility surface retained for tests and external scripts.
__all__ = [
    "SCRIPT_DIR",
    "BASE_PORT",
    "AGENT_DEFS",
    "detect_model",
    "get_git_commit_sha",
    "build_race_record",
    "build_run_manifest",
    "append_race_record",
    "run_preflight",
    "main",
]


def detect_model(agent_type):
    """Auto-detect configured/available model for an agent CLI."""
    return race_orchestrator.detect_model(race_preflight, agent_type)


def get_git_commit_sha():
    """Return current git commit SHA, or empty string if unavailable."""
    return race_results.get_git_commit_sha(SCRIPT_DIR)


def build_race_record(
    simulation_id,
    args,
    agent_names,
    agent_types,
    model_overrides,
    results,
    duration_key=None,
    duration_value=None,
):
    """Build a standardized race record with per-agent model metadata."""
    return race_results.build_race_record(
        simulation_id=simulation_id,
        args=args,
        agent_names=agent_names,
        agent_types=agent_types,
        detect_model_cb=detect_model,
        get_scenario_cb=get_scenario,
        model_overrides=model_overrides,
        results=results,
        duration_key=duration_key,
        duration_value=duration_value,
    )


def build_run_manifest(results_file, race_record):
    """Build reproducibility metadata for a race record."""
    return race_results.build_run_manifest(
        results_file,
        race_record,
        script_dir=SCRIPT_DIR,
        detect_model_cb=detect_model,
        get_git_commit_sha_cb=get_git_commit_sha,
        argv=list(sys.argv),
    )


def append_race_record(results_file, race_record):
    """Append a race record to the JSON results file and print save location."""
    return race_results.append_race_record(
        SCRIPT_DIR,
        results_file,
        race_record,
        manifest_builder=build_run_manifest,
    )


def _run_preflight(agent_types):
    """Run preflight checks for selected agent types."""
    return race_preflight.run_preflight(
        AGENT_DEFS,
        agent_types,
        check_agent_available_cb=lambda atype: race_orchestrator.check_agent_available(
            AGENT_DEFS,
            race_preflight,
            atype,
        ),
        check_api_key_cb=lambda atype: race_orchestrator.check_api_key(
            AGENT_DEFS,
            race_preflight,
            atype,
        ),
        detect_model_cb=detect_model,
        print_fn=print,
    )


def run_preflight(agent_types):
    """Compatibility wrapper around preflight execution."""
    return _run_preflight(agent_types)


def _run_agent(agent_name, agent_type, port, prompt, max_turns, model_override=None):
    """Run one agent process for local/server mode runners."""
    return race_execution.run_agent(
        SCRIPT_DIR,
        AGENT_DEFS,
        race_orchestrator.api_post,
        agent_name,
        agent_type,
        port,
        prompt,
        max_turns,
        model_override=model_override,
    )


def _collect_score(port):
    """Collect a vending-mode score from a running server instance."""
    return race_execution.collect_score(race_orchestrator.api_get, port)


# ── Main ────────────────────────────────────────────────────────────────

def main():
    race_orchestrator.run_main(
        script_dir=SCRIPT_DIR,
        base_port=BASE_PORT,
        scenario_ids_cb=scenario_ids,
        scenario_label_cb=scenario_label,
        scenario_duration_for_args_cb=scenario_duration_for_args,
        get_scenario_cb=get_scenario,
        parse_run_configuration_cb=race_config.parse_run_configuration,
        build_final_agent_lists_cb=race_preflight.build_final_agent_lists,
        deduplicate_names_cb=race_orchestrator.deduplicate_names,
        run_preflight_cb=_run_preflight,
        detect_model_cb=detect_model,
        run_agent_cb=_run_agent,
        collect_score_cb=_collect_score,
        build_race_record_cb=build_race_record,
        append_race_record_cb=append_race_record,
        local_mode_runner_cb=race_local_mode.run_local_cli_race,
        server_mode_runner_cb=race_server_mode.run_vending_server_race,
        scenario_io_module=race_scenario_io,
        print_leaderboard_cb=print_leaderboard,
        agent_defs=AGENT_DEFS,
        print_fn=print,
        exit_fn=sys.exit,
    )


if __name__ == "__main__":
    main()
