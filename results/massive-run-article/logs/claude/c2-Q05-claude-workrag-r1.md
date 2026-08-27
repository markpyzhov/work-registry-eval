# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**No — custom temporality-selector configuration is not supported.** But `v1.39.0` did ship a set of fixed, exported temporality selector *functions*, which is a different thing. These two facts are easy to conflate.

### 1. Custom temporality-selector configuration: rejected

The Go SIG explicitly declined to support user-supplied/custom temporality-selector configuration in the SDK:

- **2025-09-25 SIG** (`SRC-NOTE-01`, meeting note `entry-3389930076.md`): a PR existed proposing a string-based "temporality select"; the note records that default temporality aggregation functions were not exposed and that **replacing functions via a string selector raised concerns**. No recent activity; likely to be moved out of the milestone.
- **2025-10-09 SIG** (`SRC-NOTE-03`, `entry-3390010099.md`): decision — **"Not recommended for inclusion in SDK. Users should use full OpenTelemetry configuration file format instead of custom configuration snippets."** Rationale: standardize on the OTel configuration format rather than support fragmented approaches. Tyler Yahn to respond with the standardization feedback.
- **2025-10-16 SIG** (`SRC-NOTE-04`, `entry-3479584781.md`): the "Exposed Temporality Selector Function" PR was characterized as **API pollution and slated for closure**; Tyler took the action item to draft a cohesive comment and close it.

Per the Work State `WS-02: Metrics Performance`, item `T004` is closed out as: custom string selector parsing/configuration **rejected**.

### 2. What `v1.39.0` actually shipped

The release notes for `v1.39.0` (`SRC-REL-01`, tag `v1.39.0`, published 2025-12-08, released by MrAlias) list under **Added**:

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

PR **#7434** ("Add temporality selector functions") was contributed by **@dprotaso** — listed among the release's new contributors.

So the release exposes three **predefined** selector functions in `go.opentelemetry.io/otel/sdk/metric` that users can pass programmatically. What it does not provide is any mechanism to configure or parse a *custom* selector (e.g. from a config string) — that path was deliberately closed in favor of the full OpenTelemetry configuration file format.

### Records cited
- `work-states/WS-02-metrics-performance.md` (`path = work-state`) — Decisions and Superseded Directions; task `T004`
- `opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`, `path = sources`) — Added section, PR list, new contributors
- `opentelemetry/meeting-notes/entry-3390010099.md` (`SRC-NOTE-03`) — 2025-10-09 rejection decision and rationale
- `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`) — 2025-10-16 "API pollution" / closure action item
- `opentelemetry/meeting-notes/entry-3389930076.md` (`SRC-NOTE-01`) — 2025-09-25 concerns about the string-based selector
