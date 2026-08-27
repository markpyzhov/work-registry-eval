**Source ID**: SRC-SLACK-61

# Slack Thread: Async Batch I/O Race
**Channel**: #cipherdoc
**Date**: 2026-08-25

---

**[2026-08-25 10:20] Diana**: Blocker on the async batch path. Under concurrent load the workers hit an I/O race and throughput drops — roughly 10% versus the sync baseline.

**[2026-08-25 10:21] Bob**: Is that the scheduler shell or the workers we just added?

**[2026-08-25 10:23] Diana**: The workers. Scheduler alone was fine; once concurrent workers share I/O with the existing multi-thread batch pool, the race shows up.

**[2026-08-25 11:48] Charlie**: That pool is the multi-thread path. Mixing it with async workers without coordinating I/O was going to bite us.

**[2026-08-25 12:50] Alice**: Then we stop here. I have to leave the async batch work blocked until the race with the multi-thread pool is sorted. A 10% hit is not shippable.

**[2026-08-25 12:51] Bob**: Ok.

**[2026-08-25 12:52] Bob**: Fair. I'll hold further async work until we understand the interaction with that pool.

**[2026-08-25 12:54] Diana**: I'll capture the repro steps so we can re-run once there's a candidate fix.
