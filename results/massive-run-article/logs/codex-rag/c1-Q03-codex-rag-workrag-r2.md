# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No. As of **2026-09-22**, large-file chunking (**T031 / CIPH-41**) is **reopened and active**, not complete; the Work State keeps T031 unchecked. The overall owner is Charlie/Bob, with **Charlie owning the next engineering action**: refactor the stream handler to release each chunk buffer after processing. (WS-05; SRC-CU-CIPH-41; SRC-SLACK-43)

Timeline:

- **Aug 14–16:** Stream-and-split chunking was implemented and merged to mainline. It reads PDFs in 100-page blocks, processes temporary sub-documents, then re-merges the output. Charlie called it done on Aug 16, while noting longer runs could still surface issues. (SRC-GDOC-25; SRC-SLACK-44)
- **Aug 18:** Bob reopened it after long batches of **>2 GB** files continued to leak memory; Diana reproduced steadily rising memory and eventual process termination in QA. (SRC-SLACK-43)
- **Aug 20–23:** The cause was identified and the buffer-release refactor began. A 2.3 GB local test looked flat, but the fix had not passed the full large-file corpus end-to-end. (SRC-SLACK-44; SRC-GDOC-42)
- **Sep 22:** Authoritative state remains **Reopened/active**; a 4.7 GB PDF on an 8 GB clinic workstation is a pilot blocker. (WS-05)

Technical root cause: chunking avoided loading the entire PDF at once, but completed chunks’ buffers were retained—rather than explicitly released—so memory grew roughly linearly with file size. The intended fix is **eager per-chunk buffer release**, followed by full-corpus stress validation. (SRC-GDOC-42; SRC-CU-CIPH-41)
