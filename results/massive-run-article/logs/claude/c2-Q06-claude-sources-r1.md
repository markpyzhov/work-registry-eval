# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — the fix has shipped.

## Answer

PR [open-telemetry/opentelemetry-go#7403](https://github.com/open-telemetry/opentelemetry-go/pull/7403), "sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input" (author: pellared), was **merged on 2025-10-16** and **released in v1.39.0 on 2025-12-08** (release "v1.39.0/v0.61.0/v0.15.0/v0.0.14", published by MrAlias).

## Supporting evidence

- **PR record [SRC-PR-03]** (`opentelemetry/pulls/opentelemetry-go-7403.md`): State `merged (2025-10-16T19:07:08Z)`, branch `fix-7364` → `main`, +722/-74 across 5 files, labels `pkg:SDK` / `area:logs`, and **Milestone: v1.39.0**. Fixes issue #7364. Approvals from dmathieu (2025-09-26) and dashpole (2025-10-16).
- **Release record [SRC-REL-01]** (`opentelemetry/releases/release-v1.39.0.md`, canonical URL `https://github.com/open-telemetry/opentelemetry-go/releases/tag/v1.39.0`, created 2025-12-08T16:32:32Z):
  - Changelog "Fixed" section contains: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)"
  - The "What's Changed" commit list also includes the PR by @pellared.

## What the fix does

It resolves a concurrency bug where those three `Record` methods mutated their input parameters, causing race conditions when the same input data was used concurrently across goroutines. The implementation adds defensive copying in `sdk/log/record.go`, allocating only when necessary (i.e., when deduplication occurs or data is truncated by limits). The previously needed `sdk/log/race_on_test.go` and `race_off_test.go` workaround files were removed.

One caveat worth noting: MrAlias raised a performance concern during review (deduplication-enabled benchmarks regressed, e.g. `AddAttributes/NestedDeduplication/Enabled` +80% after pellared's optimization pass). pellared merged anyway, citing SIG-meeting consensus, and invited follow-up PRs for further performance work. So the correctness fix is in v1.39.0, but performance follow-ups may exist beyond it.
