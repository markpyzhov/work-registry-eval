**Source ID**: SRC-SLACK-43

# Slack Thread: Large File Chunking Reopen
**Channel**: #cipherdoc
**Date**: 2026-08-18

---

**[2026-08-18 10:30] Bob**: Reopening large-file chunking. On long-running batches with files over 2GB, memory is still leaking even though the chunked-read path is supposedly done.

**[2026-08-18 10:31] Charlie**: That's odd, chunking should mean each buffer gets dropped once we move past it.

**[2026-08-18 10:41] Bob**: It's not the page buffers themselves — something else is holding a reference and keeping them from being freed.

**[2026-08-18 11:08] Diana**: I can reproduce it in QA too. Memory climbs steadily and the process eventually gets killed on the larger inputs.

**[2026-08-18 11:20] Charlie**: I'll dig into what's still holding those references. Reopening this until we find it.
