# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, T011’s formal acceptance criteria require **T005** and **T029** to clear. The pre-release audit also keeps the **audit-log** and **high-DPI** blockers on the release board; release cannot open while any remains unresolved. [SRC-CU-CIPH-21] [SRC-MEET-10]

| Gate | Listed task assignee | Immediate next action owner |
|---|---|---|
| **T005 — Docker image size/CVE** | Evan | **Evan** — remove remaining Python-package bloat and resolve the failing CVE scan; then Diana can re-verify size and CVEs. [SRC-CU-CIPH-15] [SRC-SLACK-06] |
| **T029 — Windows signing / Defender-SmartScreen** | Evan | **Alice** — chase/procure the code-signing certificate. Evan then wires signing into the release build and validates it. [SRC-CU-CIPH-39] [SRC-SLACK-37] |
| **Audit-log schema validation** | Diana | **Bob** — make the CLI-emitted records conform to the defined schema; Diana keeps the gate red until verification passes. [SRC-CU-CIPH-26] [SRC-MEET-10] |
| **T036 / CIPH-46 — high-DPI coordinate scaling** | Charlie | **Alice** — decide whether to accept the limitation or move to a different rendering library; Charlie has already filed upstream, with no safe local fix identified. [SRC-CU-CIPH-46] [SRC-SLACK-58] |

The high-latency node-sync handshake is blocked as of 9/22, but the evidence calls it a prerequisite for **multi-site rollout**, not a T011 release-checklist gate. [SRC-CU-CIPH-34]
