**Source ID**: SRC-SLACK-22

# Slack Thread: Storage Quota Management Design
**Channel**: #cipherdoc
**Date**: 2026-08-04

---

**[2026-08-04 09:30] Evan**: Starting on storage quota management. We need to keep `cipherdoc` from filling up the disk on these workstations, especially on large batch jobs.

**[2026-08-04 09:39] Evan**: Implementing a disk-usage monitor loop. It'll check available space before starting any new redaction job.

**[2026-08-04 09:41] Alice**: What's the threshold?

**[2026-08-04 10:08] Evan**: Going with a hard 500MB floor for now. If free space drops below that, the engine pauses and alerts the user.

**[2026-08-04 10:26] Diana**: We also need a way to clear the cache — the `/tmp` folder doesn't always clean up properly after a crash.

**[2026-08-04 10:41] Evan**: I'll add a purge-cache option and run a sweep on startup too.

**[2026-08-04 10:44] Evan**: @Bob, can we get a hook in the `FileStreamer` to report current disk usage for the active job?

**[2026-08-04 11:30] Bob**: Sure, I'll add a `get_quota_usage()` method to the stream controller.
