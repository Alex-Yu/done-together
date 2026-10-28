# Developer evidence: environment-setup

Overall verdict: PENDING — independent QA required; this is implementation evidence.
Task / specification: [environment-setup](../tasks/environment-setup.md), [commands](../commands.md)
Revision: Task implementation commit recorded in backlog/handoff after commit.
Reviewer / independence: Developer self-check, not independent QA.
Environment: macOS x86_64; versions and command details in commands.md.
Date:2026-10-28

## Acceptance evidence

| Criterion | Executed procedure | Observed | QA verdict |
| --- | --- | --- | --- |
| AC-001 | Tool/version inventory; official checksum-verified PG source compile/install and Mailpit static binary; installed stable browser plist versions | uv0.12.19/Python3.13.15/Git2.56.0/gh2.103.3/PG17.11/Mailpit1.32.0/Chrome156.0.8078.48/Firefox158.0; existing PG13PID858 preserved | PENDING |
| AC-002 | `UV_CACHE_DIR=.local/uv-cache uv sync --locked`; imports/version probes | Exit0; Django5.2.18 and required imports; Python minor pinned; no application source | PENDING |
| AC-003 | psycopg app-role query, privilege query, disposable test DB create/drop; pg_isready; psql SELECT1; cluster stop/start | All exit0; role nonsuperuser/createdb/no createrole; appDB retained, testDB removed; loopback55432 only | PENDING |
| AC-004 | Mailpit loopback foreground start; synthetic smtplib send; API subject assertion; Chromium UI screenshot inspection; Ctrl-C/curl | Message visible sender/setup@example.test→capture@example.test; no relay configured; stop exit0, subsequent HTTP000 | PENDING |
| AC-005 | dotenv key/independent secret length/mode assertions; git check-ignore; no application-source assertion | All passed; .env0600, ignored services/private data, example/lock tracked; values never logged | PENDING |
| AC-006 | Playwright chromium/firefox install and executable existence; pytest/Ruff version probes; stable plist versions | Exit0; Chromium1248/Firefox1555 present; pytest9.2.0/Ruff0.17.3 | PENDING |
| AC-007 | Updated setup commands/provenance, full version records, service/synthetic capture/reproduction instructions; git diff --check | Exit0; application/scheduler commands still UNVERIFIED | PENDING |

## Required checks

`uv sync --locked` and imports succeeded on repeat; lockfile unchanged. Config key parity, independent secrets,0600 mode, normal/test database distinction and ignore boundaries passed. `git diff --check` passed. PG17 authenticated SELECT1 returned1; privileges `done_together,false,true,false`. Browser executable availability passed; Mailpit UI synthetic message inspected at1280×720. No application tests run.

## Findings

Default sandbox uv cache and network probes failed before authorized escalated execution/project-local cache. Existing pyenv shim cannot resolve .python-version3.13; use `uv run python`. `mailpit --version` returned1; corrected supported `mailpit version` returns0. Homebrew Intel bottles absent; supported local build/static release used. No unresolved setup failure.

## Services and artifacts

Project PG17 is left running for QA (data/log/socket under ignored .local). Mailpit stopped cleanly; QA starts with documented command. Ignored screenshot `.local/mailpit-capture.png` shows synthetic capture. Build logs and downloads/checksums remain ignored .local. No external email, deployment or push.

## Verdict rationale

Independent QA must verify every criterion at the exact implementation commit; this developer record cannot complete the task.
