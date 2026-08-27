# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

## Answer

**No — custom temporality-selector configuration is not supported.** But `v1.39.0` did ship a set of predefined temporality selector functions. These are two distinct things that are easy to conflate.

### What was rejected

Custom/string-based temporality-selector parsing and configuration was explicitly turned down by the OpenTelemetry Go SIG:

- **2025-09-25 SIG**: the proposal included a string-based "temporality select"; replacing selector functions via a string selector "raised concerns," and the PR had no recent activity (`SRC-NOTE-01`, `opentelemetry/meeting-notes/entry-3389930076.md`).
- **2025-10-09 SIG**: decision recorded as "Not recommended for inclusion in SDK. Users should use full OpenTelemetry configuration file format instead of custom configuration snippets," with the rationale of standardizing on the OTel configuration format rather than supporting fragmented approaches (`SRC-NOTE-03`, `opentelemetry/meeting-notes/entry-3390010099.md`).
- **2025-10-16 SIG**: the "Exposed Temporality Selector Function" PR was characterized as API pollution and slated for closure; Tyler Yahn took the action to draft a comment and close it (`SRC-NOTE-04`, `opentelemetry/meeting-notes/entry-3479584781.md`).

### What `v1.39.0` did ship

Under the "Added" section of the release (tag `v1.39.0`, published 2025-12-08, released as `v1.39.0/v0.61.0/v0.15.0/v0.0.14` by MrAlias):

> Add temporality selector functions `DeltaTemporalitySelector`, `CumulativeTemporalitySelector`, `LowMemoryTemporalitySelector` to `go.opentelemetry.io/otel/sdk/metric`. (#7434)

PR #7434 ("Add temporality selector functions") was authored by `dprotaso` (`SRC-REL-01`, `opentelemetry/releases/release-v1.39.0.md`).

### Net effect

The Work State for WS-02 Metrics Performance records this as task `T004`: "Custom string selector parsing/configuration rejected; selector functions themselves released in `v1.39.0`." So you get three ready-made selector functions you can pass programmatically, but no SDK-level mechanism for parsing a user-supplied selector string — for that the SIG directs users to the full OpenTelemetry configuration file format.

### Dataset records cited

- `work-states/WS-02-metrics-performance.md` (`path = work-state`) — Decisions and Superseded Directions; task `T004`
- `opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`, `path = sources`)
- `opentelemetry/meeting-notes/entry-3389930076.md` (`SRC-NOTE-01`), `entry-3390010099.md` (`SRC-NOTE-03`), `entry-3479584781.md` (`SRC-NOTE-04`) — all `path = sources`
