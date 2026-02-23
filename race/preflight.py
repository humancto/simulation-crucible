"""Pre-flight checks and agent availability helpers for run_race."""

import json
import os
import shutil
import subprocess
from typing import Callable, Dict, List, Optional, Sequence, Tuple


PreflightRow = Tuple[str, bool, str]


def check_agent_available(agent_defs: Dict[str, dict], agent_type: str) -> Tuple[bool, str, str]:
    """Check if an agent CLI tool is installed and accessible."""
    defn = agent_defs.get(agent_type)
    if not defn:
        return False, "", f"Unknown agent type: {agent_type}"

    binary = defn["binary"]

    if not shutil.which(binary):
        return False, "", f"'{binary}' not found on PATH. Install it first."

    try:
        result = subprocess.run(
            defn["check_version"],
            capture_output=True,
            text=True,
            timeout=15,
        )
        version = result.stdout.strip() or result.stderr.strip()
        version = version[:80]
        return True, version, ""
    except FileNotFoundError:
        return False, "", f"'{binary}' not found."
    except subprocess.TimeoutExpired:
        return True, "(version unknown)", ""
    except Exception as exc:
        return False, "", str(exc)


def check_api_key(
    agent_defs: Dict[str, dict],
    agent_type: str,
    env: Optional[Dict[str, str]] = None,
) -> Tuple[bool, str]:
    """Check if the expected API key env var is set."""
    if env is None:
        env = os.environ

    defn = agent_defs.get(agent_type)
    if not defn:
        return False, ""
    key_name = defn.get("env_key", "")
    if not key_name:
        return True, ""
    value = env.get(key_name, "")
    if value:
        return True, key_name
    return False, key_name


def detect_model(agent_type: str) -> Tuple[str, str]:
    """Auto-detect configured/available model for an agent CLI."""
    if agent_type == "codex":
        for path in ["~/.codex/config.toml", "~/.config/codex/config.toml"]:
            expanded = os.path.expanduser(path)
            if os.path.exists(expanded):
                try:
                    with open(expanded) as f:
                        for line in f:
                            line = line.strip()
                            if line.startswith("model") and "=" in line:
                                model = line.split("=", 1)[1].strip().strip('"').strip("'")
                                return model, f"from {path}"
                except Exception:
                    pass
        return "o4-mini", "default fallback"

    if agent_type == "gemini":
        settings_path = os.path.expanduser("~/.gemini/settings.json")
        if os.path.exists(settings_path):
            try:
                with open(settings_path) as f:
                    settings = json.load(f)
                model = settings.get("model") or settings.get("defaultModel")
                if model:
                    return model, "from ~/.gemini/settings.json"
            except Exception:
                pass
        return "gemini-2.5-pro", "default"

    if agent_type == "claude":
        return "claude (auto)", "CLI default"

    return "unknown", "not detected"


def run_preflight(
    agent_defs: Dict[str, dict],
    agent_types: Sequence[str],
    check_agent_available_cb: Callable[[str], Tuple[bool, str, str]],
    check_api_key_cb: Callable[[str], Tuple[bool, str]],
    detect_model_cb: Callable[[str], Tuple[str, str]],
    print_fn: Callable[[str], None] = print,
) -> List[PreflightRow]:
    """Run preflight checks and print status lines."""
    print_fn("  PRE-FLIGHT CHECKS")
    print_fn("  -----------------")

    results: List[PreflightRow] = []
    for atype in sorted(set(agent_types)):
        defn = agent_defs.get(atype, {})
        display = defn.get("display", atype)

        available, version, error = check_agent_available_cb(atype)
        has_key, key_name = check_api_key_cb(atype)
        model, model_source = detect_model_cb(atype)

        if available:
            print_fn(f"  [OK]   {display:<20} {version}")
            print_fn(f"         Model: {model} ({model_source})")
            if not has_key:
                if atype == "gemini":
                    print_fn("         Auth: OAuth (personal) — no API key needed")
                elif atype == "codex":
                    print_fn("         Auth: checking login status...")
                else:
                    print_fn(f"         WARNING: {key_name} not set — agent may fail to authenticate")
            else:
                print_fn(f"         Auth: {key_name} set")
            results.append((atype, True, model))
        else:
            print_fn(f"  [MISS] {display:<20} {error}")
            results.append((atype, False, error))

    print_fn("")
    return results


def build_final_agent_lists(
    raw_names: Sequence[str],
    agent_types: Sequence[str],
    model_overrides: Sequence[Optional[str]],
    preflight_rows: Sequence[PreflightRow],
) -> Tuple[List[str], List[str], List[Optional[str]], List[Tuple[str, str]]]:
    """Build filtered final agent lists from preflight results."""
    available_types = {atype for atype, ok, _ in preflight_rows if ok}

    final_names: List[str] = []
    final_types: List[str] = []
    final_models: List[Optional[str]] = []
    missing_agents: List[Tuple[str, str]] = []

    for i, (name, atype) in enumerate(zip(raw_names, agent_types)):
        if atype in available_types:
            final_names.append(name)
            final_types.append(atype)
            override = model_overrides[i] if i < len(model_overrides) else None
            final_models.append(override)
        else:
            missing_agents.append((name, atype))

    return final_names, final_types, final_models, missing_agents
