# DOPIS-PROMPT-003 v0.1.1 — Remove use-case contract/validator dual truth

Target:
`Sugar144/dopis`
worktree `/home/sugar/Proyectos/worktrees/dopis-plan-001a`
branch `planning/use-case-traceability-contract`
expected HEAD `a7cae3a5fe7530e9ac531270b7ce3125653d163d`
existing draft PR #6.

Preserve this correction prompt exactly as:
`docs/governance/prompts/DOPIS-PROMPT-003-v0.1.1.md`

Mark it as superseding v0.1.0 for this correction lineage.

## Finding

`USE_CASE_CONTRACT_VALIDATOR_DUAL_TRUTH`

The use-case contract declares model vocabulary and traceability semantics, but
`scripts/validate_specification.py` independently hard-codes several of the
same values.

## Objective

Make `DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json` the machine-readable source
for use-case modeling values while keeping deterministic validation.

Do not change product semantics or populate the real model.

## Required correction

Make the contract expose machine-consumable values for:

- actor/use-case/scenario ID patterns;
- actor required fields and allowed kinds;
- use-case required fields;
- actor-link roles;
- requirement-link roles;
- scenario types;
- BEHAVIOR/CONSTRAINT traceability relation definitions.

Update the validator so model validation consumes those values from the
contract instead of duplicating their literals in Python.

Executable invariant logic may remain in Python: uniqueness, reference
resolution, at-least-one PRIMARY, at-least-one BEHAVIOR, exactly one MAIN,
scenario-requirement subset, and future-node equality.

Cross-check the contract's structured traceability relations against
`DOPIS_TRACEABILITY_MATRIX.json`.

Keep hard-coded only genuine validator compatibility/governance boundaries
such as supported contract schema version and `NOT_GRANTED`.

Add focused disposable tests proving that contract/model drift is rejected,
including:
- actor kind or ID-pattern mismatch;
- required-field mismatch;
- contract/traceability-matrix relation mismatch.

Keep the real model:
`actors: []`
`use_cases: []`

Add one concise learning record for the dual-truth defect under
`docs/governance/learning/`.

## Validation

Run locked GOV-GEN conformance, both Dopis validators/tests, and
`git diff --check`.

Commit and push the SAME branch.
Keep PR #6 draft.
Do not merge.
Do not start DOPIS-PLAN-001B.

Report final HEAD, changed files, test/CI results, and confirmation that the
model remains empty and implementation authority remains NOT_GRANTED.
