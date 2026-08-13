# Dopis MVP Requirements Baseline

**Milestone:** `MILESTONE-SPEC-001`
**Status:** `AUDITED_PENDING_OWNER_APPROVAL`
**Baseline version:** `0.6`
**Date:** `2026-08-13`
**Business source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.19`
**Business discovery status:** `CLOSED_PENDING_VALIDATION_AND_IMPLEMENTATION_PLANNING`
**Implementation authority:** `NOT GRANTED`

<!-- Machine-checked agreement markers. scripts/validate_specification.py recomputes
     each value from the registries and fails if this document disagrees. -->

    REGISTRY-VERSION: 0.6
    REGISTRY-TOTAL: 216
    REGISTRY-EPICS: 13

## 1. Purpose and authority

This baseline translates the closed first-MVP business discovery into uniquely identified requirements. It does not authorise implementation, define the API or database, or resolve any unresolved stakeholder decision.

Canonical discovery has priority over this document. Version `0.6` consolidates the accepted VAL-007/008 Owner reconciliation: future enabled-date pickup orders, responsive staff operation, staff-mediated changes/cancellations, conditional in-person contact collection, operational POS/payment/cash-close/receipt scope, manual incident handling, calibrated capacity and delay, stock, bounded upselling, and the MVP scorecard. It replaces stale v0.5 contradictions rather than layering a delta over them.

Version `0.6` applies `docs/current/DOPIS_ACCEPTED_RECONCILIATION_DELTA_2026-08-13.md`, `docs/reviews/DOPIS_VAL_007_008_OWNER_RECONCILIATION_MAP.md`, and accepted VAL-007/008 evidence. Implementation authority remains `NOT_GRANTED`.

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

Every record carries: `id`, `statement`, `class`, `acceptance_state`, `readiness_milestone`, `status`, `priority`, `rationale`, `business_source`, `verification_method`, `validation_links`, `dependencies`, and `notes`. A record carries `block_justifications` if and only if it is `BLOCKED_BY_VALIDATION`, and `supersedes` only where it replaces another record's obligation.

**Classes:** `FR` behaviour, `BR` business rule or invariant, `DATA` data obligation, `SEC` security or access, `PRIV` privacy, `NFR` quality attribute, `AUDIT` audit or evidence, `PILOT` pilot governance, `OPS` operational constraint.

**Acceptance state** — is the obligation itself settled?

- `ACCEPTED`: confirmed by canonical discovery;
- `PROVISIONAL`: a canonical working direction whose wording or rule may still change;
- `CONDITIONAL`: exists only if a stakeholder decision promotes it.

**Readiness milestone** — by when must it hold? `PILOT`, `WITHOUT_JAIME`, or `PUBLIC_LAUNCH`.

**Status** — `BASELINED`, or `BLOCKED_BY_VALIDATION` if and only if at least one gate link has effect `BLOCK`. The validator enforces the equivalence in both directions.

Version `0.2` used a single `classification` field mixing four unrelated dimensions — acceptance state, milestone, decision ownership, and calibration. Splitting acceptance state from readiness milestone is what exposed the misclassified allergen requirements described in section 5.

**Gate effects:**

- `BLOCK`: the candidate obligation is recorded, but it cannot be accepted as final or made implementation-ready until the gate resolves;
- `CALIBRATE`: the obligation is accepted; a value or operating rule comes from evidence;
- `VALIDATE`: the obligation is accepted; wording, procedure, evidence, or confirmation is outstanding.

**Four distinct things, none of which implies the next.** *Recording a candidate requirement* means the obligation is written down and governed. *Accepting the obligation* means canonical discovery confirms Dopis will impose it. *Milestone readiness* means the conditions for entering `PILOT`, `WITHOUT_JAIME`, or `PUBLIC_LAUNCH` are met. *Implementation authority* means work may begin. A blocked record necessarily contains a candidate statement, so `BLOCK` never means the statement is missing; it means the statement may not be treated as accepted or built.

Because a gate being unresolved is not by itself a reason to block, every blocked record carries `block_justifications`: an ordered array with **exactly one justification for every gate the record links with effect `BLOCK`**. Each names which kind of unresolvedness applies to that gate, drawn from a closed vocabulary: `OBLIGATION_NOT_YET_ACCEPTED` (canonical discovery records a working direction, not an accepted rule), `SUBJECT_MATTER_NOT_YET_SELECTABLE` (the set or register the obligation refers to does not exist in any form), or `AUTHORISATION_NOT_YET_CONFERRED` (the record is a milestone entry condition). The vocabulary deliberately offers no code meaning that only wording, procedure, ownership, or evidence is outstanding, because that case is a `BASELINED` record with `VALIDATE` or `CALIBRATE`. The validator enforces this, and an `ACCEPTED` record may never claim its own obligation is undecided.

The justification set and the `BLOCK` link set must correspond **one to one**: every `BLOCK` gate is justified exactly once, no justification names a gate that is not so linked, and duplicates on either side are rejected. This is set equality rather than membership, because a membership test would let a further `BLOCK` link be attached to an already blocked record while an unrelated existing justification kept it valid. Unjustified over-blocking therefore has no representation.

An unresolved gate can still stop a whole milestone. That is expressed by the three milestone entry-condition records — `PILOT-004`, `OPS-DELEGATION-001`, and `BR-LAUNCH-001` — which correspond to the three canonical section 18A blocker lists, rather than by marking every dependent obligation blocked. Each blocks on one gate per canonical blocker it carries and justifies each separately, so no canonical blocker is dropped to simplify the record.

**Verification methods:** `TEST`, `SECURITY_TEST`, `INSPECTION`, `ANALYSIS`, `DEMONSTRATION`, `PILOT_EVIDENCE`, `BUSINESS_REVIEW`.

## 4. Validation gates

Fifteen gates come verbatim from the canonical validation register in discovery section 15, plus two closed gates retained for traceability. Three further gates are marked `DERIVED`: `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, and `JV-INCIDENT-FAIRNESS`. Each names a bounded question that canonical discovery leaves explicitly open without assigning it an identifier, and each carries a written derivation rationale. The validator refuses a derived gate that lacks one.

