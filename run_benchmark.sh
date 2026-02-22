#!/usr/bin/env bash
# =============================================================================
# Vending Machine AI Benchmark — Runner Script
# =============================================================================
# Starts the server, launches an AI agent, and collects the score.
#
# Usage:
#   ./run_benchmark.sh                    # Manual mode (prints instructions)
#   ./run_benchmark.sh --claude           # Auto-launch Claude Code
#   ./run_benchmark.sh --claude --seed 42 # Reproducible run
#   ./run_benchmark.sh --days 30          # Shorter simulation
# =============================================================================

set -e

# --- Configuration ---
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PORT=5050
DAYS=90
SEED=""
MODE="manual"
SERVER_PID=""
LOG_FILE="/tmp/vending-machine-server.log"

resolve_prompt_file() {
    local prompt_path="$SCRIPT_DIR/prompts/vending_machine/default.md"
    if [ -f "$prompt_path" ]; then
        echo "$prompt_path"
        return 0
    fi
    return 1
}

# --- Parse arguments ---
while [[ $# -gt 0 ]]; do
    case $1 in
        --claude)   MODE="claude"; shift ;;
        --seed)     SEED="$2"; shift 2 ;;
        --days)     DAYS="$2"; shift 2 ;;
        --port)     PORT="$2"; shift 2 ;;
        --help|-h)
            echo "Usage: ./run_benchmark.sh [OPTIONS]"
            echo ""
            echo "Options:"
            echo "  --claude       Auto-launch Claude Code as the AI agent"
            echo "  --seed N       Set random seed for reproducible runs"
            echo "  --days N       Number of simulation days (default: 90)"
            echo "  --port N       Server port (default: 5050)"
            echo "  -h, --help     Show this help"
            exit 0
            ;;
        *) echo "Unknown option: $1"; exit 1 ;;
    esac
done

# --- Cleanup on exit ---
cleanup() {
    if [ -n "$SERVER_PID" ]; then
        echo ""
        echo "Stopping server (PID $SERVER_PID)..."
        kill "$SERVER_PID" 2>/dev/null || true
        wait "$SERVER_PID" 2>/dev/null || true
    fi
}
trap cleanup EXIT

# --- Check dependencies ---
cd "$SCRIPT_DIR"

if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing dependencies..."
    pip3 install -r requirements.txt -q
fi

# --- Kill any existing server on the port ---
if lsof -ti:"$PORT" >/dev/null 2>&1; then
    echo "Port $PORT in use. Killing existing process..."
    lsof -ti:"$PORT" | xargs kill -9 2>/dev/null || true
    sleep 1
fi

# --- Start server ---
echo "Starting vending machine server on port $PORT..."
python3 server.py --port "$PORT" > "$LOG_FILE" 2>&1 &
SERVER_PID=$!

# Wait for server to be ready
echo -n "Waiting for server"
for i in $(seq 1 30); do
    if curl -s "http://localhost:$PORT/api/status" >/dev/null 2>&1; then
        echo " ready!"
        break
    fi
    echo -n "."
    sleep 1
done

if ! curl -s "http://localhost:$PORT/api/status" >/dev/null 2>&1; then
    echo " FAILED"
    echo "Server did not start. Check $LOG_FILE"
    exit 1
fi

# --- Start simulation ---
SEED_FLAG=""
if [ -n "$SEED" ]; then
    SEED_FLAG="--seed $SEED"
fi

echo ""
echo "============================================================"
echo "  VENDING MACHINE AI BENCHMARK"
echo "============================================================"
echo "  Server:     http://localhost:$PORT"
echo "  UI:         http://localhost:$PORT (open in browser)"
echo "  Days:       $DAYS"
echo "  Seed:       ${SEED:-random}"
echo "============================================================"
echo ""

export VM_URL="http://localhost:$PORT"
PROMPT_FILE="$(resolve_prompt_file || true)"

