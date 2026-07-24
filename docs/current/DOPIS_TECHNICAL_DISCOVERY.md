# Dopis — Technical Discovery and MVP Backend Specification

**Document status:** DRAFT — discovery in progress  
**Version:** 0.3  
**Date:** 2026-07-24  
**Implementation authority:** NOT GRANTED  
**Current authority:** This document supersedes the archived initial PRD and handoff for technical MVP decisions.

---

## 1. Purpose

This is the living technical discovery document for Dopis.

It records:

- verified repository evidence;
- confirmed business requirements;
- provisional technical decisions;
- rejected assumptions;
- unresolved decisions;
- the authorised next step.

It does not authorise backend implementation or repository reorganisation.

---

## 2. Verified repository state

Verified by the read-only repository assessment:

- Repository path: `/home/sugar/Documents/Dopis_v1`
- Git repository: yes
- Branch: `main`
- Verified HEAD: `205c1b56fc01b4f77805c44e712b8ee5edf87c10`
- Remote state: aligned with `origin/main`
- Worktree: tracked files clean; `docs/` is currently untracked
- Current application: Vue 3 + Vite frontend demo
- Current state management: custom `useCart.js` composable, not Pinia
- Current routes:
  - `/`
  - `/carta`
  - `/checkout`
  - `/confirmacion`
  - `/panel`
- All routes are currently public
- Current catalog and orders are mock data
- GitHub Pages deployment assumes the frontend lives at repository root
- University reference archive:
  `docs/reference-project/submission_PR_Brian.zip`
- Reference archive size: approximately 108 MB

The initial statement that the current Dopis frontend used Pinia was incorrect. Pinia appears only in the university reference project.

---

## 3. Current frontend assessment

### 3.1 Strengths

- Clear separation between views, components, data, and cart logic.
- Reusable and reasonably granular Vue components.
- Existing frontend validation for name, telephone, payment method, and non-empty cart.
- Explicit TODO markers at future backend integration points.
- Responsive and mobile-first UX.
- Consistent relative imports, making a directory move low-risk.
- Cart computed values and upsell detection are already isolated.

### 3.2 Blocking gaps before real orders

- `/panel` has no real authentication or backend authorisation.
- The cart is memory-only and is lost on refresh.
- Product names and prices are mock data, not a validated catalog.
- There is no API client or API environment configuration.
- There are no automated tests.
- There is no linting or formatting configuration.
- The language selector is decorative only.
- The deploy workflow will break if the frontend is moved without updating its working directory and artifact path.

---

## 4. Product source status

### Available sources

- Drinks PDF.
- Desserts PDF.
- Pizza-menu photograph.
- Original brand PDFs.
- Archived initial PRD.
- Archived initial handoff.
- University reference-project archive.

### Gaps

- No structured and validated pizza catalog exists yet.
- Current `products.js` data must not become production catalog data.
- Exact modifiers and prices are not yet closed with Jaime.
- Exact allergen and gluten cross-contact wording is not yet validated.
- Opening hours and service windows remain undefined.

The pizza photograph may be transcribed into a draft catalog, but the resulting data must be validated by Jaime before it becomes authoritative.

---

## 5. Repository architecture decision

### Decision

Use one Git repository with independently structured frontend and backend applications.

### Target structure

```text
Dopis_v1/
├── frontend/
├── backend/
├── docs/
│   ├── archive/
│   ├── brand/
│   ├── current/
│   ├── decisions/
│   ├── product-sources/
│   └── reference-project/
├── infra/
│   └── local/
├── compose.yaml
├── .env.example
├── README.md
└── .gitignore
```

### Root-level responsibilities

Keep at repository root:

- `.git/`
- `.github/`
- `.gitignore`
- `.env.example`
- `compose.yaml`
- root `README.md`
- `docs/`

Move frontend-specific files together into `frontend/`:

- `src/`
- `public/`
- `index.html`
- `package.json`
- lockfile
- Vite configuration
- Tailwind configuration
- PostCSS configuration

### Deployment constraint

The GitHub Pages workflow currently assumes the npm project and `dist/` are at repository root. Any frontend move must update the workflow in the same bounded migration.

---

## 6. Large reference archive policy

The university ZIP is reference evidence, not a runtime dependency.

Recommended policy:

- do not commit the approximately 108 MB ZIP as a normal Git object;
- keep it local and ignored, or use Git LFS only if long-term shared custody is genuinely necessary;
- commit a small `README.md` or manifest describing:
  - archive name;
  - origin;
  - purpose;
  - expected local path;
  - checksum if durable verification is needed;
