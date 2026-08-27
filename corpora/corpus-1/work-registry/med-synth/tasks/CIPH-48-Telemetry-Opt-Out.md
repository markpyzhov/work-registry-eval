# ClickUp Task: CIPH-48
**Source ID**: SRC-CU-CIPH-48

**Task ID**: CIPH-48
**Title**: Add a CLI flag to opt out of telemetry
**Status**: Completed
**Assignee**: Diana
**Priority**: Normal
**Date Created**: 2026-08-18

## Description
Give the CLI an explicit telemetry opt-out flag for privacy. A network trace confirmed no telemetry is sent once the opt-out flag is set.

## Acceptance Criteria
- CLI supports an explicit opt-out flag for telemetry.
- Network trace confirms zero outbound telemetry traffic when the flag is set.

## Activity History
- **2026-08-18**: Alice - Task Create (Open)
 - *Opened the task because telemetry must support a CLI opt-out for privacy.*
- **2026-08-24**: Diana - Telemetry Trace Confirm (Completed)
 - *Confirmed via network trace that no telemetry is sent when the opt-out flag is set.*
