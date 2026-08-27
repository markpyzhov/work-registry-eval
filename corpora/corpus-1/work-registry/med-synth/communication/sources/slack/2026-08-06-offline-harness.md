**Source ID**: SRC-SLACK-32

# Slack Thread: Offline Test Harness
**Channel**: #cipherdoc
**Date**: 2026-08-06

---

**[2026-08-06 09:05] Diana**: Building the offline harness for the air-gapped mode claim — network access denied at the OS level so we get a reproducible offline run instead of just trusting the binary not to phone home.

**[2026-08-06 09:06] Alice**: Make sure to check startup specifically — if any check blocks waiting on the network before it gives up, that's a problem even if everything after it runs fine offline.

**[2026-08-06 09:32] Diana**: That's on the list. I want to see it fail closed fast, not hang.

**[2026-08-06 09:43] Bob**: How does this interact with the offline auth work? If the license check can't reach anything, does it fail open or just error out?

**[2026-08-06 09:46] Diana**: I'll run that combination through the harness too once the base setup is solid — good thing to catch here rather than in the field.

**[2026-08-06 12:16] Evan**: Let me know when it's ready. I want to run the benchmark scripts through it too, once we have real offline numbers to compare against online.
