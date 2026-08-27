**Source ID**: SRC-SLACK-48

# Slack Thread: Memory Leak Hotspots
**Channel**: #cipherdoc
**Date**: 2026-08-17

---

**[2026-08-17 10:16] Bob**: Running into some weirdness with memory. The long-running container is hitting the memory limit after about 4 hours of processing. Looks like a slow leak.

**[2026-08-17 10:34] Charlie**: Is it in the engine or the API layer? If we're not clearing the regex caches, that could be it.

**[2026-08-17 10:37] Bob**: I'm seeing the RSS climb even when the API is idle after a batch. I suspect something in the `DocumentProcessor` isn't closing file handles or clearing buffers.

**[2026-08-17 10:38] Charlie**: Ugh.

**[2026-08-17 10:50] Diana**: I can confirm this on the staging node. I've been watching the Grafana dashboard and it's a steady 45-degree angle upward. No dips.

**[2026-08-17 11:15] Evan**: I've bumped the limit to 2GB temporarily so we don't keep crashing, but we need a real fix. @Bob are you using `tracemalloc` yet?

**[2026-08-17 11:16] Bob**: Just starting a run with it now. I'll dump the snapshots and see where the allocations are sticking.

**[2026-08-17 11:17] Alice**: @Bob if this is a deep issue in the engine core, we might need to pull Charlie in full-time on this.

**[2026-08-17 11:18] Charlie**: Already looking at the `pdfminer` wrappers. We've had issues with its object recycling before.
