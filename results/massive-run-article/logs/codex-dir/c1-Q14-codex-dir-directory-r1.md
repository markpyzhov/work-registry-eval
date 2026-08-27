# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

If Docker packaging (T005) and Windows signing (T029) remain red, **v1.0.0 must not ship after 2026-10-15**—a hard, non-advisory release-board cutoff. [WS-03-ops.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:34)

This does **not** relax or replace the earlier security-gate hold. The hold remains: T011 cannot close or ship until both Docker size/CVE verification and Windows code-signing are green. The calendar rule adds an absolute deadline to that existing gate; if they are still unresolved on October 15, shipping is prohibited. [WS-03-ops.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:31) [CIPH-21-Release-v1-Gates.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:16)
