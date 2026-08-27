# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

**No — the Windows release gate is not cleared as of 2026-09-22.** The build works; the release is still held on code-signing.

## Engineering completion (done)

- **Path handling fixed, 2026-08-10.** Backslash/Windows-style path arguments were breaking builds; Evan made path handling OS-aware (normalizing to the platform-native separator) rather than a search-and-replace, and fixed the Linux-assuming temp-directory path in the same pass. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md`
- **Build artifact produced and verified, 2026-08-12.** It doesn't just build — Evan installed it on a Windows box and it passes the same sanity checks run on Linux. Evan's own framing at the time: the engineering work for the Windows build is complete, packaging works, the binary is sound — but code-signing is a separate item, so the task isn't closed. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md`
- The 2026-09-02 audit confirms packaging is no longer the blocker. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`

## The remaining hold (not engineering)

**T029 / CIPH-39 is still Active, held on a missing Authenticode code-signing certificate.** The produced artifact is unsigned, so Windows Defender and SmartScreen flag it as untrusted — pilot testers hit a warning at best and an outright block at worst, and site IT policies commonly block unsigned/SmartScreen-flagged binaries without a manual security-policy override. Evan's position on 2026-09-02: this cannot be worked around on the engineering side; the certificate is required. Alice kept it open on the release gate rather than pushing it off the board and took the certificate-chasing action. This is a **procurement dependency, not an engineering block** — that distinction is stated explicitly in the current work state. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md` (line 36), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`

## What still has to happen

To close T029 (Windows gate):
1. **Procure a code-signing certificate** — Alice owns chasing the process; budget and procurement timeline are still flagged as needing manual triage.
2. **Wire signing into the Windows release build step** — no cert has been procured *or configured in the pipeline* yet.
3. **Verify the signed build passes Defender/SmartScreen without warnings** — this is the explicit unmet acceptance criterion on CIPH-39.

Beyond T029, for the v1.0 release itself to open:
- **T005 (Docker image slim-down / CVE)** must also go green. T011 / CIPH-21 sits under a security-gate hold from Diana pending *both* T005 and T029. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- The 2026-09-15 pre-release audit also kept the **audit-log schema mismatch** red (CLI-emitted records don't match the defined schema), alongside Docker and Windows. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`

**Deadline:** the release board set a hard **no-ship after 2026-10-15** if T005 and T029 are not green — recorded as a firm decision, not advisory. That leaves roughly three weeks from the 2026-09-22 as-of date, and the 09-22 brief lists "secure Authenticode cert" as a top follow-up with WS-03 / T005+T029 as priority #1. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-002), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

**One-line answer:** engineering for Windows compatibility is effectively done — the build packages, installs, and passes sanity checks — but the gate stays open on a procurement item: no Authenticode certificate has been bought or wired into the pipeline, so the binary ships unsigned and trips Defender/SmartScreen, and T029 continues to hold the v1.0 release alongside the Docker CVE work.
