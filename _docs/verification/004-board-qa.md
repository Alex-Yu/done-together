#004 board independent QA

Verdict: PASS. Date:2026-10-29. Separate QA subagent; no implementation fixes.
Implementation: `067addc7eda122736893d17d5ca4aff7ce1a2885`; reviewed records-only tip `0d1245ea72d337c3bf7f09fb25f3c505ff43dce7` on task/004-board. [Task](../tasks/004-board.md).

| AC | Independent evidence | Verdict |
| --- | --- | --- |
|001| Real scoped children/empty guidance; internal mixed-state provider yields correct columns and textual states. HTTP fixture query cannot select synthetic work. Two-household and unauthorized boundaries pass |PASS|
|002| Native engines inspect four directly rendered cards, old active/completed entries and no collapsed details. Actual approval/week filtering remains008 |PASS|
|003| Verified member landing enters board; native keyboard unlock→protected settings→board revisits stored children; affected PIN tests retain authority boundary. Chore/review controls remain005–007 |PASS|
|004| Installed Chrome156.0.8078.48/Firefox159.0 native100%1280×720/DPR1 and200%640×360/DPR2, keyboard/focus/labeled PIN/text states/no overflow. Four fresh screenshots visually inspected: long names/cards wrap, readable with ordinary vertical scrolling |PASS|
|005| Five board cases execute actual household isolation, locked mutation denial, passive read/no-touch/expired board visibility and generic DEBUG DB-failure/retry without private details;20 affected PIN regressions pass |PASS|

Commands: `uv run pytest tests/integration/test_board.py tests/integration/test_pins.py -q --tb=short`:25passed/11.02s. With documented loopback geckodriver, `RUN_NATIVE_BOARD=1 uv run pytest tests/e2e/test_board_native.py -q -s --tb=short`:1passed/19.78s, four native cases. Django check/drift and Ruff lint/format:exit0,111files formatted/no changes. `git diff --check`:exit0. Shared disposable PostgreSQL suites sequential; no schema/dependency change.

Findings:None. Production read-model provider returns empty work; synthetic mixed data injected only inside tests. Unchanged credential/email/real61s idle/restart evidence from003 at `d18a01c0d5d22e4ed21ce7a4bf651a673c1cde1c` retained after delta inspection; fresh PIN/board regressions cover changed integration. Full integrated regression remains010. Driver stopped exit0; test server/browser contexts closed; PG17 retained.

004attempt1/3; batch2 completions3/10 before integration. In review for administrative completion; no QA Done/merge/push.