- never copy `node_modules` or generated bundles into the Dopis source tree.

Preferred current choice:

```text
docs/reference-project/README.md        # tracked
docs/reference-project/*.zip            # ignored
```

---

## 7. University reference-project findings

### Useful concepts

The following patterns are suitable for Dopis as concepts:

1. Central API client driven by an environment variable.
2. Router metadata and a global route guard for the staff panel.
3. Cart lines containing product IDs and quantities, not trusted prices.
4. Server-side product and price resolution.
5. Cart revalidation before checkout.
6. Domain-oriented state stores when shared state becomes complex.

### Patterns rejected

Do not reuse:

- bundled backend artifact as source architecture;
- committed `node_modules`;
- hard-coded API base URLs;
- absence of schema migrations;
- absence of tests;
- unauditable minified backend code.

No code reuse from the reference project is currently authorised.

---

## 8. Backend framework decision

### Current recommendation: FastAPI

The read-only assessment recommended NestJS mainly because it provides stronger architectural conventions and keeps the stack in the JavaScript/TypeScript ecosystem.

After considering the Project Owner's actual experience, the provisional recommendation is FastAPI because:

- the Project Owner already has practical FastAPI, Python, Docker, and Kubernetes exposure;
- the current frontend is JavaScript, not TypeScript, so NestJS would still introduce a new language layer and framework model;
- the MVP does not require a Node-specific capability;
- maintainability can be protected through an explicit modular architecture, service boundaries, dependency rules, migrations, tests, and API contracts;
- PostgreSQL, authentication, real-time updates, background tasks, payment integration, and OpenAPI contracts are compatible with the proposed FastAPI architecture.

This remains provisional until the API and module boundaries are drafted. NestJS remains a valid alternative, but “the framework imposes structure” is not sufficient on its own to outweigh the Project Owner's existing experience.

### Proposed FastAPI stack

- FastAPI
- Pydantic
- SQLAlchemy 2
- Alembic
- PostgreSQL
- pytest
- HTTPX test client
- Docker Compose
- REST API
- Server-Sent Events or WebSockets for kitchen updates, to be decided

---

## 9. Frontend state strategy

Do not migrate to Pinia only because the reference project uses it.

### Keep the composable for now when:

- cart state remains small;
- no persistence is needed yet;
- no user session exists;
- only a few views consume the state.

### Introduce Pinia when backend integration begins if it materially improves:

- authenticated staff session state;
- cart persistence and revalidation;
- catalog caching;
- checkout lifecycle;
- order tracking;
- kitchen panel live state.

The migration must be driven by state complexity, not by preference or reference-project similarity.

---

## 10. Confirmed MVP business scope

- Pickup orders only.
- Guest checkout.
- Customer provides name and telephone number.
- Initial payment method: pay at the premises.
- Data model prepared for later online payment.
- Kitchen panel displayed on a tablet.
- One staff authentication type initially.
- Staff can cancel orders.
- Staff can block pickup windows.
- Staff can pause online ordering.
- Staff can mark products or options unavailable.
- Normal mode should automatically confirm feasible orders.
- Manual-review mode remains available.
- SMS planned for relevant customer state changes.
- PostgreSQL as system of record.
- No coffee.
- One pizza size.
- No half-and-half pizzas initially.
- Product-specific allowed removals, substitutions, and paid extras.
- Gluten-free dough as a configurable option, subject to validated allergen wording.
- Product availability and unit stock for countable products.
- Broad protected catalog CRUD for Jaime.
- Ingredient-level automatic inventory deferred.
- Customer accounts, loyalty, birthdays, campaigns, packs, and online payments deferred to later phases.

---

## 11. Pickup scheduling direction

Recommended flow:

1. Show an early estimated pickup time while browsing.
2. Let the customer build the basket.
3. Calculate feasible times using the actual basket.
4. Offer:
   - earliest available;
   - scheduled later slot.
5. Create a short-lived provisional capacity hold during checkout.
6. Atomically revalidate availability, stock, and capacity when submitting.
7. If the slot is no longer feasible, return nearby alternatives instead of confirming and cancelling later.

Production capacity and product inventory remain separate domains.

---

## 12. Order modes and lifecycle

### Modes

- `AUTO_ACCEPT`
- `MANUAL_REVIEW`
- `PAUSED`

