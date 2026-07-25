# Dopis — Technical Discovery and MVP Backend Specification

**Document status:** DRAFT — discovery in progress
**Version:** 0.17
**Date:** 2026-07-25
**Implementation authority:** NOT GRANTED
**Purpose:** Canonical living technical discovery document for the Dopis MVP, reconciling business discovery with verified repository and architecture state.

---

## 1. Product context and document authority

Dopis is a neighbourhood pizzeria in Les Planes, Sant Cugat. The product aims to reduce telephone orders during peak periods by allowing customers to place pickup orders from a mobile-first website.

The Vue 3 frontend demo is now maintained as an independent application under `frontend/` inside the Dopis monorepo. It has been successfully built and deployed through GitHub Pages after the repository migration.

This file is the canonical technical discovery authority:

`docs/current/DOPIS_TECHNICAL_DISCOVERY.md`

The archived initial PRD and handoff remain useful historical evidence, but they are superseded where they conflict with this document. Business discovery may continue in parallel, but proposed changes must be reconciled into this canonical file rather than replacing it with an independently generated full copy.

This document records:

- confirmed business requirements;
- provisional technical decisions;
- verified repository evidence;
- assumptions and risks;
- unresolved decisions;
- authorised sequencing.

Backend implementation authority has not yet been granted.

---

## 2. Current scope decision

### 2.1 MVP objective

The first operational MVP should allow:

1. A customer to browse the current menu.
2. A customer to place a pickup order without creating an account.
3. The customer to provide only the minimum operational details:
   - name;
   - telephone number.
4. The customer to pay at the premises when collecting the order.
5. Kitchen staff to receive the order in a protected web panel displayed on a tablet.
6. Staff to update the order status.
7. Products and orders to be persisted in a relational database.
8. The system to be structured so online payment can be added without redesigning the order domain.

### 2.2 Explicitly deferred

The following are not part of the first operational MVP unless later promoted:

- online card payments;
- Apple Pay or Google Pay;
- customer accounts;
- loyalty points;
- birthday rewards;
- marketing campaigns;
- advanced inventory by ingredient;
- production hosting;
- public domain configuration;
- delivery;
- table reservations;
- coffee products;
- full business analytics;
- advanced SEO work;
- multilingual administration;
- customer self-service cancellation.

These items remain relevant roadmap candidates and must not be made unnecessarily difficult by the MVP architecture.

---

## 3. Confirmed and provisional requirements

### 3.1 Confirmed

- Orders are pickup-only.
- Initial payment method is payment at the premises.
- Customers may order as guests.
- Guest checkout requires a name and telephone number.
- The kitchen receives orders through a web panel opened on a tablet.
- The panel must not be publicly accessible.
- The first staff authentication model has one type of authorised user.
- Staff must be able to cancel orders, block pickup slots, pause online ordering, and mark products unavailable.
- Normal operation should automatically confirm feasible orders using deterministic availability, capacity, and stock rules.
- Staff must be able to switch to a manual-confirmation mode when operational conditions require it.
- In automatic mode, a feasible order is confirmed on the web immediately; no separate acceptance SMS is required.
- Guest customers must receive one SMS containing secure access to order tracking after submission.
- Additional SMS notifications are required when the order is ready, rejected, or cancelled by staff.
- SMS provider selection remains open.
- PostgreSQL is the preferred database.
- Initial development and testing will run on the Project Owner's computer.
- The menu includes pizzas, drinks, desserts, and possibly other non-coffee products. Coffee is excluded.
- All pizzas have one size.
- Product configuration must support allowed ingredient removals, replacements, and paid extras.
- Half-and-half pizzas are excluded initially.
- Every pizza may offer a gluten-free dough option, subject to accurate allergen and cross-contact information.
- Source menu material currently exists as images and PDF documents under the repository documentation area.
- Jaime should be able to perform broad catalog administration without developer intervention.
- Initial inventory scope is product availability plus unit stock for directly countable products.
- Online payments, loyalty, customer history, business metrics, packs, and marketing capabilities are future product goals.
- Monday and Tuesday are closed.
- Wednesday and Thursday premises hours are 18:00–22:00.
- Friday, Saturday, and Sunday premises hours are 18:00–23:00.
- Pizza ordering begins at 19:00 and the earliest pizza pickup is 19:15.
- Initial latest pickup is 21:45 on Wednesday and Thursday and 22:45 from Friday through Sunday.
- Music is normally played during service, so ambient noise may make a standard tablet alert difficult to hear.
- In the kitchen panel, customer name and pickup time are operationally more important than the public order identifier.
- The current visual direction of the kitchen panel is considered a suitable starting point.
- Vegan mozzarella has a materially higher ingredient cost than conventional mozzarella.
- Gluten-free dough arrives sealed on an aluminium base.
- Gluten-free pizzas share the oven, workspace, and kitchen utensils used for other pizzas.
- The current kitchen process therefore has a real cross-contact risk that must be communicated accurately.
- Dopis currently accepts cash and card payments at the premises.
- Dopis asks whether the customer wants a receipt rather than issuing one automatically to every customer.
- Cash discrepancies frequently result from card payments being recorded incorrectly as cash.
- Dopis does not currently have a reliable baseline for comparing telephone, in-person, and web orders.
- The current frontend already contains upselling elements.
- Upselling is part of MVP discovery and must not be treated as validated only because it is visually present in the current frontend.
- Routine MVP operation is primarily performed by Jaime and one other worker who takes responsibility when Jaime is absent.
- The delegated worker can perform almost all operational and administrative tasks performed by Jaime.
- The first MVP does not need an extensive employee, permission, and escalation hierarchy.

### 3.2 Provisional

- Backend candidate: FastAPI.
- API style: REST.
- Real-time kitchen updates: Server-Sent Events or WebSockets, with polling fallback.
- Local environment: Docker Compose.
- Database access: SQLAlchemy 2.
- Database migrations: Alembic.
- Authentication: one staff role with real backend enforcement, not only a frontend route guard.
- Menu source of truth: PostgreSQL rather than hard-coded frontend files.
- Ordering modes:
  - `AUTO_ACCEPT`: feasible orders are confirmed automatically.
  - `MANUAL_REVIEW`: orders remain pending until staff accepts or rejects them.
  - `PAUSED`: new orders cannot be submitted.
- Customer-facing order statuses:
  - `PENDING_CONFIRMATION`
  - `CONFIRMED`
  - `PREPARING`
  - `READY`
  - `COMPLETED`
  - `REJECTED`
  - `CANCELLED`
  - `NO_SHOW`
- Pickup choice should be expressed as:
  - `EARLIEST_AVAILABLE`, with a concrete estimated time or range;
  - `SCHEDULED`, using only currently feasible slots.
- Pickup capacity must use configurable weighted production points per time window from the first operational version, distinct from product stock.
- Each product and eligible modifier may add production points so a simple pizza and a complex pizza do not consume equal kitchen capacity.
- Checkout should create a configurable five-minute provisional capacity hold before final atomic revalidation.
- A staff-proposed alternative pickup slot remains reserved for ten minutes.
- If the customer does not answer an alternative-slot proposal within ten minutes, the proposal expires, capacity is released, the order is rejected automatically, and an outcome SMS is sent.
- Pickup windows use an initial duration of 15 minutes.
- Product and modifier production-point values are technically configured and calibrated; Jaime controls operational window capacity rather than editing the workload model directly.
- Orders exceeding a configurable percentage of a pickup window's capacity must enter manual review, even if nominal capacity remains. The threshold requires validation with real kitchen operation.
- Initial launch accepts same-day orders only. A configurable multi-day advance-order horizon remains a future capability.
- An order whose production load cannot safely fit within a single pickup window must enter manual review in the MVP.
- Sellable-unit stock is provisionally reserved during checkout and committed only when the order is confirmed. Expired or abandoned holds release stock.
- Stock used by an order under manual review is held for ten minutes; expiry releases stock and follows the defined order-expiry outcome.
- Guest tracking should use a secure SMS-delivered access link that establishes a protected browser session without requiring an account.
- Capacity should be configured through templates by weekday and time segment, with date-specific closure, exceptional-opening, special-hours, and special-capacity overrides.
- A valid five-minute provisional checkout hold may complete during an ordering pause; carts without a valid hold cannot submit.
- The final feasible order opportunity is calculated from cart workload, remaining capacity, pickup-window rules, lead time, and latest pickup rather than one fixed cutoff.
- Staff explicitly trigger the start of preparation; accepting an order does not by itself mean that reserved stock has been consumed.
- Cancellation before preparation releases reserved stock and future capacity.
- Cancellation after preparation begins does not automatically restore consumed stock; unused future capacity is released.
- A configurable non-collection grace period begins at the end of the confirmed pickup window; the initial working value is 30 minutes.
- Staff attempt to contact the customer before manually marking an order as `NO_SHOW`.
- Operational incidents may route later orders to manual review rather than automatically blocking the customer. The current working threshold is two relevant incidents within 90 days, pending privacy and operational validation.
- An invalid telephone number is recorded as a distinct incident and may contribute to manual review, subject to fairness and privacy review.
- Operational loss is initially recorded as an occurrence without calculating a monetary amount.
- A failure to deliver the initial tracking SMS routes the order to manual review rather than automatic rejection.
- A material pickup-estimate change updates the private tracking page and sends an SMS; an agreed pickup extension updates the tracking page without requiring another SMS.
- The initial operational fallback uses a tablet plus a limited mobile backup. A ticket printer remains conditional on real operational testing.
- Scheduled orders enter the active queue according to calculated workload and available capacity; the first warning appears at the recommended preparation-start time.
- Staff may revise an estimate more than once. Every material revision appears on the private tracking page, while additional SMS messages are decided case by case.
- For an important delay, the customer may reject the revised pickup time through tracking within an initial ten-minute response window. Silence does not count as acceptance and routes the order to manual review.
- A delay attributable to Dopis is recorded as a local operational incident and must not worsen the customer's incident history.
- Compensation is not yet confirmed for the MVP. Any rules for authorisation, limits, or future-use codes are conditional on Jaime approving compensation as an MVP capability.
- Removing ingredients does not reduce the displayed pizza price as the current working rule.
- Each paid extra may define its own maximum quantity.
- A short kitchen note is permitted, but configured modifiers remain the primary mechanism and notes must not become an unrestricted modification channel.
- If one option becomes unavailable, disable only that option when the product can still be configured validly.
- Dietary and allergen consequences of substitutions or unavailability must be shown clearly.
- Until wording and procedures are validated with Jaime, the site must not claim that gluten-free dough is suitable for coeliac customers or severe allergies.
- Any authorised staff member may mark a product, critical ingredient, or option unavailable; only Jaime or the responsible shift lead may reactivate it.
- Drinks and desserts use an approximate opening count as a strict online-sales ceiling.
- Countable stock adjustments and replenishments record the operator and a simple reason.
- A predicted reactivation time is informational only; availability returns only after responsible staff confirm it.
- Shared critical ingredients may disable only the products or configurations that require them.
- The system does not substitute an unavailable ingredient automatically; the customer must choose an allowed alternative.
- Selected pizzas may have daily limits or pickup-window-specific availability.
- Critical options such as vegan mozzarella or gluten-free dough may use approximate remaining-use counts without gram-level recipe inventory.
- A valid reservation has priority while physical stock exists. A discovered physical shortage routes the affected order to `Requires attention` rather than cancelling it automatically.
- Products that reach zero remain visible as sold out, optionally with an estimated return time.
- A closing stock count is the initial working direction, subject to simplification when normal stock records prove reliable.
- Web, telephone, and in-person orders use the same operational system and share stock, production capacity, pickup windows, and kitchen queues.
- Telephone orders use a fast staff-entry flow with products, quantities, modifiers, pickup time, customer name, and telephone number.
- In-person orders also use name and telephone number as the current working direction so operational incidents can be communicated by SMS.
- Telephone and in-person orders receive the next feasible pickup opportunity and do not automatically displace confirmed web orders.
- A responsible operator may knowingly override calculated capacity for an exceptional manual order, with explicit risk confirmation and auditability.
- Every order records its origin channel: web, telephone, or in person.
- The first MVP keeps payment at the premises for web and telephone orders; online payment remains deferred.
- Customers do not select cash or card during ordering. Staff record the method actually used when collecting payment.
- Payment and handover are separate events. An order is marked paid before staff confirm delivery.
- A failed card payment may be retried or changed to cash.
- If no accepted payment method succeeds, the order is not handed over and an operational incident is recorded.
- Another person may collect using the customer name and order number.
- Product configuration determines whether remaining stock carries between service days or requires a new opening count.
- Closing reconciliation records retained, discarded, or corrected quantities for applicable perishable products.
- Each countable product may define its own low-stock threshold.
- Authorised staff may correct an incorrectly recorded payment method, with an audit trail.
- Only Jaime or the responsible shift lead may reverse an order marked paid in error, and a reason is required.
- An order marked handed over in error may return to `READY`, preserving the correction history.
- Shift close records expected-versus-actual cash differences and may include an explanation.
- Jaime or the responsible shift lead confirms shift closure after reviewing open orders, payments, and incidents.
- Before collecting name and telephone number, the interface explains that they are used to manage the order and communicate operational changes or incidents.
- An operational telephone number does not create marketing permission, a customer account, or a commercial profile.
- Any future marketing consent is separate, optional, explicit, and unchecked by default.
- Telephone numbers remain hidden in kitchen queues and are revealed only through an explicit `Contact customer` action.
- Telephone lookup may locate an order, but staff must also confirm the customer name or order identifier before disclosing information.
- Telephone support initially discloses only order status and estimated pickup time.
- Shift staff see the current order and relevant operational incidents, not the complete commercial history associated with a telephone number by default.
- Personal-data access, correction, or deletion requests are referred to Jaime through a defined procedure rather than handled by kitchen staff during service.
- Where appropriate, personal identifiers are deleted or anonymised while legitimately retainable business records are preserved.
- SMS messages contain Dopis identification, a general status, and the private tracking link rather than the complete order detail.
- The responsible operator signs out at shift end, and responsibility handover records who assumes the operational role.
- The first-month priority is to reduce order-related telephone calls during peak periods.
- Adoption is measured through weekly web-order volume and the share of orders shifting from telephone to web.
- A two-complete-week baseline is recorded before the pilot, covering order counts by channel, time band, and calls used to create or modify orders.
- The quantitative call-reduction target is set only after the real baseline is known.
- The pilot is evaluated after four complete weeks, with particular attention to Friday, Saturday, and Sunday.
- The primary reliability criterion is that no accepted order is lost or reaches the kitchen too late to fulfil reasonably.
- Jaime's judgement that the system is clearly more useful than handling all orders by telephone is a required success condition.
- Opening and closing workload is measured during the pilot before setting a permanent acceptable limit.
- The pilot starts on a lower-pressure Wednesday or Thursday with an approximately one-hour controlled session and a small group of informed regular customers.
- All web orders begin in `MANUAL_REVIEW`; automatic acceptance is enabled only after hours, capacity, alerts, stock, reception, and order handling have been demonstrated reliable.
- Before real pilot orders, staff run a complete operational rehearsal covering multiple channels, alerts, delays, sold-out products, connectivity loss, and shift close.
- The pilot pauses for critical failures such as missing or materially late accepted orders, repeatedly unattended alerts, or incorrect allergen information.
- An isolated manageable delay does not by itself require pausing the pilot.
- At pilot completion, data, incidents, staff workload, and operation are reviewed before selecting the next capability.
- Jaime can create, edit, deactivate, reorder, reprice, and manage availability or stock for products.
- Ingredient, allergen, dietary, and other safety-sensitive catalog changes remain restricted to Jaime or an explicitly authorised responsible person.
- Jaime receives a weekly pilot summary covering channel volume, peak periods, incidents, delays, channel-specific average order value, best-selling products, and frequent combinations.
- On-time performance is measured through delayed-order count, percentage prepared within the promised window, and average delay.
- Operational burden combines opening time, closing time, correction count, and Jaime's assessment.
- Product-margin reporting remains outside the MVP until cost data are sufficiently validated.
- Initial SMS scope includes private tracking access, ready notification, rejection, and cancellation.
- A ticket printer is outside the initial scope and is reconsidered only if tablet and mobile backup prove insufficient during operational testing.
- Until Jaime validates a compensation policy, staff may record the agreed resolution inside the incident without coupons, codes, automated rules, or promised future benefits.
- Initial public content is available in Spanish and Catalan.
- The first visit uses the browser language when supported, with a visible language selector and Spanish as fallback.
- A product cannot be published until its required Spanish and Catalan texts are complete and reviewed.
- Automatic translations are not published without human review.
- Jaime or an authorised responsible person validates product names and descriptions.
- Pizzas require a brief composition description; clearly named packaged drinks and desserts may use only the product name.
- Product photographs are recommended but optional. Products without photographs render without an empty image placeholder.
- Initial menu categories are pizzas, drinks, and desserts.
- Jaime manually controls product order.
- Temporary or special pizzas may have start and end dates.
- Jaime may manually feature one or more products.
- Sold-out products remain visible but cannot be added.
- Jaime may hide a product for one service only.
- Featured products appear first within a category; remaining products retain Jaime's manual order.
- Initial discovery may close when the complete operating flow is defined and remaining material questions depend mainly on Jaime validation.
- Online payment, loyalty, advanced marketing, and advanced analytics are not required to close first-MVP discovery.
- Upselling is included in the first MVP.
- Initial recommendations may include drinks, desserts, and extras compatible with the selected pizza.
- Recommended products retain their normal price; no discounts, dynamic prices, automatic promotions, or automatic cart insertion are included.
- Jaime manually defines recommendation relationships and priority order.
- Jaime or an authorised responsible person may create or change upselling relationships.
- No recommendation is generated when a pizza has no configured relationships.
- Upselling can be disabled globally or for individual source products without removing catalog products.
- Recommendations may appear after adding a pizza and once during cart review.
- At most three relevant recommendations are shown, and the customer may ignore them without friction or explicit rejection.
- Products already in the cart, previously ignored recommendations, unavailable products, duplicates, and expired temporary products are not shown again.
- Multi-pizza carts merge compatible relationships, remove duplicates, and retain one overall maximum of three recommendations.
- Recommended quantities never increase automatically.
- Adding a recommendation applies the same stock, availability, capacity, publication, allergen, and dietary validation as ordinary catalog addition.
- Only published products with complete allergen information may participate in active upselling relationships.
- Recommendations must remain compatible with the customer's final dietary configuration.
- If a later pizza modification makes an already-added recommendation incompatible, the customer is warned and chooses whether to keep or remove it; the system does not remove it silently.
- Pilot measurement records aggregated recommendation impressions and additions, separated by post-pizza and cart-review placement, without creating individual customer profiles.
- Upselling remains enabled after the pilot only if it adds products without material complaints, errors, or an appreciable reduction in checkout completion.
- Operational staff may change availability and stock during service.
- Prices, names, descriptions, commercial content, and sensitive configuration remain restricted to Jaime or an explicitly authorised responsible person.
- Temporary or reinforcement staff use operational access without sensitive administration capabilities.
- Personal and administrative credentials are never shared.
- A common kitchen operational session may exist during the first MVP only when the current responsible shift lead is explicitly recorded and the session has no sensitive administration authority.
- Only Jaime may authorise, revoke, or change staff access and permissions.
- Access for departing staff is removed before the next service, and Jaime reviews active access before the pilot and whenever personnel change.
- Weekly reports are limited to Jaime and people he authorises.
- Export of order lists, telephone numbers, reports, or other commercial or operational information requires Jaime or explicit export authority.
- Availability and stock changes retain actor and timestamp.
- Price, text, and sensitive-configuration changes retain previous value, new value, actor, and timestamp.
- Routine commercial changes do not require a written justification, but accidental corrections remain auditable.
- The mobile backup supports order management, status changes, and urgent availability changes, but not prices, commercial content, access management, or full administration.
- The responsible shift lead is explicitly identified at opening; a responsibility change records the new person and handover time.
- The responsible shift lead may correct payments, resolve incidents, confirm close, and authorise explicitly permitted operational exceptions.
- Unattended critical alerts escalate to the responsible shift lead.
- Open incidents are reviewed before close and are not closed automatically at the end of service.
- Decisions beyond shift authority remain recorded as pending Jaime, while staff apply a safe operational measure.
- A shift may close with an item pending Jaime only when immediate operation is safe and the item remains clearly visible for follow-up.
- Jaime receives a summary of pending decisions during the next shift review or report.
- The responsible shift lead may cancel an already prepared order when the reason and operational loss are recorded.
- When an accepted item is unavailable, staff may offer a valid alternative and record the customer's choice.
- If the alternative costs more, the responsible shift lead may collect the difference or absorb it as the incident resolution; the decision is recorded and does not alter the original product's published price.
- Jaime or an authorised responsible person may reopen an incorrectly resolved incident while preserving its link to the original record.
- The MVP recognises a principal responsible person, Jaime, and one pre-authorised delegated responsible person.
- Delegated authority may be stable or limited to specified shifts or dates.
- Online ordering cannot open unless Jaime or the currently authorised delegate is present and assumes responsibility.
- Delegated responsibility is never inferred from seniority or mere presence.
- The delegated responsible person may modify and validate prices, names, descriptions, ingredients, allergens, dietary rules, featured products, temporary products, and upselling relationships.
- Sensitive product validation requires reliable documentation and responsible review.
- The delegated responsible person may create and publish complete validated products and may access or export authorised operational and commercial reports.
- Only Jaime may create, revoke, or change staff access and permissions.
- Permanent business-policy changes, legal matters, exceptional decisions outside authorised rules, and permanent changes to opening hours or normal capacity remain reserved to Jaime.
- The delegate may make temporary operational adjustments for the current service.
- When Jaime is unavailable and a problem exceeds authorised rules, staff pause only the affected capability and choose the lowest-risk option for both customer and Dopis.
- Isolated safe operation continues when the affected capability can be contained.
- Pending decisions receive priority at the next service opening and in Jaime's next review report.
- Substitutions use explicit product relationships or validated fallback rules by category or price; the delegate may not improvise unrestricted alternatives.
- Jaime defines a fixed maximum per order that the delegate may absorb as a price difference without further consultation.
- Concrete retention periods for identified orders, telephone numbers, incidents, and audit records must be defined and legally reviewed before public launch.
- Outstanding numeric values are collected in one bounded Jaime-validation list rather than discovered through further extensive interview rounds.
- First-MVP business discovery is substantially complete, pending concrete Jaime validation, legal privacy and retention review, and a final cross-domain coherence review.

