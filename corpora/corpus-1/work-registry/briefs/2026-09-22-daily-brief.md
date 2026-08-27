# CipherDoc Daily Brief - 2026-09-22

<!-- DAILY_BRIEF:BEGIN -->

## Today's active CipherDoc work

- **Release gates (T011)** — Security-gate hold remains: Docker size/CVE (T005) and Windows signing (T029) still open against the **2026-10-15** no-ship deadline. Evidence: [WS-03-ops](../work-states/WS-03-ops.md); `SRC-MEET-10`, `SRC-CU-CIPH-21`, `CMT-2026-09-002`, `SRC-SLACK-37`.
- **Zero-trust node sync (T024)** — **Blocked** on high-latency handshake. Meeting deep-dive declines a simple timeout-bump pending encryption-path stabilization; Singapore field trial separately reports failures at 180ms RTT with the 5s prototype timeout and calls for a **30s** timeout budget on high-latency links. Evidence: [WS-07-storage](../work-states/WS-07-storage.md); `SRC-MEET-11`, `SRC-SLACK-27`, `SRC-CU-CIPH-34`, `CMT-2026-09-004`.
- **Storage quota (T022)** — 2GB production baseline + 10% buffer refactor still in progress. Evidence: [WS-07-storage](../work-states/WS-07-storage.md); `CMT-2026-09-003`, `SRC-SLACK-23`.
- **Async batch I/O race (T037)** — Concurrent I/O race still blocks scheduler reliability. Evidence: [WS-05-performance](../work-states/WS-05-performance.md); `SRC-SLACK-61`, `SRC-CU-CIPH-47`.
- **License compliance (T030)** — P0 Legal AGPL/whole-bundle gate still open. Evidence: `CMT-2026-08-002`, `SRC-CU-CIPH-40`.

## Priority order

1. **WS-03 / T005 + T029** — Clear before 2026-10-15 or no-ship (`CMT-2026-09-002`).
2. **WS-07 / T024** — Resolve high-latency handshake path; reconcile field 30s budget vs meeting caution (`CMT-2026-09-004`, `SRC-MEET-11`).
3. **WS-04 / T030** — Close Legal gate on non-AGPL parser.

## Blockers / waiting-on items

- **T011** — Depends on T005 and T029; hard 2026-10-15 deadline. Evidence: `CMT-2026-09-002`.
- **T024** — High-latency handshake blocked; field timeout budget vs meeting no-timeout-bump tension. Evidence: `SRC-MEET-11`, `CMT-2026-09-004`.
- **T036** — Upstream scaling + Form XObject scope. Evidence: `SRC-SLACK-58`, `CMT-2026-09-001`.
- **T031** — MedFirst pilot OOM still release-coupled. Evidence: `CMT-2026-08-003`.
- **T019** — Escrow still unimplemented. Evidence: `CMT-2026-08-001`.
- **T007** — Upstream #992 + Legal workaround gate. Evidence: `CMT-2026-06-003`.

## Recently changed requests

- **Singapore field timeout budget (30s) recorded.** Evidence: `CMT-2026-09-004`.
- **Handshake protocol deep-dive held today.** Evidence: `SRC-MEET-11`.

## Items that need follow-up in Slack or the next status update call

- Decide whether 30s timeout budget can be tested without violating the meeting's encryption-path caution.
- Secure Authenticode cert and finish Alpine/CVE Docker verification.

## Needs manual triage

- Whether a 30s timeout budget resolves Singapore 180ms RTT failures without redesigning handshake exchange count (`CMT-2026-09-004` vs `SRC-MEET-11`).
- Form XObject subset: local fix vs upstream-only (`CMT-2026-09-001`).

## Source links used

- `SRC-SLACK-23` — [communication/sources/slack/2026-08-06-storage-quota-halt.md](../med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md)
- `SRC-SLACK-27` — [communication/sources/slack/2026-08-08-node-sync-handshake-validation.md](../med-synth/communication/sources/slack/2026-08-08-node-sync-handshake-validation.md)
- `SRC-SLACK-37` — [communication/sources/slack/2026-09-02-windows-signing-gap.md](../med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)
- `SRC-SLACK-58` — [communication/sources/slack/2026-09-10-high-dpi-upstream-block.md](../med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md)
- `SRC-SLACK-61` — [communication/sources/slack/2026-08-25-async-batch-io-race.md](../med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md)
- `SRC-MEET-10` — [communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md](../med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md)
- `SRC-MEET-11` — [communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md](../med-synth/communication/sources/fireflies/2026-09-22-Handshake-Protocol-Deep-Dive.md)
- `SRC-CU-CIPH-21` — [tasks/CIPH-21-Release-v1-Gates.md](../med-synth/tasks/CIPH-21-Release-v1-Gates.md)
- `SRC-CU-CIPH-34` — [tasks/CIPH-34-Zero-Trust-Node-Sync.md](../med-synth/tasks/CIPH-34-Zero-Trust-Node-Sync.md)
- `SRC-CU-CIPH-40` — [tasks/CIPH-40-License-Compliance-Review.md](../med-synth/tasks/CIPH-40-License-Compliance-Review.md)
- `SRC-CU-CIPH-47` — [tasks/CIPH-47-Async-Batch-Processing.md](../med-synth/tasks/CIPH-47-Async-Batch-Processing.md)
- `CMT-2026-06-003` — [work-states/comments/2026-06.md](../work-states/comments/2026-06.md)
- `CMT-2026-08-001` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-002` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-08-003` — [work-states/comments/2026-08.md](../work-states/comments/2026-08.md)
- `CMT-2026-09-001` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)
- `CMT-2026-09-002` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)
- `CMT-2026-09-003` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)
- `CMT-2026-09-004` — [work-states/comments/2026-09.md](../work-states/comments/2026-09.md)

<!-- DAILY_BRIEF:END -->
