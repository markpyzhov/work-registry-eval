**Source ID**: SRC-SLACK-49

# Slack Thread: Memory Leak Tracemalloc Patch
**Channel**: #cipherdoc
**Thread opened**: 2026-08-21
**Last activity**: 2026-08-23

---

**[2026-08-21 09:00] Charlie**: Switching to `tracemalloc` for the leak hunt since the usual profiler is a no-go on the offline lab box. Kicking off a fresh capture now.

**[2026-08-21 11:05] Charlie**: Already got something. The `tracemalloc` output shows we're holding onto the full page-tree in `RedactionEngine` even after the document object is closed.

**[2026-08-21 11:50] Bob**: That lines up with the hotspot list from earlier this week. I'll start on a patch tonight.

**[2026-08-23 09:45] Bob**: Patch is in. Added explicit cleanup so the context manager actually releases the page-tree reference instead of just closing the file handle.

**[2026-08-23 09:47] Diana**: Just finished a 6-hour soak test with the new build. Memory usage is flat as a pancake after the initial load. :pancake:

**[2026-08-23 10:41] Alice**: Huge relief. Is this on top of the buffer-release fix from the large-file chunking rework, or a separate code path?

**[2026-08-23 10:43] Bob**: Same family of fix — builds on the chunking buffer-release work. PR #84 is merged.

**[2026-08-23 10:44] Evan**: On it.

**[2026-08-23 10:46] Evan**: Rolling this out to the dev clusters. @Charlie thanks for the tracemalloc deep dive.
