# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of 2026-09-22, Docker Packaging (T005 / CIPH-15) is **Active (Reopened)**—a release blocker, not release-ready. The release gate remains open pending Docker slim-down and CVE clearance. [SRC-CU-CIPH-15], [SRC-MEET-10]

It supersedes the 2026-06-16 claim that the **initial Dockerfile was complete** and packaged both API and CLI. That was only an implementation milestone; its own note required size and CVE review before release readiness. [SRC-GDOC-06]

The unmet release criteria are concrete:

- **Size:** the reviewed image measured **2.1 GB**; despite multi-stage, Alpine, and package-removal work, the latest verification still found it **over the ~450 MB target**. [SRC-CU-CIPH-15], [SRC-SLACK-06]
- **Security:** the CVE scan/verification was still **failing**, with outstanding findings that Evan still needed to investigate. The source set does not provide individual CVE identifiers. [SRC-SLACK-06]

Both conditions must be clean before T005 can close. [SRC-CU-CIPH-15]
