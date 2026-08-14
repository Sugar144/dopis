# DOPIS-PROMPT-008 — DOPIS-PLAN-004 validator-vocabulary correction

Prompt version: 0.1.2
Supersedes: DOPIS-PROMPT-008/0.1.1

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-004`
Branch: `planning/vertical-slice-design`
Accepted base: `main @ 39dade2927e743ba52360fa9034f2f3954b5a15f`
Reviewed candidate: `736df14c9a46758edb7d3975949795282f44c77d`
Draft PR: `#11`

Run `git fetch origin` and `git pull --ff-only`, verify the worktree is clean and matches the remote correction-custody HEAD containing this prompt, then apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and `docs/README.md`.

This is a tiny enforcement correction only. Do not repartition slices, alter delivery order, change baseline references, or reopen any PLAN-004 product/operational judgment.

## Independent-review finding

### DEPENDENCY_RATIONALE_SOURCE_VOCABULARY_DRIFT

`docs/traceability/DOPIS_VERTICAL_SLICE_TRACEABILITY_CONTRACT.json` defines `dependency_rationale.*.source_refs` as concrete accepted source ids limited to:

- requirement ids;
- use-case ids;
- story ids;
- acceptance-criterion ids.

The corrected validator currently builds `source_reference_ids` from those four sets **plus technical-baseline decision ids (`TB-*`)**. That means the validator can accept a dependency rationale source that the contract explicitly does not permit.

Correct the validator to enforce the contract exactly. Do not widen the contract vocabulary merely to match the implementation.

Required result:

- `dependency_rationale.*.source_refs` accepts only requirement, use-case, story, or acceptance-criterion ids;
- a `TB-*` decision id used there is deterministically rejected;
- existing real PLAN-004 rationale entries remain valid unchanged;
- add one focused negative fixture proving a resolvable technical-baseline id is still invalid in `dependency_rationale.source_refs`;
- preserve the existing positive/control fixture for a valid justified additional dependency.

Also update the existing `VERTICAL_SLICE --DEPENDS_ON--> VERTICAL_SLICE` `checked` description in `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json` so it accurately mentions that non-induced additional dependencies require validator-checked source-backed rationale. This is descriptive alignment only; do not alter relation semantics or other matrix content.

## Preserve the reviewed PLAN-004 candidate

Preserve byte-for-byte unless mechanically required by this correction:

- all 18 slice ids, membership, titles, outcomes, acceptance boundaries, dependencies, dependency rationale content, gate refs, baseline refs, deferred refs, and recommended delivery order;
- all 25-story / 27-acceptance-criterion coverage;
- the 4 hard dependency edges (2 induced + 2 additional source-backed);
- SMS deferred-reference placement;
- vertical-slice contract semantics;
- accepted requirements, gates, exclusions, epics, use cases, stories/acceptance criteria, minimum technical baseline, and application code;
- implementation authority `NOT_GRANTED`;
- technical-contract/ADR/test/task/execution-packet planning `NOT_STARTED`.

## Learning triage

Add one concise learning record:

`docs/governance/learning/DOPIS-LEARNING-010-validator-vocabulary-alignment.md`

Record only that validator reference vocabularies must exactly match their controlling contract, and a resolvable id from another namespace must not be accepted merely because it exists in the repository.

## Allowed writes

- `scripts/validate_specification.py`
- `scripts/test_validate_specification.py`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json` only for the one `checked` description alignment above
- `docs/governance/learning/DOPIS-LEARNING-010-validator-vocabulary-alignment.md`

This prompt file is immutable once executed.

Do not modify `DOPIS_VERTICAL_SLICES.json`, the vertical-slice contract, requirements, gates, exclusions, epics, use cases, stories/acceptance criteria, minimum technical baseline/evidence, frontend/application code, package manifests, workflows, ADRs, or architecture-decision records.

## Validation

Run:

1. locked GOV-GEN consumer validation;
2. `python scripts/validate_specification.py`;
3. `python scripts/test_validate_specification.py`;
4. `git diff --check`.

Confirm additionally:

- the real 18-slice model is unchanged from reviewed candidate `736df14c9a46758edb7d3975949795282f44c77d`;
- all existing PLAN-004 coverage/dependency/order checks still pass;
- a resolvable `TB-*` id in `dependency_rationale.source_refs` fails the new focused fixture;
- a valid requirement/use-case/story/acceptance-criterion source reference still passes;
- upstream product/spec/story/baseline/code artifacts remain unchanged.

All required checks block publication.

## Publication

Commit and push the SAME branch `planning/vertical-slice-design`.
Keep PR #11 draft.
Do not merge.
Do not start later planning.

Leave the exact pushed candidate for bounded independent delta review.

## Stop

Stop after successful push.

Report only:

- pre-correction HEAD;
- corrected candidate HEAD;
- changed files;
- exact validator vocabulary correction;
- focused fixture result;
- full validator/test/GOV-GEN/`git diff --check` results;
- confirmation the 18-slice model and upstream product/spec/story/baseline/code artifacts are unchanged;
- implementation authority `NOT_GRANTED`;
- later technical planning `NOT_STARTED`.
