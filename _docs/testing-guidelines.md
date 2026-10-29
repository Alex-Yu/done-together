# Verification guidelines

Derive checks from the specification and acceptance criteria, including failure and boundary cases. Avoid tests that merely mirror the implementation. Choose verification appropriate to the application: automated tests, command-line behavior, interface contracts, visual or accessibility inspection, hardware checks, or measured quality thresholds.

- Map every acceptance criterion to evidence. Use unit, integration, and end-to-end checks where they provide useful confidence.
- Use deterministic synthetic fixtures and isolate external effects. Document unavailable services and environment limitations.
- Run targeted checks during implementation and required regression checks before completion, using `_docs/commands.md`.
- Record the exact command or manual procedure, environment, expected result, observed result, and revision. Do not fabricate executions or infer behavior solely from source code.
- Mark unverified criteria BLOCKED. An unavailable environment or unconfigured command cannot yield PASS.
- QA does not fix code in the verification pass. Give the engineer reproducible findings, then verify the resulting revision.

Use `_docs/templates/verification.md` for the record. Overall verdict is FAIL if any criterion fails; otherwise BLOCKED if any required criterion or check cannot be verified; otherwise PASS. Required automated-check failures also prevent PASS. Keep all findings visible even when one fails early.

User delivery optimization (2026-10-29): run targeted feature/security checks and affected regressions per task; reuse exact prior evidence for unchanged behavior. Reserve full integrated regression and complete stable-browser journeys for final release010. Preserve every AC and critical new security/race check; record the delta and exact commands/results concisely.

Follow [team/execution-policy.md](team/execution-policy.md). Use one compact AC evidence table and command/result list; link earlier revision-bound records instead of copying them. Put verbose sanitized logs/screenshots in ignored `.local/verification/<task>/` (or another documented ignored directory), never credentials or raw private traces in source/chat. Return verdict, commit, counts, evidence path and blockers, normally within 150 words. Applicable task-specific mandatory checks still apply; efficiency does not permit skipping an AC or treating missing evidence as PASS.
