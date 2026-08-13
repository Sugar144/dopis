# Dopis documentation

## Current authority

Canonical business truth is currently a controlled two-artifact state pending consolidation:

- `current/DOPIS_TECHNICAL_DISCOVERY.md`: canonical discovery base through version `0.18`.
- `current/DOPIS_ACCEPTED_RECONCILIATION_DELTA_2026-08-13.md`: accepted post-v0.18 Owner delta. It takes precedence wherever it explicitly conflicts with v0.18 until the living discovery and derived registries are consolidated.

The reconciliation delta does **not** grant implementation authority. The requirements baseline described below remains stale where it conflicts with the accepted delta and must not be treated as implementation-ready until regeneration and validation complete.

## Requirements baseline

Derived from the canonical discovery. `BASELINED` never means implementation authority.

Current generated baseline: version `0.5`, derived from discovery v0.18 and therefore pending reconciliation with the accepted 2026-08-13 delta.

- `current/DOPIS_MVP_REQUIREMENTS.md`: governed human-readable baseline.
- `current/requirements/DOPIS_MVP_REQUIREMENTS.json`: normative requirement records.
- `current/requirements/DOPIS_VALIDATION_GATES.json`: validation gates, milestones, and origin.
- `current/requirements/DOPIS_EXCLUSIONS.json`: machine-checkable first-MVP exclusions.
- `backlog/DOPIS_EPICS.json`: business-capability epic map.
- `traceability/DOPIS_TRACEABILITY_MATRIX.json`: traceability contract and orphan expectations.
- `reviews/`: independent audit reports for specification milestones.

Validate with `python scripts/validate_specification.py` and `python scripts/test_validate_specification.py` after the baseline is regenerated.

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
