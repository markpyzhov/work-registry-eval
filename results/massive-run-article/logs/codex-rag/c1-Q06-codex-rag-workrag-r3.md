# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, the formal gates that must turn green before **T011 / CIPH-21 (Release v1.0.0 Gates)** can close are:

- **T005 / CIPH-15 — Docker image size + CVE gate:** task assignee **Evan**; immediate action also **Evan**—finish slimming the image and resolve/re-run the CVE verification. The RC threshold is 800MB when CVE-clean; GA remains ~450MB. *(WS-03; SRC-CU-CIPH-15; SRC-SLACK-06)*

- **T029 / CIPH-39 — Windows code-signing gate:** task assignee **Evan**; immediate next action is **Alice**, who committed to chase the code-signing-certificate process. Once procured, Evan can wire signing into the build and validate SmartScreen/Defender clearance. *(WS-03; WS-06; SRC-CU-CIPH-39; SRC-SLACK-37)*

There is also a material **release hold**:

- **T016 / CIPH-26 — audit-log schema alignment:** task assignee **Diana**; the immediate corrective action is **Bob** (another CLI audit-log integration pass to make emitted records match the schema), after which **Diana** owns verification/clearing the gate. *(WS-04; SRC-CU-CIPH-26; SRC-MEET-10)*

T010/CIPH-20 security scans are already complete, so they are not an outstanding gate. The release board’s hard no-ship condition is **2026-10-15** if T005 and T029 are still red. *(WS-03; CMT-2026-09-002)*
