# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

Shipping v1.0.0 is subject to a **hard no-ship cutoff after 2026-10-15** if Docker packaging/CVE work (**T005**) and Windows signing (**T029**) are still not green. This is a release-board decision, explicitly “not advisory.” [WS-03 / Blockers and Dependencies, CMT-2026-09-002]

It does **not** weaken or replace the earlier security-gate hold. The hold remains: T011 cannot close until both T005 and T029 are green. The new constraint adds a calendar deadline to that existing technical/security gate—if they remain red at the cutoff, v1.0.0 cannot ship afterward. [WS-03 / Active Work and Blockers, last updated 2026-09-22]
