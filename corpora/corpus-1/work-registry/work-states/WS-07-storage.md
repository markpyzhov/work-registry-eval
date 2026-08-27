# WS-07: Data Persistence, Encryption, and Secure Storage
**Status**: in_progress
**Priority**: P1
**Owner**: Bob / Charlie
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-31` — [ClickUp Task CIPH-31: Local Encryption at Rest](../med-synth/tasks/CIPH-31-Local-Encryption-at-Rest.md)
- `S2` — `SRC-SLACK-21` — [Slack Thread: AES-256 Pipeline](../med-synth/communication/sources/slack/2026-08-05-aes256-pipeline.md)
- `S3` — `SRC-CU-CIPH-32` — [ClickUp Task CIPH-32: Storage Quota Management](../med-synth/tasks/CIPH-32-Storage-Quota-Management.md)
- `S4` — `SRC-SLACK-23` — [Slack Thread: Storage Quota Halt](../med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md)
- `S5` — `SRC-CU-CIPH-34` — [ClickUp Task CIPH-34: Zero-Trust Node Sync](../med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md)
- `S6` — `SRC-SLACK-27` — [Slack Thread: Node Sync Handshake Validation](../med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md)
- `S7` — `SRC-MEET-11` — [Fireflies Transcript: Handshake Protocol Deep Dive](../med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md)
- `S8` — `SRC-CU-CIPH-35` — [ClickUp Task CIPH-35: Ephemeral File Cleanup](../med-synth/tasks/CIPH-35-Ephemeral-File-Cleanup.md)
- `S9` — `SRC-SLACK-29` — [Slack Thread: OCR Temp Cleanup Hooks](../med-synth/communication/sources/slack/2026-08-09-ocr-temp-cleanup-hooks.md)
- `S10` — `SRC-CU-CIPH-44` — [ClickUp Task CIPH-44: Custom Dictionary Support](../med-synth/tasks/CIPH-44-Custom-Dictionary-Support.md)
- `S11` — `SRC-SLACK-52` — [Slack Thread: CSV Dictionary Matcher](../med-synth/communication/sources/slack/2026-08-14-csv-dictionary-matcher.md)

## Request / Context
Secure storage lifecycle: AES-256 output encryption, disk quota monitoring, zero-trust node sync, OCR temp cleanup, and custom CSV dictionaries.

## Task List
- [x] `T021` (mapped to CIPH-31) — Implement AES-256 local encryption at rest. `(S1, S2)`
- [ ] `T022` (mapped to CIPH-32) — Implement storage quota management. `(S3, S4)`
- [ ] `T024` (mapped to CIPH-34) — Implement Zero-Trust distributed node sync. `(S5, S6, S7)`
- [x] `T025` (mapped to CIPH-35) — Add ephemeral file cleanup hooks for OCR. `(S8, S9)`
- [x] `T034` (mapped to CIPH-44) — Add support for custom CSV redaction dictionaries. `(S10, S11)`

## Active Work
- **T022 / CIPH-32 — production baseline (CMT-2026-09-003)**: Ops capacity planning sets production quota baseline at **2GB** free disk (not 500MB) with 10% buffer tolerance before halt. `(CMT-2026-09-003)`
- **T022 / CIPH-32**: **Reopened/active**. Storage monitor halts processing too aggressively when ~500MB remains free; Bob is refactoring the loop to allow a 10% buffer tolerance before halting. `(S4)`

## Blockers and Dependencies
- **T024 — field timeout budget (CMT-2026-09-004)**: Singapore field trial fails at 180ms RTT with 5s prototype timeout; need **30s** timeout budget on high-latency links. `(CMT-2026-09-004)`
- **T024 / CIPH-34**: **Blocked**. Nominal-latency handshake validation passed (`S6`), but high-latency simulation on September 22 times out — handshake never completes under slow links, and the team declined a timeout-bump workaround pending encryption-path stabilization (`S6`, `S7`).

## Decisions and Superseded Directions
- **Cleanup Strategy**: Cron-based cleanup superseded by in-process `atexit` hooks for zero-residual footprint. `(S8, S9)`

## Done / Evidence
- `T021 / CIPH-31` — Redaction outputs encrypted with machine-local AES-256 key; zero-leakage confirmed in cold-start audit. `(S2)`
- `T025 / CIPH-35` — Temp files purged from `/tmp/cipherdoc-*` immediately after processing. `(S9)`
- `T034 / CIPH-44` — Users can upload CSV custom name/entity lists for redaction. `(S11)`

## Needs Manual Triage
- Whether 30s timeout budget resolves Singapore 180ms RTT failures without redesigning handshake exchange count. `(CMT-2026-09-004)`
- High-latency handshake timeout root cause vs encryption overhead on the wire path.

## Next Update Needed
Quota monitor buffer refactor verification and handshake high-latency retest plan.
