**Source ID**: SRC-GDOC-23

# Windows Backslash Path Handling Notes
**Owner**: Evan
**Document Key**: DOC-2023
**Last Updated**: 2026-08-19 (retrospective, covers 2026-08-10)

Retrospective note on the path-handling fix made 2026-08-10 for CIPH-39 (Windows Compatibility).

## Issue
Path arguments containing backslashes (Windows-style, e.g. `C:\docs\input.pdf`) were mishandled by the CLI's path parser, which had only been exercised against forward-slash paths on Linux/macOS.

## Fix
Path arguments are now normalized to the platform-native separator before they reach the file-loading code, rather than assuming forward slashes everywhere.

## Scope
This note covers path-string handling only. It does not cover code signing or Windows Defender/SmartScreen behavior — those are separate, later concerns for CIPH-39 and are not addressed here.
