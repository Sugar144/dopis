# Dopis Accepted Reconciliation Delta — 2026-08-13

**Status:** `ACCEPTED_OWNER_DELTA_PENDING_CONSOLIDATION`
**Applies to:** first operational MVP
**Base canonical discovery:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md` v0.18
**Base derived requirements:** v0.5
**Owner decision date:** 2026-08-13
**Implementation authority:** `NOT_GRANTED`

## 1. Authority and precedence

This artifact records accepted post-v0.18 business decisions derived from DOPIS-VAL-007, DOPIS-VAL-008, and explicit Project Owner dispositions.

Until the canonical discovery and derived requirement registries are regenerated, this delta takes precedence over conflicting statements in v0.18 and requirements baseline v0.5. Unaffected v0.18 obligations remain in force.

This delta does not grant implementation authority. The derived requirements baseline remains stale wherever it conflicts with this artifact and must not be used as implementation-ready truth until consolidation and validation are complete.

## 2. Evidence

Primary stakeholder evidence:

- `docs/evidence/dopis-val-007/DOPIS-VAL-007.validation-cycle.json`
- `docs/evidence/dopis-val-007/DOPIS-RESP-20260729T081215Z-2daf2c56.validation-response.json`
- `docs/reviews/DOPIS_VAL_007_R1_RECONCILIATION.md`
- `docs/evidence/dopis-val-008/DOPIS-RESP-20260813T115934Z-7fa96c61.validation-response.json`

DOPIS-VAL-008 response identity:

- response: `DOPIS-RESP-20260813T115934Z-7fa96c61`
- cycle: `DOPIS-VAL-008` v1
- stakeholder: Jaime
- status: `SUBMITTED`
- answered: `28/28`
- needs discussion: `0`

## 3. Accepted first-MVP scope changes

### 3.1 Advance ordering is in scope

Supersede the v0.18 / v0.5 same-day-only rule and `EXC-ADVANCE-ORDERS`.

The first MVP shall allow customers to place pickup orders for future enabled service dates within a configurable bounded horizon.

Rules:

- customers may place an order while the premises are currently closed;
- pickup may be selected only on enabled service dates and enabled pickup windows;
- a normally closed or holiday date remains unavailable for pickup unless staff explicitly configure an exceptional opening;
- a customer may order on a holiday or closed day for a later enabled service date;
- future pickup windows have capacity limits;
- upcoming future orders remain visible to staff and enter the normal operational flow for their service date;
- the horizon is configurable; its exact number of days remains an operational parameter;
- the MVP does not reserve future ingredient stock automatically;
- the MVP does not add inventory forecasting, recurring orders, or advanced planning;
- future-order reminders may be supported without introducing online prepayment.

### 3.2 One responsive staff web application

Supersede the separate limited-mobile-backup concept.

Dopis shall expose one authenticated responsive staff web application that can be used from the kitchen tablet, counter tablet, mobile phone, laptop, or other suitable browser device.

The two current staff members operate with the same first-MVP operational capability set. The MVP does not require an extensive permission hierarchy.

Device type shall not determine business authority. Sensitive actions that require attribution, including shift close and material corrections, must retain sufficient actor/session evidence.

### 3.3 Customer changes and cancellations remain staff-mediated in MVP1

General customer self-service order editing is deferred.

For the first MVP:

- a customer requests changes or cancellation by telephone;
- authorised staff apply the change or cancellation in Dopis;
- changes must revalidate price, modifiers, allergen consequences, stock, capacity, pickup feasibility, and preparation state as applicable;
- any customer-facing tracking link remains limited to the explicitly accepted narrow tracking actions and does not become a general order editor;
- future self-service editing should remain architecturally possible without redesigning the order domain.

### 3.4 No online prepayment in MVP1

Online payment remains deferred.

A customer with relevant non-collection or payment incidents may be visibly flagged for staff handling. Any stricter payment handling is performed in person by staff; the MVP does not require an online prepayment flow or payment-account integration for that purpose.

No order is handed over without successful payment.

## 4. Point of sale, payment, and receipt scope

The first MVP now includes Dopis as the operational point-of-sale system for its own orders.

Dopis owns:

- the sale/order total;
- recorded payment method;
- payment status and timestamps;
- operator/session attribution;
- payment corrections and reversals with audit history;
- cash expected-versus-actual close data;
- receipt/ticket issuance lifecycle.

Accepted in-person payment methods are:

- `CASH`;
- `CARD` through the existing Ingenico APOS A8 terminal supplied by CaixaBank / Comercia Global Payments.

Customers do not choose the payment method during web ordering. Staff record the method actually collected.

For cash payment, Dopis records the collected amount and may calculate change before payment confirmation.

For card payment, the preferred target is automatic amount/result integration between Dopis and the Ingenico APOS A8 terminal. Until terminal capability and Comercia provisioning are verified, the compatible MVP fallback is: Dopis calculates the final amount, staff enter only that amount in APOS A8, and staff confirm the observed payment result in Dopis.

The previous first-MVP exclusion of a ticket printer is superseded. Dopis should issue the customer receipt/ticket through a compatible printer. Direct reuse of the existing printer is preferred but is subject to hardware verification; replacement with a compatible printer is allowed without changing the business/domain model.

Dopis must not store card data. Provider-specific integration belongs behind a payment-terminal adapter and printer-specific integration behind a receipt-printer adapter.

## 5. DOPIS-VAL-008 operational decisions accepted

The following stakeholder evidence is accepted as first-MVP direction, subject only to ordinary calibration or implementation design where stated:

- reference kitchen capacity: approximately 8–10 pizzas per 30-minute window;
- authorised staff may temporarily increase capacity when actual kitchen conditions permit, with explicit traceability;
- a customer-facing serious-delay notification threshold starts at approximately 10 minutes and remains configurable;
- staff must be able to introduce a temporary delay / pause new admissions when kitchen conditions require recovery;
- any current team member may cancel an accepted order, with the cancellation preserved in the operational history;
- stock operation includes counts of available drinks, desserts, and pizzas/products; exact count timing and low-stock thresholds remain operational calibration;
- either current team member may perform shift close, and the system records who performed it;
- for severe allergy/cross-contact cases such as nuts and the gluten-free-dough option, the business does not claim guarantees that its kitchen cannot provide; exact compliant wording and validated procedure remain controlled food-safety evidence;
- pizza configuration supports ingredient removals and configured paid extras; product-specific substitution details and price deltas remain governed catalog data;
- upselling should favour simple relevant supplements/extras rather than sophisticated inferred recommendations.

## 6. DOPIS-VAL-007 deltas promoted

The Owner accepts the previously identified resolved deltas from `DOPIS_VAL_007_R1_RECONCILIATION.md`:

- accepted-order problems must support customer notification and operational resolution;
- a previous uncollected order may be associated with the operational contact only within validated privacy/retention rules;
- in-person orders do not always require a telephone number: a contact route is required when operationally necessary, such as when the customer leaves and returns later;
- telephone orders are handled by whichever authorised worker is available rather than by a permanently assigned operator;
- a shared operational session may be used where appropriate without pretending that each touch uniquely re-authenticates an individual, while material actions still preserve honest attribution.

## 7. Measurement contract retained for MVP1

The existing MVP outcome remains reduction of order-related telephone calls during peak service.

Mandatory scorecard scope is retained:

- order volume by `WEB`, `PHONE`, and `IN_PERSON`;
- percentage distribution by channel;
- calls used to create orders and calls used to modify orders, by time band;
- weekly web-order volume and estimated movement from telephone to web;
- accepted-order loss / materially late kitchen reception;
- delayed-order count, on-time percentage, and average delay;
- incidents, manual interventions, and material corrections;
- channel-specific average order value;
- best-selling products and frequent product combinations;
- payment method, payment failures/corrections, and expected-versus-actual cash difference;
- opening/closing workload and Jaime's qualitative assessment;
- aggregate upselling impressions, additions, and relevant operational errors where upselling is enabled.

Implementation should capture the minimum reliable domain events required to derive this scorecard. Candidate analytics outside this set are not independently mandatory merely because they are derivable.

No numeric call-reduction or upselling-conversion target is invented before real baseline/pilot evidence exists.

## 8. Open gates that do not reopen product scope

These are bounded technical, compliance, evidence, or calibration gates. They do not require another broad business-discovery round.

### Hardware / integration

- Ingenico APOS A8 ECR / POS-controlled amount and result integration capability, subject to Comercia merchant provisioning;
- exact existing receipt-printer model and supported connection/control interface.

### Fiscal / compliance

- exact receipt/fiscal-record obligations applicable to Dopis and the implementation path required for compliant invoicing/receipt issuance;
- privacy retention periods and remaining public-launch compliance procedure.

### Operational calibration

- exact maximum advance-order horizon;
- final capacity calibration and manual-review thresholds;
- exact stock-count timing and low-stock values;
- complete product-specific modifier/substitution/extra price matrix;
- final pilot timing, participants, readiness evidence, and measurement ownership.

These values should be represented as configuration/policy where appropriate rather than hard-coded architecture.

## 9. Explicitly deferred after this reconciliation

The following remain outside MVP1 unless a later controlled change promotes them:

- online payment / online prepayment;
- Apple Pay / Google Pay;
- general customer self-service order editing or cancellation;
- customer accounts and loyalty;
- delivery and table reservations;
- gram-level recipe inventory and inventory forecasting;
- recurring orders or advanced planning;
- advanced analytics and product-margin reporting;
- dynamic pricing, automatic promotions, or inferred recommendation systems;
- extensive staff permission hierarchy.

## 10. Consolidation requirement

Before implementation authority can be granted, regenerate and validate the affected canonical/derived surfaces so they agree with this accepted delta, including at minimum:

- `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`;
- `docs/current/DOPIS_MVP_REQUIREMENTS.md`;
- `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json`;
- `docs/current/requirements/DOPIS_VALIDATION_GATES.json` where gate state/questions changed;
- `docs/current/requirements/DOPIS_EXCLUSIONS.json`;
- `docs/backlog/DOPIS_EPICS.json` if capability ownership changes;
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`.

Run:

`python scripts/validate_specification.py`

`python scripts/test_validate_specification.py`

The consolidation must remove stale contradictions rather than layering implementation assumptions over v0.5.
