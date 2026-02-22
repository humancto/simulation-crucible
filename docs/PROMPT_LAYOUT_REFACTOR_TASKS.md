# Prompt Layout Refactor Tasks

Date: 2026-02-22
Scope: Move from root-level `AGENT_*.md` sprawl to scenario-based prompt layout with safe compatibility.

## Batch 1 (Completed)
- [x] Add scenario-based prompt tree under `prompts/<scenario>/<variant>.md`.
- [x] Add prompt loader in `run_race.py` that prefers scenario-based prompts.
- [x] Keep legacy fallback behavior so runs do not break.

## Batch 2 (Completed)
- [x] Move 147 scenario-specific root files (`AGENT_<code>_<variant>.md`) into `prompts/_legacy/`.
- [x] Keep core vending prompts in root (`AGENT.md`, `AGENT_unconstrained.md`, `AGENT_soft.md`, `AGENT_hard.md`) for existing scripts.
- [x] Extend fallback loader to also check `prompts/_legacy/`.

## Batch 3 (Completed)
- [x] Add reusable migration script: `scripts/migrate_prompts_layout.py`.
- [x] Make script idempotent and support source fallback from both root and `prompts/_legacy/`.
- [x] Add prompt layout readme: `prompts/README.md`.

## Validation Checklist (Completed)
- [x] `python3 -m py_compile run_race.py`
- [x] `python3 run_race.py --help`
- [x] Smoke-test all 50 `build_*_prompt` functions (all passed)
- [x] Re-run migration script idempotently (copied all 151 prompt files)

## Follow-up Batches (Optional)
- [x] Update `run_benchmark.py` and `run_benchmark.sh` to load prompts from `prompts/vending_machine/` first.
- [x] Update README examples to reference new prompt paths.
- [ ] After 1 release cycle, remove legacy fallback from `run_race.py` if unused.
