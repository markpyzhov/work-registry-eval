**Source ID**: SRC-SLACK-34

# Slack Thread: Benchmark Scripts
**Channel**: #cipherdoc
**Date**: 2026-08-07

---

**[2026-08-07 10:08] Evan**: Writing the bare-metal benchmark scripts now — need something repeatable we can rerun on a real local node, not one-off numbers.

**[2026-08-07 10:11] Alice**: These are for the release performance claims, right? Make sure they're something we can rerun later and get the same shape of result.

**[2026-08-07 10:44] Evan**: That's the goal — same script, same inputs, comparable output every time.

**[2026-08-07 10:46] Charlie**: Yep.

**[2026-08-07 11:59] Charlie**: Are you testing across file types, or just one?

**[2026-08-07 12:16] Evan**: Multiple — want to see if the timing holds up consistently, not just on the easy case.

**[2026-08-07 12:19] Alice**: Sounds good.
