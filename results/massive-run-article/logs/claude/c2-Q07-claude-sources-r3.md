# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Answer

At the OpenTelemetry Go SIG meeting of **2025-11-20** (notes posted 2025-11-26 by pellared), the SIG decided to **merge the OTelConf RC support PR as-is, pending normal review** — i.e., not to hold it for the additional changes Alex Boten had requested.

### The decision and its reasoning

- **Merge as-is (pending normal review).** The next Go release was blocked on the RC support module, and the PR was only waiting on reviews.
- **Alex's requested changes do not need to be in the current PR.** They can land as follow-ups.
- **Justification:** the module is `0.x`, so breaking changes are acceptable later. The one caveat agreed on was to **avoid exposing public API that is known to be removed immediately**.
- **Experimental-API structure deferred to a follow-up**, tracked under the **`1.40.0` milestone**. On approach:
  - A `WithExperimentalFeatures`-style flag was judged likely unhelpful.
  - A possible **`x` submodule** to clearly isolate experimental APIs was preferred, aligning with the OTel-wide push toward opt-in experimental features.

### Resulting action items

- **Alex Boten:** open an issue to track evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers:** review the OTelConf RC support PR (the only thing gating the release).

### Context on the rest of the release

Other work discussed at the same meeting was explicitly **not** release-blocking: observability PRs (e.g. self-observability for OTel gRPC), sync-map/atomics for fixed-bucket histograms, and exemplar reservoir changes were all deemed safe to slip to the next release and to be included only if ready. The otelhttp default-HTTP-client deprecation follow-ups needed review for inclusion in the upcoming release but were not the blocker.

### Sources

- `opentelemetry/meeting-notes/entry-3581463689.md` — [SRC-NOTE-07], Go SIG meeting 2025-11-20 (published 2025-11-26, author pellared); canonical URL `https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689`. Sections used: "1. Next Go release & OTelConf RC support", "Decisions", "Action Items".

Supporting background (same dataset, not the decision itself):
- `opentelemetry/meeting-notes/entry-3479626706.md` — [SRC-NOTE-05], Go SIG 2025-10-23: earlier decision to prototype config-file support in contrib/otelconf rather than the SDK.
- `opentelemetry/issues/opentelemetry-go-contrib-8059.md` — [SRC-ISSUE-05], `otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable` (closed/completed).
