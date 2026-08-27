# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Decision: deferred, not merged — take an incremental path instead

The Go SIG declined to merge Nico Hertz's large runtime-tracer / `pprof` profiling public-API change and redirected it to a smaller first step.

**What the proposal was** (SRC-NOTE-08, SIG meeting dated 2025-11-27):
- Today every span creates a Go runtime tracing **task**, which adds noise to profiles.
- Nico's PR proposed more control over task/region creation via modes: **Default** (task only for the root span), **Auto** (task for root span, regions for child spans), **Manual** (explicit user instrumentation), plus an optional async-style hint for spans crossing goroutines.

**Why the SIG held back:**
- Changing public tracing APIs is sensitive and tightly coupled to the OTel specification.
- Risk of breaking existing instrumentation (Kafka libraries cited as an example).
- Tasks can span multiple goroutines while regions must stay within one — a semantics constraint needing wider discussion.

**The decisions recorded:**
- Do **not** merge large public API changes without prior issue discussion.
- Keep the existing large PR as a **draft / proof of concept**.
- Proceed incrementally, starting with a small change: the ability to **disable** the runtime tracer integration.
- Open an issue documenting the profiling proposal (modes, semantics, trade-offs) before continuing with API changes.

**Action items assigned to Nico Hertz:** open the issue describing the problem and proposal; create the smaller disablement PR; (separately) explore flaky test issues in `contrib`. Maintainers were also asked to provide onboarding/buddy support via Slack for new contributors.

**Current status:** The authoritative Work State (WS-04 Release Process, `T002`, status `in_progress`, last updated 2025-11-27) records the item as still open — "deferred pending issue + smaller PR." The dataset does not establish that either follow-up (the issue or the smaller PR) was actually filed; WS-04's "Next Update Needed" explicitly lists Nico's issue and smaller disablement PR as what's still awaited. The Work State index likewise lists the large runtime-profiling API change under "Blocked / deferred." No later Comments (`path = comments`, through 2026-03-11) modify this item.

**Records cited:** `work-states/WS-04-release-process.md` (work-state); `opentelemetry/meeting-notes/entry-3974113940.md` (SRC-NOTE-08, sources); `work-states/index.md` (navigation only).
