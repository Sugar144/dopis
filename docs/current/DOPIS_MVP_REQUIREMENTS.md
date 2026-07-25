# Dopis MVP Requirements Baseline

**Milestone:** `MILESTONE-SPEC-001`  
**Status:** DRAFT_FOR_REVIEW  
**Baseline version:** `0.1`  
**Date:** 2026-07-25  
**Business source:** `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, version `0.18`  
**Business discovery status:** `CLOSED_PENDING_VALIDATION_AND_IMPLEMENTATION_PLANNING`  
**Implementation authority:** `NOT GRANTED`

## 1. Purpose and authority

This document translates the closed first-MVP business discovery into uniquely identified and verifiable requirements. It does not authorise implementation, define the database or API, or supersede unresolved Jaime validation gates.

Where this document conflicts with the canonical discovery, the conflict must be reported and reconciled rather than resolved silently.

## 2. Requirement contract

Requirement identifiers use `<CLASS>-<DOMAIN>-<SEQUENCE>`.

Classes:

- `FR-*`: functional behaviour;
- `BR-*`: accepted business rule or invariant;
- `DATA-*`: data obligation;
- `SEC-*`: security and access;
- `PRIV-*`: privacy;
- `NFR-*`: quality attribute;
- `AUDIT-*`: audit, correction, and evidence;
- `PILOT-*`: pilot governance;
- `OPS-*`: operational constraint.

Statuses:

- `BASELINED`: accepted for specification, not authorised for implementation;
- `BLOCKED_BY_VALIDATION`: accepted obligation whose readiness or verification depends on one or more `JV-*` gates;
- `SUPERSEDED` and `RETIRED`: historical lifecycle states.

Priorities:

- `MUST_MVP`;
- `SHOULD_MVP`;
- `COULD_MVP`;
- `DEFERRED`.

Verification methods:

- `TEST`;
- `SECURITY_TEST`;
- `INSPECTION`;
- `ANALYSIS`;
- `DEMONSTRATION`;
- `PILOT_EVIDENCE`;
- `BUSINESS_REVIEW`.

Each requirement is governed by the following logical record:

```yaml
id:
title:
statement:
type:
domain:
classification:
status:
priority:
business_source:
rationale:
verification_method:
related_validation_gates: []
dependencies: []
notes:
```

## 3. Ordering and pickup

### FR-ORDER-001 — Browse current menu

The system shall allow a customer to browse the currently published menu without creating an account.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: canonical sections 2.1 and 3.1.

### FR-ORDER-002 — Guest pickup order

The system shall allow a customer to submit a pickup order without creating an account.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 2.1 and 3.1.

### DATA-ORDER-001 — Minimum guest identity

The system shall collect the customer's name and telephone number for a web or telephone order and shall not require account registration.

- Type: `DATA`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 2.1, 3.1, and 11.1.
- Gates: `JV-PRIVACY`.

### BR-ORDER-001 — Pickup only

The first operational MVP shall accept pickup orders only.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 2.1 and 3.1.

### FR-ORDER-003 — Pickup choice

The system shall offer the earliest feasible pickup opportunity and feasible scheduled pickup opportunities calculated from the final basket and current operational constraints.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7 and 10A.
- Gates: `JV-CAPACITY`, `JV-THRESHOLDS`.

### BR-ORDER-002 — Atomic final revalidation

An order shall become confirmed only after final revalidation of ordering mode, service hours, pickup capacity, publication, availability, and applicable stock.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.1 and 10A.
- Gates: `JV-CAPACITY`, `JV-STOCK`.

### FR-ORDER-004 — Manual-review outcomes

In manual-review mode, authorised staff shall be able to accept the requested pickup time, reject the order, or propose a feasible alternative pickup time.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 7.2.
- Gate: `JV-DELAYS`.

### FR-ORDER-005 — Staff cancellation

Authorised staff shall be able to cancel an order and record the applicable reason.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.3 and 10A.

### BR-ORDER-003 — No customer self-cancellation

The first operational MVP shall not provide general customer self-service order cancellation.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 2.2 and 7.3.

### BR-ORDER-004 — Accepted commitment stability

Later catalog deactivation, price changes, or capacity reductions shall not rewrite or displace an accepted order.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.4A and 18A.

### FR-ORDER-006 — Unfulfillable accepted order

The system shall route an accepted order that can no longer be fulfilled as confirmed to an operational attention state without silently changing or cancelling it.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.4A and 18A.

## 4. Kitchen operations

### FR-KITCHEN-001 — Protected kitchen queue

The system shall provide authenticated staff access to an operational kitchen queue and shall prevent public access to that queue.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 3.1 and 8.

### FR-KITCHEN-002 — Operational order states

Authorised staff shall be able to progress orders through the approved operational lifecycle while preventing duplicate or invalid transitions.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7 and 8.

### FR-KITCHEN-003 — Order acknowledgement

A newly received order shall remain visibly highlighted and shall require explicit acknowledgement by staff.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 8.
- Gate: `JV-PILOT`.

### NFR-KITCHEN-001 — Audible and visible alert

The kitchen panel shall provide an audible alert and persistent visible indication for a newly received order under the validated kitchen operating conditions.

- Type: `NFR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `DEMONSTRATION`.
- Source: section 8.
- Gates: `JV-PILOT`, `JV-THRESHOLDS`.

