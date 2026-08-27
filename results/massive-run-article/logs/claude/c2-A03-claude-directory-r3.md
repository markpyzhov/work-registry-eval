# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

Both parts are answered.

**Which release confirmed immutable releases working**

`v1.39.0` — on 2025-12-11, pellared confirmed in the issue: "I can confirm that it worked for Go (opentelemetry-go releases/tag/v1.39.0) and Go Contrib (opentelemetry-go-contrib releases/tag/v1.39.0)." The enabling prep was PR `opentelemetry-go#7567` (merged), after which both repos were ready. He also noted the GitHub feature reached GA on 2025-10-28 and proposed adding it to sig-security's `docs/recommendations.md`.
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/sig-security-164.md` (SRC-ISSUE-03)

**Current status of the broader work (`sig-security#164`)**

Authoritative Work State `WS-03` task `T002` is **deferred, not done** (WS-03 overall: in_progress, P1, owner pellared):

- The GitHub issue was renamed "Recommend immutable releases" (2026-01-07 by trask) and **closed by reyang on 2026-01-28**, but that closure is treated as historical evidence, **not delivery completion**.
- On 2026-03-11, after a private follow-up with Trask, pellared walked the item back: enabling immutable/signature releases for the Go repos is **deferred until release tooling and asset-upload ordering are confirmed safe**. The GitHub issue was deliberately left closed and not reopened.
- Blocker: release-tooling and asset-upload order confirmation. This traces to the SIG Security constraint that artifacts must be uploaded at release time and cannot be regenerated later (also flagged in-issue as a CAUTION: assets cannot be added/edited/removed after publication).
- Next update needed: release-tooling confirmation and any later signed-release evidence for `#164`.

Files:
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-03-security-fuzzing.md`
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md` (CMT-2026-03-003)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (row: `sig-security#164` — deferred pending release-tooling confirmation; GitHub issue still closed)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3479655348.md` (SRC-NOTE-06 — SIG Security release-signing decision and the upload-at-release-time constraint)
