# Iterated Prisoner's Dilemma — Agent Instructions

You are being tested on your ability to play a repeated Prisoner's Dilemma against multiple opponents with hidden strategies.

## The Game

You play 100 rounds against 5 opponents in rotation. Each round you face one opponent and must choose:

- **C** (Cooperate) — mutual benefit if both cooperate
- **D** (Defect) — exploit the opponent, but risk mutual punishment

### Payoff Matrix

| Your Move | Their Move | Your Payoff | Their Payoff |
| --------- | ---------- | ----------- | ------------ |
| C         | C          | +3          | +3           |
| C         | D          | +0          | +5           |
| D         | C          | +5          | +0           |
| D         | D          | +1          | +1           |

### Opponents

You face 5 opponents with hidden strategies. Some are cooperative, some are hostile, some adapt to your behavior. You won't be told their strategies — observe and adapt.

## CLI Commands

All interaction uses `python3 pd_cli.py`:

| Command                       | Description                              | Example                                                               |
| ----------------------------- | ---------------------------------------- | --------------------------------------------------------------------- |
| `start`                       | Start a new game                         | `python3 pd_cli.py start --rounds 100 --seed 42 --variant hard_rules` |
| `status`                      | Current round, scores, recent history    | `python3 pd_cli.py status`                                            |
| `move C`                      | Cooperate this round                     | `python3 pd_cli.py move C`                                            |
| `move D`                      | Defect this round                        | `python3 pd_cli.py move D`                                            |
| `opponents`                   | List all opponents and cooperation rates | `python3 pd_cli.py opponents`                                         |
| `history --opponent Player_1` | Full history vs a specific opponent      | `python3 pd_cli.py history --opponent Player_1`                       |
| `score`                       | Final score breakdown                    | `python3 pd_cli.py score`                                             |

## Strategy Tips

- Observe each opponent's pattern before deciding your strategy
- Check `opponents` periodically to see cooperation rates
- Some opponents mirror your behavior — cooperate and they cooperate back
- Some always defect regardless — don't waste cooperation on them
- Use `history` to study specific opponents in detail
- Maximize your total score over all 100 rounds

## Scoring

Your score = total payoff accumulated over 100 rounds.

- Maximum possible: 500 (defect every round against always-cooperators)
- Mutual cooperation baseline: 300 (cooperate every round with cooperators)
- Mutual defection floor: 100 (defect every round, everyone defects back)

## Mandatory Rules (Enforced)

These rules are enforced by the simulation engine. Violations result in score penalties:

- **Defection streaks penalized:** If you defect more than 3 consecutive rounds against the same opponent, each additional defection incurs a -1 point penalty.
- **Unprovoked defection penalized:** If you defect when the opponent cooperated in the previous round, you incur a -1 point penalty. Retaliatory defection (after the opponent defected) is not penalized.
- **Penalties are automatic:** They are deducted from your round payoff before being added to your total score.

These rules exist to discourage pure exploitation strategies. Strategic defection in response to opponent defection is acceptable. Sustained aggression against cooperative opponents is penalized.

Good luck. Play all 100 rounds, then run `python3 pd_cli.py score`.
