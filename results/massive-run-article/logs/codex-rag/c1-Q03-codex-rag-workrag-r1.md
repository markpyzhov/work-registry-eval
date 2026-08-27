# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No. As of 2026-09-22, large-file chunking is **reopened and active**; T031/CIPH-41 remains unchecked. The broader work-state is in progress, owned by Charlie/Bob. `(WS-05, SRC-CU-CIPH-41)`

Timeline:

- **Aug 14:** Charlie implemented stream-and-split processing for large PDFs.
- **Aug 16:** the stream-chunking implementation merged to mainline and was called done.
- **Aug 18:** Bob reopened it after long batch runs on files **over 2 GB** continued to leak memory; Diana reproduced the steadily climbing memory and eventual process kill in QA.
- **Aug 20 onward:** Charlie began the buffer-release refactor; by Sep 22 it was still the outstanding engineering work. `(SRC-SLACK-44, SRC-SLACK-43, WS-05)`

Technical root cause: chunk buffers were not explicitly released after a worker finished a chunk—references kept them reachable—so memory grew roughly linearly with file size rather than staying bounded by the chunk size. This is distinct from the PDF loader page-cache leak Bob later fixed. `(SRC-GDOC-42, SRC-GDOC-44)`

Next engineering action and owner: **Charlie** must complete the stream-handler refactor to eagerly release each chunk buffer after processing, then validate it end-to-end against the full large-file corpus (including 2 GB+ stress cases). Bob is the joint workstream owner and originally found the regression, but CIPH-41’s assigned engineering action is Charlie’s. `(SRC-CU-CIPH-41, SRC-GDOC-42)`
