# Dopis — Technical Discovery and MVP Backend Specification

**Document status:** DRAFT — discovery in progress
**Version:** 0.6
**Date:** 2026-07-24
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
- Customers may eventually order a configurable number of days in advance. The initial launch horizon remains a configuration decision rather than a hard-coded same-day rule.
- An order whose production load cannot safely fit within a single pickup window must enter manual review in the MVP.
- Sellable-unit stock is provisionally reserved during checkout and committed only when the order is confirmed. Expired or abandoned holds release stock.
- Stock used by an order under manual review is held for ten minutes; expiry releases stock and follows the defined order-expiry outcome.
- Guest tracking should use a secure SMS-delivered access link that establishes a protected browser session without requiring an account.

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
- `name`
- `description`
- `category_id`
- `price`
- `is_active`
- `is_available`
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
- `customer_name`
- `customer_phone`
- `pickup_mode`
- `pickup_slot_id`
- `requested_pickup_at`
- `estimated_ready_at`
- `payment_method`
- `payment_status`
- `subtotal`
- `total`
- `customer_note`
- `internal_note`
- `created_at`
- `confirmed_at`
- `rejected_at`
- `ready_at`
- `completed_at`
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

### 6.5 Staff user

Initial fields:

- `id`
- `username`
- `password_hash`
- `is_active`
- `last_login_at`
- `created_at`
- `updated_at`

Only one staff role is initially required, but authorisation checks must exist on the backend.

### 6.6 Payment preparation

Even while only payment at pickup is active, orders should retain:

- `payment_method`
- `payment_status`
- optional future `payment_provider`
- optional future `provider_reference`

Suggested initial values:

- method: `PAY_AT_STORE`
- status: `PENDING`

This avoids coupling order creation to a specific future provider.

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

---

## 9. Catalog, inventory, and production capacity boundary

“Inventory” and “kitchen capacity” are different systems and must not be represented by the same counter.

### 9.1 Product availability

Staff can mark a product or modifier option as available or sold out.

### 9.2 Sellable-unit stock

The system stores quantities for directly countable products, such as canned drinks, bottles, individual desserts, or a genuinely limited prepared item. Stock is decremented when an order becomes confirmed, not merely when a customer opens checkout.

For pizzas, a per-product daily quantity should be optional rather than mandatory. Requiring Jaime to estimate every pizza variety each day would add maintenance without accurately representing shared dough, cheese, oven, and labour constraints.

### 9.3 Production capacity

Kitchen capacity controls how much work may be committed to a pickup window. The first operational version must already distinguish simple and complex pizzas through weighted production points.

Initial model:

- initial time-window duration of 15 minutes;
- configurable maximum production points per window;
- each pizza has a base production-point value;
- selected modifiers may add production points;
- drinks and ready-made desserts normally consume zero points;
- the order load is the integer sum of product and modifier points;
- blocked windows accept no new orders;
- staff may add temporary delays or reduce capacity;
- the earliest-available estimate advances when nearer windows are full.

Use small integer points rather than fractional time estimates. Example values must be calibrated with Jaime and kitchen observation rather than treated as universal facts. Product and modifier point values are technical configuration in the initial MVP; Jaime adjusts the operational capacity of windows rather than editing individual workload weights. The model may later evolve into station-specific capacity or historical prediction.

A configurable large-order threshold is also required. If an order consumes more than a defined percentage of one pickup window's capacity, it enters manual review even when the raw capacity calculation would permit automatic acceptance. The initial percentage must be validated with Jaime and real kitchen observations.

For the initial MVP, any order whose calculated production load cannot be safely accommodated within one pickup window also enters manual review. The system does not automatically distribute such an order across consecutive windows until a validated production-planning rule exists.

### 9.4 Ingredient and recipe inventory

A later system may define recipes or bills of materials so confirmed orders decrement ingredients and automatically disable products or modifier options when a required ingredient is unavailable.

### MVP decision

Implement:

- availability on/off;
- unit stock for drinks, desserts, and optionally limited products;
- weighted production points by pickup window.

Defer ingredient-level automatic depletion until the real stock-taking, delivery, waste, and correction workflow has been validated with Jaime.

---

## 10. Menu administration and product configuration

The intended owner of menu data is Jaime or authorised staff.

### 10.1 MVP administration target

Provide protected catalog CRUD for:

- categories;
- products;
- descriptions;
- prices;
- active/inactive state;
- available/sold-out state;
- unit stock where applicable;
- display order;
- product-to-modifier assignments.

Historical records must be preserved through order-item snapshots and soft deletion or deactivation. Removing a product from the active menu must not corrupt old orders.

Image upload may be deferred if it materially expands storage and deployment scope; an image path or URL field can be retained.

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

### 10.3 Allergen and dietary information

The catalog must be able to store ingredients, regulated allergen information, dietary labels, and a cross-contact notice. A generic waiver must not be treated as a substitute for accurate product information and validated kitchen procedures.

The exact customer-facing wording for gluten-free dough and cross-contact risk must be reviewed before production.

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

The status page is read-only for the normal order lifecycle. One narrowly scoped action may later be enabled to accept or decline a staff-proposed alternative pickup slot. Customer self-service cancellation remains deferred.

SMS policy for the first operational MVP:

