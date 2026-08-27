# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

**No — custom temporality-selector *configuration* is not supported. But v1.39.0 did ship three ready-made temporality selector functions.**

## The two things are distinct

**1. Custom selector configuration: rejected, not shipped**

A PR ("Exposed Temporality Selector Function") proposed string-based temporality selector parsing so users could configure selectors via custom configuration snippets. The SIG rejected it:

- Initial discussion noted the PR existed but that "replacing functions via string selector raised concerns," with no recent activity and likely removal from the milestone (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3389930076.md`, SRC-NOTE-01).
- **2025-10-09 decision:** "Not recommended for inclusion in SDK. Users should use full OpenTelemetry configuration file format instead of custom configuration snippets" — the rationale being standardization on the OTel configuration format rather than fragmented approaches (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3390010099.md`, SRC-NOTE-03).
- **2025-10-16:** Tyler Yahn noted a prior SIG concluded the PR was **API pollution and should be closed**, and took the action item to draft a comment and close it (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`, SRC-NOTE-04).

**2. Selector functions: shipped in v1.39.0 via #7434**

The v1.39.0 release notes list under Added:

> "Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)"

(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`, SRC-REL-01)

So v1.39.0 gives you three predefined selectors you can pass programmatically to the metric SDK — delta, cumulative, and low-memory — but no mechanism to define or parse your own selector from configuration.

## Status

This is tracked as task `T004` in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-02-metrics-performance.md` (owner: dashpole, last updated 2025-12-15), marked complete: "Custom string selector parsing/configuration rejected; selector functions themselves released in `v1.39.0`." v1.39.0 was published 2025-12-08.
