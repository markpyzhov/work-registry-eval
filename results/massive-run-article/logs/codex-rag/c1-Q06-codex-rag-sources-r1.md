# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, there is no stated ordering among the blockers: all of these must be green before opening/closing the v1.0.0 release.

| Gate | Listed task assignee | Immediate next-action owner |
|---|---|---|
| T005 — Docker image size/CVE | Evan | Evan — remove remaining Python-package bloat and resolve the failing CVE scan; Diana then re-verifies. |
| T029 — Windows Defender/SmartScreen code signing | Evan | Evan — procure the signing certificate and wire signing into the release build. |
| Audit-trail schema validation | Diana | **Bob** — correct the CLI-emitted audit-record shape; Diana owns the subsequent verification/clearance. |
| High-DPI PDF coordinate scaling | Charlie | **No internal owner is named for the immediate fix**: it is blocked on the upstream rendering library, unless an accepted local remediation is chosen. |

The formal release tracker explicitly requires T005 and T029; the pre-release audit additionally keeps the audit-log mismatch and upstream high-DPI defect on the release-blocker board. The original T001–T006/T010 set is otherwise complete. [SRC-CU-CIPH-21] [SRC-CU-CIPH-15] [SRC-CU-CIPH-39] [SRC-CU-CIPH-26] [SRC-CU-CIPH-46] [SRC-MEET-10]

I would not add the high-latency node-sync handshake to this closure set: the evidence labels it a blocker for **multi-site rollout**, not for the T011/v1.0 release checklist. [SRC-CU-CIPH-34]
