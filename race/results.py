"""Result presentation and persistence helpers for race runs."""

import hashlib
import json
import os
import platform
import shlex
import subprocess
import time


def get_git_commit_sha(script_dir):
    """Return current git commit SHA, or empty string if unavailable."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=script_dir,
            capture_output=True,
            text=True,
            timeout=5,
        )
        if result.returncode == 0:
            return result.stdout.strip()
    except Exception:
        pass
    return ""


def sha256_file(path):
    """Return SHA-256 hex digest for a file path."""
    digest = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(8192), b""):
            digest.update(chunk)
    return digest.hexdigest()


def prompt_artifact(script_dir, simulation_id, variant):
    """Return prompt metadata for a simulation+variant pair."""
    prompt_rel = os.path.join("prompts", simulation_id, f"{variant}.md")
    prompt_abs = os.path.join(script_dir, prompt_rel)
    if not os.path.exists(prompt_abs):
        return {"path": prompt_rel, "sha256": None}
    try:
        return {"path": prompt_rel, "sha256": sha256_file(prompt_abs)}
    except OSError:
        return {"path": prompt_rel, "sha256": None}


def race_duration_field(race_record):
    """Extract duration field as {'key': <unit>, 'value': <n>} if present."""
    for key in (
        "days",
        "hours",
        "weeks",
        "months",
        "quarters",
        "rounds",
        "sessions",
        "hands",
        "seasons",
        "years",
    ):
        if key in race_record:
            return {"key": key, "value": race_record.get(key)}
    return {"key": None, "value": None}


def detected_models_for_record(race_record, detect_model_cb):
    """Return best-effort model metadata by agent type."""
    detected = {}
    for atype in sorted(set(race_record.get("agent_types", []))):
        model, source = detect_model_cb(atype)
        detected[atype] = {"model": model, "source": source}
    return detected


def build_agent_model_records(agent_names, agent_types, detect_model_cb, model_overrides=None):
    """Build per-agent requested/detected/effective model metadata."""
    if model_overrides is None:
        model_overrides = [None] * len(agent_names)

    records = []
    for i, (name, atype) in enumerate(zip(agent_names, agent_types)):
        requested_model = None
        if i < len(model_overrides):
            requested_model = model_overrides[i]
        detected_model, detected_source = detect_model_cb(atype)
        effective_model = requested_model or detected_model
        records.append(
            {
                "agent": name,
                "agent_type": atype,
                "requested_model": requested_model,
                "detected_model": detected_model,
                "detected_model_source": detected_source,
                "effective_model": effective_model,
            }
        )
    return records


def add_model_metadata_to_results(results, agent_model_records):
    """Attach model metadata to each result row by agent name."""
    model_by_agent = {entry["agent"]: entry for entry in agent_model_records}
    enriched = []
    for row in results:
        if not isinstance(row, dict):
            enriched.append(row)
            continue
        out = dict(row)
        agent_name = out.get("agent")
        meta = model_by_agent.get(agent_name)
        if meta:
            out["requested_model"] = meta.get("requested_model")
            out["detected_model"] = meta.get("detected_model")
            out["detected_model_source"] = meta.get("detected_model_source")
            out["effective_model"] = meta.get("effective_model")
        enriched.append(out)
    return enriched


def build_race_record(
    simulation_id,
    args,
    agent_names,
    agent_types,
    detect_model_cb,
    get_scenario_cb,
    model_overrides=None,
    results=None,
    duration_key=None,
    duration_value=None,
):
    """Build a standardized race record with per-agent model metadata."""
    if results is None:
        results = []

    spec = get_scenario_cb(simulation_id)
    duration_key = duration_key or spec.duration_arg
    if duration_value is None:
        duration_value = getattr(args, duration_key)

    agent_models = build_agent_model_records(
        agent_names,
        agent_types,
        detect_model_cb=detect_model_cb,
        model_overrides=model_overrides,
    )
    return {
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "simulation": simulation_id,
        "seed": args.seed,
        duration_key: duration_value,
        "variant": args.variant,
        "agents": list(agent_names),
        "agent_types": list(agent_types),
        "agent_models": agent_models,
        "results": add_model_metadata_to_results(results, agent_models),
    }


def build_run_manifest(
    results_file,
    race_record,
    script_dir,
    detect_model_cb,
    get_git_commit_sha_cb=None,
    argv=None,
):
    """Build reproducibility metadata for a race record."""
    simulation_id = race_record.get("simulation") or "vending_machine"
    variant = race_record.get("variant") or "soft_guidelines"
    duration = race_duration_field(race_record)
    prompt = prompt_artifact(script_dir, simulation_id, variant)
    if get_git_commit_sha_cb is None:
        get_git_commit_sha_cb = lambda: get_git_commit_sha(script_dir)
    if argv is None:
        argv = []

    return {
        "schema_version": "race_manifest_v1",
        "created_at_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "git_commit_sha": get_git_commit_sha_cb(),
        "python_version": platform.python_version(),
        "platform": platform.platform(),
        "script_dir": script_dir,
        "argv": list(argv),
        "argv_shell_escaped": " ".join(shlex.quote(arg) for arg in argv),
        "results_file": results_file,
        "simulation_id": simulation_id,
        "variant": variant,
        "seed": race_record.get("seed"),
        "duration": duration,
        "agent_names": list(race_record.get("agents", [])),
        "agent_types": list(race_record.get("agent_types", [])),
        "agent_models": list(race_record.get("agent_models", [])),
        "detected_models": detected_models_for_record(race_record, detect_model_cb),
        "prompt": prompt,
    }


def append_race_record(script_dir, results_file, race_record, manifest_builder):
    """Append a race record to a JSON results file and print save location."""
    results_path = os.path.join(script_dir, results_file)
    results_dir = os.path.dirname(results_path)
    if results_dir:
        os.makedirs(results_dir, exist_ok=True)
    record_to_save = dict(race_record)
    record_to_save.setdefault("manifest", manifest_builder(results_file, record_to_save))
    existing = []
    if os.path.exists(results_path):
        try:
            with open(results_path) as f:
                existing = json.load(f)
        except (json.JSONDecodeError, IOError):
            existing = []
    existing.append(record_to_save)
    with open(results_path, "w") as f:
        json.dump(existing, f, indent=2)
    print(f"\n  Results saved to {results_file}")


def print_leaderboard(results):
    """Print the race leaderboard."""
    results.sort(key=lambda r: r.get("final_balance", -9999), reverse=True)

    print("\n" + "=" * 72)
    print("  VENDING MACHINE AI RACE — FINAL LEADERBOARD")
    print("=" * 72)
    print(f"  {'Rank':<6}{'Agent':<20}{'Type':<10}{'Balance':>10}{'Profit':>10}{'Items':>8}{'Time':>8}")
    print("-" * 72)

    medals = ["1st", "2nd", "3rd"]
    for i, result in enumerate(results):
        rank = medals[i] if i < 3 else f"{i+1}th"
        bankrupt = " BANKRUPT" if result.get("bankrupt") else ""
        duration = result.get("duration", 0)
        time_str = f"{duration:.0f}s" if duration else "--"
        print(
            f"  {rank:<6}"
            f"{result['agent']:<20}"
            f"{result.get('agent_type', '?'):<10}"
            f"${result.get('final_balance', 0):>8.2f}"
            f"${result.get('total_profit', 0):>8.2f}"
            f"{result.get('total_items_sold', 0):>8}"
            f"{time_str:>8}"
            f"{bankrupt}"
        )

    if results:
        winner = results[0]
        print(f"\n  WINNER: {winner['agent']} with ${winner.get('final_balance', 0):.2f}")

    print("=" * 72)
