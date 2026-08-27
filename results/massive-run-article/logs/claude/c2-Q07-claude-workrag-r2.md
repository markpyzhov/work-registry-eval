# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Decision

At the OpenTelemetry Go SIG meeting on **2025-11-20** (notes published 2025-11-26 by pellared, `SRC-NOTE-07`), the SIG decided to **merge the OTelConf RC support PR as-is, pending normal review** — and to **defer the broader experimental-API structure question to a separate tracking issue under the `1.40.0` milestone** rather than let it hold up the release.

## Reasoning given in the meeting

- The next Go release was blocked on the RC support module; the PR simply needed reviews.
- Alex Boten's requested changes did **not** need to land in that PR.
- The module is `0.x`, so breaking changes are acceptable later.
- The one constraint agreed: avoid exposing public API that is known to be removed immediately.
- On experimental features, a `WithExperimentalFeatures`-style flag was judged likely unhelpful; a possible `x` submodule to isolate experimental APIs was preferred, aligning with the OTel-wide push toward opt-in experimental features. That evaluation was pushed to the `1.40` milestone.

## Action items assigned

- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers** — review the OTelConf RC support PR.

## Current status caveat

Work State `WS-04: Release Process` (status `in_progress`, P1, owner Tyler Yahn with actions on Alex Boten / Nico Hertz, last updated 2025-11-27) records this as task `T001`, still **unchecked**. The decision is recorded, but **delivery is not established in the dataset**: the RC PR itself and Alex's tracking issue are not present in Sources, and the Done/Evidence section notes nothing established. The work-state index summarizes the item as "decision recorded; delivery not in Sources." No later human Comment (the 2026-03 corrections file) modifies WS-04 — those three comments all concern WS-03 and WS-05.

Note: the same meeting deferred a separate runtime-tracer/`pprof` profiling API proposal (`T002`, decided 2025-11-27) — do not merge the large public-API change without prior issue discussion; keep it as a draft PoC and start with a smaller disablement change. That is a distinct item from the OTelConf RC PR.

## Dataset records cited

- `work-states/WS-04-release-process.md` (`path = work-state`)
- `opentelemetry/meeting-notes/entry-3581463689.md` (`SRC-NOTE-07`, `path = sources`) — canonical URL: `https://github.com/open-telemetry/opentelemetry-go/issues/6648#issuecomment-3581463689`
- `work-states/comments/2026-03.md` (`path = comments`) — checked, no WS-04 corrections
