# Dopis MVP Requirements Research Note

**Phase:** Specification Phase S1 — MVP requirements baseline and epic map
**Status:** `AUDITED_PENDING_OWNER_APPROVAL`
**Baseline version:** `0.3`
**Date:** `2026-07-25`
**Canonical project source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`
**Implementation authority:** `NOT GRANTED`

## 1. Research questions

1. Which properties make an MVP requirement suitable for review and later verification?
2. How should business rules, behaviour, data obligations, quality attributes, validation gates, and implementation decisions be separated?
3. How should unresolved values be represented without converting assumptions into facts?
4. What traceability structure supports forward coverage, reverse impact analysis, orphan detection, and supersession?
5. How should epics be defined without treating technical layers as business capabilities?
6. How can a specification validator be made falsifiable rather than self-confirming?

Question 6 was added by the version `0.3` audit, after the version `0.2` validator was found to pass largely because its expectations had been copied from the artifacts it was checking.

## 2. Authoritative sources reviewed

- ISO/IEC/IEEE 29148:2018, *Systems and software engineering — Life cycle processes — Requirements engineering*, official ISO catalogue entry: <https://www.iso.org/standard/72089.html>
- ISO/IEC 25010:2023, *Systems and software Quality Requirements and Evaluation — Product quality model*, official ISO catalogue entry: <https://www.iso.org/standard/78176.html>
- NASA, *Appendix C — How to Write a Good Requirement*: <https://www.nasa.gov/reference/appendix-c-how-to-write-a-good-requirement/>
- NASA Software Engineering Handbook, SWE-050 — *Software Requirements*: <https://swehb.nasa.gov/display/SWEHBVD/SWE-050+-+Software+Requirements>
- NASA Software Engineering Handbook, SWE-053 — *Manage Requirements Changes*: <https://swehb.nasa.gov/display/7150/SWE-053+-+Manage+Requirements+Changes>
- Agile Alliance glossary — *Epic*: <https://agilealliance.org/glossary/epic/>

The published 2018 requirements standard is used rather than treating a draft future edition as normative. External sources define quality criteria for how Dopis requirements are written and checked. They never create a Dopis business obligation.

## 3. Audit criteria derived from the guidance

| Criterion | Derived from | Applied as |
|---|---|---|
| Necessary, unambiguous, verifiable, traceable, singular | ISO/IEC/IEEE 29148 characteristics of individual requirements | One obligation per record; a `verification_method` on every record; `business_source` resolved against real canonical headings |
| Complete, consistent, non-redundant, bounded | ISO/IEC/IEEE 29148 characteristics of a requirement set | Independent reconstruction of the canonical obligation inventory before comparing against the baseline; machine-checked exclusions |
| Avoid vague and unverifiable terms | NASA Appendix C | Vague terms permitted only where the record links the gate that will make the term measurable, and says so in `notes` |
| State the outcome, not the design | NASA Appendix C | Mechanisms retained only where canonical discovery makes them a genuine business, security, or operational constraint |
| Bidirectional traceability | NASA SWE-050 | Every relation derived from a named field and recomputed on each validation run |
| Manage change with recorded supersession | NASA SWE-053 | Stable identifiers preserved; retired validation gates recorded with the gate that now carries the concern |
| Quality characteristics are selected, not adopted wholesale | ISO/IEC 25010 | Only reliability, usability, operability, and security attributes with canonical business backing became `NFR` records |
| Epics are capabilities, not layers | Agile Alliance | Thirteen business capabilities; every requirement has exactly one owning epic |

## 4. Guidance deliberately not adopted

- **Formal ISO conformance or certification.** Dopis is a two-person pizzeria pilot; the standards are used as quality criteria, not as a compliance target.
- **The full ISO/IEC 25010 characteristic set.** Adopting every characteristic would manufacture obligations the discovery never expressed. Portability, maintainability, and functional-suitability sub-characteristics were not turned into requirements.
- **The `shall` sentence template from ISO/IEC/IEEE 29148.** The baseline uses a single consistent imperative form instead. Mixing forms would be worse than either, and rewriting every statement would have produced churn without improving verifiability. The validator instead rejects statements that open with a weak modal verb, which is the failure mode the template exists to prevent.
- **A duplicated heavyweight SRS.** The machine registry is normative; the Markdown baseline is a governed summary that the validator forces into agreement.
- **Epics as delivery promises.** The epic map states explicitly that it implies no order, estimate, or authority.
- **External guidance as a substitute for Jaime's decisions.** No standard was used to close an open business question.

## 5. Where professional judgement was required

Four decisions were not determined by the guidance and are recorded so the Project Owner can overrule them.

1. **Derived validation gates.** Canonical discovery leaves several questions explicitly open without assigning them an identifier. Rather than silently attaching them to an unrelated gate or inventing scope, three gates are declared with `origin: DERIVED` and a written derivation rationale: `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, and `JV-INCIDENT-FAIRNESS`. The validator refuses a derived gate that lacks a rationale. The Project Owner has provisionally accepted all three as specification-derived validation nodes only: they do not become canonical section 15 gates and must retain `origin: DERIVED`.
2. **Separating acceptance from milestone.** Version `0.2` used one `classification` enum mixing acceptance state, milestone, decision ownership, and calibration. Splitting `acceptance_state` from `readiness_milestone` was a judgement call; it is what made the misclassified allergen requirements visible.
3. **Requirement granularity.** Statements were split only where separate verification, ownership, or gating was justified. Inseparable invariants were left whole even when they read as compound sentences.
4. **Priority of presentational obligations.** Canonical content rules that affect presentation rather than safety or operation were recorded at `SHOULD_MVP` or `COULD_MVP` rather than dropped, because the discovery states them but the MVP objective does not depend on them.

