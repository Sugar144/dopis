# Independent Requirements Audit — MILESTONE-SPEC-001

**Audit subject:** pull request #1, `agent/spec-001-requirements-baseline`, requirements baseline version `0.2`
**Auditor role:** independent requirements engineering audit
**Date:** `2026-07-25`
**Verdict:** `CHANGES_REQUIRED` at entry — all `CRITICAL` and `MAJOR` findings corrected in baseline version `0.3`
**Implementation authority:** `NOT GRANTED` before, during, and after this audit

> **Sections 1 to 16 record the original audit of baseline `0.2` and are preserved unchanged, including where the Project Owner's review later corrected them.** Section 17 is the Owner-review addendum: it records the Owner's findings on baseline `0.3`, their disposition, and the corrections that produced baseline `0.4`. Where the two disagree, **section 17 governs** — in particular the disposition of M3, the status of the gluten requirements, and the blocked count.

---

## 1. Verified repository state

Verified before any material claim was made, and again before publishing.

| Item | Expected | Verified actual |
|---|---|---|
| Repository | `Sugar144/dopis` | matches (`origin` fetch and push both `https://github.com/Sugar144/dopis.git`) |
| Base branch | `main` | matches |
| Base commit | `27334a56e9e2da55755a24faae4c9d46f7030392` | matches |
| Specification branch | `agent/spec-001-requirements-baseline` | matches; **not present locally at audit start**, retrieved with `git fetch --all` |
| Specification head | `bec4126644b06fc4fe79320ef85cb385648a0135` | matches |
| Pull request #1 | open | open, `MERGEABLE`, **not draft**, 16 commits, +697 / −0 |
| Canonical discovery | version `0.18` | matches, 3113 lines |
| Business discovery status | `CLOSED_PENDING_VALIDATION_AND_IMPLEMENTATION_PLANNING` | matches |
| Implementation authority | `NOT GRANTED` | matches |
| Worktree | clean | clean on `main` at start |

Additional state relevant to the audit:

- No `AGENTS.md`, `CLAUDE.md`, contributing guide, or schema file exists anywhere in the repository. There are no repository instructions constraining these artifacts beyond the canonical discovery itself.
- `docs/reviews/` did not exist and was created by this audit.
- Pull request #1 carries one prior review by the repository owner, submitted against commit `f8e0ebf`, listing five blockers. Section 7 records their disposition. The two other comments are automated bot notices with no review content.
- The audit was performed in an isolated git worktree at `.claude/worktrees/spec-001-audit`. `main` was never modified.

## 2. Audit scope

In scope: the requirements research note, the human-readable baseline, the four machine-readable registry parts, the epic map, the traceability matrix, the specification validator, the full pull-request diff and commit history, and the canonical discovery read in full.

Out of scope and untouched: `docs/current/DOPIS_TECHNICAL_DISCOVERY.md`, all frontend code, architecture and API design, and any resolution of an open stakeholder decision.

## 3. Authoritative sources reviewed

Recorded in full in `docs/research/requirements/RESEARCH_NOTE.md`, sections 2 to 5, including the criteria derived from each source, the guidance deliberately **not** adopted with reasons, and the four decisions that required professional judgement.

Summary: ISO/IEC/IEEE 29148:2018; ISO/IEC 25010:2023; NASA *How to Write a Good Requirement*; NASA SWE-050 and SWE-053; Agile Alliance epic definition.

No external source was used to create a Dopis obligation or to close an open business question.

## 4. Reconstructed canonical obligation inventory

The audit did **not** start from the version `0.2` baseline. The canonical discovery was read in full first, and an obligation inventory was extracted independently. Only then was it compared against the existing records.

Coverage of the reconstruction, with the canonical sections each was drawn from:

| Inventory area | Canonical sections |
|---|---|
| Confirmed MVP scope | 2.1, 3.1 |
| Explicit exclusions | 2.2, 7.8, 8, 9.4, 10.2, 12.7, 18A |
| Actors and responsibilities | 3.1, 6.5, 6.17, 11.7 |
| Customer-visible behaviour | 7.1, 7.4, 10A, 10B, 10.1B, 10.3 |
| Staff and kitchen workflows | 7.2, 7.5, 7.6, 8, 13.4 |
| Business rules and invariants | 7.4A, 9.3, 18A |
| Lifecycle states and transitions | 3.2, 7.1, 7.2, 7.3, 7.5 |
| Exceptional and failure paths | 7.5, 7.6, 7.7, 7.9, 8, 9.2 |
| Catalog and modifier rules | 10.1, 10.1A, 10.1B, 10.2 |
| Allergen and food-safety obligations | 10.1A, 10.3, 18A |
| Stock and availability | 9.1, 9.2, 9.2A, 9.2B, 6.13 |
| Capacity and scheduling | 9.3, 10A, 13.4, 6.8 |
| Ordering-channel rules | 7.4A, 12.2 |
| Customer communications | 10B, 11.6 |
| Tracking and access protection | 10B, 6.10 |
| Payment, handover, and close | 6.6, 7.5 |
| Privacy and retention | 11.1–11.7 |
| Pilot controls and evidence | 12.2–12.6, 18A |
| Quality attributes | 8, 12.3, 14 |
| Auditability | 6.11, 6.12, 6.16, 6.17, 6.18 |
| Unresolved Jaime decisions | 15 |
| Pilot-calibrated values | 6.20, 18A |
| Public-launch blockers | 11.5, 18A |
| Provisional technical proposals **excluded from requirements** | 4.2, 5.1, 5.2, 5.3, 13.1, 13.2 |

The last row matters as much as the others: the FastAPI recommendation, the proposed stack, the module boundaries, the Docker Compose environment, and the monorepo decision were identified as provisional technical proposals and deliberately produced **no** requirements. Version `0.2` correctly avoided them too; this is recorded as a confirmed non-finding.

The reconstruction identified **126 canonical obligations with no representation** in version `0.2`. The requirement count was an output of that comparison, not a target.

## 5. Findings ordered by severity

### CRITICAL

**C1 — Gluten cross-contact obligations almost entirely unspecified.**
Canonical section 10.3 records verified operating facts: gluten-free dough arrives sealed but shares the oven, workspace, and utensils with gluten products, creating "a real cross-contact risk that must be communicated accurately". It then imposes six interface obligations. Version `0.2` specified only `BR-ALLERGEN-001`, the rule not to claim coeliac suitability. Missing entirely: the general menu cross-contact warning; the specific warning shown on selecting the option; the **explicit customer confirmation that the warning has been read and understood**; the statement that online ordering cannot guarantee absence of cross-contact together with the advice to contact the premises; the ability to disable the gluten-free option independently; and the obligation to disable it whenever the validated procedure cannot be followed. A customer with coeliac disease could have completed an order without ever seeing a cross-contact warning.

