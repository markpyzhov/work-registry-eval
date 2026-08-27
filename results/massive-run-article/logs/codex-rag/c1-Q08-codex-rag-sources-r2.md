# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No—the **Windows (T029) release gate is not cleared** as of September 22.

- **Engineering completion:** Windows packaging works; the artifact installs and passes the Linux-equivalent sanity checks. [SRC-SLACK-38]
- **Remaining Windows release hold:** the artifact is unsigned because no code-signing certificate has been procured/configured. Defender and SmartScreen flag it, and enterprise policies may block installation. [SRC-GDOC-39; SRC-CU-CIPH-39]
- **Still required:** procure the certificate, integrate signing into the release build, then verify the signed binary passes Defender/SmartScreen without warnings. Only then can T029 clear. [SRC-GDOC-39; SRC-CU-CIPH-39]

Separately, the overall release checklist also remains held on the Docker image-size/CVE gate (T005), even after Windows signing clears. [SRC-CU-CIPH-21]
