**Source ID**: SRC-SLACK-12

# Slack Thread: Batch Failure Strategy (Fail-Closed)
**Channel**: #cipherdoc
**Thread opened**: 2026-06-12
**Last activity**: 2026-07-16

---

**[2026-06-12 10:09] Bob**: For the batch fail-closed question, we need to decide what happens if the engine crashes halfway through a 1,000-file batch. Do we keep the successful ones?

**[2026-06-12 10:26] Charlie**: Absolutely not. If we can't guarantee 100% of the batch is safe, we should fail-closed. No partial exports.

**[2026-06-12 10:28] Bob**: Agreed. Drafting the plan now. If any worker node throws an unhandled exception, we abort the entire job and purge the output buffer.

**[2026-06-12 10:43] Charlie**: I've added an exception hook to the core engine. It catches low-level segfaults and signals the controller to stop all active streams.

**[2026-06-12 11:23] Bob**: Implementation complete. Added an atomic rename step at the very end — the output folder stays empty until the last file is verified.

**[2026-06-12 12:53] Diana**: What about logs? We need to know *why* it failed.

**[2026-06-12 13:16] Bob**: Crash report gets written to a separate `audit_log.json` before the shutdown. Captures the stack trace and the filename that triggered the fault.

**[2026-06-12 13:17] Charlie**: Perfect. :lock:

**[2026-06-12 13:19] Alice**: Thanks.

**[2026-07-16 09:30] Diana**: QA pass on fail-closed is done — confirmed no output file gets written on failure and the temp files get securely deleted. Signing off before the encryption and offline work start relying on this.

**[2026-07-16 09:31] Bob**: Calling this done.
