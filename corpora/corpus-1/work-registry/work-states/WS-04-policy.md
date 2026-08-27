# WS-04: Regulatory Compliance, Privacy, and Audits
**Status**: in_progress
**Priority**: P0
**Owner**: Alice / Diana
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-23` — [ClickUp Task CIPH-23: Research Export Policy](../med-synth/tasks/CIPH-23-Research-Export-Policy.md)
- `S2` — `SRC-CU-CIPH-24` — [ClickUp Task CIPH-24: Manual Review Threshold](../med-synth/tasks/CIPH-24-Manual-Review-Threshold.md)
- `S3` — `SRC-CU-CIPH-25` — [ClickUp Task CIPH-25: Batch Fail-Closed](../med-synth/tasks/CIPH-25-Batch-Fail-Closed.md)
- `S4` — `SRC-GDOC-10` — [Policy Matrix](../med-synth/documentation/sources/2026-06-10-Policy-Matrix.md)
- `S5` — `SRC-GDOC-11` — [Compliance Audit Trail](../med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md)
- `S6` — `SRC-MEET-04` — [Fireflies Transcript: Conflict Resolution](../med-synth/communication/sources/fireflies/2026-06-12-Conflict-Resolution.md)
- `S7` — `SRC-SLACK-11` — [Slack Thread: Manual Review Threshold](../med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md)
- `S8` — `SRC-SLACK-12` — [Slack Thread: Batch Failure Strategy](../med-synth/communication/sources/slack/2026-06-12-batch-failures.md)
- `S9` — `SRC-CU-CIPH-26` — [ClickUp Task CIPH-26: Audit Trail Logging](../med-synth/tasks/CIPH-26-Audit-Trail-Logging.md)
- `S10` — `SRC-CU-CIPH-27` — [ClickUp Task CIPH-27: Conflict Resolution](../med-synth/tasks/CIPH-27-Conflict-Resolution.md)
- `S11` — `SRC-CU-CIPH-29` — [ClickUp Task CIPH-29: Offline Mode Authentication](../med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md)
- `S12` — `SRC-SLACK-17` — [Slack Thread: Offline Auth Mock Block](../med-synth/communication/sources/slack/2026-08-04-offline-auth-mock-block.md)
- `S13` — `SRC-CU-CIPH-30` — [ClickUp Task CIPH-30: PII Pattern Update HIPAA](../med-synth/tasks/CIPH-30-PII-Pattern-Update-HIPAA.md)
- `S14` — `SRC-SLACK-19` — [Slack Thread: HIPAA Regex Dictionary](../med-synth/communication/sources/slack/2026-08-05-hipaa-regex-dictionary.md)
- `S15` — `SRC-CU-CIPH-40` — [ClickUp Task CIPH-40: License Compliance Review](../med-synth/tasks/CIPH-40-License-Compliance-Review.md)
- `S16` — `SRC-SLACK-40` — [Slack Thread: AGPL Issue Found](../med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md)
- `S17` — `SRC-CU-CIPH-42` — [ClickUp Task CIPH-42: Redaction Profile Export](../med-synth/tasks/CIPH-42-Redaction-Profile-Export.md)
- `S18` — `SRC-SLACK-47` — [Slack Thread: Schema Verification](../med-synth/communication/sources/slack/2026-08-16-redaction-profile-verify.md)
- `S19` — `SRC-CU-CIPH-48` — [ClickUp Task CIPH-48: Telemetry Opt-Out](../med-synth/tasks/CIPH-48-Telemetry-Opt-Out.md)
- `S20` — `SRC-SLACK-64` — [Slack Thread: Telemetry Opt-Out Verify](../med-synth/communication/sources/slack/2026-08-24-telemetry-opt-out-verify.md)
- `S21` — `SRC-CU-CIPH-49` — [ClickUp Task CIPH-49: Accessibility a11y Audit](../med-synth/tasks/CIPH-49-Accessibility-a11y-Audit.md)
- `S22` — `SRC-SLACK-67` — [Slack Thread: A11y Audit Superseded](../med-synth/communication/sources/slack/2026-08-24-a11y-superseded.md)

## Request / Context
CipherDoc must adhere to privacy compliance rules: differential redaction policies, fail-closed batch enforcement, audit logging, offline authentication, license compliance, and telemetry opt-out.

## Task List
- [x] `T013` (mapped to CIPH-23) — Define Research Export vs Internal Review Policies. `(S1, S4)`
- [ ] `T014` (mapped to CIPH-24) — Implement Manual Review Workflow for Low Confidence OCR. `(S2, S7)`
- [x] `T015` (mapped to CIPH-25) — Implement Batch Processing Fail-Closed Strategy. `(S3, S8)`
- [ ] `T016` (mapped to CIPH-26) — Generate Compliance Audit Trail Logs. `(S5, S9)`
- [x] `T017` (mapped to CIPH-27) — Resolve Overlapping Policy Conflicts. `(S6, S10)`
- [ ] `T019` (mapped to CIPH-29) — Implement Offline Mode Authentication. `(S11, S12)`
- [x] `T020` (mapped to CIPH-30) — Update PII Patterns for HIPAA Compliance. `(S13, S14)`
- [ ] `T030` (mapped to CIPH-40) — Perform License Compliance Review. `(S15, S16)`
- [x] `T032` (mapped to CIPH-42) — Implement Redaction Profile Auditable Schema Export. `(S17, S18)`
- [x] `T038` (mapped to CIPH-48) — Implement Telemetry CLI Opt-Out Privacy Flags. `(S19, S20)`
- [ ] `T039` (mapped to CIPH-49) — Accessibility a11y Audit (**Superseded**). `(S21, S22)`

## Active Work
- **T014 / CIPH-24**: Quarantine workflow is **active**; 90% confidence threshold logic is being integrated with metadata injection for visual indicators. `(S7)`
- **T016 / CIPH-26**: Audit trail logging is **active/reopened**. Bob refactored the loader for SHA-256 hashing; Diana is verifying emitted records match the defined schema (`S5`, `S9`). The September 15 pre-release audit flagged CLI schema vs emitted-record mismatch as a release hold. `(S5, S9)`
- **T030 / CIPH-40**: **Reopened/active** after August 12 AGPL discovery in a candidate replacement PDF parser. Charlie is searching for an Apache or MIT-licensed alternative. `(S16)`

## Blockers and Dependencies
- **T019 / CIPH-29 — escrow architecture (CMT-2026-08-001)**: InfoSec approved split master-key escrow (USB token + HQ HSM); Bob is spiking implementation. Remains **blocked** until built. `(CMT-2026-08-001)`
- **T019 / CIPH-29**: **Blocked**. Local key rotation mockups exist, but rotation is impossible in a strictly air-gapped environment without centralized authority. `(S12)`
- **T030 / CIPH-40 — Legal P0 gate (CMT-2026-08-002)**: Legal memo: AGPL in bundle triggers whole-bundle copyleft; hard Legal gate — engineering library search alone cannot close T030. `(CMT-2026-08-002)`

## Decisions and Superseded Directions
- **T039 Superseded**: The standalone a11y audit (CIPH-49) was superseded by the Preview UI overhaul (CIPH-33), which natively addresses high-contrast and keyboard navigation requirements. `(S22)`
- **OCR Threshold (T014)**: 90% confidence threshold adopted for v1.0.0. `(S7)`
- **Batch Failure Strategy (T015)**: Fail-closed — on any unhandled failure the job aborts with **no output file produced** and temp files are **securely deleted**. Crash diagnostics go to a separate `audit_log.json`. `(S8, S3)`

## Done / Evidence
- `T013 / CIPH-23` — Export vs internal review policies defined in Policy Matrix. `(S1, S4)`
- `T015 / CIPH-25` — Fail-closed implemented: atomic rename ensures no partial output; Diana QA-validated no output file on failure and secure temp deletion on July 16. `(S3, S8)`
- `T017 / CIPH-27` — Overlapping policy conflict resolution merged. `(S10)`
- `T020 / CIPH-30` — HIPAA dictionary update complete and merged. `(S14)`
- `T032 / CIPH-42` — Redaction profiles export to auditable JSON schema. `(S18)`
- `T038 / CIPH-48` — Telemetry opt-out flags verified via offline network trace. `(S20)`

## Needs Manual Triage
- Finding a viable non-AGPL PDF parsing library for T030.

## Next Update Needed
Audit-log schema alignment and license compliance search status.
