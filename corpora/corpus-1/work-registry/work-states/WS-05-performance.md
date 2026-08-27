# WS-05: Performance Benchmarking and System Optimization
**Status**: in_progress
**Priority**: P1
**Owner**: Charlie / Bob
**Project**: CipherDoc
**Last Updated**: 2026-09-22

## Sources
- `S1` — `SRC-CU-CIPH-36` — [ClickUp Task CIPH-36: Multi-threading for Local Processing](../med-synth/tasks/CIPH-36-Multi-threading-for-Local-Processing.md)
- `S2` — `SRC-SLACK-31` — [Slack Thread: Batch Worker Pool Integration](../med-synth/communication/sources/slack/2026-08-05-batch-worker-pool-integration.md)
- `S3` — `SRC-CU-CIPH-38` — [ClickUp Task CIPH-38: Performance Benchmarks](../med-synth/tasks/CIPH-38-Performance-Benchmarks.md)
- `S4` — `SRC-MEET-05` — [Fireflies Transcript: Performance Benchmarks Blocker](../med-synth/communication/sources/fireflies/2026-08-09-Performance-Benchmarks-Blocker.md)
- `S5` — `SRC-SLACK-35` — [Slack Thread: Benchmark Results](../med-synth/communication/sources/slack/2026-08-11-benchmark-results.md)
- `S6` — `SRC-CU-CIPH-41` — [ClickUp Task CIPH-41: Large File Chunking](../med-synth/tasks/CIPH-41-Large-File-Chunking.md)
- `S7` — `SRC-SLACK-43` — [Slack Thread: Large File Chunking Reopen](../med-synth/communication/sources/slack/2026-08-18-large-file-chunking-reopen.md)
- `S8` — `SRC-CU-CIPH-43` — [ClickUp Task CIPH-43: Memory Leak Profiling](../med-synth/tasks/CIPH-43-Memory-Leak-Profiling.md)
- `S9` — `SRC-SLACK-49` — [Slack Thread: Memory Leak tracemalloc Patch](../med-synth/communication/sources/slack/2026-08-21-memory-leak-tracemalloc.md)
- `S10` — `SRC-CU-CIPH-47` — [ClickUp Task CIPH-47: Async Batch Processing](../med-synth/tasks/CIPH-47-Async-Batch-Processing.md)
- `S11` — `SRC-SLACK-61` — [Slack Thread: Async Batch I/O Race](../med-synth/communication/sources/slack/2026-08-25-async-batch-io-race.md)
- `S12` — `SRC-GDOC-50` — [Async Batch Processing Queue Review](../med-synth/documentation/sources/2026-09-04-Async-Batch-Processing-Queue-Review.md)

## Request / Context
Enterprise-scale workloads: multi-core utilization, bare-metal benchmarks, large-file stream chunking (2GB+), memory profiling, and async batch scheduling.

## Task List
- [x] `T026` (mapped to CIPH-36) — Implement multi-threading for local batch processing. `(S1, S2)`
- [x] `T028` (mapped to CIPH-38) — Conduct bare-metal performance benchmarks. `(S3, S4, S5)`
- [ ] `T031` (mapped to CIPH-41) — Implement large file stream chunking. `(S6, S7)`
- [x] `T033` (mapped to CIPH-43) — Profile memory leaks and patch PDF loader. `(S8, S9)`
- [ ] `T037` (mapped to CIPH-47) — Implement Async Batch API Scheduler. `(S10, S11, S12)`

## Active Work
- **T031 — MedFirst pilot OOM (CMT-2026-08-003)**: Clinic workstation OOM on 4.7GB PDF with 8GB RAM — pilot-blocker prioritized and tied to T011 release gate. `(CMT-2026-08-003)`
- **T031 / CIPH-41**: **Reopened/active**. Initial chunking landed but Bob found severe memory leaks on files exceeding 2GB during long batch runs (`S7`). Charlie is refactoring stream buffer release logic. `(S6, S7)`

## Blockers and Dependencies
- **T037 / CIPH-47**: **Blocked**. Concurrent manifest-write race reduces throughput ~10% and can corrupt JSON under load (`S11`, `S12`).

## Decisions and Superseded Directions
- **Profiling Tools**: External cloud profiler superseded by native Python `tracemalloc` for air-gapped operation. `(S8, S9)`

## Done / Evidence
- `T026 / CIPH-36` — Process pool scales linearly up to 16 cores. `(S2)`
- `T028 / CIPH-38` — Benchmarks confirm 500 pages/minute on standard enterprise hardware. `(S5)`
- `T033 / CIPH-43` — PDF loader memory leak patched; consumption stable after 10,000 documents. `(S9)`

## Needs Manual Triage
- None.

## Next Update Needed
T031 stream buffer refactor and T037 manifest-write race fix.
