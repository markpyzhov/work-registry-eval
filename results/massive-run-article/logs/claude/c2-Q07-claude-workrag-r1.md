# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## Decision

At the OpenTelemetry Go SIG meeting on **2025-11-20** (notes posted 2025-11-26 by pellared), the SIG decided to:

1. **Merge the OTelConf RC support PR as-is**, pending only normal review — it did not need to absorb Alex Boten's requested changes first.
2. **Track the experimental API structure review separately** (e.g. an `x` submodule to isolate experimental APIs) under the **`1.40.0` milestone**.

## Reasoning given in the meeting

- The next Go release was blocked on the RC support module; the PR simply needed reviews.
- The module is `0.x`, so breaking changes are acceptable later — no need to get it perfect now.
- Caveat agreed: avoid exposing public API that is known to be removed immediately.
- On experimental features, a `WithExperimentalFeatures`-style flag was judged likely unhelpful; a dedicated `x` submodule was preferred, aligning with the OTel-wide push toward opt-in experimental features.

## Action items assigned

- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers** — review the OTelConf RC support PR.

## Current status caveat

The work state (`WS-04: Release Process`, status `in_progress`, P1, last updated 2025-11-27) records this decision but notes the **outcome is not established in the dataset**: the RC PR itself and Alex's tracking issue are not in the source package, and "Done / Evidence" is empty. As of 2025-11-20 the release was still described as blocked on RC support module review. No later human comments amend WS-04 (the 2026-03 comments only touch WS-03 and WS-05).

## Records cited

- `/opentelemetry/meeting-notes/entry-3581463689.md` — SRC-NOTE-07, Go SIG note for 2025-11-20 (Discussions §1, Decisions, Action Items)
- `/work-states/WS-04-release-process.md` — T001 task, Decisions, Active Work, Blockers, Next Update Needed
- `/work-states/comments/2026-03.md` — checked; contains no correction to WS-04
