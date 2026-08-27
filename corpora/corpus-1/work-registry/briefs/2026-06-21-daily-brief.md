# CipherDoc Daily Brief - 2026-06-21

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Redaction policy configuration** — Active P0. Team converged on YAML for hand-editable policies with inline comments; Charlie is implementing the loader. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `SRC-SLACK-04`, `SRC-GDOC-03`, `SRC-MEET-02`, `SRC-CU-CIPH-16`.
- **Legacy JSON auto-migration (new)** — MedFirst still has three legacy JSON pilot policies that must auto-migrate before cutover; Evan owns the JSON→YAML converter. Treat as a release dependency on T006 and the T011 gate. Evidence: [WS-01-engine](../work-states/WS-01-engine.md); `CMT-2026-06-001`.
- **Docker image packaging** — Active P0. Evan continues packaging for local/offline deploy. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-CU-CIPH-15`.
- **REST API endpoint** — Active P1. FastAPI path still in flight post temp-file review. Evidence: [WS-02-api](../work-states/WS-02-api.md); `SRC-CU-CIPH-14`, `SRC-SLACK-03`.

## Priority order

1. **WS-01 / T006 (CIPH-16)** — Land YAML loader and plan MedFirst JSON auto-migration (`CMT-2026-06-001`).
2. **WS-03 / T005 (CIPH-15)** — Keep Docker packaging on the release path.
3. **WS-02 / T004 (CIPH-14)** — Close remaining API security review items.

## Blockers / waiting-on items

- **T006 migration dependency** — MedFirst cutover blocked until legacy JSON policies auto-migrate. Evidence: `CMT-2026-06-001`.

## Recently changed requests

- **Config format decision (YAML over JSON)** — JSON superseded for policy files to allow inline comments. Evidence: `SRC-SLACK-04`, `SRC-GDOC-03`, `SRC-MEET-02`.
- **MedFirst JSON migration requirement surfaced** — Offline client call adds converter ownership and T011 gate coupling. Evidence: `CMT-2026-06-001`.

## Items that need follow-up in Slack or the next status update call

- Evan to size the JSON→YAML converter and confirm which three MedFirst policies are in scope.

## Needs manual triage

- None currently.

## Source links used

- `SRC-SLACK-03` — [communication/sources/slack/2026-06-14-api-endpoint.md](../med-synth/communication/sources/slack/2026-06-14-api-endpoint.md)
- `SRC-SLACK-04` — [communication/sources/slack/2026-06-20-config-format-debate.md](../med-synth/communication/sources/slack/2026-06-20-config-format-debate.md)
- `SRC-GDOC-03` — [documentation/sources/2026-06-20-Config-Architecture.md](../med-synth/documentation/sources/2026-06-20-Config-Architecture.md)
- `SRC-MEET-02` — [communication/sources/fireflies/2026-06-18-Config-Format-Sync.md](../med-synth/communication/sources/fireflies/2026-06-18-Config-Format-Sync.md)
- `SRC-CU-CIPH-14` — [tasks/CIPH-14-REST-API-Endpoint.md](../med-synth/tasks/CIPH-14-REST-API-Endpoint.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-16` — [tasks/CIPH-16-Redaction-Policy-Config.md](../med-synth/tasks/CIPH-16-Redaction-Policy-Config.md)
- `CMT-2026-06-001` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)

<!-- DAILY_BRIEF:END -->
