# WS-01: Detection and Redaction Engine
**Status**: in_progress
**Priority**: P0
**Owner**: Charlie
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-11` — [ClickUp Task CIPH-11: Core Redaction Engine](../med-synth/tasks/CIPH-11-Core-Redaction-Engine.md)
- `S2` — `SRC-MEET-01` — [Fireflies Transcript: Core Engine Kickoff](../med-synth/communication/sources/fireflies/2026-06-01-Core-Engine-Kickoff.md)
- `S3` — `SRC-CU-CIPH-12` — [ClickUp Task CIPH-12: Regex Detection](../med-synth/tasks/CIPH-12-Regex-Detection.md)
- `S4` — `SRC-SLACK-02` — [Slack Thread: Regex Dependency](../med-synth/communication/sources/slack/2026-06-06-regex-dependency.md)
- `S5` — `SRC-GDOC-07` — [Test Report: Financial Regex Detection](../med-synth/documentation/sources/2026-06-08-Financial-Regex-Test.md)
- `S6` — `SRC-SLACK-07` — [Slack Thread: Blocked on Upstream](../med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md)
- `S7` — `SRC-CU-CIPH-17` — [ClickUp Task CIPH-17: Fix Offset Mismatch](../med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md)
- `S8` — `SRC-MEET-03` — [Fireflies Transcript: OCR Progress Sync](../med-synth/communication/sources/fireflies/2026-07-05-OCR-Progress-Sync.md)
- `S9` — `SRC-CU-CIPH-18` — [ClickUp Task CIPH-18: OCR Fallback](../med-synth/tasks/CIPH-18-OCR-Fallback.md)
- `S10` — `SRC-GDOC-03` — [Config Format Architecture Update](../med-synth/documentation/sources/2026-06-20-Config-Architecture.md)
- `S11` — `SRC-CU-CIPH-16` — [ClickUp Task CIPH-16: Redaction Policy Config](../med-synth/tasks/CIPH-16-Redaction-Policy-Config.md)
- `S12` — `SRC-SLACK-04` — [Slack Thread: Config Format Debate](../med-synth/communication/sources/slack/2026-06-20-config-format-debate.md)
- `S13` — `SRC-MEET-02` — [Fireflies Transcript: Config Format Sync](../med-synth/communication/sources/fireflies/2026-06-18-Config-Format-Sync.md)

## Request / Context
The core capability of CipherDoc relies on robustly parsing PDF documents, detecting sensitive spans (like financial identifiers), and applying visual redaction overlays without destroying the document's original structure. The team is building the initial parser utilizing `pdfminer.six`, adding regex detection rules, and defining how users configure custom redaction policies.

## Task List
- [x] `T001` (mapped to CIPH-11) — Implement core redaction engine for PDF text layers. `(S1, S2)`
- [x] `T002` (mapped to CIPH-12) — Add regex-based detection for financial data (Credit Cards, SSNs). `(S3, S4, S5)`
- [x] `T006` (mapped to CIPH-16) — Implement redaction policy configuration loading. `(S10, S11, S12, S13)`
- [ ] `T007` (mapped to CIPH-17) — Fix offset mismatch bug in multi-page PDFs. `(S6, S7)`
- [ ] `T008` (mapped to CIPH-18) — Add support for scanned documents (OCR fallback). `(S8, S9)`

## Active Work
- **T006 / CIPH-16 — legacy JSON migration (CMT-2026-06-001)**: MedFirst pilot requires auto-migration of three legacy JSON policies before production cutover; Evan owns the JSON→YAML converter. Migration is a release dependency on T006 and the T011 gate. `(CMT-2026-06-001)`
- **T008 / CIPH-18**: OCR fallback implementation is **active**. Charlie integrated multiprocessing for page-level parallelism and Diana is wiring OCR results into the main scanner pipeline. Confidence tuning continues as of September. `(S8, S9)`

## Blockers and Dependencies
- **T007 / CIPH-17 — Legal gate (CMT-2026-06-003)**: Maintainer DM indicates #992 earliest mid-October; any pre-normalization workaround requires written Legal sign-off in addition to upstream merge. `(CMT-2026-06-003)`
- **T007 / CIPH-17**: **Blocked** on upstream `pdfminer.six` Issue/PR #992. Charlie monitored the repository through August and evaluated a local fork in late August, but the team rejected maintaining a parser fork. As of September 10 the upstream PR remains unmerged and no safe local workaround exists. `(S6, S7)`

## Decisions and Superseded Directions
- **Configuration Format (T006 / CIPH-16)**: JSON was superseded by YAML for inline comments and hand-editing of complex regex policies. `(S10, S12, S13)`

## Done / Evidence
- `T001 / CIPH-11` — Core parser implemented with `pdfminer.six` for pixel-perfect bounding boxes; merged to main. `(S1, S2)`
- `T002 / CIPH-12` — Regex engine integrated; Diana validated 100% detection on synthetic Credit Card and SSN test cases. `(S3, S5)`
- `T006 / CIPH-16` — YAML policy loader merged; users can define target regex types in policy files. `(S11)`

## Needs Manual Triage
- None currently.

## Next Update Needed
OCR performance status and upstream #992 merge watch.
