# DOPIS-PROMPT-008 — DOPIS-PLAN-004 independent-review correction

Prompt version: 0.1.1
Supersedes: DOPIS-PROMPT-008/0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-004`
Branch: `planning/vertical-slice-design`
Accepted base: `main @ 39dade2927e743ba52360fa9034f2f3954b5a15f`
Reviewed candidate: `276f0eab94cdefe3a20adad8258bb5d5eaf49dd5`
Draft PR: `#11`

Run `git fetch origin` and `git pull --ff-only`, then verify the worktree is clean and matches the remote correction-custody HEAD containing this prompt.
Apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and `docs/README.md`.

This is a bounded semantic correction of the already prepared PLAN-004 vertical-slice model and its traceability support. Do not redesign the whole slice map, reopen accepted stories, or start later technical planning.

## Independent-review findings

### 1. EXTRA_DEPENDENCY_RATIONALE_NOT_REPRESENTABLE_OR_ENFORCED

`DOPIS_VERTICAL_SLICE_TRACEABILITY_CONTRACT.json` states that a declared slice dependency not induced by a cross-slice `STORY DEPENDS_ON STORY` relationship must carry a non-empty, source-backed rationale distinguishable from an induced dependency.

The current model represents `dependencies` only as slice-id strings, and `check_vertical_slices()` recomputes induced dependencies but accepts any additional valid slice-id dependency without requiring or validating rationale/source evidence. The validator therefore does not enforce the contract it declares.

Correct this with the smallest representation that preserves the simple dependency list while making additional hard dependencies machine-checkably distinguishable and justified. A compact optional per-slice rationale/source map for non-induced dependency ids is acceptable; an equivalent smaller representation is also acceptable.

Required invariants:

- induced cross-slice story dependencies remain directly represented;
- a declared dependency not induced by story dependency must have a non-empty rationale plus concrete accepted source reference(s);
- rationale/source metadata for an edge that is not actually declared is invalid;
- induced dependencies do not require duplicated rationale text;
- validator deterministically rejects an unjustified additional dependency;
- add a focused negative fixture for an unjustified extra dependency and a positive/control path proving a justified additional dependency can pass.

Do not add process metadata beyond what is needed to represent and validate this distinction.

### 2. CORE_ORDERING_BUNDLES_ROLLBACK_INDEPENDENT_UPSELL

`VS-ORDERING-001` currently groups:

- `ST-CATALOG-001`
- `ST-UPSELL-001`
- `ST-ORDER-001`

The catalog/basket + guest checkout stories form the core end-to-end ordering outcome. `ST-UPSELL-001` is an optional recommendation behavior with its own acceptance boundary and can be disabled independently without removing catalog or ordering. That is a distinct rollback/product-learning boundary under the PLAN-004 decomposition rules.

Split `ST-UPSELL-001` into its own vertical slice. Preserve core ordering as the smallest coherent customer outcome using `ST-CATALOG-001` + `ST-ORDER-001`.

The new upsell slice must remain product-visible, not technical. If it declares a hard dependency on the core ordering slice because its accepted context requires an existing eligible basket/catalog behavior, represent that as an additional semantic dependency using the corrected rationale/source mechanism from finding 1. Do not manufacture any other dependency merely to force delivery order.

Do not alter the accepted upsell story, its requirements, or its acceptance criteria.

### 3. CAPACITY_AUTHORITY_BOUNDARIES_RECOLLAPSED

`VS-CAPACITY-001` currently combines:

- `ST-CAPACITY-001` — Jaime-only normal/planned service hours, pickup windows, and capacity;
- `ST-CAPACITY-002` — staff temporary current-service pickup-window adjustment;
- `ST-CAPACITY-003` — responsible-person temporary current-service delay/capacity reduction.

These stories were deliberately separated because permanent/planned authority and temporary current-service authority are materially distinct acceptance, rollback, and authority boundaries.

Correct the slice map so:

- `ST-CAPACITY-001` is in a planned/normal-service capacity slice owned by Jaime's accepted result;
- `ST-CAPACITY-002` and `ST-CAPACITY-003` may remain together in one current-service temporary-control slice because they share the same temporary current-service outcome/boundary;
- the temporary-control slice must not imply permission to change normal capacity or hours;
- if the temporary-control outcome cannot exist without an established normal service plan, encode only that source-backed hard dependency using the corrected additional-dependency rationale mechanism.

Do not change any actor or authority semantics upstream.

### 4. SMS_DEFERRED_REFERENCE_OWNERSHIP_DRIFT

`VS-KITCHEN-001` includes `ST-KITCHEN-001`, whose accepted behavior includes `FR-COMMS-002` and whose observable outcome explicitly includes notifying the customer when the order becomes ready. The slice therefore encounters the still-DEFERRED SMS provider decision `TB-INTEGRATION-003`, but the candidate does not list it.

At the same time, `VS-PILOT-001` lists `TB-INTEGRATION-003` even though the pilot slice does not own SMS-provider implementation/provisioning. PLAN-003 bound that deferred choice to the communications/messaging capability before the first real pilot order, not to generic pilot-governance implementation.

