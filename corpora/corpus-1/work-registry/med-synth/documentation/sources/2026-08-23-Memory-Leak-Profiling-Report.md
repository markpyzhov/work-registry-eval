**Source ID**: SRC-GDOC-44

# Profiling Report: PDF Loader Memory Leak — Tracemalloc Patch
**Owner**: Bob
**Document Key**: DOC-2044
**Last Updated**: 2026-08-23

## Trigger
Profiling was opened after the T031 large-file chunking reopen surfaced memory growth on 2GB+ documents; the team wanted to confirm whether the loader itself, separate from the chunk-buffer issue being fixed under T031, was also retaining memory it shouldn't.

## Tooling Constraint
The offline lab environment does not have the team's usual commercial profiler available (network-gated license check), so profiling switched to Python's stdlib `tracemalloc`, which works fully offline.

## Findings and Patch
Tracemalloc traced the retained allocations to the PDF loader's internal page-object cache, which was holding references to fully-parsed page objects long after the redaction pass for that page had completed. Bob patched the loader to explicitly drop the cache entry once a page's redaction pass finishes, rather than waiting for document close.

## Validation
Re-ran the same profiling pass post-patch: peak memory during a 2GB+ document run dropped to match the chunk-bounded footprint expected from the T031 chunking work, confirming the loader-side leak — distinct from the T031 buffer-release issue — is resolved.

*Status*: Completed. Loader-side leak patched and verified; result depends on and complements the T031 chunking/buffer-release fix.
