# ADR-002: Transactional state, recurrence and approval integrity

Status: Accepted
Date: 2026-10-28
Decision owner: User (core stack selection); assistant records the recommended implementation design within that selection.
Related requirements / tasks: REQ-010–020/023/025; tasks 005–008; [architecture](../architecture.md); [plan](../plan.md)
Supersedes / superseded by: None

## Context

Competing reviews must award one star, recurrence must allow only one unfinished item and skip backlogs, edits must preserve snapshots, and schedules must advance without open browsers.

## Options

Application-only checks can race. Database constraints with transactional row locking enforce invariants across web and scheduler processes. Browser-driven recurrence fails the closed-browser requirement; an independent scheduler satisfies it without an initial task queue service.

## Decision

Use PostgreSQL transactions, consistent row locking, occurrence/approval uniqueness and a conditional unfinished-occurrence constraint. Store occurrence snapshots and unique durable approval records. Use an idempotent management command from an independent one-minute scheduler and reconcile during approval. Record UTC instants separately from calendar dates and household timezone rules. This implements the selected approach and approved product rules; it does not change them.

## Consequences

Concurrency tests must use PostgreSQL and independent transactions. Scheduler overlap/restarts and midnight/DST catch-up require tests. No Redis/Celery dependency is initially needed. Production process supervision remains a later operational decision. Definition deletion must preserve completed snapshots and awards.
