# DOPIS-LEARNING-003 — Prompt Supersession Link

- Observation: `DOPIS-PROMPT-003/0.1.1` corrected the dual-truth defect without durably recording that it superseded `0.1.0`.
- Impact: the material prompt lineage was incomplete despite immutable prompt custody.
- Cause: the correction prompt contained the instruction to mark supersession but no append-only lineage record was created.
- Containment: preserve v0.1.0 and v0.1.1 unchanged.
- Correction: v0.1.2 records the chain `0.1.0 -> 0.1.1 -> 0.1.2`.
- Prevention: every correction prompt must carry an explicit durable supersession chain before commit.
