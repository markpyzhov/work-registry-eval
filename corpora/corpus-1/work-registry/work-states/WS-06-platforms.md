# WS-06: External Interfaces and Platform Compatibility
**Status**: in_progress
**Priority**: P2
**Owner**: Diana / Evan
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-28` — [ClickUp Task CIPH-28: Local Runtime Compatibility](../med-synth/tasks/CIPH-28-Local-Runtime-Compatibility.md)
- `S2` — `SRC-SLACK-15` — [Slack Thread: Local Runtime Static Compile](../med-synth/communication/sources/slack/2026-08-04-local-runtime-static-compile.md)
- `S3` — `SRC-CU-CIPH-33` — [ClickUp Task CIPH-33: Redaction Preview UI](../med-synth/tasks/CIPH-33-Redaction-Preview-UI.md)
- `S4` — `SRC-SLACK-25` — [Slack Thread: Redaction Preview Highlighting](../med-synth/communication/sources/slack/2026-08-06-redaction-preview-highlighting.md)
- `S5` — `SRC-CU-CIPH-37` — [ClickUp Task CIPH-37: Air-Gapped Mode Testing](../med-synth/tasks/CIPH-37-Air-Gapped-Mode-Testing.md)
- `S6` — `SRC-SLACK-33` — [Slack Thread: Offline Batch Run](../med-synth/communication/sources/slack/2026-08-08-offline-batch-run.md)
- `S7` — `SRC-CU-CIPH-39` — [ClickUp Task CIPH-39: Windows Compatibility](../med-synth/tasks/CIPH-39-Windows-Compatibility.md)
- `S8` — `SRC-SLACK-38` — [Slack Thread: Windows Build Artifact](../med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md)
- `S9` — `SRC-SLACK-37` — [Slack Thread: Windows Signing Gap](../med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)
- `S10` — `SRC-CU-CIPH-45` — [ClickUp Task CIPH-45: GUI Wrapper for CLI](../med-synth/tasks/CIPH-45-GUI-Wrapper-for-CLI.md)
- `S11` — `SRC-SLACK-55` — [Slack Thread: Electron Package Test](../med-synth/communication/sources/slack/2026-08-18-electron-package-test.md)
- `S12` — `SRC-GDOC-48` — [GUI Desktop Wrapper Evaluation](../med-synth/documentation/sources/2026-08-31-GUI-Desktop-Wrapper-Evaluation.md)
- `S13` — `SRC-CU-CIPH-46` — [ClickUp Task CIPH-46: High-DPI PDF Rendering Fixes](../med-synth/tasks/CIPH-46-High-DPI-PDF-Rendering-Fixes.md)
- `S14` — `SRC-SLACK-58` — [Slack Thread: High-DPI Upstream Block](../med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md)

## Request / Context
Cross-platform accessibility: static binaries, preview UI, air-gapped verification, Electron desktop wrapper, Windows compatibility, and High-DPI rendering.

## Task List
- [x] `T018` (mapped to CIPH-28) — Ensure local runtime binary static linking. `(S1, S2)`
- [x] `T023` (mapped to CIPH-33) — Implement visual redaction preview UI overlay. `(S3, S4)`
- [x] `T027` (mapped to CIPH-37) — Conduct strict offline air-gapped mode testing. `(S5, S6)`
- [ ] `T029` (mapped to CIPH-39) — Ensure Windows OS compatibility. `(S7, S8, S9)`
- [x] `T035` (mapped to CIPH-45) — Create Electron GUI desktop wrapper for CLI. `(S10, S11, S12)`
- [ ] `T036` (mapped to CIPH-46) — Fix High-DPI PDF rendering coordinate alignment. `(S13, S14)`

## Active Work
- **T029 / CIPH-39**: **Active** — Windows path backslash handling is fixed (`S8`), but release remains **held on code-signing**: Windows Defender SmartScreen flags unsigned binaries until an Authenticode certificate is procured (`S9`). Engineering work continues; the signing gap is a procurement dependency, not an engineering block. `(S7, S8, S9)`

## Blockers and Dependencies
- **T036 — Form XObject scope (CMT-2026-09-001)**: Offline QA: 12% of MedFirst pilot corpus fails due to nested Form XObjects, beyond upstream 4K scaling alone. `(CMT-2026-09-001)`
- **T036 / CIPH-46**: **Blocked** by upstream rendering-library scaling math; redaction coordinates drift 5–10 pixels on 4K displays at 200% scaling. `(S14)`

## Decisions and Superseded Directions
- **Binary Distribution**: Python environment shipping superseded by single-file static binary via PyInstaller. `(S1, S2)`

## Done / Evidence
- `T018 / CIPH-28` — Static binary verified on bare-metal Ubuntu and CentOS without shared-library dependencies. `(S2)`
- `T023 / CIPH-33` — React preview UI renders PDF pages with redaction bounding-box overlays. `(S4)`
- `T027 / CIPH-37` — 1,000 files processed in a networking-disabled VM. `(S6)`
- `T035 / CIPH-45` — Electron wrapper bundles CLI; package test passes with IPC bridge to batch CLI (`S11`, `S12`). Progress-bar smoothness is a non-blocking UX follow-up. `(S11, S12)`

## Needs Manual Triage
- Nested Form XObject handling may require engine-side workaround if upstream scaling fix does not cover the 12% pilot subset. `(CMT-2026-09-001)`
- Budget and procurement timeline for Windows Authenticode code-signing certificate.

## Next Update Needed
Code-signing certificate status and upstream High-DPI fix timeline.
