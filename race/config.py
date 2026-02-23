"""Argument parsing and run configuration helpers for run_race.py."""

import argparse
import os
from typing import Callable, Dict, Iterable, List, Optional, Tuple


SIMULATION_FLAG_TO_ID = {
    "is_ipd": "prisoners_dilemma",
    "is_er": "emergency_room",
    "is_wb": "whistleblower",
    "is_cm": "content_moderator",
    "is_roe": "rules_of_engagement",
    "is_re": "reputation_economy",
    "is_dp": "drug_pricing",
    "is_ms": "mayor_splitsville",
    "is_ah": "auction_house",
    "is_pt": "poker_tournament",
    "is_rc": "resource_commons",
    "is_sc": "supply_chain",
    "is_pw": "pandemic_ward",
    "is_ad": "asteroid_defense",
    "is_st": "species_triage",
    "is_nl": "nuclear_launch",
    "is_ne": "news_editor",
    "is_lr": "last_restaurant",
    "is_fc": "flash_crash",
    "is_sf": "startup_founder",
    "is_re2": "real_estate",
    "is_oa": "organ_allocation",
    "is_et": "experimental_treatment",
    "is_pg": "pandemic_grand",
    "is_ds": "drone_strike",
    "is_im": "intelligence_mosaic",
    "is_pc": "pow_camp",
    "is_tp": "trolley_problem",
    "is_ps": "privacy_security",
    "is_sp": "school_principal",
    "is_hn": "hostage_negotiator",
    "is_hre": "hr_ethics",
    "is_bb": "bug_bounty",
    "is_is": "infrastructure_siege",
    "is_sm": "space_mission",
    "is_ct": "climate_tipping",
    "is_ac": "ai_containment",
    "is_ec": "ecosystem_collapse",
    "is_pp": "pollution_prosperity",
    "is_ge": "geoengineering",
    "is_dr": "disaster_relief",
    "is_cs": "colony_ship",
    "is_pa": "post_apocalyptic",
    "is_fs": "film_studio",
    "is_aa": "accessible_architecture",
    "is_tc": "territory_control",
    "is_tn": "trade_negotiation",
    "is_uc": "un_crisis",
    "is_cp": "civilization_planner",
}