**C2 — Dynamic allergen and dietary obligations missing.**
Section 10.3 additionally requires warning at selection time when a substitution *introduces* an allergen, recalculating the vegan and vegetarian classification when a modifier changes the final product, providing dietary filters, and showing clearly when an unavailable option changes the orderable dietary configuration. Version `0.2` covered only "show allergens for the final configuration and repeat them in the summary". A customer selecting a substitution would receive no allergen warning at the moment of choice.

**C3 — Post-publication safety review rules missing.**
Section 10.1A requires that a recipe, ingredient, quantity, or supplier change trigger a renewed allergen review and that **the affected product remains unavailable online until that review completes**, and that staff detecting incorrect safety information disable the item immediately. Neither was specified. Section 14 names the corresponding risk: "Product or supplier changes bypass allergen review → outdated safety information remains online."

**C4 — Free-text notes could invalidate the computed allergen result.**
Section 10.2 states a note "must not override configured modifier eligibility, price, availability, or allergen rules". Version `0.2` had no such rule. Since `FR-ALLERGEN-001` computes allergens from the configured modifiers, an unconstrained note makes that computation untrustworthy — the exact failure section 14 names as "Free-text notes bypass configured modifiers → ambiguous or unsafe kitchen requests".

### MAJOR

**M1 — Validation gates taken from a superseded canonical version.**
Version `0.2` used `JV-MANUAL-ORDERS` and `JV-PAYMENT`. Both are **absent from the current canonical validation register in section 15**. Grep of the full discovery shows they survive only in the change log at line 2992: "0.11 — Added `JV-MANUAL-ORDERS` and `JV-PAYMENT` validation gates." They were consolidated away in a later reconciliation. Version `0.2` also omitted the two closed gates. The resulting total of 17 coincidentally equalled the canonical count of 17, which concealed the substitution from a count-based check.

*Correction note:* an earlier stage of this audit characterised these two identifiers as invented. That was imprecise, and an independent cross-check caught it. They are stale, not fabricated. The distinction is recorded because it changes the remedy: the gates are now listed as `RETIRED` with the gate that carries each concern, rather than simply deleted.

**M2 — No validation gate registry existed.**
Gate identifiers lived only as bare strings inside requirement metadata and hand-written epic lists. Nothing declared any gate's meaning, milestone, canonical origin, or resolution criteria. A typo would silently create a new gate, and the validator would have counted it. This is the structural defect that allowed M1 to go unnoticed.

**M3 — Accepted obligations incorrectly reported as blocked.**
Thirty-four requirements carried `BLOCKED_BY_VALIDATION` although canonical discovery accepts the obligation and leaves open only a value, a procedure, or an ownership question. The clearest cases: the payment and handover model (`FR-PAYMENT-001`, `BR-PAYMENT-002`, `AUDIT-PAYMENT-001`, `AUDIT-PAYMENT-002`), confirmed in sections 3.2, 6.6, and 7.5 and blocked on a retired gate; manual channel entry (`FR-ORDER-007`), stated as a firm rule in 7.4A; stock counting (`FR-STOCK-002`, `FR-STOCK-003`), confirmed in 3.1 and 9.2; catalog administration (`FR-CATALOG-001`), confirmed in 3.1; weekly reporting (`AUDIT-PILOT-002`), confirmed in 3.2 and 12.3. The effect was to materially misrepresent readiness: 46 of 84 requirements appeared blocked when the underlying business intent was settled.

**M4 — Food-safety requirements assigned to the wrong milestone.**
`BR-CATALOG-001`, `DATA-ALLERGEN-001`, `FR-ALLERGEN-001`, and `BR-ALLERGEN-001` were classified `PUBLIC_LAUNCH_BLOCKER`. Section 18A lists "product-specific ingredients and allergens are complete and validated" among the blockers **before the first real order**. Treating them as public-launch concerns would have permitted a pilot with incomplete allergen data.

**M5 — Pilot privacy controls blocked on a public-launch gate.**
`PRIV-DATA-001`, `PRIV-DATA-002`, and `PRIV-DATA-003` were blocked by `JV-PRIVACY`, a public-launch gate. Sections 11.4, 12.4, and 18A all require minimum privacy, access, security, and rights-request controls to be active **from the first real pilot order**, and section 14 names the risk directly: "Pilot status is used to defer privacy controls → real customer data is handled without safeguards." The gate assignment produced exactly that deferral.

**M6 — `JV-PILOT` used as a catch-all with inconsistent effects.**
One gate spanned kitchen alert audibility, the opening checklist, pilot baseline recording, rollout, reliability, and weekly reporting, and was used as `BLOCK` on some requirements and `CALIBRATE` on others without any recorded reason. `JV-DELAYS` was similarly inconsistent between `FR-ORDER-004` (`CALIBRATE`) and `FR-ORDER-009` (`BLOCK`) for the same alternative-slot mechanism. With no `rationale` field, neither choice could be reviewed.

**M7 — Traceability matrix contained no traceable relationships.**
The matrix declared node types, relation types, and coverage rules, but not a single requirement-to-gate, requirement-to-epic, or requirement-to-source link. `normalized_link_sources` merely pointed at other files. Consequently the research note's claims — "exact agreement between the epic map and traceability matrix" and "exact agreement between requirement gate metadata and traceability links" — described checks that did not exist, because there was nothing to compare against. The matrix also stored `"last_local_result": "PASS: ..."`, a claim recorded as data.

**M8 — Explicit exclusions incomplete and unenforceable.**
Missing from the baseline: compensation capabilities (section 7.8 forbids coupon codes, discount codes, automatic compensation rules, future credits, and loyalty benefits), half-and-half pizzas, the ticket printer, Apple Pay and Google Pay, multilingual administration, advanced SEO, multi-day advance orders, and commercial automation. Exclusions existed only as Markdown prose, so no validator could check that a requirement had not reintroduced excluded scope.

**M9 — Material canonical obligations omitted.**
Beyond the food-safety findings, the reconstruction found no representation for: the operational threshold register of section 6.20, which every `JV-THRESHOLDS` link depends on; the pending-Jaime decision record of section 6.18; substitution rules and the absorbed price-difference limit of sections 6.19 and 7.9, which section 18A lists as a **pilot blocker**; the non-collection and `NO_SHOW` process of section 7.5; transactional capacity and stock commitment preventing overbooking, required by section 6.8; the provisional checkout hold and its behaviour during an ordering pause; routing an order to manual review when the initial tracking SMS fails, rather than rejecting it; alternative-slot expiry with automatic rejection and outcome SMS; approximate remaining-use allowances for critical shared ingredients; queue ordering by recommended preparation time; the telephone-support disclosure limit of section 11.3; the prohibition on storing payment-card data in section 11.7; and the upselling incompatibility warning of section 12.7.

