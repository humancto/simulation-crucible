# Vending Machine AI Benchmark

A local, self-contained vending machine simulator that AI models (Claude Code, Codex, etc.) can interact with and be graded on. Tests an AI's ability to understand UI state, execute multi-step transactions, handle errors, and make decisions.

## Two Modes

| Mode              | What It Tests                                  | Scoring                                |
| ----------------- | ---------------------------------------------- | -------------------------------------- |
| **Practice Mode** | Vending machine transactions (10 scenarios)    | 0–100 per scenario, letter grade       |
| **Business Mode** | Running a vending machine business for 90 days | Final bank balance (started with $500) |

## Quick Start

```bash
cd vending-machine-ai-test
pip install -r requirements.txt
python server.py
```

Open http://localhost:5050 to see the live UI.

## For AI Agents

See **[AGENT.md](AGENT.md)** for complete instructions that can be fed to any AI model.

## Practice Mode

AI uses `vm_cli.py` to complete 10 test scenarios:

```bash
python vm_cli.py scenarios              # See all 10 test scenarios
python vm_cli.py start-scenario 1       # Start scenario 1
python vm_cli.py status                 # Check machine state
python vm_cli.py insert-money 1.00      # Insert $1.00
python vm_cli.py insert-money 0.50      # Insert $0.50
python vm_cli.py select A1              # Buy from slot A1
python vm_cli.py collect-item           # Pick up the item
python vm_cli.py collect-change         # Collect any change
python vm_cli.py grade                  # Get your score
```

The browser UI updates in real-time showing every action.

### 10 Test Scenarios

| #   | Scenario           | What It Tests                |
| --- | ------------------ | ---------------------------- |
| 1   | Basic Purchase     | Simple buy flow              |
| 2   | Exact Change       | Precise money handling       |
| 3   | Out of Stock       | Adapt to unavailability      |
| 4   | Budget Shopping    | Multi-item budget constraint |
| 5   | Change Calculation | Verify correct change        |
| 6   | Multi-Purchase     | Sequential transactions      |
| 7   | Error Recovery     | Handle machine jams          |
| 8   | Price Comparison   | Find optimal choice          |
| 9   | Insufficient Funds | Recover from errors          |
| 10  | Full Workflow      | End-to-end competency        |

### Scoring (0-100 per scenario)

- **Completion (40 pts):** Achieved the goal?
- **Efficiency (20 pts):** Steps vs optimal
- **Correctness (20 pts):** Errors encountered
- **Error Handling (20 pts):** Recovery quality

Final grade: A (90+), B (80+), C (70+), D (60+), F (<60)

## Business Simulation Mode

Inspired by [Andon Labs' Vending-Bench](https://github.com/andon-labs/vending-bench), Business Mode is a 90-day business simulation that tests an AI's ability to run a profitable vending machine operation.

### What It Tests

- **Long-term coherence:** Can the AI maintain a strategy over 90 simulated days?
- **Business strategy:** Supplier selection, pricing, inventory management
- **Adaptability:** Responding to weather, seasons, and demand patterns
- **Error handling:** Dealing with unreliable suppliers, scams, and cash flow pressure
- **Planning:** Ordering ahead, stocking for weekends, adjusting to forecasts

### How It Works

The AI starts with $500 and an empty vending machine. Each day it must manage suppliers, inventory, pricing, and sales. The simulation includes realistic demand patterns (weather, day of week, seasons), multiple suppliers (some honest, some adversarial), and economic mechanics (price elasticity, delivery delays).

### How to Run

```bash
python server.py                        # Start the server
python vm_cli.py sim start              # Start 90-day simulation
python vm_cli.py sim status             # Check current state
python vm_cli.py sim suppliers          # View known suppliers
python vm_cli.py sim order freshco water 20   # Order inventory
python vm_cli.py sim advance            # Advance one day
python vm_cli.py sim score              # Check final score
```

### Scoring

The score is the final bank balance after 90 days. The AI started with $500, so:

- **Below $500:** Lost money
- **Above $500:** Made a profit
- **Above $1000:** Strong performance

## Architecture

```
Browser UI (localhost:5050) <-> Flask + WebSocket <-> vm_cli.py (AI uses this)
```

## License

MIT
