# Dopis MVP Requirements Baseline

**Milestone:** `MILESTONE-SPEC-001`
**Status:** `AUDITED_PENDING_OWNER_APPROVAL`
**Baseline version:** `0.3`
**Date:** `2026-07-25`
**Business source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`
**Business discovery status:** `CLOSED_PENDING_VALIDATION_AND_IMPLEMENTATION_PLANNING`
**Implementation authority:** `NOT GRANTED`

<!-- Machine-checked agreement markers. scripts/validate_specification.py recomputes
     each value from the registries and fails if this document disagrees. -->

    REGISTRY-VERSION: 0.3
    REGISTRY-TOTAL: 210
    REGISTRY-EPICS: 13

## 1. Purpose and authority

This baseline translates the closed first-MVP business discovery into uniquely identified requirements. It does not authorise implementation, define the API or database, or resolve any unresolved stakeholder decision.

Canonical discovery has priority over this document. Where the two conflict, the affected scope stops and returns to explicit business validation rather than being reconciled silently.

Version `0.3` is the result of an independent requirements audit of version `0.2`. The audit findings, evidence, and disposition are recorded in `docs/reviews/MILESTONE_SPEC_001_AUDIT.md`.

## 2. Authoritative artifacts

| Artifact | Role |
|---|---|
| `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json` | Normative requirement records |
| `docs/current/requirements/DOPIS_VALIDATION_GATES.json` | Validation gate definitions, milestones, and origin |
| `docs/current/requirements/DOPIS_EXCLUSIONS.json` | Machine-checkable first-MVP exclusions |
| `docs/backlog/DOPIS_EPICS.json` | Business-capability epic map |
| `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json` | Traceability contract and orphan expectations |
| `scripts/validate_specification.py` | Reproducible integrity validation |
| `scripts/test_validate_specification.py` | Negative tests proving the validator detects defects |

The registry is a single file. Version `0.2` split it into four arbitrary parts of twenty-one records each, which forced the validator to hard-code both the part count and the requirement total. Consolidation removed that coupling.

## 3. Requirement record contract

Every record carries: `id`, `statement`, `class`, `acceptance_state`, `readiness_milestone`, `status`, `priority`, `rationale`, `business_source`, `verification_method`, `validation_links`, `dependencies`, and `notes`.

**Classes:** `FR` behaviour, `BR` business rule or invariant, `DATA` data obligation, `SEC` security or access, `PRIV` privacy, `NFR` quality attribute, `AUDIT` audit or evidence, `PILOT` pilot governance, `OPS` operational constraint.

**Acceptance state** — is the obligation itself settled?

- `ACCEPTED`: confirmed by canonical discovery;
- `PROVISIONAL`: a canonical working direction whose wording or rule may still change;
- `CONDITIONAL`: exists only if a stakeholder decision promotes it.

**Readiness milestone** — by when must it hold? `PILOT`, `WITHOUT_JAIME`, or `PUBLIC_LAUNCH`.

**Status** — `BASELINED`, or `BLOCKED_BY_VALIDATION` if and only if at least one gate link has effect `BLOCK`. The validator enforces the equivalence in both directions.

Version `0.2` used a single `classification` field mixing four unrelated dimensions — acceptance state, milestone, decision ownership, and calibration. Splitting acceptance state from readiness milestone is what exposed the misclassified allergen requirements described in section 5.

**Gate effects:**

- `BLOCK`: the obligation cannot be specified or implemented until the gate resolves;
- `CALIBRATE`: the obligation is accepted; a value or operating rule comes from evidence;
- `VALIDATE`: the obligation is accepted; wording, procedure, or confirmation is outstanding.

**Verification methods:** `TEST`, `SECURITY_TEST`, `INSPECTION`, `ANALYSIS`, `DEMONSTRATION`, `PILOT_EVIDENCE`, `BUSINESS_REVIEW`.

## 4. Validation gates

Fifteen gates come verbatim from the canonical validation register in discovery section 15, plus two closed gates retained for traceability. Three further gates are marked `DERIVED`: `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, and `JV-INCIDENT-FAIRNESS`. Each names a bounded question that canonical discovery leaves explicitly open without assigning it an identifier, and each carries a written derivation rationale. The validator refuses a derived gate that lacks one.

Version `0.2` used two gate identifiers that appear nowhere in canonical discovery and were not marked as derived, while omitting the two closed gates. The resulting total coincidentally matched the canonical count of seventeen, which concealed the substitution. The audit report names both identifiers and records their disposition.

