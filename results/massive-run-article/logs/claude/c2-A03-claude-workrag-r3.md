# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

## The confirming release

**v1.39.0** — pellared (Robert Pająk) commented on **2025-12-11T17:43:19Z** in `sig-security#164` that immutable releases worked for both:
- `opentelemetry-go` v1.39.0
- `opentelemetry-go-contrib` v1.39.0

Source: `SRC-ISSUE-03` — `opentelemetry/issues/sig-security-164.md` (path = sources).

## Current status of the broader work

The authoritative Work State is **WS-03: Security and Fuzzing** (`work-states/WS-03-security-fuzzing.md`, path = work-state), status **in_progress**, priority P1, owner pellared, last updated **2026-03-11**.

Within it, `sig-security#164` is tracked as task **`T002`**, and its current state is **deferred, not done**:

- The GitHub issue is closed (closed 2026-01-28, state "closed (completed)"), but **closure is explicitly not treated as delivery completion**. That record is held as historical evidence only.
- Immutable / signature-release enablement for the Go repos is deferred **until the release tooling and asset-upload order are confirmed safe** — this is the recorded blocker.
- The reason is a documented walk-back: **`CMT-2026-03-003`** (effective 2026-03-11, author pellared) records that after a private follow-up with trask, the team walked back treating `#164` as done. The GitHub issue was deliberately left closed and not reopened.
- Task List shows `T002` unchecked; `T001` (OSS-Fuzz / Go-maintainers mailing list, issue `#7549`) is checked complete internally, though public auto-filing of OSS-Fuzz findings remains deferred because findings may be security-sensitive.
- **Next update needed** for `#164`: release-tooling confirmation and any later signed-release evidence.

Note the tension worth flagging: the source-level confirmation that immutable releases worked on v1.39.0 (2025-12-11) predates the 2026-03-11 correction, and the Work State still classifies the broader enablement as deferred. The v1.39.0 confirmation is a successful trial data point, not delivery of the work item.

### Records cited
- `work-states/WS-03-security-fuzzing.md` (work-state) — Task List, Active Work, Blockers, Decisions, Done/Evidence, Next Update Needed
- `work-states/comments/2026-03.md` (comments) — `CMT-2026-03-003`
- `opentelemetry/issues/sig-security-164.md` (sources, `SRC-ISSUE-03`)
- `opentelemetry/meeting-notes/entry-3479655348.md` (sources, `SRC-NOTE-06`)
