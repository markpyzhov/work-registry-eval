# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

## No — the Windows release gate is **not** cleared as of 2026-09-22

T029 / CIPH-39 is still open, and it is one of two gates holding the v1.0 release.

### Engineering completion (done)
- **Path handling fixed (2026-08-10).** Backslash/Windows-style path assumptions in the CLI's path parser were replaced with OS-aware normalization to the platform-native separator; the OS-level temp-directory assumption was fixed in the same pass. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md`
- **Working build artifact produced and validated (2026-08-12).** Evan produced a Windows artifact, installed it on a Windows box, and it passed the same sanity checks run on Linux — it runs, not just builds. He explicitly scoped this: "The engineering work for the Windows build is complete — packaging works, the binary is sound," while noting signing had not been started. Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md`
- The authoritative Work State records this the same way: packaging/path work is done, and the remaining item is explicitly characterized as "a procurement dependency, not an engineering block." Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md` (Active Work, T029)

### The remaining release hold (open)
- **Missing Authenticode code-signing certificate.** The artifact is unsigned, so Windows Defender flags it and SmartScreen warns; pilot testers hit warnings at best and outright blocks at worst. Site IT policies commonly block unsigned/SmartScreen-flagged binaries entirely, which would prevent installation on target deployment workstations without a manual security-policy override. Root cause: no certificate has been procured or wired into the Windows build pipeline. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`
- **CIPH-39 remains Active**, with acceptance criteria requiring a code-signed build that passes Defender/SmartScreen without warnings — two of three criteria unmet. Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`
- Alice's decision on 2026-09-02 was to keep it open **on the release gate** rather than push it off the board, and to chase the certificate process herself. Procurement had no firm timeline as of the 2026-08-15 sync. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`

### Release-level impact
- The 2026-09-15 pre-release audit reconfirmed Windows signing as an open gate alongside Docker slim/CVE and the audit-log schema mismatch; Alice: "No one closes those today." Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`
- **T011 / CIPH-21 (Release v1.0 gates) cannot close** until both T005 (Docker size/CVE) and T029 (Windows signing) are green. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`
- **Hard deadline: the release board set a no-ship after 2026-10-15** if T005 and T029 are not green — recorded as a hard deadline, not advisory. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-002), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

### What still has to happen
1. **Procure an Authenticode code-signing certificate** (Alice chasing procurement; budget and procurement timeline are flagged as needing manual triage in WS-06).
2. **Wire signing into the Windows release build step** so the artifact ships signed.
3. **Verify the signed build passes Defender/SmartScreen with no warnings** — the audit calls this the sole remaining item before T029 clears.
4. **Then** T011 can only clear once T005 (Docker slim-down/CVE verification) also goes green; the 2026-09-22 brief lists the paired action as "Secure Authenticode cert and finish Alpine/CVE Docker verification," before 2026-10-15.

Note (separate from T029): the other open WS-06 item, T036 / CIPH-46 High-DPI PDF rendering, remains blocked on an upstream scaling fix plus a nested Form XObject subset affecting 12% of the MedFirst pilot corpus. It is a distinct release blocker tracked in the same platform area, not part of the Windows signing gate. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-001)
