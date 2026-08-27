# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

I have complete evidence. Here is the answer.

---

**No — the Windows release gate is not cleared as of 2026-09-22.** A working build artifact exists, but the gate itself remains open. The engineering work and the release hold are two separate things, and only the first is done.

## Engineering completion (done)

- The backslash path-handling defects that broke Windows builds were fixed on **2026-08-10**. Path arguments are now normalized to the platform-native separator before reaching the file-loading code (SRC-GDOC-23 / DOC-2023, `med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md`).
- A Windows build artifact was successfully produced by **2026-08-12**. Evan confirmed it does not just build — it was installed on a Windows box and passed the same sanity checks run on Linux (SRC-SLACK-38, `2026-08-12-windows-build-artifact.md`).
- Evan drew the line explicitly in that same thread: the engineering work for the Windows build is complete, packaging works and the binary is sound, but code-signing is a separate item not yet started, so he would not call the whole thing closed. Alice agreed to track signing on its own (SRC-SLACK-38).
- Packaging is confirmed as no longer the blocker (SRC-GDOC-39 / DOC-2039, `2026-09-02-Windows-Compatibility-Audit-Report.md`).

## The remaining release hold (open)

- **The artifact is unsigned.** No Authenticode code-signing certificate has been procured or configured in the Windows build pipeline. Windows Defender and SmartScreen flag the unsigned binary as untrusted (SRC-GDOC-39; SRC-SLACK-37, `2026-09-02-windows-signing-gap.md`).
- **Impact:** every pilot install trips a warning at best and is blocked outright at worst; site IT policies commonly block unsigned/SmartScreen-flagged binaries without a manual security-policy override (SRC-SLACK-37; SRC-GDOC-39).
- **Nature of the block:** this is a **procurement dependency, not an engineering block**. Evan's position on 2026-09-02: it cannot be worked around on the engineering side — the certificate is required. Alice decided to keep it open on the release gate rather than push it off the board, and took the certificate chase (SRC-SLACK-37; WS-06 Active Work).
- **Task status:** CIPH-39 / T029 remains **Active**, assigned to Evan. Its acceptance criteria are three-part: artifact produced (met), build code-signed with a valid certificate (not met), signed build passes Defender/SmartScreen without warnings (not met) (SRC-CU-CIPH-39).
- WS-06 (`work-states/WS-06-platforms.md`, last updated 2026-09-22) is `in_progress` with T029 unchecked, and lists "Budget and procurement timeline for Windows Authenticode code-signing certificate" under Needs Manual Triage. Its Next Update Needed is code-signing certificate status.

## What still has to happen

1. **Procure a Windows Authenticode code-signing certificate.** This is the sole open blocker on the Windows gate (SRC-GDOC-39). Budget and procurement timeline are still untriaged (WS-06); Alice owns chasing the process (SRC-SLACK-37).
2. **Wire signing into the release build step** so the artifact ships signed (SRC-GDOC-39).
3. **Verify the signed build passes Defender/SmartScreen with no warnings** — the third acceptance criterion on CIPH-39 (SRC-CU-CIPH-39).

Only then does T029 go green and CIPH-39 close.

## Wider release context

Clearing Windows signing alone will not open the v1.0.0 release. Per WS-03 (`work-states/WS-03-ops.md`, last updated 2026-09-22) and CIPH-21:

- **T011 / CIPH-21** is Active under a security-gate hold placed by Diana, and cannot close until **both** T005 (Docker image size/CVE) and T029 (Windows code-signing) are green. Checklist dependencies T001–T006 and T010 are satisfied.
- **T005 / CIPH-15** is reopened/active: the image ballooned to 2.1GB after OCR dependencies were bundled; multi-stage builds and an Alpine swap were implemented, but as of August 12 it still exceeds the ~450MB target and CVE verification is failing. A CISO review set dual thresholds — interim RC at 800MB once CVE-clean, GA at ~450MB (CMT-2026-06-002).
- The **2026-09-15 pre-release audit** (SRC-MEET-10) listed Docker slim/CVE, Windows signing, and audit-log schema alignment as open blockers, with the upstream high-DPI rendering bug also still blocked. Diana is holding the audit-log gate red until the CLI-emitted records match the defined schema (verification found a mismatch on 2026-09-18, CIPH-26). Alice's close: security-gate work stays open, nobody closes those.
- **Hard deadline:** the release board set a **no-ship after 2026-10-15** if T005 and T029 are not green (CMT-2026-09-002).

**Bottom line:** engineering-complete, release-blocked. The build works; the gate is held on a certificate purchase nobody has made yet, with roughly three weeks to the no-ship date as of the 2026-09-22 state.
