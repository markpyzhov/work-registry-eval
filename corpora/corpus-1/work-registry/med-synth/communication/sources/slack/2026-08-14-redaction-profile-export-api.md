**Source ID**: SRC-SLACK-46

# Slack Thread: Redaction Profile Export API
**Channel**: #cipherdoc
**Date**: 2026-08-14

---

**[2026-08-14 09:23] Bob**: Hey @engine, just pushed the initial implementation for the export API. You can hit `/v1/export/profile` on the dev branch now. It should return the full Pydantic-validated policy bundle.

**[2026-08-14 09:28] Charlie**: Nice. Does it include the regex manifest, or is that a separate call? I need to know what patterns were active for the audit trail.

**[2026-08-14 09:46] Bob**: It's all in the one bundle. I've got a `regex_manifest` key that maps the pattern IDs to the actual compiled strings and their internal tags.

**[2026-08-14 09:57] Alice**: @Bob will this export include the user-defined overrides too? We had that discussion in the standup about making sure manual reviewers can see why a rule was bypassed.

**[2026-08-14 09:59] Bob**: Yeah, the `overrides` list is included. It's basically a JSON dump of the current state of the profile.

**[2026-08-14 10:36] Diana**: Just pulled the latest and tried hitting it with an uninitialized profile. It's returning a 500 right now instead of a 404. I'll open a sub-task, but Bob can you look at the null check on the `profile_manager`?

**[2026-08-14 10:39] Bob**: My bad, I see it. The session wasn't being validated before the export call. Pushing a fix to `feature/export-api` in 5 mins. :pinched_fingers:

**[2026-08-14 10:41] Diana**: Fixed! Returning 404 now for empty states. :thumbsup:
