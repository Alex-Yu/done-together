# Project commands

Status: Unconfigured — this template has no application runtime or test runner.

The developer owns installation, configuration, and command validation through the bootstrap tasks. After selecting the stack, record intended commands; during implementation, replace each applicable entry with exact commands, working directory, prerequisites, and required environment variables (names only). Mark inapplicable entries with a reason. Never report an unconfigured check as passing.

| Operation | Command | Working directory / notes |
| --- | --- | --- |
| Install / setup | Unconfigured | Include tool versions and dependency installation |
| Run locally | Unconfigured | Include expected readiness signal and shutdown |
| Build / package | Unconfigured | Document outputs |
| Fast targeted checks | Unconfigured | Explain how to select a test or component |
| Full automated tests | Unconfigured | Include prerequisites and expected result |
| Formatting / static analysis | Unconfigured | Use stack-appropriate tools |
| Acceptance / smoke check | Unconfigured | Provide repeatable steps and expected behavior |

Document additional platform-specific commands only after the project needs them. Use separate rows for supported environments when commands differ.

## Configuration

List required configuration, safe example values, and how to supply local secrets. If adding an example environment file, use placeholders only. Document test isolation and external-service requirements.
