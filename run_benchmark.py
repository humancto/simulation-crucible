#!/usr/bin/env python3
"""
Vending Machine AI Benchmark — Python Runner

Manages the server lifecycle, starts simulations, and collects scores.
Can run multiple AI models sequentially and produce a leaderboard.

Usage:
    python3 run_benchmark.py --claude                  # Run Claude Code
    python3 run_benchmark.py --claude --seed 42        # Reproducible
    python3 run_benchmark.py --manual                  # Manual mode
    python3 run_benchmark.py --leaderboard scores.json # View past scores
"""

import argparse
import json
import os
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DEFAULT_PORT = 5050


def load_vending_prompt():
    """Load vending-machine prompt, preferring scenario-based layout."""
    candidates = [
        os.path.join(SCRIPT_DIR, "prompts", "vending_machine", "default.md"),
        os.path.join(SCRIPT_DIR, "AGENT.md"),  # legacy fallback
    ]

    for path in candidates:
        if os.path.isfile(path):
            with open(path) as f:
                return f.read(), path

    raise FileNotFoundError(
        "Prompt file not found. Expected one of: "
        + ", ".join(candidates)
    )


def wait_for_server(port, timeout=30):
    """Wait for the server to respond."""
    for _ in range(timeout):
        try:
            req = urllib.request.Request(f"http://localhost:{port}/api/status")
            with urllib.request.urlopen(req, timeout=2):
                return True
        except Exception:
            time.sleep(1)
    return False


