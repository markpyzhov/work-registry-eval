# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

No. Nominal-latency success is explicitly insufficient for field sign-off; high-latency validation is required. Singapore failed at 180ms RTT with the 5s prototype timeout; planning calls for a 30s high-latency budget. But this is a planning requirement, not an approved fix: whether 30s works remains manual triage, and the team rejected a timeout-only workaround pending encryption/handshake changes.

Cites: [WS-07](c1/work-states/WS-07-storage.md:36), [field comment](c1/work-states/comments/2026-09.md:30), [validation log](c1/med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md:16), [deep-dive](c1/med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md:19).
