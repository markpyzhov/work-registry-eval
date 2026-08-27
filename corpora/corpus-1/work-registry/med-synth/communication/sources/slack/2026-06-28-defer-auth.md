**Source ID**: SRC-SLACK-08

# Slack Thread: API Authentication Deferral
**Channel**: #cipherdoc
**Thread opened**: 2026-06-28
**Last activity**: 2026-08-20

---

**[2026-06-28 13:07] Bob**: Looking into REST API auth for v1.0. Do we need a full auth story now, or is trusted local network enough for the first release?

**[2026-06-28 13:22] Diana**: Given the PII involved, something robust would be nice. But if this is strictly local-network-only, we might not need it for v1.0.

**[2026-06-28 14:00] Bob**: Doing a short study either way — what we'd need if we keep auth in scope versus what we defer.

**[2026-06-29 14:23] Diana**: If we defer, we should at least write down the v1.1 requirements so we don't lose them.

**[2026-06-30 09:01] Alice**: Team, we're falling behind on core engine work. I'm deferring the auth module to v1.1. For v1.0, the API assumes a trusted local network.

**[2026-06-30 09:19] Diana**: Manageable if we stay local-network-only. I'll note the deferral.

**[2026-06-30 09:21] Bob**: Fine. I'll keep the seams clean so adding auth later isn't a rewrite.

**[2026-08-05 11:04] Bob**: Still deferred — capturing v1.1 auth requirements while we remember them: REST auth with rotation support, since v1.0 is local-network-only.

**[2026-08-05 11:06] Diana**: Agreed. Folding that into the deferred-work notes so it survives until v1.1 planning.

**[2026-08-20 10:11] Alice**: Rechecked release scope for v1.0 — auth stays deferred to post-v1.0.0. Trusted-network assumption still holds.