The frontend may initially present a simplified subset while the backend retains safe terminal states and ordering modes.

---

## 4. Verified repository state and monorepo architecture

### 4.1 Reconciled repository baseline

Repository evidence integrated by this version:

- local path: `/home/sugar/Documents/Dopis_v1`;
- GitHub repository: `Sugar144/dopis`;
- primary branch: `main`;
- repository state integrated through commit `1eb4156`;
- tracked worktree was clean after the migration and deployment sequence;
- documentation custody was established under `docs/`;
- the frontend was moved from the repository root into `frontend/`;
- the GitHub Pages workflow was updated for the new frontend path;
- feature-branch workflow validation completed with:
  - build successful;
  - deploy intentionally skipped outside `main`;
- production workflow run `30117452063` completed with:
  - build successful;
  - deploy successful;
- public frontend URL:
  `https://sugar144.github.io/dopis/`;
- the large university reference ZIP is intentionally ignored by Git and represented by a tracked README;
- generated `node_modules/` and `dist/` directories remain ignored.

The repository audit and frontend migration are complete. They must not remain listed as future work.

### 4.2 Accepted monorepo decision

Dopis uses one Git repository with independently structured applications.

Current and target structure:

```text
Dopis_v1/
├── .github/
│   └── workflows/
├── frontend/
│   ├── public/
│   ├── src/
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   ├── tailwind.config.js
│   └── postcss.config.js
├── backend/                         # not created yet
├── docs/
│   ├── README.md
│   ├── archive/
│   ├── brand/
│   ├── current/
│   │   └── DOPIS_TECHNICAL_DISCOVERY.md
│   ├── decisions/
│   ├── product-sources/
│   └── reference-project/
├── infra/
│   └── local/                       # not created yet
├── compose.yaml                     # not created yet
├── .env.example                     # not created yet
├── README.md
└── .gitignore
```

The frontend and backend remain independently buildable and deployable even though they share one repository.

### 4.3 Reference-project assessment

The university project was assessed read-only.

Useful concepts retained as architectural references:

1. central API client configured through an environment variable;
2. router metadata and a global route guard for staff-only views;
3. cart lines containing product identifiers and quantities rather than trusted client prices;
4. server-side resolution of current product data and prices;
5. cart revalidation before checkout;
6. domain-oriented shared state when frontend state complexity justifies it.

Rejected patterns:

- committed `node_modules`;
- hard-coded API base URLs;
- bundled or minified backend output used as source architecture;
- absence of migrations;
- absence of automated tests;
- unauditable backend structure.

No code reuse from the university project is authorised merely because the concepts were useful.

### 4.4 Frontend state-management direction

The current Dopis frontend uses a scoped `useCart.js` composable, not Pinia.

Do not migrate to Pinia solely because it appears in the reference project. Introduce Pinia only when backend integration creates material shared-state needs such as:

- authenticated staff session;
- persisted and revalidated cart state;
- API-backed catalog caching;
- checkout lifecycle;
- order tracking;
- live kitchen-panel state.

---

## 5. Backend architecture direction

### 5.1 Provisional framework decision

FastAPI is the current backend recommendation.

Project-specific rationale:

- the Project Owner already has practical experience with Python, FastAPI, Docker, and Kubernetes;
- the current Vue frontend is JavaScript rather than a shared TypeScript codebase;
- Dopis has no Node-specific backend requirement;
- FastAPI supports PostgreSQL, validation, OpenAPI, authentication, background work, real-time transports, testing, and future payment integration;
- maintainability will be enforced through module boundaries, dependency rules, migrations, tests, and explicit API contracts rather than relying on framework convention alone.

NestJS remains a valid alternative, but it is not currently preferred merely because it imposes stronger default structure.

### 5.2 Proposed backend stack

```text
FastAPI
Pydantic
SQLAlchemy 2
Alembic
PostgreSQL
pytest
HTTPX test client
Docker Compose
REST
SSE or WebSockets, pending decision
```

### 5.3 Proposed module boundaries

```text
auth
catalog
orders
scheduling
inventory
business_hours
notifications
staff_admin
analytics
```

MVP-active modules:

- `auth`;
- `catalog`;
- `orders`;
- `scheduling`;
- `inventory`;
- `business_hours`;
- `notifications`;
- `staff_admin`;
- minimal operational analytics events.

Deferred but architecturally anticipated:

- registered `customers`;
- online `payments`;
- loyalty;
- campaigns;
- advanced analytics.

A future capability should be anticipated through stable boundaries and extensible data models, not through partial unused implementation.

---

## 6. Draft domain model

### 6.1 Product

Suggested fields:

- `id`
- `name_es`
- `name_ca`
- `description_es`
- `description_ca`
- `category_id`
- `price`
- `is_active`
- `is_available`
- `is_featured`
- `available_from`
- `available_until`
- `hidden_service_date`
- `stock_mode`
- `stock_quantity`
- `production_points`
- `allergen_summary`
- `dietary_labels`
- `image_url`
- `display_order`
- `created_at`
- `updated_at`

### 6.2 Category

Suggested fields:

- `id`
- `name`
- `slug`
- `is_active`
- `display_order`

### 6.3 Order

Suggested fields:

- `id`
- `public_code`
- `status`
- `order_channel`
- `customer_name`
- `customer_phone`
- `pickup_mode`
- `pickup_slot_id`
- `requested_pickup_at`
- `estimated_ready_at`
- `payment_method`
- `payment_status`
- `paid_at`
- `paid_by`
- `subtotal`
- `total`
- `customer_note`
- `internal_note`
- `created_at`
- `confirmed_at`
- `rejected_at`
- `ready_at`
- `completed_at`
- `handed_over_at`
- `handed_over_by`
- `collected_by_name`
- `cancelled_at`
- `cancellation_reason`

### 6.4 Order item

Store a commercial snapshot so historical orders do not change when the menu changes:

- `id`
- `order_id`
- `product_id`
- `product_name_snapshot`
- `unit_price_snapshot`
- `quantity`
- `line_total`
- `selected_options_snapshot`

### 6.5 Responsible people, operational access, and delegation

Candidate identity and authorisation fields:

- `id`
- `username`
- `password_hash`
- `responsibility_type`
- `is_active`
- `authorised_by`
- `authorised_from`
- `authorised_until`
- `authorised_shift_scope`
- `last_login_at`
- `revoked_at`
- `created_at`
- `updated_at`

The first MVP uses a deliberately small responsibility model:

- `PRINCIPAL`: Jaime;
- `DELEGATED`: one person previously authorised by Jaime, either continuously or for specified shifts or dates;
- `OPERATIONAL`: bounded order, status, availability, and stock access;
- `KITCHEN_SHARED`: common operational session attributed to the responsible person currently on duty.

These are capability boundaries, not an extensive organisational hierarchy.

Principal and delegated responsibility:

- either Jaime or an authorised delegate must be present before online ordering opens;
- the current responsible person is identified at service opening;
- responsibility changes record the new person and handover time;
- delegated authority is never assigned automatically;
- the delegated person may perform normal operational and administrative work, including validated safety-sensitive catalog work;
- reliable supplier or product documentation is required before validating ingredients, allergens, or dietary rules.

Reserved to Jaime:

- create, revoke, or change staff access;
- define permanent business policies;
- decide legal matters;
- approve exceptional decisions outside existing rules;
- make permanent changes to opening hours or normal capacity.

