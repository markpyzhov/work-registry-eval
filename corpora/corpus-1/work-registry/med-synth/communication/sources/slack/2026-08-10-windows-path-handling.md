**Source ID**: SRC-SLACK-36

# Slack Thread: Windows Path Handling
**Channel**: #releases
**Date**: 2026-08-10

---

**[2026-08-10 10:19] Evan**: Windows builds have been failing on path separators — the ingestion logic has backslash assumptions baked in that don't hold up on Windows.

**[2026-08-10 10:34] Bob**: Quick search-and-replace for the separator, or something more thorough?

**[2026-08-10 10:39] Evan**: More thorough — moving the path handling to be OS-aware instead of hardcoded, so this doesn't come back the next time we touch it.

**[2026-08-10 10:41] Bob**: LGTM.

**[2026-08-10 12:46] Charlie**: What about the temp directory? I remember some older code assuming a Linux-style path there too.

**[2026-08-10 13:00] Evan**: Already on it. Fixing that in the same pass so it respects the OS-level temp location instead of guessing.

**[2026-08-10 13:01] Alice**: How's this looking for a first test build?

**[2026-08-10 13:03] Evan**: Once the path fix holds up under test, I should be able to produce a build artifact from it.
