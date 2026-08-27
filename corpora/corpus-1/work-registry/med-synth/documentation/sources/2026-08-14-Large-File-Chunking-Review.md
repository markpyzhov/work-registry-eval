**Source ID**: SRC-GDOC-25

# Design Note: Large File Chunking Strategy
**Owner**: Charlie
**Document Key**: DOC-2025
**Last Updated**: 2026-08-14

## The Failure Mode
When processing massive multi-GB PDF documents (e.g., a 4,000-page merged archive), the loader attempts to load the entire document tree into RAM. For files exceeding 2GB, this consistently results in an `OOMKilled` exception in our standard 4GB Docker containers.

## Chunking Implementation
We implemented and merged a "Stream-and-Split" pre-processing layer today. 
1. The CLI reads the source PDF in 100-page blocks.
2. Each block is saved as a temporary sub-document (`doc_part_1.pdf`, `doc_part_2.pdf`).
3. The worker pool processes these sub-documents independently.
4. A post-processing step merges the redacted sub-documents back into a single final PDF.

## Ordering and Memory Trade-off
This approach solves the RAM issue but introduces a significant disk I/O and ordering overhead. Re-merging the PDFs requires careful tracking of the chunk sequence. Furthermore, if a regex pattern was supposed to match across a page boundary (e.g., a sentence split across pages 100 and 101), the chunking will break the match. We are trading context-awareness for memory stability.

*Pending*: We need to run a stress test with a 10,000-page document to verify if the final re-merge step (which also uses RAM) re-introduces the OOM crash.
