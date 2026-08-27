# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

I have everything needed.

## Answer

**Release that confirmed immutable releases working: v1.39.0**

On 2025-12-11, pellared (Robert Pająk) commented on `sig-security#164`: he confirmed it worked for **opentelemetry-go v1.39.0** and **opentelemetry-go-contrib v1.39.0** (release tags `v1.39.0` in both repos). In the same comment he noted the GitHub feature had gone GA (2025-10-28 changelog) and proposed adding GitHub Immutable Releases to the SIG Security `docs/recommendations.md`.

Preparation for that was PR `opentelemetry-go#7567` (merged), announced on 2025-11-03 as making both Go and Go Contrib ready for enabling immutable releases.

Source: `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/sig-security-164.md` (`SRC-ISSUE-03`)

**Current status of the broader work**

The authoritative Work State is `WS-03: Security and Fuzzing` — status **in_progress**, P1, owner pellared, last updated 2026-03-11.

The `#164` work is tracked as task `T002` and is **deferred, not done**:

- The GitHub issue itself is **closed (completed)** — renamed by trask on 2026-01-07 from "Enable immutable releases where possible" to "Recommend immutable releases", cross-referenced to `sig-security#219`, and closed by reyang on 2026-01-28.
- However, per `CMT-2026-03-003` (pellared, effective 2026-03-11), after a private follow-up with trask the team **walked back** treating `#164` as done. Enabling immutable/signature releases for the Go repos is deferred until **release tooling and asset-upload ordering are confirmed safe**. The GitHub issue was deliberately left closed and was not reopened; the closure is historical evidence, not delivery completion.
- Blocker: release-tooling and asset-upload order confirmation. This traces back to the constraint raised in the issue and the SIG meeting — assets cannot be added/edited/removed after an immutable release is published, so artifacts must be uploaded at release time.
- Next update needed: release-tooling confirmation and any later signed-release evidence for `#164`.

The sibling task `T001` (`opentelemetry-go#7549`, OSS-Fuzz notifications) is complete internally — Go-maintainers mailing list live and trial monitoring finished — but public automatic GitHub issue filing remains deferred because findings may be security-sensitive, and the GitHub issue has not been updated.

Supporting files:
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-03-security-fuzzing.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` (`CMT-2026-03-001`, `CMT-2026-03-003`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/sig-security-164.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md` (`SRC-NOTE-06` — SIG decision to proceed with signature releases, plus the upload-at-release-time constraint)
