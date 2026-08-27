# ClickUp Task: CIPH-26
**Source ID**: SRC-CU-CIPH-26

**Task ID**: CIPH-26
**Title**: Audit Trail Logging
**Status**: Active
**Assignee**: Diana
**Priority**: High
**Date Created**: 2026-07-08

## Description
Build an audit-trail system for the redaction pipeline that captures a SHA-256 hash of each input stream together with a companion JSON document recording the redaction map applied to that file, then wire this audit-log generation into the CLI batch path. As of the most recent verification pass, the audit records emitted by the CLI do not match the defined schema, so this remains an open release blocker.

## Acceptance Criteria
- SHA-256 hash is computed for every input stream and captured in the audit record.
- Companion JSON schema pairs the input hash with the redaction map for each processed file.
- Audit-log generation is wired into the CLI batch path.
- CLI-emitted audit records validate cleanly against the defined companion JSON schema (currently failing verification).

## Activity History
- **2026-07-08**: Diana - Task Create (Open)
 - *Opened the task to build a centralized audit-trail system for tracking redaction activity across the pipeline.*
- **2026-07-11**: Bob - Loader Refactor (Active)
 - *Refactored the document loader to prepare for streaming input ahead of hashing and audit capture.*
- **2026-08-05**: Bob - SHA-256 Hashing (Active)
 - *Added SHA-256 hashing of input streams because the audit design requires an input hash alongside the redaction map.*
- **2026-08-15**: Bob - Audit Schema Definition (Active)
 - *Defined the companion JSON audit schema (hash + redaction map) needed before CLI wiring.*
- **2026-09-10**: Bob - CLI Integration (Active)
 - *Wired audit-log generation into the CLI path now that the schema was defined, to satisfy the release gate.*
- **2026-09-18**: Diana - Audit Verify (Mismatch) (Active)
 - *Verification found the CLI-emitted audit records inconsistent with the defined schema; this mismatch remains an open release blocker.*
