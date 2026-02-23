# Prompt Layout Refactor Tasks

Date: 2026-02-22
Scope: Move from root-level `AGENT_*.md` sprawl to scenario-based prompt layout with safe compatibility.

## Batch 1 (Completed)
- [x] Add scenario-based prompt tree under `prompts/<scenario>/<variant>.md`.
- [x] Add prompt loader in `run_race.py` that prefers scenario-based prompts.
- [x] Keep legacy fallback behavior so runs do not break.

## Batch 2 (Completed)
- [x] Move 147 scenario-specific root files (`AGENT_<code>_<variant>.md`) into `prompts/_legacy/`.
- [x] Keep core vending prompts in root (`AGENT.md`, `AGENT_unconstrained.md`, `AGENT_soft.md`, `AGENT_hard.md`) during transition.
- [x] Extend fallback loader to also check `prompts/_legacy/`.

## Batch 3 (Completed)
- [x] Add reusable migration script: `scripts/migrate_prompts_layout.py`.
- [x] Make script idempotent and support source fallback from both root and `prompts/_legacy/`.
- [x] Add prompt layout readme: `prompts/README.md`.

## Validation Checklist (Completed)
- [x] `python3 -m py_compile run_race.py`
- [x] `python3 run_race.py --help`
- [x] Smoke-test all 50 `build_*_prompt` functions (all passed)
- [x] Re-run migration script idempotently during transition (initially copied all 151 prompt files)

## Follow-up Batches (Optional)
- [x] Update `run_benchmark.py` and `run_benchmark.sh` to load prompts from `prompts/vending_machine/` first.
- [x] Update README examples to reference new prompt paths.
- [x] Remove root legacy vending prompt files after benchmark runner migration.
- [x] Remove `prompts/_legacy/` prompt archive after scenario prompt tree stabilized.
- [x] Remove legacy fallback branches from `run_race.py` and migration script if no longer needed.

## Batch 5.5 (Completed)
- [x] Prompt loader now resolves only `prompts/<scenario>/<variant>.md` paths.
- [x] Legacy root and `prompts/_legacy/` fallback branches removed from `race/prompts.py`.
- [x] Migration script no longer uses `prompts/_legacy/` fallback sources.
- [x] Prompt loader tests updated to enforce strict scenario-based prompt resolution.
