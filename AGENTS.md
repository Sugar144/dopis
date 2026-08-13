# Dopis — Repository Execution Contract

This file defines how any agent (human-directed or autonomous) executes work inside
this repository. It is provider-neutral and applies to every AI coding assistant.

It states durable rules, not current project state. For current state, follow the
pointers below instead of asking what "should" be true.

## Durable truth

Repository state and accepted canonical artifacts are durable truth. Chat history and
model memory are working context and are not authoritative.

Before any material mutation, resolve from the repository itself:

- the exact active repository and worktree;
- current branch and HEAD;
- any applicable nested instructions;
- the living technical discovery and canonical business authority
  (`docs/current/DOPIS_TECHNICAL_DISCOVERY.md`), and the documentation/authority map
  (`docs/README.md`), which identifies the applicable derived requirements, decisions,
  reviews, and validators;
- the task or packet that actually grants the authority being exercised.

If any of these is unclear, stay read-only until it is resolved.

A ChatGPT Project, a repository, a branch, and a worktree are four distinct concepts.
Do not infer one from the shape of another — e.g. a nested directory that looks
related to Dopis may be a separate Git repository; check before treating it as part
of this one, and never modify a repository other than this one from inside this one.

## External governance binding

Dopis adopts the immutable GOV-GEN revision identified by `framework-lock.json`.
Before material governed work, acquire that exact framework with
`scripts/acquire-framework.py` and apply its
`framework/core/project-operating-contract.md` together with this project-local
`AGENTS.md`. The Project Owner's authority and the closest project-local
specialization remain applicable under the framework precedence rules.

Failure to resolve, acquire, or validate the locked framework is a read-only
boundary for work that depends on it. Never copy or override framework-owned
normative surfaces inside Dopis.

## Authority

```text
design != modify
modify != commit/push
commit/push != PR
PR/review != merge/release/acceptance
```

Repository access is not authority. Only an accepted task/packet or an explicit Owner
decision grants a bounded transformation.

Once such authority is granted, do not manufacture extra approval gates for routine
mechanics it already covers (branch/worktree setup, routine commits/pushes, draft-PR
bookkeeping, focused validation, mechanically determined corrections, routine evidence
recording). Owner attention is a scarce resource — spend it on material decisions only.

Nested instruction files (e.g. a package- or directory-scoped `AGENTS.md`) may narrow
practice for their subtree. They may never enlarge authority beyond what this file and
the active task/packet grant.

## Proportional governance

Do not require a separate Owner approval, a PR, a durable report, or an independent
review for every small repository mutation. Several bounded execution steps may share
one PR and one material result — do not assume `packet == commit == branch == PR ==
Owner decision`.

Reserve Owner decisions for material risk: product/business requirement changes,
canonical-state transitions, implementation-authority changes, architecture with
material semantic impact, and anything explicitly reserved by canonical governance
documents (see `docs/README.md`, `docs/decisions/`).

## Context and token economy

Context, tokens, and Owner attention are finite. Reference canonical artifacts by path
instead of retelling their contents. Prefer targeted reads, greps, and bounded line
ranges over rereading whole trees. Do not copy requirements, contracts, or
validator-enforced rules into prompts, PR descriptions, or new instruction files —
point to them instead. Prompt length is not evidence of safety.

## Decomposition

Pick the smallest coherent unit that produces one result. Combine steps that share one
outcome, one authority, one context, and one validation boundary. Split only when
authority, semantic risk, evidence gates, review independence, or context burden are
materially independent. Decomposition must not automatically multiply PRs, reviews, or
Owner approvals.

## Validation

Before publishing a change, know which checks are blocking. Validate the smallest
affected surface first; broaden only if risk or dependencies require it. An agent's own
claim that something works is not evidence — run the applicable validator
(`docs/README.md` lists them for specification artifacts, e.g.
`scripts/validate_specification.py`). Do not fix unrelated defects while executing a
bounded task. Reserve independent review for material semantic, architectural,
authority, security, or acceptance-fidelity risk — not routine low-risk work.

## Completion

When a bounded task ends, state exactly what changed, what was validated, the
publication state (committed / pushed / draft PR / none), any blockers or residual
risk, and the smallest next authorised action or Owner decision. Never claim
acceptance, merge, release, or canonical status without durable evidence for it.

## Where to look instead of asking

- Canonical business/technical authority and requirements map: `docs/README.md`.
- Architecture decisions: `docs/decisions/`.
- Independent audits and reviews: `docs/reviews/`.
- Specification validators: `scripts/validate_specification.py`,
  `scripts/test_validate_specification.py`.
