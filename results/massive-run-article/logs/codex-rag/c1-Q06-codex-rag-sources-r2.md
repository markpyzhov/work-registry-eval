# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

To close the formal v1.0 release checklist (T011), **two unresolved dependency gates must be green**:

| Gate | Listed task assignee | Immediate next action owner | What must happen |
|---|---|---|---|
| **T005 — Docker image size/CVE** (CIPH-15) | Evan | Evan (then Diana re-verifies) | Get the image to the ~450 MB target and clear CVE verification. |
| **T029 — Windows code-signing / Defender–SmartScreen** (CIPH-39) | Evan | **Alice** | Alice is to chase/procure the signing certificate; Evan then wires signing into the release build and validates it. |

So the material ownership mismatch is **T029: Evan owns the task, but Alice owns the immediate certificate-procurement action**. The original seven-gate checklist had the other six prerequisites already complete; T005 remained open, and the later prerequisite audit added T029 as a second mandatory hold. `SRC-GDOC-05`, `SRC-CU-CIPH-21`, `SRC-CU-CIPH-15`, `SRC-CU-CIPH-39`, `SRC-SLACK-37`

Separately, the pre-release audit still called **high-DPI rendering** and the **audit-log schema mismatch** release blockers. They are not enumerated as T011’s two pending formal dependencies, but the release was not to open with them unresolved: high-DPI is assigned to Charlie while Alice must decide whether to accept the limitation or change rendering approach; audit logging is assigned to Diana while Bob owns the queued CLI-record fix. `SRC-MEET-10`, `SRC-CU-CIPH-46`, `SRC-CU-CIPH-26`