Correct the references so:

- `VS-TRACKING-001` retains `TB-INTEGRATION-003`;
- `VS-KITCHEN-001` includes `TB-INTEGRATION-003` because its accepted ready notification encounters that provider boundary;
- remove `TB-INTEGRATION-003` from `VS-PILOT-001` unless a concrete slice-specific accepted behavior proves the pilot slice itself must resolve/hand forward the provider decision;
- do not select an SMS provider.

Keep technical/deferred baseline references minimal and slice-relevant.

## Preserve the rest of the reviewed result

Do not perform unrelated repartitioning. Preserve unless mechanically affected by the corrections above:

- every accepted story remains assigned exactly once;
- all 27 product acceptance criteria remain covered through their stories;
- `VS-TRACKING-001 -> VS-ORDERING-001` remains the dependency induced by `ST-COMMS-001 -> ST-ORDER-001`;
- `VS-COLLECTION-001 -> VS-KITCHEN-001` remains the dependency induced by `ST-PAYMENT-001 -> ST-KITCHEN-001`;
- all other slice outcomes/boundaries remain unchanged unless an identifier/order reference must change because of the two bounded splits;
- no horizontal technical slice may be introduced;
- no whole-MVP mega-slice may be introduced;
- no new requirement/story/use-case behavior may be invented.

The two required semantic splits should increase the slice count by two relative to the reviewed 16-slice candidate unless a deterministic identifier/mechanical representation detail requires an equivalent count. Do not use the count itself as a design target.

## Learning triage

Add one concise learning record:

`docs/governance/learning/DOPIS-LEARNING-009-vertical-slice-boundaries-and-dependencies.md`

Record only:

- a traceability contract must not promise additional-dependency justification that its model/validator cannot represent and enforce;
- optional independently disableable behavior is a distinct slice candidate when it creates its own rollback/product-learning boundary;
- deliberate actor/authority separations in accepted stories must not be casually recombined into one delivery boundary;
- deferred technical references belong to the slice that actually encounters/owns the boundary, not a later generic milestone slice;
- prevention: review slice grouping against acceptance/rollback/authority boundaries and review every declared contract invariant against executable validator behavior.

## Allowed writes

- `docs/planning/DOPIS_VERTICAL_SLICES.json`
- `docs/traceability/DOPIS_VERTICAL_SLICE_TRACEABILITY_CONTRACT.json`
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json` only for exact future-node/index changes caused by corrected slice ids/count
- `scripts/validate_specification.py`
- `scripts/test_validate_specification.py`
- `docs/README.md` only if current PLAN-004 registration becomes inaccurate
- `docs/governance/learning/DOPIS-LEARNING-009-vertical-slice-boundaries-and-dependencies.md`

This prompt file is immutable once executed.

Do not modify canonical discovery, requirements, gates, exclusions, epics, use cases, accepted stories/acceptance criteria, story/use-case contracts, minimum technical baseline/evidence, frontend/application code, package manifests, workflows, ADRs, or architecture-decision records.

## Revalidation

Run the locked GOV-GEN consumer validation, then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`

Recompute and confirm:

- every accepted story appears in exactly one slice;
- all acceptance criteria remain covered through story membership;
- actor unions and readiness-gate unions are exact;
- every baseline/deferred reference resolves and deferred refs point only to `DEFERRED` decisions;
- every cross-slice story dependency is directly represented;
- every additional hard dependency is explicitly distinguishable, source-backed, and validator-enforced;
- dependencies remain acyclic;
- recommended delivery order covers every slice exactly once and respects every hard dependency;
- `future_nodes.vertical_slices` exactly matches the corrected model;
- no horizontal-layer slice, one-story mechanical decomposition, or mega-slice was introduced by the correction;
- upstream product/spec/story/technical-baseline/code artifacts are unchanged;
- implementation authority remains `NOT_GRANTED`;
- technical-contract/ADR/test/task planning remains `NOT_STARTED`;
- `git diff --check` passes.

All required checks block publication.

## Publication

Commit and push the SAME branch `planning/vertical-slice-design`.
Keep PR #11 draft and update its summary if useful.
Do not merge.
Do not start per-slice technical contracts, ADRs, technical acceptance criteria, tests, tasks, execution packets, or implementation.

Because this changes the material vertical-slice planning baseline and validator semantics, leave the exact pushed candidate for bounded independent delta review.

## Stop

Stop after successful push.

Report only:

- pre-correction HEAD;
- corrected candidate HEAD;
- changed files;
- corrected slice count;
- corrected slice IDs/titles/member-story counts for the affected slices;
- hard dependency edge count, distinguishing induced versus additional source-backed edges;
- recommended delivery order;
- story/acceptance coverage result;
- SMS deferred-reference correction result;
- validator/test/GOV-GEN/`git diff --check` results;
- confirmation upstream product/spec/story/technical-baseline/code artifacts are unchanged;
- implementation authority `NOT_GRANTED`;
- technical-contract/ADR/test/task planning `NOT_STARTED`.
