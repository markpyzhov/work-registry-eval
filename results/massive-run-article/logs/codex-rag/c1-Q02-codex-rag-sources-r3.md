# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of **2026-09-22**, Docker Packaging (T005/CIPH-15) is authoritatively **Active (Reopened)**—a release blocker, not release-ready. The 2026-09-15 pre-release audit confirms the Docker slim-down/CVE gate remains open. [SRC-CU-CIPH-15; SRC-MEET-10]

It supersedes the **2026-06-16 claim that the initial Dockerfile was complete** and packaged both API and CLI. That was only a first milestone; its own release note said size and CVE checks had not yet run. [SRC-GDOC-06]

The concrete blockers are:

- **Size:** the image measured **2.1 GB** when reviewed, versus a target of approximately **450 MB**; subsequent verification still found it above target.
- **Security:** the **CVE verification is still failing/outstanding**; release acceptance requires a clean pass with no outstanding findings.

The task remains reopened until both conditions are met. [SRC-SLACK-06; SRC-CU-CIPH-15]
