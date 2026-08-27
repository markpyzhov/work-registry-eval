# Has the SDK log `Record` mutation fix in `opentelemetry-go` pull request `#7403` been released?

<!-- RESPONSE_START -->

Yes — it has been released.

## Answer

The `Record` mutation fix in `open-telemetry/opentelemetry-go#7403` shipped in **v1.39.0**, published **2025-12-08**.

**Chronology**
- PR #7403 ("sdk/log: Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` to not mutate input", author `pellared`, fixes issue #7364) was opened **2025-09-23** and assigned to milestone **v1.39.0** on 2025-09-25. It went through several draft/ready cycles, including a performance rework after `MrAlias` flagged a double-pass dedup algorithm, which `pellared` replaced with a single-pass version on 2025-10-01.
- Approved by `dmathieu` (2025-09-26) and `dashpole` (2025-10-16), and **merged 2025-10-16** by `pellared`.
- The v1.39.0 milestone is **closed** (335 closed / 0 open).
- Release **v1.39.0** (tag `v1.39.0`, released as v1.39.0/v0.61.0/v0.15.0/v0.0.14 by `MrAlias`) was published **2025-12-08T16:45:46Z**, and its **Fixed** section contains the exact entry: "Fix `AddAttributes`, `SetAttributes`, `SetBody` on `Record` in `go.opentelemetry.io/otel/sdk/log` to not mutate input. (#7403)".

The Work State tracking this is **WS-01: SDK Logs**, status **completed**, owner `pellared`, last updated 2025-12-08, with its single task `T001` (mapped to PR #7403) marked done and evidenced as "Released in `v1.39.0` on 2025-12-08".

**Sources**
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-01-sdk-logs.md` (authoritative status)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/pulls/opentelemetry-go-7403.md` (SRC-PR-03 — PR history, merge)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01 — changelog entry, publish date)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13145551.md` (SRC-MILE-02 — v1.39.0 milestone closed)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479584781.md` (SRC-NOTE-04 — SIG review discussion)
