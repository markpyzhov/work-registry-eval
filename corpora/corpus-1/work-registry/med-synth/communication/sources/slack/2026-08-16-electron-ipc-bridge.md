**Source ID**: SRC-SLACK-54

# Slack Thread: Electron IPC Bridge
**Channel**: #cipherdoc
**Date**: 2026-08-16

---

**[2026-08-16 11:11] Bob**: Just finished the IPC bridge between the Electron main process and the React frontend. We can now pass configuration objects directly through to the batch CLI tool it wraps.

**[2026-08-16 11:43] Evan**: I'm seeing some issues with the process state when a large batch is running. The GUI freezes up because the IPC channel is getting flooded with progress updates.

**[2026-08-16 12:04] Bob**: We should probably throttle those updates. We don't need a message for every single file if it's a 10,000 document batch.

**[2026-08-16 12:07] Charlie**: Or use a separate worker thread for the CLI monitoring?

**[2026-08-16 12:19] Evan**: I'll try debouncing the updates in the main process first. If that doesn't work, I'll move the child process management to a background utility.

**[2026-08-16 13:46] Alice**: @Evan, @Bob, let's keep it simple for now. Even a 1-second update interval is fine for the UI.

**[2026-08-16 13:51] Diana**: Agree. As long as it doesn't look like it's crashed, users are happy.
