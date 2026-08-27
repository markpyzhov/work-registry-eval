# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

## Storage quota monitoring (T022 / CIPH-32) — status as of 2026-09-22

### Current status: reopened and active (not done)
`WS-07-storage.md` — the authoritative Work State, last updated 2026-09-22 — lists `T022` as **unchecked** in the Task List and under **Active Work** as "**Reopened/active**." The ClickUp task carries **Status: Active (Reopened)**, assignee **Evan**. The 2026-09-22 daily brief repeats it: "2GB production baseline + 10% buffer refactor still in progress."

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-32-Storage-Quota-Management.md` (`SRC-CU-CIPH-32`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### How it was originally marked done
- **2026-08-04** (`SRC-SLACK-22`): Evan implemented a disk-usage monitor loop with a **hard 500MB free-space floor**; engine pauses and alerts below it.
- **2026-08-05** (`SRC-GDOC-16`, DOC-2016): loop in place but "not yet a signed-off gate" — nobody had confirmed it actually halts writes.
- **2026-08-06** (`SRC-SLACK-23`, `SRC-GDOC-36` / DOC-2036): Diana filled the disk with dummy data, confirmed the engine halts writes at the configured 500MB floor, and **called it done**. That validation explicitly scoped itself narrowly — it "does not redefine the quota policy or introduce a soft buffer above the hard halt."

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-storage-quota-monitor.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-05-Storage-Quota-Management-Review.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-06-Storage-Quota-Halt-Validation.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md`

### What later evidence reopened it
**2026-09-15, Evan, in the same Slack thread (`SRC-SLACK-23`)**: "Reopening this. Production-like batches are tripping the 500MB hard halt before they've done any useful work — it's too aggressive for how these jobs actually run." Diana concurred that a flat cutoff doesn't account for how much a batch has already written before nearing the line. The root cause named by Bob was the **hard cutoff having no soft buffer**.

The Aug 6 validation had only proven the halt fires at the configured threshold — it never tested whether that threshold was right for real batch sizes, which is exactly what failed later.

### The buffer change underway
1. **Buffer refactor (Bob, 2026-09-18, `SRC-SLACK-23` + CIPH-32 activity history)**: the disk-usage monitor was refactored to allow a **10% buffer tolerance above the quota** instead of the hard 500MB halt. Evan re-tested on 2026-09-18 against the same production-like batches — no premature halts.
2. **Baseline correction (`CMT-2026-09-003`, Evan, 2026-09-15, offline ops capacity planning)**: the production quota baseline is **2GB free disk, not 500MB**. Direction: keep the 10% buffer refactor but **retarget halt thresholds to the 2GB baseline before re-verifying in clinic VMs**. This was applied to WS-07 Active Work.

So the change in flight is: **2GB free-disk production baseline with 10% buffer tolerance**, replacing the original 500MB hard halt. Despite the 2026-09-18 re-test passing, the task remains open because the retarget to 2GB and the clinic-VM re-verification have not landed.

Files: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-003`), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-15-daily-brief.md`

### Open follow-ups
- WS-07 "Next Update Needed": **quota monitor buffer refactor verification**.
- 2026-09-15 brief follow-up item: **clinic VM re-verify plan after the 2GB quota retarget**.
- Priority ranking: WS-07/T022 sits third in the 2026-09-15 priority order, behind the release-gate items (T005/T029) and the MedFirst OOM (T031).

Note: T022's owner shifts across records — CIPH-32 assigns Evan, while WS-07 Active Work credits **Bob** with the refactor loop and WS-07 as a whole is owned by Bob/Charlie. Evan reopened and re-tested; Bob did the refactor.
