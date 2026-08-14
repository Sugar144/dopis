# DOPIS-LEARNING-006 — Fixture isolation after story population

- Observation: the disposable populated-use-case fixture copied the real story backlog, then replaced its upstream use-case model without resetting dependent story state.
- Impact: the fixture passed while the real backlog was empty but failed after valid PLAN-002B story population, reporting artificial story/use-case orphan relationships.
- Cause: the fixture isolated the replaced use-case model and its index, but not the downstream story backlog and story/acceptance-criterion indexes.
- Containment: preserve the populated PLAN-002B backlog and product semantics unchanged.
- Correction: reset the disposable story backlog and both dependent future-node indexes whenever the disposable use-case model is replaced.
- Prevention: a disposable fixture that replaces an upstream artifact must also isolate every dependent downstream artifact and derived index.
- Evidence limits: this correction changes test-fixture setup only; it does not change validator logic, requirements, use cases, contracts, product semantics, or implementation authority.
- Validation plan: run the locked GOV-GEN consumer validator, specification validator, negative-fixture suite, and formatting check.
