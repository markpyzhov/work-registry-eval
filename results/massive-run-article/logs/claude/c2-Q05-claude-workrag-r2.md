# Is custom temporality-selector configuration supported in OpenTelemetry Go `v1.39.0`, and what related selector API did that release ship?

<!-- RESPONSE_START -->

**Short answer: No — custom temporality-selector configuration is not supported. What `v1.39.0` shipped is a set of three fixed, predefined selector functions, not user-configurable selector parsing.**

## Custom temporality-selector configuration: rejected

The authoritative Work State (`work-states/WS-02-metrics-performance.md`, task `T004`, workstream WS-02 "Metrics Performance", owner `dashpole`, last updated 2025-12-15) records custom string selector parsing/configuration as **rejected**:

- **2025-10-09 (SIG meeting, `SRC-NOTE-03` / `opentelemetry/meeting-notes/entry-3390010099.md`)**: Tyler Yahn and David Ashpole discussed exposing temporality-selector *parsing* functions for configuration. Decision: **not recommended for inclusion in the SDK**. Rationale — users should use the full OpenTelemetry configuration file format rather than custom configuration snippets, to standardize on the OTel config format instead of supporting fragmented approaches. Tyler took the action to respond with the standardization feedback.
- **Earlier context (2025-09-25, `SRC-NOTE-01` / `entry-3389930076.md`)**: the original PR proposed a string-based "temporality select"; replacing functions via a string selector raised concerns, and the item had stalled with a likelihood of being moved out of the milestone.
- **2025-10-16 (`SRC-NOTE-04` / `entry-3479584781.md`)**: during the v1.39.0 milestone check-in, the "Exposed Temporality Selector Function" PR was described as **API pollution** and slated for closure; Tyler said he would draft a comment and close it that day.

## What `v1.39.0` did ship

Separately from the rejected configuration work, the `v1.39.0` release (`SRC-REL-01` / `opentelemetry/releases/release-v1.39.0.md`; tag `v1.39.0`, published 2025-12-08, released as v1.39.0/v0.61.0/v0.15.0/v0.0.14 by MrAlias) added three **temporality selector functions** to `go.opentelemetry.io/otel/sdk/metric` via PR **#7434** ("Add temporality selector functions", by `dprotaso`):

- `DeltaTemporalitySelector`
- `CumulativeTemporalitySelector`
- `LowMemoryTemporalitySelector`

So the distinction is: the ready-made selector *functions* are available in `v1.39.0`, while the mechanism for users to configure/parse a *custom* selector (e.g. from a string) was deliberately not added — that need is directed at the OpenTelemetry configuration file format instead.

## Dataset records cited

- `work-states/WS-02-metrics-performance.md` (`path = work-state`) — task `T004`, Decisions and Superseded Directions section
- `opentelemetry/meeting-notes/entry-3390010099.md` (`SRC-NOTE-03`) — 2025-10-09 SIG rejection and rationale
- `opentelemetry/meeting-notes/entry-3479584781.md` (`SRC-NOTE-04`) — 2025-10-16 "API pollution" / closure
- `opentelemetry/meeting-notes/entry-3389930076.md` (`SRC-NOTE-01`) — 2025-09-25 string-selector concerns
- `opentelemetry/releases/release-v1.39.0.md` (`SRC-REL-01`) — the three selector functions, `#7434`
- `work-states/index.md` corroborates the as-of state ("custom parsing rejected; selector functions released in `v1.39.0`"), though as a navigation aid rather than evidence.
