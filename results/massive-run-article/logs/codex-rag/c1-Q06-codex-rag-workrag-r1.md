# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, **T011 / CIPH-21 (Release v1.0 Gates) cannot close until two gates are green**; the original dependencies other than these are already satisfied.

| Gate | What must be green | Listed task assignee | Immediate next-action owner |
|---|---|---|---|
| **T005 / CIPH-15 — Docker packaging** | Docker image must meet the applicable size gate and pass CVE verification; for GA the target remains ~450 MB. | **Evan** | **Evan** — remove remaining Python-package bloat and resolve the CVE-scan failure, then re-verify. |
| **T029 / CIPH-39 — Windows signing** | Obtain a code-signing certificate, wire it into the release build, and clear Defender/SmartScreen. | **Evan** | **Alice** — she explicitly took the immediate action to chase the certificate process; Evan owns the task/build work once it is available. |

So the ownership split is material only for **T029**: Evan is the assigned task owner, while Alice owns the immediate procurement action. The release board’s hard no-ship date is **2026-10-15** if either gate remains red. *(WS-03; SRC-CU-CIPH-15; SRC-SLACK-06; SRC-CU-CIPH-39; SRC-GDOC-39; SRC-SLACK-37; CMT-2026-09-002)*
