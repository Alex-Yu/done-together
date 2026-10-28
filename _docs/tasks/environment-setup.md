# Set up the development environment

Status: Draft
Labels: `environment-setup`
Requirement links: [_docs/plan.md](../plan.md), [_docs/architecture.md](../architecture.md); add applicable requirement IDs during grooming.
Dependencies: Product scope and architecture reviewed.

## Goal

The developer agent prepares a working local development environment for the chosen architecture without requiring the user to perform installation or configuration steps.

## Acceptance criteria

- [ ] AC-001: The developer inspects the target environment, records required tool versions, and installs or configures missing prerequisites for the selected stack.
- [ ] AC-002: Project dependencies and required local services, if applicable, are configured by the developer and pass architecture-specific readiness checks defined during grooming.
- [ ] AC-003: Required local configuration is created with safe defaults; committed examples contain no secrets and sensitive local files are ignored.
- [ ] AC-004: `_docs/commands.md` contains exact setup commands, prerequisites, working directories, and observed validation results sufficient to reproduce the environment.

## Out of scope

Application skeleton and startup smoke check: [Application skeleton](application-skeleton.md). Product features, production deployment, and paid service provisioning are separate tasks.

## Constraints

Follow the selected architecture. Prefer project-local tools where practical. Request required installation permissions or unavailable credentials; do not bypass restrictions. Unavailable access blocks completion.

## Verification plan

During grooming, define exact version probes, dependency checks, service readiness checks, and configuration checks for AC-001 through AC-004. QA executes the applicable checks and inspects the recorded setup instructions and secret handling. Mark inapplicable services explicitly with a reason.

## Questions and assumptions

Draft until architecture, target environment, installation method, applicable tools/services, and concrete verification commands are identified. The developer owns setup execution.

## Handoff

- Implementation summary: Pending
- Changed files / revision: Pending
- Checks and results: Pending
- Verification record: Pending
- Remaining risks or blockers: Pending
