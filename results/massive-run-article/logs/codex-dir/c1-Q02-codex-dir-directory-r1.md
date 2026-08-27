# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of 2026-09-22, Docker packaging (T005/CIPH-15) is **reopened and active**, not finished; it remains a release-security gate. The release cannot clear until its size/CVE gate is green. [WS-03-ops.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:28)

This supersedes the earlier claim that CIPH-15 was **initially completed at approximately 800MB**. The authoritative work state says that claim was superseded when bundled OCR dependencies expanded the image to **2.1GB**, prompting the June 25 reopen; it explicitly identifies the Slack evidence as superseding the original Docker release note. [WS-03-ops.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:37) The older note itself only documented an initial Dockerfile milestone and said its size review and CVE check had not yet run. [2026-06-16-Docker-Release-Notes.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md:9)

The concrete blockers are:

- **Size:** after multi-stage and Alpine remediation, the August 12 verification still found the image **over the ~450MB GA target**; remaining bloat was identified in the Python `site-packages` layer. [2026-06-25-docker-size.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md:22) An interim RC could only ship at **800MB if CVE-clean**; GA remains ~450MB. [2026-06.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-06.md:13)
- **CVEs:** the August 12 scan was still **failing**, with the specific trigger not yet resolved; acceptance requires a clean CVE verification with no outstanding findings. [2026-06-25-docker-size.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md:22) [CIPH-15-Docker-Packaging.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md:14)

Thus, the evidence supports no newer exact post-remediation size or CVE list—only that it remains above 450MB and CVE-failing—so the image cannot be called release-ready.