Version `0.2` referenced `JV-MANUAL-ORDERS` and `JV-PAYMENT` as if they were current gates. Both are absent from the section 15 validation register of canonical discovery version `0.18`. They survive only as historical entries in the section 19 change log, which records their introduction in discovery version `0.11`. They are therefore stale or retired identifiers — not fabricated, and not absent from the complete canonical document. Version `0.2` also omitted the two closed gates, so its total coincidentally matched the canonical count of seventeen and concealed the substitution from a count-based check. `docs/current/requirements/DOPIS_VALIDATION_GATES.json` records both as `RETIRED` together with the gate that now carries each concern, and the validator rejects any requirement that references a retired identifier.

## 5. Audit corrections in version `0.3`

**Food safety.** Version `0.2` covered gluten only with the rule not to claim coeliac suitability. Discovery section 10.3 additionally requires a general menu cross-contact warning, a specific warning on selection, explicit customer acknowledgement, a statement that online ordering cannot guarantee absence of cross-contact, independent disablement of the option, and disablement whenever the validated procedure cannot be followed. All are now specified, together with allergen warnings on substitution, dietary recalculation, and the rule that a free-text note may never override configured modifier, price, availability, or allergen rules.

**Milestone correction.** Allergen and catalog-publication requirements were labelled public-launch blockers. Discovery section 18A requires validated product-specific allergen data before the first real pilot order. They are now `PILOT`-milestone obligations. Conversely, `PRIV-DATA-001`, `PRIV-DATA-002`, and `PRIV-DATA-003` were blocked on a public-launch gate even though sections 11.4, 12.4, and 18A require minimum privacy controls from the first real order; they are now baselined pilot obligations, and `OPS-PILOT-001` makes that binding.

