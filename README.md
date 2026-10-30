# Done Together

A shared family chore board for computer browsers. Parents assign and review chores; children submit their own work with a PIN. Approvals award stars, recurring chores follow the household calendar, and connected boards update automatically.

Built with Python 3.13, Django 5.2, PostgreSQL 17 and locally served HTMX. No frontend build is needed.

## Quick start

Run from the repository root. Scripts find the project directory and configure tool/cache paths automatically.

1. Install `uv`, PostgreSQL 17 and Mailpit. On macOS with Homebrew, use the optional installer; skip this if tools are already available:

   ```sh
   ./scripts/install-tools.sh
   ```

2. Set up dependencies, private configuration and the local database:

   ```sh
   ./scripts/setup.sh
   ```

3. Start the app, local email capture and recurrence scheduler together:

   ```sh
   ./scripts/dev.sh
   ```

   Open [Done Together](http://127.0.0.1:8000/) and [local email](http://127.0.0.1:8025/). Register, verify your email through Mailpit, create a household, set your parent PIN, then add children and chores. Ctrl-C stops all three services; PostgreSQL stays running.

4. Run checks and server tests in another terminal:

   ```sh
   ./scripts/test.sh
   ```

   Tests use a separate disposable PostgreSQL database. Allow several minutes; run database suites sequentially. See [testing](_docs/testing-guidelines.md) for browser and email checks.

For subsequent use, run `./scripts/dev.sh`. After pulling changes, rerun `./scripts/setup.sh`; it preserves existing secrets and data while applying migrations.

## Develop new features

1. Define the feature against the existing [product rules](_docs/plan.md) and [architecture](_docs/architecture.md).
2. Follow the [development process](_docs/process.md), [agent role guides](_docs/team/orchestrator.md) and [execution policy](_docs/team/execution-policy.md). Use the [feature prompts](_docs/prompts.md) to start or resume coordinated delivery.
3. Keep task criteria, verification evidence and the [current checkpoint](_docs/tasks.md) up to date.

The original application-template guide is preserved in [README.template.md](README.template.md).

## Project documentation

- [Setup, configuration, commands and troubleshooting](_docs/commands.md)
- [Testing](_docs/testing-guidelines.md)
- [Product rules and requirements](_docs/plan.md)
- [Architecture and data integrity](_docs/architecture.md)
- [Project status and remaining work](_docs/tasks.md)
- [Release verification summary](_docs/verification/release.md)

Local release verification is complete. Production hosting, email delivery, backups and deployment are not configured.
