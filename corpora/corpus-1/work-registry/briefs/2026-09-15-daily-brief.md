# CipherDoc Daily Brief - 2026-09-15

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Release gates (T011)** — Pre-release audit holds ship on Docker slim/CVE (T005), Windows signing (T029), and related open items. Release board: **no-ship after 2026-10-15** if T005 and T029 are not green — hard deadline. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-MEET-10`, `SRC-CU-CIPH-21`, `SRC-SLACK-37`, `CMT-2026-09-002`.
- **Docker packaging (T005)** — Still active under dual RC/GA size gates. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-CU-CIPH-15`, `CMT-2026-06-002`.
- **Storage quota (T022)** — Monitor too aggressive near ~500MB free; keep 10% buffer refactor but retarget production baseline to **2GB** free disk. Evidence: [WS-07-storage](../work-states/WS-07-storage.md); `SRC-SLACK-23`, `SRC-CU-CIPH-32`, `CMT-2026-09-003`.
- **High-DPI / Form XObjects (T036)** — Upstream 4K scaling still blocked; offline QA: ~12% of MedFirst pilot corpus fails coordinate alignment due to nested Form XObjects — beyond scaling alone. Evidence: [WS-06-platforms](../work-states/WS-06-platforms.md); `SRC-SLACK-58`, `SRC-GDOC-49`, `SRC-CU-CIPH-46`, `CMT-2026-09-001`.
- **MedFirst OOM (T031)** — Remains pilot-blocker tied to T011. Evidence: `CMT-2026-08-003`.

## Priority order

1. **WS-03 / T005 + T029** — Must go green before 2026-10-15 or no-ship (`CMT-2026-09-002`).
2. **WS-05 / T031** — Keep MedFirst OOM on the release-critical path.
3. **WS-07 / T022** — Retarget quota halt thresholds to 2GB + 10% buffer (`CMT-2026-09-003`).

## Blockers / waiting-on items

- **T011 no-ship deadline** — Hard 2026-10-15 gate on T005 and T029. Evidence: `CMT-2026-09-002`, `SRC-MEET-10`.
- **T036 expanded scope** — Form XObject failures may outlive upstream scaling fix. Evidence: `CMT-2026-09-001`, `SRC-SLACK-58`.
- **T030 Legal P0** — AGPL gate still open. Evidence: `CMT-2026-08-002`.
- **T019 escrow** — Still unimplemented. Evidence: `CMT-2026-08-001`.

## Recently changed requests

- **Release board no-ship deadline.** Evidence: `CMT-2026-09-002`.
- **Quota production baseline corrected to 2GB.** Evidence: `CMT-2026-09-003`.
- **Form XObject scope added to T036.** Evidence: `CMT-2026-09-001`.

## Items that need follow-up in Slack or the next status update call

- Certificate procurement status for T029.
- Clinic VM re-verify plan after 2GB quota retarget.

## Needs manual triage

- Whether Form XObject subset needs a separate local fix vs waiting on upstream (`CMT-2026-09-001`).

## Source links used

- `SRC-SLACK-23` — [communication/sources/slack/2026-08-06-storage-quota-halt.md](../med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md)
- `SRC-SLACK-37` — [communication/sources/slack/2026-09-02-windows-signing-gap.md](../med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)
- `SRC-SLACK-58` — [communication/sources/slack/2026-09-10-high-dpi-upstream-block.md](../med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md)
- `SRC-MEET-10` — [communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md](../med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md)
- `SRC-GDOC-49` — [documentation/sources/2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md](../med-synth/documentation/sources/2026-09-10-High-DPI-PDF-Rendering-Coordinates-Report.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-21` — [tasks/CIPH-21-Release-v1-Gates.md](../med-synth/tasks/CIPH-21-Release-v1-Gates.md)
- `SRC-CU-CIPH-32` — [tasks/CIPH-32-Storage-Quota-Management.md](../med-synth/tasks/CIPH-32-Storage-Quota-Management.md)
- `SRC-CU-CIPH-46` — [tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md](../med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-08-001` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-002` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-003` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-09-001` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)
- `CMT-2026-09-002` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)
- `CMT-2026-09-003` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)

<!-- DAILY_BRIEF:END -->
