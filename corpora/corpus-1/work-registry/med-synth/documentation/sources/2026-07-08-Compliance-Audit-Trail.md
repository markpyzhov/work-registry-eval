**Source ID**: SRC-GDOC-11

# Compliance Audit Trail — Design Intent

**Owner**: Diana
**Document Key**: DOC-2011
**Last Updated**: 2026-07-08

T016 opens today: build an audit-trail system for the redaction pipeline.

## Intended Design
Each processed file should produce:
- a SHA-256 hash of the input stream, and
- a companion JSON document recording the redaction map applied to that file.

The hash and the redaction map travel together so a given audit record can be tied back to a specific input.

## Status
Open — this captures design intent at task creation. No implementation has started.

## Next Step
A loader refactor to support streaming input is expected to come first, ahead of wiring in hashing and audit capture.
