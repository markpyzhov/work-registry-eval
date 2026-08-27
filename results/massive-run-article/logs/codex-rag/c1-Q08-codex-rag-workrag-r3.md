# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No—the Windows release gate was **not cleared** as of 2026-09-22.

- **Engineering completion:** Windows packaging works; the binary runs on Windows and passes the Linux-equivalent sanity checks. The path-handling fix and build artifact are complete. [SRC-SLACK-38; WS-06]
- **Release hold:** The artifact is unsigned, so Defender/SmartScreen treats it as untrusted and may block pilot installs. This is a procurement dependency, not an engineering defect. [SRC-SLACK-37; WS-06]
- **Still required:** procure a valid code-signing certificate, integrate signing into the release build, sign the binary, and confirm it passes Defender/SmartScreen without warnings. [SRC-CU-CIPH-39; SRC-GDOC-39]

Separately, the overall v1 release gate also remains held on Docker image/CVE work (and the release work state lists audit-log schema alignment as open), so clearing Windows signing alone would not open the full release. [WS-03; SRC-CU-CIPH-21]
