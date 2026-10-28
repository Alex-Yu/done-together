# ADR-003: Shared-board authority, polling and offline recovery

Status: Accepted
Date: 2026-10-28
Decision owner: User (core stack selection); assistant records the recommended implementation design within that selection.
Related requirements / tasks: REQ-003–007/011/016/018/021–023/026/027; tasks 003/004/007/009; [architecture](../architecture.md); [plan](../plan.md)
Supersedes / superseded by: None

## Context

A signed-in board stays visible to children while parent controls lock. Either member parent may unlock; child PINs permit only their own submissions. Boards must synchronize within five seconds and preserve the last view offline.

## Options

UI-only PIN gates permit direct-request bypass. Server-enforced authority satisfies shared-board isolation. Two-second polling is simpler to operate than push connections for the initial board; WebSockets/SSE remain possible if measured scale or latency requires them. Persistent offline storage adds privacy and cache invalidation work beyond retaining an open board.

## Decision

Separate board membership from per-session server-side parent unlock with a 60-second parent-only activity timeout. Verify child PINs for submission and share exact P-05 identity failure limits in PostgreSQL. Poll household revisions every two seconds; refresh changed content without disturbing forms. Disable mutations after connectivity failure and require a fresh authorized snapshot on reconnect. This records the recommended design within the user-selected stack; the five-second target remains unverified.

## Consequences

Use protected credential hashes, additional request throttles and token-safe logging. Polling traffic cannot extend parent authority. Preserve local-date timeliness classification under P-04. Retain the currently displayed board in memory only; do not add offline startup or write queues. Measure synchronization and verify direct requests, multi-session lockouts, stable browser accessibility and lost-response recovery.
