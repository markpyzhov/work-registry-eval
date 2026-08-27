# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, formal T011 checklist closure needs **T005** and **T029** green; the board’s 2026-10-15 no-ship rule is explicitly tied to those two. [WS-03](c1/work-states/WS-03-ops.md) [T011](c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md)

- **T005 / CIPH-15—Docker size + CVEs:** assignee and immediate action owner are both **Evan**. Reduce the image to the ~450MB GA target (800MB only interim RC if CVE-clean) and obtain a clean CVE verification. [T005](c1/med-synth/tasks/CIPH-15-Docker-Packaging.md) [WS-03](c1/work-states/WS-03-ops.md)
- **T029 / CIPH-39—Windows signing:** task assignee **Evan**; immediate owner for the blocking action is **Alice**, who is chasing Authenticode-certificate procurement. Evan then signs and validates that Defender/SmartScreen no longer warns. [WS-06](c1/work-states/WS-06-platforms.md) [signing thread](c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md)

A separate material release hold is **T016 / CIPH-26**: assignee **Diana**, but **Bob** owns the queued CLI record/schema correction; Diana owns verification and keeps the gate red until they match. It is flagged as a release blocker, though not listed as a formal T011 closure dependency. [WS-04](c1/work-states/WS-04-policy.md) [pre-release audit](c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md)
