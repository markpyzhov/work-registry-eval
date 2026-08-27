# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

## Answer

**No — the earlier nominal-latency pass is explicitly not sufficient for field sign-off** as of the final snapshot (as-of `2026-09-22T12:00:00Z`).

### What the nominal-latency pass actually covered
Bob's 2026-08-08 validation ran two nodes on the same local network, dozens of back-to-back connect attempts, zero failures or retries — but it was scoped to nominal latency only, and was left "in progress until we cover high latency" at Diana's insistence. The 2026-08-06 prototype retrospective says the same: exercised on one LAN segment only; multi-site latency/jitter untested.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md` (`SRC-SLACK-27`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md` (`SRC-GDOC-18`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-06-node-sync-handshake-prototype.md` (`SRC-SLACK-26`)

### The high-latency field constraint that now applies
T024 / CIPH-34 is **Blocked** in the authoritative Work State. High-latency simulation on 2026-09-22 times out — the handshake never completes the exchange, and it degrades as the link slows (suspected AES-256 per-packet overhead on the wire path pushing the exchange past the timeout window). The task's acceptance criteria require success under high latency, not only nominal.

A field data point makes it concrete and explicit: the **Singapore field trial fails at 180ms RTT with the current 5s prototype timeout**, and the QA disposition states directly: *do not treat nominal-latency pass as sufficient for field sign-off*.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (authoritative; T024 Blockers)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-004`, Diana, 2026-09-22)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md` (`SRC-CU-CIPH-34`, Status: Blocked)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (T024 listed under Key Blockers)

### Timeout budget planning must assume
**30 seconds** on high-latency links, up from the 5s prototype timeout. Plan against that number — with an important caveat.

**The caveat (unresolved tension, do not plan as if settled):** the same-day Handshake Protocol Deep Dive **declined a timeout bump as the fix**. Evan: bumping timeouts "just hides it — if the link is slow enough, we still fail"; Bob agreed to no timeout bump; Alice left the work blocked pending encryption-path stabilization. So the 30s budget is a field-derived requirement, not an approved remedy. WS-07 carries this forward as an open triage item: *whether 30s resolves the Singapore 180ms RTT failures without redesigning the handshake exchange count* — i.e. the exchange may need fewer round trips regardless of the timeout value.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (`SRC-MEET-11`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (Needs Manual Triage)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### Bottom line for planning
Budget **30s** for high-latency handshake completion, treat the high-latency repro (kept in place by Diana) as a mandatory gate before multi-site rollout, and expect that the budget alone may not close the item — the dependency on the encryption path and a possible reduction in handshake exchange count are still open. Note also that a 2026-09-02 brief characterized these as "intermittent... not yet a hard field failure"; that framing is superseded by the 2026-09-22 state.
