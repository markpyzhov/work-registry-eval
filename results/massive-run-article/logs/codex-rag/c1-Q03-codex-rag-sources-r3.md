# Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

<!-- RESPONSE_START -->

No. As of 2026-09-22, large-file chunking is still **Active (Reopened)**, assigned to **Charlie**—the merge held, but the completion claim did not. (SRC-CU-CIPH-41)

- **Aug 12:** CIPH-41 opened for multi-GB streaming.  
- **Aug 16:** Charlie merged stream chunking to mainline and called it done. (SRC-SLACK-44)  
- **Aug 18:** Long-running batches over 2 GB still leaked memory; QA reproduced steady growth and eventual process kills, so the work was reopened. (SRC-SLACK-43)  
- **Aug 20–23:** The team identified the open chunking defect and Charlie began the fix. A 2.3 GB local run was flat, but the full large-file corpus had not yet been validated end-to-end. (SRC-SLACK-44; SRC-GDOC-42)

**Root cause:** the stream handler did not explicitly release each chunk buffer after processing. References remained live, so memory grew roughly with total file size rather than staying bounded by the chunk size. (SRC-GDOC-42)

There was also a **separate** PDF-loader page-object-cache leak. Bob patched and verified that loader-side issue on Aug 23, but it was explicitly distinct from CIPH-41’s still-open buffer-release work. (SRC-GDOC-44)

**Next engineering owner:** **Charlie**. He owns completing the eager per-chunk buffer-release refactor and handing off a build for the full ≥2 GB stress/corpus validation; Diana is the QA partner for that rerun. (SRC-CU-CIPH-41; SRC-SLACK-44)