Temporary and shared operational access does not include access management.

Personal and administrative credentials remain individual. The shared kitchen session remains an explicitly attributed operational exception.

### 6.6 Payment and handover preparation

Initial active payment direction:

- payment occurs at the premises;
- accepted methods are cash and card;
- the customer does not preselect the method during web or telephone ordering;
- staff record the method actually used;
- the order must be paid before handover;
- card failure may be retried or changed to cash;
- inability to complete payment prevents handover and creates an operational incident.

Orders retain:

- `payment_method`;
- `payment_status`;
- `paid_at`;
- operator or session attribution;
- optional future `payment_provider`;
- optional future `provider_reference`.

Suggested initial status values:

- method before collection: `UNSPECIFIED`;
- method after collection: `CASH` or `CARD`;
- status before collection: `PENDING`;
- status after successful collection: `PAID`;
- failed or corrected payment states require explicit design;
- correction events retain previous value, new value, actor, reason, and timestamp.

Payment and delivery are separate auditable events.

Correction authority:

- authorised staff may correct the recorded payment method;
- only Jaime or the responsible shift lead may reverse a mistaken `PAID` state;
- a mistaken handover may return the order to `READY`;
- every correction preserves an append-only event trail.

Shift-close capability must compare expected and actual cash, allow an explanation, and require responsible approval after reviewing open orders, payments, and incidents.

Future online payment remains outside the first MVP. The domain must later support optional online payment alongside pay-at-store without replacing the operational order lifecycle.

### 6.7 Modifier group and option

Suggested fields:

- modifier group: `id`, `name`, `selection_type`, `minimum_selections`, `maximum_selections`, `is_required`, `display_order`;
- modifier option: `id`, `group_id`, `name`, `price_delta`, `production_points_delta`, `is_active`, `is_available`, optional `stock_quantity`;
- product assignment: `product_id`, `group_id`, product-specific rules and display order.

### 6.8 Pickup capacity window

Suggested fields:

- `id`
- `starts_at`
- `ends_at`
- `capacity_points_total`
- `capacity_points_committed`
- `is_blocked`
- `block_reason`
- `created_at`
- `updated_at`

Capacity commitment must be transactionally safe so simultaneous checkouts cannot overbook the same window.

### 6.9 Ordering configuration

Suggested fields:

- `ordering_mode`
- `default_window_minutes`
- `default_capacity_points`
- `minimum_lead_minutes`
- `maximum_advance_days`
- `pizza_service_start_time`
- `earliest_pickup_time`
- `latest_pickup_time`
- `temporary_delay_minutes`
- `large_order_manual_review_threshold_percent`
- `alternative_slot_hold_minutes`
- `manual_review_hold_minutes`
- `online_ordering_enabled`
- `updated_by`
- `updated_at`

### 6.10 Guest tracking token

Suggested fields:

- `id`
- `order_id`
- `token_hash`
- `expires_at`
- `used_at`
- `revoked_at`
- `created_at`

The raw token must not be stored in plaintext. The preferred flow is a one-time, high-entropy URL token delivered by SMS, exchanged for a secure browser session, followed by a redirect to a clean tracking URL.

### 6.11 Order status event

Keep an append-only operational history:

- `id`
- `order_id`
- `from_status`
- `to_status`
- `actor_type`
- `actor_id`
- `reason`
- `created_at`

### 6.12 Stock adjustment and availability event

The MVP needs an auditable operational record for:

- opening count;
- replenishment;
- sale not otherwise registered;
- breakage or waste;
- internal consumption;
- incorrect count correction;
- sold-out action;
- reactivation;
- physical-shortage exception.

Exact persistence remains a schema decision. Each event must identify the affected item, quantity or availability change, operator, reason, and timestamp.

### 6.13 Lightweight critical-ingredient allowance

Shared limited ingredients and options may use an approximate number of available uses rather than a recipe-level quantity.

This capability must support:

- one allowance affecting multiple product configurations;
- provisional reservation during checkout or manual review;
- definitive consumption on confirmation;
- release on expiry;
- manual correction;
- independent disablement;
- optional availability by pickup window.

It is not gram-level ingredient inventory and must not be presented as exact recipe depletion.

### 6.14 Upselling relationship

Upselling is configuration-driven rather than automatically inferred.

Candidate fields:

- `id`
- `source_product_id`
- `recommended_product_id`
- `priority`
- `is_active`
- `created_by`
- `updated_by`
- `created_at`
- `updated_at`

Rules:

- the source product is normally a pizza;
- the recommendation may be a drink, dessert, or compatible extra;
- source and recommended products must be distinct;
- one relationship must not be duplicated;
- activation requires the recommended product to be published with complete allergen information;
- global and source-product upselling switches are evaluated independently from product publication;
- temporary-product validity, current availability, dietary compatibility, and cart contents are evaluated at presentation time.

### 6.15 Upselling measurement event

The pilot needs aggregated events for:

- recommendation shown;
- recommendation added.

Each event may retain:

- recommendation relationship;
- placement: `POST_PIZZA` or `CART_REVIEW`;
- order or anonymous checkout session reference where operationally necessary;
- timestamp.

Routine reporting must aggregate these events and must not construct individual customer recommendation profiles.

### 6.16 Administrative change event

Material administrative changes retain an append-only history.

Candidate fields:

- `id`
- `entity_type`
- `entity_id`
- `field_name`
- `previous_value`
- `new_value`
- `actor_id`
- `shared_session_responsible_id`
- `reason`
- `created_at`

Rules:

- availability and stock changes require actor and timestamp;
- price, text, and sensitive-configuration changes also retain previous and new values;
- routine commercial changes do not require a written reason;
- payment-state reversal, incident escalation, cancellation of a prepared order, and other exceptional corrections require a reason;
- correcting an accidental change creates another event rather than deleting history.

### 6.17 Shift responsibility and handover event

The operational system records:

- responsible person at service opening;
- whether responsibility is principal or delegated;
- delegation validity and applicable shift or date scope;
- start time;
- replacement responsible person;
- handover time;
- temporary current-service adjustments;
- closing confirmation;
- unresolved incidents and decisions pending Jaime.

Opening is blocked when neither Jaime nor a currently authorised delegate assumes responsibility.

A common kitchen session is attributed to the current principal or delegated responsible person without pretending that every action identifies an individual operator.

### 6.18 Pending-Jaime decision

When an incident exceeds shift authority, retain:

- related order or incident;
- safe operational measure applied;
- summary of the unresolved decision;
- responsible shift lead;
- created time;
- review status;
- Jaime review or resolution.

The record may remain open after shift close when immediate operation is safe.

### 6.19 Substitution rule

Authorised substitutions are defined through:

- a specific relationship between unavailable and alternative products; or
- a validated fallback rule based on category, compatible configuration, and price boundary.

Candidate fields:

- `id`
- `unavailable_product_id`
- `alternative_product_id`
- `category_rule`
- `maximum_price_difference`
- `dietary_constraints`
- `allergen_constraints`
- `is_active`
- `approved_by`
- `created_at`
- `updated_at`

Specific relationships take priority over general fallback rules.

The delegated responsible person may apply configured rules but may not invent unrestricted alternatives.

### 6.20 Operational threshold register

Outstanding numerical values should be held in one bounded pre-pilot validation list, including:

- large-order threshold;
- relevant-delay threshold;
- severe-delay threshold;
- customer-response windows;
- reservation or review extensions;
- maximum absorbed price difference per order;
- alert and escalation timeouts;
- other already identified operational limits.

This register validates values for discovered rules; it is not a new broad discovery phase.

---

## 7. Draft order lifecycle

### 7.1 Normal automatic mode

```text
CHECKOUT
   -> AVAILABILITY_REVALIDATION
   -> CONFIRMED
   -> PREPARING
   -> READY
   -> COMPLETED
```

In `AUTO_ACCEPT` mode, an order is confirmed only after the backend atomically revalidates:

- online ordering is enabled;
- the selected slot is still available;
- the order fits the slot's remaining production capacity;
- all products and selected modifier options remain available;
- unit stock remains sufficient;
- the order is within operating and cutoff rules.

If revalidation fails, the order should not be silently accepted and rejected later. The customer should receive the nearest feasible alternatives before final confirmation whenever possible.

### 7.1A Upselling interaction

Upselling is optional and must never block checkout.

Presentation opportunities:

1. immediately after a pizza is added;
2. once during cart review.

Selection rules:

- combine relationships from every pizza currently in the cart;
- remove duplicate recommendations;
- exclude products already in the cart;
- exclude recommendations already ignored in the current checkout;
- exclude inactive, unpublished, sold-out, unavailable, temporally expired, or incompatible products;
- apply configured priority;
- show at most three recommendations overall;
- never increase a recommended quantity automatically.

Adding a recommendation uses the ordinary add-to-cart path and revalidates publication, stock, availability, capacity, allergen data, and dietary compatibility.

If a later pizza modification makes an already-added recommendation incompatible, the customer receives a visible warning and decides whether to retain or remove the item. No cart item is silently removed.

### 7.2 Manual-review mode

```text
PENDING_CONFIRMATION
   ├──> CONFIRMED -> PREPARING -> READY -> COMPLETED
   ├──> ALTERNATIVE_PROPOSED -> CONFIRMED / DECLINED / EXPIRED
   └──> REJECTED
```

In `MANUAL_REVIEW` mode, the interface must clearly state that the request is pending kitchen confirmation. The initial tracking-link SMS is sent after submission. Acceptance is shown on the tracking page; rejection triggers an additional SMS. Staff may accept the requested slot, reject the order, or propose an alternative slot.

A proposed alternative slot is reserved for ten minutes. The tracking page allows the customer to accept or decline it. Acceptance atomically confirms the order and commits the reserved capacity. Decline or expiry releases the hold. If no response is received before expiry, the order is automatically rejected and an outcome SMS is sent.

### 7.3 Cancellation path

```text
PENDING_CONFIRMATION / CONFIRMED -> CANCELLED
```

Staff cancellation is required. Customer self-service cancellation is deferred. A later policy may permit it only before preparation or before a configurable cutoff.

### 7.4 Customer wording

Recommended customer-facing distinction:

- **request received:** stored but awaiting manual confirmation;
- **order confirmed:** capacity and availability have been committed;
- **in preparation:** kitchen work has started;
- **ready:** the customer may collect it.

### 7.4A Manual order entry and channel parity

Web, telephone, and in-person orders enter the same order domain.

Shared rules:

- one stock ledger;
- one capacity model;
- one pickup-window model;
- one kitchen queue;
- one status lifecycle;
- one payment and handover trail.

Telephone order entry must be optimised for staff speed while still requiring explicit product, modifier, pickup, name, and telephone data.

In-person order entry follows the same domain flow. Requiring a telephone number for every in-person order remains a working decision pending Jaime's validation of operational burden and privacy necessity.

Manual orders receive the next feasible pickup opportunity. They do not silently displace already confirmed orders.

A responsible operator may override calculated capacity only through an explicit exceptional action that records the actor and acknowledged operational risk.

Each order preserves its source channel:

- `WEB`;
- `PHONE`;
- `IN_PERSON`.

### 7.5 Preparation, payment, handover, and non-collection

- A confirmed future order remains scheduled until it approaches its recommended preparation time.
- Staff may begin preparation earlier; the action is permitted and recorded.
- Preparation formally begins when staff select `Start preparation`.
- Payment and physical handover are separate events.
- Staff confirm successful payment before handover.
- `COMPLETED` is assigned only when authorised staff confirm handover to the customer.
- A different collector may identify the order using customer name and order number.
- If no accepted payment method succeeds, the order is not handed over and an operational incident is recorded.
- An incorrectly recorded payment method may be corrected by authorised staff with traceability.
- A mistaken `PAID` state requires responsible-staff reversal and a reason.
- A mistaken handover may return the order to `READY` without deleting the original event.
- The working `NO_SHOW` process is:
  1. wait until the end of the confirmed pickup window;
  2. apply the configurable grace period, initially 30 minutes;
  3. attempt customer contact;
  4. allow an authorised extension within a configurable maximum;
  5. let staff mark `NO_SHOW` manually.
- If a customer explicitly says they will not collect an already prepared order, record a customer cancellation and an operational loss rather than an unexplained `NO_SHOW`.

### 7.6 Operational queues and delays

The panel should distinguish:

- `Requires attention`;
- active preparation;
- `Ready for pickup`;
- `Scheduled`;
- shift history.

Operational queues are ordered by the calculated recommended preparation time, not only by submission time. Delayed orders rise in prominence and show the elapsed delay without relying on hover.

Delay handling distinguishes a warning from a serious delay. A serious delay produces a one-time audible escalation. Staff may start preparation, revise the estimate, or cancel.

Cancelled orders and unresolved incidents remain visible until staff select `Incident reviewed`.

### 7.7 Customer response to an important delay

For an important revised pickup estimate:

1. the revised time appears on the private tracking page;
2. the customer may reject it through a narrowly scoped tracking action;
3. the initial response window is ten minutes;
4. silence does not count as acceptance;
5. no response routes the order to manual review;
6. rejection places the order in `Requires attention`.

Resolution depends on preparation state:

- before preparation: staff may cancel or offer another feasible pickup time;
- after preparation begins: staff contact the customer before resolving the order;
- the customer may still reject the delay;
- the final resolution and any operational loss are recorded.

A cancellation caused by Dopis failing to meet its commitment is a local operational incident, not a customer incident. If preparation has not started, that cancellation does not create a prepared-product operational loss.

### 7.8 Conditional compensation direction

Compensation is not currently an accepted MVP capability.

Until Jaime validates a formal policy, staff may record the resolution actually agreed with the customer inside the incident.

The MVP must not assume:

- coupon codes;
- discount codes;
- automatic compensation rules;
- future credits;
- loyalty benefits.

If Jaime later validates compensation as an MVP capability, structured authorisation, type, value, responsibility, expiry, and fulfilment rules may be added.

### 7.9 Responsible-person incident authority and escalation

Jaime or the authorised delegated responsible person may:

- correct permitted payment errors;
- resolve ordinary operational incidents;
- authorise exceptions already covered by validated rules;
- cancel an already prepared order;
- offer configured valid substitutions;
- decide whether to collect or absorb an authorised price difference;
- confirm shift close;
- reopen an incorrectly resolved incident.

Prepared-order cancellation records:

- reason;
- operational loss;
- actor;
- timestamp.

When an accepted product is unavailable:

1. the order moves to `Requires attention`;
2. staff apply a specific substitution relationship when available;
3. otherwise, staff may apply a validated category or price fallback rule;
4. the customer's selection is recorded;
5. any higher price is collected or absorbed within Jaime's configured per-order limit;
6. the substitution does not change the original product's published price.

The delegated responsible person may not improvise an alternative outside approved rules.

When an issue exceeds authorised rules and Jaime is unavailable:

- pause only the affected product, option, channel, or capability where safe isolation is possible;
- apply the lowest-risk operational measure;
- preserve the issue as pending Jaime;
- keep unaffected service running when it remains safe;
- prioritise the pending decision at the next opening and in Jaime's report.

A shift may close with a pending Jaime decision only when immediate operation is safe and the unresolved item remains visible.

Incident reopening preserves the original incident and adds a linked continuation.
---

## 8. Kitchen tablet requirements

The tablet panel is viable for an MVP, but it must be treated as an operational system rather than only a visual dashboard.

Minimum requirements:

- authenticated access;
- large touch targets;
- high-contrast order states;
- audible alert for a newly received order;
- visible connection status;
- automatic refresh or live updates;
- fallback manual refresh;
- prevention of duplicate state transitions;
- clear indication of orders requiring action;
- optional screen wake strategy to be evaluated;
- recovery after browser refresh;
- no dependency on a printer for normal operation.

Operational fallback must still be defined for:

- internet or Wi-Fi failure;
- server failure;
- tablet battery loss;
- browser logout;
- missed audible notification.

A printer is not required for the MVP, but the business needs a documented fallback procedure.

Additional working requirements from business discovery:

- a new order produces an audible alert, remains highlighted, and requires explicit `Order seen` acknowledgement;
- an unacknowledged order repeats its alert and pauses automatic acceptance after a configurable timeout;
- the alert must be tested with the real music level, tablet position, and kitchen noise;
- if the tablet loses connection, the panel retains the last visible data as clearly stale and prevents state-changing actions;
- after an initial three-minute disconnection, new online orders pause;
- recovery requires staff review and explicit `Resume`;
- a mobile backup may view orders, change operational states, and apply urgent availability changes;
- the mobile backup must not edit prices, commercial content, access permissions, or expose full administration;
- staff complete a readiness checklist, explicitly identify Jaime or the currently authorised delegate, and select `Open orders`;
- opening is blocked if neither authorised responsible person is present;
- a common kitchen operational session may be used during the first MVP only after the responsible person is registered;
- the common kitchen session never exposes sensitive administrative functions;
- the pre-opening checklist covers kitchen readiness, shift capacity, countable drinks and desserts, sold-out products, and a short list of critical ingredients or options;
- any authorised operator may mark an item sold out, while reactivation requires Jaime or the responsible shift lead;
- delivered orders leave the primary view but remain available in shift history;
- customer name and pickup time have greater visual prominence than the order identifier;
- telephone numbers remain hidden in operational queues;
- an explicit `Contact customer` action reveals the telephone number only when operationally needed;
- the same telephone-visibility rule applies to tablet and mobile backup;
- previous incidents appear as a minimal summary, with detail available only when operationally necessary;
- no essential action or information may depend on hover.

The digital panel remains the source of truth. A ticket printer is outside the initial MVP scope and is reconsidered only if operational tests show that tablet and mobile alerts are insufficient. If later introduced, reprints must be marked `COPY`, telephone numbers are omitted by default, and print failure must not silently leave automatic acceptance running.

At shift end, the current responsible person reviews open incidents, payments, and pending Jaime decisions before confirming close. Incidents do not close automatically. A responsibility change during service records the new responsible person and handover time. Jaime reviews pending decisions before the next service opens.

---

## 9. Catalog, inventory, and production capacity boundary

“Inventory” and “kitchen capacity” are different systems and must not be represented by the same counter.

### 9.1 Product and option availability

Any authorised staff member may mark a product, critical ingredient, or option sold out.

Reactivation rules:

- drinks and desserts may be reactivated after a replenishment is recorded;
- pizzas, ingredients, and modifier options require explicit confirmation from Jaime or the responsible shift lead;
- an expected reactivation time is informative and never re-enables online sale automatically.

An unavailable shared ingredient disables only the products and configurations that actually require it. No automatic substitution is performed.

A sold-out product remains visible to the customer, clearly marked unavailable. When known, the interface may show an estimated return time.

### 9.2 Sellable-unit stock

Track countable stock for drinks, desserts, and other directly countable products.

Opening operation:

- staff enter an approximate count at the start of the shift;
- the recorded quantity is a strict online-sales ceiling;
- responsibility for counting and the product set requiring counts remain pending Jaime validation.

Reservation semantics:

- checkout provisionally reserves countable stock for five minutes;
- automatic confirmation commits stock;
- manual review reserves stock for the applicable review period;
- expiry or abandonment releases the reservation;
- a daily product limit follows the same reserve, commit, and release semantics;
- cancellation before preparation restores eligible stock;
- after `Start preparation`, consumed stock is not automatically restored.

Adjustment and replenishment:

- any authorised operator may record replenishment or correction;
- each change records operator and one simple reason;
- initial reasons are:
  - unregistered sale;
  - breakage or waste;
  - internal consumption;
  - incorrect count;
  - replenishment.

A valid reservation keeps priority when physical stock exists. If staff discover that the reserved unit does not physically exist, the order moves to `Requires attention`; staff offer an allowed alternative or cancel manually.

If stock reaches zero before reservation, the customer must remove or replace the item before continuing.

### 9.2A Limited products and shared critical ingredients

Selected pizzas may have daily limits when they depend on limited preparations or ingredients.

Shared critical ingredients can control several product configurations. The system disables only configurations that require the exhausted ingredient.

For items such as vegan mozzarella or gluten-free dough, the MVP may track an approximate number of remaining uses without requiring weight-based inventory.

Limited products or options may also be available only for selected pickup windows.

Before opening online orders, staff review a short configured list of critical ingredients and options.

### 9.2B Stock reconciliation

The initial working procedure includes a closing count.

Repeated differences between expected and physical stock must be highlighted for responsible review.

The closing count should later be reduced or removed where ordinary records of sales, reservations, replenishments, and corrections prove sufficiently reliable.

Web, telephone, and in-person orders must all reserve and consume from the same stock records.

Each product may define one of these service-day policies:

- carry remaining stock into the next service day;
- require a fresh opening count;
- require closing treatment for retained, discarded, or corrected quantities.

Applicable perishable products require an explicit closing outcome.

Each countable product may also define a low-stock threshold. The exact warning behaviour remains open.

### 9.3 Production capacity

Kitchen capacity controls how much work may be committed to a pickup window. The first operational version must already distinguish simple and complex pizzas through weighted production points.

Initial model:

- initial time-window duration of 15 minutes;
- configurable maximum production points per window;
- capacity templates may vary by weekday and time segment, with date-specific overrides;
- each pizza has a base production-point value;
- selected modifiers may add production points;
- drinks and ready-made desserts normally consume zero points;
- the order load is the integer sum of product and modifier points;
- blocked windows accept no new orders;
- staff may add temporary delays or reduce capacity;
- the earliest-available estimate advances when nearer windows are full;
- web, telephone, and in-person orders consume the same capacity;
- manual orders normally receive the next feasible window;
- Jaime or the authorised delegate may explicitly override the capacity warning for an exceptional current-service order without altering prior confirmed commitments;
- the delegate may make temporary capacity adjustments for the current service;
- permanent normal-capacity or operating-hours changes remain reserved to Jaime.

Use small integer points rather than fractional time estimates. Example values must be calibrated with Jaime and kitchen observation rather than treated as universal facts. Product and modifier point values are technical configuration in the initial MVP; Jaime adjusts the operational capacity of windows rather than editing individual workload weights. The model may later evolve into station-specific capacity or historical prediction.

A configurable large-order threshold is also required. If an order consumes more than a defined percentage of one pickup window's capacity, it enters manual review even when the raw capacity calculation would permit automatic acceptance. The initial percentage must be validated with Jaime and real kitchen observations.

For the initial MVP, any order whose calculated production load cannot be safely accommodated within one pickup window also enters manual review. The system does not automatically distribute such an order across consecutive windows until a validated production-planning rule exists.

### 9.4 Ingredient and recipe inventory

A later system may define recipes or bills of materials so confirmed orders decrement precise ingredient quantities.

This remains distinct from the MVP's lightweight approximate-use allowances for a small set of critical shared ingredients or options.

### MVP decision

Implement:

- availability on/off with restricted reactivation;
- strict sellable-unit stock for countable products;
- auditable replenishment and adjustment reasons;
- transactional reservations;
- optional daily limits;
- lightweight approximate-use counts for selected critical ingredients or options;
- window-specific availability where needed;
- weighted production points by pickup window;
- opening review and provisional closing reconciliation.

Defer:

- gram-level ingredient inventory;
- full recipe or bill-of-material depletion;
- automatic substitutions;
- automatic reactivation from estimated replenishment times.

The operating burden and reliability of opening and closing counts require validation with Jaime.

---

## 10. Menu administration and product configuration

The intended owner of menu data is Jaime or authorised staff.

### 10.1 MVP administration target

Provide protected catalog CRUD for:

- categories;
- products;
- Spanish and Catalan names and descriptions;
- prices;
- active/inactive state;
- available/sold-out state;
- featured-product selection;
- temporary start and end dates;
- service-specific hiding;
- optional image references;
- unit stock where applicable;
- daily limits and approximate critical-option uses where applicable;
- pickup-window-specific availability;
- stock adjustments and replenishments;
- display order;
- product-to-modifier assignments;
- upselling relationship creation, editing, prioritisation, and activation;
- global and source-product upselling enablement.

Historical records must be preserved through order-item snapshots and soft deletion or deactivation. Removing a product from the active menu must not corrupt old orders.

Availability permissions are intentionally asymmetric: authorised staff may disable an item quickly, while reactivation requires Jaime or the responsible shift lead. Stock and availability changes retain operator, timestamp, and reason.

Operational staff may change availability and stock during service.

Jaime and the currently authorised delegate may manage prices, names, descriptions, commercial content, featured and temporary products, upselling relationships, ingredients, allergens, dietary rules, and product publication.

Sensitive information may be validated only from reliable documentation with an explicit responsible review.

Temporary or reinforcement staff receive no sensitive administration access.

Administrative corrections retain the original change and the corrective event.

Image upload may be deferred if it materially expands storage and deployment scope; an image path or URL field can be retained.

### 10.1A Catalog publication and approval

A product may be published for online sale only when these minimum data are complete:

- Spanish and Catalan product name;
- required Spanish and Catalan description;
- ingredients;
- regulated allergens and known traces;
- price;
- availability;
- applicable dietary labels.

Jaime or another explicitly authorised responsible person provides final approval for new or materially changed products, including product names and descriptions in both launch languages.

Change rules:

- a price-only change may be published without repeating the full allergen review only when recipe, quantity, product, and supplier remain unchanged;
- a recipe, ingredient, quantity, or supplier change requires review of ingredients, allergens, possible traces, and dietary labels;
- the affected product or option remains unavailable online until that review is complete;
- if staff detect incorrect safety or dietary information, they immediately disable the affected product or option and notify the responsible person;
- material changes to ingredients, allergens, availability, and price retain who-and-when traceability.

A product with incomplete or unverifiable allergen information must not be sold online at public launch.

### 10.1B Multilingual content and menu presentation

Initial public languages:

- Spanish;
- Catalan.

Language behaviour:

- use the browser language on first visit when supported;
- expose a visible language selector;
- fall back to Spanish;
- do not publish automatic translations without human review.

Content requirements:

- pizzas need a short composition description;
- clearly named packaged drinks and desserts may omit a separate description;
- photographs are recommended but optional;
- missing photographs do not reserve an empty visual area;
- names and descriptions require approval from Jaime or an authorised responsible person.

Initial categories:

- pizzas;
- drinks;
- desserts.

Within each category:

- active featured products appear first;
- remaining products follow Jaime's manual order;
- sold-out products stay visible and cannot be added;
- temporary products respect configured start and end dates;
- a product may be hidden for one specific service without permanent deactivation.

### 10.2 Modifier model

Products must support explicitly configured modifier groups and options rather than an unrestricted free-text ingredient editor.

Candidate modifier groups:

- dough:
  - regular;
  - gluten-free;
- cheese substitution where permitted:
  - vegan mozzarella;
  - standard mozzarella;
- removable ingredients configured per pizza;
- paid extras, such as extra cheese;
- future replacement options.

Suggested modifier-group fields:

- selection type: single or multiple;
- minimum and maximum selections;
- required or optional;
- price delta;
- availability;
- product-specific eligibility;
- display order.

Half-and-half pizzas are excluded initially.

Additional working rules:

- ingredient removal does not reduce price unless Jaime later defines an explicit exception;
- substitutions are configured per product rather than inferred from free text;
- each extra may have an independent maximum quantity;
- a short kitchen note is allowed only for constrained, previously accepted exceptions;
- unavailable options are removed individually when a valid product configuration remains;
- vegan mozzarella and other higher-cost substitutions may require their own price delta, pending Jaime's validation;
- free-text notes are limited to non-ingredient instructions and exceptions explicitly authorised by Jaime;
- a note must not override configured modifier eligibility, price, availability, or allergen rules.

### 10.3 Allergen and dietary information

The catalog must store ingredients, regulated allergens, known traces, dietary labels, and cross-contact notices. A generic waiver is not a substitute for accurate product information and validated kitchen procedures.

Information sources are product labels and supplier documentation reviewed with Jaime. Supplier, recipe, ingredient, or quantity changes trigger a new review.

Customer-facing requirements:

- show allergens on every product;
- recalculate and display allergens from the final selected configuration;
- warn at selection time when a substitution introduces an allergen;
- repeat the final allergen information in the order summary before confirmation;
- update vegan or vegetarian classification when a modifier changes the final product;
- provide initial filters for:
  - `Vegan`;
  - `Vegetarian`;
  - `Gluten-free dough option`;
- show clearly when an unavailable option changes the dietary configuration that can still be ordered.

Current verified operating facts are that gluten-free dough arrives sealed on an aluminium base but shares the oven, workspace, and utensils with products containing gluten.

The option must therefore be presented as `Gluten-free dough option`, not as a guarantee that the complete pizza is gluten-free.

The interface must:

- show a general cross-contact warning in the menu;
- show a specific warning when the customer selects the option;
- require explicit confirmation that the customer has read and understood the warning;
- avoid claiming suitability for coeliac customers or severe allergies before validation;
- advise customers with severe allergies to contact the premises before ordering;
- state that online ordering cannot guarantee absence of cross-contact;
- allow staff to disable the gluten-free dough option independently;
- disable it whenever the validated operating procedure cannot be followed.

Public launch is blocked until Jaime validates:

- supplier documentation;
- actual kitchen procedure;
- complete ingredient, allergen, and trace information;
- exact customer-facing wording;
- which severe-allergy requests the premises can responsibly accept;
- who besides Jaime may approve safety and dietary information.
---

## 10A. Pickup scheduling and slot-selection UX

### Recommended hybrid flow

1. Before or while browsing the menu, show whether online ordering is open and the current earliest estimated pickup time.
2. Let the customer build the basket without permanently reserving a slot.
3. When the basket is complete, calculate feasible pickup times using the actual items, modifiers, current stock, operating hours, blocked windows, and remaining capacity.
4. Offer:
   - **Earliest available**, displaying a concrete estimated time or narrow range;
   - **Schedule for later**, displaying only feasible slots.