if [ -z "$PROMPT_FILE" ]; then
    echo "Error: Could not find prompt file."
    echo "Expected:"
    echo "  $SCRIPT_DIR/prompts/vending_machine/default.md"
    exit 1
fi

# --- Launch AI agent ---
if [ "$MODE" = "claude" ]; then
    # Check Claude Code is installed
    if ! command -v claude &>/dev/null; then
        echo "Error: 'claude' command not found."
        echo "Install Claude Code: https://docs.anthropic.com/en/docs/claude-code"
        exit 1
    fi

    AGENT_PROMPT="$(cat "$PROMPT_FILE")

---

# YOUR MISSION

The vending machine server is running at http://localhost:$PORT.
You are playing the Vending Machine Business Simulation.

Your goal: **Maximize your final bank balance** over $DAYS simulated days.
You start with \$500. You pay \$2/day rent. The machine starts empty.

## RULES
- Run ALL commands from this directory: $SCRIPT_DIR
- Use: python3 -m sim_cli.vm_cli sim <command>
- You must manage the business for ALL $DAYS days
- After the final day, run: python3 -m sim_cli.vm_cli sim score

## STRATEGY TIPS
- Order inventory ASAP on day 0 (delivery takes 1-3 days)
- Stock all 8 products for maximum revenue
- Use FreshCo for bulk orders (cheap, 2-day delivery)
- Use QuickStock for urgent restocks (fast, 1-day delivery)
- Search for more suppliers with: sim search \"cheap\"
- Restock the machine from storage daily
- Adjust prices based on season and weather
- Order more before weekends (higher demand)
- Keep notes to track your strategy

## BEGIN NOW
Start the simulation:
python3 -m sim_cli.vm_cli sim start --days $DAYS $SEED_FLAG

Then manage the business day by day until you complete all $DAYS days.
Good luck!"

    echo "Launching Claude Code agent..."
    echo "(Watch the UI at http://localhost:$PORT)"
    echo ""

    # Launch Claude Code with the prompt
    # --verbose shows what Claude is doing
    # Set max turns high enough for 90 days (~5-8 actions per day)
    claude -p "$AGENT_PROMPT" \
        --allowedTools "Bash" \
        --max-turns 800 \
        2>&1 | tee /tmp/vending-benchmark-agent.log

    echo ""
    echo "============================================================"
    echo "  BENCHMARK COMPLETE"
    echo "============================================================"

    # Collect final score
    echo ""
    python3 -m sim_cli.vm_cli sim score 2>/dev/null || echo "(Could not retrieve score)"

    echo ""
    echo "Agent log saved to: /tmp/vending-benchmark-agent.log"
    echo "Server log saved to: $LOG_FILE"

else
    # Manual mode — print instructions
    echo "Starting simulation..."
    python3 -m sim_cli.vm_cli sim start --days "$DAYS" $SEED_FLAG
    echo ""
    echo "============================================================"
    echo "  READY FOR AI AGENT"
    echo "============================================================"
    echo ""
    echo "Open the browser UI: http://localhost:$PORT"
    echo ""
    echo "Option 1 — Claude Code (auto):"
    echo "  ./run_benchmark.sh --claude"
    echo ""
    echo "Option 2 — Claude Code (manual):"
    echo "  claude -p \"\$(cat \\\"$PROMPT_FILE\\\") Run the business simulation for $DAYS days.\""
    echo ""
    echo "Option 3 — Any AI agent:"
    echo "  Feed $PROMPT_FILE to your AI, then let it run python3 -m sim_cli.vm_cli commands."
    echo ""
    echo "Option 4 — Play it yourself:"
    echo "  python3 -m sim_cli.vm_cli sim status"
    echo "  python3 -m sim_cli.vm_cli sim order freshco water 20"
    echo "  python3 -m sim_cli.vm_cli sim advance"
    echo "  ... (repeat for $DAYS days)"
    echo ""
    echo "Press Ctrl+C to stop the server."
    echo ""

    # Keep server running until Ctrl+C
    wait "$SERVER_PID"
fi
