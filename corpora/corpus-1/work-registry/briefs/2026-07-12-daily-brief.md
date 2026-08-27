# CipherDoc Daily Brief - 2026-07-12

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **OCR fallback support** — Active P0. Base Tesseract works but is slow on large docs; Charlie is exploring multiprocessing for page OCR. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-MEET-03`, `SRC-CU-CIPH-18`.
- **Compliance audit trail logging** — Active P0. Bob refactoring loader to include SHA-256 of originals in companion JSON audit logs. Evidence: [WS-04-policy](../work-states/WS-04-policy.md); `SRC-CU-CIPH-26`, `SRC-GDOC-11`.
- **Manual review workflow** — Active P0. 90% low-confidence OCR threshold set; waiting on OCR performance before quarantine testing. Evidence: [WS-04-policy](../work-states/WS-04-policy.md); `SRC-CU-CIPH-24`, `SRC-SLACK-11`.
- **Release v1.0.0 gates and docs** — Active P0. Release checklist drafted; still pending Docker slim/CVE work and docs. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-GDOC-05`, `SRC-CU-CIPH-21`.
- **Docker image packaging** — Active P0. Multi-stage refactor continues under dual RC/GA size gates. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-CU-CIPH-15`, `CMT-2026-06-002`.

## Priority order

1. **WS-01 / T008 (CIPH-18)** — Parallelize OCR fallback for acceptable performance.
2. **WS-03 / T005 (CIPH-15)** — Finish Docker multi-stage build toward dual size gates.
3. **WS-03 / T011 (CIPH-21)** — Keep release checklist/docs current against open gates.

## Blockers / waiting-on items

- **T007 (CIPH-17) Offset Bug** — Blocked on upstream #992; mid-October ETA and Legal sign-off required for any pre-normalization workaround. Team previously noted this need not hard-block generic v1.0.0, but Legal gate remains. Evidence: `SRC-SLACK-07`, `CMT-2026-06-003`.
- **T009 MedFirst auth deadline** — JWT deferred to v1.1 for generic local launch, but MedFirst renewal requires REST API auth by 2026-03-31. Evidence: `SRC-SLACK-08`, `SRC-CU-CIPH-19`, `CMT-2026-07-001`.
- **T006 MedFirst JSON migration** — Still a release dependency. Evidence: `CMT-2026-06-001`.

## Recently changed requests

- **REST API Auth Deferred (with MedFirst exception).** Generic deferral stands; MedFirst contractual deadline now tracked. Evidence: `SRC-SLACK-08`, `CMT-2026-07-001`.
- **Security scans patched + external attestation.** CORS origin restriction landed; RedByte pen-test attestation letter dated 2026-07-11 goes into the release evidence pack. Evidence: `SRC-SLACK-09`, `SRC-CU-CIPH-20`, `CMT-2026-07-002`.
- **CLI/API parity complete.** YAML schema shared across CLI args and API. Evidence: `SRC-SLACK-10`, `SRC-CU-CIPH-22`.

## Items that need follow-up in Slack or the next status update call

- Review multiprocessing approach for OCR.
- Confirm MedFirst auth work is on the roadmap despite v1.1 deferral (`CMT-2026-07-001`).

## Needs manual triage

- None currently.

## Source links used

- `SRC-SLACK-07` — [communication/sources/slack/2026-06-26-blocked-on-upstream.md](../med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md)
- `SRC-SLACK-08` — [communication/sources/slack/2026-06-28-defer-auth.md](../med-synth/communication/sources/slack/2026-06-28-defer-auth.md)
- `SRC-SLACK-09` — [communication/sources/slack/2026-07-10-security-patch.md](../med-synth/communication/sources/slack/2026-07-10-security-patch.md)
- `SRC-SLACK-10` — [communication/sources/slack/2026-07-11-cli-parity.md](../med-synth/communication/sources/slack/2026-07-11-cli-parity.md)
- `SRC-SLACK-11` — [communication/sources/slack/2026-06-28-manual-review-threshold.md](../med-synth/communication/sources/slack/2026-06-28-manual-review-threshold.md)
- `SRC-GDOC-05` — [documentation/sources/2026-07-12-Release-Checklist.md](../med-synth/documentation/sources/2026-07-12-Release-Checklist.md)
- `SRC-GDOC-11` — [documentation/sources/2026-07-08-Compliance-Audit-Trail.md](../med-synth/documentation/sources/2026-07-08-Compliance-Audit-Trail.md)
- `SRC-MEET-03` — [communication/sources/fireflies/2026-07-05-OCR-Progress-Sync.md](../med-synth/communication/sources/fireflies/2026-07-05-OCR-Progress-Sync.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-18` — [tasks/CIPH-18-OCR-Fallback.md](../med-synth/tasks/CIPH-18-OCR-Fallback.md)
- `SRC-CU-CIPH-19` — [tasks/CIPH-19-REST-API-Auth.md](../med-synth/tasks/CIPH-19-REST-API-Auth.md)
- `SRC-CU-CIPH-20` — [tasks/CIPH-20-Security-Audit.md](../med-synth/tasks/CIPH-20-Security-Audit.md)
- `SRC-CU-CIPH-21` — [tasks/CIPH-21-Release-v1-Gates.md](../med-synth/tasks/CIPH-21-Release-v1-Gates.md)
- `SRC-CU-CIPH-22` — [tasks/CIPH-22-CLI-API-Parity.md](../med-synth/tasks/CIPH-22-CLI-API-Parity.md)
- `SRC-CU-CIPH-24` — [tasks/CIPH-24-Manual-Review-Threshold.md](../med-synth/tasks/CIPH-24-Manual-Review-Threshold.md)
- `SRC-CU-CIPH-26` — [tasks/CIPH-26-Audit-Trail-Logging.md](../med-synth/tasks/CIPH-26-Audit-Trail-Logging.md)
- `CMT-2026-06-001` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-003` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-07-001` — [work-states/comments/2026-07.md](../work-states/comments/2026-07.md)
- `CMT-2026-07-002` — [work-states/comments/2026-07.md](../work-states/comments/2026-07.md)

<!-- DAILY_BRIEF:END -->
