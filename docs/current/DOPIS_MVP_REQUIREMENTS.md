# Dopis MVP Requirements Baseline

**Milestone:** `MILESTONE-SPEC-001`  
**Status:** `REVIEWED_PENDING_OWNER_APPROVAL`  
**Baseline version:** `0.2`  
**Date:** `2026-07-25`  
**Business source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`  
**Business discovery status:** `CLOSED_PENDING_VALIDATION_AND_IMPLEMENTATION_PLANNING`  
**Implementation authority:** `NOT GRANTED`

## 1. Purpose and authority

This baseline translates the closed first-MVP business discovery into uniquely identified requirements. It does not authorise implementation, define the API or database, or supersede unresolved Jaime validation gates.

Where a requirement conflicts with canonical discovery, the affected scope must stop and be reconciled explicitly rather than resolved silently.

## 2. Authoritative registry

The normative requirement records are stored as four machine-readable JSON documents, which are also valid YAML 1.2:

- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS_PART_1.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS_PART_2.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS_PART_3.json`
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS_PART_4.json`

Together they contain **84 unique requirements**. Splitting the registry keeps individual files reviewable while preserving one governed baseline version.

Every active record contains:

- stable `id` and class;
- normative statement;
- classification;
- lifecycle status;
- MVP priority;
- verification method;
- canonical source sections;
- typed validation-gate links.

## 3. Taxonomy

Classes:

- `FR`: functional behaviour;
- `BR`: business rule or invariant;
- `DATA`: data obligation;
- `SEC`: security or access;
- `PRIV`: privacy;
- `NFR`: quality attribute;
- `AUDIT`: audit or evidence;
- `PILOT`: pilot governance;
- `OPS`: operational constraint.

Classifications:

- `ACCEPTED_BUSINESS_RULE`;
- `PENDING_JAIME_VALIDATION`;
- `PILOT_CALIBRATION`;
- `PUBLIC_LAUNCH_BLOCKER`.

Statuses:

- `BASELINED`: accepted for specification only;
- `BLOCKED_BY_VALIDATION`: not implementation-ready until at least one blocking gate is resolved.

Gate effects:

- `BLOCK`: prevents readiness;
- `CALIBRATE`: sets or adjusts an operational value through evidence;
- `VALIDATE`: confirms wording, procedure, or evidence without reopening the accepted obligation.

Verification methods:

- `TEST`;
- `SECURITY_TEST`;
- `INSPECTION`;
- `ANALYSIS`;
- `DEMONSTRATION`;
- `PILOT_EVIDENCE`;
- `BUSINESS_REVIEW`.

## 4. Independent-review corrections

Version `0.2` adds explicit coverage missing from the first draft for:

- telephone and in-person order entry;
- order-origin recording;
- automatic, manual-review, and paused ordering modes;
- acceptance or rejection of alternative pickup times;
- customer response to important delays;
- readiness checklist, responsible-person registration, and explicit opening;
- kitchen touch, contrast, and no-hover usability;
- dynamic final-order cutoff;
- material estimate communication;
- shift cash reconciliation and responsible close;
- incident handling without automatic customer blocking;
- caller verification before disclosure;
- report and export restrictions;
- weekly pilot reporting.

The review also replaces ambiguous validation links with typed `BLOCK`, `CALIBRATE`, and `VALIDATE` effects.

## 5. Explicit exclusions

The following remain outside the first operational MVP unless promoted through an authorised scope change:

- online payment;
- customer accounts and loyalty;
- birthday benefits and marketing campaigns;
- delivery and table reservations;
- coffee products;
- customer self-service cancellation;
- gram-level recipe inventory;
- automatic substitutions;
- automatic recommendation engines;
- advanced analytics and product-margin reporting;
- production hosting and public-domain readiness as part of the local operational implementation slice.

## 6. Implementation-readiness boundary

No requirement is implementation-ready merely because it is `BASELINED`. Readiness additionally requires linked use cases and exception flows, measurable acceptance criteria, reviewed architecture decisions and contracts, resolved blocking gates, dependency and test strategy, and an explicitly authorised bounded task packet.

`scripts/validate_specification.py` validates identifiers, metadata, gate semantics, epic coverage, cross-file consistency, and orphan claims without external dependencies.
