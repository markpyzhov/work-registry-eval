# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

No hard calendar date is documented. If Docker/CVE (T005) and Windows signing (T029) remain red, v1.0.0 simply cannot ship; the constraint is an unresolved-gates hold, not a deadline or scheduled exception. `SRC-CU-CIPH-21`

This does not relax the earlier security-gate hold. It remains in force pending both items (with the audit-log mismatch also still a release blocker in the pre-release review). `SRC-MEET-10`
