**Source ID**: SRC-SLACK-39

# Slack Thread: License Audit
**Channel**: #cipherdoc
**Date**: 2026-08-09

---

**[2026-08-09 11:13] Diana**: Starting the third-party license audit across the dependency tree — need a full inventory before we sign off on anything for release.

**[2026-08-09 12:37] Alice**: Watch closely for GPL or AGPL. Our client agreements rule out shipping copyleft code in the core engine.

**[2026-08-09 12:46] Diana**: That's exactly what I'm scanning for, using license-checker against the dependency manifests to flag anything outside MIT/Apache/BSD.

**[2026-08-09 13:19] Bob**: Are you following transitive dependencies too? A clean top-level library can still pull in something restrictive underneath.

**[2026-08-09 13:24] Diana**: Yes, doing a recursive pass, not just the direct dependencies.

**[2026-08-09 13:51] Evan**: Want a hand with the Docker base image layers once the app-level scan is done?

**[2026-08-09 14:07] Diana**: That'd help. Still working through the results — nothing conclusive to report yet, I'll have the full inventory soon.