- submission: send the secure tracking-access link;
- acceptance: show on the web/tracking page, without an additional SMS;
- ready: send SMS;
- rejected or cancelled by staff: send SMS with the outcome and contact guidance.

---

## 11. Privacy and customer data baseline

The first MVP should separate operational order data from future marketing and loyalty data.

### Operational order purpose

Candidate minimum data:

- name;
- telephone number;
- ordered products;
- pickup information;
- timestamps;
- operational status.

### Marketing and loyalty purpose

Future uses such as offers, birthday rewards, loyalty points, or customer profiling require separate business and privacy decisions. The system must not silently treat an operational telephone number as marketing permission.

### Technical baseline

- collect only fields required for the current purpose;
- clearly explain why the data is collected;
- define retention and deletion rules before production;
- protect the kitchen panel and administration endpoints;
- avoid storing sensitive payment-card data directly;
- keep marketing consent separate from order submission;
- support later anonymisation or deletion workflows;
- obtain legal review before public production use.

This section is a design baseline, not legal advice.

---

## 12. Analytics and business value

The first backend should capture reliable operational events without requiring customer accounts.

Candidate MVP metrics:

- orders per day;
- orders by hour;
- average order value;
- products sold;
- category mix;
- items per order;
- order acceptance time;
- preparation time;
- cancellation and rejection counts;
- repeat orders inferred from a normalised phone number only if legally and operationally justified;
- product unavailability frequency;
- upsell conversion for drinks, desserts, or packs.

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

Current reported schedule, interpreted provisionally:

- Wednesday and Thursday: premises open from 18:00 to 22:00.
- Friday, Saturday, and Sunday: premises open from 18:00 to 23:00.
- Pizza ordering begins at 19:00.
- Earliest pizza pickup is 19:15.
- Monday and Tuesday status remains unconfirmed.
- The reported opening time of “6” is interpreted as 18:00 and requires explicit confirmation before production.

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
2. Date-specific closures or exceptional openings.
3. Manual online-ordering pause and resume.
4. Temporary global delay applied to new estimates.
5. Blocking or capacity reduction for individual pickup windows.
6. Separate pizza-service hours from the premises' broader opening hours.

The final order-submission time must be derived from the latest permitted pickup and the minimum lead time rather than assumed to equal the premises closing time.

## 14. Main risks

| Risk | Consequence | Current mitigation direction |
|---|---|---|
| Panel accessible without real backend authorisation | Exposure or manipulation of orders | Implement functional staff authentication from the first operational backend |
| Tablet misses an order | Lost revenue and customer dissatisfaction | Sound, live updates, connection indicator, manual refresh, operational fallback |
| Product availability is inaccurate | Orders cannot be fulfilled | Start with simple availability controls and define ownership |
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
- the initial `maximum_advance_days` value;
- the exact latest pickup time and minimum lead time for each service day;
- whether Monday and Tuesday are closed;
- confirmation that the stated 18:00 opening interpretation is correct;
- how staff should handle an expired alternative proposal when direct customer contact has already occurred.

### Tablet and notifications

Resolved direction:

- audible alert, visual highlighting, automatic updates, and connection status are sufficient for the first iteration;
- no second staff notification channel is currently required.

Still open:

- which physical tablet and browser will be used;
- whether the tablet stays permanently logged in;
- session lifetime and re-authentication behaviour;
- screen wake and kiosk-mode behaviour;
- operational fallback when the panel, Wi-Fi, or local server is unavailable.

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
- ingredient-level inventory deferred.

Still open:

- the exact modifier matrix for every pizza;
- price of each extra or substitution;
- whether gluten-free dough changes price;
- the exact allergen and cross-contact wording;
- whether any pizza has a daily product-specific limit;
- who records stock deliveries, corrections, and waste;
- whether modifiers require independent stock;
- whether image upload belongs in the first admin interface.

### Customers and privacy

- Is the telephone number only for order contact?
- When will customer accounts be introduced?
- Which future marketing channel is preferred?
- What constitutes explicit loyalty enrolment?
- Is a birthday benefit important enough to collect birth information?
- How long should operational order data be retained?
- Who responds to deletion or access requests?

### Business outcomes

- What baseline exists for calls, orders, average ticket, and peak periods?
- Which result would make the MVP successful after 30 days?
- Which products have the best margin?
- Which combinations should become packs?
- What customer behaviour should the first dashboard help Jaime change?

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

### Phase 0B — business and architecture discovery — IN PROGRESS

Remaining:

- continue business discovery through delta checkpoints;
- normalise and validate the real menu;
- confirm operating hours and date exceptions;
- calibrate production-point rules;
- close modifier and allergen details;
- decide staff authentication UX;
- decide SSE versus WebSockets;
- define SMS abstraction and retry behaviour;
- define exact MVP catalog administration;
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
2. Continue business discovery using delta checkpoints rather than independent full-document replacements.
3. Create and review ADRs for:
   - monorepo architecture;
   - provisional FastAPI selection;
   - weighted pickup-capacity windows;
   - secure guest tracking;
   - transactional stock and capacity holds.
4. Transcribe product-source material into a draft structured catalog.
5. Validate the catalog, modifiers, prices, allergens, and operating hours with Jaime.
6. Draft the MVP requirements baseline.
7. Draft the API contract and database schema.
8. Draft a bounded backend-scaffold plan.
9. Grant separate implementation authority only after those artifacts are reviewed.

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

## 19. Change log

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