5. When checkout begins, create a configurable five-minute provisional capacity and sellable-stock hold.
6. On final submission, atomically revalidate and commit the slot together with the order.
7. If the selected time is no longer feasible, return nearby alternatives without creating a confirmed order.

This avoids both bad extremes:

- asking for a precise time before the system knows the basket workload;
- accepting a complete order and only afterwards discovering that no feasible pickup time exists.

### Staff controls

The staff panel should eventually support:

- switching between automatic, manual-review, and paused modes;
- blocking or reopening individual pickup windows;
- changing temporary capacity;
- adding a temporary preparation delay;
- disabling products or options;
- cancelling a confirmed order with a reason.

---

## 10B. Guest order tracking

A customer account is not required for basic order tracking. Cookies alone are not a sufficient primary recovery mechanism because they are device-specific, may be cleared, and do not help when the customer changes browser or device. Requiring the customer to manually copy a link also creates avoidable friction.

Confirmed practical security model:

1. After order submission, the current browser receives an opaque tracking session in a `Secure`, `HttpOnly`, `SameSite` cookie.
2. The customer receives one SMS whose purpose is access to tracking, not a redundant acceptance notification.
3. The SMS contains a high-entropy, time-limited, single-use access token.
4. Opening the link exchanges the raw token for a protected browser session.
5. The backend redirects to a clean order-status URL so the token does not remain in normal navigation.
6. Only a hash of the raw access token is stored server-side.
7. The tracking page exposes only the minimum order, status, and pickup information.
8. Sequential public order codes alone never authorise access.
9. The tracking session can be revoked when necessary and expires after a configurable retention period.

The status page is read-only for the normal order lifecycle, except for narrowly scoped responses to:

- accept or decline a staff-proposed alternative pickup slot;
- reject an important revised pickup estimate.

These actions do not give the customer general order-editing or self-service cancellation authority.

SMS policy for the first operational MVP:

- submission: send the secure tracking-access link;
- acceptance: show on the web/tracking page, without an additional SMS;
- ready: send SMS;
- rejected or cancelled by staff: send SMS with the outcome and contact guidance;
- SMS content is minimised to Dopis identification, general status, and private tracking link rather than full order detail;
- every material estimate change appears in tracking;
- staff decide whether each additional material change also requires an SMS;
- an agreed pickup extension updates tracking without necessarily sending another SMS.

---

## 11. Privacy and customer data baseline

The first MVP separates operational order data from future marketing, loyalty, or customer-account data.

### 11.1 Operational purpose and notice

Before requesting name and telephone number, the interface explains briefly that the data are used to:

- manage and fulfil the order;
- communicate status changes or operational incidents;
- locate the current order when the customer contacts Dopis.

Candidate operational data:

- name;
- telephone number;
- ordered products;
- pickup information;
- timestamps;
- operational status;
- relevant incident and correction events.

Providing a telephone number for an order does not automatically create:

- a customer account;
- a commercial profile;
- marketing consent.

### 11.2 Marketing and loyalty separation

Any future commercial consent must be:

- separate from checkout;
- optional;
- explicit;
- unchecked by default;
- revocable through a defined process.

Operational telephone numbers must not be silently reused for promotions.

### 11.3 Staff access and disclosure

Operational access follows least-necessary visibility:

- telephone numbers remain hidden in kitchen queues;
- an explicit `Contact customer` action reveals the number when needed;
- tablet and mobile backup follow the same rule;
- staff may search by telephone when a customer calls;
- before disclosing information, staff also confirm the customer name or order identifier;
- telephone support initially discloses only order status and estimated pickup time;
- shift staff see the current order and relevant incident summary;
- complete commercial history is not exposed by default.

Access events, report access, exports, and administrative changes should be auditable where proportionate.

A common kitchen operational session may exist during the first MVP, but:

- the current shift lead must be registered;
- the session exposes only operational functions;
- personal and administrative credentials remain individual;
- audit history must identify shared-session use honestly rather than claiming individual attribution.

### 11.4 Personal-data requests

Requests to access, correct, or delete personal data are referred to Jaime through a documented procedure.

Kitchen staff do not resolve these requests during active service.

Where removal is appropriate, the accepted direction is to delete or anonymise identifying data while preserving only business, accounting, or operational records that may legitimately remain.

The procedure, identity-verification method, response ownership, and legal retention exceptions must be defined before production.

### 11.5 Retention and anonymisation

Concrete retention periods must be defined and legally reviewed before public launch for:

- identified orders;
- telephone numbers;
- operational incidents;
- payment and cash-close records;
- audit and correction events;
- SMS delivery records.

The provisional 90-day incident-risk window is not itself a retention policy and cannot substitute for approved retention periods.

Metrics should use anonymised or aggregated data where identifiable records are no longer required.

### 11.6 Communication minimisation

SMS messages contain only:

- Dopis identification;
- general order status;
- private tracking link.

They do not include the complete order detail.

### 11.7 Technical baseline

- collect only data required for a defined purpose;
- display the operational-purpose notice before collection;
- protect kitchen and administration endpoints;
- enforce role and session boundaries;
- close responsible sessions at shift end;
- separate operational data from future marketing consent;
- avoid direct storage of payment-card data;
- support correction, anonymisation, and deletion workflows;
- retain auditability for material corrections;
- restrict access creation, revocation, and permission changes to Jaime;
- represent stable or shift-bounded delegated authority explicitly;
- block opening without Jaime or an authorised delegate;
- remove departing-staff access before the next service;
- restrict weekly reports and data exports to Jaime and authorised delegated access;
- preserve previous and new values for sensitive administrative changes;
- record shift responsibility and shared-session attribution;
- obtain legal and privacy review before public production.

This section is a design baseline, not legal advice.
---

## 12. Analytics, baseline, and MVP validation

The first backend should capture reliable operational events without requiring customer accounts.

### 12.1 Primary MVP outcome

The first-month priority is to reduce order-related telephone calls during peak service.

Primary adoption measures:

- web orders per week;
- absolute order volume by channel;
- percentage of orders by channel;
- estimated share of telephone orders shifted to web;
- order-creation and order-modification calls by time band.

A numeric call-reduction target must not be invented before a reliable baseline exists.

### 12.2 Pre-pilot baseline

Dopis currently lacks a reliable channel baseline.

Before pilot activation, record two complete weeks of:

- order count by `WEB`, `PHONE`, and `IN_PERSON`;
- time band;
- calls used to create an order;
- calls used to modify an order.

The baseline does not require full item-level detail for every historical order.

Compare both:

- absolute volume by channel;
- percentage distribution by channel.

Exact days, time bands, observer ownership, and acceptable recording burden require Jaime validation.

### 12.3 Four-week pilot scorecard

Weekly reports are accessible only to Jaime and people he explicitly authorises.

Exporting order lists, telephone numbers, reports, or other commercial or operational information requires Jaime or a person with explicit export authority.

Jaime receives a weekly summary containing:

- orders by channel;
- peak periods;
- incidents;
- delays;
- average order value separately for web, telephone, and in-person orders;
- best-selling products;
- frequent product combinations.

Evaluate the pilot after four complete weeks, paying special attention to Friday, Saturday, and Sunday.

Required success dimensions:

1. **Reliability**
   - no accepted order is lost;
   - no accepted order reaches the kitchen too late to be fulfilled reasonably;
   - alerts and order reception remain operational.

2. **Adoption**
   - weekly web-order volume;
   - movement from telephone ordering toward web ordering.

3. **Operational value**
   - Jaime considers the system clearly more useful than handling all orders by telephone;
   - opening time, closing time, and correction count are measured;
   - Jaime's qualitative assessment is recorded;
   - incidents and manual interventions remain reviewable.

4. **On-time performance**
   - delayed-order count;
   - percentage prepared within the promised pickup window;
   - average delay.

5. **Commercial observation**
   - channel-specific average order value;
   - best-selling products;
   - frequent combinations;
   - upselling exposure and response where rules are validated.

6. **Controlled progression**
   - the next capability is selected only after reviewing data, incidents, workload, and staff experience.

Thresholds for sufficient adoption and call reduction remain pending the real baseline and Jaime's validation.

### 12.4 Controlled pilot rollout

Initial rollout direction:

- start on a Wednesday or Thursday under lower operational pressure;
- first live segment lasts approximately one hour;
- begin with a small set of informed regular customers;
- keep all web orders in `MANUAL_REVIEW`;
- do not enable `AUTO_ACCEPT` until staff have validated:
  - operating hours;
  - capacity;
  - alerts and acknowledgement;
  - stock and availability;
  - order reception;
  - order handling.

Before accepting real pilot orders, run a complete operational rehearsal including:

- web, telephone, and in-person orders;
- alerts and acknowledgement;
- delays and revised estimates;
- sold-out products and stock conflicts;
- connection loss and recovery;
- payment and handover;
- shift close.

### 12.5 Pilot pause and rollback

Pause the pilot when a critical failure occurs, including:

- an accepted order is missing;
- an accepted order appears too late for reasonable fulfilment;
- alerts repeatedly remain unattended;
- allergen or dietary information is incorrect.

A single manageable delay does not automatically require a pause.

Transition from `MANUAL_REVIEW` to `AUTO_ACCEPT`, rollback from automatic acceptance, and expansion to the full service schedule require explicit validated criteria.

### 12.6 Candidate operational metrics

Additional candidate MVP metrics:

- orders per day and hour;
- average order value;
- products sold;
- category mix;
- items per order;
- order acceptance time;
- preparation time;
- cancellation and rejection counts;
- product unavailability frequency;
- upsell conversion for drinks, desserts, or packs;
- order volume and value by source channel;
- telephone-order volume before and after web launch;
- manual capacity overrides;
- payment method actually collected;
- payment failures and corrections;
- non-payment incidents;
- stock differences attributable to unregistered telephone or in-person sales;
- mistaken paid-state reversals;
- handover corrections;
- expected-versus-actual cash difference;
- unresolved open orders at shift close;
- opening and closing workload;
- pilot pause events and causes;
- accepted orders not received on time by the kitchen;
- personal-data requests by type and resolution status, without exposing request content in routine analytics.

Product-margin reporting is explicitly deferred until Dopis has validated product-cost data.

### 12.7 MVP upselling

Upselling is included in the first operational MVP.

#### Commercial configuration

Jaime manually defines:

- recommended products for each pizza;
- priority order.

Jaime or an explicitly authorised responsible person may maintain the relationships.

Initial eligible recommendation types:

- drinks;
- desserts;
- compatible pizza extras.

The MVP does not include:

- discounts;
- dynamic pricing;
- automatic promotions;
- recommendation inference from sales;
- random recommendations;
- automatic addition to the cart;
- automatic quantity increases.

A pizza without configured active relationships produces no recommendation.

Upselling may be disabled:

- globally;
- for an individual source product;
- without removing recommended products from the menu.

#### Customer presentation

Recommendations may appear:

- after a pizza is added;
- once during cart review.

At most three relevant recommendations appear across the whole cart.

The customer may add one through a simple action or ignore it without explicit rejection. Upselling must not block, delay, or make checkout materially harder.

For carts with multiple pizzas:

- merge configured relationships;
- remove duplicates;
- apply configured priority;
- retain one overall maximum of three;
- do not infer larger quantities.

A recommendation already in the cart or ignored in the current checkout is not repeated.

#### Operational and safety constraints

A recommendation is eligible only when:

- the recommended product is published;
- allergen information is complete;
- the product is active and currently available;
- stock remains sufficient;
- temporal validity remains active;
- the result is compatible with the customer's selected dietary configuration;
- adding it passes normal capacity validation where applicable.

The recommendation displays the same allergen and dietary information as its normal menu presentation.

If a later pizza modification makes an already-added recommendation incompatible, warn the customer and let them decide whether to retain or remove it. Never remove the product silently.

#### Pilot measurement

Measure in aggregate:

- recommendation impressions;
- recommendation additions;
- addition rate;
- placement: post-pizza or cart review;
- checkout completion with and without recommendation exposure;
- relevant complaints or operational errors.

Do not associate recommendation analytics with persistent individual customer profiles.

No minimum conversion target is fixed before pilot evidence exists.

Retain upselling after the pilot only when:

- it increases additions to the cart;
- it does not create relevant complaints or operational errors;
- it does not produce an appreciable fall in checkout completion.

Exact recommendation relationships, authorised editors, dietary-compatibility rules, and success or shutdown thresholds require Jaime validation.
Future business capabilities:

- customer registration;
- loyalty points;
- packs and bundles;
- birthday benefits;
- segmented campaigns;
- SEO landing pages;
- copy experiments;
- conversion funnel measurement;
- cohort and retention analysis.

Metrics should be driven by specific business questions, not collected without purpose.
---

## 13. Development and deployment environments

### 13.1 Current frontend environment

The current Vue 3 + Vite frontend:

- lives under `frontend/`;
- builds with `npm ci` and `npm run build`;
- uses GitHub Pages for the current public demo;
- deploys only from `main`;
- may validate builds from feature branches while skipping production deployment;
- remains a frontend prototype with mock catalog and order data.

GitHub Pages is suitable for the current static demo. It is not the final hosting decision for the operational product.

### 13.2 Proposed local operational environment

Initial backend and integration testing may run on the Project Owner's computer.

Proposed local stack:

```text
Vue 3 frontend
FastAPI backend
PostgreSQL
Docker Compose
```

Optional development-only additions:

- Adminer or pgAdmin;
- seed scripts;
- an SMS provider adapter with a local fake implementation;
- Mailpit only if email is introduced;
- local object storage only if product-image management requires it.

### 13.3 Environment boundary

The local environment is not production.

Production readiness requires separate decisions and gates for:

- domain and DNS;
- TLS;
- backend and database hosting;
- secrets;
- backups and restoration tests;
- monitoring and alerting;
- log retention;
- availability;
- SMS provider;
- privacy notices and retention;
- deployment and rollback;
- operational fallback.

The current GitHub Pages deployment must not be mistaken for operational backend readiness.

---

## 13.4 Operating-hours and pizza-service model

Business opening hours and pizza-ordering hours are distinct configuration concepts.

Confirmed weekly baseline:

- Monday and Tuesday: closed.
- Wednesday and Thursday: premises open from 18:00 to 22:00.
- Friday, Saturday, and Sunday: premises open from 18:00 to 23:00.
- Pizza ordering begins at 19:00.
- Earliest pizza pickup is 19:15.
- Initial latest pickup is 21:45 on Wednesday and Thursday.
- Initial latest pickup is 22:45 on Friday, Saturday, and Sunday.
- Initial launch accepts same-day orders only.

The system must configure separately:

- premises opening time;
- premises closing time;
- online pizza-ordering start time;
- earliest pickup time;
- latest pickup time;
- minimum lead time;
- final order-submission time;
- day-specific schedules;
- date-specific exceptions;
- manual pause/resume;
- temporary delay;
- blocked pickup windows.

