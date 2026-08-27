**Source ID**: SRC-SLACK-59

# Slack Thread: Async Batch Scheduler
**Channel**: #cipherdoc
**Date**: 2026-08-20

---

**[2026-08-20 09:39] Bob**: Starting the async job scheduler for the batch API. The sync path saturates once a few concurrent jobs show up — need something that can accept work without blocking the API.

**[2026-08-20 09:50] Charlie**: So jobs get queued and processed off the request thread?

**[2026-08-20 09:52] Bob**: Right. Scheduler takes the batch, hands back a handle, and processes in the background. Keeping it local for now — no external queue service.

**[2026-08-20 10:03] Alice**: Does this replace the existing sync batch path or sit beside it?

**[2026-08-20 10:59] Bob**: Beside it for now. Sync stays for simple single-job calls; async is for concurrent load.

**[2026-08-20 11:15] Diana**: Once the shell is in, I'll need a way to pile concurrent jobs on it. Workers can come in a follow-up.

**[2026-08-20 11:17] Bob**: Agreed. Getting the scheduler shell working first; workers next.
