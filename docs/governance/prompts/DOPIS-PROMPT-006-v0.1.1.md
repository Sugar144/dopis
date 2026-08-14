# DOPIS-PROMPT-006 — DOPIS-PLAN-002B fixture-isolation correction
Prompt version: 0.1.1
Supersedes: DOPIS-PROMPT-006/0.1.0

Speak to the Owner in Spanish.
Write repository artifacts, code, commit text, and technical documentation in English.

## Target

Repository: `Sugar144/dopis`
Worktree: `/home/sugar/Proyectos/worktrees/dopis-plan-002b`
Branch: `planning/mvp-stories-acceptance`
Accepted base: `1914eb9cfd1212531b081a7cf194472d9e84e6df`
Initial custody commit: `38221735262dafa5d5a86416553cdcabadfb7ab9`

The previous PLAN-002B execution produced valid-looking local backlog changes but
correctly stopped before commit/push because the required test suite exposed a
fixture-isolation defect.

Preserve the existing local PLAN-002B working changes. Do not discard or recreate
the story backlog merely to apply this correction.

Fetch the remote branch. If needed, use routine reversible Git mechanics such as a
temporary stash to fast-forward the local branch to the commit containing this
custodied correction prompt, then restore the existing working changes. Stop if
that cannot be done without ambiguity or loss.

Apply root `AGENTS.md`, `framework-lock.json`, and locked GOV-GEN conformance.

## Finding

`PLAN_002B_POPULATED_MODEL_FIXTURE_LEAKAGE`

`scripts/test_validate_specification.py` builds disposable trees by copying the
current real specification artifacts, including `DOPIS_STORIES.json`.

Its `populate_valid_use_case_model()` fixture replaces the disposable use-case
model and `future_nodes.use_cases`, but does not isolate the copied story backlog or
its story/acceptance-criterion future-node indexes.

That fixture happened to pass while the real story backlog was empty. Once
DOPIS-PLAN-002B correctly populated the real backlog, the disposable replacement
use-case model became inconsistent with the copied real stories and produced
story/use-case orphan failures.

This is a test-fixture isolation defect. It is not evidence that the populated
PLAN-002B backlog is invalid.

## Objective

Make the disposable use-case-model fixture self-contained so the test suite remains
valid with either an empty or populated real story backlog, then complete the
already-authorised PLAN-002B validation and publication.

Do not redesign the validator, story contract, or backlog model.

## Allowed correction surface

Modify only:

`scripts/test_validate_specification.py`

as needed to isolate the disposable use-case-model fixture from the real story
backlog.

The minimum expected correction is that a disposable tree whose use-case model is
replaced also carries a story-backlog state and `future_nodes.stories` /
`future_nodes.acceptance_criteria` indexes coherent with that disposable model.
For a use-case-only fixture, an empty disposable story backlog and empty story/AC
indexes are sufficient.

You may also update stale test-output wording in the same file if it incorrectly
claims the real backlog is empty after PLAN-002B.

Do not modify `scripts/validate_specification.py` unless a new independent defect is
proven. If such a defect appears, stop instead of broadening this correction.

Add one concise learning record:

`docs/governance/learning/DOPIS-LEARNING-006-fixture-isolation.md`

covering the fixture leakage, why it appeared only after backlog population, and
the prevention rule that disposable fixtures replacing an upstream artifact must
also isolate dependent downstream artifacts.

## Preserve the PLAN-002B semantic work

Retain the existing authorised local changes to:

- `docs/backlog/DOPIS_STORIES.json`;
- `docs/traceability/DOPIS_TRACEABILITY_MATRIX.json`;
- `docs/README.md`.

Do not change their semantics merely to make tests pass.

Requirements, epics, accepted use cases, validation gates, exclusions, both
traceability contracts, and product semantics remain immutable in this correction.

## Validation

After restoring the existing PLAN-002B working changes and applying the fixture
correction, run:

`python scripts/acquire-framework.py`

Run the locked GOV-GEN consumer validator.

Then run:

`python scripts/validate_specification.py`
`python scripts/test_validate_specification.py`
`git diff --check`

All required checks must pass before publication.

Reconfirm the PLAN-002B semantic completion report:

- story count;
- product acceptance-criterion count;
- use-case coverage;
- scenario coverage;
- distinct BEHAVIOR and CONSTRAINT requirement-link counts;
- story dependency-edge count;
- no unresolved gate was silently resolved;
- implementation authority remains `NOT_GRANTED`.

## Publication

This correction remains within the Owner-authorised DOPIS-PLAN-002B scope.

Commit the complete PLAN-002B candidate, including the already-authored backlog
changes, this correction prompt, the focused test correction, and the learning
record.

Push the SAME branch using the configured authenticated remote. Publication is
successful only when the remote branch resolves to the reported exact candidate
SHA.

Do not merge.
Do not start the minimum technical baseline or any later planning packet.

Leave the exact pushed candidate for bounded independent semantic review.

## Stop

Stop after successful push.

Report only:

- accepted base HEAD;
- initial custody HEAD;
- correction-custody HEAD if known;
- final candidate HEAD;
- changed files;
- story/acceptance-criterion counts;
- use-case/scenario coverage;
- BEHAVIOR/CONSTRAINT distinct requirement counts;
- dependency-edge count;
- GOV-GEN/specification/test/diff-check results;
- confirmation immutable product artifacts were unchanged;
- implementation authority `NOT_GRANTED`;
- later planning packets not started.