### MODERATE

**D1 — The validator was self-confirming.** It hard-coded `expected 4 registry parts`, `expected 84 requirements`, `expected 11 epics`, `baseline_version == "0.2"`, and `schema_version == "1.1"`. It never checked that a `source` section exists in the discovery, never resolved gates against any registry, never verified the hand-written epic `gates` lists, never compared the Markdown baseline with the registry, and permitted a `BASELINED` requirement to carry a `BLOCK` gate. Five of its nine orphan keys were declared but never computed. No negative test existed, so nothing demonstrated it could fail.

**D2 — Non-atomic statements.** `OPS-HOURS-001` (seven concepts), `PILOT-004` (eight preconditions), `FR-CATALOG-001` (eight verbs), `OPS-ALLERGEN-001` (four obligations, with the required service pause missing), `AUDIT-PAYMENT-002` (four obligations), `NFR-KITCHEN-002` (three), `FR-COMMS-002` (a positive duty plus a prohibition), `PILOT-005` (a pause trigger plus a recurrence rule).

**D3 — Metadata contract incomplete.** Records carried nine fields. `rationale`, `dependencies`, and `notes` were absent, and the field names diverged from the contract the baseline document itself declared. The repository owner had already raised this in the prior review. Additionally, `classification` conflated four orthogonal dimensions: acceptance state, milestone, decision ownership, and calibration.

**D4 — No supersession state.** Only `BASELINED` and `BLOCKED_BY_VALIDATION` existed, making any requirement split unrecordable.

**D5 — Inconsistent terminology.** "operational attention", "operational review", and "staff attention" all appeared alongside the canonical `Requires attention`.

**D6 — Epic defects.** Cross-cutting mappings were unmarked, so a requirement appearing in three epics gave no indication of ownership. Epic `gates` arrays were hand-written and never verified. One epic would have grown to 49 requirements spanning catalog administration, food safety, and commercial upselling.

**D7 — Registry architecture.** The four-part split fell at exactly 21 records each, not on any domain boundary, and forced the part count into the validator. Part 1 was pretty-printed while parts 2 to 4 used a compressed header, guaranteeing noisy diffs.

### MINOR

**N1 —** Files containing JSON carried a `.yaml` extension. The `"format": "JSON subset of YAML 1.2"` marker made this deliberate, but the naming misleads tooling and readers.
**N2 —** `SRC-DISCOVERY-018` was defined in the traceability matrix and never referenced.
**N3 —** `implementation_authority` was absent from the four registry parts and from the traceability matrix.
**N4 —** Sorting registry parts by `glob` would misorder a hypothetical `PART_10` before `PART_2`.

### OBSERVATION

**O1 —** The canonical discovery change log at section 19 references four gate identifiers that no longer exist in the section 15 register: `JV-MANUAL-ORDERS`, `JV-PAYMENT`, `JV-UPSELL`, and `JV-LEGAL-RETENTION`. This is a canonical inconsistency and the proximate cause of M1. It is recorded as a follow-up for the Project Owner rather than corrected, since the audit must not modify canonical business intent. The gate registry now records all four as `RETIRED` with the gate that carries each concern.
**O2 —** Section references such as `7` or `8` point at whole sections spanning 60 or more lines, which is coarse for verifying a specific obligation. Section identifiers were nevertheless retained over line numbers because they have remained stable across versions 0.1 to 0.18, whereas line numbers change on every canonical edit.
**O3 —** ISO/IEC/IEEE 29148 recommends a `shall`-based sentence template. The baseline retains a consistent imperative form; the rationale is recorded in the research note, section 4.
**O4 —** The exclusion contradiction check is currently latent: no requirement violates an exclusion today. Its value is as a guard against future edits, and the negative test suite proves it fires.

## 6. Evidence for each finding

Every finding above cites the canonical section that supports it. The specific evidence commands used:

```bash
# M1 — the two gates exist only in the change log, not in the section 15 register
grep -n 'JV-MANUAL-ORDERS\|JV-PAYMENT\|JV-UPSELL\|JV-LEGAL-RETENTION' \
  docs/current/DOPIS_TECHNICAL_DISCOVERY.md
# -> lines 2905, 2934, 2947, 2992, all inside "## 19. Change log"

# M1 — the declared canonical gate set matches the section 15 register exactly
# (scoped to the register, excluding the change log): 17 == 17, match=True

# D1 — hard-coded expectations in the version 0.2 validator
git show bec4126:scripts/validate_specification.py | grep -n 'expected\|!= 84\|!= 4\|!= 11'

# M3 — canonical acceptance of the payment model said to be blocked
sed -n '213,225p;665,706p' docs/current/DOPIS_TECHNICAL_DISCOVERY.md

# M4/M5 — canonical pilot blockers versus public-launch blockers
sed -n '2803,2836p' docs/current/DOPIS_TECHNICAL_DISCOVERY.md
```

## 7. Disposition of every finding