### Proposed lifecycle

```text
PENDING_CONFIRMATION
    ├── CONFIRMED
    │      └── PREPARING
    │             └── READY
    │                    └── COMPLETED
    ├── REJECTED
    └── CANCELLED
```

In automatic mode, a feasible order may enter `CONFIRMED` directly after atomic validation.

---

## 13. Guest tracking

A customer account is not required for tracking.

Provisional design:

- high-entropy, non-guessable tracking token;
- SMS link;
- read-only order status page;
- no exposure through sequential order IDs alone;
- customer cancellation deferred.

---

## 14. Catalog and modifiers

Use explicit modifier groups rather than unrestricted free-text changes.

Candidate groups:

- dough;
- cheese substitution;
- removable ingredients;
- paid extras.

Each option requires:

- selection rules;
- price delta;
- availability;
- product eligibility;
- display order.

Catalog CRUD must preserve historical orders through snapshots and product deactivation rather than destructive deletion.

---

## 15. Documentation authority

### Current

- `docs/current/DOPIS_TECHNICAL_DISCOVERY.md` — current technical discovery authority.

### Historical

- `docs/archive/PRD-Dopis-v1.md`
- `docs/archive/initial-handoff.yaml`

The archived PRD still provides useful product history, but its original MVP scope is superseded where it conflicts with this document.

### Future authorities

After business discovery is closed:

- revised PRD;
- architecture decision records;
- API contract;
- database schema;
- implementation plan.

---

## 16. Accepted next sequence

### Step 1 — documentation custody

- place this document in `docs/current/`;
- mark `docs/` structure intentionally;
- add the reference ZIP to `.gitignore`;
- add a tracked reference-project manifest or README.

### Step 2 — bounded frontend migration

In one reviewable change set:

- move frontend-specific files to `frontend/`;
- update GitHub Pages workflow;
- preserve deployed output and Vite base behaviour;
- verify build;
- do not create backend code.

### Step 3 — close remaining architecture decisions

- FastAPI module layout;
- authentication mechanism;
- API contract style;
- real-time transport;
- capacity model;
- SMS abstraction;
- exact MVP catalog-admin scope.

### Step 4 — backend scaffold

Only after the preceding decisions are recorded:

- create modular FastAPI application;
- add PostgreSQL and migrations;
- add tests;
- add local Compose environment;
- no business implementation beyond approved scaffold scope.

---

## 17. Decisions still open

1. Exact SMS events:
   - confirmed;
   - rejected;
   - cancelled;
   - ready.
2. Whether staff can propose a replacement slot during manual review.
3. Pickup-window duration and capacity-unit calculation.
4. Whether guest read-only tracking is included in operational MVP.
5. Whether Jaime can upload product images in the first catalog admin.
6. Exact login UX for kitchen staff.
7. SSE versus WebSockets.
8. Cart persistence strategy.
9. Exact i18n phase.
10. Exact payment-provider phase and abstraction.

---

## 18. Current risks

| Risk | Direction |
|---|---|
| Public staff panel | Backend authorisation required before real data |
| Invalid mock catalog | Transcribe and validate source data with Jaime |
| Missed kitchen orders | Sound, live updates, connection state, fallback |
| Incorrect capacity rules | Model and simulate before launch |
| Unmaintained inventory | Start with availability and countable units |
| Oversized reference archive in Git | Ignore locally or use explicit LFS decision |
| Frontend migration breaks deploy | Update workflow in same bounded migration |
| Framework chosen for abstract preference | Use Project Owner experience and explicit architecture rules |
| PRD scope conflicts with current MVP | Treat archived PRD as historical only |

---

## 19. Change log

### 0.3 — 2026-07-24

- Incorporated verified repository assessment.
- Corrected the false Pinia assumption.
- Confirmed monorepo architecture.
- Added GitHub Pages migration constraint.
- Added large reference-archive custody policy.
- Recorded reusable and rejected patterns from the university project.
- Changed provisional backend recommendation from NestJS to FastAPI based on actual Project Owner experience.
- Deferred Pinia adoption until shared state complexity justifies it.
- Formalised documentation authority and next sequence.

### 0.2 — 2026-07-24

- Added hybrid pickup-time flow.
- Separated production capacity from inventory.
- Added automatic, manual-review, and paused ordering modes.
- Added product modifiers and guest tracking direction.

### 0.1 — 2026-07-24

- Created initial technical discovery baseline.
