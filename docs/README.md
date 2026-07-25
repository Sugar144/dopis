# Dopis documentation

## Current authority

- `current/DOPIS_TECHNICAL_DISCOVERY.md`: living technical discovery and canonical business authority. It has priority over every derived artifact below.

## Requirements baseline

Derived from the canonical discovery. `BASELINED` never means implementation authority.

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