### NFR-KITCHEN-002 — Connection awareness

The kitchen panel shall display connection status, identify stale data, and prevent state-changing actions while disconnected.

- Type: `NFR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 8.

### OPS-KITCHEN-001 — Automatic-acceptance safety pause

The system shall pause automatic acceptance after the validated unattended-alert or disconnection condition and shall require explicit staff review before resuming.

- Type: `OPS`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 8.
- Gates: `JV-PILOT`, `JV-THRESHOLDS`.

### FR-KITCHEN-004 — Limited mobile backup

The system shall provide a bounded mobile backup for order operations, status changes, and urgent availability changes without exposing sensitive administration.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 8 and 11.3.
- Gate: `JV-ACCESS`.

## 5. Capacity and service scheduling

### BR-CAPACITY-001 — Shared capacity

Web, telephone, and in-person orders shall consume the same kitchen capacity and pickup-window commitments.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.4A, 9.3, and 18A.

### FR-CAPACITY-001 — Weighted production load

The system shall calculate order production load using configurable integer production points for products and eligible modifiers.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.3.
- Gate: `JV-CAPACITY`.

### FR-CAPACITY-002 — Capacity windows

The system shall evaluate order admission against configurable pickup-window capacity, weekday templates, and date-specific exceptions.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 9.3 and 13.4.
- Gate: `JV-CAPACITY`.

### BR-CAPACITY-002 — Large-order review

An order above the validated large-order threshold or unable to fit safely within one pickup window shall enter manual review.

- Type: `BR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.3.
- Gates: `JV-CAPACITY`, `JV-THRESHOLDS`.

### AUDIT-CAPACITY-001 — Exceptional override evidence

A responsible operator's exceptional capacity override shall record the actor, time, affected order, and acknowledged operational risk.

- Type: `AUDIT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.4A and 9.3.
- Gate: `JV-SHIFT-AUTHORITY`.

### OPS-HOURS-001 — Separate service schedules

The system shall configure premises hours, pizza-ordering hours, earliest pickup, latest pickup, lead time, day-specific schedules, and date-specific exceptions as distinct operational concepts.

- Type: `OPS`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 13.4.

## 6. Stock and availability

### FR-STOCK-001 — Shared stock

Web, telephone, and in-person orders shall reserve and consume from the same applicable stock records.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.2B.

### FR-STOCK-002 — Countable stock ceiling

The system shall support an opening count for directly countable products and shall treat the recorded quantity as the online-sales ceiling.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.2.
- Gate: `JV-STOCK`.

### BR-STOCK-001 — Reserve, commit, and release

Applicable stock shall be reserved during checkout or manual review, committed on confirmation, and released on expiry, abandonment, or eligible pre-preparation cancellation.

- Type: `BR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.2.
- Gates: `JV-STOCK`, `JV-THRESHOLDS`.

### FR-STOCK-003 — Stock adjustment

Authorised staff shall be able to record replenishment and stock corrections with an operator, timestamp, and configured reason.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 9.2.
- Gate: `JV-STOCK`.

### FR-STOCK-004 — Availability control

Authorised staff shall be able to disable a product, critical ingredient, or option immediately, while reactivation shall require Jaime or the responsible shift lead.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 9.1 and 10.1.

