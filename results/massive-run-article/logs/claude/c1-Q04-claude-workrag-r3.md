# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

## Answer

**Work item:** T022 / CIPH-32 — Storage Quota Management ("Halt batch writes when disk quota is hit"), tracked under **WS-07: Data Persistence, Encryption, and Secure Storage** (Status `in_progress`, P1, Owner Bob / Charlie, Project CipherDoc, Last Updated 2026-09-22).

### Current status as of 2026-09-22

**Reopened and active — not done.** In WS-07 the task list still shows `T022` (mapped to CIPH-32) unchecked, and Active Work records it as **Reopened/active**: the storage monitor halts processing too aggressively when ~500MB remains free, and Bob is refactoring the loop to allow a 10% buffer tolerance before halting. The ClickUp record CIPH-32 carries **Status: Active (Reopened)**, Assignee Evan, Priority Normal.

The earlier "done" was the hard-halt acceptance: on **2026-08-06** Diana verified in `#cipherdoc` that she filled the disk with dummy data and confirmed the engine halts writes at the configured 500MB floor, and called it done. The validation doc "Storage Quota Halt Validation" (SRC-GDOC-36, DOC-2036, owner Diana, 2026-08-06) recorded the Outcome as *Completed — quota-halt behavior verified for the configured threshold checked here*, and explicitly scoped out redefining quota policy or introducing a soft buffer above the hard halt.

### Later evidence that reopened it

- **2026-09-15 — Evan, `#cipherdoc` (SRC-SLACK-23):** reopened the task because *production-like batches are tripping the 500MB hard halt before they've done any useful work — it's too aggressive for how these jobs actually run.* Diana concurred that a flat cutoff doesn't account for how much a batch has already written before it approaches the line.
- **Root cause** as stated by Bob on 2026-09-18: the hard cutoff had **no soft buffer**.
- **2026-09-15 — CMT-2026-09-003 (Evan, correction, WS-07/T022):** ops capacity planning offline determined the **production quota baseline is 2GB free disk, not 500MB**; keep the 10% buffer refactor but retarget halt thresholds to the 2GB baseline before re-verifying in clinic VMs.

### Buffer change underway

The disk-usage monitor is being **refactored from the hard 500MB halt to a 10% buffer tolerance above quota**, so writes are not stopped abruptly at the hard limit.

- **2026-09-18 — Bob (CIPH-32 activity, "Buffer Refactor", Active (Reopened)):** refactored the disk-usage monitor to allow a 10% buffer above quota, since the reopened hard halt was tripping too aggressively on production-like batches.
- **2026-09-18 — Evan:** re-tested against the same production-like batches that previously tripped it and saw **no premature halts**.
- **Revised acceptance criteria on CIPH-32:** monitor halts writes at the configured quota during batch runs; halt behavior tolerates a 10% buffer above quota rather than stopping abruptly at the hard limit; refactored monitor no longer trips prematurely on production-like batch sizes.
- **Threshold retarget:** per CMT-2026-09-003, WS-07 Active Work now sets the **production quota baseline at 2GB free disk (not 500MB) with 10% buffer tolerance before halt**, to be re-verified in clinic VMs.
- **Next update needed (WS-07):** *quota monitor buffer refactor verification* (alongside the handshake high-latency retest plan) — i.e. the refactor is implemented and smoke-re-tested, but formal verification against the 2GB baseline is still outstanding, which is why T022 remains open.

### Records cited

- `work-states/WS-07-storage.md` (path = work-state) — status, task list, Active Work, Next Update Needed
- `work-states/comments/2026-09.md` — CMT-2026-09-003 (2026-09-15, Evan, correction)
- `med-synth/tasks/CIPH-32-Storage-Quota-Management.md` — SRC-CU-CIPH-32, status, description, acceptance criteria, 2026-09-18 Buffer Refactor activity
- `med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md` — SRC-SLACK-23, verification, reopen, refactor, re-test
- `med-synth/documentation/sources/2026-08-06-Storage-Quota-Halt-Validation.md` — SRC-GDOC-36 / DOC-2036, original hard-halt acceptance
- `med-synth/documentation/sources/2026-08-05-Storage-Quota-Management-Review.md` — SRC-GDOC-16 / DOC-2016, monitor-loop background
- `med-synth/communication/sources/slack/2026-08-04-storage-quota-monitor.md` — SRC-SLACK-22, original 500MB hard floor design
