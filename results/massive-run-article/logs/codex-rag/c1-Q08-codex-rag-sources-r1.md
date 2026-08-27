# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No—the Windows release gate was **not cleared** as of 2026-09-22.

- **Engineering completion:** Windows path handling and packaging were fixed; the artifact was produced, installed on Windows, and passed the Linux-equivalent sanity checks. The build itself is sound. *(SRC-SLACK-38; SRC-GDOC-39)*

- **Remaining Windows release hold (T029):** The artifact is unsigned because no code-signing certificate has been procured/configured. Defender and SmartScreen therefore flag it as untrusted and may block pilot/customer installation. *(SRC-GDOC-39; SRC-CU-CIPH-39; SRC-SLACK-37)*

Still required: procure a valid code-signing certificate, integrate signing into the release build, produce a signed build, and verify it passes Defender/SmartScreen without warnings. Only then can T029 clear. The overall v1.0 release checklist also remains held by the separate T005 Docker image size/CVE gate. *(SRC-GDOC-39; SRC-CU-CIPH-21)*
