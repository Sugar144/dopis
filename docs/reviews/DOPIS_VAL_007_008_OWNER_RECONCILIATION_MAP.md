# DOPIS-VAL-007/008 — Owner Reconciliation Map

**Status:** `EXECUTION_MAP_FOR_ACCEPTED_DELTA`
**Accepted delta:** `docs/current/DOPIS_ACCEPTED_RECONCILIATION_DELTA_2026-08-13.md`
**Base requirements:** v0.5
**Implementation authority:** `NOT_GRANTED`

This map identifies the minimum derived-baseline transformations required to consolidate the accepted 2026-08-13 Owner delta. It is not a second source of business truth; the accepted delta controls.

## 1. Requirements that must be replaced or materially revised

| Existing record | Required reconciliation |
|---|---|
| `BR-ORDER-010` | Replace same-day-only admission with bounded future enabled service dates/windows. Exact horizon remains configurable. |
| `FR-KITCHEN-004` | Remove the concept of a separate limited mobile backup. Fold into one responsive authenticated staff web application usable from any suitable browser device. |
| `SEC-KITCHEN-001` | Remove device-class restrictions tied specifically to mobile backup. Authority follows authenticated staff capability, not device type. |
| `DATA-ORDER-003` | Resolve the universal in-person telephone requirement: telephone/contact is not mandatory when the customer waits on premises; require a contact route only when operationally necessary, such as leaving and returning later. |
| `BR-PAYMENT-002` | Close the unpaid-handover question: successful payment is required before handover; no invited/unpaid-order exception in MVP1. |
| `BR-INCIDENT-002` | Remove the provisional automatic two-incidents-in-90-days rule as an implementation obligation. MVP1 may visibly flag relevant incidents for manual staff handling; it must not require online prepayment or automatic refusal. |
| `FR-RECEIPT-001` | Add a functional receipt/ticket capability distinct from the former `BR-SCOPE-004` exclusion. The digital operational panel remains source of operational truth. |
| `OPS-KITCHEN-003` | Update rationale so fallback does not depend on the previous printer exclusion. |
| `PRIV-DATA-002` | Replace references to separate tablet/mobile-backup surfaces with the responsive staff operational application. |
| `SEC-TRACKING-002` | Retain narrow tracking actions and explicitly defer general customer order editing/cancellation. |
| `FR-ORDER-005` | Retain staff cancellation and incorporate accepted authority that either current team member may perform it, subject to audit/history. |
| `FR-COMMS-003` / delay rules | Calibrate the first serious-delay customer-notification reference to approximately 10 minutes while keeping the value configurable. |
| `FR-CAPACITY-002` / capacity calibration | Preserve configurable capacity admission; incorporate the initial operational reference of approximately 8–10 pizzas per 30 minutes and manual temporary increase with auditability. Do not silently discard or overcommit to the existing production-point mechanism; final capacity mechanics belong to architecture/calibration. |
| `AUDIT-PAYMENT-002` / `OPS-SHIFT-001` | Retain cash reconciliation and allow either current team member to close the shift, recording who performed the close. |
| `FR-UPSELL-*` / `BR-UPSELL-*` | Keep simple configured upselling and bias initial content toward relevant supplements/extras rather than inferred recommendation logic. |

## 2. New or newly explicit MVP obligations

The consolidated requirements should introduce independently verifiable obligations for:

1. **Future pickup ordering** — customers can order while the premises are closed, but only for enabled future service dates/windows inside a configurable horizon.
2. **Upcoming-order operation** — future orders are visible to staff and enter normal preparation flow for their service date.
3. **Staff-mediated order modification** — staff can modify an existing order after a customer phones, with revalidation of price, modifiers, allergens, stock, capacity, pickup feasibility, and preparation state.
4. **Responsive staff operation** — the same protected staff application works across kitchen tablet, counter tablet, mobile, and laptop-sized devices without changing business authority by device.
5. **Operational POS ownership** — Dopis owns sale total, payment state/method, payment correction history, cash reconciliation, and receipt lifecycle for Dopis orders.
6. **Cash collection** — Dopis records cash payment and supports collected-amount/change calculation before confirmation.
7. **Card-terminal handoff** — Dopis supports a provider-neutral card-terminal boundary for Ingenico APOS A8 / CaixaBank / Comercia Global Payments; automatic amount/result integration is conditional on Comercia provisioning, with manual-final-amount fallback permitted for MVP1.
8. **Receipt issuance** — Dopis can issue/print the customer receipt/ticket through a printer adapter; current-printer reuse is conditional on hardware verification.
9. **Problem-customer flagging** — relevant payment/non-collection incidents can be surfaced to staff for manual in-person handling without automatic online prepayment or automatic customer refusal.
10. **Operational measurement event capture** — capture the minimum domain events needed to derive the accepted pilot scorecard rather than creating separate mandatory analytics for every candidate metric.

