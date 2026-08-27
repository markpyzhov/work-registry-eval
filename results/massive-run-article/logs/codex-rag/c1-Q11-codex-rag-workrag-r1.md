# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

As of 2026-09-22, the security-gate hold clears only after these actions:

- **Docker/CVE gate (T005): Evan** must finish slimming the image and remediate the failing CVE check. **Diana** then re-runs and confirms the size/CVE verification. The interim RC threshold is 800 MB *and CVE-clean*; GA remains ~450 MB. *(WS-03 `f0b9411efcd33230`; `SRC-SLACK-06` `8ff122c766f3ade8`; CMT-2026-06-002 `ee4651f6de85c0fa`)*

- **Windows signing gate (T029): Alice** owns chasing/procuring the missing code-signing certificate—despite the release-gates task being assigned to Evan. **Evan** then wires signing into the release build pipeline. *(SRC-SLACK-37 `4eeefef9fc806102`; `SRC-GDOC-39` `3a7b937808b6fadd`)*

- **Audit-log schema blocker (T016/CIPH-26): Bob** must make the queued fix so CLI-emitted audit records conform to the defined JSON schema. **Diana** owns verification and will keep the audit gate red until they match. *(WS-04 `917ecd0b3736fd18`; `SRC-MEET-10` `c466edd67f6ef08b`; CIPH-26 `27857d38103c6293`)*

- **Gate clearance:** once the above are green, **Diana** can remove the security/audit hold; **Evan** updates and closes the T011 release checklist. The formal no-ship deadline is **2026-10-15** if T005 or T029 is still not green. *(CIPH-21 `9446122a438f23cb`; CMT-2026-09-002 `107620722594e9cc`)*
