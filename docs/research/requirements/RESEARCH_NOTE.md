# Dopis MVP Requirements Research Note

**Phase:** Specification Phase S1 — MVP requirements baseline and epic map  
**Status:** REVIEWED_PENDING_OWNER_APPROVAL  
**Date:** 2026-07-25  
**Canonical project source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`  
**Implementation authority:** `NOT GRANTED`

## 1. Research questions

1. Which properties make an MVP requirement suitable for review and later verification?
2. How should business rules, behaviour, data obligations, quality attributes, validation gates, and implementation decisions be separated?
3. How should unresolved values be represented without converting assumptions into facts?
4. What traceability structure supports forward coverage, reverse impact analysis, orphan detection, and supersession?
5. How should epics be defined without treating technical layers as business capabilities?

## 2. Authoritative sources reviewed

- ISO/IEC/IEEE 29148:2018, official ISO catalogue: <https://www.iso.org/standard/72089.html>
- ISO/IEC 25010:2023, official ISO catalogue: <https://www.iso.org/standard/78176.html>
- NASA, Appendix C — How to Write a Good Requirement: <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>
- NASA Software Engineering Handbook, SWE-050 — Software Requirements: <https://swehb.nasa.gov/display/SWEHBVD/SWE-050+-+Software+Requirements>
- NASA Software Engineering Handbook, SWE-053 — Manage Requirements Changes: <https://swehb.nasa.gov/display/7150/SWE-053+-+Manage+Requirements+Changes>
- Agile Alliance glossary — Epic: <https://agilealliance.org/glossary/epic/>

The published 2018 requirements standard is used rather than treating a draft future edition as normative. External sources guide specification quality; they do not create Dopis business rules.

## 3. Adopted guidance

A baselinable requirement must be necessary, uniquely identified, atomic enough for later verification, explicit about its actor or system obligation, traceable to canonical evidence, and independent of implementation unless a genuine constraint requires otherwise.

Unresolved numeric values do not become invented facts. The requirement may establish the existence of a configurable rule while a typed validation link records whether the missing decision blocks readiness, calibrates an accepted rule, or validates stakeholder evidence.

Epics represent customer or operational capabilities, never code layers such as frontend, backend, API, or database.

## 4. Dopis taxonomy

Requirement classes are `FR`, `BR`, `DATA`, `SEC`, `PRIV`, `NFR`, `AUDIT`, `PILOT`, and `OPS`.

Classifications used in this baseline are:

- `ACCEPTED_BUSINESS_RULE`;
- `PENDING_JAIME_VALIDATION`;
- `PILOT_CALIBRATION`;
- `PUBLIC_LAUNCH_BLOCKER`.

Validation effects are:

- `BLOCK`: prevents readiness;
- `CALIBRATE`: sets or adjusts a value through observation;
- `VALIDATE`: confirms wording, procedure, or evidence without reopening the accepted obligation.

## 5. Independent review findings and disposition

The first draft was not ready to merge. It declared metadata fields that were not present consistently, omitted several discovered capabilities, used ambiguous gate semantics, and asserted zero orphan links without a reproducible check.

Version `0.2` corrects those problems by:

1. replacing the aspirational metadata contract with a complete tabular registry;
2. adding explicit requirements for manual channels, order origin, ordering modes, alternative-slot and delay responses, opening readiness, kitchen usability, dynamic cutoff, material estimate communication, cash close, incident handling, caller verification, report/export restrictions, and weekly pilot reporting;
3. distinguishing blocking, calibration, and validation gate effects;
4. encoding epic and traceability artifacts as JSON, which is a valid YAML 1.2 subset;
5. adding `scripts/validate_specification.py`, using only the Python standard library.

## 6. Validation result

The reviewed registry contains **84 unique requirements**, **11 business-capability epics**, and **17 validation gates**.

The validator checks:

- JSON/YAML syntax for machine-readable artifacts;
- unique and structurally valid requirement IDs;
- class-prefix consistency;
- allowed statuses, classifications, priorities, and verification methods;
- mandatory `BLOCK:*` links for blocked requirements;
- references to existing requirement IDs;
- complete epic coverage;
- exact agreement between the epic map and traceability matrix;
- exact agreement between requirement gate metadata and traceability links;
- accuracy of declared orphan-check arrays.

## 7. Guidance not adopted

Dopis does not adopt formal ISO certification, every ISO 25010 characteristic as an MVP obligation, a duplicated heavyweight SRS, technology choices as requirements, epics as delivery promises, or external guidance as a substitute for Jaime's decisions.

## 8. Remaining boundary

Architecture, API, database design, use cases, stories, acceptance criteria, tasks, and tests remain future governed artifacts. `BASELINED` never means implementation authority. Implementation remains `NOT GRANTED`.