Recommended operating-hours administration:

1. A weekly default schedule.
2. Date-specific closure, exceptional opening, special hours, and special capacity.
3. Manual online-ordering pause and resume.
4. Temporary global delay applied to new estimates.
5. Blocking or capacity reduction for individual pickup windows.
6. Separate pizza-service hours from the premises' broader opening hours.

The final order-submission opportunity must be derived dynamically from the latest permitted pickup, minimum lead time, basket workload, remaining capacity, and temporary delays rather than assumed to equal the premises closing time.

Online orders open only after staff complete the readiness checklist and explicitly select `Open orders`.

## 14. Main risks

| Risk | Consequence | Current mitigation direction |
|---|---|---|
| Panel accessible without real backend authorisation | Exposure or manipulation of orders | Implement functional staff authentication from the first operational backend |
| Tablet misses an order | Lost revenue and customer dissatisfaction | Sound, live updates, connection indicator, manual refresh, operational fallback |
| Tablet alert is inaudible in a noisy kitchen | Order remains unseen | Persistent highlight, explicit acknowledgement, repeated alert, safety pause, real-device testing |
| Panel loses connectivity | Staff act on stale information or unseen orders arrive | Stale indicator, blocked writes, mobile backup, timed pause, manual resume |
| Telephone-based incidents unfairly affect future orders | Privacy and fairness harm | Correction trail, limited working risk window, manual review, no automatic block |
| Shared access is mistaken for individual attribution | Misleading audit history | Record the shared kitchen session and current responsible person accurately |
| Permission hierarchy exceeds the real two-person operation | Unnecessary complexity and configuration errors | Use principal, delegated, and bounded operational access rather than a broad hierarchy |
| Delegated authority is expired or absent at opening | Service runs without accountable responsibility | Validate delegation scope and block online opening |
| Temporary service adjustment becomes permanent policy | Delegated action exceeds authorised scope | Store current-service scope and reserve permanent policy changes to Jaime |
| Sensitive catalog data is validated without evidence | Incorrect allergen or dietary information | Require reliable documentation and responsible review |
| Delegate improvises an unsupported substitution | Safety, pricing, or customer-dispute risk | Enforce specific relationships or approved category and price rules |
| Absorbed price differences are unbounded | Inconsistent financial decisions | Configure a fixed per-order maximum approved by Jaime |
| Retention periods remain undefined at public launch | Personal data is retained indefinitely | Treat approved legally reviewed periods as a launch gate |
| Discovery continues through repetitive numeric interviews | Delay without new business-rule value | Consolidate unresolved numbers into one bounded validation register |
| Shared kitchen access exposes administration | Temporary or operational staff change sensitive data | Limit shared sessions to operational functions only |
| Shift lead can change access permissions | Privilege expansion without owner control | Reserve authorisation, revocation, and permission changes to Jaime |
| Departing staff retain access | Unauthorised access after employment | Revoke access before the next service and review when personnel change |
| Reports or telephone lists are broadly exportable | Commercial and personal data leave controlled use | Restrict viewing and export authority and audit exports |
| Sensitive catalog edits overwrite prior values | Incorrect content cannot be reconstructed | Retain previous value, new value, actor, and timestamp |
| Incident is hidden to permit shift close | Material unresolved decision is lost | Allow safe close with a visible `Pending Jaime` record |
| Prepared-order cancellation lacks loss recording | Operational waste and responsibility are unclear | Require reason and operational-loss record |
| Uncontrolled substitution changes published pricing | Customer disputes and catalog inconsistency | Record incident resolution without modifying the original published price |
| Incorrect incident resolution cannot be revisited | Permanent operational or customer-history error | Permit linked reopening with preserved history |
| Product availability is inaccurate | Orders cannot be fulfilled | Start with simple availability controls and define ownership |
| Physical stock differs from a valid reservation | Accepted order cannot be fulfilled as configured | Route to `Requires attention`; offer allowed alternative or cancel manually |
| Telephone or in-person orders bypass shared stock and capacity | Overbooking and stock discrepancies | Require every order channel to use the same operational system |
| Manual capacity override becomes routine | Pickup promises become unreliable | Restrict override to responsible staff, require explicit acknowledgement, and measure usage |
| In-person telephone collection is excessive | Slower service and unnecessary personal-data collection | Validate necessity with Jaime and minimise data where operationally possible |
| Payment and handover are collapsed into one action | Unpaid orders may be released or audit becomes unclear | Keep paid and handed-over events separate |
| Payment method or delivery is corrected without traceability | Cash and order history become unreliable | Restrict correction authority and retain audit events |
| Cash discrepancy is not reviewed at shift close | Repeated accounting errors remain unexplained | Compare expected and actual cash and require responsible confirmation |
| Telephone numbers are visible throughout kitchen operations | Unnecessary personal-data exposure | Hide by default and reveal only through `Contact customer` |
| Caller is identified only by telephone number | Order information may be disclosed to the wrong person | Also verify customer name or order identifier |
| Operational telephone data is reused for marketing | Invalid consent and loss of trust | Separate optional explicit consent, unchecked by default |
| Incident summaries expose excessive history | Staff see more personal context than needed | Default to minimal relevant summary and controlled detail access |
| Data requests are handled informally during service | Incorrect disclosure, deletion, or missed request | Route to Jaime through a documented process |
| Staff sessions remain active after shifts or employment | Unauthorised later access | Shift-end sign-out, responsibility handover, and account deactivation |
| Pilot starts without a reliable baseline | Call-reduction claims cannot be evaluated | Record two complete weeks before activation and set targets afterward |
| Accepted order is missing or reaches kitchen too late | Revenue loss and broken customer trust | Treat as critical reliability failure and pause the pilot |
| Automatic acceptance is enabled before operations are proven | Orders may bypass unresolved capacity, stock, or alert failures | Begin in manual review and require explicit promotion criteria |
| Pilot expands too quickly | Peak-service failures are harder to isolate | Start with a one-hour lower-pressure session and informed regular customers |
| Opening and closing workload is assumed rather than measured | Staff burden may make the system unsustainable | Measure during the four-week pilot before fixing limits |
| A single manageable delay triggers unnecessary shutdown | Pilot evidence is interrupted by normal variation | Distinguish isolated manageable delay from critical repeated failure |
| One launch language is incomplete or unreviewed | Customers receive inconsistent or misleading content | Block publication until Spanish and Catalan text is complete and approved |
| Automatic translation is published without review | Incorrect product or allergen communication | Require human validation before publication |
| Temporary or service-hidden product remains orderable | Customer orders an unavailable commercial offer | Enforce date and service visibility at add-to-cart and confirmation |
| Featured products bypass stock or safety constraints | Commercial presentation overrides operational rules | Apply stock, availability, allergen, and publication gates before ranking |
| Upselling recommendation is unavailable or unpublished | Customer cannot add the advertised item | Filter at display and revalidate through the ordinary add-to-cart path |
| Upselling conflicts with the selected dietary configuration | Unsafe or misleading recommendation | Require compatibility filtering and show normal allergen information |
| Recommendation is repeatedly shown after being ignored | Checkout becomes intrusive | Suppress ignored recommendations for the current checkout |
| Multi-pizza cart produces duplicates or excessive prompts | Customer friction and clutter | Deduplicate, prioritise, and cap at three overall |
| Later pizza changes make an added recommendation incompatible | Cart becomes inconsistent | Warn the customer and require an explicit keep-or-remove decision |
| Upselling reduces checkout completion | Commercial optimisation harms the primary MVP goal | Compare aggregate exposure, additions, completion, complaints, and errors during the pilot |
| Product-margin reporting uses unvalidated costs | Misleading profitability decisions | Defer margin calculation until cost data are reliable |
| Unauthorised reactivation exposes unavailable items | Repeated fulfilment failure | Allow broad disablement but restrict reactivation to responsible staff |
| Stock counting creates excessive operational burden | Staff bypass or falsify the process | Limit counts to relevant items and reevaluate closing counts from observed reliability |
| Shared ingredient depletion disables too many products | Unnecessary lost sales | Model configuration-level dependency rather than blanket product shutdown |
| Estimated replenishment reopens an item prematurely | Customer orders unavailable stock | Keep return time informational; require manual confirmation |
| Gluten-free messaging overstates safety | Health risk and misleading customer communication | Validated allergen matrix, cross-contact warning, no coeliac or severe-allergy suitability claim before approval |
| Product or supplier changes bypass allergen review | Outdated safety information remains online | Disable affected item until ingredients, traces, allergens, and labels are revalidated |
| Free-text notes request unsupported ingredient changes | Kitchen ambiguity and incorrect allergen result | Restrict notes and enforce configured modifiers as authoritative |
| Unauthorised catalog changes alter safety information | Incorrect dietary or allergen claims | Authorised approval and auditable change history |
| Free-text notes bypass configured modifiers | Ambiguous or unsafe kitchen requests | Short constrained notes only; configured modifiers remain authoritative |
| Delay-response workflow creates an unattended queue | Customer request remains unresolved | Ten-minute response window, manual-review routing, visible `Requires attention` queue |
| Compensation is implemented before business approval | Scope expansion and inconsistent commercial treatment | Keep compensation conditional until Jaime validates inclusion, limits, and policy |
| Customer receives premature confirmation | Kitchen may be unable to fulfil | Separate received and accepted states |
| Future payment support forces redesign | Rework and payment inconsistencies | Model payment method/status now, integrate provider later |
| Excessive customer data is collected | Privacy and security risk | Separate operational, loyalty, and marketing purposes |
| Local test setup is mistaken for production readiness | Downtime or security issues | Explicit environment separation and deployment gate |
| MVP expands into loyalty, SEO, inventory, and marketing simultaneously | Delayed usable release | Phase capabilities and protect the operational order slice |

---

## 15. Open decisions — discovery backlog

### Order operation

Resolved direction:

- automatic confirmation is the normal mode;
- manual review and paused ordering are staff-controlled modes;
- in manual mode, staff may accept the requested slot, reject the order, or propose an alternative slot;
- staff cancellation is required;
- customer self-service cancellation is deferred;
- earliest-available and scheduled pickup should both use deterministic capacity rules;
- a five-minute provisional checkout hold is the initial configurable value;
- acceptance is shown on the web rather than sent as a redundant SMS;
- one initial SMS provides secure tracking access, followed by SMS only for ready, rejection, or staff cancellation.

Still open:

- exact wording and retry behaviour for the initial tracking, ready, rejection, and cancellation SMS messages;
- exact cancellation reasons and customer communication;
- capacity-point values and the initial calibration method;
- the initial large-order manual-review threshold percentage;
- whether and when a later release may automatically distribute large orders across consecutive pickup windows;
- the exact minimum lead-time calculation and calibration;
- how staff should handle an expired alternative proposal when direct customer contact has already occurred;
- whether the provisional two-incidents-in-90-days rule is operationally appropriate;
- the full retention period and correction process for operational incidents;
- the exact grace-period and pickup-extension settings after validation with Jaime.
- the exact threshold for an important delay and a material estimate revision;
- whether the initial ten-minute customer delay-response window is operationally appropriate;
- whether and when repeated estimate changes require additional SMS messages;
- the final resolution policy when the customer rejects a delay after preparation has started;
- whether compensation belongs in the MVP at all;
- if promoted, compensation types, limits, expiry, revocation, redemption, and evidence requirements.

### Tablet and notifications

Resolved direction:

- audible alert, persistent visual highlighting, automatic updates, and connection status are required;
- new orders require explicit acknowledgement;
- repeated alerts and a safety pause protect against unattended orders;
- a mobile device provides limited operational backup;
- the initial launch does not require a printer;
- a printer may be promoted only after real operational testing;
- the digital panel remains the source of truth.

Still open:

- which physical tablet, browser, placement, and sound level will be used;
- the timeout before an unacknowledged order pauses automatic acceptance;
- whether staff use individual identities or shared operational access;
- session lifetime and re-authentication behaviour;
- screen wake and kiosk-mode behaviour;
- the simultaneous tablet, mobile, network, and backend failure procedure;
- the test criteria that would promote a ticket printer.

### Catalog and inventory

Resolved direction:

- weighted integer production points are required from the first operational version;
- products and eligible modifiers may contribute different production points;
- individual product and modifier point values are initially maintained as technical configuration;
- Jaime controls operational capacity totals and temporary capacity changes;
- pickup windows initially last 15 minutes;
- orders above a configurable percentage of window capacity require manual review;
- orders that cannot fit safely in one window also require manual review in the MVP;
- advance-order horizon is configurable;
- stock is provisionally held during checkout and manual review, then committed or released transactionally;
- operating hours, pizza-service hours, earliest pickup, latest pickup, and lead time are configured separately;
- one pizza size;
- no half-and-half pizzas initially;
- configurable removals, substitutions, and paid extras;
- gluten-free dough option across pizzas;
- product availability plus unit stock for countable products;
- broad protected catalog CRUD for Jaime;
- any authorised staff member may disable stock or availability;
- only Jaime or the responsible shift lead may reactivate pizzas, critical ingredients, or options;
- countable opening stock acts as a strict sales ceiling;
- stock changes are auditable and reason-coded;
- daily limits and approximate-use counts may apply to selected limited items;
- shared ingredients disable only dependent configurations;
- no automatic substitution or estimated-time reactivation;
- provisional closing reconciliation;
- precise recipe-level inventory deferred.

Still open:

- the exact modifier matrix for every pizza;
- price of each extra or substitution;
- whether gluten-free dough changes price;
- the exact allergen and cross-contact wording;
- whether any pizza has a daily product-specific limit;
- who records stock deliveries, corrections, and waste;
- whether modifiers require independent stock;
- whether image upload belongs in the first admin interface;
- whether removing ingredients always preserves price;
- the permitted substitution matrix by pizza;
- free versus paid substitutions and the price delta for vegan mozzarella;
- maximum quantity for each extra;
- permitted kitchen-note exceptions;
- supplier information for gluten-free dough;
- exact gluten cross-contact wording and whether explicit acknowledgement is required;
- the complete allergen matrix for products and modifiers;
- how substitutions change allergen and vegan/vegetarian labelling;
- when staff must disable gluten-free dough because the validated procedure cannot be followed;
- who besides Jaime may approve dietary and allergen information;
- the exact provider-document review procedure;
- which non-ingredient instructions and authorised exceptions may use free-text notes;
- whether every product without documentary allergen verification must remain offline at launch;
- who normally performs opening and closing counts;
- which drinks, desserts, and limited products require mandatory counts;
- whether closing reconciliation is daily or product-specific;
- which pizzas require daily limits;
- which ingredients and options belong to the critical opening checklist;
- how approximate available uses are estimated for vegan mozzarella, gluten-free dough, and similar items;
- which products may be replenished during service;
- which stock-adjustment reasons match real staff practice;
- which products or options may vary by pickup window;
- how expected reactivation is communicated to customers;
- how telephone and walk-in sales affect online stock and capacity;
- whether remaining stock carries between service days or is recounted;
- low-stock warning policy;
- how reliability is measured before removing redundant counts;
- which products carry stock between service days and which require recounting;
- how retained, discarded, and corrected perishable quantities are recorded;
- low-stock thresholds and warning behaviour by product;
- how manual, telephone, and in-person orders are entered during peak service.