| Finding | Disposition |
|---|---|
| C1 | Corrected. `FR-GLUTEN-001` to `FR-GLUTEN-005` and `OPS-GLUTEN-001` added. |
| C2 | Corrected. `FR-ALLERGEN-002` to `FR-ALLERGEN-005` added. |
| C3 | Corrected. `BR-CATALOG-003`, `BR-CATALOG-004`, `OPS-ALLERGEN-003` added. |
| C4 | Corrected. `BR-CATALOG-005`, `BR-CATALOG-006` added. |
| M1 | Corrected. Retired identifiers recorded with disposition; `JV-MANUAL-CHANNELS` and `JV-PAYMENT-PROCEDURE` declared `DERIVED` with written rationale; validator rejects any reference to a retired gate. |
| M2 | Corrected. `DOPIS_VALIDATION_GATES.json` created; every gate carries milestone, origin, source sections, resolution criteria, and open questions. |
| M3 | Corrected. 34 requirements moved to `BASELINED` with `VALIDATE` or `CALIBRATE` links. Blocked count 46 → 24. |
| M4 | Corrected. Allergen and publication requirements moved to `PILOT` milestone. |
| M5 | Corrected. Privacy requirements baselined at `PILOT` milestone; `OPS-PILOT-001` added to make the minimum-controls obligation binding. |
| M6 | Corrected. Gate registry gives each gate one coherent concern; every link now carries a `rationale`; `JV-PILOT` narrowed and `JV-DELAYS` made consistent. |
| M7 | Corrected. Matrix now declares derived relations and 19 orphan expectations, all recomputed. Stored `last_local_result` removed with an explicit note on why. |
| M8 | Corrected. `DOPIS_EXCLUSIONS.json` created with 17 exclusions, each with `forbidden_terms`, `enforced_by`, and canonical sections; `BR-SCOPE-001` to `BR-SCOPE-006` added. |
| M9 | Corrected. All listed obligations specified; see section 9. |
| D1 | Corrected. Validator rewritten; 17-case negative test suite added. |
| D2 | Corrected. Statements split where separate verification was justified; see section 9. |
| D3 | Corrected. Thirteen-field contract; `classification` replaced by `acceptance_state` and `readiness_milestone`. |
| D4 | Partially corrected. A `supersedes` field is defined and validated, but no requirement needed it, because every split preserved the original identifier for the primary obligation. |
| D5 | Corrected. `Requires attention` used consistently. |
| D6 | Corrected. `primary` and `supporting` separated with a mandatory `supporting_rationale`; epic gate lists derived, not declared; 11 epics → 13. |
| D7 | Corrected. Single registry file; no part count anywhere. |
| N1 | Corrected. `.yaml` files holding JSON renamed to `.json`. |
| N2 | Corrected. `SRC-DISCOVERY-018` retained and now carries the section-reference rule. |
| N3 | Corrected. All five machine artifacts declare `NOT_GRANTED`; the validator fails if any changes. |
| N4 | Corrected by removal — there are no parts. |
| O1 | **Not corrected — deliberate.** Canonical inconsistency, referred to the Project Owner. |
| O2 | **Not corrected — deliberate.** Rationale recorded; section identifiers are the more stable choice. |
| O3 | **Not adopted — deliberate.** Rationale recorded in the research note. |
| O4 | No action. Guard behaves as designed and is proven by the negative test suite. |

### Disposition of the prior owner review (commit `f8e0ebf`)

| Owner blocker | Disposition |
|---|---|
| 1. Declared metadata contract not carried by the records | Resolved. Full 13-field contract, enforced by the validator. |
| 2. Missing MVP capabilities | Resolved, and materially wider than reported: 126 obligations were missing, not the listed subset. |
| 3. Gate semantics must distinguish calibration from blocking and validate both | Resolved. Both directions enforced: a `BASELINED` record may not carry `BLOCK`, and a blocked record must. |
| 4. Orphan checks asserted without reproducible evidence | Resolved. All 19 recomputed each run; the negative suite proves a false declaration fails. |
| 5. `EPIC-COMMUNICATIONS` had an empty gate list while its requirements depended on unresolved SMS behaviour | Resolved structurally: epic gate lists are no longer hand-written, so they cannot disagree with the requirements. |

## 8. Files changed

| File | Change |
|---|---|
| `docs/current/requirements/DOPIS_MVP_REQUIREMENTS.json` | **added** — single normative registry, 210 records |
| `docs/current/requirements/DOPIS_VALIDATION_GATES.json` | **added** — 20 gates plus 4 retired |
| `docs/current/requirements/DOPIS_EXCLUSIONS.json` | **added** — 17 machine-checkable exclusions |
| `docs/current/requirements/DOPIS_MVP_REQUIREMENTS_PART_{1..4}.json` | **removed** — consolidated |
| `docs/backlog/DOPIS_EPICS.yaml` → `docs/backlog/DOPIS_EPICS.json` | replaced — 13 epics, primary/supporting |
| `docs/traceability/DOPIS_TRACEABILITY_MATRIX.yaml` → `.json` | replaced — derived relations, 19 orphan checks |
| `docs/current/DOPIS_MVP_REQUIREMENTS.md` | rewritten — version `0.3`, machine-checked agreement markers |
| `docs/research/requirements/RESEARCH_NOTE.md` | rewritten — criteria, non-adoption, judgement, reconstruction method |
| `scripts/validate_specification.py` | rewritten — fully derived |
| `scripts/test_validate_specification.py` | **added** — 17 negative cases plus control |
| `docs/reviews/MILESTONE_SPEC_001_AUDIT.md` | **added** — this report |

`docs/current/DOPIS_TECHNICAL_DISCOVERY.md` was **not** modified.

## 9. Requirement changes

**Totals:** 84 → 210. Added 126. Removed 0. **Every one of the 84 original identifiers is preserved**, so no external reference is broken.

Added by domain: `ORDER` 15, `KITCHEN` 15, `CATALOG` 14, `STOCK` 12, `PILOT` 7, `ALLERGEN` 6, `GLUTEN` 6, `CAPACITY` 6, `UPSELL` 6, `SCOPE` 6, `SUBST` 5, `PAYMENT` 4, `ACCESS` 3, `GOVERNANCE` 3, `DATA` 3, `THRESHOLD` 2, `TRACKING` 2, `COMMS` 2, `SHIFT` 2, `INCIDENT` 2, `ADMIN` 1, `HOURS` 1, `PRIV` 1, `REPORT` 1, `OPERABILITY` 1.

**Reclassified:** 34 requirements moved `BLOCKED_BY_VALIDATION` → `BASELINED`. None moved the other way. Gate links changed on 45 records; statements reworded on 73.

**Split, with the original identifier retained for the primary obligation:**

| Original | Retained | New sibling |
|---|---|---|
| `NFR-KITCHEN-002` | connection status and stale-data indication | `BR-KITCHEN-001` — write barrier while disconnected |
| `FR-COMMS-002` | ready, rejected, cancelled SMS | `BR-COMMS-001` — no acceptance SMS |
| `OPS-ALLERGEN-001` | immediate containment plus the previously missing service pause | `OPS-ALLERGEN-002` — accepted-order review and trail |
| `AUDIT-PAYMENT-002` | cash reconciliation | `OPS-SHIFT-001` — responsible close |
| `PILOT-005` | pause triggers | `BR-PILOT-003` — recurrence rollback |
| `FR-CATALOG-001` | catalog administration | `SEC-CATALOG-001` — sensitive-field authority |

**Merged or removed:** none.

**Distribution after correction:** 203 `PILOT`, 6 `PUBLIC_LAUNCH`, 1 `WITHOUT_JAIME`; 185 `MUST_MVP`, 23 `SHOULD_MVP`, 2 `COULD_MVP`; verification 141 `TEST`, 32 `INSPECTION`, 12 `SECURITY_TEST`, 12 `DEMONSTRATION`, 7 `ANALYSIS`, 5 `PILOT_EVIDENCE`, 1 `BUSINESS_REVIEW`.

