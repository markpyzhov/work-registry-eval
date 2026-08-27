# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

## Storage quota monitoring (T022 / CIPH-32) — status as of 2026-09-22

### Current status: Reopened and active — not done

The Work State authoritative as of 2026-09-22 lists `T022` as an **unchecked** task item, and the ClickUp task carries status **"Active (Reopened)"**, assignee **Evan**, priority Normal.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (Last Updated 2026-09-22; `- [ ] T022 (mapped to CIPH-32)`, plus two Active Work entries)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-32-Storage-Quota-Management.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (as-of 2026-09-22T12:00:00Z; lists T022 "quota buffer" under **Active / Reopened**)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` — "2GB production baseline + 10% buffer refactor still in progress"

### The original hard-halt check that closed it

On **2026-08-06** Diana verified the disk monitor by filling the disk with dummy data and confirming the engine halts writes at the configured **500MB** floor, and called it done. Evan agreed but said he'd watch for threshold logic drifting. The accompanying validation doc recorded the outcome as "Completed" but explicitly scoped itself: it did **not** redefine quota policy or introduce a soft buffer above the hard halt.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md` (`SRC-SLACK-23`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-06-Storage-Quota-Halt-Validation.md` (`SRC-GDOC-36`, DOC-2036, owner Diana)

Background on the original design (hard 500MB floor, monitor loop, `get_quota_usage()` hook in the stream controller): `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-04-storage-quota-monitor.md` (`SRC-SLACK-22`) and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-05-Storage-Quota-Management-Review.md` (`SRC-GDOC-16`).

### Later evidence that reopened it

1. **2026-09-15 — production-like batches trip the hard halt.** Evan reopened the item: production-like batches were hitting the 500MB hard halt *before doing any useful work* — too aggressive for how those jobs actually run. Diana concurred that a flat cutoff doesn't account for how much a batch has already written before nearing the line. (`SRC-SLACK-23`)
2. **2026-09-15 — ops capacity-planning correction (`CMT-2026-09-003`, author Evan).** Offline ops capacity planning established that the **production quota baseline is 2GB free disk, not 500MB**. Direction: keep the 10% buffer refactor but retarget halt thresholds to the 2GB baseline before re-verifying in clinic VMs. Disposition: applied to WS-07/T022 Active Work.
   - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`
   - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-15-daily-brief.md`

So the 2026-08-06 "done" was invalidated on two axes: the halt *behavior* (hard cutoff vs. soft buffer) and the halt *threshold* (500MB vs. 2GB).

### Buffer change underway

Bob is refactoring the disk-usage monitor to use a **10% buffer tolerance above the quota** instead of the hard halt. Root cause identified: the hard cutoff had no soft buffer.

- **2026-09-18** — Bob landed the refactor to the 10% buffer tolerance (`SRC-SLACK-23`; also recorded as CIPH-32 Activity History "Buffer Refactor", 2026-09-18, Bob).
- **2026-09-18** — Evan re-tested against the same production-like batches that had tripped it before: **no premature halts** (`SRC-SLACK-23`).
- Revised acceptance criteria on CIPH-32: monitor halts at configured quota; halt tolerates a 10% buffer above quota rather than stopping abruptly at the hard limit; refactored monitor no longer trips prematurely on production-like batch sizes.

### Why it's still open despite the 2026-09-18 re-test

The work state's Active Work carries the ops correction alongside the refactor: the production baseline is **2GB free disk with 10% buffer tolerance before halt**, and the thresholds must be retargeted to that baseline and **re-verified in clinic VMs** — which had not happened as of 2026-09-22. WS-07's "Next Update Needed" is explicitly "Quota monitor buffer refactor verification" (with the handshake retest plan), and the 2026-09-15 brief lists "Clinic VM re-verify plan after 2GB quota retarget" as outstanding.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (Active Work, Next Update Needed)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-15-daily-brief.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

One discrepancy worth flagging: WS-07 Active Work names **Bob** as the one refactoring the loop (consistent with the 2026-09-18 Slack message and the CIPH-32 activity entry), while the CIPH-32 task record lists **Evan** as assignee (he opened the reopen and ran the re-test). Both are cited as-is above.