### BR-STOCK-002 — No automatic substitution or reactivation

The system shall not substitute unavailable items automatically and shall not reactivate sales solely from an estimated replenishment time.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 9.1 and 9.4.

## 7. Catalog, modifiers, allergens, and upselling

### FR-CATALOG-001 — Protected catalog administration

The system shall allow Jaime or an authorised responsible person to create, edit, deactivate, reorder, reprice, feature, schedule, and publish eligible catalog products.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 10.1.
- Gates: `JV-CATALOG-APPROVAL`, `JV-CONTENT`.

### FR-CATALOG-002 — Configured modifiers

The system shall support product-specific allowed removals, substitutions, and paid extras through configured modifier rules rather than unrestricted ingredient free text.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 10.2.
- Gate: `JV-MODIFIERS`.

### BR-CATALOG-001 — Publication gate

A product shall not participate in real orders until required bilingual content, price, ingredients, allergens, traces, availability, and applicable dietary labels are complete and approved.

- Type: `BR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 10.1A and 18A.
- Gates: `JV-ALLERGENS`, `JV-CATALOG-APPROVAL`, `JV-CONTENT`.

### DATA-CATALOG-001 — Bilingual public content

The public catalog shall support reviewed Spanish and Catalan names and required descriptions, with Spanish fallback and a visible language selector.

- Type: `DATA`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: section 10.1B.
- Gate: `JV-CONTENT`.

### BR-CATALOG-002 — Historical order snapshot

Catalog changes or deactivation shall not corrupt the commercial description and confirmed price of historical or accepted orders.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 10.1 and 7.4A.

### DATA-ALLERGEN-001 — Product-specific safety data

The catalog shall retain ingredients, regulated allergens, known traces, dietary labels, and applicable cross-contact notices for each sellable configuration.

- Type: `DATA`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: section 10.3.
- Gates: `JV-ALLERGENS`, `JV-GLUTEN`.

### FR-ALLERGEN-001 — Final-configuration disclosure

The customer interface shall show allergens for the selected final configuration and repeat them in the order summary before confirmation.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 10.3.
- Gate: `JV-ALLERGENS`.

### BR-ALLERGEN-001 — Gluten-free wording boundary

The system shall present the option as a gluten-free dough option and shall not claim suitability for coeliac customers or severe allergies unless separately validated.

- Type: `BR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: section 10.3.
- Gate: `JV-GLUTEN`.

### OPS-ALLERGEN-001 — Incorrect-information containment

When published allergen information is found incorrect, the system shall disable affected new sales, identify accepted undelivered affected orders, route them to review, and preserve the incident and correction trail.

- Type: `OPS`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 10.3 and 18A.

### FR-UPSELL-001 — Configured recommendations

The system shall present only manually configured, active, available, published, allergen-complete, and dietary-compatible recommendations for drinks, desserts, or eligible extras.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 12.7.
- Gate: `JV-CATALOG-APPROVAL`.

### BR-UPSELL-001 — Bounded optional upselling

Upselling shall be optional, shall not block checkout, shall show no more than three recommendations overall, and shall never add or increase quantities automatically.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 7.1A and 12.7.

### AUDIT-UPSELL-001 — Aggregate upsell evidence

The system shall record aggregate recommendation impressions and additions by placement without creating persistent individual customer recommendation profiles.

- Type: `AUDIT`; status: `BASELINED`; priority: `SHOULD_MVP`; verification: `ANALYSIS`.
- Source: section 12.7.

## 8. Customer communications and tracking

### FR-COMMS-001 — Tracking-access SMS

After order submission, the system shall send an SMS providing secure access to private order tracking.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 10B.

### FR-COMMS-002 — Outcome notifications

The system shall send an SMS when an order is ready, rejected, or cancelled by staff and shall not send a redundant acceptance SMS.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 10B.

### SEC-TRACKING-001 — Protected guest tracking

Private order tracking shall require an opaque, time-limited access mechanism or protected browser session; a sequential public order code alone shall not authorise access.

- Type: `SEC`; status: `BASELINED`; priority: `MUST_MVP`; verification: `SECURITY_TEST`.
- Source: section 10B.

### PRIV-COMMS-001 — SMS minimisation

SMS content shall be limited to Dopis identification, general order status, and the private tracking link rather than complete order details.