def api_post(port, path, data=None):
    """POST to the API."""
    payload = json.dumps(data or {}).encode()
    req = urllib.request.Request(
        f"http://localhost:{port}{path}",
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def api_get(port, path):
    """GET from the API."""
    req = urllib.request.Request(f"http://localhost:{port}{path}")
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        return json.loads(e.read())


def start_server(port):
    """Start the Flask server in background."""
    log = open("/tmp/vending-machine-server.log", "w")
    proc = subprocess.Popen(
        [sys.executable, "server.py", "--port", str(port)],
        cwd=SCRIPT_DIR,
        stdout=log,
        stderr=log,
    )
    return proc


def build_agent_prompt(days, seed, port):
    """Build the prompt for the AI agent."""
    instructions, _ = load_vending_prompt()

    seed_flag = f"--seed {seed}" if seed else ""

    return f"""{instructions}

---

# YOUR MISSION

The vending machine server is running at http://localhost:{port}.
You are playing the Vending Machine Business Simulation.

Your goal: **Maximize your final bank balance** over {days} simulated days.
You start with $500. You pay $2/day rent. The machine starts empty.

## RULES
- Run ALL commands from this directory: {SCRIPT_DIR}
- Use: python3 vm_cli.py sim <command>
- You must manage the business for ALL {days} days
- After the final day, run: python3 vm_cli.py sim score

## STRATEGY TIPS
- Order inventory ASAP on day 0 (delivery takes 1-3 days)
- Stock all 8 products for maximum revenue
- Use FreshCo for bulk orders (cheap, 2-day delivery)
- Use QuickStock for urgent restocks (fast, 1-day delivery)
- Search for more suppliers with: sim search "cheap"
- Restock the machine from storage daily
- Adjust prices based on season and weather
- Order more before weekends (higher demand)
- Keep notes to track your strategy

## BEGIN NOW
Start the simulation:
python3 vm_cli.py sim start --days {days} {seed_flag}

Then manage the business day by day until you complete all {days} days.
Good luck!"""


def run_claude(prompt, max_turns=800):
    """Launch Claude Code with the given prompt."""
    cmd = [
        "claude",
        "-p", prompt,
        "--allowedTools", "Bash",
        "--max-turns", str(max_turns),
    ]
    log_path = "/tmp/vending-benchmark-agent.log"
    with open(log_path, "w") as log:
        proc = subprocess.Popen(
            cmd,
            cwd=SCRIPT_DIR,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            env={**os.environ, "VM_URL": f"http://localhost:{DEFAULT_PORT}"},
        )
        for line in iter(proc.stdout.readline, b""):
            decoded = line.decode("utf-8", errors="replace")
            sys.stdout.write(decoded)
            log.write(decoded)
        proc.wait()
    print(f"\nAgent log: {log_path}")
    return proc.returncode


def collect_score(port):
    """Collect the final score from the simulation."""
    score = api_get(port, "/api/sim/score")
    if "error" in score:
        print(f"Could not get score: {score['error']}")
        return None
    return score


def save_score(score, model_name, scores_file):
    """Append score to the leaderboard file."""
    scores = []
    if os.path.exists(scores_file):
        with open(scores_file) as f:
            scores = json.load(f)

    entry = {
        "model": model_name,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        "final_balance": score.get("final_balance", 0),
        "total_revenue": score.get("total_revenue", 0),
        "total_costs": score.get("total_costs", 0),
        "total_profit": score.get("total_profit", 0),
        "items_sold": score.get("total_items_sold", 0),
        "days_played": score.get("total_days", 0),
        "bankrupt": score.get("bankrupt", False),
        "bankrupt_day": score.get("bankrupt_day"),
    }
    scores.append(entry)

    with open(scores_file, "w") as f:
        json.dump(scores, f, indent=2)

    return entry


def print_leaderboard(scores_file):
    """Print the leaderboard from saved scores."""
    if not os.path.exists(scores_file):
        print("No scores recorded yet.")
        return

    with open(scores_file) as f:
        scores = json.load(f)

    if not scores:
        print("No scores recorded yet.")
        return

    scores.sort(key=lambda s: s["final_balance"], reverse=True)

    print("\n" + "=" * 70)
    print("  VENDING MACHINE AI BENCHMARK — LEADERBOARD")
    print("=" * 70)
    print(f"  {'Rank':<6}{'Model':<25}{'Balance':>10}{'Profit':>10}{'Items':>8}{'Days':>6}")
    print("-" * 70)

    for i, s in enumerate(scores, 1):
        bankrupt = " (BANKRUPT)" if s.get("bankrupt") else ""
        print(
            f"  {i:<6}"
            f"{s['model']:<25}"
            f"${s['final_balance']:>8.2f}"
            f"${s['total_profit']:>8.2f}"
            f"{s['items_sold']:>8}"
            f"{s['days_played']:>6}"
            f"{bankrupt}"
        )

    print("=" * 70)
    print(f"  {len(scores)} run(s) recorded")
    print()


def print_score(score):
    """Print a single score nicely."""
    print("\n" + "=" * 60)
    print("  BENCHMARK RESULTS")
    print("=" * 60)
    print(f"  Days played:       {score.get('total_days', 0)}")
    print(f"  Final balance:     ${score.get('final_balance', 0):.2f}")
    print(f"  Starting balance:  ${score.get('starting_balance', 500):.2f}")
    print(f"  Total revenue:     ${score.get('total_revenue', 0):.2f}")
    print(f"  Total costs:       ${score.get('total_costs', 0):.2f}")
    print(f"  Net profit:        ${score.get('total_profit', 0):.2f}")
    print(f"  Items sold:        {score.get('total_items_sold', 0)}")
    print(f"  Avg daily revenue: ${score.get('avg_daily_revenue', 0):.2f}")
    if score.get("bankrupt"):
        print(f"  BANKRUPT on day {score.get('bankrupt_day', '?')}")
    print("=" * 60)


def main():
    parser = argparse.ArgumentParser(description="Vending Machine AI Benchmark Runner")
    parser.add_argument("--claude", action="store_true", help="Auto-launch Claude Code")
    parser.add_argument("--manual", action="store_true", help="Manual mode (just start server)")
    parser.add_argument("--seed", type=int, default=None, help="Random seed")
    parser.add_argument("--days", type=int, default=90, help="Simulation days (default: 90)")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Server port")
    parser.add_argument("--model-name", type=str, default="claude-code", help="Model name for leaderboard")
    parser.add_argument("--scores-file", type=str, default="scores.json", help="Leaderboard file")
    parser.add_argument("--leaderboard", action="store_true", help="Show leaderboard and exit")
    parser.add_argument("--max-turns", type=int, default=800, help="Max agent turns")
    args = parser.parse_args()

    os.chdir(SCRIPT_DIR)

    if args.leaderboard:
        print_leaderboard(os.path.join(SCRIPT_DIR, args.scores_file))
        return

    # Start server
    print("Starting server...")
    server = start_server(args.port)

    def cleanup(signum=None, frame=None):
        print("\nShutting down...")
        server.terminate()
        server.wait()
        sys.exit(0)

    signal.signal(signal.SIGINT, cleanup)
    signal.signal(signal.SIGTERM, cleanup)

    if not wait_for_server(args.port):
        print("Server failed to start. Check /tmp/vending-machine-server.log")
        server.terminate()
        sys.exit(1)

    print(f"Server running on port {args.port}")
    print(f"UI: http://localhost:{args.port}")
    print()

    try:
        if args.claude:
            try:
                prompt = build_agent_prompt(args.days, args.seed, args.port)
            except FileNotFoundError as exc:
                print(f"Error: {exc}")
                return
            print(f"Launching Claude Code ({args.days} days, seed: {args.seed or 'random'})...")
            print(f"Watch the UI: http://localhost:{args.port}")
            print()
            run_claude(prompt, max_turns=args.max_turns)

            score = collect_score(args.port)
            if score:
                print_score(score)
                entry = save_score(score, args.model_name, os.path.join(SCRIPT_DIR, args.scores_file))
                print(f"\nScore saved to {args.scores_file}")
                print_leaderboard(os.path.join(SCRIPT_DIR, args.scores_file))

        elif args.manual:
            # Start sim and wait
            seed_data = {"days": args.days}
            if args.seed is not None:
                seed_data["seed"] = args.seed
            api_post(args.port, "/api/sim/start", seed_data)

            print(f"Simulation started ({args.days} days)")
            print()
            print("Connect your AI agent and run vm_cli.py sim commands.")
            print("Press Ctrl+C when done.")
            print()

            server.wait()

        else:
            parser.print_help()
            print("\nUse --claude or --manual to start a benchmark run.")
            server.terminate()

    finally:
        server.terminate()
        server.wait()


if __name__ == "__main__":
    main()
