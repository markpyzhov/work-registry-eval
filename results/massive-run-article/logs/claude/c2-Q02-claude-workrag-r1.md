# What did the Go SIG decide to do with Nico’s large runtime-tracer / profiling public-API proposal?

<!-- RESPONSE_START -->

## Answer

The Go SIG **deferred the large public-API change and told Nico to break it into an issue plus a much smaller PR** — it was not merged.

### The proposal (SIG meeting of 2025-11-27)
Nico Hertz brought a PR for Go runtime profiling (`pprof`) integration. The problem: every span currently creates a runtime tracing **task**, which adds noise to profiles. His proposal added public API control over task/region creation:
- **Default** — task only for the root span
- **Auto** — task for root span, regions for child spans
- **Manual** — explicit task/region instrumentation by the user
- Plus an optional async-style hint for spans that cross goroutines

### The SIG's concerns
- Tasks can span multiple goroutines, but regions must stay within one goroutine.
- Changing public tracing APIs is sensitive and tightly coupled to the OTel specification.
- Risk of breaking existing instrumentation (Kafka libraries were named as an example).

### The decision
- **Do not merge large public API changes without prior issue discussion.**
- **Keep the current large PR as a draft / proof of concept.**
- **Proceed incrementally** — start with a small change, e.g. the ability to disable the runtime tracer integration entirely.
- **Open an issue documenting the profiling proposal** (modes, semantics, trade-offs) before continuing with API changes.

### Action items assigned to Nico Hertz
1. Open an issue describing the runtime profiling problem and proposal.
2. Create a smaller PR allowing the runtime tracer integration to be disabled.
3. (Separately) explore flaky test issues in `contrib`.

Maintainers also committed to onboarding support (a buddy / help via Slack) for new contributors.

### Current status
Tracked as `WS-04 / T002` (Release Process workstream, `in_progress`, P1). The item is **deferred pending the issue + smaller PR**, and the large runtime-profiling API change is listed among the workstream's blocked/deferred items. The Sources do **not** establish that either follow-up (the issue or the smaller disablement PR) was actually filed — that is explicitly what the work state flags as the next update needed. No later Comment revises this.

### Records cited
- `work-states/WS-04-release-process.md` (`path = work-state`) — Task List `T002`, Active Work, Decisions and Superseded Directions, Next Update Needed
- `opentelemetry/meeting-notes/entry-3974113940.md` — `SRC-NOTE-08`, Go SIG note dated 2025-11-27 (comment `#issuecomment-3974113940` on `opentelemetry-go#6648`), author pellared
- `work-states/index.md` (`path = work-state-index`, navigation only) — corroborates "deferred pending issue + smaller PR"

One dating quirk worth flagging: the source note carries a meeting **Date of 2025-11-27** but its GitHub comment was created **2026-02-27**. I used the meeting date, consistent with how the work state records the decision.