- Type: `PRIV`; status: `BASELINED`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 10B and 11.6.

## 9. Payment, handover, and shift close

### BR-PAYMENT-001 — Pay at premises

The first operational MVP shall use payment at the premises and shall not include online payment.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 2.2 and 6.6.

### FR-PAYMENT-001 — Record actual method

Staff shall record the payment method actually used at collection as cash or card.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.6 and 7.5.
- Gate: `JV-PAYMENT`.

### BR-PAYMENT-002 — Payment before handover

Payment and handover shall be separate events, and an order shall not be handed over unless an accepted payment method succeeds.

- Type: `BR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.6 and 7.5.
- Gate: `JV-PAYMENT`.

### AUDIT-PAYMENT-001 — Payment and handover corrections

Corrections to payment method, paid state, or handover state shall preserve the previous event, actor, time, and required reason.

- Type: `AUDIT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.6 and 7.5.
- Gate: `JV-PAYMENT`.

## 10. Incidents, exceptions, and recovery

### FR-INCIDENT-001 — Requires-attention queue

The system shall provide a visible operational queue for orders, failures, or customer responses requiring staff attention.

- Type: `FR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 7.6.

### AUDIT-INCIDENT-001 — Append-only incident history

Material operational incidents, corrections, reopenings, and safe interim measures shall remain traceable without deleting prior history.

- Type: `AUDIT`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.16 and 7.9.

### OPS-INCIDENT-001 — Safe isolation

When a problem exceeds authorised rules, staff shall be able to pause only the affected product, option, channel, or capability when unaffected operation remains safe.

- Type: `OPS`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `DEMONSTRATION`.
- Source: sections 7.9 and 18A.
- Gate: `JV-SHIFT-AUTHORITY`.

## 11. Responsibility, access, and audit

### FR-ACCESS-001 — Responsible opening

Online ordering shall not open until Jaime or a currently authorised delegate assumes and records responsibility for the service.

- Type: `FR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.17 and 8.
- Gate: `JV-DELEGATION` before operating without Jaime.

### SEC-ACCESS-001 — Jaime-only access management

Only Jaime shall authorise, revoke, or change staff access and permissions.

- Type: `SEC`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 11.7 and 18A.
- Gate: `JV-ACCESS`.

### SEC-ACCESS-002 — Bounded operational access

Temporary staff and shared kitchen sessions shall have operational access only and shall not expose sensitive administration.

- Type: `SEC`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 8 and 11.3.
- Gate: `JV-ACCESS`.

### AUDIT-ACCESS-001 — Responsibility attribution

The system shall record the responsible person at opening, responsibility handovers, shared-session use, and shift close without falsely claiming individual attribution.

- Type: `AUDIT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 6.17 and 11.3.
- Gates: `JV-DELEGATION`, `JV-ACCESS`.

## 12. Privacy and compliance

### PRIV-DATA-001 — Purpose notice

Before collecting name and telephone number, the system shall explain that the data are used to manage the order and communicate operational changes or incidents.

- Type: `PRIV`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: section 11.1.
- Gate: `JV-PRIVACY`.

### BR-PRIV-001 — No implicit marketing use

Providing operational contact data shall not create a customer account, commercial profile, loyalty enrolment, or marketing consent.

- Type: `BR`; status: `BASELINED`; priority: `MUST_MVP`; verification: `TEST`.
- Source: sections 11.1 and 11.2.

### PRIV-DATA-002 — Least-necessary visibility

Telephone numbers shall remain hidden in routine kitchen queues and shall be revealed only through an explicit operational contact action.

- Type: `PRIV`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `TEST`.
- Source: section 11.3.
- Gate: `JV-PRIVACY`.

### PRIV-DATA-003 — Personal-data request routing

The system and operating procedure shall route personal-data access, correction, or deletion requests to Jaime rather than kitchen staff during active service.

- Type: `PRIV`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `DEMONSTRATION`.
- Source: section 11.4.
- Gates: `JV-PRIVACY`, `JV-COMPLIANCE`.

### PRIV-RETENTION-001 — Approved retention rules

Identified orders, telephone numbers, incidents, payment records, audit events, and SMS records shall use retention and anonymisation rules approved through the pre-launch compliance review.

- Type: `PRIV`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 11.5 and 18A.
- Gates: `JV-COMPLIANCE`, `JV-PRIVACY`.

## 13. Pilot governance and reporting

### PILOT-001 — Two-week baseline

Before pilot activation, Dopis shall record two complete weeks of order volume by channel and order-related call activity using the validated observation procedure.

- Type: `PILOT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `PILOT_EVIDENCE`.
- Source: section 12.2.
- Gate: `JV-PILOT`.

