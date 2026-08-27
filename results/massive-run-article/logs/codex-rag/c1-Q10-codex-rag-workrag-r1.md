# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

As of 2026-09-22, CipherDoc is not ship-ready: release gating is P0 and several previously closed items are active again.

- **Release/security (WS-03):** security scanning remains a durable success—the CORS fix was re-scanned and still holds. But Docker packaging **CIPH-15 is reopened/active**: image size remains above the ~450MB GA target and CVE verification fails. Release gate **T011** cannot close until Docker/CVE and Windows signing are green; the board’s hard no-ship date is 2026-10-15. `{WS-03: 1024f18927beaa06, f0b9411efcd33230, f9c5d923ad85c212}`

- **Performance (WS-05):** completed milestones still hold: the process pool scales to 16 cores and benchmarks reached 500 pages/minute. However, large-file chunking **CIPH-41 is reopened/active** after severe >2GB memory leaks; it is also a MedFirst pilot release dependency. Async scheduling **CIPH-47 is blocked** by a manifest-write race that can corrupt JSON under load. `{WS-05: 18ae303b6edf58b7, ec16f901e952ecd9, 93e3e9a1cb4874a8}`

- **Compliance (WS-04):** audit logging **CIPH-26 is active/reopened** because emitted records do not match the required schema—a release hold. License review **CIPH-40 is reopened/active** following AGPL discovery; this is a hard Legal P0 gate pending a suitable permissive replacement. `{WS-04: 917ecd0b3736fd18, 9e4ee6741c6cd253}`

- **Platform (WS-06):** durable completed milestones include verified static binaries and a 1,000-file air-gapped run. Windows compatibility is still held on Authenticode certificate procurement; High-DPI rendering may need an engine workaround for a 12% pilot subset. `{WS-06: bf446f227eff425c, b6de3e9600732a79, de0401767cdd8dd7}`

- **Storage (WS-07):** storage quota management **CIPH-32 is reopened/active** because it halts processing too aggressively. Node sync **CIPH-34 is blocked**: handshakes fail at 180ms RTT and the team declined a timeout workaround pending encryption-path stabilization. `{WS-07: bcafdf0ed04b56a6, 22220ee873af20a8}`

Top escalations before ship: resolve Docker/CVE and code-signing procurement, obtain Legal disposition/replacement for the AGPL parser, clear audit-log schema mismatch, and decide on large-file memory plus async JSON-corruption fixes. These are release-quality risks, not completed work.
