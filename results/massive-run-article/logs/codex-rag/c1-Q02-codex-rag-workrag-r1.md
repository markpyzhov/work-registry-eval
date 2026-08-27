# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of 2026-09-22, Docker packaging (T005 / CIPH-15) is authoritatively **in progress—reopened/active**, not complete. It remains under the release security-gate hold. *(WS-03, 2026-09-22)*

It supersedes the earlier claim that CIPH-15 was completed at approximately **800 MB** (and the 2026-06-16 “initial Dockerfile complete” milestone). The task was reopened on 2026-06-25 after OCR bundling produced a **2.1 GB** image. *(WS-03: Decisions and Superseded Directions; SRC-GDOC-06; SRC-SLACK-06)*

It is not release-ready because:

- **Size:** it remains above the GA target of approximately **450 MB**. An **800 MB** image is only an interim RC threshold—and only if CVE-clean. *(WS-03: Active Work)*
- **CVE verification:** the 2026-08-12 scan still **failed**; the acceptance criterion is a passing verification with **no outstanding findings**. *(SRC-SLACK-06; SRC-CU-CIPH-15)*

The separate CORS finding was patched and later re-verified, but that does not clear the Docker image’s outstanding CVE gate. *(WS-03: Done/Evidence; SRC-SLACK-09)*
