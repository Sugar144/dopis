# DOPIS-PROMPT-006 — DOPIS-PLAN-002B semantic correction
Prompt version: 0.1.2
Supersedes: DOPIS-PROMPT-006/0.1.1

Speak to the Owner in Spanish.
Write repository artifacts, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-002b`
Branch: `planning/mvp-stories-acceptance`
Reviewed candidate: `96bef0c5a80ec9c9dd6036c41eadbfb7432fcdaa`
Draft PR: `#9`

Run `git fetch origin` and `git pull --ff-only`, then verify the worktree is clean
and matches the remote branch.

Apply root `AGENTS.md`, `framework-lock.json`, the locked GOV-GEN framework, and
the integrated story/acceptance contract.

This is a bounded semantic correction of the already populated PLAN-002B backlog.
Do not redesign the model or regenerate the backlog from scratch.

## Independent-review findings

### STORY_ACTOR_BOUNDARY_CONFLATION

`ST-CAPACITY-001` declares `ACT-OWNER-JAIME` as its story actor while its second
acceptance criterion accepts behavior performed by authorised staff and by the
responsible person.

The parent `UC-CAPACITY-001` deliberately distinguishes:

- normal service schedule/capacity changes by Jaime (`UC-CAPACITY-001-S001`);
- temporary current-service adjustments by authorised staff / responsible person
  (`UC-CAPACITY-001-S002`).

Correct the capacity decomposition so every resulting story has one coherent
actor goal and authority boundary.

Because `FR-CAPACITY-004` belongs to authorised staff and `FR-CAPACITY-005` belongs
to the responsible person, do not hide those distinct authorities inside a story
whose `actor_id` is Jaime. Multiple child stories may reference the same parent
scenario where that is the smallest faithful decomposition.

Preserve `BR-CAPACITY-003`: permanent normal-capacity/hours changes remain Jaime-only;
delegated adjustment remains temporary and current-service-only.

### MATERIAL_CONSTRAINT_TRACEABILITY_LOSS

The candidate carries zero story-level `CONSTRAINT` links, but several product
acceptance boundaries are materially defined by parent constraints. Some current
criteria even paraphrase those constraints without tracing them.

At minimum correct these known cases:

1. `ST-ORDER-002` / `UC-ORDER-002-S002`
   - `BR-ORDER-007` defines the unanswered alternative-slot expiry outcome:
     release reserved capacity and stock, reject the order automatically, and send
     the outcome SMS.
   - `BR-ORDER-012` defines silence on an important revised pickup estimate as
     non-acceptance, routing the order to manual review and placing the explicit
     rejection in Requires attention.
   - Do not collapse these materially different observable outcomes into generic
     "safe handling".
   - Link the material constraints at story level and from the criterion/criteria
     whose acceptance they determine.
   - Keep configured/calibrated response windows unresolved; do not invent values.

2. Assisted order acceptance currently states that the next feasible opportunity
   does not displace accepted orders. That observable rule is `BR-ORDER-011`; if
   retained as an acceptance outcome, trace it as the material parent constraint.

3. Capacity acceptance currently states that actor authority is bounded to current
   service. That boundary is materially governed by `BR-CAPACITY-003`; trace it in
   the corrected capacity story/stories where it determines acceptance.

Then perform one bounded materiality pass across every populated story:

- inspect only that story's parent use-case `CONSTRAINT` links;
- include a parent constraint when violating it would allow the story to pass its
  product acceptance criteria incorrectly;
- reference that constraint from the acceptance criterion whose observable outcome
  it changes;
- do not bulk-copy all parent constraints;
- privacy, audit, NFR, governance, or other cross-cutting constraints may remain
  outside a story when they do not define that story's product acceptance boundary;
- do not create a durable constraint-classification registry merely for this pass.

A final total of zero story `CONSTRAINT` links is not compatible with the known
cases above.

## Preserve accepted semantics

Do not modify:

- discovery;
- requirements;
- epics;
- validation gates;
- exclusions;
- accepted use-case model;
- use-case traceability contract;
- story/acceptance traceability contract;
- validator;
- validator tests, except the already integrated fixture-isolation correction must
  remain intact;
- product evidence;
- application/frontend code;
- architecture decisions.

Do not resolve any open gate or choose any undecided/calibratable value.

Do not create technical acceptance criteria, tests, tasks, task packets, ADRs,
architecture, or implementation.

Implementation authority remains `NOT_GRANTED`.

## Required updates

Update only as semantically required:

- `docs/backlog/DOPIS_STORIES.json`;
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json` so story and acceptance-criterion
  future-node indexes exactly match the corrected backlog;
- `docs/README.md` only if its current wording becomes inaccurate.

Add one concise learning record under `docs/governance/learning/` covering:

- actor-boundary conflation in story decomposition;
- loss of material constraint traceability caused by behavior-only coverage checks;
- the prevention rule that observable acceptance text must trace the accepted
  requirement, including a parent constraint when that constraint determines the
  acceptance boundary.

## Revalidation

Recompute and report:

- story count;
- acceptance-criterion count;
- 23/23 use-case coverage;
- 26/26 scenario coverage;
- distinct BEHAVIOR-linked requirements;
- distinct CONSTRAINT-linked requirements;
- dependency-edge count.

Confirm:

- every story has one coherent actor/goal boundary;
- every parent scenario remains represented;
- every parent BEHAVIOR requirement remains covered by child stories and criteria;
- every material story-level constraint is linked with the same `CONSTRAINT` role
  as its parent use case;
- no constraint is promoted to BEHAVIOR;
- no new requirement link is invented;
- alternative/exception outcomes remain observably distinguishable;
- no open gate has been resolved or calibrated.

Run:

`python scripts/acquire-framework.py`

Run the locked GOV-GEN consumer validator, then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

## Publication

This correction remains within the Owner-authorised DOPIS-PLAN-002B scope.

Commit and push the SAME branch using the configured authenticated remote.
Keep PR #9 draft.
Do not merge.
Do not start any later planning packet.

Because this is material semantic backlog correction, leave the final exact pushed
candidate for bounded independent review.

## Stop

Stop after successful push.

Report only:

- pre-correction HEAD;
- corrected candidate HEAD;
- changed files;
- story/criterion/BEHAVIOR/CONSTRAINT/dependency counts;
- use-case/scenario coverage;
- GOV-GEN/validator/test/diff-check results;
- confirmation accepted upstream semantics are unchanged;
- implementation authority `NOT_GRANTED`;
- later planning not started.
