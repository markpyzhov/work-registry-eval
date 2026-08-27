# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

I have sufficient evidence. Here is the complete answer.

---

## Storage quota monitoring (T022 / CIPH-32) — status as of 2026-09-22

### Current status: Reopened and active — not done

The Work State `WS-07: Data Persistence, Encryption, and Secure Storage` (Status: `in_progress`, P1, Owner: Bob / Charlie, Last Updated 2026-09-22) still lists `T022` (mapped to CIPH-32) as **unchecked** in its Task List, and describes it under Active Work as:

> "**T022 / CIPH-32**: **Reopened/active**. Storage monitor halts processing too aggressively when ~500MB remains free; Bob is refactoring the loop to allow a 10% buffer tolerance before halting."

The ClickUp task CIPH-32 ("Halt batch writes when disk quota is hit", assignee Evan) carries status **Active (Reopened)**.

### How it was marked done, and what reopened it

**The hard-halt check that closed it (2026-08-06).** Diana's validation (`SRC-GDOC-36`, DOC-2036, "Storage Quota Halt Validation") confirmed the disk-usage monitor actually stops further writes at the configured quota rather than merely running. In Slack `#cipherdoc` (`SRC-SLACK-23`) she wrote on 2026-08-06 that she filled the disk with dummy data, confirmed the engine halts writes at the configured 500MB floor, and called it done. That document explicitly scoped itself narrowly: it did not redefine quota policy or introduce a soft buffer above the hard halt.

**Later evidence that reopened it — two distinct items:**

1. **Premature halts on production-like batches (2026-09-15, `SRC-SLACK-23`).** Evan reopened the task: production-like batches were tripping the 500MB hard halt *before they had done any useful work* — too aggressive for how those jobs actually run. Diana concurred that a flat cutoff doesn't account for how much a batch has already written before approaching the line. The root cause Bob identified was the hard cutoff having no soft buffer.

2. **A production baseline correction (2026-09-15, `CMT-2026-09-003`, author Evan, type `correction`).** Ops capacity planning offline established that the **production quota baseline is 2GB free disk, not 500MB**. The instruction was to keep the 10% buffer refactor but retarget halt thresholds to the 2GB baseline before re-verifying in clinic VMs. This is reflected in WS-07 Active Work as: "Ops capacity planning sets production quota baseline at **2GB** free disk (not 500MB) with 10% buffer tolerance before halt."

### The buffer change underway

The monitor is being **refactored from a hard halt at the quota floor to a 10% buffer tolerance above quota**, so it no longer stops abruptly at the hard limit.

- **2026-09-18 (CIPH-32 activity history, Bob — "Buffer Refactor"):** refactored the disk-usage monitor to allow a 10% buffer above quota, since the reopened hard halt was tripping too aggressively on production-like batches.
- **2026-09-18 (`SRC-SLACK-23`):** Bob replaced the hard 500MB halt with the 10% buffer tolerance; Evan re-tested against the same production-like batches that had failed and reported no premature halts.
- **Revised acceptance criteria on CIPH-32:** the monitor halts writes at the configured quota during batch runs; halt behavior tolerates a 10% buffer above quota rather than stopping abruptly at the hard limit; and the refactored monitor no longer trips prematurely on production-like batch sizes.
- **Threshold retarget still pending:** per `CMT-2026-09-003`, the buffer refactor must be retargeted to the **2GB** production baseline (with the 10% buffer) and re-verified in clinic VMs. WS-07's "Next Update Needed" is "Quota monitor buffer refactor verification and handshake high-latency retest plan" — so Evan's 2026-09-18 ad-hoc re-test has not yet been converted into a formal sign-off against the corrected 2GB baseline, which is why T022 remains open as of 2026-09-22.

### Records cited

- `work-states/WS-07-storage.md` (`path = work-state`) — authoritative status, Task List, Active Work, Next Update Needed
- `work-states/comments/2026-09.md` — `CMT-2026-09-003` (WS-07/T022, correction, Evan, 2026-09-15)
- `med-synth/tasks/CIPH-32-Storage-Quota-Management.md` — `SRC-CU-CIPH-32` (status, description, acceptance criteria, activity history)
- `med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md` — `SRC-SLACK-23` (2026-08-06 done call; 2026-09-15 reopen; 2026-09-18 buffer refactor and re-test)
- `med-synth/documentation/sources/2026-08-06-Storage-Quota-Halt-Validation.md` — `SRC-GDOC-36` (the hard-halt check, and its explicit out-of-scope note on soft buffers)
- `med-synth/documentation/sources/2026-08-05-Storage-Quota-Management-Review.md` — `SRC-GDOC-16` (monitor loop landed 2026-08-04, not yet a signed-off gate)
- `med-synth/communication/sources/slack/2026-08-04-storage-quota-monitor.md` — `SRC-SLACK-22` (original 500MB hard floor decision)
- `med-synth/communication/sources/fireflies/2026-08-05-*` — `SRC-MEET-07` (weekly sync: monitor in, halt sign-off pending)