## 10. Gate changes

- Registry created. 17 `CANONICAL` gates, verified by scoped comparison to match the section 15 register **exactly**.
- 3 `DERIVED` gates added, each with a written derivation rationale: `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, `JV-INCIDENT-FAIRNESS`.
- 4 gates recorded as `RETIRED` with disposition: `JV-MANUAL-ORDERS`, `JV-PAYMENT`, `JV-UPSELL`, `JV-LEGAL-RETENTION`.
- 2 `CLOSED` gates retained and confirmed unreferenced.
- Blocked requirements 46 → 24.

## 11. Epic and traceability changes

Epics 11 → 13. `EPIC-FOOD-SAFETY` and `EPIC-UPSELL` were separated from what would otherwise have been a 49-requirement catalog epic. Every requirement has exactly one `primary` epic; `supporting` mappings require a written rationale and may not duplicate the epic's own primary. Gate lists are derived.

Traceability now declares eight derived relation types, each naming the field it is computed from, and 19 orphan expectations, all recomputed on every run. Counts are present as integrity checksums that fail when stale rather than as assumptions. The stored pass result was removed.

## 12. Validator changes

Removed: every hard-coded count and version. Added: canonical section resolution, gate resolution, retired-gate rejection, exclusion contradiction detection, dependency resolution and cycle detection, epic ownership checks, Markdown-to-registry agreement, weak-modal statement rejection, status/`BLOCK` equivalence in both directions, derived-gate rationale enforcement, and an implementation-authority guard. Standard library only; deterministic; exit 1 with an itemised list on failure.

`scripts/test_validate_specification.py` covers 17 defect classes — duplicate identifier, unknown gate, unresolvable canonical source, `BASELINED` with `BLOCK`, blocked without `BLOCK`, missing field, orphan requirement, epic referencing an unknown requirement, stale count, dependency cycle, unresolved dependency, contradicted exclusion, derived gate without rationale, closed gate blocking, Markdown disagreement, granted implementation authority, weak modal statement — plus a control case.

## 13. Commands executed

```bash
git fetch --all --prune
git ls-remote origin
gh pr view 1 --repo Sugar144/dopis --json isDraft,reviews,comments,mergeable,baseRefName,headRefOid
git diff --stat main...origin/agent/spec-001-requirements-baseline
grep -n '^#\+ ' docs/current/DOPIS_TECHNICAL_DISCOVERY.md
grep -n 'JV-MANUAL-ORDERS\|JV-PAYMENT\|JV-UPSELL\|JV-LEGAL-RETENTION' docs/current/DOPIS_TECHNICAL_DISCOVERY.md
python3 scripts/validate_specification.py          # against version 0.2, then 0.3
python3 scripts/test_validate_specification.py
```

Plus independent cross-check scripts written directly against the artifacts, deliberately sharing no code with the audited validator, covering identifier uniqueness, canonical section resolution, gate resolution, epic coverage and multi-primary detection, supporting/primary overlap, status and `BLOCK` equivalence, mandatory field population, dependency resolution, exclusion contradiction, Markdown agreement, and a scoped comparison of the declared canonical gate set against the section 15 register.

The independent cross-check is what caught the imprecision in M1, which the audited validator could not have caught by construction.

## 14. Final validation results

```text
$ python3 scripts/validate_specification.py
PASS: 210 requirements, 13 epics, 18 of 20 gates referenced, 17 exclusions, 24 blocked requirements
      canonical discovery sections resolved: 112
      unreferenced gates (expected: closed only): ['JV-COHERENCE', 'JV-DISCOVERY-CLOSE']
      all declared orphan checks recomputed and matching
exit=0

$ python3 scripts/test_validate_specification.py
ok   control: unmutated artifacts pass
ok   duplicate requirement id ... ok   weak modal statement          [17 defect cases, all rejected]
PASS: 17 defect fixtures rejected, control fixture accepted
      no fixture state written to the repository
exit=0

$ independent cross-checks
requirements=210 unique=210 epics=13 exclusions=17
blocked=24 sections_resolved=112
section-15 register gates : 17
declared CANONICAL        : 17  match=True
result: ALL INDEPENDENT CHECKS PASS
```

During the audit the rewritten validator rejected three defects in the auditor's own work — a contradicted exclusion, a dependency cycle between `FR-SUBST-001` and `OPS-STOCK-001`, and two stale gate references in the Markdown baseline. All three were fixed. This is recorded as evidence that the validator detects real defects rather than confirming its inputs.

## 15. Residual risks and unresolved matters

1. **17 canonical validation gates remain unresolved.** 12 before the first pilot order, 2 before operating without Jaime, 3 before public launch. 24 requirements remain `BLOCKED_BY_VALIDATION`.
2. **Three derived gates require Project Owner confirmation.** `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, and `JV-INCIDENT-FAIRNESS` name questions the discovery leaves open without identifiers. If the Owner prefers them folded into existing canonical gates, or added to the canonical register, that is a legitimate alternative.
3. **Canonical follow-up (O1).** The change log references four retired gate identifiers. Recommended fix: a bounded, separately justified canonical note. Not performed here.
4. **Food-safety obligations remain gated on `JV-GLUTEN` and `JV-ALLERGENS`.** The requirements now exist, but the wording, the supplier documentation, the kitchen procedure, and the complete allergen matrix require Jaime. **No pilot order may be accepted before these resolve.**
5. **Legal compliance is not established.** `PRIV-RETENTION-001` is correctly blocked. No retention period was invented.
6. **Substitution rules and the absorbed price-difference limit are pilot blockers** with no approved values.
7. **The threshold register (`DATA-THRESHOLD-001`) does not yet exist as an artifact.** Every `CALIBRATE` link resolves through it.
8. **Verification methods are declared, not yet demonstrated.** Acceptance criteria and test strategy are future artifacts.
9. **The reconstruction is one auditor's reading.** It is reproducible from the cited sections, but a second independent reading could reasonably differ on granularity — particularly on whether presentational content rules warrant separate records.

## 16. Recommendation to the Project Owner

**Pull request #1 is suitable for your review. It is not suitable for automatic approval, and it must not be merged by anyone but you.**

All `CRITICAL` and `MAJOR` findings are corrected, and validation is reproducible and falsifiable. Under the audit's own disposition rule the PR is left **open and ready for Project Owner review**, not returned to draft.

Before approving, please make three decisions that are yours rather than the auditor's:

