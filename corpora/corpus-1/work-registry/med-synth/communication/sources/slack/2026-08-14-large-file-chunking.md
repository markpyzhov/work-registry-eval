**Source ID**: SRC-SLACK-42

# Slack Thread: Large File Chunking
**Channel**: #cipherdoc
**Date**: 2026-08-14

---

**[2026-08-14 11:30] Charlie**: Starting on stream-based chunked reads for large PDFs. Loading the whole document into memory before redacting is what's causing the pressure on bigger files.

**[2026-08-14 11:32] Bob**: Makes sense. What's the plan for entities that span a chunk boundary — like an address that gets split across two reads?

**[2026-08-14 11:58] Charlie**: Adding a small overlap window between chunks so anything near a boundary gets caught on both sides instead of falling through the gap.

**[2026-08-14 11:59] Alice**: Does this help or hurt the multi-threading work?

**[2026-08-14 12:04] Charlie**: Should help — lower memory per worker means we're not as constrained on how many workers we can run at once.

**[2026-08-14 12:22] Bob**: Good. Let me know when it's ready for a real large-file test.
