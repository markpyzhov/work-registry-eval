# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

T011 cannot close until both formal dependency gates are green—there is no supported sequence between them:

| Gate | Listed task assignee | Immediate next-action owner |
|---|---|---|
| **T005 / CIPH-15 — Docker size and CVE** | Evan | **Evan**: remove remaining Python-package bloat and investigate the failing CVE scan; Diana then verifies both checks. No ownership mismatch. |
| **T029 / CIPH-39 — Windows code signing** | Evan | **Alice** owns the immediate unblock: chase/procure the signing certificate. Evan owns the subsequent technical work of wiring signing into the release build. **Mismatch: Evan → Alice for the next action.** |

The prerequisite set T001–T006 and T010 is already satisfied; the authoritative September 22 work state says T011 cannot close until T005 and T029 are green, with a hard no-ship date of 2026-10-15 if they are not. [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:31) [CIPH-21](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:12)

Also treat **T016 / CIPH-26 audit-log schema alignment** as a material release hold, although it is not stated as a formal T011 dependency gate: its listed assignee is **Diana**, while **Bob** owns the immediate remediation pass to make CLI-emitted records match the schema; Diana retains verification/gate-clearance ownership. [CIPH-26](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md:11) [Pre-release audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:13)

For T029 specifically, Alice’s certificate-procurement action is explicit; the certificate is the sole blocker before Evan can wire signing into the build. [Windows signing thread](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-09-02-windows-signing-gap.md:22) [Windows audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-09-02-Windows-Compatibility-Audit-Report.md:16)