1. **Accept or reject the three derived gates** (residual risk 2). They are the only place where this audit named scope the discovery had not itself identified.
2. **Confirm the expansion from 84 to 210 requirements is the granularity you want.** The evidence supports each record, but granularity is a governance choice.
3. **Decide the canonical follow-up in O1.**

Two things this audit deliberately did not do: it did not resolve any Jaime decision, and it did not modify canonical business intent.

Implementation authority remains **`NOT GRANTED`**. A `BASELINED` requirement is an accepted obligation for specification only. Architecture, contracts, use cases, acceptance criteria, and a bounded task packet remain prerequisites before any implementation authority is considered.

---

## 17. Owner-review addendum — baseline `0.3` to `0.4`

**Review subject:** requirements baseline version `0.3`, as published in this pull request
**Reviewer:** Project Owner
**Date:** `2026-07-25`
**Result:** six findings, all accepted and corrected in baseline version `0.4`
**Implementation authority:** unchanged — `NOT GRANTED`

### 17.1 Provisional acceptances recorded

The Project Owner provisionally accepts, and this addendum records:

1. the three derived gates `JV-MANUAL-CHANNELS`, `JV-PAYMENT-PROCEDURE`, and `JV-INCIDENT-FAIRNESS` — **as specification-derived validation nodes only**. They do not become canonical section 15 gates, and each retains `origin: DERIVED` with its written derivation rationale. The validator rejects a derived gate that lacks one, and the independent cross-check asserts the derived set and its origins have not silently changed;
2. the 210-requirement granularity of baseline `0.3`, as the basis on which this correction pass builds;
3. handling the stale canonical change-log identifiers through a later bounded canonical-maintenance change rather than modifying discovery in this pull request. Finding O1 therefore remains open and deliberately uncorrected.

### 17.2 Root cause common to findings 2, 3, and 5

Baseline `0.3` treated *"the gate is unresolved"* as equivalent to *"the obligation is undecided."* They are not the same. Canonical discovery frequently accepts an obligation in full while leaving its exact wording, its operating procedure, its owner, or its supporting evidence to a validation gate. Baseline `0.3` recorded those cases as `BLOCKED_BY_VALIDATION`, which reported settled business intent as unspecifiable and materially understated readiness — the same defect the original audit had itself identified as M3, applied at a smaller scale to the records M3 did not reach.

### 17.3 Finding OW1 — stale-gate historical statement

**Finding.** `docs/current/DOPIS_MVP_REQUIREMENTS.md` stated that the version `0.2` identifiers appear in no part of the canonical discovery document. That contradicted both the audit report at section 5 (M1) and the gate registry, each of which correctly records the identifiers as present in the section 19 change log.

**Evidence.** `JV-MANUAL-ORDERS` and `JV-PAYMENT` appear at discovery line 2992, inside `## 19. Change log`, entered by discovery version `0.11`. They are absent from the section 15 validation register of version `0.18`.

**Disposition — corrected.** The Markdown baseline now states all three parts: absent from the current section 15 register; surviving only as historical entries in the section 19 change log; therefore **stale or retired, not fabricated and not absent from the complete document**.

A sweep of every changed artifact and of the pull request description found the inaccurate wording in that one sentence only. The gate registry's `retired_gates` evidence and the M1 entry in section 5 were already accurate; the M1 correction note at section 5 had already caught and recorded the earlier imprecision.

**Regression control.** The validator previously rejected *any* mention of a retired identifier in the Markdown baseline, which meant the correction could not be written at all. It now permits a retired identifier only on a line that identifies it as retired or stale, so a historical statement is expressible while a stale reference that reads as live still fails. A negative fixture covers it.

### 17.4 Finding OW2 — `JV-GLUTEN` reopened a settled obligation

**Finding.** `JV-GLUTEN` asked "whether explicit acknowledgement is required" in both its resolution criteria and its open questions. Canonical section 10.3 already requires "explicit confirmation that the customer has read and understood the warning". The gate was reopening a settled food-safety obligation.

**Disposition — corrected.** The gate no longer questions the existence of the acknowledgement obligation. It now covers only genuinely unresolved matters: the exact customer-facing cross-contact and acknowledgement wording, supplier documentation for gluten-free dough, the actual kitchen procedure, which severe-allergy requests the premises can responsibly accept, the detailed conditions under which staff must disable the option, and who besides Jaime may approve safety and dietary information. A `canonical_note` field records the eight section 10.3 interface obligations the gate does not reopen.

### 17.5 Finding OW3 — gluten requirement status against `BLOCK` semantics

**Finding.** Seven gluten records were `BLOCKED_BY_VALIDATION` although canonical section 10.3 states each obligation as a requirement of the interface.

**Evidence.** Section 10.3, "The interface must:" — show a general cross-contact warning in the menu; show a specific warning when the customer selects the option; require explicit confirmation that the customer has read and understood the warning; avoid claiming suitability for coeliac customers or severe allergies before validation; advise customers with severe allergies to contact the premises before ordering; state that online ordering cannot guarantee absence of cross-contact; allow staff to disable the option independently; disable it whenever the validated operating procedure cannot be followed.

**Disposition — corrected.** All seven are now `acceptance_state: ACCEPTED`, `status: BASELINED`, with `VALIDATE` on `JV-GLUTEN`.

| Requirement | Canonical acceptance | What remains open |
|---|---|---|
| `BR-ALLERGEN-001` | Present as a dough option; claim no coeliac suitability | Exact wording |
| `FR-GLUTEN-001` | General menu cross-contact warning | Exact wording |
| `FR-GLUTEN-002` | Specific warning on selection | Exact wording |
| `FR-GLUTEN-003` | Explicit read-and-understood confirmation | Exact acknowledgement wording |
| `FR-GLUTEN-004` | No-guarantee statement and severe-allergy contact advice | Exact wording; severe-allergy policy |
| `FR-GLUTEN-005` | Independent disablement of the option | Nothing; linked for coherence with `OPS-GLUTEN-001` |
| `OPS-GLUTEN-001` | Disablement when the validated procedure cannot be followed | Detailed conditions; kitchen procedure |

**No gluten requirement remains `BLOCKED_BY_VALIDATION`.** Food safety is not weakened by this: `PILOT-004` still carries `BLOCK` on `JV-GLUTEN`, so the unresolved gate continues to block the `PILOT` milestone globally and no pilot order may be accepted before it resolves. What changed is that an accepted obligation is no longer described as one that cannot be stated.

### 17.6 Finding OW4 — telephone-number scope

**Finding.** `DATA-ORDER-001` stated that name and telephone number are mandatory for **every** order, while `JV-MANUAL-CHANNELS` simultaneously recorded whether every in-person order needs a telephone number as unresolved. The accepted record decided the open question.

