**Source ID**: SRC-SLACK-09

# Slack Thread: Security Patch - CORS Issue
**Channel**: #cipherdoc
**Thread opened**: 2026-07-10
**Last activity**: 2026-07-15

---

**[2026-07-10 14:20] Diana**: @Bob, I just ran a security scan on the API. We've got a wide-open CORS policy. `Access-Control-Allow-Origin: *` is a no-go for this project.

**[2026-07-10 14:23] Bob**: Oops, that was left over from local testing on the scaffold. I'll tighten it up now.

**[2026-07-10 14:43] Bob**: Applying the CORS patch. It now only allows requests from the defined `ALLOWED_ORIGINS` in the environment config.

**[2026-07-10 14:50] Diana**: Scan is coming back clean now.

**[2026-07-10 14:52] Bob**: Thanks for the catch, Diana. I've added a lint check to prevent `*` from being committed in the future.

**[2026-07-10 15:45] Alice**: Good catch. Let's make sure we don't have any other dev-only flags leaking into the main branch.

**[2026-07-15 09:54] Diana**: Re-ran the CVE and CORS scans ahead of the release evidence pack — patch is still holding, no regressions since Bob's fix.

**[2026-07-15 09:55] Bob**: Good. I'll note that in the security patch record.