**Over-blocking.** Manual channel entry, the payment and handover model, stock counting, catalog administration, report access, and weekly reporting were marked blocked although canonical discovery accepts each obligation and leaves only procedure or calibration open. They are baselined with `VALIDATE` or `CALIBRATE` links.

**Omissions now specified.** The operational threshold register that every `JV-THRESHOLDS` link resolves through, the pending-Jaime decision record, substitution rules and the absorbed price-difference limit, the non-collection process, transactional capacity and stock commitment, the provisional checkout hold, tracking-SMS delivery failure routing, alternative-slot expiry, approximate critical-ingredient allowances, queue ordering by recommended preparation time, telephone-support disclosure limits, card-data storage prohibition, and the upselling incompatibility warning.

**Exclusions.** Compensation, half-and-half pizzas, commercial automation, coffee, and multilingual administration remain recorded. Advance orders and receipt/ticket printing are accepted MVP capabilities, not exclusions.

## 5A. Owner-review corrections in version `0.4`

**`BLOCK` semantics.** Version `0.3` defined `BLOCK` as "the obligation cannot be specified or implemented". A blocked record necessarily contains a candidate statement, so that wording was self-contradictory. Section 3 now states the corrected definition and keeps the four levels — recording, acceptance, milestone readiness, implementation authority — explicitly distinct.

**Gluten.** Canonical section 10.3 already imposes the six gluten interface obligations, including explicit confirmation that the customer has read and understood the cross-contact warning. Version `0.3` nevertheless recorded all of them as blocked, and `JV-GLUTEN` asked whether explicit acknowledgement was required at all. The gate no longer reopens the acknowledgement obligation; it now covers only the exact customer-facing wording, supplier documentation, actual kitchen procedure, severe-allergy handling, detailed disablement conditions, and approval authority. `BR-ALLERGEN-001`, `FR-GLUTEN-001` to `FR-GLUTEN-005`, and `OPS-GLUTEN-001` are baselined with `VALIDATE`. No gluten obligation is blocked. `PILOT-004` still blocks the pilot on `JV-GLUTEN`, so no pilot order can be accepted before the gate resolves.

**Telephone-number scope.** Version `0.3` stated that name and telephone number are mandatory for every order while simultaneously recording the in-person rule as open. `DATA-ORDER-001` is now scoped to web and telephone orders, where canonical section 2.1 accepts both fields. `BR-ORDER-013` keeps data minimisation binding on every channel regardless. `DATA-ORDER-003` records the in-person telephone requirement as a candidate obligation that is explicitly not accepted, because canonical section 7.4A leaves it pending Jaime's validation of operational burden and privacy necessity.

**Re-audited blocked records.** Every blocked record was tested against one question: is the obligation itself undecided, or is only a value, wording, procedure, owner, or evidence outstanding? Nineteen of the twenty-four failed that test and are now baselined with `VALIDATE` or `CALIBRATE`, including the whole gluten set, the substitution rules, the threshold register, the delegation data model, retention, and the pilot governance records. The blocked count was treated as an output, not a target.

**Milestone entry conditions.** Unblocking those records exposed a gap: canonical section 18A states three blocker lists, but only the pilot list was represented. `OPS-DELEGATION-001` and `BR-LAUNCH-001` now carry the operating-without-Jaime and public-launch conditions, alongside the existing `PILOT-004`.

**Incident fairness.** `FR-INCIDENT-002` bundled an accepted resolution obligation with the provisional two-incidents-in-90-days rule. It is split: the resolution obligation and the prohibition on automatic customer blocking (`BR-INCIDENT-003`) are accepted and baselined; the provisional repeat-incident rule (`BR-INCIDENT-002`) is recorded as a candidate and remains blocked.

