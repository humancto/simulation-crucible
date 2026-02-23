# What This Tests (and What It Does Not)

The Simulation Crucible is an **open behavioral stress-test suite** for AI agents.

It evaluates how agents make tradeoffs under pressure in synthetic environments with:

- visible objectives (what the agent can optimize directly)
- hidden metrics (what the evaluator tracks but agent cannot see)
- ethical temptation patterns
- constraint variants (`unconstrained`, `soft_guidelines`, `hard_rules`)

## What This Can Measure Well

- Relative behavior differences between agents in the same setup.
- Constraint sensitivity: how behavior changes when rules move from guidance to enforcement.
- Failure mode discovery: where an agent optimizes visible metrics while harming hidden values.
- Regression tracking across prompt/model/runtime changes over time.

## What This Does Not Prove

- It is **not** a universal or final benchmark for "AI quality".
- It is **not** certification for real-world deployment safety.
- It is **not** a standalone ranking oracle across all domains.
- It does **not** remove the need for independent due diligence.

## How to Interpret Scores

- Treat scores as **comparative signals**, not absolute truth.
- Compare runs only when scenario, seed policy, variant, and runtime policy are aligned.
- Use run logs and hidden-metric breakdowns to explain *why* scores differ.
- Prefer repeated runs over single-run conclusions.

## Minimum Credibility Checklist for Published Claims

When publishing any leaderboard or comparison, include:

- commit SHA
- scenario id and duration
- variant
- model identifier(s)
- seed policy (fixed/listed/random)
- number of runs per condition
- result artifact path(s)

Without this metadata, claims should be treated as anecdotal.
