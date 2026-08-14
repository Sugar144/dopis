# DOPIS-LEARNING-004 — Use-case semantic fidelity

- Observation: independent review found authority-role collapse and scenarios that did not share their parent use case's goal and trigger.
- Impact: the prepared model could delegate Jaime-only decisions or obscure distinct operational behavior.
- Cause: role labels and scenario grouping were treated as structural traceability rather than semantic constraints.
- Containment: preserve the accepted requirements and traceability contract; correct only the model and its exact index.
- Correction: add the Owner (Jaime) role, retain authorised-staff behavior, and separate later order changes, manual order review, and non-collection into coherent use cases.
- Prevention: before publication, verify every scenario's actors against its parent links, its goal/trigger context, and each requirement's explicit authority wording.
- Evidence limits: this record describes the model correction; it does not grant implementation authority or resolve open validation gates.
- Validation plan: run the locked GOV-GEN consumer validator, specification validator, negative tests, formatting check, and focused semantic pass.