## 3. Exclusion changes

### Remove / supersede

- `EXC-ADVANCE-ORDERS`
- `EXC-PRINTER`

### Retain

- online card payment, Apple Pay, and Google Pay;
- customer accounts / loyalty / marketing;
- delivery and table reservations;
- coffee;
- customer general self-service editing/cancellation;
- gram-level recipe inventory and inventory forecasting;
- compensation automation;
- half-and-half pizzas;
- multilingual administration;
- advanced analytics / product-margin reporting;
- dynamic pricing, automatic promotions, inferred/random recommendations;
- extensive permission hierarchy.

## 4. Validation-gate reconciliation

### `JV-ACCESS`

Close the mobile-backup semantic question. Remaining access work is bounded to authentication/session/onboarding/revocation and honest attribution mechanics.

### `JV-MANUAL-CHANNELS`

Promote the VAL-007 rules: telephone orders are handled by whichever authorised worker is available; an in-person telephone/contact route is required only when operationally necessary.

### `JV-PAYMENT-PROCEDURE`

Close the invited/unpaid-order question: no handover without payment. Preserve receipt/cash-close procedural validation and treat APOS A8/printer compatibility as technical evidence rather than reopening business scope.

### `JV-INCIDENT-FAIRNESS`

Do not implement the two-incidents-in-90-days automatic rule. Retain manual incident visibility/flagging and privacy/fairness review as applicable. No online prepayment in MVP1.

### `JV-CAPACITY`

Record approximately 8–10 pizzas per 30 minutes as the first real operational reference. Final admission mechanics, production weighting, and override threshold remain calibratable.

### `JV-DELAYS`

Record approximately 10 minutes as the initial serious-delay notification reference. Keep the value configurable and preserve remaining delay-flow validation where not answered.

### `JV-STOCK`

Record that drinks, desserts, and available pizzas/products are counted. Exact timing, ownership, carry-over, and low-stock thresholds remain calibration/evidence.

### `JV-GLUTEN` / `JV-ALLERGENS`

Preserve Jaime's real operating statement that severe cross-contact cases such as nuts and the gluten-free-dough option cannot be guaranteed in the current kitchen. Exact safe wording, supplier evidence, allergen matrix, and validated operating procedure remain required before the applicable real-order milestone.

### `JV-PILOT`

Do not reopen product discovery. Exact date, participant group, readiness evidence, baseline observer ownership, and progression thresholds remain pilot-planning/calibration work.

### `JV-COMPLIANCE`

Extend the existing compliance review to the now-in-scope receipt/fiscal-record lifecycle. Do not invent the implementation mechanism in requirements.

## 5. Technical evidence gates outside business scope

These do not require another Jaime decision unless the discovered hardware capability forces a material product trade-off:

- `COMERCIA_APOS_A8_COMPATIBILITY`: Ingenico APOS A8 ECR/POS integration capability after Comercia merchant provisioning;
- `RECEIPT_PRINTER_COMPATIBILITY`: Epson TM-m30III compatibility/control and real-device printing over the observed local-network TCP transport.

If automatic APOS A8 integration is unavailable, the accepted MVP fallback is manual entry of only the final amount into APOS A8 plus payment-result confirmation in Dopis.

If the existing printer is incompatible, replacing it with a compatible receipt printer does not change product scope.

## 6. Metrics reconciliation

Retain the existing four-week scorecard and pre-pilot baseline. Do not promote the entire candidate-metrics list into independent MVP obligations.

Minimum required measurement coverage:

- channel volume and share;
- order-creation and order-modification calls by time band;
- weekly web adoption / telephone-to-web movement;
- lost or materially late accepted orders;
- on-time percentage, delayed count, average delay;
- incidents/manual interventions/material corrections;
- channel-specific average order value;
- best sellers and frequent combinations;
- payment method, failures/corrections, expected-vs-actual cash;
- opening/closing workload;
- aggregate upselling impressions/additions/errors;
- Jaime qualitative assessment.

Prefer derivation from operational domain events and timestamps already required by the product.

## 7. Completion gate for baseline consolidation

A regenerated baseline is complete only when:

- the canonical discovery contains no conflicting same-day/mobile-backup/printer-exclusion wording;
- the requirements registry contains no active requirement enforcing superseded scope;
- exclusions agree with the accepted delta;
- validation gates distinguish resolved business questions from remaining calibration/evidence;
- epic/traceability ownership covers POS/receipt capability without orphan requirements;
- `python scripts/validate_specification.py` passes;
- `python scripts/test_validate_specification.py` passes;
- implementation authority remains unchanged unless separately granted by the Owner.
