# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Decision

At the **OpenTelemetry Go SIG meeting on 2025-11-20** (notes posted 2025-11-26 by pellared), the SIG decided to **merge the OTelConf RC support PR as-is, pending only normal review** — rather than hold it for the additional changes Alex Boten had requested.

**Reasoning recorded in the meeting notes:**
- The next Go release was blocked on the RC support module; the PR simply needed reviews.
- Requested changes from Alex do **not** need to be in the current PR.
- The module is `0.x`, so breaking changes are acceptable later.
- The one caveat: avoid exposing public API that is known to be removed immediately.

**Paired decision on experimental API structure:** the SIG agreed to track the experimental-API-layout review separately under the **`1.40.0` milestone**. In discussion they concluded a `WithExperimentalFeatures`-style flag would likely be unhelpful, and favored a possible **`x` submodule** to clearly isolate experimental APIs — consistent with the OTel-wide push toward opt-in experimental features.

## Action items from that meeting

- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers** — review the OTelConf RC support PR.

## Current status (as of the registry)

`WS-04: Release Process` is **in_progress** (P1, owner Tyler Yahn as SIG lead, actions on Alex Boten / Nico Hertz; last updated 2025-11-27). Task `T001` remains **open**: the decision is recorded, but **delivery is not established in the dataset** — the RC PR itself and Alex's tracking issue are not present in the sources, and the Done/Evidence section notes nothing established. The Work State Index summarizes this line as "decision recorded; delivery not in Sources," and lists OTelConf RC / experimental API tracking among the active/open items.

Note that the release blockage is described as of 2025-11-20; the work state explicitly says the final merge/delivery outcome of that PR is not in the package. No later human Comments amend WS-04 (the 2026-03 corrections all target WS-03 and WS-05).

## Records used

- `work-states/WS-04-release-process.md` (`path = work-state`) — decisions, task list, active work, blockers, next update needed
- `opentelemetry/meeting-notes/entry-3581463689.md` (`SRC-NOTE-07`, `path = sources`) — Go SIG 2025-11-20 meeting note, discussion + decisions + action items
- `work-states/index.md` (`path = work-state-index`, navigation aid only) — as-of summary line
- `work-states/comments/2026-03.md` (`path = comments`) — checked; contains no corrections affecting WS-04