## 5. Audit corrections in version `0.3`

**Food safety.** Version `0.2` covered gluten only with the rule not to claim coeliac suitability. Discovery section 10.3 additionally requires a general menu cross-contact warning, a specific warning on selection, explicit customer acknowledgement, a statement that online ordering cannot guarantee absence of cross-contact, independent disablement of the option, and disablement whenever the validated procedure cannot be followed. All are now specified, together with allergen warnings on substitution, dietary recalculation, and the rule that a free-text note may never override configured modifier, price, availability, or allergen rules.

**Milestone correction.** Allergen and catalog-publication requirements were labelled public-launch blockers. Discovery section 18A requires validated product-specific allergen data before the first real pilot order. They are now `PILOT`-milestone obligations. Conversely, `PRIV-DATA-001`, `PRIV-DATA-002`, and `PRIV-DATA-003` were blocked on a public-launch gate even though sections 11.4, 12.4, and 18A require minimum privacy controls from the first real order; they are now baselined pilot obligations, and `OPS-PILOT-001` makes that binding.

**Over-blocking.** Manual channel entry, the payment and handover model, stock counting, catalog administration, report access, and weekly reporting were marked blocked although canonical discovery accepts each obligation and leaves only procedure or calibration open. They are baselined with `VALIDATE` or `CALIBRATE` links.

**Omissions now specified.** The operational threshold register that every `JV-THRESHOLDS` link resolves through, the pending-Jaime decision record, substitution rules and the absorbed price-difference limit, the non-collection process, transactional capacity and stock commitment, the provisional checkout hold, tracking-SMS delivery failure routing, alternative-slot expiry, approximate critical-ingredient allowances, queue ordering by recommended preparation time, telephone-support disclosure limits, card-data storage prohibition, and the upselling incompatibility warning.

**Exclusions.** Compensation, half-and-half pizzas, the ticket printer, multi-day advance orders, commercial automation, coffee, and multilingual administration are now recorded, each with a requirement that enforces it and machine-checkable forbidden terms.

## 6. Explicit exclusions

Recorded in `docs/current/requirements/DOPIS_EXCLUSIONS.json` with the canonical section supporting each one. The validator fails if a forbidden term appears in any requirement other than the one that states the exclusion.

Online payment including Apple Pay and Google Pay; customer accounts, loyalty, birthday benefits, and marketing campaigns; delivery and table reservations; coffee; customer self-service cancellation; gram-level recipe inventory; automatic substitution and automatic reactivation; discounts, dynamic pricing, automatic promotions, and inferred or random recommendations; compensation capabilities; half-and-half pizzas; the ticket printer; multilingual administration; multi-day advance orders; advanced analytics and product-margin reporting; advanced SEO; production hosting and public-domain readiness; an extensive permission hierarchy.

## 7. Epic map

Thirteen business capabilities: `EPIC-ORDERING`, `EPIC-KITCHEN-OPERATIONS`, `EPIC-CAPACITY`, `EPIC-STOCK`, `EPIC-CATALOG`, `EPIC-FOOD-SAFETY`, `EPIC-UPSELL`, `EPIC-COMMUNICATIONS`, `EPIC-PAYMENT-HANDOVER`, `EPIC-INCIDENTS`, `EPIC-ACCESS`, `EPIC-PRIVACY`, `EPIC-PILOT`.

Every requirement has exactly one primary epic that owns it. A supporting mapping records a deliberate cross-cutting concern and never duplicates the obligation. Version `0.2` had eleven epics, one of which would have grown to forty-nine requirements spanning catalog administration, food safety, and commercial upselling; those are now separate capabilities with distinct goals and distinct gate profiles.

The map implies no implementation order, estimate, delivery commitment, or authority.

## 8. Implementation-readiness boundary

`BASELINED` means the obligation is accepted for specification. It is not implementation authority.

Readiness additionally requires linked use cases and exception flows, measurable acceptance criteria, reviewed architecture decisions and contracts, resolved blocking gates, a dependency and test strategy, and an explicitly authorised bounded task packet.

Implementation authority remains `NOT GRANTED`.

## 9. Validation

```text
python scripts/validate_specification.py
python scripts/test_validate_specification.py
```

The validator derives every total from the artifacts, resolves every canonical section reference, gate reference, epic reference, and dependency, recomputes every orphan expectation, checks that no exclusion is contradicted, confirms this document agrees with the registry, and verifies that no artifact grants implementation authority. It records no stored pass result, because a stored result is a claim rather than evidence.
