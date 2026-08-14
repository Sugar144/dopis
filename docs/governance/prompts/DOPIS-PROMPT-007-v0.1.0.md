# DOPIS-PROMPT-007 — DOPIS-PLAN-003 Minimum Technical Baseline

Prompt version: 0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-003`
Branch: `planning/minimum-technical-baseline`
Accepted base: `main @ 831571be7164076a84367e15ee4e5ee173d38faf`

This packet is authorised to prepare the minimum technical baseline required before vertical-slice design.
It does **not** grant implementation authority.

Use or create the authorised worktree if needed. Before mutation:

1. `git fetch origin`;
2. verify this repository/worktree/branch and clean status;
3. verify the branch starts from the repository-custodied prompt commit descended directly from the accepted base;
4. apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and the documentation authority map.

Stop read-only if repository identity, governing instructions, or framework acquisition/validation cannot be resolved.

## Objective

Create one compact, durable **minimum technical baseline** that is sufficient to constrain later vertical-slice and technical-contract design without prematurely designing implementation details.

The baseline must distinguish:

- technical decisions inherited from accepted repository/discovery state;
- provisional discovery directions promoted into the baseline candidate;
- genuinely new minimum technical decisions needed now;
- decisions deliberately deferred to a later vertical slice, contract, validation gate, or deployment decision.

Do not redesign the product, reopen business discovery, or turn this packet into a full architecture specification.

## Canonical references

Read only as needed:

- `AGENTS.md`
- `framework-lock.json`
- `docs/README.md`
- `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`
- `docs/current/requirements/DOPIS_VALIDATION_GATES.json`
- `docs/current/requirements/DOPIS_EXCLUSIONS.json`
- `docs/planning/DOPIS_USE_CASE_MODEL.json`
- `docs/backlog/DOPIS_STORIES.json`
- `frontend/package.json`
- current repository structure and existing frontend state-management evidence only where relevant.

Do not rewrite or reinterpret accepted product requirements through architecture prose.

## Research basis

A bounded primary-source research pass has already established the following useful design references. Record them in the evidence note with concise applicability, not as claims of formal compliance:

- FastAPI official documentation: Bigger Applications / `APIRouter`, dependency-based security, OpenAPI support;
- SQLAlchemy 2.0 official documentation: request/session transaction scope and explicit transaction management;
- PostgreSQL current documentation, Chapter 13: transaction isolation, row-level locking, and application-level consistency;
- RFC 9110: HTTP semantics;
- RFC 9457: Problem Details for HTTP APIs;
- OWASP Session Management Cheat Sheet and OWASP API Security Top 10 2023: secure browser sessions, authentication, object/function-level authorization;
- Docker official Compose documentation: local multi-container application definition and lifecycle.

If another primary source is materially necessary, use only official documentation/specification sources and record why it was needed. Do not perform broad technology comparison research.

## Required artifacts

Create:

`docs/research/architecture/DOPIS_PLAN_003_MINIMUM_TECHNICAL_BASELINE_EVIDENCE.md`

This is an evidence note, not an architecture decision document. Keep it short. For each source family record:

- source/standard;
- relevant principle;
- applicability to Dopis;
- what it does **not** decide.

Create:

`docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json`

Use a compact machine-readable structure with at least:

- `schema_version`;
- `baseline_id`: `DOPIS-PLAN-003`;
- `status`: `PREPARED`;
- `implementation_authority`: `NOT_GRANTED`;
- canonical source artifact references;
- evidence-note reference;
- `decisions` with stable IDs, concern, classification, decision, rationale, source references, downstream rule, and deferred detail where relevant;
- explicit `deferred_decisions`;
- explicit `non_goals`.

Decision classification vocabulary:

- `INHERITED_ACCEPTED`
- `PROMOTE_PROVISIONAL`
- `NEW_MINIMUM_BASELINE`
- `DEFERRED`

Decision IDs must be stable, unique, and use one consistent `TB-<DOMAIN>-NNN` form.

Update `docs/README.md` only to register the new evidence note and minimum technical baseline and to state that it grants no implementation authority.

## Minimum baseline content

The candidate must settle only the minimum necessary concerns below while preserving accepted discovery semantics.

### Repository and application topology

Preserve the accepted monorepo with independently buildable frontend and backend applications.

Do not introduce microservices, Kubernetes, a service mesh, a message broker, or another repository.

### Frontend baseline

Preserve the current frontend direction unless repository evidence proves otherwise:

- Vue 3;
- Vite;
- Vue Router;
- Tailwind CSS;
- JavaScript;
- scoped composable-first state management.

Do not migrate to TypeScript or Pinia in this packet. Pinia remains conditional on demonstrated shared-state pressure.
Do not upgrade dependency versions.

### Backend baseline

Promote the discovery's current backend direction into a **baseline candidate** unless a concrete canonical contradiction is found:

- Python / FastAPI;
- Pydantic transport validation;
- SQLAlchemy 2;
- Alembic;
- PostgreSQL;
- one modular-monolith backend application for the first MVP.

Define module/dependency boundaries conceptually, not as an implementation folder tree. Domain/application behavior must not depend directly on HTTP routers, ORM persistence objects, or provider SDKs.

### HTTP/API contract baseline

Use JSON REST semantics over HTTP and FastAPI-generated OpenAPI as the API description surface.
Respect RFC 9110 method/status semantics.
Use one consistent machine-readable HTTP error model based on RFC 9457 Problem Details rather than inventing unrelated error envelopes per endpoint.
Keep transport request/response models distinct from persistence models and domain behavior.

Do not populate endpoint inventories or per-story API contracts yet.

### Persistence, transactions, and concurrency

PostgreSQL is the authoritative operational data store for persisted MVP state. Frontend mocks/hard-coded data are not an operational source of truth.
Schema evolution uses Alembic migrations.

Establish the invariant that any operation whose accepted outcome depends on coordinated order, stock, capacity, hold, payment, or handover state must define one explicit transactional consistency boundary.

Do **not** choose a universal isolation level, row-lock recipe, advisory-lock strategy, optimistic versioning scheme, or retry algorithm in this packet. PostgreSQL/SQLAlchemy provide the mechanisms; each later technical contract must select the smallest correct mechanism for its invariant and prove concurrent behavior where required.

Do not introduce Redis or another cache/coordination store without a demonstrated need.

### Browser authentication and authorization

Preserve server-enforced authentication and authorization; frontend route guards are never sufficient.

Use a browser-session security baseline that keeps session credentials inaccessible to ordinary frontend JavaScript and applies secure cookie properties and CSRF protection appropriate to the eventual same-origin/cross-origin deployment topology.

Do not adopt localStorage bearer tokens as the default architecture.

Production hosting/topology is still deferred, so exact cookie domain/origin settings, identity provisioning, credential-reset flow, and session-storage implementation remain for the protected-staff vertical contract unless already fixed canonically.

Every protected operation must enforce object/function authorization on the backend according to accepted actor authority.

### Frontend/server state authority

The backend is authoritative for persisted catalog, orders, availability, stock, capacity, payment state, and auditable operational state.
Frontend state may cache or stage interaction state but must revalidate against authoritative server state at accepted consistency boundaries.

Do not prescribe a global client store solely for this reason.

### Realtime operational updates

Do not prematurely choose SSE versus WebSockets.
The backend must expose queryable authoritative state and preserve a polling-compatible fallback.
Realtime push is a replaceable transport concern and must not become the source of truth or leak into domain rules.
The exact transport is deferred to the first vertical slice that materially needs live kitchen updates.

### External integration boundaries

Preserve provider-neutral boundaries for:

- SMS/operational messaging;
- Epson-compatible receipt printing;
- payment terminal interaction.

Provider-specific credentials, device identifiers, protocols, and SDK details stay outside domain behavior and outside committed secrets.
Preserve the accepted APOS A8 manual-total fallback until Comercia provisioning and real-device evidence support a richer adapter implementation.
Dopis stores no card data.

Do not select an SMS provider in this packet.
Do not design provider-specific adapters in detail.

### Local environment and production deferral

Use Docker Compose as the local backend/PostgreSQL orchestration baseline while keeping the frontend independently runnable/buildable.

Production hosting, reverse proxy, TLS termination, public domain configuration, scaling topology, and production container orchestration remain deferred. Do not infer production architecture from GitHub Pages demo deployment.

### Configuration, secrets, time, money, and audit boundaries

Keep secrets out of Git and inject environment-specific secrets/configuration externally.
Operational thresholds that canonical requirements mark configurable/calibratable must remain configuration/data, not hard-coded architecture decisions.

Define only the minimum stable data semantics needed downstream:

- business scheduling is interpreted in the Dopis local timezone (`Europe/Madrid`);
- persisted event instants are timezone-aware and must have an unambiguous UTC representation;
- monetary values use an exact representation suitable for EUR and must never depend on binary floating-point arithmetic.

Keep domain audit records required by accepted requirements distinct from diagnostic application logs. Diagnostic logs must not become a second business source of truth and must avoid unnecessary personal/sensitive data.

Do not choose an observability vendor or logging platform.

### Testing boundary

The baseline may name `pytest` for backend testing because it is part of the provisional stack, but do not author technical acceptance tests or a full test strategy.
Later technical contracts must prove transactional/concurrency invariants at the smallest affected surface and use real PostgreSQL behavior where database semantics matter.

## Mandatory deferrals / non-goals

At minimum, keep these outside PLAN-003 unless canonical evidence already fixes them:

- production hosting/provider/topology;
- SMS provider;
- SSE versus WebSockets;
- exact endpoint inventory;
- exact database schema;
- universal transaction isolation/locking algorithm;
- queue/background-worker/cache technology;
- detailed staff credential lifecycle;
- provider-specific printer/payment-terminal implementation;
- online payment architecture;
- Pinia/TypeScript migration;
- Kubernetes/microservices;
- vertical slices;
- ADRs and per-vertical technical contracts;
- technical acceptance criteria;
- tests/tasks/execution packets;
- application implementation.

If a minimum baseline decision cannot be made without a genuinely new material Owner choice, record the exact decision as `DEFERRED` with the blocking reason instead of guessing.

## Authority and write surface

Allowed semantic writes:

- `docs/research/architecture/DOPIS_PLAN_003_MINIMUM_TECHNICAL_BASELINE_EVIDENCE.md`
- `docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json`
- `docs/README.md`

The custodied prompt file is immutable once executed.
Do not modify requirements, epics, stories, use cases, gates, exclusions, traceability contracts/matrix, validators, frontend/application code, package manifests, workflows, or architecture-decision records.

No implementation authority is granted.
No later planning packet is authorised.

## Validation

Before publication:

1. acquire and validate the locked GOV-GEN consumer;
2. run `python scripts/validate_specification.py`;
3. run `python scripts/test_validate_specification.py`;
4. validate the new JSON parses successfully;
5. deterministically verify decision IDs are unique and all repository artifact references used as authority/evidence resolve;
6. verify every decision is one of the four classification values and every `DEFERRED` decision states what later gate/contract/decision must resolve it;
7. verify there are no endpoint inventories, schemas, ADRs, vertical slices, tests, tasks, or implementation changes;
8. run `git diff --check`;
9. confirm the diff is limited to the authorised write surface plus this already-custodied prompt.

Because this creates a material architectural planning baseline, leave the final exact pushed candidate for independent review.

## Publication

Commit and push the same branch using the configured authenticated remote.
Do not merge.
Do not start vertical-slice planning.

## Stop

Stop after successful push.

Report only:

- accepted base;
- custody starting HEAD;
- candidate HEAD;
- changed files;
- number of baseline decisions by classification;
- explicit deferred-decision count and topics;
- validation results;
- confirmation that requirements/stories/use cases/gates/contracts/code remain unchanged;
- implementation authority `NOT_GRANTED`;
- vertical-slice planning `NOT_STARTED`.