**Evidence.** Discovery line 85 (section 2.1): "Guest checkout requires a name and telephone number." Discovery line 208 (section 3.2): in-person orders "also use name and telephone number **as the current working direction**". Discovery line 1058 (section 7.4A): "Requiring a telephone number for every in-person order **remains a working decision pending Jaime's validation** of operational burden and privacy necessity." Section 14 additionally names "In-person telephone collection is excessive" as a risk.

**Disposition — corrected.** The single record is reformulated as three:

| Requirement | Statement | State |
|---|---|---|
| `DATA-ORDER-001` | Name and telephone number are the only mandatory customer data **for a web or telephone order** | `ACCEPTED` / `BASELINED` / `VALIDATE JV-PRIVACY` |
| `BR-ORDER-013` | Collect no mandatory customer data beyond name and telephone number **on any order channel** | `ACCEPTED` / `BASELINED` / `VALIDATE JV-PRIVACY` |
| `DATA-ORDER-003` | Require a telephone number for every in-person order | `PROVISIONAL` / `BLOCKED_BY_VALIDATION` / `BLOCK JV-MANUAL-CHANNELS` |

Data minimisation stays binding on every channel through `BR-ORDER-013`, which states the ceiling and therefore holds whichever way the in-person question resolves. No accepted statement now claims the in-person rule has been decided. Dependencies, the epic map, the traceability counts, and the negative fixtures were updated with them.

### 17.7 Finding OW5 — re-audit of every blocked requirement

Each of the twenty-four blocked records was tested against one question. **A:** is the obligation itself genuinely undecided? **B:** is the obligation accepted, with only a value, wording, procedure, owner, or evidence unresolved? Nineteen were case B.

| Requirement | New state | Canonical acceptance of the obligation |
|---|---|---|
| `BR-CATALOG-001` | `VALIDATE` ×2 | 10.1A, 18A — the prohibition on publishing an incomplete product |
| `DATA-CATALOG-001` | `VALIDATE JV-CONTENT` | 10.1B, 3.1 — the bilingual mechanism and fallback |
| `DATA-ALLERGEN-001` | `VALIDATE JV-ALLERGENS` | 10.3 — "The catalog must store…" |
| `BR-ALLERGEN-001`, `FR-GLUTEN-001…004`, `OPS-GLUTEN-001` | `VALIDATE JV-GLUTEN` | 10.3 — see OW3 |
| `FR-SUBST-001` | `VALIDATE` + `CALIBRATE` | 6.19, 7.9 — the two-tier substitution mechanism and its preference order |
| `BR-SUBST-001` | `VALIDATE` | 7.9 — "may not improvise an alternative outside approved rules" |
| `BR-SUBST-003` | `CALIBRATE` | 7.9 step 5 — collect or absorb within the configured limit; the limit is a value |
| `OPS-INCIDENT-001` | `VALIDATE` | 7.9 — pause only the affected scope, lowest-risk measure |
| `BR-GOVERNANCE-001` | `VALIDATE` | 7.9 — the shift-close condition, stated verbatim |
| `DATA-THRESHOLD-001` | `VALIDATE` | 6.20 — the register and its columns; the rows are content |
| `DATA-ACCESS-001` | `VALIDATE` | 6.5, 11.7 — explicit representation of delegated responsibility |
| `PRIV-RETENTION-001` | `CALIBRATE` + `VALIDATE` | 11.5, 18A — apply the approved periods; the periods are values |
| `PILOT-001` | `VALIDATE` + `CALIBRATE` | 12.2 — the two-week pre-pilot baseline |
| `PILOT-002` | `VALIDATE` | 12.4 — the first-segment shape |
| `PILOT-003` | `VALIDATE` | 12.4, 18A — the rehearsal and its coverage |
| `BR-PILOT-002` | `VALIDATE` | 12.5 — the requirement for explicit validated criteria |
| `PILOT-006` | `CALIBRATE` | 12.3 — the four-week evaluation |

`FR-INCIDENT-002` bundled two obligations of different status and was split. The staff contact and resolution obligation (7.5, 3.2) and the prohibition on automatic customer blocking (`BR-INCIDENT-003`) are accepted and baselined. The provisional two-incidents-in-90-days rule is now `BR-INCIDENT-002` and remains blocked.

**Five records remain blocked, each with a written justification.**

| Requirement | Reason code | Why `BLOCK` is valid |
|---|---|---|
| `PILOT-004` | `AUTHORISATION_NOT_YET_CONFERRED` | The canonical section 18A pilot entry condition; authorisation to begin the pilot has not been conferred |
| `OPS-DELEGATION-001` | `AUTHORISATION_NOT_YET_CONFERRED` | The canonical section 18A operating-without-Jaime entry condition |
| `BR-LAUNCH-001` | `AUTHORISATION_NOT_YET_CONFERRED` | The canonical section 18A public-launch entry condition |
| `DATA-ORDER-003` | `OBLIGATION_NOT_YET_ACCEPTED` | Section 7.4A records the in-person telephone rule as a working decision pending Jaime |
| `BR-INCIDENT-002` | `OBLIGATION_NOT_YET_ACCEPTED` | Section 3.2 records the repeat-incident rule as pending fairness and privacy validation |

**A gap this re-audit exposed.** Canonical section 18A states three blocker lists — pilot, operating without Jaime, and public launch — but baseline `0.3` represented only the pilot one, as `PILOT-004`. The other two were carried implicitly by individual blocked obligations such as `DATA-ACCESS-001` and `PRIV-RETENTION-001`. Correcting those to `BASELINED` would have silently removed the only representation of two canonical milestone conditions. `OPS-DELEGATION-001` and `BR-LAUNCH-001` were added so each list is represented explicitly, by a record whose whole subject is the authorisation. The independent cross-check asserts that all three milestones are covered by an authorisation-blocked record; losing one is now a validation failure rather than an unnoticed regression.

**Totals.** Requirements 210 → 216, none removed. Blocked 24 → 5. The blocked count was treated as an output of the evidence, not as a target; no record was unblocked to reach a number, and three of the five remaining blocks are new records rather than survivors.

### 17.8 Finding OW6 — `BLOCK` wording

**Finding.** `BLOCK` was defined as "the obligation itself cannot be specified or implemented until the gate resolves." A blocked record necessarily contains a candidate statement, so "cannot be specified" contradicted the artifact's own contents.

**Disposition — corrected.** In all four places that define the effect — the gate registry, the requirement registry field contract, the traceability contract, and the Markdown baseline — `BLOCK` now reads:

