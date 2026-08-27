# ClickUp Task: CIPH-47
**Source ID**: SRC-CU-CIPH-47

**Task ID**: CIPH-47
**Title**: Async job scheduler for concurrent batch API work
**Status**: Blocked
**Assignee**: Bob
**Priority**: Normal
**Date Created**: 2026-08-18

## Description
Add an asynchronous job scheduler to the batch API for higher throughput under concurrent load. Async workers were added, but a concurrent I/O race was found to cut throughput by roughly 10%; the task is blocked, depending on the multi-threading work.

## Acceptance Criteria
- Async job scheduler processes batch API jobs concurrently without a throughput regression.
- Concurrent I/O race condition is resolved (currently the blocking issue).

## Activity History
- **2026-08-18**: Alice - Task Create (Open)
 - *Opened the task because an async batch API scheduler is needed for higher throughput.*
- **2026-08-25**: Diana - I/O Race Block (Blocked)
 - *Blocked after finding a concurrent I/O race that cuts throughput by roughly 10%, depending on the multi-threading work.*
