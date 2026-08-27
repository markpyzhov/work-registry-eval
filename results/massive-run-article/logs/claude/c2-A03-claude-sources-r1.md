# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

**Answer**

**Which release confirmed it:** `v1.39.0`. On 2025-12-11, pellared commented on open-telemetry/sig-security#164: "I can confirm that it worked for Go (opentelemetry-go/releases/tag/v1.39.0) and Go Contrib (opentelemetry-go-contrib/releases/tag/v1.39.0)." The OTel Go v1.39.0 release was published 2025-12-08.

**How it got there:**
- 2025-09-16 / 09-17 — pellared trialed GitHub immutable releases on side projects (goyek/goyek v2.3.0, golang-templates/seed v0.22.0), verifying with `gh release verify` / `verify-asset`. Key caveat flagged: assets cannot be added/edited/removed after publish, so each repo's release process must be checked before enabling; also `gh release verify` cannot verify the auto-generated source zip/tarball.
- 2025-10-23 / 10-27 — trask asked whether the release attestation replaces per-artifact attestation (sig-security#79); pellared: "I think it can replace it."
- 2025-11-03 — pellared prepared OTel Go via opentelemetry-go PR #7567 (merged), making both opentelemetry-go and opentelemetry-go-contrib ready to enable the feature. A terraform-provider-github limitation (issue #2746) was raised; trask said on 2025-11-07 it need not block, pointing to open-telemetry/admin PR #346.
- The Go SIG meeting of 2025-10-30 recorded the decision to proceed with GitHub signature/immutable releases, update releasing docs, and ensure artifacts are uploaded at release time, with Robert (pellared) as owner, referencing sig-security#164.

**Current status of sig-security#164:** Closed as completed. The feature went GA on 2025-10-28, and the issue's scope shifted from enabling to recommending: on 2026-01-07 trask renamed it from "Enable immutable releases where possible" to "Recommend immutable releases," and pellared took assignment, proposing that GitHub Immutable Releases be added to sig-security's `docs/recommendations.md`. That landed via sig-security PR #219 (cross-referenced 2026-01-28), and the issue was closed by reyang on 2026-01-28T22:16:50Z. Along the way it was also cross-referenced from opentelemetry-dotnet PR #6646 and issue #6748, and opentelemetry-ebpf-instrumentation issue #13, indicating uptake beyond Go.

**Sources cited (all `path: sources` in dataset 74f29ea88a9c11f197db2303d7337e37):**
- `opentelemetry/issues/sig-security-164.md` — [SRC-ISSUE-03], "Recommend immutable releases" (open-telemetry/sig-security#164)
- `opentelemetry/meeting-notes/entry-3479655348.md` — [SRC-NOTE-06], OTel Go SIG 2025-10-30 (SIG Security: release signing; action items)
- `opentelemetry/releases/release-v1.39.0.md` — OTel Go v1.39.0 release record (published 2025-12-08)
