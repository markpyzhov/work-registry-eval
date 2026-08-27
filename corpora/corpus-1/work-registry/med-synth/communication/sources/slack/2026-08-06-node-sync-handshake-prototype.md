**Source ID**: SRC-SLACK-26

# Slack Thread: Node Sync Handshake Prototype
**Channel**: #cipherdoc
**Date**: 2026-08-06

---

**[2026-08-06 09:30] Bob**: Starting on the replication handshake for the zero-trust node sync. First requirement is that two nodes have to authenticate each other before either one accepts replicated entries.

**[2026-08-06 09:37] Evan**: How's a node proving who it is right now?

**[2026-08-06 09:38] Bob**: Each node has a registered identity it presents at connect time. If the peer doesn't recognize it, the connection gets dropped before any data moves.

**[2026-08-06 09:49] Charlie**: Does the handshake add noticeable overhead to the redaction jobs running on the same box?

**[2026-08-06 10:40] Bob**: Negligible so far — it's a short exchange before the sync session opens, nothing that touches the active redaction path.

**[2026-08-06 10:41] Diana**: What's next after the prototype?

**[2026-08-06 11:47] Bob**: Need to check it holds up under real network delay, not just on my two test nodes on the same switch. That's the next pass.
