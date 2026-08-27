# CipherDoc Daily Brief - 2026-09-02

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Windows signing gap (T029)** — Native Windows build is functional after path fixes, but Defender SmartScreen flags unsigned binaries; Authenticode certificate needed. Evidence: [WS-06-platforms](../work-states/WS-06-platforms.md); `SRC-SLACK-37`, `SRC-GDOC-39`, `SRC-CU-CIPH-39`.
- **GUI wrapper (T035)** — Desktop pack test: CLI binary bundled and reachable via IPC bridge. Evidence: [WS-06-platforms](../work-states/WS-06-platforms.md); `SRC-CU-CIPH-45`, `SRC-GDOC-29`, `SRC-GDOC-48`.
- **High-DPI PDF rendering (T036)** — Coordinate report confirms 5–10px drift on 4K monitors; appears upstream scaling-related. Evidence: [WS-06-platforms](../work-states/WS-06-platforms.md); `SRC-GDOC-30`, `SRC-CU-CIPH-46`.
- **Memory leak / large-file path (T031)** — Remains a MedFirst pilot-blocker until buffer release is proven on clinic hardware. Evidence: [WS-05-performance](../work-states/WS-05-performance.md); `CMT-2026-08-003`, `SRC-CU-CIPH-43`.
- **Async batch processing (T037)** — Queue/workers work continues; I/O race still a risk. Evidence: [WS-05-performance](../work-states/WS-05-performance.md); `SRC-SLACK-59`, `SRC-SLACK-60`, `SRC-CU-CIPH-47`.

## Priority order

1. **WS-06 / T029 (CIPH-39)** — Secure code-signing certificate path for Windows release.
2. **WS-05 / T031 (CIPH-43)** — Close MedFirst OOM pilot-blocker.
3. **WS-06 / T036 (CIPH-46)** — Log/track upstream scaling bug; keep local repro current.

## Blockers / waiting-on items

- **T029 signing** — SmartScreen / Authenticode gap blocks clean Windows ship. Evidence: `SRC-SLACK-37`.
- **T030 Legal P0** — AGPL whole-bundle gate still open. Evidence: `CMT-2026-08-002`.
- **T019 escrow** — Still Blocked pending implementation. Evidence: `CMT-2026-08-001`.
- **T005 Docker** — Dual size gates and CVE verification still open. Evidence: `CMT-2026-06-002`, `SRC-CU-CIPH-15`.
- **T024 handshake** — Intermittent high-latency timeouts noted earlier; not yet a hard field failure. Evidence: `SRC-SLACK-27`.

## Recently changed requests

- **Windows signing gap surfaced.** Evidence: `SRC-SLACK-37`.
- **High-DPI coordinate report dated today.** Evidence: `SRC-GDOC-30`.

## Items that need follow-up in Slack or the next status update call

- Alice: budget/process for Authenticode certificate.
- Diana: upstream bug filing for 4K scaling drift.

## Needs manual triage

- None currently.

## Source links used

- `SRC-SLACK-27` — [communication/sources/slack/2026-08-08-node-sync-handshake-validation.md](../med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md)
- `SRC-SLACK-37` — [communication/sources/slack/2026-09-02-windows-signing-gap.md](../med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)
- `SRC-SLACK-59` — [communication/sources/slack/2026-08-20-async-batch-scheduler.md](../med-synth/communication/sources/slack/2026-08-20-async-batch-scheduler.md)
- `SRC-SLACK-60` — [communication/sources/slack/2026-08-22-async-batch-workers.md](../med-synth/communication/sources/slack/2026-08-22-async-batch-workers.md)
- `SRC-GDOC-29` — [documentation/sources/2026-08-31-GUI-Wrapper-for-CLI-Review.md](../med-synth/documentation/sources/2026-08-31-GUI-Wrapper-for-CLI-Review.md)
- `SRC-GDOC-30` — [documentation/sources/2026-09-02-High-DPI-PDF-Rendering-Fixes-Review.md](../med-synth/documentation/sources/2026-09-02-High-DPI-PDF-Rendering-Fixes-Review.md)
- `SRC-GDOC-39` — [documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md](../med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md)
- `SRC-GDOC-48` — [documentation/sources/2026-08-31-GUI-Desktop-Wrapper-Evaluation.md](../med-synth/documentation/sources/2026-08-31-GUI-Desktop-Wrapper-Evaluation.md)
- `SRC-CU-CIPH-15` — [tasks/CIPH-15-Docker-Packaging.md](../med-synth/tasks/CIPH-15-Docker-Packaging.md)
- `SRC-CU-CIPH-39` — [tasks/CIPH-39-Windows-Compatibility.md](../med-synth/tasks/CIPH-39-Windows-Compatibility.md)
- `SRC-CU-CIPH-43` — [tasks/CIPH-43-Memory-Leak-Profiling.md](../med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md)
- `SRC-CU-CIPH-45` — [tasks/CIPH-45-GUI-Wrapper-for-CLI.md](../med-synth/tasks/CIPH-45-GUI-Wrapper-for-CLI.md)
- `SRC-CU-CIPH-46` — [tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md](../med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md)
- `SRC-CU-CIPH-47` — [tasks/CIPH-47-Async-Batch-Processing.md](../med-synth/tasks/CIPH-47-Async-Batch-Processing.md)
- `CMT-2026-06-002` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-08-001` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-002` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-003` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)

<!-- DAILY_BRIEF:END -->
