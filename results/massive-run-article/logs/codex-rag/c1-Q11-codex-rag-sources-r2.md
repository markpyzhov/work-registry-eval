# On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

<!-- RESPONSE_START -->

The security-gate hold clears only after both gates below are cleared:

| Critical-path action | Action owner |
|---|---|
| Finish Docker remediation: remove remaining Python-package bloat, identify/fix the CVE-scan trigger, reach the ~450MB target, then obtain a clean CVE result. | **Evan** owns the remediation; **Diana** owns the size/CVE verification that keeps T005 open until both pass. 【SRC-SLACK-06】【SRC-CU-CIPH-15】 |
| Obtain the missing Windows code-signing certificate. | **Alice** owns chasing the certificate process—despite T029/CIPH-39 being assigned to Evan. 【SRC-SLACK-37】 |
| Configure the certificate in the release build, produce the signed build, and confirm it no longer triggers Defender/SmartScreen. | **Evan** owns the signing/build-pipeline work. 【SRC-GDOC-39】【SRC-CU-CIPH-39】 |
| Lift the release security-gate hold once T005 and T029 are demonstrably clear. | **Diana** is the gate holder; the release-gates record says her hold remains pending both items. 【SRC-CU-CIPH-21】 |

The audit-log schema/emitted-record mismatch is also still a release blocker, with **Bob** owning the queued correction and **Diana** retaining the audit gate; however, it is not one of the two explicit prerequisites for the stated *security-gate hold*. 【SRC-MEET-10】
