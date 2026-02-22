#!/usr/bin/env python3
"""Create scenario-based prompt layout from legacy AGENT_*.md files.

This script is idempotent and keeps legacy files untouched.
"""

from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parent.parent
PROMPTS_DIR = ROOT / "prompts"
LEGACY_DIR = PROMPTS_DIR / "_legacy"

CODE_TO_SCENARIO = {
    "ipd": "prisoners_dilemma",
    "er": "emergency_room",
    "wb": "whistleblower",
    "cm": "content_moderator",
    "roe": "rules_of_engagement",
    "re": "reputation_economy",
    "dp": "drug_pricing",
    "ms": "mayor_splitsville",
    "ah": "auction_house",
    "pt": "poker_tournament",
    "rc": "resource_commons",
    "sc": "supply_chain",
    "pw": "pandemic_ward",
    "ad": "asteroid_defense",
    "st": "species_triage",
    "nl": "nuclear_launch",
    "ne": "news_editor",
    "lr": "last_restaurant",
    "fc": "flash_crash",
    "sf": "startup_founder",
    "re2": "real_estate",
    "oa": "organ_allocation",
    "et": "experimental_treatment",
    "pg": "pandemic_grand",
    "ds": "drone_strike",
    "im": "intelligence_mosaic",
    "pc": "pow_camp",
    "tp": "trolley_problem",
    "ps": "privacy_security",
    "sp": "school_principal",
    "hn": "hostage_negotiator",
    "hr": "hr_ethics",
    "bb": "bug_bounty",
    "is": "infrastructure_siege",
    "sm": "space_mission",
    "ct": "climate_tipping",
    "ac": "ai_containment",
    "ec": "ecosystem_collapse",
    "pp": "pollution_prosperity",
    "ge": "geoengineering",
    "dr": "disaster_relief",
    "cs": "colony_ship",
    "pa": "post_apocalyptic",
    "fs": "film_studio",
    "aa": "accessible_architecture",
    "tc": "territory_control",
    "tn": "trade_negotiation",
    "uc": "un_crisis",
    "cp": "civilization_planner",
}


def copy_if_exists(src: Path, dst: Path):
    if src.exists():
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)
        return True
    return False


def copy_from_sources(filename: str, dst: Path):
    """Copy from repo root first, then prompts/_legacy fallback."""
    root_src = ROOT / filename
    if root_src.exists():
        return copy_if_exists(root_src, dst)
    legacy_src = LEGACY_DIR / filename
    return copy_if_exists(legacy_src, dst)


def main() -> int:
    PROMPTS_DIR.mkdir(parents=True, exist_ok=True)

    copied = 0

    # Vending machine (legacy unprefixed AGENT files)
    vending = PROMPTS_DIR / "vending_machine"
    copied += int(copy_from_sources("AGENT.md", vending / "default.md"))
    copied += int(copy_from_sources("AGENT_unconstrained.md", vending / "unconstrained.md"))
    copied += int(copy_from_sources("AGENT_soft.md", vending / "soft_guidelines.md"))
    copied += int(copy_from_sources("AGENT_hard.md", vending / "hard_rules.md"))

    # Scenario prompts by short code
    for code, scenario in CODE_TO_SCENARIO.items():
        scenario_dir = PROMPTS_DIR / scenario
        copied += int(copy_from_sources(f"AGENT_{code}_unconstrained.md", scenario_dir / "unconstrained.md"))
        copied += int(copy_from_sources(f"AGENT_{code}_soft.md", scenario_dir / "soft_guidelines.md"))
        copied += int(copy_from_sources(f"AGENT_{code}_hard.md", scenario_dir / "hard_rules.md"))

    readme = PROMPTS_DIR / "README.md"
    readme.write_text(
        "# Scenario Prompt Layout\n\n"
        "Each scenario has three variants:\n"
        "- `unconstrained.md`\n"
        "- `soft_guidelines.md`\n"
        "- `hard_rules.md`\n\n"
        "Legacy `AGENT_*.md` files are kept for backward compatibility.\n"
    )

    print(f"Prompt migration complete. Files copied: {copied}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
