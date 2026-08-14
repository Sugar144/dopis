# DOPIS-GOV-ADOPT-001B-R2 — Close Prompt-Custody Finding

Speak to the Owner in Spanish.
Write repository artifacts and PR text in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-gov-adopt`
Branch: `governance/adopt-gov-gen-rc1`
Expected HEAD: `01595e7855fa847713db77a293785ade772e5311`
Existing draft PR: `#5`

Apply root `AGENTS.md` and the locked GOV-GEN RC.2 operating contract.

Verify identity and clean state before mutation. Stop on mismatch.

## Objective

Close the independent-review finding that:

`docs/governance/prompts/DOPIS-PROMPT-001-v0.1.0.md`

contains a condensed representation rather than demonstrably exact executed
prompt text.

Do not reconstruct or overwrite historical evidence.

## Changes

1. Leave `DOPIS-PROMPT-001-v0.1.0.md` byte-identical.

2. Add one concise correction record:

`docs/governance/prompts/DOPIS-PROMPT-001-custody-correction.md`

Record:
- affected prompt: `DOPIS-PROMPT-001/0.1.0`;
- custody status: `NOT_PRESERVED`;
- defect: committed body is a condensed representation, not exact-text custody;
- no claim that it is the original exact prompt;
- resulting RC.2 implementation evidence remains independently validated;
- future material prompts require exact-text custody.

3. Add one concise learning record under:

`docs/governance/learning/`

covering observation, impact, cause, containment, correction and prevention.

4. Custody THIS R2 prompt as the next material prompt:

`DOPIS-PROMPT-002/0.1.0`

under `docs/governance/prompts/`.

Preserve this R2 prompt exactly, not as a summary.

5. Update PR #5 body so it reflects the actual current state:
- GOV-GEN RC.2;
- Dopis L1 configuration;
- `DOPIS-PROMPT` namespace;
- RC.1 -> RC.2 controlled upgrade;
- original GOV-GEN consumer-gap resolved;
- Dopis prompt-custody defect recorded as `NOT_PRESERVED`;
- conformance and Dopis validators PASS;
- no product semantic changes;
- implementation authority remains `NOT_GRANTED`.

Keep PR #5 draft.

## Do not change

Do not modify:
- GOV-GEN lock/configuration/upgrade;
- AGENTS.md;
- product/discovery/requirements/epics/traceability;
- application code;
- `DOPIS-PROMPT-001-v0.1.0.md`.

Do not merge.
Do not start `DOPIS-PLAN-001A`.

## Validation

Run:

`python scripts/acquire-framework.py`

Run the official locked GOV-GEN consumer validator.

Run:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Verify `DOPIS-PROMPT-001-v0.1.0.md` is unchanged.

Commit, push the existing branch, update PR #5, and let CI run.

## Stop

Stop after the correction is pushed, PR #5 is accurate and still draft, and
the exact-head CI state is known.

Report only:
- final HEAD;
- changed files;
- confirmation historical v0.1.0 is unchanged;
- custody correction status;
- learning record;
- validation/CI;
- PR #5 state;
- product semantics unchanged;
- implementation authority `NOT_GRANTED`;
- PLAN-001A not started.
