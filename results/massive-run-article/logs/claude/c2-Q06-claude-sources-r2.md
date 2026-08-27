# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — it has been released, in **opentelemetry-go v1.39.0**.

## Answer

**PR #7403** — "sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input" by **pellared** — was **merged into `main` on 2025-10-16** (19:07:08Z), carrying the **v1.39.0 milestone**. It fixed issue #7364, a concurrency bug where those three `Record` methods mutated their input parameters, causing race conditions when the same input data was used across goroutines. The fix adds defensive copying in `sdk/log/record.go`, with allocations occurring only when deduplication or limit-based truncation actually happens.

**Release v1.39.0** (tag `v1.39.0`, released as `v1.39.0/v0.61.0/v0.15.0/v0.0.14`) was **published 2025-12-08** by MrAlias. The fix appears in that release's changelog under **Fixed**:

> "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)"

It is also listed in the v1.39.0 "What's Changed" commit list, attributed to @pellared.

So the timeline is: opened 2025-09-23 → merged 2025-10-16 → shipped 2025-12-08 in v1.39.0.

## Notable context from the PR

- Approved by **dmathieu** (2025-09-26) and **dashpole** (2025-10-16); 12 reviews, 9 review comments.
- **MrAlias** pushed back on the initial implementation iterating `attrs` twice, calling it a regression and arguing for a single-pass algorithm from the start. pellared revised the approach on 2025-10-01, improving the deduplication benchmark from +67.92% to +14.71% overhead vs. base.
- pellared merged it himself, noting the SIG meeting consensus was to land it and address any remaining performance opportunities in follow-up PRs.
- The change also removed `sdk/log/race_on_test.go` and `race_off_test.go`, which were race-condition workarounds no longer needed. Coverage on `sdk/log/record.go` stayed at 100%.

## Sources

- `opentelemetry/pulls/opentelemetry-go-7403.md` — [SRC-PR-03], canonical URL https://github.com/open-telemetry/opentelemetry-go/pull/7403
- `opentelemetry/releases/release-v1.39.0.md` — [SRC-REL-01], canonical URL https://github.com/open-telemetry/opentelemetry-go/releases/tag/v1.39.0
