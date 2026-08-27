# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No. As of 2026-09-22, the Windows release gate remains **open**.

- **Engineering completion:** Windows path handling was fixed; the build artifact was produced, installed on Windows, and passed the Linux-equivalent sanity checks. **CIPH-39’s build/packaging work is complete.** [SRC-SLACK-38; WS-06]
- **Release hold:** The binary is unsigned, so Defender/SmartScreen flags or can block it. This is a **certificate-procurement dependency**, not an engineering defect. [SRC-SLACK-37; SRC-CU-CIPH-39; WS-06]
- **Still required:** procure a valid code-signing certificate, wire signing into the Windows release build, then verify the signed binary passes Defender/SmartScreen without warnings. [SRC-CU-CIPH-39; SRC-GDOC-39]

Separately, the overall v1 release remains on hold for the Docker image-size/CVE gate as well as Windows signing. [WS-03; SRC-CU-CIPH-21]
