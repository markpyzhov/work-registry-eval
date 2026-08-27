**Source ID**: SRC-GDOC-29

# Document: Electron-Shell-Scaffold-Review
**Owner**: Evan
**Document Key**: DOC-2029
**Last Updated**: 2026-08-31 (retrospective, covers 2026-08-14)

## Decision Notes
Note on the initial Electron shell scaffolded 2026-08-14 for CIPH-45 (GUI Wrapper for CLI), for desktop users who don't want a command-line entry point.

## Electron Scaffold
Evan put together a minimal Electron shell that spawns the existing CLI engine as a child process and streams its stdout back into a simple window, rather than reimplementing any redaction logic in the GUI layer. Wrapping the CLI as a subprocess keeps the wrapper thin and means the GUI inherits every CLI fix and feature without duplicated logic.

## Open item at this stage
At the time this scaffold was put together, the wrapper had not yet been packaged or run through a package test; that came afterward and is not part of this scaffold note.
