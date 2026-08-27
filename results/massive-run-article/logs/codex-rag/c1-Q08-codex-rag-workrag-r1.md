# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No. As of 2026-09-22, the Windows gate (T029/CIPH-39) is still active and the release remains held. *(WS-06, 2026-09-22; SRC-CU-CIPH-39)*

- Engineering is complete: Windows path handling was fixed; the artifact builds, installs, runs, and passes the Linux-equivalent sanity checks. *(SRC-SLACK-38; SRC-GDOC-39)*
- The remaining hold is release/procurement: obtain a valid Authenticode code-signing certificate, configure it in the Windows release pipeline, sign the build, then verify it passes Defender/SmartScreen without warnings. Unsigned binaries are still flagged or blocked. *(SRC-CU-CIPH-39; SRC-GDOC-39; SRC-SLACK-37)*

Separately, clearing Windows signing alone would not open the overall v1 release: Docker image slim-down/CVE work and the audit-log schema-versus-output mismatch are also open release blockers. *(WS-03, 2026-09-22; SRC-MEET-10)*
