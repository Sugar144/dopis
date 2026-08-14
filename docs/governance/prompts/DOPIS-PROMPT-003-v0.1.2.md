# DOPIS-PROMPT-003 v0.1.2 — Close supersession-link gap

Target:
Sugar144/dopis
worktree: /home/sugar/Proyectos/worktrees/dopis-plan-001a
branch: planning/use-case-traceability-contract
expected HEAD: 4c14ce1a3e1ba924a3de770e0fd67b3f69755133
PR: #6

This correction records the missing prompt-lineage supersession.

Supersession chain:
DOPIS-PROMPT-003/0.1.0
-> DOPIS-PROMPT-003/0.1.1
-> DOPIS-PROMPT-003/0.1.2

v0.1.1 remains immutable. It performed the dual-truth correction but failed
to durably record its supersession of v0.1.0.

Preserve this entire prompt exactly as:
docs/governance/prompts/DOPIS-PROMPT-003-v0.1.2.md

Add one concise learning record:
docs/governance/learning/DOPIS-LEARNING-003-prompt-supersession.md

Do not modify:
- v0.1.0 or v0.1.1 prompt files;
- use-case contract/model;
- traceability matrix;
- validators/tests;
- product artifacts.

Run git diff --check.

Commit and push the SAME branch using SSH.
Keep PR #6 draft.
Do not merge.
Do not start PLAN-001B.

Report final HEAD and changed files only.
