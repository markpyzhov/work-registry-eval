**Source ID**: SRC-GDOC-50

# Queue Design Review: Async Batch Processing — Concurrency Block
**Owner**: Bob
**Document Key**: DOC-2050
**Last Updated**: 2026-09-04 (retrospective, covers 2026-08-25)

## Worker Management Decision
Retrospective note on the concurrency block confirmed 2026-08-25. For large-scale redaction jobs, the batch API moved from a synchronous blocking loop to an `asyncio`-driven queue: a single producer walks the file system and pushes document tasks, while a fixed pool of async workers pulls from the queue and orchestrates I/O against the redaction engine, built on top of the already-completed multi-threaded worker pool (T026).

## Ordering & Race Risk
Because documents vary widely in size, workers finish out of order. When multiple workers append to the same shared results manifest concurrently, writes can interleave and corrupt the JSON structure.

## Update: Confirmed I/O Race, Throughput Regression
Concurrency testing on 2026-08-25 confirmed the race is real, not just theoretical: under concurrent load, the race condition measurably cuts batch throughput by roughly 10% compared to the expected async speedup, because workers end up retrying/serializing around the corrupted-write recovery path. This is now blocking further rollout of the async scheduler.

## Status
T037 is **Blocked** on resolving the manifest-write race before the async scheduler can be considered production-ready; the throughput regression it causes depends directly on how the T026 worker pool's result-writing is serialized.

*Note*: Do not treat the async queue as production-stable until the manifest-write race is fixed and the ~10% throughput regression is recovered.
