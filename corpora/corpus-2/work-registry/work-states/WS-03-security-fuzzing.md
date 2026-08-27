# WS-03: Security and Fuzzing
**Status**: in_progress
**Priority**: P1
**Owner**: pellared (Robert Pająk)
**Project**: opentelemetry-go / sig-security
**Last Updated**: 2026-03-11

## Sources
- `SRC-ISSUE-04` — [opentelemetry-go-7549.md](../opentelemetry/issues/opentelemetry-go-7549.md)
- `SRC-ISSUE-03` — [sig-security-164.md](../opentelemetry/issues/sig-security-164.md)
- `SRC-NOTE-06` — [entry-3479655348.md](../opentelemetry/meeting-notes/entry-3479655348.md)

## Applied Comments
- `CMT-2026-03-001` — [2026-03.md](comments/2026-03.md) — mailing-list + trial-monitoring completion.
- `CMT-2026-03-003` — [2026-03.md](comments/2026-03.md) — signature-release work deferred.

## Request / Context
Improve continuous-fuzzing visibility (OSS-Fuzz findings) and release-artifact signing / immutable-release practice for Go OpenTelemetry.

## Task List
- [x] `T001` (mapped to Issue `#7549`) — Go-maintainers mailing list and trial monitoring complete; public automatic GitHub issue filing remains deferred. `(SRC-ISSUE-04, SRC-NOTE-06, CMT-2026-03-001)`
- [ ] `T002` (mapped to Issue `#164`) — Immutable/signature-release enablement deferred pending release-tooling and asset-upload confirmation. `(SRC-ISSUE-03, SRC-NOTE-06, CMT-2026-03-003)`

## Active Work
- **`T001` / `#7549` external follow-up**: The Go-maintainers mailing list is live and trial monitoring is complete internally. The GitHub issue has not been updated, and automatic public issue filing remains deferred until triage matures. `(SRC-ISSUE-04, SRC-NOTE-06, CMT-2026-03-001)`
- **`T002` / `#164`**: Treat immutable/signature-release enablement as **deferred, not done**, until release tooling and asset-upload order are confirmed safe. The GitHub issue remains closed, but closure is not delivery completion. `(SRC-ISSUE-03, SRC-NOTE-06, CMT-2026-03-003)`

## Blockers and Dependencies
- **`T002`**: Release-tooling and asset-upload ordering must be confirmed safe before enablement. `(CMT-2026-03-003)`
- **Public OSS-Fuzz auto-filing**: remains deferred because findings may be security-sensitive. `(SRC-NOTE-06, CMT-2026-03-001)`

## Decisions and Superseded Directions
- **OSS-Fuzz public auto-filing (`T001`)**: On 2025-10-30 the SIG declined enabling automatic public GitHub issue filing for OSS-Fuzz findings because findings may be security-sensitive. Chosen path: maintainers mailing list + multi-month trial `(SRC-NOTE-06)`.
- **Signature-release walk-back (`T002`)**: The 2026-01-28 issue closure does not establish delivery. A private follow-up deferred enablement pending release-tooling confirmation. `(SRC-ISSUE-03, CMT-2026-03-003)`

## Done / Evidence
- `T001 / Issue #7549` — Go-maintainers mailing-list setup and trial monitoring are complete internally. Public automatic filing remains deferred and the GitHub issue may still appear open. `(CMT-2026-03-001)`
- Historical `T002 / Issue #164` record — opened 2025-08-27, moved toward immutable releases, and closed 2026-01-28. That closure is historical evidence, not the current delivery state; `T002` is deferred. `(SRC-ISSUE-03, SRC-NOTE-06, CMT-2026-03-003)`

## Needs Manual Triage
- None.

## Next Update Needed
- GitHub update for `#7549`; decision on public auto-filing after the completed trial; release-tooling confirmation and any later signed-release evidence for `#164`.
