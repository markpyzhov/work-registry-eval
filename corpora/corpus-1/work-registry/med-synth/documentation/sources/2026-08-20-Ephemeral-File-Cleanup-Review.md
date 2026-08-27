**Source ID**: SRC-GDOC-19

# OCR Temp File Path Trace
**Owner**: Charlie
**Document Key**: DOC-2019
**Last Updated**: 2026-08-20 (retrospective, covers 2026-08-07)

Retrospective trace of where the OCR fallback module writes temporary files during a run, recorded 2026-08-07.

## Traced paths
A single run of the per-page OCR fallback pool creates three categories of temporary artifact:

1. A per-page rasterized image, one file per page, in a process-local temp directory.
2. A per-page OCR output buffer, written before confidence-threshold filtering is applied.
3. A run-level manifest listing which pages fell back to OCR versus native text extraction.

## Purpose of this trace
This trace was compiled as an input to the ephemeral-file-cleanup work so that whatever cleanup mechanism is built has a concrete list of paths to target. It only records where files land and when they are created.

## Open item
Confirming that these three path categories are actually removed after a run, on both the success and failure paths, is outside the scope of this trace and is not addressed here.
