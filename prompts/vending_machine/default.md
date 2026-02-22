# Vending Machine AI Benchmark — Agent Instructions

You are being tested on your ability to interact with a vending machine simulator.
There are two modes: **Practice Mode** (learn the basics) and **Business Mode** (run a business for 90 days).

- Practice Mode tests transaction skills across 10 scenarios. Score = average scenario grade.
- Business Mode tests business strategy over 90 simulated days. Score = your final bank balance. Higher is better.

## Quick Start

The vending machine server runs at `http://localhost:5050`.
You interact with it using the CLI tool: `python -m sim_cli.vm_cli <command>`.

---

## Practice Mode (Tutorial)

Practice Mode tests your ability to operate a vending machine: inserting money, selecting items, handling errors, and making purchases efficiently.

### Available Commands

| Command                 | Description                                    | Example                              |
| ----------------------- | ---------------------------------------------- | ------------------------------------ |
| `status`                | View full machine state (slots, balance, tray) | `python -m sim_cli.vm_cli status`            |
| `insert-money <amount>` | Insert money ($0.05–$20.00)                    | `python -m sim_cli.vm_cli insert-money 1.00` |
| `select <slot>`         | Buy item from slot (A1–D4)                     | `python -m sim_cli.vm_cli select A1`         |
| `cancel`                | Cancel transaction, get refund                 | `python -m sim_cli.vm_cli cancel`            |
| `collect-item`          | Pick up dispensed item(s) from tray            | `python -m sim_cli.vm_cli collect-item`      |
| `collect-change`        | Collect change from tray                       | `python -m sim_cli.vm_cli collect-change`    |
| `scenarios`             | List all 10 test scenarios                     | `python -m sim_cli.vm_cli scenarios`         |
| `start-scenario <id>`   | Start a scenario (1–10)                        | `python -m sim_cli.vm_cli start-scenario 1`  |
| `scenario-status`       | Check scenario timer and progress              | `python -m sim_cli.vm_cli scenario-status`   |
| `grade`                 | End scenario and get score                     | `python -m sim_cli.vm_cli grade`             |
| `reset`                 | Reset machine to defaults                      | `python -m sim_cli.vm_cli reset`             |

### Valid Money Denominations

$0.05, $0.10, $0.25, $0.50, $1.00, $2.00, $5.00, $10.00, $20.00

### Machine Layout (4x4 Grid)

| Slot | Default Item | Price |
| ---- | ------------ | ----- |
| A1   | Coca-Cola    | $1.50 |
| A2   | Water        | $1.00 |
| A3   | Sprite       | $1.50 |
| A4   | Red Bull     | $3.00 |
| B1   | Snickers     | $1.75 |
| B2   | Trail Mix    | $1.75 |
| B3   | M&Ms         | $1.50 |
| B4   | Kind Bar     | $2.00 |
| C1   | Doritos      | $1.75 |
| C2   | Cheetos      | $1.50 |
| C3   | Pringles     | $2.25 |
| C4   | Lays         | $1.75 |
| D1   | Sandwich     | $2.50 |
| D2   | Apple        | $1.25 |
| D3   | Granola Bar  | $1.50 |
| D4   | Cookies      | $2.00 |

### How a Purchase Works

1. **Check status** — see what's available and prices
2. **Insert money** — add enough to cover the item price
3. **Select slot** — the item is dispensed (or error if insufficient funds/out of stock)
4. **Collect item** — pick up the dispensed item from the tray
5. **Collect change** — pick up any change returned

**Important:** You MUST collect items and change after each purchase. Items sit in the tray until collected.

### Scenario Descriptions

1. **Basic Purchase** — Buy a Coca-Cola from slot A1
2. **Exact Change** — Pay exactly $1.75 for trail mix (no overpay)
3. **Out of Stock** — C1 is empty, find an alternative under $2.00
4. **Budget Shopping** — Buy 2 items spending under $5.00
5. **Change Calculation** — Insert $5, buy $1.50 item, verify $3.50 change
6. **Multi-Purchase** — Buy 3 items from 3 different rows
7. **Error Recovery** — Machine jams, recover and complete purchase
8. **Price Comparison** — Find and buy the cheapest drink in row A
9. **Insufficient Funds** — Try with too little money, add more, complete
10. **Full Workflow** — 3 purchases, collect everything, end at $0 balance

### Scoring Breakdown (per scenario, 0–100)

- **Completion (40 pts):** Did you achieve the scenario goal?
- **Efficiency (20 pts):** Steps taken vs optimal (fewer = better)
- **Correctness (20 pts):** Errors encountered (fewer = better)
- **Error Handling (20 pts):** Recovered from problems gracefully

### Tips for High Scores

1. **Always check status first** — know prices and stock before acting
2. **Use exact change when possible** — avoid unnecessary overpayment
3. **Collect items AND change** after every purchase
4. **Read error messages carefully** — they tell you exactly what went wrong
5. **If the machine jams**, try `cancel` to clear it, then retry
6. **Be efficient** — don't insert money in tiny increments when a larger bill works
7. **Plan multi-purchase scenarios** before starting

