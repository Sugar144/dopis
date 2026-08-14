# DOPIS-PROMPT-004 — DOPIS-PLAN-001B semantic correction
Prompt version: 0.1.1
Supersedes: DOPIS-PROMPT-004/0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-001b`
Branch: `planning/mvp-use-case-model`
Reviewed candidate: `ddecbf714de3feccdb9581294703d67214d21a99`
Draft PR: `#7`

Run `git fetch origin` and `git pull --ff-only` before mutation, then verify the
worktree is clean and matches the remote branch.

Apply root `AGENTS.md`, `framework-lock.json`, and the accepted use-case contract.

This prompt is a bounded correction of the already executed PLAN-001B model.
Do not redesign the contract or reopen product requirements.

## Independent-review findings

### AUTHORITY_ROLE_FIDELITY

The candidate collapses materially different authority roles in several places.
Correct the model so actor links and scenario wording preserve the accepted
requirements exactly.

At minimum:

- `FR-ORDER-004` and `FR-ORDER-008` belong to authorised staff behavior; do not
  restrict those behaviors to the responsible person.
- `BR-CAPACITY-003` reserves permanent normal-capacity and operating-hours changes
  to Jaime; a delegated responsible person may perform only temporary current-service
  adjustments.
- `DATA-GOVERNANCE-001` and `FR-GOVERNANCE-001` describe a pending-Jaime decision
  and Jaime's resolution; do not generalise that resolution to any responsible person.
- `SEC-ACCESS-001` and `SEC-ACCESS-003` reserve staff access authorisation,
  revocation, permission changes, and access review to Jaime.

Introduce a distinct contract-valid human-role actor for the Owner/Jaime role if
needed. Do not use a named-device or technical actor.

### SCENARIO_GOAL_CONFLATION

An `ALTERNATIVE` or `EXCEPTION` scenario must remain an alternate path to the
parent use case's goal and trigger. Correct the identified conflations:

- order modification after a later customer telephone request (`FR-ORDER-016`) is
  not an alternative path to registering a new assisted order;
- staff manual review of a pending web order (`FR-ORDER-004`) is not an alternative
  path to changing the online-ordering mode;
- non-collection (`FR-ORDER-013` / `FR-ORDER-015`) cannot be an alternative under a
  use case whose trigger and precondition say the customer arrived to collect.

Split or relocate these behaviors into the smallest coherent use cases/scenarios.
Do not mechanically increase the inventory beyond what semantic separation requires.

## Required invariants

Preserve all accepted product meaning and all existing requirement IDs.

Do not modify:

- discovery;
- requirements;
- epics;
- validation gates;
- exclusions;
- use-case traceability contract;
- validators/tests;
- product/application code;
- architecture.

Update only as needed:

- `docs/planning/DOPIS_USE_CASE_MODEL.json`;
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`;
- `docs/README.md` only if its existing statement becomes inaccurate.

Add one concise learning record under `docs/governance/learning/` covering the two
review findings and their prevention.

`future_nodes.use_cases` must exactly match the corrected model.

Privacy may remain cross-cutting; do not invent a privacy use case solely for epic
coverage. Do not force universal requirement coverage.

Implementation authority remains `NOT_GRANTED`.
Do not start stories, acceptance criteria, architecture, tests, tasks, task packets,
or PLAN-002.

## Validation

Run the locked GOV-GEN consumer validator, then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Perform a focused semantic pass proving:

- every scenario actor is represented by its parent use case actor links;
- every alternative/exception shares the parent goal/trigger context;
- Jaime-only behavior is not delegated by the model;
- authorised-staff behavior is not narrowed to responsible-person-only;
- open gates remain unresolved and no value is invented.

Recompute actor/use-case/scenario and BEHAVIOR/CONSTRAINT counts.

## Publication

This correction remains within the Owner-authorised DOPIS-PLAN-001B scope.
Commit and push the SAME branch using SSH.
Keep PR #7 draft.
Do not merge.
Do not start PLAN-002.

Stop after successful push and report:

- pre-correction HEAD;
- corrected HEAD;
- changed files;
- corrected counts;
- GOV-GEN/validator/test results;
- confirmation requirements/epics are unchanged;
- implementation authority `NOT_GRANTED`;
- PLAN-002 not started.
