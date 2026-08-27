# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

If both Docker packaging (T005) and Windows signing (T029) remain red, v1.0.0 has a hard **no-ship cutoff after 2026-10-15**. The release board set that deadline explicitly.  

This does not lift or replace the earlier security-gate hold: T011 remains held until both dependencies are green. The new constraint adds a calendar-based prohibition on top of that gate. *(Work State WS-03, updated 2026-09-22; CMT-2026-09-002; S9–S10.)*
