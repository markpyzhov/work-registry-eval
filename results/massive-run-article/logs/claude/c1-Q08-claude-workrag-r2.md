# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

**No — as of 2026-09-22 the Windows release gate (T029 / CIPH-39) is not cleared.** A working build artifact is necessary but not sufficient; the gate's acceptance criteria include code-signing, which has not happened.

## What is engineering-complete

- The backslash path-handling defects that broke Windows builds were fixed on **2026-08-10**, and a Windows build artifact was successfully produced by **2026-08-12**. Packaging itself is no longer the blocker. *(SRC-GDOC-39 / DOC-2039; SRC-SLACK-38)*
- The artifact is not just a build — Evan installed it on a Windows box and it passed the same sanity checks run on Linux. On 2026-08-12 he stated the engineering work for the Windows build was complete (packaging works, the binary is sound), while explicitly noting code-signing was a separate, not-yet-started item, so he would not call the whole thing closed. Alice agreed to track signing on its own. *(SRC-SLACK-38)*
- The path fix has held up with no regressions since. *(SRC-MEET-08, 2026-08-15)*

## What is still holding the gate

- **The release remains held on code-signing.** The produced artifact is unsigned, so Windows Defender flags it as untrusted and SmartScreen warns on it. Site IT policies commonly block unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override. Root cause: no code-signing certificate has been procured or configured in the Windows build pipeline. *(SRC-GDOC-39; SRC-CU-CIPH-39)*
- CIPH-39 is still **Active** (assignee Evan, High priority), pending that certificate. Its acceptance criteria require not only that the artifact is produced, but that it is code-signed with a valid certificate and passes Defender/SmartScreen without warnings. Only the first of the three is met. *(SRC-CU-CIPH-39)*
- Importantly, this is a **procurement dependency, not an engineering block** — the WS-06 work state states engineering work continues and characterizes the signing gap that way. On 2026-09-02 Evan said plainly that this is not something that can be worked around on the engineering side; the certificate is required. Alice chose to keep it open on the release gate rather than push it off the board, and took on chasing the certificate process. *(WS-06; SRC-SLACK-37)*
- As of 2026-08-15 there was **no firm timeline** for the certificate coming through procurement. *(SRC-MEET-08)*

## What still has to happen

1. **Procure the Windows Authenticode code-signing certificate.** This is the sole open blocker on T029. Budget and procurement timeline for it are flagged as needing manual triage in WS-06; Alice owns chasing the process. *(SRC-GDOC-39; WS-06; SRC-SLACK-37)*
2. **Wire signing into the release build step** so the artifact is signed as part of the pipeline. *(SRC-GDOC-39)*
3. **Verify the signed build passes Defender/SmartScreen without warnings** — the third acceptance criterion on CIPH-39. *(SRC-CU-CIPH-39)*

## Downstream consequence

Clearing T029 does not by itself unblock the release. The T011 release checklist (CIPH-21) is under a security-gate hold placed by Diana and **cannot close until both T029 (Windows code-signing) and T005 (Docker image slim-down / CVE work) are green**. T005 is separately still reopened — as of 2026-08-12 the image remained over the ~450MB target with CVE verification failing. The release board has set a hard **no-ship after 2026-10-15** if T005 and T029 are not green. *(SRC-CU-CIPH-21; WS-03, incl. CMT-2026-09-002; SRC-SLACK-06)*

WS-06 lists the code-signing certificate status as one of the two items it needs a next update on.

**Dataset records cited:** `work-states/WS-06-platforms.md`, `work-states/WS-03-ops.md`, `work-states/index.md`, `med-synth/tasks/CIPH-39-Windows-Compatibility.md`, `med-synth/tasks/CIPH-21-Release-v1-Gates.md`, `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md`, `med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md`, `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md`, `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md`, `med-synth/communication/sources/slack/2026-06-25-docker-size.md`.
