**Source ID**: SRC-GDOC-39

# Compatibility Audit: Windows Build Signing Gap
**Owner**: Evan
**Document Key**: DOC-2039
**Last Updated**: 2026-09-02

## Background: Path Fix Cleared Packaging
Backslash path-handling defects that previously broke Windows builds were fixed on 2026-08-10, and a Windows build artifact was successfully produced by 2026-08-12. Packaging itself is no longer the blocker.

## Current Blocker: Missing Code-Signing Certificate
The produced build artifact is unsigned, which triggers a SmartScreen warning and Defender flagging the binary as untrusted.
- **Impact**: Site IT policies commonly block execution of unsigned/SmartScreen-flagged binaries outright, which would prevent installation on target deployment workstations without a manual security-policy override.
- **Root Cause**: No code-signing certificate has been procured or configured in the Windows build pipeline yet.

## Path to Resolution
Procuring a code-signing certificate and wiring signing into the release build step is the only remaining item before this clears the T029 Windows compatibility gate — and, by extension, the T011 release checklist, which is holding on this exact signing gap alongside the T005 image slim-down.

*Audit Status*: Active. Build produces successfully; signing certificate procurement is the sole open blocker.
