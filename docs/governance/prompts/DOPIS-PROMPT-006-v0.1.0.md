# DOPIS-PROMPT-006 — DOPIS-PLAN-002B: MVP Stories and Product Acceptance Criteria
Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Accepted base: `main @ 1914eb9cfd1212531b081a7cf194472d9e84e6df`
Branch: `planning/mvp-stories-acceptance`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-002b`

Run `git fetch origin` before evaluating refs.

The remote branch was created from the accepted base and may contain only this
custodied prompt before execution. If the worktree does not exist, creating the
tracking worktree is authorised routine mechanics.

Verify repository, branch, HEAD ancestry from the accepted base, clean state,
applicable `AGENTS.md`, `framework-lock.json`, and locked GOV-GEN conformance
before material mutation. Stop on mismatch.

## Objective

Populate the real MVP product-story backlog and product acceptance criteria from
the accepted use-case model and requirements baseline.

This is behavioral product planning only.

Do not create architecture, technical contracts, ADRs, technical acceptance
criteria, tests, tasks, task packets, or implementation.

## Governing sources

Normative story/acceptance contract:

`docs/traceability/DOPIS_STORY_ACCEPTANCE_TRACEABILITY_CONTRACT.json`

Populate:

`docs/backlog/DOPIS_STORIES.json`

Use as source truth:

- `docs/planning/DOPIS_USE_CASE_MODEL.json`
- `docs/traceability/DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `docs/backlog/DOPIS_EPICS.json`
- `docs/current/requirements/DOPIS_VALIDATION_GATES.json`
- `docs/current/requirements/DOPIS_EXCLUSIONS.json`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`

The accepted story/acceptance contract already defines the modeling vocabulary
and traceability rules. Do not redesign methodology or modify the contract in this
packet.

Use the use-case model as the primary behavioral working set. Consult requirements,
epics, gates, and exclusions only as needed to preserve accepted semantics,
authority, constraints, and unresolved values.

## Story decomposition

Create the smallest coherent set of stories that preserves the accepted MVP
behavior.

Do not mechanically create one story per requirement, scenario, or use case.

A story represents one coherent actor-visible product outcome under exactly one
accepted parent use case.

A story may reference several scenarios from that same use case when they belong
to the same actor goal and acceptance boundary. Split when actor goal, product
outcome, acceptance boundary, or genuine behavioral dependency is materially
distinct.

Preserve actor authority exactly. Do not broaden Jaime-only behavior, narrow
authorised-staff behavior, invent device-based actors, or convert implementation
surfaces into actors.

Story dependencies are optional. Add one only when a genuine behavioral planning
dependency exists between product outcomes. Do not use dependencies to encode
technical build order, architecture, likely implementation sequence, or convenience.

## Product acceptance criteria

Each story must have enough product acceptance criteria to make its accepted
behavior observably decidable without prescribing implementation.

Use the contract's structured context/event/expected-outcomes form.

Criteria must describe observable product or business outcomes. They must not
prescribe UI layout, components, APIs, classes, database structure, framework,
deployment topology, test code, or architecture.

Do not merely copy requirement statements into criteria. Express the observable
condition that demonstrates the behavior while linking the accepted requirement ID.

Every `BEHAVIOR` requirement linked by a story must be covered by at least one of
that story's acceptance criteria.

A `CONSTRAINT` requirement should be linked at story level only where it materially
constrains that story. Reference it from a criterion when it materially affects that
criterion's observable acceptance condition; do not force every cross-cutting
constraint into every criterion.

## Semantic completeness

Before publication, prove all of the following over the accepted use-case model:

1. Every accepted use case is covered by at least one story.
2. Every accepted use-case scenario is represented by at least one child story's
   `parent_scenario_ids`.
3. For each use case, the union of child-story `BEHAVIOR` requirement links covers
   every `BEHAVIOR` requirement linked by that use case.
4. No story promotes a parent `CONSTRAINT` into `BEHAVIOR` or invents a requirement
   link.
5. Every story `BEHAVIOR` requirement is covered by at least one product acceptance
   criterion.
6. Alternative and exception behavior remains distinguishable in acceptance where
   it materially changes the observable outcome.

Do not inflate story count merely to satisfy these checks.

If accepted behavior cannot be represented under the existing contract without a
genuinely new material Owner decision, stop and identify the exact use case,
scenario, requirement, or gate rather than inventing an answer.

## Open gates and undecided values

Open gates remain open.

Do not calibrate or resolve an undecided value in a story or acceptance criterion.
Where accepted behavior depends on a configurable or later-calibrated value, express
acceptance in terms of the configured/authorised value or rule rather than inventing
a number, threshold, provider behavior, policy, or operational decision.

Do not turn a future milestone condition into implementation authority.

## Mutation surface

Populate:

`docs/backlog/DOPIS_STORIES.json`

Update:

`docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`

so `future_nodes.stories` and `future_nodes.acceptance_criteria` exactly match the
populated backlog.

Update `docs/README.md` only to remove the now-stale statement that the story backlog
is intentionally empty.

Do not modify:

- discovery;
- requirements;
- epics;
- validation gates;
- exclusions;
- accepted use-case model;
- use-case contract;
- story/acceptance contract;
- validators or validator tests;
- product evidence;
- application/frontend code;
- architecture decisions.

If the accepted contract or validator prevents faithful representation of accepted
behavior, stop and report the defect instead of changing those surfaces in this
packet.

Implementation authority remains:

`NOT_GRANTED`

## Completeness report

Before publication, report internally and verify:

- story count;
- acceptance-criterion count;
- accepted use cases covered;
- accepted scenarios covered;
- distinct `BEHAVIOR` requirements linked by stories;
- distinct `CONSTRAINT` requirements linked by stories;
- story dependency-edge count;
- any intentionally omitted parent constraint and why it is cross-cutting or not
  material to child-story acceptance.

Do not create a second durable coverage registry merely to report these checks.
The backlog, parent references, requirement links, future-node indexes, and validator
remain the durable traceability surfaces.

## Validation

Run:

`python scripts/acquire-framework.py`

Run the locked GOV-GEN consumer validator.

Then run:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Also perform a semantic coverage pass proving the six completeness conditions above.

Confirm:

- `future_nodes.stories` exactly matches backlog story IDs;
- `future_nodes.acceptance_criteria` exactly matches backlog criterion IDs;
- requirements, epics, use cases, contracts, validators, and tests are unchanged;
- no architecture/contract/task/test nodes were populated;
- implementation authority remains `NOT_GRANTED`.

## Publication

Owner authorises this bounded PLAN-002B mutation, validation, mechanical correction,
commit, and push.

Push the SAME branch using the configured authenticated remote. Transport is not
material; publication succeeds only when the remote branch resolves to the reported
exact candidate SHA.

Do not merge.
Do not start the minimum technical baseline or any later planning packet.
Do not create a PR with local `gh`; the orchestrator will create the draft PR after
the exact pushed HEAD is known.

Because this is material semantic product-backlog modeling, leave the pushed exact
candidate for bounded independent review.

## Stop

Stop after successful push.

Report only:

- accepted base HEAD;
- starting custody HEAD;
- candidate HEAD;
- changed files;
- story and acceptance-criterion counts;
- use-case/scenario coverage counts;
- distinct `BEHAVIOR`/`CONSTRAINT` requirement counts;
- dependency-edge count;
- any parent-constraint omission dispositions;
- GOV-GEN/validator/test results;
- confirmation requirements/epics/use cases/contracts/validators are unchanged;
- implementation authority `NOT_GRANTED`;
- confirmation no later planning packet was started.