> The candidate obligation is recorded, but it cannot be accepted as final or made implementation-ready until the gate resolves.

Section 3 of the Markdown baseline now keeps four levels explicitly distinct, none implying the next: **recording a candidate requirement**; **accepting the obligation**; **milestone readiness**; **implementation authority**.

### 17.9 Regression control added

A gate being unresolved is not by itself a reason to block. Every `BLOCKED_BY_VALIDATION` record now carries a `block_justification` object with `reason_code`, `gate`, `canonical_open_question`, and `explanation`. The validator enforces:

1. `BLOCKED_BY_VALIDATION` if and only if a well-formed `block_justification` is present; a `BASELINED` record carrying one fails;
2. `reason_code` drawn from a closed vocabulary of three codes — `OBLIGATION_NOT_YET_ACCEPTED`, `SUBJECT_MATTER_NOT_YET_SELECTABLE`, `AUTHORISATION_NOT_YET_CONFERRED`. **The vocabulary contains no code meaning that only wording, procedure, ownership, or evidence is unresolved**, because that case is a `BASELINED` record with `VALIDATE` or `CALIBRATE`;
3. `gate` must be one of that record's own `BLOCK`-linked gates;
4. `canonical_open_question` must match an entry in that gate's `open_questions` **verbatim**, so a blocking concern is always a registered open question rather than an unstated one;
5. **an `ACCEPTED` record may not use `OBLIGATION_NOT_YET_ACCEPTED`** — acceptance and undecidedness are contradictory by the definition of `acceptance_state`;
6. `AUTHORISATION_NOT_YET_CONFERRED` requires a prohibition statement, so the milestone code cannot be borrowed for an ordinary obligation.

Rules 2 and 5 together make the reported defect unrepresentable: an accepted canonical obligation whose final wording or operating procedure is unresolved has no way to be recorded as blocked. None of the rules names a requirement identifier, a gate identifier, or a count, so they do not encode the current records.

Six negative fixtures were added, each selecting its target by scanning rather than by identifier: a blocked record with the justification removed; an `ACCEPTED` blocked record claiming its obligation is undecided; a justification citing an open question the gate does not declare; a justification naming a gate the record does not block on; a `BASELINED` record carrying a justification; and a Markdown baseline using a retired gate identifier as if it were current. The suite covers 23 defect classes, up from 17. `mutate_stale_counts` and `mutate_markdown_disagreement` were also made count-agnostic, so no fixture hard-codes a requirement total.

### 17.10 Incidental observation

The M6 disposition in section 7 states that "every link now carries a `rationale`". That is not literally true of `validation_links`, which are `[effect, gate]` pairs with no per-link field; the `rationale` is carried once per requirement. The new `block_justification` supplies a per-link explanation for `BLOCK` links specifically. This is recorded for accuracy rather than corrected in the historical section, which is preserved as written.

### 17.11 Validation after correction

```text
$ python3 scripts/validate_specification.py
PASS: 216 requirements, 13 epics, 18 of 20 gates referenced, 17 exclusions, 5 blocked requirements
      canonical discovery sections resolved: 112
      unreferenced gates (expected: closed only): ['JV-COHERENCE', 'JV-DISCOVERY-CLOSE']
      all declared orphan checks recomputed and matching
exit=0

$ python3 scripts/test_validate_specification.py
PASS: 23 defect fixtures rejected, control fixture accepted
      no fixture state written to the repository
exit=0

$ independent cross-checks (sharing no code with the validator)
requirements=216 unique=216 epics=13 exclusions=17 gates=20 retired=4
canonical headings parsed: 112
gates: CANONICAL=17 DERIVED=3
section-15 register gates : 17
declared CANONICAL        : 17  match=True
blocked=5: ['DATA-ORDER-003', 'BR-INCIDENT-002', 'OPS-DELEGATION-001', 'BR-LAUNCH-001', 'PILOT-004']
milestone entry conditions: ['BR-LAUNCH-001', 'OPS-DELEGATION-001', 'PILOT-004']
                            covering ['PILOT', 'PUBLIC_LAUNCH', 'WITHOUT_JAIME']
gluten records: 7
result: ALL INDEPENDENT CHECKS PASS
```

Confirmed by the run above: every canonical source section resolves; all gate references resolve; no retired gate is referenced by any requirement; the three derived gates remain `DERIVED` with rationales and are excluded from the canonical set, which still matches the section 15 register exactly at 17; every blocked requirement satisfies the corrected `BLOCK` semantics; `DATA-ORDER-001` no longer decides the in-person telephone rule; `JV-GLUTEN` no longer asks whether canonical acknowledgement is required; the Markdown baseline, registries, epic map, traceability matrix, and this report agree; and implementation authority is `NOT_GRANTED` in all five machine artifacts and in the Markdown baseline.

During this correction pass the validator again rejected a defect in the corrector's own work: the first attempt at the OW1 wording named the two retired identifiers in the Markdown baseline and was rejected as a stale gate reference. That is what prompted the historical-mention rule in 17.3 rather than a silent loosening of the check.

### 17.12 Residual risks after this pass

Residual risks 2 to 9 of section 15 stand, with these amendments:

1. **Risk 1 is restated.** 17 canonical gates remain unresolved — 12 pilot, 2 operating-without-Jaime, 3 public launch. **5** requirements are `BLOCKED_BY_VALIDATION`, not 24. The lower number reflects corrected semantics, not increased readiness: three unresolved milestone entry conditions still stop the pilot, operating without Jaime, and public launch respectively.
2. **Risk 2 is partially closed.** The Owner provisionally accepts the three derived gates as specification-derived nodes; they do not enter the canonical register.
3. **Risk 5 is restated.** `PRIV-RETENTION-001` is now `BASELINED` with `CALIBRATE`. No retention period was invented, and `BR-LAUNCH-001` blocks public launch until the periods are defined.
4. **New.** `OPS-DELEGATION-001` and `BR-LAUNCH-001` are the auditor's formulation of canonical section 18A blocker lists that had no baseline representation. They introduce no new business intent, but the Owner should confirm the wording matches the intended entry conditions.
5. **New.** The three-code block vocabulary is a governance decision embedded in the validator. If the Owner later finds a legitimate blocking situation none of the three codes describes, the vocabulary must be extended deliberately rather than by relabelling a record.

### 17.13 Disposition

Pull request #1 remains **open, unmerged, and ready for Project Owner review**. It was not merged, and no Jaime decision was resolved. Canonical business intent was not modified; finding O1 remains open by the Owner's own instruction.

Implementation authority remains **`NOT GRANTED`**.
