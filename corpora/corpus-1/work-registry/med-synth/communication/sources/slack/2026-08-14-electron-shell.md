**Source ID**: SRC-SLACK-53

# Slack Thread: Electron Shell Scaffold
**Channel**: #cipherdoc
**Date**: 2026-08-14

---

**[2026-08-14 09:20] Evan**: Kicking off. I've got a basic Electron scaffold running. It's successfully spawning the CLI as a child process and capturing stdout.

**[2026-08-14 09:25] Alice**: Nice.

**[2026-08-14 09:27] Bob**: Are you bundling the CLI binary with the app, or expecting it to be in the PATH?

**[2026-08-14 09:31] Evan**: Plan is to bundle it. I'm using `electron-builder` to package the platform-specific binaries into the `resources` folder.

**[2026-08-14 09:55] Alice**: @Evan, how are we handling the redaction preview in the GUI? Is it just a log view, or something more visual?

**[2026-08-14 11:51] Diana**: We really need the visual overlay integrated here. Users aren't going to want to look at raw JSON logs.

**[2026-08-14 13:27] Evan**: Right now it's just a progress bar and a log. I'll start looking at how to bridge the preview UI into the Electron window next week.

**[2026-08-14 13:41] Charlie**: Make sure you handle the IPC channel securely. We don't want to expose any file paths through the renderer process.
