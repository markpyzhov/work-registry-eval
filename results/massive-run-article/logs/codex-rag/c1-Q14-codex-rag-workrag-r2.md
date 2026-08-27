# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

If Docker packaging (T005) and Windows signing (T029) are still red, v1.0.0 has a **hard no-ship cutoff after 2026-10-15**—not an advisory date. [WS-03/T011; CMT-2026-09-002]

This does not lift or weaken the earlier security-gate hold. The hold remains: T011 cannot close until Docker size/CVE verification and Windows code signing are green. The new decision adds an absolute calendar constraint: unresolved gates by that date mean the release cannot ship afterward. [WS-03, updated 2026-09-22; CMT-2026-09-002]
