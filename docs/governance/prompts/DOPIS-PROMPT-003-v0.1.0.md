# DOPIS-PROMPT-003 — DOPIS-PLAN-001A: Use-Case Model and Traceability Contract
Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, code, commit/PR text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`

Accepted base:
`main @ b9b33a46f9855f878056200e158e532ecdd789eb`

Create a fresh worktree/branch:

- worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-001a`
- branch: `planning/use-case-traceability-contract`

If `origin/main` is not exactly the expected base, stop before mutation and report.

Apply root `AGENTS.md` and the exact GOV-GEN revision in `framework-lock.json`.

Before material mutation, preserve this entire prompt verbatim as:

`docs/governance/prompts/DOPIS-PROMPT-003-v0.1.0.md`

Do not summarize or rewrite it.

## Objective

Establish the minimum machine-checkable contract that allows a later
`DOPIS-PLAN-001B` to populate the MVP actor/use-case/scenario model without
changing the accepted requirements baseline or inventing downstream semantics.

This task defines the contract and validator support only.

DO NOT create the real Dopis use-case inventory yet.

## Canonical references

Use only the necessary repository sources:

- `docs/README.md`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `docs/backlog/DOPIS_EPICS.json`
- `scripts/validate_specification.py`
- `scripts/test_validate_specification.py`

External modeling references:

- OMG UML 2.5.1
- ISO/IEC/IEEE 29148:2018

Treat these as design references, not as a claim that Dopis formally conforms
to either standard.

## Required result

Create:

`docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json`

and:

`docs/planning/DOPIS_USE_CASE_MODEL.json`

The model must be valid but intentionally empty:

- `actors: []`
- `use_cases: []`
- implementation authority remains `NOT_GRANTED`

Update the existing traceability matrix, validator, negative tests, and
`docs/README.md` only as required to support the contract.

## Contract semantics

Keep the contract small and behavioral.

Actor IDs:
`ACT-<STABLE-NAME>`

Use-case IDs:
`UC-<DOMAIN>-NNN`

Scenario IDs:
`<USE-CASE-ID>-SNNN`

Actors represent human roles or genuinely external systems.
A device alone is not an actor.

Each use case must define:

- stable ID and title;
- actor-visible goal;
- trigger;
- actor links, with at least one `PRIMARY`;
- preconditions;
- success outcome;
- requirement links;
- scenarios.

Requirement links have exactly two roles:

- `BEHAVIOR`: obligation the use case behavior refines;
- `CONSTRAINT`: accepted requirement that constrains the use case.

Every use case requires at least one `BEHAVIOR` requirement.

All requirement IDs must resolve to the accepted requirements registry.
The same requirement must not appear twice in one use case.

Do not restate requirement text inside the use-case artifact.

Each use case must contain exactly one `MAIN` scenario.
`ALTERNATIVE` and `EXCEPTION` scenarios are optional.

Scenario requirement references must resolve and must be a subset of the
requirements already linked by their parent use case.

Scenario steps describe observable behavior, not UI design, classes, APIs,
database structure, or architecture.

Use cases do not own requirements and do not imply implementation readiness.
Do not require every one of the 218 accepted requirements to belong to a use
case: cross-cutting, governance, milestone, audit, privacy, NFR, or other
non-behavioral requirements may legitimately remain outside the use-case model.

## Traceability

Extend the existing matrix so that:

`USE_CASE --REFINES--> REQUIREMENT`

is derived from `BEHAVIOR` links.

And:

`REQUIREMENT --CONSTRAINS--> USE_CASE`

is derived from `CONSTRAINT` links.

`future_nodes.use_cases` becomes an exact, validator-recomputed index of the
use-case IDs in `DOPIS_USE_CASE_MODEL.json`.

For this task it therefore remains:

`[]`

because PLAN-001B has not started.

Add only the orphan/integrity checks actually needed to prove:

- use cases cannot exist without a behavior requirement;
- requirement references resolve;
- actor references resolve;
- IDs are unique and valid;
- exactly one MAIN scenario exists;
- scenario requirement references stay within the parent use case;
- `future_nodes.use_cases` exactly matches the model.

Do not introduce STORY, ACCEPTANCE_CRITERION, TASK, TEST, or architecture
linking rules in this packet.

## Validator proof

Extend `scripts/validate_specification.py` deterministically.

Extend `scripts/test_validate_specification.py`.

The test suite must prove both:

1. the real empty PLAN-001A model passes; and
2. a disposable temporary model containing one syntactically valid actor,
   one valid use case, one MAIN scenario, real requirement references, and a
   matching `future_nodes.use_cases` entry also passes.

Add focused negative fixtures proving rejection of at least:

- use case with no BEHAVIOR requirement;
- unknown requirement;
- unknown actor;
- scenario requirement outside the parent use-case links;
- stale/mismatched `future_nodes.use_cases`.

Do not populate the repository model merely to test this.

## Invariants

Do not modify:

- discovery v0.19;
- requirements baseline v0.6;
- validation gates;
- exclusions;
- epic semantics;
- product evidence;
- frontend/application code;
- architecture decisions.

Do not create stories, acceptance criteria, tasks, tests, or real use cases.

Implementation authority remains:

`NOT_GRANTED`

## Validation

Run:

`python scripts/acquire-framework.py`

Run the locked GOV-GEN consumer validator.

Then run:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Confirm the real use-case model is still empty and product semantics are
unchanged.

## Publication

Owner authorizes this bounded PLAN-001A execution, including:

- fresh branch/worktree;
- scoped mutations;
- validation;
- mechanical corrections;
- commit;
- push;
- one draft PR against `main`.

Do not merge.

Because this changes the downstream traceability contract and validator
semantics, leave the exact candidate for one bounded independent review.

Do not start DOPIS-PLAN-001B.

Suggested PR title:

`planning: establish use-case traceability contract`

## Stop

Stop after commit, push, and draft PR.

Report only:

- base HEAD;
- candidate HEAD;
- changed files;
- contract/model paths;
- validator and test results;
- GOV-GEN conformance result;
- draft PR;
- confirmation the model inventory is empty;
- confirmation product semantics are unchanged;
- implementation authority remains `NOT_GRANTED`;
- PLAN-001B not started.
