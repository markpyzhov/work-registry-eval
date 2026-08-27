# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

## Answer

**Short answer: No — the earlier nominal-latency handshake pass is not enough for field sign-off. A high-latency success constraint now applies, and planning must assume a 30-second timeout budget on high-latency links (up from the 5s prototype timeout) — while noting that the team has *not* approved a timeout bump as the fix.**

Snapshot context: the authoritative as-of timestamp for the package is **2026-09-22T12:00:00Z** (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md`). The governing Work State is **WS-07 (Data Persistence, Encryption, and Node Sync)**, item **T024 → CIPH-34**.

### 1. Is the nominal-latency pass enough? No.

- The nominal-latency validation did pass: on 2026-08-08 Bob ran dozens of back-to-back connects between two nodes on the local network with zero failures or retries — but he explicitly left it "in progress until we cover high latency," and Diana required the high-latency case "before this goes anywhere near the field" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md`, SRC-SLACK-27).
- The prototype retrospectives are explicit that the LAN result carried no field claim: only one LAN segment was exercised, and multi-site latency/jitter "has not been tested" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md`, SRC-GDOC-18; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Architecture-Review.md`, SRC-GDOC-38, which states nominal-latency validation is "outside this write-up").
- The decisive statement is in the field comment: "do not treat nominal-latency pass as sufficient for field sign-off" (`CMT-2026-09-004`, in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md`).
- Current status is **Blocked**, not merely incomplete: WS-07 records "Nominal-latency handshake validation passed (S6), but high-latency simulation on September 22 times out." The ClickUp task is likewise **Blocked** as of 2026-09-22 by Diana (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md`; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`).

### 2. The high-latency field constraint that now applies

CIPH-34's acceptance criteria now require, beyond reliable completion between nodes:

- **"Handshake succeeds under high-latency network conditions, not only nominal latency."**
- **"Blocking timeout issue is resolved before multi-site rollout can proceed."**

(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md`)

Concretely, on a simulated high-latency link the handshake never completes the exchange — it times out, and degrades further as the link slows, suggesting the handshake does more work per round trip than it should. Bob attributes this to the AES-256 output-path pipeline adding per-packet overhead that pushes the exchange past the timeout window, which is why resolution is coupled to the encryption workstream (SRC-SLACK-27; `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md`, SRC-MEET-11).

### 3. Timeout budget planning must assume: 30 seconds

- Field data: the **Singapore field trial fails at 180 ms RTT with the current 5 s prototype timeout**; the requirement recorded is a **30 s timeout budget on high-latency links** (`CMT-2026-09-004`; carried into WS-07 "Blockers and Dependencies" and into `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`).

**Important caveat — the 30s figure is a planning budget, not an approved fix.** On the same date, the Handshake Protocol Deep Dive explicitly **declined a timeout-bump workaround** pending encryption-path stabilization: Evan's position was that bumping timeouts "just hides it," Bob agreed to "no timeout bump," and Alice left the work blocked (SRC-MEET-11). Diana kept the high-latency repro in place for retest when encryption or the handshake design changes.

This tension is unresolved and is formally flagged in two places as **Needs Manual Triage**:
1. Whether the 30 s budget resolves the Singapore 180 ms RTT failures **without redesigning the handshake exchange count**.
2. High-latency timeout root cause vs. encryption overhead on the wire path.

(WS-07 "Needs Manual Triage"; daily brief 2026-09-22, which also ranks WS-07/T024 as priority #2 behind the release-gate items.)

### Bottom line for sign-off planning

Plan for a **30 s** handshake timeout budget on high-latency links and treat **success at ≥180 ms RTT** as the field bar — but do not plan on a timeout bump alone clearing the block. Sign-off requires a passing **high-latency** retest, which is gated on the encryption path settling, and may require reducing the handshake's exchange count rather than extending the window. Next update owed per WS-07: the **handshake high-latency retest plan**.

**Files supporting these claims (all absolute):**
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md` (authoritative current state, T024)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/index.md` (as-of timestamp; T024 listed under Key Blockers)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (`CMT-2026-09-004` — 180 ms RTT, 5 s → 30 s, no-nominal-sign-off directive)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md` (Blocked status, acceptance criteria)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md` (nominal pass; 2026-09-22 reopen, AES-256 overhead)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md` (no timeout bump; stays blocked)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Review.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-15-Zero-Trust-Node-Sync-Architecture-Review.md` (prototype scope limits)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md` (snapshot-day summary and triage items)
