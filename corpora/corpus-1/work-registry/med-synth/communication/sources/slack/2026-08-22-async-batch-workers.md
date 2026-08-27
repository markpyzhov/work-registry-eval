**Source ID**: SRC-SLACK-60

# Slack Thread: Async Batch Workers
**Channel**: #cipherdoc
**Date**: 2026-08-22

---

**[2026-08-22 14:21] Bob**: The async processing is looking good. I've integrated the progress callbacks so the GUI can show a real-time percentage.

**[2026-08-22 14:30] Diana**: I'm seeing some race conditions when two different users try to process the same file simultaneously. The lock isn't being released correctly.

**[2026-08-22 15:00] Bob**: Ah, I see it. I'm using the filename as the key in the lock manager, but not accounting for the user ID.

**[2026-08-22 15:02] Charlie**: Why not use the file hash instead? That way even if they have different filenames but it's the same content, we don't process it twice.

**[2026-08-22 15:12] Bob**: Good idea. I'll swap out the keys for the SHA-256 hash.

**[2026-08-22 15:17] Charlie**: Perfect.

**[2026-08-22 15:35] Alice**: @Bob how does this affect the multi-threading work Charlie did?

**[2026-08-22 16:56] Bob**: They should play well together. The scheduler distributes the *files* to different workers, and each worker uses Charlie's multi-threaded engine to process the *internal* pages.
