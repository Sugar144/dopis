# Dopis documentation

## Current authority

Canonical business truth is `current/DOPIS_TECHNICAL_DISCOVERY.md` version `0.19`. The accepted reconciliation delta is retained as source evidence; its accepted changes are consolidated into the living discovery and derived registries.

Consolidation does **not** grant implementation authority.

## External governance framework

Dopis is an external consumer of the immutable GOV-GEN revision recorded in
`../framework-lock.json`. Its controlled RC.1-to-RC.2 transition is recorded in
`../framework-upgrade.json`; the project-owned L1 instance is
`governance/configuration.yaml`. Acquire and verify the framework with
`python3 scripts/acquire-framework.py`; then run its official consumer check with
`python3 <acquired-framework-root>/tools/validate_consumer.py --consumer . --framework <acquired-framework-root> --lock framework-lock.json`.

Material execution prompts are held under `governance/prompts/`; governed-work
learning is held under `governance/learning/`. These project-owned custody
surfaces support the external process contract without duplicating it.

GOV-GEN governs repository execution and process semantics. It does not replace
Dopis discovery, requirements, business decisions, epics, validation gates,
exclusions, traceability, architecture decisions, or product-specific validators,
and it grants no implementation authority.

## Requirements baseline

Derived from the canonical discovery. `BASELINED` never means implementation authority.

Current generated baseline: version `0.6`, Owner-approved and derived from discovery v0.19.

- `current/DOPIS_MVP_REQUIREMENTS.md`: governed human-readable baseline.
- `current/requirements/DOPIS_MVP_REQUIREMENTS.json`: normative requirement records.
- `current/requirements/DOPIS_VALIDATION_GATES.json`: validation gates, milestones, and origin.
- `current/requirements/DOPIS_EXCLUSIONS.json`: machine-checkable first-MVP exclusions.
- `backlog/DOPIS_EPICS.json`: business-capability epic map.
- `traceability/DOPIS_TRACEABILITY_MATRIX.json`: traceability contract and orphan expectations.
- `reviews/`: independent audit reports for specification milestones.

Validate with `python scripts/validate_specification.py` and `python scripts/test_validate_specification.py`.

## Historical documents

- `archive/PRD-Dopis-v1.md`: initial product requirements, retained for historical context.
- `archive/initial-handoff.yaml`: initial discovery handoff, retained for historical context.

## Source material

- `brand/`: original brand PDFs.
- `product-sources/`: menu and product source documents awaiting validation.

## Reference material

- `reference-project/`: local university-project reference evidence. Large ZIP archives are intentionally ignored by Git.

## Architecture decisions

- `decisions/`: future architecture decision records.
