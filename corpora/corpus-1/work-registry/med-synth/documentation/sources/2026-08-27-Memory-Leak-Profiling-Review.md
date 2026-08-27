**Source ID**: SRC-GDOC-27

# Document: Memory-Leak-Hotspot-Identification-Review
**Owner**: Bob
**Document Key**: DOC-2027
**Last Updated**: 2026-08-27 (retrospective, covers 2026-08-17)

## Decision Notes
Analysis of memory consumption patterns in the redaction engine, targeting long-running batch processes. This review was triggered by signals from the large-file stream chunking rework.

## Identification and Profiling Findings
Bob began identifying leak hotspots in the PDF loader on 2026-08-17. The standard profiler tooling normally used for this kind of investigation was not available in the offline lab environment, which blocked progress for a few days until Charlie switched the approach to Python's stdlib `tracemalloc` on 2026-08-21. Tracing allocations during a chunked large-file run with tracemalloc pointed to the PDF loader's page-buffer handling as the source of retained allocations across chunk boundaries — buffers that should have been released between chunks were staying reachable.

## Scope of this note
This note covers only the identification pass: where the leak signal traces to and how it was found. Patching the loader is separate follow-up work and is not reported on here.
