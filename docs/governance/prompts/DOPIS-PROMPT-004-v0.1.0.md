# DOPIS-PROMPT-004 — DOPIS-PLAN-001B: MVP Use-Case Inventory
Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Accepted base: `main @ 8d0b771f2b9aed60c3e94941c1601c1fada9c96b`

Remote branch already exists at that exact base:

`planning/mvp-use-case-model`

Use worktree:

`/home/sugar/Proyectos/worktrees/dopis-plan-001b`

Run `git fetch origin` before evaluating remote refs.

Verify repository, worktree, branch, HEAD, clean state, applicable AGENTS.md,
and the locked GOV-GEN framework before mutation. Stop on mismatch.

Apply root `AGENTS.md` and `framework-lock.json`.

Before material mutation, preserve this prompt verbatim as:

`docs/governance/prompts/DOPIS-PROMPT-004-v0.1.0.md`

## Objective

Populate the accepted MVP actor/use-case/scenario model from the existing
Dopis business baseline.

This is behavioral product modeling only.

Do not create stories, acceptance criteria, architecture, tests, tasks,
task packets, or implementation.

## Governing sources

Normative model contract:

`docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json`

Populate:

`docs/planning/DOPIS_USE_CASE_MODEL.json`

Use as source truth:

- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `docs/backlog/DOPIS_EPICS.json`
- `docs/current/requirements/DOPIS_VALIDATION_GATES.json`
- `docs/current/requirements/DOPIS_EXCLUSIONS.json`
- `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`

Use the requirements registry and epics as the primary working set.
Consult discovery only where needed to resolve behavioral context; do not
reread or restate it unnecessarily.

The accepted use-case contract already embodies the modeling rules. Do not
perform a new methodology redesign.

## Modeling rules

Inspect the full accepted requirements baseline and all epics.

Create the smallest coherent set of use cases that represents the observable
MVP behavior.

Follow the contract exactly.

In particular:

- actors are human roles or genuinely external systems;
- devices alone are not actors;
- use cases represent actor-visible goals, not technical components;
- each use case has one MAIN scenario;
- add ALTERNATIVE or EXCEPTION scenarios only for materially distinct accepted
  behavior;
- scenario steps remain observable and technology-neutral;
- BEHAVIOR links identify requirements refined by the use case;
- CONSTRAINT links identify accepted requirements constraining it.

Do not force all 218 requirements into use cases. Cross-cutting NFR, privacy,
audit, governance, milestone, and similar obligations may remain outside the
behavioral model or constrain relevant use cases.

Do not invent behavior to achieve artificial coverage.

Preserve current accepted authority semantics and role equivalence. Do not
create artificial actors based on device, screen, frontend surface, or
implementation component.

Open gates remain open. Do not resolve, calibrate, or silently select an
undecided value.

If an accepted behavior cannot be modeled without a genuinely new material
Owner decision, stop and identify the exact requirement/gate instead of
inventing an answer.

## Mutation surface

Populate:

`docs/planning/DOPIS_USE_CASE_MODEL.json`

Update:

`docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`

so `future_nodes.use_cases` exactly matches the populated model.

Update `docs/README.md` only to remove the now-stale statement that the
use-case inventory is intentionally empty.

Do not modify the use-case contract, validators, requirements, epics,
discovery, gates, exclusions, product code, or architecture.

If the accepted contract itself prevents representation of accepted behavior,
stop and report the contract defect instead of changing it in this packet.

Implementation authority remains:

`NOT_GRANTED`

## Completeness check

Before publication, perform a semantic coverage pass across all epics and the
full requirements registry.

Do not require universal requirement coverage.

Report:

- actor count;
- use-case count;
- scenario count;
- distinct BEHAVIOR-linked requirements;
- distinct CONSTRAINT-linked requirements;
- any epic with no behavioral use case and why;
- any accepted behavioral requirement intentionally left outside a use case
  and why.

Do not create a duplicate durable coverage registry merely to report these
checks.

## Validation

Run:

`python scripts/acquire-framework.py`

Run the locked GOV-GEN consumer validator.

Then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Confirm:

- `future_nodes.use_cases` exactly matches the model;
- no product requirement or epic changed;
- no stories/AC/tasks/tests were created;
- implementation authority remains `NOT_GRANTED`.

## Publication

Owner authorizes this bounded PLAN-001B mutation, validation, mechanical
correction, commit, and push.

Commit and push the SAME branch:

`planning/mvp-use-case-model`

Use SSH for push.

Do not merge.
Do not start DOPIS-PLAN-002.

Do not attempt PR creation with `gh`; the orchestrator will create the draft
PR after the exact pushed HEAD is known.

Because this is material semantic product modeling, leave the pushed exact
candidate for bounded independent review.

## Stop

Stop after successful push.

Report only:

- base HEAD;
- candidate HEAD;
- changed files;
- actor/use-case/scenario counts;
- BEHAVIOR/CONSTRAINT requirement counts;
- uncovered-epic/behavioral-requirement dispositions;
- validator/test/GOV-GEN results;
- confirmation product requirements are unchanged;
- implementation authority `NOT_GRANTED`;
- PLAN-002 not started.
