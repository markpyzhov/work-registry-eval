# CipherDoc Daily Brief - 2026-06-27

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Offset bug / upstream block** — T007 is **Blocked** on `pdfminer.six` #992. Maintainer DM: earliest realistic merge mid-October; any pre-normalization workaround needs written Legal sign-off. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-SLACK-07`, `SRC-CU-CIPH-17`, `CMT-2026-06-003`.
- **Docker packaging** — Still active against dual RC (800MB CVE-clean) / GA (~450MB) gates after the 2.1GB OCR bloat reopen. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-SLACK-06`, `SRC-CU-CIPH-15`, `CMT-2026-06-002`.
- **OCR fallback** — Active; scanned-doc path still in build. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-CU-CIPH-18`.
- **MedFirst JSON migration** — Remains a T006/T011 release dependency. Evidence: `CMT-2026-06-001`.

## Priority order

1. **WS-01 / T007 (CIPH-17)** — Confirm Legal path vs wait-on-upstream; do not ship a pre-normalization workaround without written sign-off (`CMT-2026-06-003`).
2. **WS-03 / T005 (CIPH-15)** — Continue multi-stage slim-down toward dual size gates.
3. **WS-01 / T008 (CIPH-18)** — Keep OCR fallback progressing in parallel.

## Blockers / waiting-on items

- **T007** — Upstream #992 + Legal sign-off for any workaround. Evidence: `SRC-SLACK-07`, `CMT-2026-06-003`.
- **T005** — Dual size gates still unmet after OCR dependency bloat. Evidence: `SRC-SLACK-06`, `CMT-2026-06-002`.

## Recently changed requests

- **Legal dependency added on T007.** Maintainer ETA and Legal gate clarified offline. Evidence: `CMT-2026-06-003`.
- **Upstream block acknowledged in Slack.** Team recorded #992 as the blocking dependency. Evidence: `SRC-SLACK-07`.

## Items that need follow-up in Slack or the next status update call

- Alice/Legal: can we get written sign-off criteria for a temporary pre-normalization workaround, or do we explicitly accept mid-October upstream timing?

## Needs manual triage

- Whether v1.0.0 can ship with known multi-page offset issues while #992 remains open.

## Source links used

- `SRC-SLACK-06` — [communication/sources/slack/2026-06-25-docker-size.md](../med-synth/communication/sources/slack/2026-06-25-docker-size.md)
- `SRC-SLACK-07` — [communication/sources/slack/2026-06-26-blocked-on-upstream.md](../med-synth/communication/sources/slack/2026-06-26-blocked-on-upstream.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-17` — [tasks/CIPH-17-Fix-Offset-Mismatch.md](../med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md)
- `SRC-CU-CIPH-18` — [tasks/CIPH-18-OCR-Fallback.md](../med-synth/tasks/CIPH-18-OCR-Fallback.md)
- `CMT-2026-06-001` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-003` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)

<!-- DAILY_BRIEF:END -->
