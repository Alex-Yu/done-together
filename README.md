# Build an application with AI using specifications

Use this template to turn an application idea into working, verified code with an AI coding assistant. You describe the product and review decisions; the assistant maintains the specifications, creates tasks, writes code, and runs checks.

The template works with any programming language, platform, or AI assistant. It starts with Markdown documents. Application code is created in step 5, after you agree on what to build and how to build it.

## What you need

- An application idea and someone who can decide its scope (usually you).
- A copy of this repository and an AI coding assistant that can read and edit it and run commands.
- Permission for the coding assistant to install and configure the tools required by the chosen stack during setup tasks.

If you use a chat assistant without repository access, supply the relevant documents and apply its proposed file changes and commands yourself.

## 1. Create your project

Use this repository as a template, or copy it into a new project directory. Open that directory in your editor and start your coding assistant there.

Tell the assistant:

> Read `AGENTS.md`. We will use this repository to build an application. Follow its spec-driven workflow and ask questions when important details are uncertain.

Keep the workflow documents in your new project; they provide context when you start a fresh AI session. You can use one assistant throughout. Separate agents and automation are optional.

## 2. Describe the application you want

Replace `[your application idea]` in this prompt and send it to the assistant:

> Help me turn [your application idea] into a product specification in `_docs/plan.md`. Ask one focused question at a time about users, main workflows, expected outcomes, first-release scope, failure cases, data, and constraints. Record my answers. Keep technology choices separate. Do not write application code yet.

Answer the questions, then read the completed plan. Correct anything that does not describe the application you want. Pay particular attention to what the first version includes and excludes.

**Before continuing:** confirm the first-release scope and resolve questions that would change its behavior. The result is your product specification in [_docs/plan.md](_docs/plan.md).

## 3. Choose the stack

Ask:

> Read the product specification. Compare suitable implementation approaches, explain their tradeoffs, and recommend one. Include the development tools I will need. Do not scaffold the application until I choose an approach.

Choose an approach you can run, maintain, and review. If you have a preferred language, platform, or framework, tell the assistant now. Then ask:

> Record the selected approach in `_docs/architecture.md` and significant decisions in `_docs/decisions/`. Document prerequisites and intended setup, run, and verification commands in `_docs/commands.md`. Identify the installation and configuration work for the developer to perform as setup tasks. Leave commands explicitly unverified until those tasks validate them.

The developer agent will install tools, configure the local environment, and validate it through the initial tasks. You review the architecture; no manual setup is required as a workflow step. If installation needs elevated permissions, account access, or credentials, the agent requests only that specific input or authorization and continues once it is available.

**Before continuing:** the architecture is agreed and the setup work is identified for the developer. There is still no requirement to have application code at this stage.

## 4. Turn the specification into implementation tasks

Ask:

> Read `AGENTS.md` and the agreed specifications. Create small, dependency-ordered tasks using `_docs/task-template.md`, store them under `_docs/tasks/`, and link them from `_docs/tasks.md`. Each task must have requirement links, observable acceptance criteria, and a verification plan. Refine the existing Draft task labeled `environment-setup` and the runnable application skeleton task for the selected architecture. The developer must perform installation and configuration in the task labeled `environment-setup`; the application skeleton task depends on it and adds a meaningful smoke check. Add feature tasks after these setup tasks. Do not implement yet.

Review the task list for missing requirements and unnecessary work. Ask the assistant to split tasks that are too large. Then prepare the first task:

> Act as the PM in `_docs/team/pm.md` and groom <task path>. Ask me about blocking questions. Once I have reviewed its scope and acceptance criteria, record my review and mark it Ready if the readiness gate is met.

Replace `<task path>` with the actual file created by the assistant. Repeat this preparation for later tasks before implementing them.

**Before continuing:** the first task is Ready, with a clear outcome and a way to check it. You do not need to finalize every future task before starting.

## 5. Let the developer set up and build the application

Ask:

> Read `AGENTS.md`. Act as the engineer in `_docs/team/software-engineer.md` and implement <ready task path>. Perform the agreed installation, configuration, or application implementation yourself. Run the applicable checks and record the results and handoff. Leave the task In review. Request only permissions, credentials, or decisions you cannot obtain yourself; do not hand me a setup checklist to execute.

