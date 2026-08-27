**Source ID**: SRC-GDOC-42

# Design Review: Large-File Chunking — Post-Merge Reopen
**Owner**: Charlie
**Document Key**: DOC-2042
**Last Updated**: 2026-08-23

## Implemented Approach: Stream Chunking
To keep multi-GB PDFs from being loaded whole into memory, the redaction pipeline now streams large documents in fixed-size page chunks rather than holding the entire document in RAM. This implementation was merged to mainline on 2026-08-16.

## Reopen: 2GB+ Leak
Post-merge testing on files at and above 2GB surfaced a memory leak: buffers allocated for each chunk were not being released once the chunk finished processing, so peak memory climbed roughly linearly with file size instead of staying bounded by the chunk size. This defeated the point of chunking for the largest files, and the task was reopened as Active (Reopened).

## In-Progress Fix: Per-Chunk Buffer Release
Charlie is refactoring the stream-chunk handler to explicitly release each chunk's buffer once processing completes, rather than relying on it falling out of scope. Early local testing on a 2.3GB sample shows flat memory usage across chunks instead of the previous climb, but the fix has not yet been validated against the full large-file test corpus.

*Status*: Chunking mechanism is in place and merged; buffer-release refactor to close the 2GB+ leak is still Active and not yet verified end-to-end.
