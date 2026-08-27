# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No. As of **2026-09-22**, T031/CIPH-41 is **reopened and active**—not complete. The work state remains `in_progress`, and the task is unchecked. `(WS-05; SRC-CU-CIPH-41; SRC-SLACK-43)`

Timeline:

- **Aug 14–16:** Stream-and-split chunking was implemented and merged to mainline; PDFs were processed in fixed-size chunks rather than loaded wholesale. Charlie called it done on Aug 16. `(SRC-GDOC-25; SRC-SLACK-44)`
- **Aug 18:** Bob reopened it after long batches of **>2 GB** files still showed steadily rising memory; Diana reproduced the failure, including eventual process termination. `(SRC-SLACK-43)`
- **Aug 20:** Root cause was identified: processed chunk buffers were not explicitly released, so references persisted and memory accumulated. Charlie began an eager, per-chunk buffer-release refactor. `(SRC-SLACK-44; SRC-CU-CIPH-41)`
- **Aug 23:** A 2.3 GB local test looked flat after the refactor, but it had **not** been validated across the full large-file corpus. `(SRC-GDOC-42)`

Technical root cause: chunking limited the input slice size, but completed chunks’ buffers were retained rather than released. Consequently peak memory grew roughly linearly with file size instead of remaining bounded by the chunk size. This is distinct from the PDF loader page-object-cache leak, which Bob separately fixed and verified under CIPH-43. `(SRC-GDOC-42; SRC-GDOC-44)`

**Next engineering action and owner:** **Charlie** owns CIPH-41 and must complete the stream-buffer release refactor, then validate it end-to-end on the large-file/stress corpus. Bob is the co-owner at the work-stream level and discovered the regression, but Charlie owns this specific fix. `(WS-05; SRC-CU-CIPH-41)`
