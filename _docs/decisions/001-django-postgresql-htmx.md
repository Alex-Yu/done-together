# ADR-001: Django monolith with PostgreSQL and HTMX

Status: Accepted
Date: 2026-10-28
Decision owner: User (core stack selection); assistant records the recommended implementation design within that selection.
Related requirements / tasks: REQ-001–027; environment-setup; application-skeleton; [architecture](../architecture.md); [plan](../plan.md)
Supersedes / superseded by: None

## Context

The release is a computer-browser household board with accounts, forms, shared state, and scheduled work. Reliable domain rules and maintainability dominate; no native client is in scope.

## Options

Django/PostgreSQL/HTMX keeps rendering and business rules together. Next.js/Supabase adds managed realtime/account services but custom PIN authorization remains. React plus a separate Django API offers independent clients at additional contract and state-management cost.

## Decision

Use Django + PostgreSQL + HTMX, selected explicitly by the user on 2026-10-28. Python 3.13, Django 5.2 LTS and PostgreSQL 17 are the documented implementation baseline, subject to setup compatibility validation. Serve pinned HTMX locally with plain CSS and small JavaScript modules.

## Consequences

Operate one application plus a scheduler and database. No separate frontend build toolchain is required. Use uv and locked dependencies; record actual patches during setup. Hosting, provider costs, backup/recovery arrangements and deployment remain unresolved and unauthorized. See architecture.md for boundaries and commands.md for unverified commands.