### Catalog content and presentation

- who besides Jaime may administer ordinary products and content;
- final Spanish and Catalan names and descriptions;
- initial category and product order;
- launch featured products;
- first temporary products and active dates;
- available launch photography;
- whether ticket-printer reliability is required after rehearsal;
- formal compensation policy;
- cost data required for future margin reporting.

### Manual channels, payment, and handover

- who normally enters telephone and in-person orders;
- whether every in-person order genuinely requires a telephone number;
- when a responsible operator may override calculated capacity;
- exact receipt issue and retention practice;
- detailed permissions for payment and handover corrections beyond the accepted baseline;
- how cash discrepancies are investigated and when escalation is required;
- whether any exceptional unpaid handover is allowed and who authorises it;
- how an erroneous handover is corrected;
- which channel metrics Jaime needs to evaluate whether the web reduces calls;
- current cash-register, receipt, and end-of-shift procedures;
- future refund rules before and after preparation when online payments are introduced;
- future criteria for requiring prepayment after repeated incidents.

### Shift authority and incident escalation

- which operational exceptions the delegate may approve without contacting Jaime;
- which decisions always require Jaime;
- the initial specific substitution relationships;
- validated fallback substitution rules by category or price;
- the fixed per-order amount the delegate may absorb;
- which measures count as operationally safe when Jaime is unavailable;
- how and when Jaime receives the pending-decision summary;
- which validations block the pilot;
- which validations block only public launch;
- which pending validations block formal discovery closure.

### Customers and privacy

- Is the telephone number only for order contact?
- When will customer accounts be introduced?
- Which future marketing channel is preferred?
- What constitutes explicit loyalty enrolment?
- Is a birthday benefit important enough to collect birth information?
- How long should identified orders, telephone numbers, incidents, payment records, and audit events be retained?
- What exact procedure and identity checks will Jaime use for access, correction, or deletion requests?
- Which accounting or legal records must remain identifiable?
- Which data can be anonymised while preserving useful metrics?
- Who is the delegated responsible person?
- Is delegated authority stable or limited to defined shifts or dates?
- Which exceptional actions remain outside delegated authority?
- What exact onboarding, revocation, and access-review procedure will Jaime use?
- When must the shared kitchen session be replaced by individual operational identities?
- How is the tablet physically protected outside service hours?
- Which operational incidents may affect manual review?
- How long should incident data be retained beyond the provisional 90-day risk window?
- How are incorrect incidents corrected and communicated?
- How should invalid telephone numbers be treated without unfairly penalising customers?

### Pending external validation — Jaime

The detailed validation register will be created as a structured artifact for the stakeholder-validation workflow. Until then, the canonical discovery tracks these current validation gates:

- `JV-CAPACITY`: production points, capacity templates, and preparation timing;
- `JV-DELAYS`: serious-delay thresholds, customer-contact rules, and delay-response timing;
- `JV-COMPENSATION`: whether compensation belongs in the MVP and, if so, its permitted types and limits;
- `JV-MODIFIERS`: allowed removals, substitutions, extras, limits, and pricing;
- `JV-GLUTEN`: supplier information, actual kitchen procedure, cross-contact wording, and online offer policy;
- `JV-ALLERGENS`: complete product and modifier ingredient, allergen, and trace information;
- `JV-CATALOG-APPROVAL`: authorised approvers, supplier-change review, and publication gates;
- `JV-STOCK`: opening and closing counts, critical ingredients, daily limits, carry-over, perishables, replenishment, adjustment reasons, and physical-sales reconciliation;
- `JV-MANUAL-ORDERS`: telephone and in-person entry, required customer data, manual capacity overrides, and channel workflow;
- `JV-PAYMENT`: cash/card operation, optional receipts, correction authority, non-payment, handover, cash discrepancies, and shift-close procedure;
- `JV-PRIVACY`: operational notice, anonymisation, data requests, staff visibility, and lawful record preservation;
- `JV-LEGAL-RETENTION`: legally reviewed periods for identified orders, telephones, incidents, payment records, audit history, and SMS records before public launch;
- `JV-DELEGATION`: named delegate, authorisation duration or shift scope, opening responsibility, administrative authority, reporting and export access, and boundary between temporary adjustment and permanent policy;
- `JV-ACCESS`: Jaime-only access management, onboarding, revocation, review, shared kitchen session, mobile-backup limits, and physical tablet protection;
- `JV-PILOT`: baseline burden, launch timing, participant group, observer ownership, weekly reporting, manual-review evidence, automatic-acceptance criteria, pause and rollback rules, expansion, and success thresholds;
- `JV-CONTENT`: authorised editors, Spanish and Catalan copy, category order, featured and temporary products, and launch photography;
- `JV-UPSELL`: concrete relationships, priority, authorised editors, dietary compatibility, excluded products, checkout-impact threshold, and post-pilot success threshold;
- `JV-THRESHOLDS`: one bounded list of large-order, delay, response, extension, alert, escalation, and absorbed-price-difference values;
- `JV-DISCOVERY-CLOSE`: pilot blockers, public-launch blockers, remaining material Jaime validations, and explicit first-MVP exclusions;
- `JV-SHIFT-AUTHORITY`: permitted exceptions, prepared-order cancellation, approved substitution rules, price-difference handling, safe isolation measures, escalation, reopening, and Jaime review channel;
- `JV-COHERENCE`: final cross-domain contradiction and consistency review before formal discovery closure.

These references are validation gates, not replacements for the future structured register.

### Business outcomes and pilot

Resolved direction:

- the first-month priority is reducing order-related calls during peak periods;
- a two-week baseline precedes pilot activation;
- the pilot runs for four complete weeks;
- weekly web orders and channel shift measure adoption;
- no accepted order may be lost or reach the kitchen materially too late;
- Jaime's judgement of operational usefulness is required;
- opening and closing workload is measured during the pilot;
- initial web orders use manual review;
- automatic acceptance requires validated operational criteria;
- critical reliability or allergen failures pause the pilot.

Still open:

- exact baseline days and time bands;
- who records and reviews daily baseline and pilot evidence;
- which regular customers participate in the first live segment;
- exact Wednesday or Thursday launch date;
- sufficient weekly web-order adoption threshold;
- valuable call-reduction threshold after baseline;
- number and variety of manually reviewed orders required before `AUTO_ACCEPT`;
- exact rollback criteria from automatic acceptance;
- conditions for expanding the pilot to the full service schedule;
- acceptable opening and closing workload;
- exact set of material Jaime validations required before initial discovery closure;
- exact boundary of capabilities remaining outside the operational MVP;
- concrete pizza-to-drink, dessert, and extra recommendation relationships for the pilot;
- priority order for each recommendation group;
- exact authorised people who may edit commercial relationships;
- dietary-compatibility rules for every relevant configuration;
- products for which upselling remains disabled;
- threshold defining an appreciable reduction in checkout completion;
- minimum result Jaime requires to retain upselling after the pilot;
- which combinations should become later packs;
- future product-margin requirements after cost validation.

### Technical reference project

Assessment status: completed read-only.

Verified findings:

- the archive contained a Vue/Vite/Router/Pinia frontend;
- it also contained committed `node_modules`;
- the backend was available only as a large bundled/minified artifact and was not suitable as maintainable source architecture;
- useful concepts were extracted without authorising code reuse;
- the archive remains local and ignored by Git;
- the tracked `docs/reference-project/README.md` records its purpose and custody policy.

This item is closed as an assessment task. Future use must refer to the accepted and rejected patterns recorded in Section 4.3.

---

## 16. Phase sequence and current progress

### Phase 0A — repository and evidence baseline — COMPLETED

Completed:

- inspected the current frontend;
- established documentation custody;
- archived the initial PRD and handoff;
- catalogued current product-source files;
- assessed the university reference project read-only;
- selected a monorepo structure;
- moved the frontend into `frontend/`;
- updated and validated GitHub Pages deployment;
- recorded the current FastAPI recommendation.

### Phase 0B — business discovery substantially complete; architecture discovery in progress

Remaining:

- stop broad business-interview expansion and prepare bounded Jaime validation;
- normalise and validate the real menu;
- confirm operating hours and date exceptions;
- calibrate production-point rules;
- validate stock-counting burden, critical-item allowances, daily limits, carry-over, perishables, replenishment, and reconciliation with telephone or walk-in sales;
- validate manual order-entry roles, in-person telephone collection, payment correction, handover, optional receipts, cash discrepancies, and cash-close procedures;
- define privacy notice, retention, anonymisation, data-request handling, operational access, session closure, and staff-account deactivation with Jaime and legal review;
- validate the two-week baseline, weekly report, four-week pilot scorecard, controlled rollout, manual-to-automatic promotion, rollback, pause, and expansion criteria with Jaime;
- validate bilingual content ownership, launch copy, product presentation, featured and temporary products, photography, concrete upselling relationships, compatibility, permissions, and pilot thresholds;
- confirm the material gates required to close initial discovery and the explicit first-MVP exclusions;
- validate tablet placement, alert audibility, mobile backup, and printer-reconsideration criteria;
- close modifier pricing, kitchen-note boundaries, gluten cross-contact wording, supplier evidence, catalog approval, and the complete allergen matrix with Jaime;
- validate the delegated responsible person, authorisation scope, Jaime-only access management, report/export authority, shared kitchen attribution, mobile-backup permissions, and revocation procedure;
- validate delegated exceptions, explicit and fallback substitution rules, absorbed-price limit, safe isolation measures, escalation, incident reopening, and Jaime's review channel;
- validate the bounded operational threshold register;
- complete legal review of privacy procedures and retention periods;
- perform the final cross-domain coherence review;
- decide staff authentication UX;
- decide SSE versus WebSockets;
- define SMS abstraction, retry behaviour, repeated-delay messaging, and customer delay-response handling;
- define incident retention, correction, and fairness controls;
- decide whether compensation belongs in the MVP and define exact MVP catalog administration;
- freeze the operational MVP;
- create architecture decision records;
- define API and database contracts.

### Phase 1 — local operational backend

After explicit implementation authority:

- modular FastAPI scaffold;
- PostgreSQL schema and Alembic migrations;
- menu API and validated initial import;
- guest order creation;
- protected staff login;
- scheduling and capacity engine;
- transactional stock and capacity holds;
- tablet order queue;
- order status transitions;
- SMS abstraction;
- local Compose environment;
- automated tests.

### Phase 2 — launch readiness

- two-week channel and call baseline;
- complete operational rehearsal;
- one-hour lower-pressure controlled launch;
- initial manual-review operation;
- validated promotion and rollback criteria for automatic acceptance;
- four-week pilot measurement and review;
- weekly pilot reporting;
- bilingual content readiness;
- validated menu presentation and bounded upselling configuration;
- production hosting;
- domain and TLS;
- backups and restoration tests;
- monitoring and alerting;
- secure secret management;
- privacy notices and retention process;
- operational fallback;
- production analytics baseline.

### Phase 3 — online payments

- provider selection;
- payment-intent lifecycle;
- webhook verification;
- reconciliation;
- refunds and failures;
- customer-facing payment states.

### Phase 4 — growth capabilities

- registered customers;
- loyalty points;
- packs;
- birthday rewards;
- marketing consent and campaigns;
- business dashboard;
- SEO and conversion optimisation.

---

## 17. Current recommendation and authorised next sequence

Do not begin backend business implementation yet.

The repository audit, documentation custody, frontend migration, and GitHub Pages validation are complete. The next work is no longer repository reorganisation.

Recommended sequence:

1. Install this reconciled version as the canonical document.
2. Prepare a bounded Jaime validation package covering delegation, thresholds, substitutions, catalog and allergen evidence, pilot gates, and launch gates.
3. Complete legal privacy and retention review and a final cross-domain coherence review.
4. Create and review ADRs for:
   - monorepo architecture;
   - provisional FastAPI selection;
   - weighted pickup-capacity windows;
   - secure guest tracking;
   - transactional stock and capacity holds.
5. Transcribe product-source material into a draft structured catalog.
6. Validate the catalog, modifiers, prices, allergens, and operating hours with Jaime.
7. Draft the MVP requirements baseline.
8. Draft the API contract and database schema.
9. Draft a bounded backend-scaffold plan.
10. Grant separate implementation authority only after those artifacts are reviewed.

### 17.1 Cross-chat synchronisation protocol

The repository is the source of truth; no chat is authoritative by itself.

Canonical path:

`docs/current/DOPIS_TECHNICAL_DISCOVERY.md`

The business-discovery chat should accumulate answers and produce a delta checkpoint when the first of these occurs:

- approximately 15–20 questions have been answered;
- five material decisions have been closed;
- a previous decision is contradicted;
- scope, domain model, or operating rules change materially.

Each checkpoint should contain only:

1. confirmed new decisions;
2. provisional decisions;
3. modified or revoked decisions;
4. affected canonical sections;
5. proposed entities or fields;
6. unresolved questions;
7. recommended changelog text.

The integration workflow is:

```text
business discovery
    -> delta checkpoint
    -> compare with repository and ADRs
    -> reconcile conflicts
    -> update canonical document
    -> commit
    -> resume both chats from the committed baseline
```

A discovery chat must not independently increment the canonical version or authorise implementation.

---

## 18. External evidence considered

The scheduling recommendation was informed by current restaurant-ordering platform documentation that supports:

- preparation-time estimates;
- automatic pickup-time calculation;
- capacity limits per pickup window;
- removal of full future slots;
- extension of earliest-available time when near-term capacity is full;
- temporary staff throttling, delays, and online-order pauses.

Sources reviewed on 2026-07-24:

- Square Support — pickup options and order limits per pickup window.
- Toast Platform Guide — quote-time strategies, kitchen-capacity throttling, and online ordering schedules.
- European Commission, AESAN, and BOE materials on allergen information and gluten-related consumer information.

These sources inform the discovery model; Dopis business rules still require validation with Jaime.

---

## 18A. Initial discovery closure criteria

First-MVP business discovery is substantially complete.

It may close formally when:

- the complete customer and staff operating flow remains coherent after cross-domain review;
- Jaime validates the named delegate and delegation scope;
- the bounded numerical threshold list is approved;
- substitution rules and the absorbed-price limit are approved;
- initial catalog content and allergen evidence are validated;
- pilot blockers and public-launch blockers are explicitly separated;
- privacy procedure and retention periods receive required legal review;
- every remaining material item has a clear owner and validation gate;
- unresolved implementation details do not imply implementation authority.

The following are not required to close first-MVP discovery:

- online payment;
- loyalty;
- advanced marketing;
- advanced analytics;
- validated product-margin reporting;
- automatic recommendation engines.

