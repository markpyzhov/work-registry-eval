# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — it shipped in opentelemetry-go v1.39.0.

**Answer**

PR #7403 ("sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input", author pellared) was merged into `main` on 2025-10-16T19:07:08Z against milestone v1.39.0, and that milestone has since been released.

Evidence chain:
- **PR record** — state `merged (2025-10-16T19:07:08Z)`, branch `fix-7364` → `main`, labels `pkg:SDK`, `area:logs`, milestone **v1.39.0**. It fixes issue #7364, a concurrency/race bug where those three `Record` methods mutated their input parameters; the fix adds defensive copying (allocating only when deduplication or limit-truncation actually occurs) in `sdk/log/record.go`, plus tests, and deletes the `race_on_test.go` / `race_off_test.go` workarounds. Source: `opentelemetry/pulls/opentelemetry-go-7403.md` [SRC-PR-03].
- **Release record** — Release `v1.39.0` (Release v1.39.0/v0.61.0/v0.15.0/v0.0.14), tag `v1.39.0`, authored by MrAlias, **published 2025-12-08T16:45:46Z**. Its "What's Changed" list includes the PR by name and URL, and its changelog "Fixed" section states: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)". Source: `opentelemetry/releases/release-v1.39.0.md` [SRC-REL-01].

Supporting context: the 2025-10-16 OpenTelemetry Go SIG meeting note records the review push on this PR ahead of a pre-KubeCon release (`opentelemetry/meeting-notes/entry-3479584781.md` [SRC-NOTE-04]).

One caveat worth noting: reviewer MrAlias raised a performance concern about the deduplication path iterating `attrs` twice; pellared reworked it and merged, with the agreement that any further optimization would come in a follow-up PR. So the correctness fix is released, but the performance follow-up is not part of #7403.
