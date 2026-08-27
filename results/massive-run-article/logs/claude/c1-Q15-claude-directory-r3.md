# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

## Answer

**No — the earlier nominal-latency handshake pass is not sufficient for field sign-off.** As of the final snapshot (Work State Index as-of `2026-09-22T12:00:00Z`), zero-trust node sync (T024 / CIPH-34) is **Blocked**, and the field record explicitly says the nominal-latency pass must not be treated as sufficient.

### What the nominal pass actually covered
Bob's 2026-08-08 validation ran two nodes on the same LAN segment across dozens of back-to-back connect attempts with zero failures or retries — but Diana flagged at the time that "the high-latency case [must be] covered before this goes anywhere near the field," and the work was deliberately left in progress. The 2026-08-15 review confirms the scope limit: one LAN segment, nominal RTT, with multi-site latency/jitter untested and named as the prerequisite for multi-site rollout.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md`

### The high-latency field constraint that now applies
The handshake **must succeed under high-latency network conditions, not only nominal latency** — this is an explicit acceptance criterion on CIPH-34, and the blocking timeout must be resolved *before* multi-site rollout can proceed. On 2026-09-22 Diana reopened the thread: over a simulated high-latency link the handshake **times out and never completes the exchange**, degrading further as the link slows. Bob attributes it to AES-256 per-packet overhead on the output path pushing the exchange past the timeout window, making the fix dependent on the encryption workstream.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`

### The timeout budget planning must assume
**30 seconds on high-latency links** — up from the 5s prototype timeout. The Singapore field trial failed at **180ms RTT** with the 5s prototype value, and the field comment states plainly: do not treat the nominal-latency pass as sufficient for field sign-off.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-004`, Diana, 2026-09-22)

### Important tension to carry into planning
The 30s budget is a **field requirement, not an approved fix**. In the same-day deep dive the team **declined a timeout bump** — Evan: bumping timeouts "just hides it," since a sufficiently slow link still fails; Alice closed the meeting leaving the work blocked with no workaround invented, pending the encryption path. Diana kept the high-latency repro in place for retest.

So planning should assume a 30s budget as the field-derived target, while treating it as **unvalidated**: WS-07 carries it under *Needs Manual Triage* — whether 30s resolves the 180ms RTT failures **without redesigning the handshake exchange count** is explicitly open, as is the root cause (timeout vs. encryption overhead on the wire path). Bob stated he has no fix that keeps the current exchange as-is, which suggests an exchange-count redesign may be required regardless of the timeout value.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### Trajectory note
The 2026-09-02 brief recorded these as "intermittent high-latency timeouts … not yet a hard field failure." By 2026-09-22 that had hardened into a reproducible block plus a quantified field failure (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-02-daily-brief.md`).
