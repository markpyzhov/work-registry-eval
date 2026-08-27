# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## The decision

At the OpenTelemetry Go SIG meeting on **2025-11-20**, the SIG decided to **merge the OTelConf RC support PR as-is, pending normal review** — the requested changes from Alex Boten do *not* need to land in that PR. Review of the experimental API structure was split out and tracked separately under the **`1.40.0` milestone**.

Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (SRC-NOTE-07, posted by pellared as a comment on `opentelemetry-go#6648`), and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md`.

## Reasoning recorded in the discussion

- The next Go release was blocked on the RC support module; the PR simply needed reviews.
- The module is `0.x`, so breaking changes are acceptable later — no need to perfect the API now.
- Caveat agreed: avoid exposing public API that is known to be removed immediately.
- On experimental features, a `WithExperimentalFeatures`-style flag was judged likely unhelpful; a dedicated **`x` submodule** to isolate experimental APIs was floated as the better option, aligning with the OTel-wide push for opt-in experimental features.

(`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md`, section 1 and Decisions)

## Assigned follow-ups

- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module, and add it to the `1.40` milestone.
- **SIG reviewers** — review the OTelConf RC support PR.

(same file, Action Items)

## Current status caveat

Per the authoritative Work State (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md`), task `T001` is still **open / in_progress**: the decision is recorded, but the package's frozen Sources contain **neither the RC support PR itself nor Alex's tracking issue**, so the actual merge and delivery are not established. The index concurs: "OTelConf RC / experimental API (SIG topic) — decision recorded; delivery not in Sources" (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md`). No `CMT-*` correction in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` touches WS-04.

Note: this is distinct from the other otelconf thread — `opentelemetry-go-contrib#8059` (`OTEL_EXPERIMENTAL_CONFIG_FILE` support), where the 2025-10-23 SIG rejected short-term SDK-level support in favor of a contrib `otelconf` prototype (`/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md`).
