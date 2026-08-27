# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

## Answer

**No — the Windows release gate is not cleared as of 2026-09-22.** A working build artifact exists, but that satisfied only part of the gate. T029 / CIPH-39 is still **Active**, and the release is still **held on code-signing**.

### What is engineering-complete

- Backslash/path-separator defects that broke Windows builds were fixed on 2026-08-10 — the handling was reworked to be OS-aware rather than hardcoded, including the temp-directory assumption (`SRC-SLACK-36`, Windows Path Handling, 2026-08-10).
- A Windows build artifact was produced on 2026-08-12, and it **runs**: Evan installed it on a Windows box and it passed the same sanity checks used on Linux (`SRC-SLACK-38`, Windows Build Artifact).
- Evan stated explicitly at the time: the engineering work for the Windows build is complete — packaging works, the binary is sound — but he "wouldn't call the whole thing closed" because code-signing was a separate item not yet started (`SRC-SLACK-38`). Alice agreed to track signing on its own.
- The fix held: at the 2026-08-15 Windows & License Sync, Evan confirmed the path fix had been holding up in the build with no regressions (`SRC-MEET-08`).
- Packaging is confirmed no longer the blocker (`SRC-GDOC-39`, Compatibility Audit: Windows Build Signing Gap, 2026-09-02).

### What is still holding the gate

- The produced artifact is **unsigned**. Windows Defender and SmartScreen flag it as untrusted; pilot testers hit a warning at best and an outright block at worst (`SRC-SLACK-37`, Windows Signing Gap, 2026-09-02).
- Root cause: **no Authenticode code-signing certificate has been procured or configured** in the Windows build pipeline (`SRC-GDOC-39`).
- Impact: site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override (`SRC-GDOC-39`).
- This is a **procurement dependency, not an engineering block** — WS-06 states this directly, and Evan said on 2026-09-02 that it "isn't something we can work around on the engineering side, we need the certificate." Alice decided to keep it open on the release gate rather than push it off the board, and took the certificate chase herself (`SRC-SLACK-37`, WS-06 Active Work).
- As of the 2026-08-15 sync, procurement had **no firm timeline** for the certificate (`SRC-MEET-08`).
- Still open as of the last checkpoint: the 2026-09-15 pre-release audit re-confirmed Windows signing as an open blocker alongside Docker slim/CVE and the audit-log schema mismatch; Alice closed with "Security-gate work stays open… No one closes those today" (`SRC-MEET-10`).
- WS-06 carries an open triage item: **budget and procurement timeline for the Windows Authenticode code-signing certificate** (WS-06, Needs Manual Triage).

### What still has to happen

Per CIPH-39's acceptance criteria (`SRC-CU-CIPH-39`) and the resolution path in `SRC-GDOC-39`:

1. **Procure an Authenticode code-signing certificate** (Alice is chasing the certificate process; budget/timeline still untriaged). This is the sole open blocker on T029.
2. **Wire signing into the release build step** — configure the certificate in the Windows build pipeline.
3. **Verify the signed build passes Defender/SmartScreen without warnings.** Only then does T029 go green.

### Downstream consequence

T029 is not an isolated item — it gates the release checklist:

- **T011 / CIPH-21 (Release v1.0 Gates)** cannot close until both T005 (Docker size/CVE) and T029 (Windows code-signing) are green (WS-03, Blockers and Dependencies). Diana placed a security-gate hold on the release pending exactly those two (`SRC-CU-CIPH-21`).
- Even if the certificate lands, the release does not open on Windows alone: Docker slim-down/CVE work and the audit-log schema-vs-emitted-records mismatch (T016, Diana keeping that gate red) also remain open (`SRC-MEET-10`).
- The release board set a **hard no-ship after 2026-10-15** if T005 and T029 are not green (`CMT-2026-09-002`, WS-03).

**Bottom line:** engineering delivered a working, verified Windows build; the gate remains closed on a non-engineering dependency — certificate procurement — and clearing it requires the cert in hand, signing wired into the pipeline, and a clean SmartScreen/Defender pass, with a 2026-10-15 no-ship deadline in force.
