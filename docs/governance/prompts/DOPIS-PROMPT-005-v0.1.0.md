# DOPIS-PROMPT-005 — DOPIS-PLAN-002A: Story and Product Acceptance-Criteria Contract
Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, code, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Accepted base: `main @ 6697ab7473ae35f35b6140043d759726e025ae89`
Branch: `planning/story-acceptance-contract`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-002a`

Run `git fetch origin` before evaluating refs.

The remote branch was created from the accepted base and may contain only this
custodied prompt before execution. If the worktree does not exist, creating the
tracking worktree is authorised routine mechanics. Verify repository, branch,
HEAD ancestry from the accepted base, clean state, applicable `AGENTS.md`, and
`framework-lock.json` before material mutation.

Apply the locked GOV-GEN framework.

## Objective

Establish the minimum machine-checkable contract for product stories and product
acceptance criteria so a later `DOPIS-PLAN-002B` can populate the real backlog.

This packet defines the contract, an intentionally empty backlog artifact, and
validator support only.

DO NOT create real Dopis stories or acceptance criteria yet.

## Canonical references

Use only what is needed:

- `docs/planning/DOPIS_USE_CASE_MODEL.json`
- `docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `scripts/validate_specification.py`
- `scripts/test_validate_specification.py`
- `docs/README.md`

Design references:

- ISO/IEC/IEEE 29148:2018
- Cucumber Gherkin Reference guidance for context/event/observable outcome

These are design references, not claims of formal Dopis compliance. ISO/IEC/IEEE
29148:2018 remains the published edition; Edition 3 is currently a DIS.

## Required result

Create:

`docs/traceability/DOPIS_STORY_ACCEPTANCE_TRACEABILITY_CONTRACT.json`

and:

`docs/backlog/DOPIS_STORIES.json`

The backlog must be valid but intentionally empty:

- `stories: []`
- implementation authority remains `NOT_GRANTED`

Update the traceability matrix, validator, negative tests, and `docs/README.md`
only as required to support this contract.

## Contract semantics

Keep the contract small, structured, and machine-consumable.

Story IDs:
`ST-<DOMAIN>-NNN`

Acceptance-criterion IDs:
`<STORY-ID>-ACNNN`

A story represents one coherent actor-visible product outcome derived from an
accepted use case. It is a planning decomposition, not a new requirement and not
an implementation task.

Each story must define machine-readable fields for:

- stable ID and title;
- actor ID;
- actor goal and value/outcome;
- exactly one parent use-case ID;
- one or more parent scenario IDs;
- requirement links;
- story dependencies;
- product acceptance criteria.

The story actor must resolve to an actor linked by the parent use case.
Scenario IDs must resolve and belong to the parent use case.

Requirement-link roles remain exactly:

- `BEHAVIOR`
- `CONSTRAINT`

Every story requires at least one `BEHAVIOR` requirement.
Every story requirement must already be linked by the parent use case with the
same role. A story must not promote a parent constraint into behavior or invent a
new requirement link.

Story dependencies are behavioral planning dependencies only. They must resolve,
may not be self-referential, and must be acyclic. They do not define technical
implementation order.

Each populated story requires at least one product acceptance criterion.

Each acceptance criterion must define machine-readable fields for:

- stable ID and short title;
- context (`Given`-equivalent);
- event (`When`-equivalent);
- one or more observable expected outcomes (`Then`-equivalent);
- requirement IDs.

Acceptance-criterion requirement IDs must resolve and be a subset of the parent
story's requirement links.

Acceptance criteria describe observable product behavior or business outcomes.
They must not prescribe APIs, classes, database structure, deployment topology,
framework choice, or other architecture. They are acceptance conditions, not test
implementations.

Do not restate accepted requirement text merely to make the backlog self-contained;
reference requirement IDs.

Stories and acceptance criteria do not own requirements and do not grant
implementation readiness or implementation authority.

## Traceability

Make the contract the machine-readable source for these relations:

`STORY --REFINES--> USE_CASE`

`STORY --REFINES--> REQUIREMENT`
for `BEHAVIOR` links.

`REQUIREMENT --CONSTRAINS--> STORY`
for `CONSTRAINT` links.

`STORY --DEPENDS_ON--> STORY`
for declared behavioral story dependencies.

`ACCEPTANCE_CRITERION --REFINES--> STORY`

`ACCEPTANCE_CRITERION --REFINES--> REQUIREMENT`
from each criterion's requirement references.

Cross-check the structured contract relations against
`DOPIS_TRACEABILITY_MATRIX.json`.

`future_nodes.stories` must be an exact validator-recomputed index of story IDs.

`future_nodes.acceptance_criteria` must be an exact validator-recomputed index of
acceptance-criterion IDs.

For PLAN-002A both therefore remain `[]`.

Do not introduce architecture, CONTRACT, TASK, TEST, or release-evidence linking
rules in this packet.

## Validator proof

Extend `scripts/validate_specification.py` deterministically.

The validator must consume story/acceptance vocabulary, patterns, required fields,
roles, and relation definitions from the new contract instead of duplicating those
literals in Python. Hard-code only genuine validator compatibility/governance
boundaries such as supported schema versions and `NOT_GRANTED`.

Executable invariant logic remains in Python.

Extend `scripts/test_validate_specification.py` so it proves both:

1. the real empty PLAN-002A backlog passes; and
2. a disposable temporary backlog containing one valid story and one valid product
   acceptance criterion, using real actor/use-case/scenario/requirement references
   and matching future-node indexes, also passes.

Add focused negative fixtures proving rejection of at least:

- unknown parent use case;
- scenario outside the parent use case;
- actor outside the parent use case;
- story requirement outside the parent use case or role drift;
- story with no BEHAVIOR requirement;
- populated story with no acceptance criterion;
- acceptance-criterion requirement outside the parent story;
- unknown or cyclic story dependency;
- stale `future_nodes.stories`;
- stale `future_nodes.acceptance_criteria`;
- contract/traceability-matrix relation drift.

Do not populate the repository backlog merely to test this.

## Invariants

Do not modify:

- discovery;
- requirements;
- validation gates;
- exclusions;
- epic semantics;
- accepted use-case model semantics;
- use-case traceability contract;
- product evidence;
- frontend/application code;
- architecture decisions.

Do not create real stories, real acceptance criteria, tasks, tests, technical
contracts, ADRs, or task packets.

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

Confirm the real story backlog remains empty, both future-node indexes are empty,
and product semantics are unchanged.

## Publication

Owner authorises this bounded PLAN-002A execution, including worktree creation if
needed, scoped mutation, validation, mechanical correction, commit, and push.

Push the SAME branch using the configured authenticated remote. The transport
mechanism is not material; publication is successful only when the remote branch
resolves to the reported exact candidate SHA.

Do not merge.
Do not start DOPIS-PLAN-002B.
Do not start architecture, tasks, tests, or implementation.

Do not create a PR with local `gh`; the orchestrator will create one draft PR after
the exact pushed HEAD is known.

Because this changes downstream traceability and validator semantics, leave the
exact candidate for one bounded independent review.

## Stop

Stop after successful push.

Report only:

- accepted base HEAD;
- starting custody HEAD;
- candidate HEAD;
- changed files;
- contract/backlog paths;
- validator/test/GOV-GEN results;
- confirmation the real backlog is empty;
- confirmation `future_nodes.stories` and `future_nodes.acceptance_criteria` are empty;
- confirmation product/use-case semantics are unchanged;
- implementation authority `NOT_GRANTED`;
- PLAN-002B not started.
