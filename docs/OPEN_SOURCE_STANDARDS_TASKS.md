# Open Source Standards Tasks

Date: 2026-02-23
Goal: Raise the project to a high-trust, contributor-friendly OSS baseline.

## Batch 1: Governance and Community (Completed)

- [x] Add `LICENSE` (MIT).
- [x] Add `CODE_OF_CONDUCT.md`.
- [x] Add `SECURITY.md`.
- [x] Add `SUPPORT.md`.
- [x] Add PR template and issue templates.

## Batch 2: Methodology and Contributor Docs (Completed)

- [x] Add `docs/WHAT_THIS_TESTS.md` with explicit claims and limits.
- [x] Add `docs/TESTING.md` with local and CI commands.
- [x] Add `docs/SCREENSHOTS.md` with documentation asset standards.
- [x] Link these docs from `README.md`.
- [x] Add project copy updates to avoid "ultimate benchmark" positioning.

## Batch 3: Correctness and Drift Reduction (Completed)

- [x] Add runner persistence tests in `tests/test_run_race_results.py`.
- [x] Fix result persistence helper to create missing output directories.
- [x] Remove stale simulation-count drift in docs/marketing copy.

## Batch 4: Next Priority (Recommended)

- [ ] Add run manifest schema (`commit_sha`, prompt hash, model id, seed policy).
- [ ] Add schema validation tests for result artifacts.
- [ ] Add a reproducibility command to replay published runs.
- [ ] Add a docs consistency CI check (live simulation list vs registry).
