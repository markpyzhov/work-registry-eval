# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Answer

The decision came out of the **OpenTelemetry Go SIG meeting on 2025-11-20** (notes posted 2025-11-26 by pellared).

**The decision: merge the OTelConf RC support PR as-is, pending normal review** — and track the experimental-API structure question separately under the `1.40.0` milestone rather than letting it hold up the release.

### Context behind the decision

- The next Go release was **blocked on the RC support module**; the PR simply needed reviews.
- **Alex Boten's requested changes did not need to land in the current PR.** The rationale: the module is `0.x`, so breaking changes are acceptable later.
- The one guardrail agreed on was to **avoid exposing public API that is known to be removed immediately**.
- On handling experimental features, the SIG discussed:
  - A `WithExperimentalFeatures`-style flag was judged **likely unhelpful**.
  - A possible **`x` submodule** to clearly isolate experimental APIs was seen as the more promising route, aligning with the OTel-wide push toward opt-in experimental features.
  - This was deferred to a follow-up, not made a blocker.

### Resulting action items

- **Alex Boten**: open an issue to track evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers**: review the OTelConf RC support PR (the remaining gate on the release).

### Sources

- `opentelemetry/meeting-notes/entry-3581463689.md` — [SRC-NOTE-07], Meeting Note: OpenTelemetry Go SIG, meeting date 2025-11-20, canonical URL https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689 (sections "1. Next Go release & OTelConf RC support", "Decisions", "Action Items"). Attendees: Tyler Yahn, Owen Williams, Sam Xie, Alex Boten, David Ashpole, Bryan Boreham.

Related background (same dataset), for how otelconf got to this point:
- `opentelemetry/meeting-notes/entry-3479626706.md` — [SRC-NOTE-05], Go SIG 2025-10-23: chose the contrib-first approach in `otelconf` over SDK-level support for `OTEL_EXPERIMENTAL_CONFIG_FILE`.
- `opentelemetry/issues/opentelemetry-go-contrib-8059.md` — [SRC-ISSUE-05], "otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable" (closed/completed).
