# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No—the **Windows release gate is not cleared** as of 2026-09-22.

- **Engineering completion:** Windows path fixes, packaging, and the binary itself are complete. The artifact installed on Windows and passed the Linux-equivalent sanity checks. [SRC-SLACK-38]
- **Remaining Windows release hold:** the build is unsigned. A valid code-signing certificate must be procured, signing added to the release-build pipeline, and the signed artifact must pass Defender/SmartScreen without warnings. Until then, installations may be warned or blocked, so T029 remains open. [SRC-GDOC-39] [SRC-CU-CIPH-39]
- **Overall release:** even after Windows signing clears, the release checklist remains held on the separate T005 Docker image slim-down/CVE gate. [SRC-CU-CIPH-21]