### PILOT-002 — Controlled initial rollout

The first real pilot segment shall operate under manual review with a limited informed participant group during a lower-pressure Wednesday or Thursday session.

- Type: `PILOT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `PILOT_EVIDENCE`.
- Source: section 12.4.
- Gate: `JV-PILOT`.

### PILOT-003 — Operational rehearsal

Before the first real pilot order, Dopis shall pass a rehearsal covering every order channel, alerts, delays, stock conflicts, connectivity loss, payment, handover, and shift close.

- Type: `PILOT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `DEMONSTRATION`.
- Source: section 12.4.
- Gate: `JV-PILOT`.

### PILOT-004 — Real-order prerequisites

The pilot shall not begin until the participating catalog, allergens, hours, stock, alerts, conservative thresholds, minimum privacy controls, and responsible presence are validated.

- Type: `PILOT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `INSPECTION`.
- Source: sections 12.4 and 18A.
- Gates: `JV-PILOT`, `JV-ALLERGENS`, `JV-CATALOG-APPROVAL`, `JV-STOCK`, `JV-THRESHOLDS`, `JV-PRIVACY`.

### PILOT-005 — Pause and rollback

A missing or materially late accepted order, repeatedly unattended alerts, or incorrect allergen information shall pause the affected pilot scope; recurrence after a supposed fix shall trigger manual review or continued pause until corrected.

- Type: `PILOT`; status: `BASELINED`; priority: `MUST_MVP`; verification: `DEMONSTRATION`.
- Source: section 12.5.
- Gate: `JV-PILOT` for exact criteria.

### AUDIT-PILOT-001 — Test-data separation

Simulated and internal-test orders shall be excluded from real pilot calculations or reported in a separately labelled test-data segment.

- Type: `AUDIT`; status: `BASELINED`; priority: `MUST_MVP`; verification: `ANALYSIS`.
- Source: sections 12.6 and 18A.

### PILOT-006 — Four-week evaluation

Dopis shall evaluate the pilot after four complete weeks using reliability, adoption, operational value, on-time performance, commercial observation, and controlled-progression evidence.

- Type: `PILOT`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `PILOT_EVIDENCE`.
- Source: section 12.3.
- Gate: `JV-PILOT`.

### NFR-RELIABILITY-001 — Accepted-order visibility

No accepted order shall be lost or reach the kitchen materially too late for reasonable fulfilment under validated operating conditions.

- Type: `NFR`; status: `BLOCKED_BY_VALIDATION`; priority: `MUST_MVP`; verification: `PILOT_EVIDENCE`.
- Source: sections 12.3 and 12.5.
- Gates: `JV-PILOT`, `JV-THRESHOLDS`.

## 14. Explicit exclusions

The following are not requirements of the first operational MVP unless promoted through an authorised scope change:

- online payment;
- customer accounts;
- loyalty;
- birthday benefits;
- marketing campaigns;
- delivery;
- table reservations;
- coffee products;
- customer self-service cancellation;
- gram-level recipe inventory;
- automatic substitutions;
- automatic recommendation engines;
- advanced analytics and product-margin reporting;
- production hosting and public-domain readiness as part of the local operational implementation slice.

## 15. Readiness interpretation

A requirement marked `BASELINED` is accepted for specification purposes. It is not automatically ready for implementation.

Implementation readiness additionally requires:

- linked use cases and exception flows;
- measurable acceptance criteria;
- reviewed architecture decisions and contracts;
- resolved blocking validation gates;
- dependency and test strategy;
- an explicitly authorised bounded task packet.

## 16. Baseline review checklist

- Every requirement has a stable ID.
- Every requirement references canonical project evidence.
- No requirement silently converts a provisional technology into a product obligation.
- Pending values link to validation gates.
- Epics cover all requirements.
- The traceability skeleton supports reverse navigation.
- No implementation authority is inferred.
