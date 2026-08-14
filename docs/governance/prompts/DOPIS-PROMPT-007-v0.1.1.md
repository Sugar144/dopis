# DOPIS-PROMPT-007 — DOPIS-PLAN-003 independent-review correction

Prompt version: 0.1.1
Supersedes: DOPIS-PROMPT-007/0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-003`
Branch: `planning/minimum-technical-baseline`
Accepted base: `main @ 831571be7164076a84367e15ee4e5ee173d38faf`
Reviewed candidate: `af0ddd1d8a3f808d69e1c36ee9c55b53f7ede424`
Draft PR: `#10`

Run `git fetch origin` and `git pull --ff-only`, then verify the worktree is clean and matches the remote correction-custody HEAD containing this prompt.
Apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and `docs/README.md`.

This is a bounded semantic correction of the already prepared PLAN-003 baseline. Do not redesign the baseline or reopen technology selection.

## Independent-review findings

### 1. MIXED_PROVENANCE_API_CLASSIFICATION

`TB-API-001` is classified `NEW_MINIMUM_BASELINE` and its rationale says canonical discovery does not fix the API style, but discovery §3.2 explicitly records `API style: REST` as provisional.

Correct the provenance so the baseline distinguishes the promotion of the existing provisional REST direction from genuinely new minimum standardisation such as RFC 9110/OpenAPI rules. Use the smallest clear representation: reclassification and/or a narrowly split decision is acceptable, but do not change the resulting REST/HTTP/OpenAPI baseline semantics.

### 2. MIXED_PROVENANCE_AUTH_CLASSIFICATION

`TB-AUTH-001` is classified `NEW_MINIMUM_BASELINE`, but discovery §3.2 already records as provisional that staff authentication has real backend enforcement and is not only a frontend route guard.

Correct the provenance. Preserve the resulting server-enforced authorization rule and the OWASP-derived object/function authorization requirement; do not weaken security.

### 3. DATA_PROVENANCE_CONTRADICTION

`TB-DATA-001` is `INHERITED_ACCEPTED` while its decision includes PostgreSQL and Alembic. The same baseline correctly treats the backend stack including PostgreSQL/Alembic as promoted from provisional under `TB-BACKEND-001`, and discovery §3.2 lists SQLAlchemy/Alembic in the provisional direction.

Remove this classification contradiction. Preserve PostgreSQL as the authoritative operational store in the PLAN-003 candidate and Alembic as the schema-migration baseline; only correct provenance/classification representation.

### 4. AUTH_DEFERRAL_FALSE_DEPENDENCY

`TB-AUTH-003` currently says identity provisioning, credential-reset flow, and session-storage implementation are blocked on production hosting/topology and are resolved only once production topology is decided.

That dependency is too strong. The protected-staff vertical must be able to resolve identity provisioning, credential/reset behavior, and session-storage implementation without waiting for production hosting. Only deployment-specific cookie/origin/domain parameters genuinely depend on the eventual topology.

Correct `TB-AUTH-003` (or split it minimally if clearer) so:

- protected-staff authentication/session implementation can be resolved by its vertical technical contract before production hosting is chosen;
- only topology-dependent cookie/origin/domain configuration remains dependent on deployment topology;
- no concrete credential/session implementation is chosen in PLAN-003.

### 5. SMS_PROVIDER_DEFERRED_TOO_LATE

`TB-INTEGRATION-003` defers SMS provider selection to production readiness. Accepted requirements `FR-COMMS-001` and `FR-COMMS-002` are `MUST_MVP` with `readiness_milestone: PILOT` and require real SMS outcomes for the first operational pilot.

PLAN-003 still must not select a provider, but its deferral must be resolved no later than the communications/messaging vertical's pilot-readiness provisioning before the first real pilot order. Production hosting is not a prerequisite to selecting/provisioning the SMS provider.

Update the decision, rationale, downstream rule, `deferred_detail`, and the matching `deferred_decisions` entry accordingly. Cite the accepted communication requirements as authority.

## Preserve the accepted technical result

Do not change the selected/prepared technical direction except where needed to correct provenance or resolution timing:

- Vue/Vite frontend direction remains unchanged;
- FastAPI/Pydantic/SQLAlchemy 2/Alembic/PostgreSQL remains the baseline candidate;
- modular-monolith direction remains unchanged;
- REST/HTTP/OpenAPI/Problem Details semantics remain unchanged;
- transaction-boundary rule remains unchanged;
- secure browser-session and backend authorization baseline remains unchanged;
- SSE vs WebSockets remains deferred;
- provider-neutral integration boundaries and APOS A8 fallback remain unchanged;
- Docker Compose local direction remains unchanged;
- production hosting remains deferred;
- implementation authority remains `NOT_GRANTED`.

Do not modify requirements, stories, use cases, gates, exclusions, traceability artifacts, validators, frontend/application code, package manifests, workflows, or architecture-decision records.
Do not start vertical-slice planning.

## Learning triage

Add one concise learning record:

`docs/governance/learning/DOPIS-LEARNING-008-technical-baseline-provenance-and-deferrals.md`

Record only:

- mixed-provenance decisions can misclassify promoted discovery directions as new or accepted;
- a deferred technical choice must be bound to the earliest real dependency/milestone, not a later convenient phase;
- prevention: check each baseline decision against canonical provenance and readiness milestone before assigning classification/resolution timing.

## Allowed writes

- `docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json`
- `docs/research/architecture/DOPIS_PLAN_003_MINIMUM_TECHNICAL_BASELINE_EVIDENCE.md` only if a factual/provenance statement needs corresponding correction
- `docs/README.md` only if its current text becomes inaccurate
- `docs/governance/learning/DOPIS-LEARNING-008-technical-baseline-provenance-and-deferrals.md`

This prompt file is immutable once executed.

## Revalidation

Recompute and report decision counts by classification and explicit deferred-decision count/topics.

Confirm:

- every decision has one accurate classification relative to canonical provenance;
- no decision rationale contradicts discovery;
- every deferred decision is bound to the earliest actual dependency/vertical/gate that must resolve it;
- SMS provider selection remains undecided in PLAN-003 but must resolve before first real pilot SMS capability;
- protected-staff auth implementation is not falsely blocked on production hosting;
- no product requirement, gate, story, use case, contract, validator, or code changed;
- implementation authority remains `NOT_GRANTED`;
- vertical-slice planning remains `NOT_STARTED`.

Run the locked GOV-GEN consumer validation, then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`

Validate the baseline JSON parses, decision IDs remain unique, classifications use only the declared vocabulary, deferred entries match DEFERRED decisions, all referenced repository artifacts resolve, and `git diff --check` passes.

## Publication

Commit and push the SAME branch.
Keep PR #10 draft.
Do not merge.
Do not start any later planning packet.

Because this is a material architecture-baseline correction, leave the exact pushed candidate for bounded independent delta review.

## Stop

Stop after successful push.

Report only:

- pre-correction HEAD;
- corrected candidate HEAD;
- changed files;
- decision counts by classification;
- deferred count/topics and corrected resolution timing for auth/SMS;
- validation results;
- confirmation upstream product/spec/code artifacts are unchanged;
- implementation authority `NOT_GRANTED`;
- vertical-slice planning `NOT_STARTED`.
