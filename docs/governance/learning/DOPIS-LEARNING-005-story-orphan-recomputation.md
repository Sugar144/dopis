# DOPIS-LEARNING-005 — Story orphan recomputation

- Observation: `stories_without_requirements` remained a fixed empty placeholder after stories became a supported validator node.
- Impact: a populated story with no requirement links could be rejected directly while the traceability matrix comparison still treated its declared orphan array as empty.
- Cause: the future-node placeholder was not replaced when the story validator gained populated-backlog support.
- Containment: preserve the empty real backlog and all product, use-case, and story/acceptance-contract semantics.
- Correction: derive `stories_without_requirements` from each supported story's actual requirement links and include it in the global recomputed orphan map.
- Prevention: when a node type becomes supported, replace every placeholder orphan for that node type with real recomputation and a focused negative fixture.
- Evidence limits: this record corrects validator coverage only; it does not populate stories, grant implementation authority, or add downstream semantics.
- Validation plan: run the locked GOV-GEN consumer validator, specification validator, negative fixtures, and formatting check.
