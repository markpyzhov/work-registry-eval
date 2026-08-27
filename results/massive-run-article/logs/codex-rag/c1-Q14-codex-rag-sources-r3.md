# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

No new hard calendar deadline is evidenced. If Docker/CVE or Windows signing stay red, v1.0.0 remains blocked until both clear—there is no documented “ship anyway by date” exception.

So the earlier security-gate hold is unchanged, not superseded: both T005 and T029 remain mandatory release gates. [SRC-CU-CIPH-21] The pre-release audit also explicitly says release does not open with unresolved Docker or Windows holds. [SRC-MEET-10]
