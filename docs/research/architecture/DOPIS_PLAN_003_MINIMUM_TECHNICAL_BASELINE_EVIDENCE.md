# DOPIS-PLAN-003 Minimum Technical Baseline — Evidence Note

**Status:** `PREPARED`
**Implementation authority:** `NOT_GRANTED`
**Canonical project source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.19`
**Related artifact:** `docs/planning/DOPIS_MINIMUM_TECHNICAL_BASELINE.json`

## Purpose

This is an evidence note, not an architecture decision document. It records, per primary
source, the principle used, its applicability to Dopis, and what it deliberately does not
decide. It supports the decisions in `DOPIS_MINIMUM_TECHNICAL_BASELINE.json` without
restating canonical requirements or reopening business discovery.

## 1. FastAPI official documentation — Bigger Applications / `APIRouter`, dependency-based security, OpenAPI

- **Principle:** Large FastAPI applications are structured with `APIRouter` per feature area, shared dependencies express cross-cutting concerns (authentication, authorization), and OpenAPI generation is a byproduct of typed path operations rather than a separately maintained document.
- **Applicability:** Supports keeping the backend one modular-monolith application (discovery §5.3) with conceptual module boundaries instead of a folder-tree prescription, and using FastAPI-generated OpenAPI as the API description surface.
- **Does not decide:** router file layout, dependency-injection wiring for a specific module, or which endpoints exist.

## 2. SQLAlchemy 2.0 official documentation — request/session transaction scope, explicit transaction management

- **Principle:** SQLAlchemy 2.0's unit-of-work pattern expects one session/transaction scoped per unit of work (typically one request), with explicit `begin`/`commit`/`rollback` boundaries rather than implicit autocommit behavior.
- **Applicability:** Grounds the baseline invariant that any operation whose accepted outcome depends on coordinated order/stock/capacity/hold/payment/handover state must define one explicit transactional consistency boundary.
- **Does not decide:** isolation level, row-lock strategy, optimistic-versioning scheme, or retry algorithm for any specific operation — each later technical contract selects its own smallest correct mechanism.

## 3. PostgreSQL current documentation, Chapter 13 — transaction isolation, row-level locking, application-level consistency

- **Principle:** PostgreSQL offers multiple isolation levels and explicit row-level locking primitives; the correct choice is workload-specific, and default `READ COMMITTED` does not by itself prevent all application-level race conditions (e.g., lost updates on concurrently read-then-written rows).
- **Applicability:** Confirms that PostgreSQL supplies the mechanisms needed for concurrency-sensitive invariants (stock, capacity, payment/handover) without the baseline having to pick one universal mechanism now.
- **Does not decide:** which isolation level or locking primitive applies to which invariant; that remains for the technical contract that owns each concurrency-sensitive operation.

## 4. RFC 9110 — HTTP Semantics

- **Principle:** Defines standard HTTP method semantics (safety, idempotency) and status-code meaning.
- **Applicability:** Grounds the baseline's requirement to respect RFC 9110 method/status semantics for the JSON REST API contract, instead of inventing ad hoc method/status conventions per endpoint.
- **Does not decide:** the endpoint inventory or any specific route's method/status choice.

## 5. RFC 9457 — Problem Details for HTTP APIs

- **Principle:** Defines one standard machine-readable JSON error format (`type`, `title`, `status`, `detail`, `instance`, extensible members) for HTTP API error responses.
- **Applicability:** Grounds the baseline decision to use one consistent Problem-Details-based error model across the API rather than a distinct error envelope per endpoint.
- **Does not decide:** the specific `type` URIs or extension members used by individual error conditions.

## 6. OWASP Session Management Cheat Sheet and OWASP API Security Top 10 2023

- **Principle:** Session Management: keep session tokens inaccessible to JavaScript (e.g., `HttpOnly` cookies), apply `Secure`/`SameSite` cookie attributes, and pair cookie-based sessions with CSRF protection. API Security Top 10: enforce object-level and function-level authorization on the server for every protected operation; never trust client-side authorization alone.
- **Applicability:** Grounds the baseline's browser authentication/authorization decisions — server-enforced session-based auth with credentials inaccessible to ordinary frontend JavaScript, secure cookie properties, CSRF protection, and mandatory backend object/function authorization on every protected operation. Directly supports discovery §11.7's requirement to "protect kitchen and administration endpoints" and "enforce role and session boundaries."
- **Does not decide:** exact cookie domain/origin values, identity-provisioning mechanism, or credential-reset flow — these depend on the still-deferred production hosting topology (discovery §13.3) and remain for the protected-staff vertical contract.

## 7. Docker official Compose documentation

- **Principle:** Compose defines and orchestrates multi-container local applications (service, network, volume definitions) from one declarative file, suited to reproducible local development environments.
- **Applicability:** Grounds using Docker Compose as the local backend/PostgreSQL orchestration baseline (discovery §13.2 "Proposed local stack"), while the frontend remains independently runnable/buildable outside the container set.
- **Does not decide:** production container orchestration, scaling topology, or deployment strategy — explicitly deferred (discovery §13.3).

## Boundary

No source above was used to settle a business requirement, reopen discovery, or select a
production topology, SMS provider, transport (SSE vs. WebSockets), universal isolation
level, or provider-specific integration detail. Those remain `DEFERRED` in
`DOPIS_MINIMUM_TECHNICAL_BASELINE.json`.
