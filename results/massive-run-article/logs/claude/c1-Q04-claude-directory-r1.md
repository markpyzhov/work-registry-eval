# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

## Storage quota monitoring (T022 / CIPH-32) — status as of 2026-09-22

**Current status: reopened and still active — not done.** The work-state lists `T022` as unchecked in the WS-07 task list and under **Active Work**; the ClickUp task carries status **Active (Reopened)**, assignee Evan; the registry index groups T022 under "Active / Reopened" as "quota buffer."
Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-32-Storage-Quota-Management.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`

### How it was originally closed
- 2026-08-04: Evan implemented a disk-usage monitor loop with a **hard 500MB free-space floor**; below it the engine pauses and alerts. Bob added a `get_quota_usage()` hook on the stream controller. (`SRC-SLACK-22`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-storage-quota-monitor.md`; `SRC-GDOC-16`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-05-Storage-Quota-Management-Review.md` — which explicitly said the loop was "not yet a signed-off gate")
- 2026-08-06: Diana filled the disk with dummy data, confirmed the engine halts writes at the configured 500MB floor, and called it done. The validation doc accepted only that narrow behavior and explicitly stated it did **not** redefine quota policy or introduce a soft buffer. (`SRC-SLACK-23`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md`; `SRC-GDOC-36`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-06-Storage-Quota-Halt-Validation.md`)

### Later evidence that reopened it
- **2026-09-15 — Evan reopened it in Slack:** production-like batches were tripping the 500MB hard halt *before doing any useful work* — too aggressive for how those jobs actually run. Diana concurred that a flat cutoff ignores how much a batch has already written. Root cause per Bob: the hard cutoff had no soft buffer. (`SRC-SLACK-23`)
- **2026-09-15 — `CMT-2026-09-003` (Evan, correction):** ops capacity planning offline established that the **production quota baseline is 2GB free disk, not 500MB**; keep the 10% buffer refactor but retarget halt thresholds to the 2GB baseline before re-verifying in clinic VMs. Applied to WS-07/T022 Active Work. (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`)

### Buffer change underway
Bob is refactoring the monitor to use a **10% buffer tolerance above the quota** instead of the hard 500MB halt, with the halt thresholds retargeted to the **2GB production baseline** (i.e., 2GB + 10% buffer tolerance). CIPH-32's acceptance criteria now require that halt behavior tolerate the 10% buffer rather than stopping abruptly at the hard limit and that the refactored monitor no longer trip prematurely on production-like batch sizes; the ClickUp activity log records Bob's 2026-09-18 "Buffer Refactor."

Progress so far: on 2026-09-18 Evan re-tested against the same production-like batches that had failed and saw **no premature halts** (`SRC-SLACK-23`). That re-test is not yet a closure — the 2026-09-22 brief still reports "2GB production baseline + 10% buffer refactor **still in progress**," WS-07's "Next Update Needed" is quota-monitor buffer refactor verification, and the outstanding follow-up is the **clinic VM re-verify plan after the 2GB retarget**.
Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-15-daily-brief.md`

### One-line summary
Marked done 2026-08-06 on a narrow hard-halt check at 500MB → reopened 2026-09-15 because that flat cutoff fired prematurely on production-like batches, compounded by an ops correction that the real production baseline is 2GB → currently active with Bob's 10% buffer-tolerance refactor (Evan's 2026-09-18 re-test clean, clinic VM re-verification against the 2GB + 10% thresholds still pending).