### Error Handling

- **Insufficient funds:** Insert more money, then select again
- **Out of stock:** Choose a different slot
- **Machine jammed:** Use `cancel` to attempt to clear the jam, then retry
- **Invalid slot:** Check the slot code (A1–D4)
- **Invalid denomination:** Use only the accepted amounts listed above

---

## Business Mode (The Real Test)

### The Challenge

Run a vending machine business for 90 simulated days starting with $500.
You pay $2/day rent. The machine starts EMPTY. You must:

- Find suppliers and negotiate prices
- Order inventory (delivered in 1–5 days)
- Stock the machine from storage
- Set competitive prices
- Adapt to weather, seasons, and demand
- Avoid bankruptcy (balance below -$50)

### Available Commands

All business mode commands use the `sim` prefix:

| Command                                | Description                                | Example                                                        |
| -------------------------------------- | ------------------------------------------ | -------------------------------------------------------------- |
| `sim start [--days N] [--seed S]`      | Start a new simulation                     | `python -m sim_cli.vm_cli sim start`                                   |
| `sim status`                           | Current day, balance, weather, inventory   | `python -m sim_cli.vm_cli sim status`                                  |
| `sim financials`                       | Profit/loss report, balance history        | `python -m sim_cli.vm_cli sim financials`                              |
| `sim suppliers`                        | List known suppliers                       | `python -m sim_cli.vm_cli sim suppliers`                               |
| `sim search <query>`                   | Search for new suppliers                   | `python -m sim_cli.vm_cli sim search "bulk wholesale"`                 |
| `sim quote <supplier> <product> <qty>` | Get a price quote                          | `python -m sim_cli.vm_cli sim quote freshco water 20`                  |
| `sim negotiate <supplier> <message>`   | Negotiate with a supplier                  | `python -m sim_cli.vm_cli sim negotiate freshco "Can you do 10% off?"` |
| `sim order <supplier> <product> <qty>` | Place an order                             | `python -m sim_cli.vm_cli sim order freshco water 20`                  |
| `sim orders`                           | List all orders (pending/delivered/failed) | `python -m sim_cli.vm_cli sim orders`                                  |
| `sim inventory`                        | Machine and storage inventory              | `python -m sim_cli.vm_cli sim inventory`                               |
| `sim set-price <product> <price>`      | Set selling price                          | `python -m sim_cli.vm_cli sim set-price water 1.75`                    |
| `sim restock <product> <qty>`          | Move items from storage to machine         | `python -m sim_cli.vm_cli sim restock water 10`                        |
| `sim weather`                          | Weather and 3-day forecast                 | `python -m sim_cli.vm_cli sim weather`                                 |
| `sim sales`                            | Sales report and customer feedback         | `python -m sim_cli.vm_cli sim sales`                                   |
| `sim note <content>`                   | Save a note for yourself                   | `python -m sim_cli.vm_cli sim note "Order more water before weekend"`  |
| `sim notes`                            | View all saved notes                       | `python -m sim_cli.vm_cli sim notes`                                   |
| `sim advance`                          | Advance one day                            | `python -m sim_cli.vm_cli sim advance`                                 |
| `sim score`                            | Get final score (bank balance)             | `python -m sim_cli.vm_cli sim score`                                   |
| `sim reset`                            | Reset the simulation                       | `python -m sim_cli.vm_cli sim reset`                                   |

### Products (8 types)

| ID           | Name         | Category | Reference Price |
| ------------ | ------------ | -------- | --------------- |
| water        | Water        | drink    | $1.50           |
| soda         | Soda         | drink    | $2.00           |
| energy_drink | Energy Drink | drink    | $3.50           |
| juice        | Juice        | drink    | $2.50           |
| chips        | Chips        | snack    | $1.75           |
| candy_bar    | Candy Bar    | snack    | $1.50           |
| trail_mix    | Trail Mix    | snack    | $2.25           |
| cookies      | Cookies      | snack    | $2.00           |

### Machine Specs

- **Slots:** 8 (one per product)
- **Items per slot:** 10 max
- **Machine capacity:** 80 items total
- **Storage capacity:** 200 items
- **Restock labor cost:** $0.50 per item moved from storage to machine

### Supplier Tips

- You start knowing 2 suppliers: **FreshCo Wholesale** and **QuickStock Distributors**
- Search for more with: `sim search <query>`
- Not all suppliers are honest — some will scam you
- Negotiate for better prices where possible (not all suppliers negotiate)
- Watch delivery times vs your stock levels
- Check minimum order quantities before ordering

### Economics

- Wholesale base cost is roughly 40% of reference price
- Suppliers add their own markup on top of the base cost
- Your profit = selling price - wholesale cost - rent - labor
- Higher prices = fewer sales (price elasticity applies)
- Demand varies by: day of week, season, weather

Demand varies based on day of week, season, and weather. Observe sales patterns to develop your strategy.

### Scoring

Your score = final bank balance after 90 days.
You started with $500. A good score is above $500. A great score is above $1000.
