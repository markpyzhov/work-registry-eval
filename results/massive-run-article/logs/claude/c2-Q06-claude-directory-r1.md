# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — it has been released.

**Answer: Released in `v1.39.0` on 2025-12-08.**

Details:

- **PR #7403** ("sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input") was opened 2025-09-23 by `pellared` (Robert Pająk), fixing issue #7364. It was assigned to the `v1.39.0` milestone on 2025-09-25, approved by `dmathieu` and `dashpole`, and merged 2025-10-16T19:07:08Z. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7403.md`
- The `v1.39.0` release (tag `v1.39.0`, published 2025-12-08) lists the change in its Fixed section: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)". `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md`
- The authoritative work state marks the item complete: WS-01 SDK Logs, status `completed`, task `T001` mapped to PR #7403, with evidence "Released in `v1.39.0` on 2025-12-08". `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-01-sdk-logs.md`

Supporting context: during review `MrAlias` flagged a double-iteration inefficiency in the dedup path; `pellared` reworked it to a single pass (2025-10-01) and re-ran benchstat before merge. The SIG meeting note (2025-10-16) records that Tyler encouraged other reviewers and David Ashpole offered to review, after which `dashpole` approved and `pellared` merged the same day. `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md`
