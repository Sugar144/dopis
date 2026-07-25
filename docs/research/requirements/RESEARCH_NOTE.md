# Dopis MVP Requirements Research Note

**Phase:** Specification Phase S1 — MVP requirements baseline and epic map  
**Status:** DRAFT_FOR_REVIEW  
**Date:** 2026-07-25  
**Canonical project source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`  
**Implementation authority:** `NOT GRANTED`

## 1. Research questions

1. Which properties make an MVP requirement suitable for review and later verification?
2. How should business rules, functional behaviour, data obligations, quality attributes, validation gates, and implementation decisions be separated?
3. How should unresolved values be represented without converting assumptions into facts?
4. What traceability structure supports forward coverage, reverse impact analysis, orphan detection, and supersession?
5. How should epics be defined without treating code layers as business capabilities?

## 2. Sources reviewed

### ISO/IEC/IEEE 29148:2018

Official ISO catalogue entry:

- <https://www.iso.org/standard/72089.html>

The published standard defines requirements-engineering processes, information items, and characteristics for requirements in systems and software engineering. ISO lists a later revision as under development; this note relies on the published 2018 edition rather than treating a draft edition as normative.

### ISO/IEC 25010:2023

Official ISO catalogue entry:

- <https://www.iso.org/standard/78176.html>

The product-quality model is used as a completeness checklist for relevant quality attributes. Dopis does not adopt every quality characteristic as an MVP requirement merely because it appears in the model.

### NASA — Appendix C: How to Write a Good Requirement

Official source:

- <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>

Relevant guidance includes one obligation per requirement, clear subject and predicate, measurable values, avoidance of ambiguous adjectives, explicit rationale and assumptions, unique identification, feasibility, and bidirectional traceability.

### NASA Software Engineering Handbook — Software Requirements

Official source:

- <https://swehb.nasa.gov/display/SWEHBVD/SWE-050+-+Software+Requirements>

Relevant guidance includes decomposition from higher-level expectations, traceability to the originating need, and avoidance of unsupported lower-level requirements.

### NASA Software Engineering Handbook — Manage Requirements Changes

Official source:

- <https://swehb.nasa.gov/display/7150/SWE-053+-+Manage+Requirements+Changes>

Relevant guidance includes impact analysis, controlled baseline changes, and preserving traceability when a requirement changes.

### Agile Alliance — Epic

Official glossary entry:

- <https://agilealliance.org/glossary/epic/>

An epic is a body of work too large for one iteration that can be divided into smaller stories. The source does not prescribe one universal epic format.

## 3. Relevant guidance

### 3.1 Requirement quality

A baselinable requirement should be:

- necessary for an accepted Dopis objective or rule;
- atomic enough to verify without interpreting multiple independent obligations;
- unambiguous in its actors, conditions, and outcome;
- feasible within the declared product boundary;
- implementation-independent unless a genuine constraint requires a technology or mechanism;
- uniquely identified;
- traceable to canonical project evidence;
- associated with at least one verification method;
- explicitly classified when blocked by stakeholder validation or pilot calibration.

### 3.2 Requirement classes

The baseline separates:

- functional behaviour (`FR-*`);
- business invariants (`BR-*`);
- data obligations (`DATA-*`);
- security and access (`SEC-*`);
- privacy (`PRIV-*`);
- quality attributes (`NFR-*`);
- audit and evidence (`AUDIT-*`);
- pilot governance (`PILOT-*`);
- operational constraints (`OPS-*`).

This separation prevents implementation details, validation questions, and operational procedures from being mixed into one undifferentiated list.

### 3.3 Pending values and validation

A requirement may define that a threshold exists and is configurable while leaving the initial value unresolved. The unresolved value is linked to a `JV-*` gate and the requirement remains `BLOCKED_BY_VALIDATION` where the missing value prevents complete verification.

No numeric value is invented merely to make a statement appear complete.

### 3.4 Traceability

Traceability should support:

- source decision to requirement;
- requirement to epic;
- requirement to validation gate;
- later requirement to use case, story, acceptance criterion, architecture decision, task, test, and release evidence;
- reverse navigation for impact analysis;
- explicit supersession rather than silent rewriting.

Stable identifiers and typed links are preferable to duplicated prose or document hyperlinks alone.

### 3.5 Epics

Epics represent coherent operational or customer capabilities. The baseline therefore avoids epics named after technical layers such as database, backend, API, or frontend.

## 4. Applicability to Dopis

The canonical discovery contains both accepted business rules and provisional technical proposals. Specification Phase S1 applies the following boundary:

- accepted operating rules become requirements;
- pending Jaime decisions become validation links;
- pilot-calibrated values remain configurable and unresolved;
- provisional frameworks, ORM choices, transport choices, table layouts, and candidate fields do not become requirements;
- architecture derives later from the reviewed requirement and use-case baseline.

## 5. Guidance not adopted

Dopis does not adopt:

- formal ISO certification as an MVP objective;
- a heavy duplicated software-requirements specification;
- every ISO 25010 quality characteristic as a mandatory MVP requirement;
- epics as estimates or contractual delivery promises;
- implementation technology merely because an external source recommends it;
- external guidance as a substitute for Jaime's business decisions;
- a draft future edition of a standard as though it were the current published authority.

## 6. Resulting design decisions

1. Requirement IDs use `<CLASS>-<DOMAIN>-<SEQUENCE>`.
2. Requirement statements use normative wording and avoid design detail.
3. Every requirement records source, priority, status, verification, dependencies, and validation gates.
4. `BASELINED` means the obligation is accepted, not that implementation is authorised.
5. `BLOCKED_BY_VALIDATION` means the requirement exists but one or more linked gates prevent complete readiness.
6. Epics map business capabilities to requirement IDs.
7. The traceability matrix uses typed links and supports future node classes without duplicating requirement text.
8. No story or task can be considered ready merely because a requirement link exists.

## 7. Open uncertainties

- The local checkout state could not be inspected from the connected environment; the branch is created from the verified remote `main` commit.
- Exact values, named delegates, safety wording, catalog content, and several operating procedures remain governed by the existing `JV-*` gates.
- Verification criteria will become more concrete during use-case, acceptance-criteria, architecture, and test-design phases.
- The canonical discovery header and sequencing language contain minor metadata inconsistencies; these should be reconciled through a separate complete-file edit because partial replacement of the 3,000-line canonical artifact would be unsafe.

## 8. Source references

Project decisions remain governed by:

- `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`;
- its referenced `BD-DELTA-*` reconciliation history;
- future bounded Jaime validation resolutions.

External sources provide specification guidance only. They do not create Dopis business requirements.
