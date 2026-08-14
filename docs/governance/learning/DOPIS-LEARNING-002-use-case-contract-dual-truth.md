# DOPIS-LEARNING-002 — Use-Case Contract/Validator Dual Truth

- Observation: the use-case contract declared model vocabulary while the validator separately hard-coded the same values.
- Impact: a contract update could leave validation semantics stale or make the contract misleading.
- Cause: the initial validator treated contract vocabulary as a fixed schema assertion instead of its machine-readable input.
- Containment: retain deterministic invariant checks while loading identifiers, fields, roles, types, and traceability relations from the contract.
- Correction: represent the vocabulary and relation definitions structurally in `DOPIS_USE_CASE_TRACEABILITY_CONTRACT.json` and cross-check its relations against the traceability matrix.
- Prevention: disposable drift fixtures must reject contract/model and contract/matrix disagreement.
