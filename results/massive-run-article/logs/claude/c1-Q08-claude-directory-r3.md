# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

**No — the Windows release gate is not cleared as of 2026-09-22.** The engineering work is done; the gate is held on a procurement item.

## Engineering completion (done)

- **Path handling fixed (2026-08-10).** Windows builds had been failing on backslash/path-separator assumptions in the ingestion logic. Evan reworked path handling to be OS-aware rather than hardcoded, and fixed the temp-directory assumption in the same pass so it uses the OS-level temp location. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md`
- **Build artifact produced and validated (2026-08-12).** The artifact not only builds but runs — installed on a Windows box and passing the same sanity checks used on Linux. Evan explicitly said "the engineering work for the Windows build is complete — packaging works, the binary is sound," while noting code-signing was a separate, not-yet-started item. Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md`
- The 2026-08-19 retrospective note explicitly scopes itself to path-string handling only and states it does **not** cover code signing or Defender/SmartScreen — those are separate, later concerns for CIPH-39.

## The remaining hold (not engineering)

- **Missing Authenticode code-signing certificate.** On 2026-09-02 Evan reported Windows Defender and SmartScreen flagging the build for pilot testers: unsigned binaries are treated as untrusted by default. Alice asked if the missing certificate was the actual blocker; Evan confirmed and said "this isn't something we can work around on the engineering side, we need the certificate." Alice kept it open on the release gate and took the certificate-procurement chase. Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`
- **Impact.** Site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, preventing installation on target deployment workstations without a manual security-policy override. Root cause: no certificate procured or configured in the Windows build pipeline. Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`
- **Authoritative current state.** WS-06 records T029 / CIPH-39 as **Active, not complete**: path handling fixed, "but release remains held on code-signing… the signing gap is a procurement dependency, not an engineering block." CIPH-39 remains Active with unmet acceptance criteria (build must be code-signed and pass SmartScreen without warnings). Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md`

## What still has to happen

1. **Procure the Authenticode code-signing certificate.** Alice owns chasing the certificate process; budget and procurement timeline are flagged under WS-06 "Needs Manual Triage" as an unresolved item.
2. **Wire signing into the release build step.** The audit report names procurement *plus* configuring signing in the Windows build pipeline as the only remaining work before T029 clears.
3. **Re-verify against Defender/SmartScreen.** CIPH-39's acceptance criteria require the signed build to pass without warnings — so a verification pass on the signed artifact is needed, not just the certificate.

## Release-level consequence

Clearing T029 is necessary but not sufficient for shipping. T011 (release gates, CIPH-21) is under a security-gate hold and **cannot close until both T029 and T005 (Docker image slim-down/CVE) are green** — the 2026-09-15 pre-release audit also kept the audit-log schema mismatch visible as a blocker. The release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green (explicitly "not advisory"). As of the 2026-09-22 brief, both remain open, and securing the Authenticode cert is listed as a required follow-up. Sources: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md` (CMT-2026-09-002), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md`

**Bottom line:** a working build artifact settled the engineering question on 2026-08-12, but the gate measures shippability, not compilability. With roughly three weeks to the 2026-10-15 no-ship date and the sole remaining step sitting in procurement rather than engineering, the schedule risk is now outside the team's direct control.
