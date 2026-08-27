# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

No new hard calendar constraint is supported by the assigned sources. The release remains blocked until Docker size/CVE (T005) and Windows signing (T029) clear.

So the earlier security-gate hold is unchanged—not overridden or converted into a date-driven exception. The gate task is still Active with both conditions unresolved. [SRC-CU-CIPH-21] The last pre-release audit likewise states release does not open while those holds remain. [SRC-MEET-10]
