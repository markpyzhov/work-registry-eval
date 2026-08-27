**Source ID**: SRC-GDOC-31

# Engineering Note: Async Job Scheduler
**Owner**: Bob
**Document Key**: DOC-2031
**Last Updated**: 2026-09-04 (retrospective, covers 2026-08-20)

Retrospective note on the async job scheduler added 2026-08-20 to the batch API under CIPH-47, for higher throughput under concurrent load.

## What was added
An asynchronous scheduler that accepts batch API jobs and dispatches them to worker threads without blocking the request path, building on the multi-threading work already integrated into the batch CLI.

## Design
Jobs are queued with a job ID returned immediately to the caller; a separate status endpoint reports progress. Workers pull from the same queue used by the multi-threaded batch path.

## Scope
This note covers the scheduler's implementation and design only. It does not cover any concurrency issues found during later evaluation of the scheduler under load; those are separate from what this note documents.
