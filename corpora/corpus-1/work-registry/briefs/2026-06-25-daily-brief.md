# CipherDoc Daily Brief - 2026-06-25

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Docker image packaging (REOPENED)** — Active P0. OCR/Tesseract deps blew the image to 2.1GB; Evan is refactoring to a multi-stage build. CISO offline review now sets dual size gates: RC may ship at 800MB once CVE-clean; GA target remains ~450MB — do not conflate on the checklist. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-SLACK-06`, `SRC-CU-CIPH-15`, `CMT-2026-06-002`.
- **Offset mismatch bug in multi-page PDFs** — Active P0. Charlie is debugging `pdfminer.six` dropping whitespace at page boundaries. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-SLACK-05`, `SRC-CU-CIPH-17`.
- **OCR fallback support** — Active P0. Tesseract integration for scanned docs without text layers. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-CU-CIPH-18`.
- **MedFirst JSON migration** — Still open release dependency on T006/T011; Evan owns converter. Evidence: `CMT-2026-06-001`.

## Priority order

1. **WS-01 / T007 (CIPH-17)** — Find a consistent workaround or upstream path for offset drift.
2. **WS-03 / T005 (CIPH-15)** — Multi-stage Docker build toward dual RC/GA size gates (`CMT-2026-06-002`).
3. **WS-01 / T008 (CIPH-18)** — Prove out the Tesseract OCR fallback pipeline.

## Blockers / waiting-on items

- **T007 (CIPH-17) Offset Bug** — No consistent local patch yet; upstream status still unclear as of today.
- **T005 dual size gates** — Track 800MB RC (CVE-clean) and ~450MB GA separately. Evidence: `CMT-2026-06-002`.

## Recently changed requests

- **Configuration Format Changed.** YAML superseded JSON for redaction policies; YAML parser merged. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-SLACK-04`, `SRC-GDOC-03`, `SRC-CU-CIPH-16`.
- **Docker size gates clarified.** Dual RC/GA thresholds from CISO offline review. Evidence: `CMT-2026-06-002`.

## Items that need follow-up in Slack or the next status update call

- Decide whether the `pdfminer.six` offset bug is a hard v1.0.0 blocker or a known issue for specific multi-page PDFs.

## Needs manual triage

- None currently.

## Source links used

- `SRC-SLACK-04` — [communication/sources/slack/2026-06-20-config-format-debate.md](../med-synth/communication/sources/slack/2026-06-20-config-format-debate.md)
- `SRC-SLACK-05` — [communication/sources/slack/2026-06-23-offset-bug-debug.md](../med-synth/communication/sources/slack/2026-06-23-offset-bug-debug.md)
- `SRC-SLACK-06` — [communication/sources/slack/2026-06-25-docker-size.md](../med-synth/communication/sources/slack/2026-06-25-docker-size.md)
- `SRC-GDOC-03` — [documentation/sources/2026-06-20-Config-Architecture.md](../med-synth/documentation/sources/2026-06-20-Config-Architecture.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-16` — [tasks/CIPH-16-Redaction-Policy-Config.md](../med-synth/tasks/CIPH-16-Redaction-Policy-Config.md)
- `SRC-CU-CIPH-17` — [tasks/CIPH-17-Fix-Offset-Mismatch.md](../med-synth/tasks/CIPH-17-Fix-Offset-Mismatch.md)
- `SRC-CU-CIPH-18` — [tasks/CIPH-18-OCR-Fallback.md](../med-synth/tasks/CIPH-18-OCR-Fallback.md)
- `CMT-2026-06-001` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)

<!-- DAILY_BRIEF:END -->
