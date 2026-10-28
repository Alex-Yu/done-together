# Backlog

Authoritative backlog: this file and the task files it links until origin detection selects GitHub mode under `_docs/process.md`.

Backlog mode / origin repository: Not yet checked
Pending issue synchronization: None

Two Draft bootstrap tasks are provided below. After choosing the architecture, refine their scope and acceptance criteria before marking them Ready. Feature tasks are added from the product specification.

| Labels | Task file | Status | Dependencies |
| --- | --- | --- | --- |
| `environment-setup` | [Set up the development environment](tasks/environment-setup.md) | Draft | Product scope and architecture reviewed |
| — | [Create a runnable application skeleton](tasks/application-skeleton.md) | Draft | `environment-setup` |

The predefined `environment-setup` label identifies environment preparation independently of task numbering. Preserve it when moving tasks to an issue tracker. The application skeleton task depends on the completed task with this label.

Create task files as `_docs/tasks/001-short-title.md` using `_docs/task-template.md`. Keep task status here consistent with the task file. See `_docs/process.md` for valid states.

The developer executes setup as ordinary tasks: first install and configure the development environment, then build and verify the application skeleton. Users review choices and provide required authorization or credentials; they are not assigned manual installation steps. Later tasks should deliver small, verifiable slices of behavior.

If `origin` points to GitHub, record its issue tracker as authoritative here and add issue links to this index. Keep task files synchronized with those issues; this table becomes an index/checkpoint rather than a separate backlog. Otherwise retain the local backlog. Follow the synchronization policy in `_docs/process.md`.
