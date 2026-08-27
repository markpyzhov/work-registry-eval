**Source ID**: SRC-SLACK-45

# Slack Thread: Redaction Profile Schema
**Channel**: #cipherdoc
**Date**: 2026-08-12

---

**[2026-08-12 11:29] Bob**: Designing an exportable schema for the redaction profile — dictionary versions, regex patterns, thresholds, everything that went into a given batch, so it can be reviewed later.

**[2026-08-12 11:32] Alice**: This is the piece that makes redaction decisions reproducible for compliance, right? If someone asks why a name got redacted, we need to be able to show the exact rule.

**[2026-08-12 11:38] Bob**: Exactly the goal — a machine-readable export of everything that fired.

**[2026-08-12 12:09] Charlie**: Are you including the engine version in it? Regex behavior can shift slightly between versions.

**[2026-08-12 12:12] Bob**: Good call, adding that to the schema.

**[2026-08-12 12:13] Diana**: What about custom dictionaries someone's added locally? Do those need to be part of the export too?

**[2026-08-12 12:54] Bob**: They have to be, otherwise the profile's incomplete. Still working out the shape of the schema before I touch the export endpoint itself.