Upselling is included in the first MVP through manually configured relationships; automatic recommendation engines remain outside scope.

Further broad interview rounds are not required merely to choose already identified numerical values. Those values belong in the bounded validation package.

---

## 19. Change log

### 0.17 — 2026-07-25

- Reconciled `BD-DELTA-013` against canonical version 0.16.
- Confirmed that normal MVP operation is primarily Jaime plus one worker who assumes delegated responsibility.
- Revoked the extensive first-MVP permission hierarchy and simplified it to principal, delegated, bounded operational, and shared-kitchen access.
- Added stable or shift/date-bounded delegation and blocked online opening without Jaime or an authorised delegate.
- Granted the delegate near-equivalent normal operational, catalog, allergen, dietary, reporting, export, publishing, incident, and current-service authority.
- Preserved Jaime-only access management, permanent policy, legal, exceptional, opening-hours, and normal-capacity decisions.
- Added safe isolation of affected capabilities when Jaime is unavailable.
- Added explicit and category/price fallback substitution rules plus a fixed absorbed-price limit.
- Made legally reviewed retention periods a public-launch gate.
- Consolidated outstanding numerical values into a bounded threshold register.
- Marked business discovery substantially complete pending Jaime validation, legal review, and final coherence review.
- Added `JV-DELEGATION`, `JV-LEGAL-RETENTION`, `JV-THRESHOLDS`, and `JV-COHERENCE`.
- Preserved implementation authority as `NOT GRANTED`.

### 0.16 — 2026-07-25

- Reconciled `BD-DELTA-012` against canonical version 0.15.
- Defined operational, shift-lead, authorised-manager, owner-admin, and common-kitchen access boundaries.
- Reserved staff access creation, revocation, and permission changes to Jaime.
- Restricted temporary staff, mobile backup, and common kitchen sessions to bounded operational capabilities.
- Restricted weekly reports and commercial or personal-data exports to explicitly authorised people.
- Added append-only auditing for availability, stock, prices, text, sensitive configuration, and corrective changes.
- Added explicit shift-lead registration, responsibility handover, close review, and critical-alert escalation.
- Added `Pending Jaime` handling that permits safe shift close without hiding unresolved decisions.
- Added prepared-order cancellation, valid substitution, price-difference resolution, and incident-reopening rules.
- Expanded access, authority, export, audit, and incident risks and added `JV-SHIFT-AUTHORITY`.
- Preserved implementation authority as `NOT GRANTED`.

### 0.15 — 2026-07-25

- Reconciled `BD-DELTA-011` against canonical version 0.14.
- Promoted bounded upselling into the first operational MVP.
- Limited recommendations to normal-price drinks, desserts, and compatible extras.
- Defined manual relationship and priority configuration without random, inferred, discounted, or automatically added products.
- Added global and source-product enablement controls.
- Added post-pizza and cart-review presentation with one overall maximum of three recommendations.
- Added multi-pizza merge, deduplication, ignored-item suppression, and no automatic quantity increase.
- Required publication, allergen, dietary, stock, availability, temporal-validity, and capacity checks.
- Added explicit customer handling when later modifications make an added recommendation incompatible.
- Added aggregate, placement-aware pilot measurement without individual customer profiling.
- Refined `JV-UPSELL` to the remaining Jaime validations and preserved automatic recommendation engines outside scope.
- Preserved implementation authority as `NOT GRANTED`.

### 0.14 — 2026-07-25

- Reconciled `BD-DELTA-010` against canonical version 0.13.
- Confirmed that current frontend upselling elements are not themselves validated business requirements.
- Expanded Jaime's catalog administration while preserving restricted authority for safety-sensitive data.
- Added weekly pilot reporting, on-time performance metrics, operational workload measures, and explicit deferral of margin reporting.
- Kept the ticket printer outside initial scope and bounded the first SMS use cases.
- Allowed incident-level recording of agreed resolutions without assuming a compensation program.
- Added Spanish and Catalan launch content, browser-language selection, visible switching, Spanish fallback, and bilingual publication gates.
- Added category structure, manual ordering, featured products, temporary dates, service-specific hiding, sold-out visibility, and optional photography.
- Added bounded upselling discovery, constraints, risks, open questions, and the `JV-UPSELL` validation gate.
- Added explicit initial-discovery closure criteria and first-MVP exclusions.
- Added `JV-CONTENT` and `JV-DISCOVERY-CLOSE`.
- Preserved implementation authority as `NOT GRANTED`.

### 0.13 — 2026-07-25

- Reconciled `BD-DELTA-009` against canonical version 0.12.
- Confirmed that Dopis currently lacks a reliable channel baseline.
- Defined reduction of peak-period order calls as the first-month priority.
- Added a two-complete-week pre-pilot baseline and deferred numeric call-reduction targets until real evidence exists.
- Added a four-complete-week pilot scorecard covering reliability, adoption, operational usefulness, and staff workload.
- Defined missing or materially late accepted orders as critical reliability failures.
- Added a controlled Wednesday-or-Thursday launch, approximately one-hour first segment, and informed regular-customer group.
- Required initial manual review and explicit validation before enabling automatic acceptance.
- Added a complete pre-live operational rehearsal and critical pilot pause criteria.
- Added pilot metrics, risks, open decisions, rollout sequence, and the `JV-PILOT` validation gate.
- Preserved implementation authority as `NOT GRANTED`.

### 0.12 — 2026-07-25

- Reconciled `BD-DELTA-008` against canonical version 0.11.
- Confirmed optional receipt issuance and the common cash-discrepancy cause of card payments recorded as cash.
- Added auditable payment-method correction, responsible reversal of mistaken paid states, and reversible mistaken handover.
- Added expected-versus-actual cash reconciliation and responsible shift-close confirmation.
- Added an operational-purpose notice before collecting name and telephone number.
- Explicitly separated order contact data from customer accounts, commercial profiling, and future marketing consent.
- Added hidden-by-default telephone access through `Contact customer`, caller verification, and minimal operational-history visibility.
- Added a defined escalation path to Jaime for personal-data access, correction, and deletion requests.
- Added anonymisation direction, retention questions, minimal SMS content, shift-end sign-out, and responsibility handover.
- Added privacy, cash-control, session, and disclosure risks plus `JV-PRIVACY` and `JV-ACCESS` validation gates.
- Preserved implementation authority as `NOT GRANTED`.

### 0.11 — 2026-07-25

- Reconciled `BD-DELTA-007` against canonical version 0.10.
- Confirmed that Dopis currently accepts cash and card payments at the premises.
- Added web, telephone, and in-person orders to one shared stock, capacity, pickup-window, queue, and status model.
- Added fast manual order entry and explicit source-channel tracking.
- Added responsible-staff capacity override with explicit risk acknowledgement and auditability.
- Added product-level stock carry-over, opening recount, perishable closing treatment, and low-stock threshold capabilities.
- Kept online payment outside the first MVP while preserving future coexistence with pay-at-store.
- Separated actual payment collection from physical handover and added non-payment incident handling.
- Added collector identification by customer name and order number.
- Added channel, payment, stock-reconciliation, and manual-override metrics and risks.
- Added `JV-MANUAL-ORDERS` and `JV-PAYMENT` validation gates.
- Preserved implementation authority as `NOT GRANTED`.

### 0.10 — 2026-07-25

- Reconciled `BD-DELTA-006` against canonical version 0.9.
- Added asymmetric availability permissions: authorised staff may disable items, while responsible staff control reactivation.
- Added strict opening counts, transactional reservations, replenishments, reason-coded corrections, and provisional closing reconciliation for countable stock.
- Added manual `Requires attention` handling when a valid reservation conflicts with physical stock.
- Added optional daily limits and pickup-window-specific availability for limited products.
- Added lightweight approximate-use allowances for selected shared critical ingredients or options without introducing gram-level recipe inventory.
- Added configuration-level shared-ingredient availability and prohibited automatic substitutions.
- Kept estimated reactivation times informational and required manual confirmation before online sale resumes.
- Added stock and availability audit candidates, risks, open questions, and the `JV-STOCK` validation gate.
- Preserved implementation authority as `NOT GRANTED`.

### 0.9 — 2026-07-24

- Reconciled `BD-DELTA-005` against canonical version 0.8.
- Added explicit customer acknowledgement of the gluten cross-contact warning.
- Defined general and option-specific warning placement and the `Gluten-free dough option` label.
- Added dynamic allergen and dietary-label calculation from the final product configuration.
- Added product-level allergen display, final checkout review, and initial vegan, vegetarian, and gluten-free-dough filters.
- Added supplier-document and change-triggered review requirements for ingredients, allergens, traces, and dietary labels.
- Added a publication gate preventing online sale of products with incomplete or unverifiable allergen information.
- Added authorised catalog approval and who-and-when traceability for material catalog changes.
- Restricted free-text kitchen notes so they cannot bypass configured modifiers, prices, availability, or allergen rules.
- Added `JV-CATALOG-APPROVAL` to the pending external validation gates.
- Preserved implementation authority as `NOT GRANTED`.

### 0.8 — 2026-07-24

- Reconciled `BD-DELTA-003` and `BD-DELTA-004` against canonical version 0.7.
- Added dynamic activation of scheduled orders and repeated estimate revision with tracking-page updates.
- Added a ten-minute customer response path for rejecting an important delay, with manual-review and `Requires attention` routing.
- Distinguished Dopis-caused delay incidents from customer incidents and preserved preparation-state-dependent resolution.
- Kept compensation outside the confirmed MVP while recording conditional authority and limit rules pending Jaime's validation.
- Added modifier boundaries for removals, substitutions, per-extra limits, constrained kitchen notes, and option-level unavailability.
- Recorded the actual gluten-free dough handling facts and the resulting cross-contact risk.
- Added a launch gate preventing claims of suitability for coeliac customers or severe allergies before supplier, process, allergen, and wording validation.
- Added concise `JV-*` external-validation gates in preparation for the future structured stakeholder-validation register.
- Preserved implementation authority as `NOT GRANTED`.

### 0.7 — 2026-07-24

- Reconciled the three inherited discovery checkpoints plus `BD-DELTA-001` and `BD-DELTA-002` without replacing the established architecture baseline.
- Confirmed weekly opening days and hours, pizza-service start, earliest pickup, latest pickup, and same-day ordering for launch.
- Added capacity templates by weekday and time segment and date-specific service exceptions.
- Refined checkout holds, pause behaviour, preparation start, cancellation release, non-collection handling, and operational incidents.
- Added kitchen queues, order acknowledgement, repeated alerts, connectivity safety pause, manual resume, and limited mobile backup.
- Kept the digital panel as the source of truth and the ticket printer as a conditional fallback after real operational testing.
- Added privacy and fairness constraints for telephone-based incident routing.
- Preserved implementation status as `NOT GRANTED`.

### 0.6 — 2026-07-24

- Reconciled the complete v0.5 business-discovery content with verified repository and architecture state.
- Recorded documentation custody, the completed reference-project assessment, and the accepted monorepo structure.
- Recorded the completed frontend migration into `frontend/`.
- Recorded successful feature-branch build validation and successful GitHub Pages deployment from `main`.
- Replaced the stale repository-audit and migration recommendations with the actual next sequence.
- Promoted FastAPI to the current provisional backend recommendation using project-specific evidence.
- Recorded the current frontend composable strategy and conditional future adoption of Pinia.
- Closed the university reference-project assessment backlog item.
- Removed the duplicated minimum-lead-time configuration field.
- Confirmed the five-minute provisional checkout capacity and stock hold in the scheduling UX.
- Added the cross-chat delta-checkpoint and canonical-document synchronisation protocol.

### 0.5 — 2026-07-24

- Confirmed a configurable advance-order horizon.
- Confirmed manual review for orders that cannot safely fit within one pickup window.
- Confirmed provisional stock reservation during checkout and ten-minute stock holds during manual review.
- Confirmed separate configuration for premises hours, pizza-service hours, earliest pickup, latest pickup, and minimum lead time.
- Recorded the provisional schedule: Wednesday–Thursday 18:00–22:00; Friday–Sunday 18:00–23:00; pizza ordering from 19:00; earliest pickup at 19:15.
- Marked Monday–Tuesday status, latest pickup times, minimum lead time, and the interpretation of “6” as 18:00 for confirmation.
- Adopted the recommended schedule administration model: weekly defaults, date exceptions, manual pause/resume, temporary delays, and per-window blocking or capacity reduction.

### 0.4 — 2026-07-24

- Confirmed a ten-minute hold for staff-proposed alternative pickup slots.
- Confirmed automatic rejection, capacity release, and outcome SMS when the customer does not respond before proposal expiry.
- Confirmed that product and modifier production points are initially configured and calibrated technically, while Jaime controls operational window capacity.
- Confirmed configurable percentage-based manual review for unusually large orders, subject to business validation.
- Confirmed 15-minute pickup windows for the initial operational model.
- Added configuration fields for alternative-slot holds and the large-order manual-review threshold.
- Refined the remaining discovery backlog around multi-window orders, calibration, operating hours, stock corrections, and exception handling.

### 0.3 — 2026-07-24

- Confirmed manual-review option C: staff may accept the requested slot, reject the order, or propose an alternative slot.
- Set a configurable five-minute provisional checkout hold as the initial value.
- Removed redundant acceptance SMS notifications; acceptance is shown on the web and tracking page.
- Confirmed one initial SMS for secure tracking access plus ready, rejection, and staff-cancellation SMS notifications.
- Defined a one-time URL-token exchange into a `Secure`, `HttpOnly`, `SameSite` tracking session.
- Confirmed weighted integer production points from the first operational version.
- Added product and modifier production-point fields and capacity-point window fields.
- Added the `ALTERNATIVE_PROPOSED` manual-review state and identified the customer-response mechanism as the next decision.

### 0.2 — 2026-07-24

- Selected automatic confirmation as the normal mode, with manual-review and paused modes controlled by staff.
- Added the hybrid pickup-time flow: early estimate, basket-aware slot calculation, provisional hold, and atomic revalidation.
- Separated product stock from kitchen production capacity.
- Added production-capacity units by pickup window.
- Added staff controls for slot blocking, temporary delays, product blocking, and cancellation.
- Added read-only guest order tracking by secure SMS link as a candidate MVP capability.
- Recorded one pizza size, configurable modifiers, gluten-free dough, paid extras, and no half-and-half pizzas.
- Expanded catalog administration toward protected CRUD with historical preservation.
- Added allergen and cross-contact information requirements.
- Defined the read-only assessment of `submission_PR_Brian` as the next activity.
- Added external evidence considered.

### 0.1 — 2026-07-24

- Created the living technical discovery document.
- Recorded guest pickup and pay-at-store as the initial order flow.
- Recommended a frontend/backend monorepo.
- Proposed FastAPI, PostgreSQL, and Docker Compose provisionally.
- Distinguished product availability, sellable-unit stock, and ingredient inventory.
- Separated operational data from future loyalty and marketing purposes.
- Added staged roadmap and discovery backlog.