def build_parser(base_port: int, simulation_choices: Iterable[str]) -> argparse.ArgumentParser:
    """Build run_race CLI parser."""
    parser = argparse.ArgumentParser(
        description="The Simulation Crucible — AI Race Runner",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
    # Vending Machine (default)
    python3 run_race.py --agents claude,codex,gemini --seed 42 --days 90

    # Prisoner's Dilemma
    python3 run_race.py --simulation prisoners_dilemma --agents claude,codex --seed 42 --rounds 100

    # Override models per agent (use '-' to keep default):
    python3 run_race.py --agents claude,codex --models opus,o4-mini

Agent types: claude, codex, gemini
Simulations: vending_machine, prisoners_dilemma
Duplicates auto-deduplicate: claude,claude -> claude-1, claude-2
        """,
    )
    parser.add_argument(
        "--simulation",
        type=str,
        default="vending_machine",
        choices=list(simulation_choices),
        help="Simulation type (default: vending_machine)",
    )
    parser.add_argument(
        "--agents",
        type=str,
        required=True,
        help="Comma-separated agent names (e.g., claude,codex,gemini)",
    )
    parser.add_argument("--seed", type=int, default=None, help="Random seed (same for all agents)")
    parser.add_argument("--days", type=int, default=90, help="Simulation days (vending_machine default: 90, intelligence_mosaic default: 30)")
    parser.add_argument("--rounds", type=int, default=100, help="Game rounds (prisoners_dilemma, default: 100)")
    parser.add_argument("--hours", type=int, default=72, help="Simulation hours (emergency_room default: 72, nuclear_launch default: 24, news_editor default: 48, flash_crash default: 120, drone_strike default: 48)")
    parser.add_argument("--weeks", type=int, default=8, help="Simulation weeks (whistleblower default: 8, supply_chain default: 52, last_restaurant default: 52, organ_allocation default: 52, pow_camp default: 52)")
    parser.add_argument("--quarters", type=int, default=12, help="Simulation quarters (drug_pricing default: 12, species_triage default: 40)")
    parser.add_argument("--months", type=int, default=24, help="Simulation months (mayor_splitsville default: 24, asteroid_defense, startup_founder default: 24, real_estate default: 36, experimental_treatment default: 18, pandemic_grand default: 24)")
    parser.add_argument("--sessions", type=int, default=10, help="Auction sessions (auction_house, default: 10)")
    parser.add_argument("--hands", type=int, default=20, help="Poker hands (poker_tournament, default: 20)")
    parser.add_argument("--seasons", type=int, default=30, help="Seasons (resource_commons, default: 30)")
    parser.add_argument("--years", type=int, default=30, help="Simulation years (climate_tipping default: 30, pollution_prosperity default: 20)")
    parser.add_argument("--base-port", type=int, default=base_port, help="Starting port (default: 5050)")
    parser.add_argument("--max-turns", type=int, default=800, help="Max agent turns (default: 800)")
    parser.add_argument("--results-file", type=str, default="results/race_results_v2.json", help="Results output file")
    parser.add_argument("--skip-missing", action="store_true", help="Skip missing agents instead of aborting")
    parser.add_argument("--no-constraints", action="store_true", help="Disable integrity constraints in agent prompt")
    parser.add_argument(
        "--models",
        type=str,
        default=None,
        help="Comma-separated model overrides per agent (e.g., 'opus,gpt-5.2-codex,gemini-2.5-flash'). Use '-' to keep the default for that agent.",
    )
    parser.add_argument(
        "--variant",
        type=str,
        default="soft_guidelines",
        choices=["unconstrained", "soft_guidelines", "hard_rules"],
        help="V2 ethical constraint variant (default: soft_guidelines)",
    )
    return parser


def build_simulation_flags(simulation_id: str) -> Dict[str, bool]:
    """Build boolean simulation flags keyed by run_race legacy names."""
    return {
        flag_name: simulation_id == sim_id
        for flag_name, sim_id in SIMULATION_FLAG_TO_ID.items()
    }


def parse_agent_inputs(
    agents_arg: str,
    models_arg: Optional[str],
    get_agent_type_cb: Callable[[str], Optional[str]],
    warn_fn: Callable[[str], None] = print,
) -> Tuple[List[str], List[Optional[str]], List[str]]:
    """Parse agent names, model overrides, and derived agent types."""
    raw_names = [n.strip().lower() for n in agents_arg.split(",") if n.strip()]
    if not raw_names:
        raise ValueError("No agents specified")

    model_overrides: List[Optional[str]] = [None] * len(raw_names)
    if models_arg:
        models_list = [m.strip() for m in models_arg.split(",")]
        for i, model in enumerate(models_list):
            if i < len(raw_names) and model and model != "-":
                model_overrides[i] = model

    agent_types: list[str] = []
    for name in raw_names:
        atype = get_agent_type_cb(name)
        if not atype:
            warn_fn(f"  WARNING: Unknown agent type '{name}', will use Claude CLI as fallback")
            atype = name.split("-")[0]
        agent_types.append(atype)

    return raw_names, model_overrides, agent_types


def parse_run_configuration(
    script_dir: str,
    base_port: int,
    simulation_choices: Iterable[str],
    get_agent_type_cb: Callable[[str], Optional[str]],
    argv: Optional[List[str]] = None,
    warn_fn: Callable[[str], None] = print,
):
    """Parse CLI and return prepared run configuration values."""
    parser = build_parser(base_port, simulation_choices)
    args = parser.parse_args(argv)

    results_dir = os.path.dirname(args.results_file)
    if results_dir:
        os.makedirs(os.path.join(script_dir, results_dir), exist_ok=True)

    os.chdir(script_dir)

    try:
        raw_names, model_overrides, agent_types = parse_agent_inputs(
            args.agents,
            args.models,
            get_agent_type_cb,
            warn_fn=warn_fn,
        )
    except ValueError:
        warn_fn("Error: No agents specified.")
        raise SystemExit(1)

    sim_flags = build_simulation_flags(args.simulation)
    return args, sim_flags, raw_names, model_overrides, agent_types
