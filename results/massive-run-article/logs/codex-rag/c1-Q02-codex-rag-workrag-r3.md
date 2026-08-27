# Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

<!-- RESPONSE_START -->

As of **2026-09-22**, Docker packaging (**T005 / CIPH-15**) is **in progress / Active (Reopened)**, not complete. It remains a release-gate blocker. [WS-03 Work State, `f0b9411efcd33230`; CIPH-15, `461c66a96e55b847`]

It supersedes the **2026-06-16** claim that the initial Dockerfile was complete—a first milestone that packaged the API and CLI, but had not yet undergone size or CVE review. [SRC-GDOC-06, `16a7009f06b883c3`]

The concrete non-release-ready outcomes are:

- The image had ballooned to **2.1 GB**; despite multi-stage, Alpine, and package-removal work, it was still **over the ~450 MB GA target** as of the latest verification. An interim RC can only ship at **800 MB if CVE-clean**. [WS-03 Work State, `f0b9411efcd33230`; CMT-2026-06-002, `ee4651f6de85c0fa`]
- The **CVE verification is still failing/outstanding**. Acceptance requires a clean CVE verification with no outstanding findings; the task stays reopened until both the size and CVE checks pass. [CIPH-15, `461c66a96e55b847`; SRC-SLACK-06, `8ff122c766f3ade8`]

So, the image is neither GA-ready nor eligible for the conditional RC path: it has not met the applicable size gate and is not CVE-clean.
