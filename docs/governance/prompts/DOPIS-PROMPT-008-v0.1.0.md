# DOPIS-PROMPT-008 — DOPIS-PLAN-004 Vertical Slice Design

Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-004`
Branch: `planning/vertical-slice-design`
Accepted base: `main @ 39dade2927e743ba52360fa9034f2f3954b5a15f`

This packet is authorised to design the first-MVP vertical-slice planning model and the minimum deterministic traceability support needed to keep `STORY -> VERTICAL_SLICE` durable and machine-checkable.

It does **not** grant implementation authority and does **not** author per-slice technical contracts, ADRs, technical acceptance criteria, tests, tasks, execution packets, or application code.

Use or create the authorised worktree if needed. Before mutation:

1. `git fetch origin`;
2. verify repository/worktree/branch and clean status;
3. verify the branch starts from the repository-custodied prompt commit descended directly from the accepted base;
4. apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and `docs/README.md`.

Stop read-only if repository identity, governing instructions, or framework acquisition/validation cannot be resolved.

## Objective

Create the smallest coherent set of observable first-MVP vertical slices that:

- covers all accepted product stories exactly once;
- groups stories by one coherent end-to-end product/operational outcome and acceptance boundary rather than by technical layer;
- preserves existing story/use-case/requirement semantics and actor authority;
- makes hard inter-slice dependencies explicit without manufacturing implementation order;
- provides a recommended delivery order that respects hard dependencies and exposes useful product/risk learning early, without becoming an implementation commitment;
- identifies which accepted validation gates and minimum-technical-baseline decisions constrain each slice without resolving open values or deferred technical choices;
- creates the minimum traceability contract, matrix entries, validator support, and fixtures needed so this mapping cannot silently drift.

Do not target a preselected slice count. Do not create one slice per story mechanically, and do not create one whole-MVP mega-slice.

## Canonical references

Read only as needed:

- `AGENTS.md`
- `framework-lock.json`
- `docs/README.md`
- `docs/backlog/DOPIS_STORIES.json`
- `docs/backlog/DOPIS_EPICS.json`
- `docs/planning/DOPIS_USE_CASE_MODEL.json`
- `docs/traceability/DOPIS_STORY_ACCEPTANCE_TRACEABILITY_CONTRACT.json`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`
- `docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `docs/current/requirements/DOPIS_VALIDATION_GATES.json`
- `docs/current/requirements/DOPIS_EXCLUSIONS.json`

Use `DOPIS_STORIES.json` as the primary working set for slice composition. Consult requirements/gates only to derive readiness metadata or resolve ambiguity. Do not reopen discovery or story decomposition.

Current accepted planning inventory at the base is 25 stories and 27 product acceptance criteria. Treat repository artifacts and validator recomputation as source of truth rather than hard-coding those counts into semantics.

## Vertical-slice definition

For PLAN-004, a vertical slice is a bounded delivery increment that produces one observable product or operational outcome across whatever existing application boundaries are necessary.

A valid slice:

- has at least one accepted story;
- has one coherent observable outcome and one bounded demonstration/acceptance boundary;
- may contain stories from multiple use cases, epics, or actors when they participate in the same end-to-end outcome;
- may rely on previously delivered slices through an explicit hard dependency;
- does not exist merely to create backend scaffolding, a database, an API layer, authentication infrastructure, frontend components, migrations, adapters, or another horizontal technical concern;
- does not silently add product behavior absent from accepted stories;
- does not resolve an open gate or deferred technical decision merely to make the slice easier to describe.

Cross-cutting technical enabling work belongs to later technical contracts/tasks unless it is itself represented by accepted actor-visible/operational stories.

## Slice-decomposition rules

Derive the slice set from the accepted stories and their outcomes.

Prefer combining stories when they share:

- one end-to-end outcome;
- one meaningful demonstration/acceptance boundary;
- strongly coupled product behavior;
- the same practical stop/rollback boundary.

Prefer splitting when there is a material difference in:

- observable outcome;
- actor/authority boundary that creates a distinct accepted result;
- external provisioning or validation readiness boundary;
- rollback/recovery independence;
- behavioral dependency;
- product-risk/learning boundary.

Do not split mechanically by epic, use case, actor, file, frontend/backend/database, or one story per slice.
Do not combine unrelated outcomes simply to reduce slice count.

Every accepted story must belong to **exactly one** slice. There is no secondary/supporting story membership in PLAN-004; cross-slice reuse is represented by dependencies, not duplicate membership.

## Hard dependencies versus recommended order

Keep these distinct.

### Hard slice dependency

A slice depends on another slice only when the dependent slice cannot satisfy its accepted observable outcome without the prerequisite slice's accepted behavior already existing.

Every cross-slice `STORY DEPENDS_ON STORY` relationship in `DOPIS_STORIES.json` must induce a direct slice dependency when the two stories belong to different slices.

Additional hard slice dependencies are allowed only when they are grounded in accepted product/authority semantics and carry a concise source-backed rationale. Do not use dependencies to encode convenience, team preference, or a desired build sequence.

Dependencies must resolve, be non-self-referential, and be acyclic.

### Recommended delivery order

Provide one `recommended_delivery_order` containing every slice exactly once and respecting all hard dependencies.

The order is a planning recommendation, not implementation authority or release commitment. Prefer:

1. an early usable end-to-end outcome over horizontal foundation work;
2. early exposure of material product/integration/concurrency/security risk where doing so yields useful learning;
3. dependency-respecting progression;
4. pilot-critical capabilities before later reporting/governance polish when dependencies permit;
5. no assumption that unresolved PILOT/PUBLIC_LAUNCH gates block slice design itself.

Do not invent dates, estimates, sprint counts, staffing commitments, or release promises.

## Readiness gates

Each slice must declare `readiness_gate_ids` as the exact sorted unique union of validation gates referenced by the requirements linked by its member stories.

This is traceability metadata only. It does not mean every listed gate blocks design or implementation. Preserve the source requirement's existing `BLOCK`, `CALIBRATE`, or `VALIDATE` semantics; do not flatten them into a new slice-level status.

Do not resolve, calibrate, close, rename, or reinterpret any gate.

## Minimum technical baseline references

Each slice may declare `technical_baseline_refs` containing only existing `TB-*` decision IDs that materially constrain later technical-contract design for that slice.

Keep the list minimal and relevant. Do not attach the entire baseline to every slice.

Each slice may also declare `deferred_baseline_decision_refs`, containing only existing baseline decisions whose classification is `DEFERRED` and which the slice is expected to encounter or hand forward to its later technical contract/readiness work.

These references **do not resolve** the deferred decision.

Preserve in particular:

- `TB-DATA-003`: concurrency mechanism remains selected per invariant by the later technical contract;
- protected-staff identity/session implementation remains for its protected-staff technical contract, independent of production hosting;
- `TB-REALTIME-001`: SSE versus WebSockets remains deferred until a slice materially needs live kitchen updates; polling-compatible authoritative state remains valid;
- `TB-INTEGRATION-003`: SMS provider remains undecided but must resolve during communications/messaging pilot-readiness provisioning before the first real pilot order;
- production hosting and observability-provider choices remain deferred.

Do not choose any of these in PLAN-004.

## Required artifacts

### 1. Vertical-slice traceability contract

Create:

`docs/traceability/DOPIS_VERTICAL_SLICE_TRACEABILITY_CONTRACT.json`

Use a compact machine-readable contract with at least:

- `schema_version`: `1.0`;
- `status`: `PREPARED`;
- `implementation_authority`: `NOT_GRANTED`;
- source artifact references;
- identifier pattern `^VS-[A-Z][A-Z0-9-]*-[0-9]{3}$`;
- required slice fields;
- coverage/dependency/readiness/baseline-reference invariants;
- matrix relation definitions.

Slice required fields:

- `id`
- `title`
- `observable_outcome`
- `actor_ids`
- `story_ids`
- `dependencies`
- `acceptance_boundary`
- `readiness_gate_ids`
- `technical_baseline_refs`
- `deferred_baseline_decision_refs`

Contract rules must state at minimum:

- every slice has >=1 story;
- every story ID resolves;
- every accepted story is assigned to exactly one slice;
- `actor_ids` equals the exact sorted unique union of actor IDs from member stories;
- hard dependencies resolve/non-self/acyclic;
- every cross-slice story dependency is represented by a direct slice dependency;
- extra hard dependencies require a non-empty rationale/source representation in the model if the chosen dependency representation supports it;
- `readiness_gate_ids` equals the exact sorted unique union derived from member-story requirement validation links;
- every `technical_baseline_refs` ID resolves to a baseline decision;
- every `deferred_baseline_decision_refs` ID resolves to a baseline decision classified `DEFERRED`;
- no slice field grants implementation authority or carries API/schema/test/task/implementation detail;
- recommended delivery order covers every slice exactly once and respects hard dependencies.

Choose the smallest dependency representation that permits the validator to distinguish an induced story dependency from any additional justified hard dependency. Do not add process fields that are not needed for these rules.

### 2. Real vertical-slice model

Create:

`docs/planning/DOPIS_VERTICAL_SLICES.json`

Envelope must include at least:

- `schema_version`: `1.0`;
- `format`: `JSON`;
- `status`: `PREPARED`;
- `implementation_authority`: `NOT_GRANTED`;
- contract and accepted-source references;
- `slices`;
- `recommended_delivery_order`;
- a short note that order is non-binding planning guidance and does not grant implementation authority.

Populate the real slice set from the accepted 25-story backlog.

Descriptions must stay at product/operational planning level. Do not write endpoints, tables, ORM models, classes, event topics, test cases, task lists, file layouts, or implementation algorithms.

### 3. Traceability matrix integration

Update:

`docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`

Only as required to integrate the new planning node type and deterministic relationships.

At minimum:

- add baseline references for the vertical-slice contract/model;
- add `VERTICAL_SLICE` to `node_types`;
- derive `VERTICAL_SLICE --COVERS--> STORY` from slice story membership;
- derive `VERTICAL_SLICE --DEPENDS_ON--> VERTICAL_SLICE` from hard slice dependencies;
- add exact validator-recomputed `future_nodes.vertical_slices`;
- add the minimum orphan/integrity expectations needed by the validator for this node type.

Do not alter existing accepted relation semantics.

### 4. Validator and fixture support

Update only the minimum necessary parts of:

- `scripts/validate_specification.py`
- `scripts/test_validate_specification.py`

Add deterministic validation for the contract/model/matrix rules above.

Preserve all existing checks and existing positive/negative fixtures.

Add focused fixtures for at least:

- valid populated vertical-slice model;
- unknown story reference;
- duplicate story assignment;
- uncovered accepted story;
- actor-union drift;
- unknown slice dependency;
- slice dependency cycle;
- missing induced cross-slice dependency from a story dependency;
- readiness-gate union drift;
- unknown technical-baseline decision reference;
- non-DEFERRED ID placed in `deferred_baseline_decision_refs`;
- stale `future_nodes.vertical_slices` index;
- recommended order missing/duplicating a slice or violating a hard dependency.

Use disposable fixture trees; do not make fixture correctness depend on the real model staying empty or on a future slice count.

### 5. Documentation map

Update `docs/README.md` only to register the new contract/model and state clearly that they are planning artifacts with implementation authority `NOT_GRANTED`.

## Scope and semantic preservation

Do not modify:

- canonical discovery;
- requirements registry/markdown;
- validation gates;
- exclusions;
- epics;
- accepted use-case model/contract;
- story/acceptance contract;
- accepted story backlog;
- minimum technical baseline/evidence;
- frontend/application code;
- package manifests;
- workflows;
- ADRs or architecture-decision records.

If existing story semantics or the minimum technical baseline make a coherent vertical-slice model impossible without a new material product decision, stop and report the exact conflict. Do not silently correct upstream accepted artifacts.

## Validation

Before publication:

1. acquire and validate the locked GOV-GEN consumer;
2. run `python scripts/validate_specification.py`;
3. run `python scripts/test_validate_specification.py`;
4. parse all new/modified JSON artifacts;
5. verify all vertical-slice IDs are valid/unique;
6. verify every accepted story appears in exactly one slice;
7. verify actor unions, readiness-gate unions, baseline refs, deferred refs, and matrix future index are recomputed exactly;
8. verify hard dependencies are acyclic and all cross-slice story dependencies are represented;
9. verify recommended order covers every slice exactly once and topologically respects hard dependencies;
10. inspect the real slice set semantically for horizontal-layer slices, one-story mechanical slicing, or whole-MVP mega-slicing;
11. verify requirements, gates, epics, use cases, stories, accepted contracts, technical baseline, and application code are unchanged;
12. run `git diff --check`.

All required checks block publication.

Because this creates a material delivery-planning baseline and new traceability semantics, the exact final pushed candidate requires independent semantic review before Owner merge disposition.

## Publication

Commit and push the coherent result to `planning/vertical-slice-design` using the configured authenticated remote.

Creating/updating a draft PR is routine and authorised if useful, but do not merge.

Do not start per-slice technical-contract/ADR/test/task planning.

## Stop

Stop after successful push.

Report only:

- accepted base;
- custody starting HEAD;
- candidate HEAD;
- changed files;
- number of slices;
- slice IDs/titles and member-story counts;
- recommended delivery order;
- hard dependency edge count;
- coverage result for stories and acceptance criteria through story membership;
- readiness-gate and technical-baseline/deferred-reference integrity results;
- validator/test/GOV-GEN/`git diff --check` results;
- confirmation that upstream product/spec/story/technical-baseline/code artifacts remain unchanged;
- implementation authority `NOT_GRANTED`;
- technical-contract/ADR/test/task planning `NOT_STARTED`.
