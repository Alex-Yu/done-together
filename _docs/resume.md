# Compact delivery resume

Delivery is paused at the user's request. This file is a handoff, not authorization to resume.

When ready, open a fresh chat in this repository, select low coordinator reasoning if available, and send:

> Read AGENTS.md, _docs/team/execution-policy.md and the current checkpoint in _docs/tasks.md. Resume the paused delivery goal. Preserve scope, retry counts, the active batch and all uncommitted work. Use fresh task-only developer/QA agents with the recorded model/reasoning policy; reuse valid PM grooming. Continue the authorized graph without per-task prompts. Start by completing/integrating task 004 after its recorded QA PASS, then select the next eligible task. Keep handoffs concise and use targeted checks until final release verification.

## State to verify before acting

- Branch: `task/004-board`; task 004 remains In review with independent QA PASS.
- Verified implementation: `067addc7eda122736893d17d5ca4aff7ce1a2885`; QA evidence commit: `797846a2e61ca0054724545424843c32cc422f8d`; pause checkpoint commit: `5c982f92b45f2463df42013c864c0750db21b41f`.
- Evidence: [board QA](verification/004-board-qa.md). Next: administrative completion, integration and affected checks, then issue #4 closure and task 005 readiness using existing grooming.
- Active batch 2: 3/10 completions before board integration; task 004 QA attempts 1/3. Preserve earlier counters from [tasks.md](tasks.md); do not start a new batch merely because the chat is fresh.
- Setup, skeleton and tasks 001–003 are integrated. Tasks 005–010 remain Draft; their grooming and verification plans are already prepared.
- No push or deployment authorization. PostgreSQL 17 is project-owned on loopback 55432; preserve unrelated PostgreSQL 13 on 5432. Inspect actual service/process state before starting or stopping anything.
- Inspect `git status` first. The user-requested workflow optimization is a scoped documentation edit; preserve any reviewable uncommitted changes. Never run two delivery coordinators concurrently.

If this state differs from Git or GitHub, use current authoritative evidence and update the checkpoint before continuing.
