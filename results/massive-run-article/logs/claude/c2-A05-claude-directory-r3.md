# Why was `opentelemetry-go-contrib` pull request `#8014` (otelgin context save/restore) closed?

<!-- RESPONSE_START -->

PR #8014 was **closed without merge on 2025-10-17 by dmathieu (Damien Mathieu)**, after the OpenTelemetry Go SIG decided the fix was incorrect and that the existing context save/restore behavior is the intended one.

## What the PR proposed

`nicksherron` opened it 2025-10-14 (branch `fix/otelgin-data-race`, +83/−10 across 2 files), arguing the deferred `c.Request = c.Request.WithContext(savedCtx)` in otelgin's middleware served no purpose and caused a real data race: after `c.Next()` returns, the deferred write to `c.Request` races with goroutines spawned by downstream handlers that read `c.Request.Context()`. He tied it to the two-year-old issue #4588 and argued the removal was also a small performance win.

## How the review turned

- `flc1125` initially objected that the change did not provide thread safety and that concurrency safety should be left to users; after further discussion he changed position and **approved conceptually**, reframing the value as "removes unnecessary code with unintended side effects" rather than "fixes a data race."
- `akats7` **formally approved** the PR on 2025-10-14.
- `dmathieu` then identified the actual purpose of the defer: it removes the span from the context so that spans created in *parent* middleware after their `c.Next()` call do not become children of the finished otelgin span. He noted this has been the default behavior for years and matches other instrumentations such as otelecho, so the defer could not simply be dropped. He asked the author to bring the discussion to the SIG meeting.
- The author conceded this was a strong point and said he would look for a fix preserving the existing semantics; no such revision landed.

## The closing decision

At the Go SIG meeting of **2025-10-16**, Damien Mathieu presented the problem and stated the current behavior is correct — users should explicitly pass the current context into spawned goroutines (citing the collector's pattern of passing context directly outside HTTP requests). **Tyler Yahn agreed**, adding that OpenTelemetry's pattern for asynchronous operations is to *link* spans rather than make them child references. Damien's action item from that meeting was to respond on #8014 accordingly.

The next day, 2025-10-17T10:41:58Z, dmathieu commented "We have been discussing this in yesterday's SIG meeting, and have decided this fix is incorrect and the current behavior is the proper one," pointing at issue #4588, and closed the PR. The timeline records a `closed` event with no merge event.

## Registry status

Tracked as task `T007` in the WS-05 work state, marked **`closed_without_merge`** and left unchecked (not done). One open triage item remains: whether any in-tree follow-up replaced #8014.

## Sources

- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-contrib-8014.md` (SRC-PR-07) — PR body, full 27-comment discussion, approval, closing comment and timeline
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04) — 2025-10-16 Go SIG meeting notes and action items
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` — task `T007` status and the recorded decision
