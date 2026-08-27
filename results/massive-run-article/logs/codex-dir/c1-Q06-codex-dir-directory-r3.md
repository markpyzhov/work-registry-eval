# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

Formal T011 checklist closure requires only two remaining gates:

- **T005 / Docker size + CVE** — assignee **Evan**; immediate action is also **Evan**: remove remaining Python-package bloat and resolve CVE findings, then pass size/CVE verification. [CIPH-21](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:12) [Docker task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md:11)

- **T029 / Windows signing** — assignee **Evan**; immediate action owner is **Alice**, who is chasing procurement of the Authenticode certificate. Evan can wire signing after it arrives. [CIPH-39](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md:11) [signing thread](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md:19)

All original T001–T006 and T010 checklist dependencies are recorded met; T011 cannot close until T005 and T029 are green. [CIPH-21](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:14) [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:33)

Important broader holds: **T016 audit logs** is a release blocker (assignee **Diana**, immediate fix **Bob**, then Diana verifies); the pre-release audit also keeps **T036 high-DPI** open (assignee **Charlie**, blocked on upstream—no different immediate owner named). [audit task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md:29) [pre-release audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:11)
