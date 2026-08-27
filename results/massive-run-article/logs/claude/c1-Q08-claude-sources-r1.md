# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

## Answer

**No — the Windows release gate is not cleared as of 2026-09-22.** The engineering work is done, but the gate itself remains open on a non-engineering blocker: a missing code-signing certificate.

### Engineering completion (done)

- The backslash/path-handling defects that broke Windows builds were fixed on **2026-08-10**, moving path handling to be OS-aware rather than hardcoded, and covering the temp-directory assumption in the same pass (SRC-SLACK-36).
- A Windows build artifact was successfully produced by **2026-08-12**. Evan confirmed it does not just build but runs: installed on a Windows box and passing the same sanity checks used on Linux (SRC-SLACK-38).
- Evan's own framing at the time: the engineering work for the Windows build is complete — packaging works, the binary is sound — but code-signing is a separate item, so he "wouldn't call the whole thing closed" (SRC-SLACK-38). Alice agreed to track signing separately.
- The compatibility audit states this plainly: "Packaging itself is no longer the blocker" (SRC-GDOC-39).

### The remaining release hold (not done)

- The produced artifact is **unsigned**, so Windows Defender flags the binary as untrusted and SmartScreen warns on it. Root cause per the audit: no code-signing certificate has been procured or configured in the Windows build pipeline (SRC-GDOC-39, last updated 2026-09-02).
- Practical impact: site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override (SRC-GDOC-39). Pilot testers were already hitting this — "a warning at best, get blocked outright at worst" (SRC-SLACK-37, 2026-09-02).
- This is explicitly **not** an engineering-solvable item: "this isn't something we can work around on the engineering side, we need the certificate" (Evan, SRC-SLACK-37). Alice decided to keep it open on the release gate rather than pushing it off the board, and took the certificate chase herself.
- Task **CIPH-39 / T029** ("Fix Windows builds and clear Defender/SmartScreen signing") remains **Active**, with two of three acceptance criteria unmet: the build must be code-signed with a valid certificate, and the signed build must pass Defender/SmartScreen without warnings (SRC-CU-CIPH-39).
- Procurement has been the bottleneck since at least **2026-08-15**, when Evan reported "still waiting on the code-signing certificate to come through procurement. No firm timeline yet" (SRC-MEET-08).
- The **most recent gate review before the 2026-09-22 date, on 2026-09-15**, confirms the status had not changed: Alice's gate check lists Windows signing as still open, and Evan notes it stacks with the other holds — "Release isn't opening with any of those unresolved" (SRC-MEET-10). No source in the dataset records the certificate arriving between 2026-09-15 and 2026-09-22.

### What still has to happen

1. **Procure a code-signing certificate** — the sole open blocker per the audit; owned on the procurement side by Alice, with Evan chasing.
2. **Wire signing into the release build step** so the Windows build pipeline emits a signed artifact.
3. **Re-verify the signed build passes Windows Defender/SmartScreen without warnings**, satisfying CIPH-39's remaining acceptance criteria.

Only then does T029 clear. Note also that clearing T029 alone does not open the release: the T011 release checklist (CIPH-21, still Active) is under a security-gate hold from Diana pending **both** T029's Windows signing **and** T005's Docker image slim-down/CVE work, which as of 2026-08-12 was still over the ~450MB target with CVE verification failing (SRC-SLACK-06). The 2026-09-15 pre-release audit adds two further open items on the board: the audit-log gate (CLI-emitted records don't match the defined schema, kept red by Diana) and the upstream high-DPI rendering bug (SRC-MEET-10, SRC-SLACK-58).

### Sources cited

- `med-synth/tasks/CIPH-39-Windows-Compatibility.md` (SRC-CU-CIPH-39)
- `med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md` (SRC-GDOC-39)
- `med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md` (SRC-SLACK-38)
- `med-synth/communication/sources/slack/2026-08-10-windows-path-handling.md` (SRC-SLACK-36)
- `med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md` (SRC-SLACK-37)
- `med-synth/communication/sources/fireflies/2026-08-15-Windows-License-Sync.md` (SRC-MEET-08)
- `med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md` (SRC-MEET-10)
- `med-synth/tasks/CIPH-21-Release-v1-Gates.md` (SRC-CU-CIPH-21)
- `med-synth/communication/sources/slack/2026-06-25-docker-size.md` (SRC-SLACK-06)
- `med-synth/communication/sources/slack/2026-09-10-high-dpi-upstream-block.md` (SRC-SLACK-58)
