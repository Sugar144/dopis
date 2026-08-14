---
prompt_id: DOPIS-PROMPT-001
version: 0.1.0
category: governance adoption correction
authority_scope: >-
  Bounded RC.2 external-adoption correction on governance/adopt-gov-gen-rc1,
  including commit, push, and update of existing draft PR #5 only.
forbidden_actions: >-
  No amend, squash, force-push, branch rename, new PR, merge, release, deploy,
  GOV-GEN modification, product-semantic change, implementation-authority grant,
  or DOPIS-PLAN-001A.
execution_status: EXECUTED
repository: Sugar144/dopis
branch: governance/adopt-gov-gen-rc1
pull_request: '#5'
---

# DOPIS-GOV-ADOPT-001B-R1 — Complete GOV-GEN External Adoption with RC.2

## Identity

Repository: `Sugar144/dopis`.

Worktree: `/home/sugar/Proyectos/worktrees/dopis-gov-adopt`.

Branch: `governance/adopt-gov-gen-rc1`.

Existing draft PR: `#5`.

Expected current branch HEAD: `9466848009f151e086d0412241e8d14fcf2d42f9`.
PR base: `main @ 971c1b9abba7ff58233b3917ceb9219515867a99`.

This is a prospective correction to the existing adoption candidate. Do not amend,
squash, force-push, rename the branch, close PR #5, or create another PR. Preserve
the existing RC.1 adoption commit as historical evidence. Before mutation verify the
exact repository/worktree, branch and HEAD, clean working tree, upstream/divergence,
PR #5 baseline, and applicable `AGENTS.md`; stop if identities do not match.

## Controlling framework correction

Use exactly GOV-GEN repository `Sugar144/general-governance`, version `0.1.0-rc.2`,
immutable commit `b7f399d629e50087868dd21a1cab9620c785607a`, and release-manifest
SHA-256 `49bcd2705a18b2d5f6dde2b998b5ba4e17f254b2f8cce3cd95303f034da78ad8`.
Compatibility is framework contract `2.0.0`, consumer-lock schema `2.0.0`, and
consumer-configuration schema `1.0.0`. Read only the targeted consumer contract,
upgrade guide, listed schemas, configuration contract, operating contract, official
validator, and release manifest; do not modify GOV-GEN.

## Objective

Complete Dopis external-adopter #2 conformance against GOV-GEN RC.2: upgrade the
immutable lock; add mandatory Dopis-owned L1 configuration; resolve reusable-core
placeholders; establish a project-owned material-prompt namespace; record the
controlled upgrade; establish minimum prompt/learning custody; keep automated
conformance green; preserve all Dopis product semantics and authority state. Do not
begin product planning.

## Dopis-owned configuration

Create `docs/governance/configuration.yaml` with correction example IDs
`DOPIS-RUN-001` and `DOPIS-RUN-001-R1`; formal prompt-snapshot path
`docs/governance/runs/<run>/prompt/`; learning README path
`docs/governance/learning/README.md`; allocator namespace `dopis.governance` with
state and ledger paths under `docs/governance/identity/`; and material prompt
identity namespace `DOPIS-PROMPT`, sequence width `3`. These are Dopis L1 values.
Do not use `HP-PROMPT`; do not create allocator state or ledger without actual use.

## Lock and upgrade record

Byte-preserve the existing RC.1 lock temporarily before replacement. Replace the
root lock with the RC.2 schema-2 lock that binds
`docs/governance/configuration.yaml` and declares the required compatibility.
Create root `framework-upgrade.json`, conforming to the RC.2 upgrade schema, with
the exact original RC.1 lock as `previous_lock`, exact new lock as `new_lock`, and
`conformance_result: PASS` only after controlled-upgrade validation passes. Do not
retain a redundant permanent prior-lock copy.

## Local custody and CI

Create the minimal learning README. Assign this material execution prompt
`DOPIS-PROMPT-001`, version `0.1.0`, under `docs/governance/prompts/`, with metadata
for ID, version, category, authority, forbidden actions, status, repository/branch,
and PR #5. Do not fabricate the prior RC.1 prompt. Keep existing adoption surfaces;
update only where RC.2 requires it. The conformance workflow must use Python 3.12,
install only `pyyaml` and `jsonschema`, acquire the exact lock, run the official
validator, and run Dopis specification validators; do not modify `deploy.yml`.

## Invariants, validation, and publication

Do not modify discovery v0.19, requirements v0.6, epics, exclusions, validation or
traceability semantics, architecture decisions, source evidence, product code, use
cases, stories, acceptance criteria, or implementation tasks. Implementation
authority remains `NOT_GRANTED`; do not begin `DOPIS-PLAN-001A`.

Acquire and verify RC.2, run official controlled-upgrade validation with the exact
temporary RC.1 lock, run disposable negative tests for absent configuration, absent
prompt identity, invalid namespace, and unresolved placeholder, validate the upgrade
record, repeat dirty-cache regression, run both Dopis validators, run `git diff
--check`, and confirm no copied framework-owned prefixes. Commit, push the same
branch, update (but keep draft) PR #5 with the RC.1 finding, RC.2 correction,
DOPIS-PROMPT namespace, durable upgrade, conformance, unchanged product semantics,
and `NOT_GRANTED` authority. Do not merge or start PLAN-001A.
