# DOPIS-PROMPT-005 — DOPIS-PLAN-002A orphan-recomputation correction
Prompt version: 0.1.1
Supersedes: DOPIS-PROMPT-005/0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, code, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-002a`
Branch: `planning/story-acceptance-contract`
Reviewed candidate: `001b74b6063431aee3299859e021977e1e3234b5`
Draft PR: `#8`

Run `git fetch origin` and `git pull --ff-only`, then verify the worktree is clean and matches the remote branch.
Apply root `AGENTS.md`, `framework-lock.json`, and the locked GOV-GEN framework.

## Finding

`STORY_ORPHAN_NOT_RECOMPUTED`

PLAN-002A now makes stories a supported validator node, but `scripts/validate_specification.py` still inserts:

`"stories_without_requirements": []`

as a fixed value in the recomputed orphan map.

`DOPIS_TRACEABILITY_MATRIX.json` explicitly states that every orphan array is recomputed and compared exactly. A populated defective story with no requirement links therefore must produce a computed `stories_without_requirements` entry rather than relying only on a direct validator error while the declared orphan remains permanently hard-coded empty.

## Required correction

Keep the story/acceptance contract, empty real backlog, product semantics, use-case model, requirements, epics, and traceability relations unchanged.

Update the story validator so `stories_without_requirements` is derived from the actual backlog and returned with the other story orphan sets.

Remove the hard-coded `"stories_without_requirements": []` placeholder from the global computed orphan map once the real story computation supplies it.

Add one focused negative fixture proving that a disposable populated story with no requirement links is rejected with `stories_without_requirements` populated/reported.

Preserve the existing `stories_without_behavior_requirements` check; these are distinct invariants:

- no requirement links at all;
- requirement links exist but none is BEHAVIOR.

Do not add new downstream semantics or coverage rules.

Add one concise learning record under:

`docs/governance/learning/`

covering the stale future-placeholder defect and the rule that a placeholder orphan must become a real recomputation when its node type becomes supported.

## Validation

Run the locked GOV-GEN consumer validator, then:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

Confirm:

- the real `DOPIS_STORIES.json` remains `stories: []`;
- `future_nodes.stories` remains `[]`;
- `future_nodes.acceptance_criteria` remains `[]`;
- requirements, epics, use cases, story/acceptance contract, and product semantics are unchanged;
- implementation authority remains `NOT_GRANTED`.

## Publication

This correction is within the already Owner-authorised DOPIS-PLAN-002A scope.
Commit and push the SAME branch using the configured authenticated remote.
Keep PR #8 draft.
Do not merge.
Do not start PLAN-002B.
Do not start architecture, tasks, tests, technical contracts, ADRs, task packets, or implementation.

Stop after successful push and report:

- pre-correction HEAD;
- corrected HEAD;
- changed files;
- negative-fixture count;
- GOV-GEN/validator/test results;
- confirmation the real story backlog and both future-node indexes remain empty;
- confirmation product/use-case/contract semantics are unchanged;
- implementation authority `NOT_GRANTED`;
- PLAN-002B not started.