Start with the task labeled `environment-setup`: the developer inspects the environment, installs missing tools, configures dependencies and local services as applicable, and verifies setup. Verify and complete it using step 6. Then groom and implement the application skeleton task: the developer creates the application skeleton, starts it, and runs its smoke check.

The agent records reproducible setup and run commands in [_docs/commands.md](_docs/commands.md) for future use. If setup or startup fails, the developer diagnoses and fixes it within the task. If the agent cannot access the required environment, keep the task Blocked and resolve access or authorization before continuing.

**Expected result after both tasks pass:** a configured development environment and a runnable application skeleton with documented, validated commands. It will gain the requested features as you implement the remaining tasks.

## 6. Verify the task and fix failures

Start a fresh assistant session for verification when practical, then ask:

> Read `AGENTS.md`. Act as QA in `_docs/team/qa-engineer.md` for <task path> and the current implementation. Verify every acceptance criterion and required check. Save evidence under `_docs/verification/` using the verification template. Report PASS, FAIL, or BLOCKED. Do not modify application code during this review.

Review the evidence and any manual checks that require your environment.

- **PASS:** if all completion conditions in `_docs/process.md` are met, mark the task Done in its file and the backlog, or ask the assistant to do so.
- **FAIL:** ask the engineer to fix the reported failures within the agreed scope, then run QA again against the changed code.
- **BLOCKED:** resolve the missing decision or grant the required access; have the developer handle outstanding installation or configuration, then repeat verification. Keep the task incomplete until it can be checked.

Ask the assistant to commit completed work if you want it to manage commits, or commit it yourself.

## 7. Repeat until the first release works

For each next task whose dependencies are Done, repeat the same cycle: groom and review it, mark it Ready, implement it, and verify it. Continue until all tasks for the agreed first release are Done.

Then run the application using `_docs/commands.md` and exercise the complete user journeys from `_docs/plan.md`. Confirm that the features work together and that the required regression checks pass. Record any gaps as defects or follow-up tasks and verify their fixes.

**You have reached working application code when:** the agreed first-release tasks are Done, the application starts using the documented instructions, its specified user journeys work, and required checks have passing evidence. Packaging, distribution, or deployment should be included as explicit tasks if they are needed for your intended users to access it.

When you want to change the product, update the specification and affected tasks before implementing the new behavior.

## Where the project information lives

| Document | What you use it for |
| --- | --- |
| [AGENTS.md](AGENTS.md) | Give a new AI session the project rules and document map |
| [_docs/plan.md](_docs/plan.md) | Define what the application must do |
| [_docs/architecture.md](_docs/architecture.md) | Record how it will be built |
| [_docs/commands.md](_docs/commands.md) | Find exact setup, run, and verification instructions |
| [_docs/tasks.md](_docs/tasks.md) | Find the next task and track progress |
| [_docs/task-template.md](_docs/task-template.md) | Specify each task before implementation |
| [_docs/process.md](_docs/process.md) | Check readiness, completion, and change rules |
| [_docs/testing-guidelines.md](_docs/testing-guidelines.md) | Define how to verify behavior |
| [_docs/prompts.md](_docs/prompts.md) | Find additional reusable prompts |
| [_docs/team/](_docs/team/) | Give the assistant PM, engineer, QA, or coordinator responsibilities |
| [_docs/templates/](_docs/templates/) | Create decision and verification records |

Replace angle-bracket placeholders in prompts and documents with project facts. Resolve blocking placeholders before marking a task Ready; a task may explicitly deliver configuration that does not exist yet.

The local Markdown backlog is the default. If you move to an issue tracker, record its location in `_docs/tasks.md` and archive the local backlog so there is one authoritative task list.

`CLAUDE.md` points to `AGENTS.md`. For other assistants, explicitly ask them to read `AGENTS.md` if they do not discover it automatically. The role files and prompts describe a workflow; they do not launch agents or automate it. Optional bounded loops are described in `_docs/process.md`.

## Inspiration

Based on Alexey Grigorev’s [AI-Native Development: Specifications, Loop and Graph Engineering](https://aishippingblog.com/p/ai-native-development-specifications), adapted into a local-first, language- and platform-agnostic template with requirement links and verification records.
