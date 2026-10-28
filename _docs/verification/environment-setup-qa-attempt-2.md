# Verification: environment-setup — attempt 2

Overall verdict: PASS
Task / specification: [environment-setup](../tasks/environment-setup.md), [commands](../commands.md)
Revision or exact working-tree state: implementation `1dc5e2406abd49d3cb20e2a20c4f5e191f577274`, reviewed on `task/environment-setup` at `e7808387b218a50ec281d283485868c7dfff988e`. Subsequent handoff changes are records only.
Reviewer / independence: Separate QA subagent; no implementation fixes made.
Environment: Same macOS x86_64 checkout and toolchain as [attempt1](environment-setup-qa.md): Python3.13.15/Django5.2.18/PostgreSQL17.11/Mailpit1.32.0; dedicated cluster127.0.0.1:55432.
Date: 2026-10-28

## Acceptance evidence

| Criterion | Procedure / command | Expected | Observed / evidence | Verdict |
| --- | --- | --- | --- | --- |
| AC-001 | Inspect exact fix diff and reuse unaffected [attempt1 AC001](environment-setup-qa.md); inspect current listeners | Same installed toolchain; preserve existing services | Fix changes only commands and handoff/evidence documents; installed versions/checksum evidence remains valid. PG13PID858 unchanged on loopback5432; project PG17 alone on55432 | PASS |
| AC-002 | `git diff --exit-code f31e725ed4356ee142370cf8323e36f9ea43d8d5..1dc5e2406abd49d3cb20e2a20c4f5e191f577274 -- .gitignore .env.example .python-version pyproject.toml uv.lock`; inspect complete changed-file list | No runtime/source/dependency change invalidating successful locked reproduction | Exit0; only documentation changed. Attempt1 locked sync/import/source-absence execution remains applicable | PASS |
| AC-003 | Reuse unchanged role/testDB evidence from attempt1; rerun documented dedicated-cluster stop/start/readiness/authenticated SELECT1 | Project shutdown/startup work and application role remains usable | All exit0; SELECT1 returns1; PG13 preserved. Prior successful nonsuperuser/createdb/isolated testDB evidence unaffected | PASS |
| AC-004 | Compare fix against verified Mailpit startup/capture configuration; reuse attempt1 SMTP/API/UI/listener/shutdown evidence | No capture behavior changed | Only installed-version probe changed; capture command/configuration untouched. Actual synthetic UI/capture/clean-stop evidence remains applicable; Mailpit remains stopped | PASS |
| AC-005 | Compare tracked config/ignore files and complete fix diff; reuse secret-safe attempt1 assertions | Config/ignore/credential boundaries unchanged | No config, dependency, ignore or application-source changes; prior key parity, independent-secret, permissions and tracking checks remain applicable | PASS |
| AC-006 | Execute corrected `mailpit version --no-release-check`; reuse unchanged browser/tool probes from attempt1 | Version probe needs no online lookup; installed browsers/toolchain unchanged | Mailpit1.32.0 probe exit0 in default network-restricted sandbox; prior Chromium/Firefox executable and stable browser versions plus pytest/Ruff probes unaffected | PASS |
| AC-007 | Inspect commands lines151/155/189 and replay corrected procedures; confirm skeleton/features remain UNVERIFIED | Consistent exact instructions and resolved F001 | All PostgreSQL stop entries now use dedicated `.local/pgdata` pg_ctl; inappropriate Homebrew stop entry removed. Offline-safe Mailpit probe passes; project stop/start passes; application/scheduler commands remain UNVERIFIED | PASS |

## Required checks

Working directory: `/Users/alexy/Studies/sdd-apps/done-together`. PostgreSQL commands use documented project bin PATH and `PGPASSFILE="$PWD/.local/pgpass"`; no credentials printed.

| Command / check | Result | Evidence / limitation |
| --- | --- | --- |
| `.local/bin/mailpit version --no-release-check` | Exit0 | v1.32.0; succeeds without network release lookup |
| Exact implementation delta inspection | PASS | Original implementation→fix changes only commands, tasks/checkpoints, developer evidence and QA evidence. Fix→handoff tip changes only task/checkpoint records. No runtime, source, dependency or config changes |
| Runtime-file `git diff --exit-code` above | Exit0 | Lockfile, metadata, example and ignore files identical to runtime-verified revision |
| `pg_ctl -D .local/pgdata stop -m fast` | Exit0 | Corrected instruction stops only this project cluster |
| `pg_ctl -D .local/pgdata -l .local/postgresql-server.log start` | Exit0 | Project cluster restored for next task |
| `pg_isready -h 127.0.0.1 -p 55432` | Exit0 | Accepting connections |
| `psql -h 127.0.0.1 -p 55432 -U done_together -d done_together -c 'SELECT 1;'` | Exit0 | Authenticated result1 |
| `lsof -nP -iTCP:5432 -iTCP:55432 -iTCP:8025 -iTCP:1025 -sTCP:LISTEN` | Expected bindings | Existing PG13PID858 unchanged; project PG17PID65494 on127.0.0.1:55432; no Mailpit listener |
| `git diff --check` | Exit0 | No whitespace errors |

## Findings

F-001 resolved by the committed documentation correction. Offline Mailpit probe robustness note also resolved. [Attempt1 FAIL](environment-setup-qa.md) remains retained as historical evidence; it is superseded for the new implementation by this PASS.

No remaining QA finding or blocker. Reusing unaffected executed checks is justified by exact documentation-only diff inspection and unchanged local environment; no claim is based solely on the developer summary.

## Verdict rationale

PASS for AC001–007 at implementation `1dc5e2406abd49d3cb20e2a20c4f5e191f577274`, using fresh affected checks and explicitly retained unaffected runtime evidence. Attempt2/3, batch completions0/10. Task remains In review pending orchestrator requirements re-check and integration; QA has not marked Done or merged. Project PostgreSQL17 is left running; unrelated PostgreSQL13 unchanged; Mailpit stopped. No application tests, merge or push claimed.
