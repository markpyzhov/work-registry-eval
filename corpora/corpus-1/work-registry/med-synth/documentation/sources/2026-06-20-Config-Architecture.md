**Source ID**: SRC-GDOC-03

# Redaction Policy Configuration — Format Decision

**Owner**: Alice
**Document Key**: DOC-2003
**Last Updated**: 2026-06-20

## Decision
For T006 (redaction-policy configuration system, WS-01), we are moving the format decision from the earlier JSON choice (decided 2026-06-18) to **YAML**.

## Rationale
YAML was chosen over JSON for inline comments and general readability for the humans who maintain redaction-policy config files day to day.

## Status
Active. Implementation against the YAML decision has not started as of this note.

## Follow-up
Charlie is expected to pick up implementation next; no completion date has been set yet.
