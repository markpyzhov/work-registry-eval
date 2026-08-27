# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**No — custom temporality-selector *configuration* is not supported, but v1.39.0 did ship temporality selector *functions*.** These are two distinct things that are easy to conflate.

### What was rejected: custom temporality-selector configuration

- At the 2025-09-25 SIG (recorded 2025-10-10), a PR proposed exposing default temporality aggregation functions plus a string-based "temporality select." Concerns were raised about replacing functions via a string selector, and the item had no recent activity and was likely to be moved out of the milestone — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3389930076.md` (SRC-NOTE-01)
- At the 2025-10-09 SIG, the decision was explicit: exposing temporality-selector parsing functions for configuration is **not recommended for inclusion in the SDK**. Users should use the full OpenTelemetry configuration file format rather than custom configuration snippets; the rationale was standardizing on the OTel config format instead of fragmented approaches — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3390010099.md` (SRC-NOTE-03)
- At the 2025-10-16 SIG, Tyler Yahn noted a prior SIG had concluded the "Exposed Temporality Selector Function" PR was **API pollution and should be closed**, and took the action item to draft a comment and close it — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04)

### What v1.39.0 did ship: three selector functions (PR #7434)

The v1.39.0 release notes (Added section) list:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

Contributed by @dprotaso (their first contribution), in `go.opentelemetry.io/otel/sdk/metric`. Release tag `v1.39.0`, published 2025-12-08, released by MrAlias — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01)

### Authoritative current state

The work state tracks this as task `T004`: "Custom string selector parsing/configuration rejected; selector functions themselves released in `v1.39.0`" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`. The index summarizes the same: "custom parsing rejected; selector functions released in `v1.39.0`" — `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`

**Practical upshot:** in v1.39.0 you get three ready-made selector functions you can pass programmatically to the metrics SDK, but there is no supported mechanism for parsing/configuring a custom temporality selector from a string or config snippet. That path was deliberately closed in favor of the standard OpenTelemetry configuration file format.
