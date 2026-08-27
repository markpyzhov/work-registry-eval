# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of 2026-09-22, T005/CIPH-15 is **Active (Reopened)** and remains a release/security-gate blocker. It supersedes the earlier claim that Docker packaging was complete—initially described as an initial Dockerfile milestone, and recorded as completed at roughly 800MB—after OCR bundling produced a 2.1GB image. [Work state](c1/work-states/WS-03-ops.md), [initial claim](c1/med-synth/documentation/sources/2026-06-16-Docker-Release-Notes.md)

Release readiness is still prevented because the rebuilt Alpine/multi-stage image remains **over the ~450MB GA target** and its **CVE scan is failing/outstanding**. The separate interim RC threshold is 800MB, but only if CVE-clean; neither condition justifies closing the task. [CIPH-15](c1/med-synth/tasks/CIPH-15-Docker-Packaging.md), [size/CVE verification](c1/med-synth/communication/sources/slack/2026-06-25-docker-size.md)
