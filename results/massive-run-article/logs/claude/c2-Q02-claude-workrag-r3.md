# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## What the Go SIG decided

The SIG **deferred the large public-API change and told Nico to break it up**, rather than merging it.

**The proposal (Nico Hertz's PR)** — Go runtime tracer / `pprof` profiling integration. Today every span creates a runtime tracing *task*, which adds noise to profiles. Nico proposed more control over task/region creation via modes:
- **Default**: task only for the root span
- **Auto**: task for the root span, regions for child spans
- **Manual**: explicit task/region instrumentation by the user
- Plus an optional async-style hint for spans crossing goroutines

**Concerns raised** — tasks can cross goroutines while regions must stay on one goroutine; changing public tracing APIs is sensitive and tightly coupled to the specification; risk of breaking existing instrumentation (e.g. Kafka libraries).

**Decision (SIG meeting of 2025-11-27, notes published 2026-02-27):**
- Do **not** merge large public API changes without prior issue discussion.
- Keep the existing large PR as a **draft / proof of concept**.
- Proceed **incrementally**, starting with a small change: the ability to **disable** the runtime tracer integration.
- Open an issue documenting the profiling proposal (modes, semantics, trade-offs) before continuing with API changes.

**Action items on Nico Hertz:** open the issue describing the problem and proposal; create the smaller PR allowing runtime-tracer integration to be disabled; also explore flaky test issues in `contrib`. Maintainers were to provide onboarding support (buddy / Slack help) for new contributors.

**Current status:** the item is tracked as WS-04 (Release Process), task `T002`, owner context Tyler Yahn with actions on Nico Hertz. State as of the registry: **deferred pending the issue plus the smaller PR** — the dataset does not establish that either follow-up was actually filed, and no later comment revises this.

**Records used:** `work-states/WS-04-release-process.md` (work-state); `opentelemetry/meeting-notes/entry-3974113940.md` (SRC-NOTE-08, sources); `work-states/index.md` (navigation only). No `CMT-*` entries in `work-states/comments/2026-03.md` touch WS-04/T002.
