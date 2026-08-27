**Source ID**: SRC-SLACK-27

# Slack Thread: Node Sync Handshake Validation
**Channel**: #cipherdoc
**Thread opened**: 2026-08-08
**Last activity**: 2026-09-22

---

**[2026-08-08 09:04] Bob**: Ran the handshake validation under nominal latency — two nodes on the local network, dozens of connect attempts back to back. No failures.

**[2026-08-08 09:05] Evan**: Any dropped or retried handshakes at all?

**[2026-08-08 09:30] Bob**: None. Every attempt authenticated cleanly on the first try at this latency.

**[2026-08-08 09:32] Diana**: We still need the high-latency case covered before this goes anywhere near the field.

**[2026-08-08 09:38] Bob**: Agreed, it's next on the list. First cut of the nominal-latency pass looks solid — leaving it in progress until we cover high latency.

**[2026-08-08 09:41] Diana**: Good.

**[2026-09-22 09:50] Diana**: Reopening this. Ran the handshake over a simulated high-latency link and it's timing out — never completes the exchange.

**[2026-09-22 10:08] Bob**: Timing out, or actively failing? Could just be the round trip budget being too tight.

**[2026-09-22 10:09] Diana**: Times out. And it gets worse the slower the link — feels like the handshake is doing more work per round trip than it should.

**[2026-09-22 10:18] Bob**: That tracks. The AES-256 pipeline we added on the output path adds per-packet overhead, and on a slow link that pushes the exchange past the timeout window. This depends on the encryption work settling down before we can retest — handshake work stays blocked for now.
