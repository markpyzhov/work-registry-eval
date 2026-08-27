**Source ID**: SRC-GDOC-04

# OCR Fallback — Tesseract Proof of Concept

**Owner**: Charlie
**Document Key**: DOC-2004
**Last Updated**: 2026-06-28

Task T008 (OCR fallback for documents without a usable native text layer, WS-01) has reached a Tesseract-based proof of concept today.

## What This Covers
A POC path for routing documents with no usable native text layer through OCR instead, so the redaction pipeline still has text to run detection against.

## Status
Active — POC only.

## Limitation
This is a proof of concept, not a production integration. Performance characteristics under real batch load and confidence-threshold behavior have not been evaluated yet.

## Next Step
Move from POC toward integration with the rest of the scan pipeline; no timeline set yet.
