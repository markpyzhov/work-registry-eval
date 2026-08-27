# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

As of 2026-09-22, if both Docker T005 and Windows signing T029 remain red, the release board’s hard constraint applies: **no ship after 2026-10-15**. It is not advisory. [WS-03](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:34>) [September comments](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md:12>)

This does not replace or clear the earlier security-gate hold; it gives that hold a deadline-backed release consequence. T011 remains active and cannot close until Docker size/CVE and the Windows Authenticode/SmartScreen gate are green; the September 15 audit also keeps the audit-log schema mismatch visible as an unresolved release blocker. [WS-03](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:31>) [CIPH-21](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:12>) [Pre-release audit](</Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:8>)
