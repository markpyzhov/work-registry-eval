# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**No — custom temporality-selector configuration is not supported.** The SIG explicitly rejected it. But `v1.39.0` *did* ship a related, narrower API: three plain temporality **selector functions**.

### 1. Custom temporality-selector configuration: rejected

- **2025-09-25 SIG** (`SRC-NOTE-01`): a PR existed proposing a **string-based "temporality select"** because the default temporality-aggregation functions were not exposed. Concerns were raised about replacing functions via a string selector; no recent activity, likely to be moved out of the milestone.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3389930076.md`
- **2025-10-09 SIG** (`SRC-NOTE-03`): decision — **not recommended for inclusion in the SDK**. Users should use the **full OpenTelemetry configuration file format** rather than custom configuration snippets; rationale was to standardize on the OTel config format instead of fragmented approaches. Tyler (Yahn) to respond with the standardization feedback.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3390010099.md`
- **2025-10-16 SIG** (`SRC-NOTE-04`): the "Exposed Temporality Selector Function" PR was judged **API pollution and slated for closure**; Tyler took the action to draft a comment and close it.
  - `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`

### 2. What `v1.39.0` did ship: selector functions (PR #7434)

Under **Added** in the release notes:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

PR #7434 was authored by `@dprotaso` (listed as a first-time contributor in this release). Release `v1.39.0` was published 2025-12-08 by `MrAlias`.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`

### 3. Authoritative work state

`WS-02-metrics-performance` (status: in_progress, owner `dashpole`) records this as task `T004`: "Custom string selector parsing/configuration rejected; selector functions themselves released in `v1.39.0`." Its Decisions section keeps the two things distinct — the custom-parsing/configuration path was rejected, while the three selector functions shipped separately via #7434.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (coverage row: "custom parsing rejected; selector functions released in `v1.39.0`")

### Summary

The distinction is deliberate: `v1.39.0` gives you three ready-made selector **functions** you call in Go code, not a mechanism to configure or parse a *custom* temporality selector. For configuration-driven temporality, the SIG's direction is the full OpenTelemetry configuration file format, not SDK-level selector parsing. No comments in `work-states/comments/2026-03.md` modify this item.
