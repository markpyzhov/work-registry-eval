# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of 2026-09-22, Docker packaging (T005/CIPH-15) is **in progress / Active (Reopened)**, not finished. It is a P0 release dependency, and v1.0 release gates remain under a security hold until its size and CVE checks are green. [WS-03 Work State, record `f0b9411efcd33230`]

This supersedes the **2026-06-16 “initial Dockerfile complete”** claim—the working API-and-CLI image was only a first milestone, with size review and CVE checking still pending. [SRC-GDOC-06, record `16a7009f06b883c3`]

What prevents release readiness:

- The image measured **2.1 GB** when reviewed, prompting reopening. The GA target is **~450 MB**; an interim RC may be up to **800 MB only if CVE-clean**. [SRC-SLACK-06, record `8ff122c766f3ade8`; CMT-2026-06-002, record `ee4651f6de85c0fa`]
- After multi-stage, Alpine, and package-removal work, the **2026-08-12 verification still exceeded ~450 MB**. The dataset does not provide a newer exact image size. [SRC-CU-CIPH-15, record `461c66a96e55b847`]
- That same verification found **CVE verification still failing/outstanding**. The task cannot close—and the image cannot be called release-ready—until both the size target and a clean CVE check pass. [SRC-CU-CIPH-15, record `461c66a96e55b847`]
