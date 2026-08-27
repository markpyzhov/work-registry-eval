**Source ID**: SRC-SLACK-62

# Slack Thread: Telemetry Opt-Out Design
**Channel**: #cipherdoc
**Date**: 2026-08-20

---

**[2026-08-20 11:16] Diana**: Starting the design for the telemetry opt-out. Given the privacy sensitivity, I think we should go with an "opt-in" model instead, but Alice wants a clear "opt-out" toggle in the first-run wizard.

**[2026-08-20 11:20] Alice**: The legal team says as long as it's prominent and clear what data is being sent (mostly crash logs and performance metrics), opt-out is fine for the beta.

**[2026-08-20 11:23] Bob**: I've got the backend ready to check for a `telemetry_enabled` flag in the config. If it's false, the `Segment` client never even initializes.

**[2026-08-20 12:38] Charlie**: Make sure we don't accidentally log any PII in the crash reports. That would defeat the whole purpose of the tool.

**[2026-08-20 13:15] Diana**: I'm adding a redaction filter to the logger itself. Any string that looks like a path or a filename gets scrubbed before it hits the telemetry pipe.

**[2026-08-20 13:18] Alice**: @Diana, let's make sure the GUI has a very obvious toggle in the "Security" tab too.
