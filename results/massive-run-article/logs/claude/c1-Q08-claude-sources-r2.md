# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

## No — the Windows release gate is not cleared as of 2026-09-22.

Engineering completion and gate clearance are two different things here, and the sources are explicit about the split.

### What is done (engineering)

- The backslash path-handling defects that had been breaking Windows builds were fixed on **2026-08-10**. Path arguments are now normalized to the platform-native separator before reaching the file-loading code, and the OS-level temp location is respected instead of a hardcoded Linux-style path (SRC-SLACK-36; SRC-GDOC-23 / DOC-2023).
- A Windows build artifact was successfully produced by **2026-08-12**, and it runs — Evan installed it on a Windows box and it passed the same sanity checks used on Linux (SRC-SLACK-38; SRC-GDOC-39 / DOC-2039).
- Evan stated the position plainly on 2026-08-12: the engineering work for the Windows build is complete — packaging works, the binary is sound — but code-signing is a separate item, so he would not call the whole thing closed (SRC-SLACK-38).
- Packaging itself is explicitly no longer the blocker, and the path fix has held up with no regressions (SRC-GDOC-39; SRC-MEET-08, 2026-08-15).

### What is still holding the gate

- The produced artifact is **unsigned**. Windows Defender flags the binary as untrusted and SmartScreen warns on it. Site IT policies commonly block unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override (SRC-GDOC-39).
- Root cause: **no code-signing certificate has been procured or configured** in the Windows build pipeline. As of 2026-09-02, Evan confirmed the team still does not have one, and that this is not something engineering can work around — the certificate is required (SRC-SLACK-37; SRC-CU-CIPH-39).
- CIPH-39 ("Fix Windows builds and clear Defender/SmartScreen signing") remains **Active**, assigned to Evan, High priority. Two of its three acceptance criteria are unmet: the build is not code-signed with a valid certificate, and it has not passed Defender/SmartScreen without warnings (SRC-CU-CIPH-39).
- Procurement had **no firm timeline** as of 2026-08-15, with Alice taking on chasing the certificate process on 2026-09-02 (SRC-MEET-08; SRC-SLACK-37).
- At the pre-release audit on **2026-09-15** — the last gate review in the sources before 2026-09-22 — Alice confirmed Windows signing is still open, alongside the Docker slim-down/CVE work and the upstream high-DPI bug, with Evan noting "Release isn't opening with any of those unresolved" (SRC-MEET-10).
- The release checklist task CIPH-21 (T011) is **Active**, with Diana's security-gate hold in place pending both T005 (Docker image slim-down/CVE) and T029 (Windows Defender/SmartScreen code-signing). Its dependency criteria T001–T006 and T010 are met; the two security gates are not (SRC-CU-CIPH-21).

No source in the dataset records the certificate arriving, signing being wired in, or the gate being cleared at any point up to 2026-09-22. The latest gate review on record (2026-09-15) still lists it as open, and CIPH-39's last activity entry is the 2026-09-02 "Signing Cert Missing" update.

### What still has to happen

1. **Procure a code-signing certificate.** This is a procurement action, not an engineering one — it is the sole open blocker on the Windows item and cannot be worked around in code (SRC-GDOC-39; SRC-SLACK-37).
2. **Wire signing into the release build step** so the Windows artifact is signed as part of the pipeline (SRC-GDOC-39).
3. **Verify the signed build passes Defender/SmartScreen without warnings**, satisfying CIPH-39's remaining acceptance criteria and closing the T029 gate (SRC-CU-CIPH-39).
4. Only then does the Windows leg of the release checklist clear. Note that **clearing Windows alone does not open the release**: CIPH-21 is held on T005's Docker slim-down/CVE work as well, and as of the 2026-09-15 audit the audit-log gate was also red (CLI-emitted records not matching the defined schema) with the upstream high-DPI rendering bug still blocked (SRC-CU-CIPH-21; SRC-MEET-10; SRC-CU-CIPH-26).

### Sources cited

- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39 / DOC-2039)
- `med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md` (SRC-GDOC-23 / DOC-2023)
- `med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md` (SRC-SLACK-36)
- `med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md` (SRC-SLACK-38)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/tasks/CIPH-26-Audit-Trail-Logging.md` (SRC-CU-CIPH-26)