**Totals.** 210 → 216 requirements, 0 removed. Blocked 24 → 5. Epics unchanged at 13. Gates unchanged at 20.

## 5B. Owner-review corrections in version `0.5`

**Complete `BLOCK`-link justification coverage.** Version `0.4` gave each blocked record a single `block_justification`, and the validator checked only that the gate it named was one of the record's `BLOCK` gates. That is a membership test, not coverage. A milestone entry-condition record blocks on several gates — `PILOT-004` on seven — so an arbitrary further `BLOCK` link could have been attached to an already blocked record while the single existing justification kept it valid. Unjustified over-blocking was therefore still representable.

The singular field is replaced by `block_justifications`, an ordered array carrying one justification per `BLOCK` link in the order of those links. The validator now compares the two sets for equality: every `BLOCK` gate justified exactly once, no justification for a gate that is not `BLOCK`-linked, duplicates rejected on either side, each `canonical_open_question` matched verbatim against its own gate, and the existing acceptance-state and prohibition-statement rules applied per justification. The five blocked records now carry fourteen justifications between them. No canonical milestone blocker was removed to simplify them.

**Totals.** Requirements, epics, gates, and blocked records are unchanged. The version moves to `0.5` because the requirement metadata contract changed.

## 6. Explicit exclusions

Recorded in `docs/current/requirements/DOPIS_EXCLUSIONS.json` with the canonical section supporting each one. The validator fails if a forbidden term appears in any requirement other than the one that states the exclusion.

Online payment including Apple Pay and Google Pay; customer accounts, loyalty, birthday benefits, and marketing campaigns; delivery and table reservations; coffee; general customer self-service cancellation; gram-level recipe inventory; automatic substitution and automatic reactivation; discounts, dynamic pricing, automatic promotions, and inferred or random recommendations; compensation capabilities; half-and-half pizzas; multilingual administration; advanced analytics and product-margin reporting; advanced SEO; production hosting and public-domain readiness; an extensive permission hierarchy.

## 7. Epic map

Thirteen business capabilities: `EPIC-ORDERING`, `EPIC-KITCHEN-OPERATIONS`, `EPIC-CAPACITY`, `EPIC-STOCK`, `EPIC-CATALOG`, `EPIC-FOOD-SAFETY`, `EPIC-UPSELL`, `EPIC-COMMUNICATIONS`, `EPIC-PAYMENT-HANDOVER`, `EPIC-INCIDENTS`, `EPIC-ACCESS`, `EPIC-PRIVACY`, `EPIC-PILOT`.

Every requirement has exactly one primary epic that owns it. A supporting mapping records a deliberate cross-cutting concern and never duplicates the obligation. Version `0.2` had eleven epics, one of which would have grown to forty-nine requirements spanning catalog administration, food safety, and commercial upselling; those are now separate capabilities with distinct goals and distinct gate profiles.

The map implies no implementation order, estimate, delivery commitment, or authority.

## 8. Implementation-readiness boundary

`BASELINED` means the obligation is accepted for specification. It is not implementation authority, and it is not milestone readiness. Section 3 states why those four levels are distinct: a baselined obligation whose milestone entry condition is still blocked may not be exercised, and no obligation at all may be built until authority is granted.

Readiness additionally requires linked use cases and exception flows, measurable acceptance criteria, reviewed architecture decisions and contracts, resolved blocking gates, a dependency and test strategy, and an explicitly authorised bounded task packet.

Implementation authority remains `NOT GRANTED`.

## 9. Validation

```text
python scripts/validate_specification.py
python scripts/test_validate_specification.py
```

The validator derives every total from the artifacts, resolves every canonical section reference, gate reference, epic reference, and dependency, recomputes every orphan expectation, checks that no exclusion is contradicted, confirms this document agrees with the registry, and verifies that no artifact grants implementation authority. It records no stored pass result, because a stored result is a claim rather than evidence.
