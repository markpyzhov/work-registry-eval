# CipherDoc Daily Brief - 2026-08-12

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **License compliance (T030)** — AGPL found in a candidate PDF parser; dependency reverted and search reopened. Legal memo: AGPL in the bundle triggers whole-bundle copyleft — escalate to P0 Legal gate; engineering search alone is insufficient. Evidence: [WS-04-policy](../work-states/WS-04-policy.md); `SRC-SLACK-40`, `SRC-SLACK-41`, `SRC-CU-CIPH-40`, `CMT-2026-08-002`.
- **Windows native build (T029)** — Windows build artifact progress; path handling work continues. Evidence: [WS-06-platforms](../work-states/WS-06-platforms.md); `SRC-SLACK-38`, `SRC-SLACK-36`, `SRC-CU-CIPH-39`.
- **Offline auth escrow (T019)** — Still Blocked pending implementation of approved USB+HSM escrow. Evidence: [WS-04-policy](../work-states/WS-04-policy.md); `CMT-2026-08-001`, `SRC-CU-CIPH-29`.
- **Docker packaging (T005)** — Image still above GA ~450MB target; CVE verification open. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-CU-CIPH-15`, `CMT-2026-06-002`.
- **Custom CSV dictionary / redaction profiles** — Schema and loader work opening this week. Evidence: `SRC-SLACK-45`, `SRC-SLACK-50`.

## Priority order

1. **WS-04 / T030 (CIPH-40)** — Treat as P0 Legal gate; engage Legal on Apache/MIT-only alternatives (`CMT-2026-08-002`).
2. **WS-04 / T019 (CIPH-29)** — Continue escrow spike to unblock offline auth.
3. **WS-03 / T005 (CIPH-15)** — Keep Docker size/CVE on the release path.

## Blockers / waiting-on items

- **T030 Legal P0** — Whole-bundle copyleft exposure; hard Legal gate. Evidence: `CMT-2026-08-002`, `SRC-SLACK-40`.
- **T019** — Escrow approved but not yet implemented. Evidence: `CMT-2026-08-001`.
- **T007** — Upstream #992 + Legal workaround gate unchanged. Evidence: `CMT-2026-06-003`.

## Recently changed requests

- **AGPL reopen + Legal escalation.** Evidence: `SRC-SLACK-40`, `CMT-2026-08-002`.
- **Windows build artifact shared.** Evidence: `SRC-SLACK-38`.

## Items that need follow-up in Slack or the next status update call

- Diana/Legal: acceptable non-AGPL parser shortlist and timeline for T030 close.
- Bob: escrow spike ETA.

## Needs manual triage

- None currently.

## Source links used

- `SRC-SLACK-36` — [communication/sources/slack/2026-08-10-windows-path-handling.md](../med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md)
- `SRC-SLACK-38` — [communication/sources/slack/2026-08-12-windows-build-artifact.md](../med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md)
- `SRC-SLACK-40` — [communication/sources/slack/2026-08-12-license-agpl-reopen.md](../med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md)
- `SRC-SLACK-41` — [communication/sources/slack/2026-08-11-license-parser-swap.md](../med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md)
- `SRC-SLACK-45` — [communication/sources/slack/2026-08-12-redaction-profile-schema.md](../med-synth/communication/sources/slack/2026-08-12-redaction-profile-schema.md)
- `SRC-SLACK-50` — [communication/sources/slack/2026-08-12-csv-dictionary-loader.md](../med-synth/communication/sources/slack/2026-08-12-csv-dictionary-loader.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-29` — [tasks/CIPH-29-Offline-Mode-Authentication.md](../med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md)
- `SRC-CU-CIPH-39` — [tasks/CIPH-39-Windows-Compatibility.md](../med-synth/tasks/CIPH-39-Windows-Compatibility.md)
- `SRC-CU-CIPH-40` — [tasks/CIPH-40-License-Compliance-Review.md](../med-synth/tasks/CIPH-40-License-Compliance-Review.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-003` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-08-001` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-002` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)

<!-- DAILY_BRIEF:END -->
