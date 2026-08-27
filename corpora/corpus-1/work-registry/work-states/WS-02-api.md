# WS-02: REST API and Batch CLI
**Status**: in_progress
**Priority**: P1
**Owner**: Bob
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-13` — [ClickUp Task CIPH-13: Batch CLI](../med-synth/tasks/CIPH-13-Batch-CLI.md)
- `S2` — `SRC-GDOC-02` — [CLI Architecture](../med-synth/documentation/sources/2026-06-09-CLI-Architecture.md)
- `S3` — `SRC-CU-CIPH-14` — [ClickUp Task CIPH-14: REST API Endpoint](../med-synth/tasks/CIPH-14-REST-API-Endpoint.md)
- `S4` — `SRC-GDOC-08` — [API Security Validation](../med-synth/documentation/sources/2026-06-17-API-Security-Test.md)
- `S5` — `SRC-SLACK-08` — [Slack Thread: Defer Auth](../med-synth/communication/sources/slack/2026-06-28-defer-auth.md)
- `S6` — `SRC-CU-CIPH-19` — [ClickUp Task CIPH-19: REST API Auth](../med-synth/tasks/CIPH-19-REST-API-Auth.md)
- `S7` — `SRC-SLACK-10` — [Slack Thread: CLI Parity claim](../med-synth/communication/sources/slack/2026-07-11-cli-parity.md)
- `S8` — `SRC-CU-CIPH-22` — [ClickUp Task CIPH-22: CLI-API Parity](../med-synth/tasks/CIPH-22-CLI-API-Parity.md)
- `S9` — `SRC-SLACK-13` — [Slack Thread: Config Parity Bug discovery](../med-synth/communication/sources/slack/2026-07-09-config-parity-discovery.md)

## Request / Context
This work stream provides user interfaces to the core redaction engine: a batch CLI for directory processing and a FastAPI REST endpoint for single-document uploads.

## Task List
- [x] `T003` (mapped to CIPH-13) — Build Batch processing CLI tool. `(S1, S2)`
- [x] `T004` (mapped to CIPH-14) — Build REST API endpoint for single-document redaction. `(S3, S4)`
- [ ] `T009` (mapped to CIPH-19) — Add JWT Authentication for REST API. `(S5, S6)`
- [x] `T012` (mapped to CIPH-22) — Ensure CLI tool parity with REST API configuration features. `(S7, S8, S9)`

## Active Work
*None.*

## Blockers and Dependencies
- **T009 / CIPH-19 — MedFirst contract (CMT-2026-07-001)**: Deferred for v1.0.0 general launch, but MedFirst IT renewal requires REST authentication no later than 2026-03-31. `(CMT-2026-07-001)`
*None.*

## Decisions and Superseded Directions
- **Deferred Auth (T009 / CIPH-19)**: JWT authentication is **deferred** to v1.1. The v1.0.0 launch targets local single-machine usage where authentication is not a release blocker. `(S5)`
- **Configuration Parity Correction**: An initial parity belief was disproved on July 9 when Bob found the CLI ignored `custom_regex` flags (`S9`). PR #52 fixed the engine initialization bug; July 11 tests confirm unified configuration loading across both interfaces (`S7`).

## Done / Evidence
- `T003 / CIPH-13` — Batch CLI complete with multiprocessing for parallel directory processing. `(S1, S2)`
- `T004 / CIPH-14` — REST API complete; FastAPI uses `tempfile.SpooledTemporaryFile` so temporary files are deleted on request completion. `(S3, S4)`
- `T012 / CIPH-22` — CLI-API parity verified after the July 9 fix. `(S7, S9)`

## Needs Manual Triage
- None currently.

## Next Update Needed
Ensure documentation reflects the deferred auth state.
