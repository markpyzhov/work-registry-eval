**Source ID**: SRC-GDOC-20

# Performance Design: Multi-threading Page Processing
**Owner**: Charlie
**Document Key**: DOC-2020
**Last Updated**: 2026-08-03

## Work-Allocation Approach
Instead of our initial multiprocessing (forking) model which consumed too much RAM per worker, we are moving to a ThreadPoolExecutor model within a single process. 
- **Allocation**: We allocate work at the **Page Level** rather than the Document Level. A 100-page PDF is split into 100 individual rendering tasks, which are distributed across 8 worker threads.

## Observed Bottleneck
Because the Python GIL (Global Interpreter Lock) restricts true parallel execution of Python bytecode, we expected a bottleneck. However, the actual bottleneck is in the `re2` C-extension during the pattern matching phase. When 8 threads simultaneously hit the regex engine with large text spans, lock contention inside the C-extension causes CPU cache trashing, dropping throughput by 15% compared to sequential processing for very dense text.

## The Trade-off
We are trading CPU efficiency for memory stability. Multi-threading allows us to keep only one copy of the 50MB PII Dictionary in RAM. If we used multiprocessing, a 16-core machine would need nearly 1GB just for the dictionary copies.

## Undecided: Safety Limits
We haven't finalized the `max_workers` cap for systems with high core counts (e.g., 32-core workstations). Should we cap the thread pool at 16 to prevent OS-level I/O starvation when writing the temporary BMPs to disk? We need a heavy I/O benchmark before hardcoding this limit.
