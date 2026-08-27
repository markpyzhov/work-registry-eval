# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

## Answer

**No — as of 2026-09-22 the Windows release gate is not cleared.** The engineering work is done, but the gate is a compound one and its second condition (code signing) is still open, so both the Windows compatibility task (CIPH-39 / T029) and the release checklist that depends on it (CIPH-21 / T011) remain Active.

### Engineering completion (done)

- Windows builds had been failing on backslash/path-separator assumptions in the ingestion logic. Evan fixed this on **2026-08-10** by moving path handling to be OS-aware rather than hardcoded, and fixed the Linux-style temp-directory assumption in the same pass. Path arguments are now normalized to the platform-native separator before reaching the file-loading code (SRC-SLACK-36; SRC-GDOC-23 / DOC-2023).
- On **2026-08-12** the path fix unblocked packaging and a Windows build artifact was produced. Evan installed it on a Windows box and it passed the same sanity checks run on Linux. Asked directly whether Windows compatibility was therefore done, Evan drew the line explicitly: the engineering work for the Windows build is complete — packaging works, the binary is sound — but code-signing was a separate item not yet started, so he would not call the whole thing closed. Alice agreed to track signing on its own (SRC-SLACK-38).
- The 2026-09-02 compatibility audit confirms this framing: packaging itself is no longer the blocker (SRC-GDOC-39 / DOC-2039).
- The path fix also held up over time — on 2026-08-15 Evan reported no regressions in the build (SRC-MEET-08).

### The remaining release hold (open)

- The produced artifact is **unsigned**, so Windows Defender flags the binary as untrusted and SmartScreen warns on it. On 2026-09-02 Evan reported both were flagging the build for pilot testers; every pilot install would trip a warning at best and be blocked outright at worst (SRC-SLACK-37).
- **Root cause**: no code-signing certificate has been procured or configured in the Windows build pipeline. The impact is material for deployment — site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override (SRC-GDOC-39).
- This is explicitly not solvable on the engineering side. Evan: the team needs the certificate, and it cannot be worked around. Alice decided to keep it open on the release gate rather than push it off the board, and took ownership of chasing the certificate process (SRC-SLACK-37). On 2026-08-15 she had already asked Evan to keep chasing procurement, with Evan reporting no firm timeline (SRC-MEET-08).
- CIPH-39's acceptance criteria make the gap formal: producing the artifact is only the first of three criteria; the build must also be code-signed with a valid certificate and pass Defender/SmartScreen without warnings. Its last activity entry is Evan's 2026-09-02 "Signing Cert Missing," status Active (SRC-CU-CIPH-39).

### What still has to happen

1. **Procure a code-signing certificate** — the sole open blocker, owned by Alice on the procurement side, with no firm timeline recorded.
2. **Wire signing into the release build step** so the Windows build pipeline emits a signed artifact (SRC-GDOC-39).
3. **Verify the signed build passes Defender/SmartScreen without warnings**, satisfying CIPH-39's remaining two acceptance criteria (SRC-CU-CIPH-39).

Only then does T029 clear, and by extension its contribution to the T011 release checklist.

### Status as of 2026-09-22

The most recent gate review in the dataset is the **2026-09-15 pre-release audit**, where Alice opened by listing Windows signing as still open alongside the Docker slim-down/CVE work and the upstream high-DPI block; Evan noted the release is not opening with any of those unresolved, and Alice closed with "no one closes those today" (SRC-MEET-10). Nothing in the dataset dated between 2026-09-15 and 2026-09-22 reports the certificate arriving or the signing gate clearing — the 2026-09-22 records concern a different workstream (the handshake timeout block, SRC-MEET-11 / SRC-SLACK-27 / SRC-CU-CIPH-34). So the position on 2026-09-22 is unchanged.

**Worth flagging for release planning**: even once Windows signing clears, the release itself does not open. Diana placed a security-gate hold pending *both* T029's Windows signing and T005's Docker image slim-down/CVE work, and CIPH-21 remains Active with those two gates unresolved (SRC-CU-CIPH-21). The 2026-09-15 audit adds a third live hold — Diana is keeping the audit-log gate red because the CLI-emitted records don't match the defined schema (SRC-MEET-10). Clearing Windows signing is necessary but not sufficient.

### Sources cited

- `SRC-CU-CIPH-39` — med-synth/tasks/CIPH-39-Windows-Compatibility.md
- `SRC-GDOC-39` (DOC-2039) — med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md
- `SRC-SLACK-38` — med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md
- `SRC-SLACK-37` — med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md
- `SRC-SLACK-36` — med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md
- `SRC-GDOC-23` (DOC-2023) — med-synth/documentation/sources/2026-08-19-Windows-Compatibility-Review.md
- `SRC-MEET-08` — med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md
- `SRC-MEET-10` — med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md
- `SRC-CU-CIPH-21` — med-synth/tasks/CIPH-21-Release-v1-Gates.md
