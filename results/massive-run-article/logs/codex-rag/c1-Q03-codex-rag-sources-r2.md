# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No. As of 2026-09-22, large-file chunking remains **Active (Reopened)** under **Charlie**; the original “done” did not hold. [SRC-CU-CIPH-41]

Timeline:

- **Aug 16:** Charlie merged stream chunking to mainline and called it done. [SRC-SLACK-44]
- **Aug 18:** Bob reopened it after long-running batches with files **over 2 GB** still leaked memory; QA reproduced steady memory growth ending in process kills. [SRC-SLACK-43]
- **Aug 20–23:** Charlie identified/refactored the buffer-release path. A 2.3-GB local run was flat, but the fix was still unverified across the full large-file corpus. [SRC-SLACK-44] [SRC-GDOC-42]

Technical root cause: chunk buffers remained reachable after a worker had finished a chunk—they were not explicitly released, so peak memory grew roughly linearly with input size rather than remaining chunk-bounded. [SRC-GDOC-42] A related but distinct PDF-loader page-object-cache retention was patched and verified by Bob; that did not close the outstanding chunk-buffer task. [SRC-GDOC-44]

Next engineering action: **Charlie** must finish the eager per-chunk buffer release and run the full large-file/stress corpus, demonstrating no leak for files ≥2 GB before closing CIPH-41. Diana is positioned to rerun the QA stress case once a build is available. [SRC-CU-CIPH-41] [SRC-GDOC-42] [SRC-SLACK-44]