## 6. Method of independent reconstruction

The audit did not begin from the version `0.2` baseline. It began from the canonical discovery read in full, from which an obligation inventory was extracted across confirmed scope, exclusions, actors, customer behaviour, staff and kitchen workflows, business rules and invariants, lifecycle states, exception paths, catalog and modifier rules, allergen and food-safety duties, stock, capacity, channels, communications, tracking protection, payment and handover, privacy and retention, pilot controls, quality attributes, auditability, unresolved decisions, calibrated values, and public-launch blockers.

Only afterwards was that inventory compared against the existing records. The comparison is what produced the omissions listed in the audit report, rather than a reading of the previous baseline's own claims. The requirement count was treated as an output of the evidence, not as a target: it moved from 84 to 210 because the reconstruction found 126 canonical obligations with no representation. The subsequent Project Owner review moved it to 216, by splitting three records whose parts had different acceptance states and by adding the two canonical milestone entry conditions that had no baseline representation; see section 17 of the audit report.

## 7. Validation approach

`scripts/validate_specification.py` derives every total from the artifacts. It resolves each `business_source` entry against headings parsed from the canonical discovery, resolves every gate against the gate registry, resolves every epic and dependency reference, detects dependency cycles, recomputes all nineteen orphan expectations declared by the traceability matrix, checks that no exclusion term appears outside the requirement that states it, forces the Markdown baseline to agree with the registry, rejects any requirement referencing a retired gate, requires every blocked requirement to justify why its candidate obligation cannot yet be accepted as final, and fails if any artifact claims implementation authority.

`scripts/test_validate_specification.py` is the answer to research question 6. It copies the artifacts into a temporary tree, introduces one controlled defect per case, and asserts rejection with a recognisable message. Twenty-three defect classes are covered, plus a control case asserting the unmutated artifacts still pass. Six of them were added by the Owner-review correction pass to enforce the corrected BLOCK semantics, and no fixture hard-codes a requirement total. No fixture state is written to the repository.

## 8. Remaining boundary

Architecture, API, database design, use cases, stories, acceptance criteria, tasks, and tests remain future governed artifacts. `BASELINED` records an accepted obligation for specification only. Implementation authority remains `NOT GRANTED`.
