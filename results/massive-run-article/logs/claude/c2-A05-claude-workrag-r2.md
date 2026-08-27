# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

I have the closing rationale directly from the record.

## Why PR #8014 was closed

**PR #8014** — "otelgin: remove unneeded context save/restore to avoid data race" (author: nicksherron, branch `fix/otelgin-data-race`, +83/−10 across 2 files) was **closed without merge on 2025-10-17**, because the OpenTelemetry Go SIG decided the existing context save/restore behavior is intentional and correct, and that the proposed fix was the wrong remedy.

**The closing statement.** dmathieu (Damien Mathieu), 2025-10-17T10:41:58Z, on the PR:

> "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one."

He pointed to a comment on issue #4588 for the fuller reasoning.

**The reasoning behind that decision.**

1. **The deferred restore has a real purpose.** dmathieu (2025-10-14): the `defer` removes the span from the request context so that spans created in a *parent* middleware after `c.Next()` are not children of the (already-finished) otelgin span. Dropping it silently changes span parentage.
2. **It would be a behavior change for long-standing semantics.** dmathieu noted this had been the default for years and the same behavior exists in other instrumentations such as otelecho. The author (nicksherron) conceded this was "a strong argument" and said he had not intended a breaking change, and would try to preserve semantics while fixing the race.
3. **The SIG's position on the race.** At the 2025-10-16 SIG meeting (Tyler Yahn, Damien Mathieu, Bryan Boreham, David Ashpole, Robert Pająk), Damien argued the current behavior is correct and that **users should explicitly pass the current context into spawned goroutines**, citing the Collector's pattern of passing context directly outside HTTP requests. Tyler Yahn agreed, adding that OpenTelemetry's pattern for async work is to *link* spans rather than make them children. The meeting produced an explicit action item for Damien to respond on #8014 recommending that approach — which is the 2025-10-17 closing comment.
4. **Not a case of no support.** The PR had one approving review (akats7, 2025-10-14) and flc1125 also came around to approving, framing the value as removing unnecessary code with unintended side effects rather than as a race fix. dmathieu had even asked for a CI regression test, which the author added. The synchronous SIG discussion overrode this.

**Aftermath / current state.** WS-05 (Contrib Modules) records this as task `T007`, status `closed_without_merge` — explicitly **not done**, and it remains an unchecked open item in the work-state index ("`#8014` closed without merge (not done)"). The underlying data race reported in issue #4588 (open ~2 years at the time) was not fixed by this route; the SIG's resolution is that users pass context explicitly into goroutines instead.

**Dataset records used:** `SRC-PR-07` (`opentelemetry/pulls/opentelemetry-go-contrib-8014.md`), `SRC-NOTE-04` (`opentelemetry/meeting-notes/entry-3479584781.md`, SIG 2025-10-16), `work-states/WS-05-contrib.md`, `work-states/index.md`.
