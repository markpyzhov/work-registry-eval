# For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

<!-- RESPONSE_START -->

As of 2026-09-22, **T011 / CIPH-21 (v1.0.0 release checklist)** cannot close until these two gates are green:

- **T005 / CIPH-15 — Docker image size and CVE gate:** reduce the image to the GA target (~450 MB) and clear CVE verification. The listed task assignee is **Evan**, and the immediate remediation/verification action is also **Evan’s**—so there is no ownership split. *(WS-03; SRC-CU-CIPH-15; SRC-SLACK-06)*

- **T029 / CIPH-39 — Windows code-signing gate:** procure an Authenticode certificate, sign the build, and clear Defender/SmartScreen. The listed task assignee is **Evan**, but **Alice owns the immediate next action**: chasing the certificate procurement process. After procurement, Evan must wire signing into the release build and validate the signed artifact. *(WS-03; WS-06; SRC-CU-CIPH-39; SRC-SLACK-37; SRC-GDOC-39)*

The release board set a hard **no-ship after 2026-10-15** if T005 and T029 are not green. *(WS-03; CMT-2026-09-002)*
