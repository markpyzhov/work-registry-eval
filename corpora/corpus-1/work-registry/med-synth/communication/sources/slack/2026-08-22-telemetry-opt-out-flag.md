**Source ID**: SRC-SLACK-63

# Slack Thread: Telemetry Opt-Out Flag
**Channel**: #cipherdoc
**Date**: 2026-08-22

---

**[2026-08-22 14:12] Bob**: The `telemetry_enabled` flag is now fully integrated into the CLI and the API. Default is set to `true` but it's easily overridden in `config.yaml`.

**[2026-08-22 14:37] Evan**: Can we also support an environment variable like `DISABLE_TELEMETRY=1`? That would be easier for the Docker deployments.

**[2026-08-22 14:43] Bob**: Good call. I'll add that to the `Settings` loader.

**[2026-08-22 14:46] Diana**: I noticed that even when it's off, the app still tries to ping the update server on startup. Does that count as telemetry?

**[2026-08-22 14:57] Alice**: Update checks are fine, that's a security requirement. But we shouldn't send any machine IDs with that request.

**[2026-08-22 15:13] Bob**: It's a clean GET request, no headers other than the current version string.

**[2026-08-22 15:16] Diana**: Okay, I'll verify that with a packet capture tomorrow.
