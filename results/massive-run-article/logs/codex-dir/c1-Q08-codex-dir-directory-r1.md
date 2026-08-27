# Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

<!-- RESPONSE_START -->

No—the Windows release gate (`T029`) is not cleared as of 2026-09-22.

Engineering completion: the path fix enabled packaging; a Windows artifact was produced, installed on Windows, and passed the Linux-equivalent sanity checks. Packaging/build engineering is complete. [Build-artifact evidence](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-windows-build-artifact.md) [WS-06](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md)

Remaining release hold: the artifact is unsigned because no Authenticode code-signing certificate has been procured/configured. Defender and SmartScreen flag it, potentially blocking installation under site IT policy. The release must procure the certificate, integrate signing into the release build, sign the artifact, and verify Defender/SmartScreen pass without warnings. [Windows audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md) [CIPH-39 acceptance criteria](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md)

Separately, clearing Windows alone would not clear the v1 release: `T005` Docker image size/CVE work also remains open. The authoritative release state keeps `T011` under a security-gate hold until both `T005` and `T029` are green, with a hard no-ship deadline of 2026-10-15. [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md) [release-gate task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md)
