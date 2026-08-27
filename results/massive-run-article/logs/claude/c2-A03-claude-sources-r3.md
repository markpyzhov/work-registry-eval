# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

**Release that confirmed it: v1.39.0**

On 2025-12-11, pellared reported in `open-telemetry/sig-security#164`: "I can confirm that it worked for Go (opentelemetry-go/releases/tag/v1.39.0) and Go Contrib (opentelemetry-go-contrib/releases/tag/v1.39.0)."

**Path to that confirmation**
- 2025-09-16 / 2025-09-17 — pellared trialed GitHub immutable releases on side projects (goyek/goyek v2.3.0, golang-templates/seed v0.22.0), verifying with `gh release verify` / `gh release verify-asset`. He flagged a caution: assets cannot be added/edited/removed after publish, so each repo's release process must be checked before enabling; also `gh release verify` cannot verify the auto-generated source zip/tarball.
- 2025-10-23 / 2025-10-27 — trask asked whether the release attestation JSON replaces per-artifact attestation (sig-security#79); pellared: "I think it can replace it."
- 2025-10-30 Go SIG meeting — decision to proceed with enabling signature/immutable releases for OTel Go, update release docs, ensure artifacts are uploaded at release time; assigned to Robert Pająk, referencing sig-security#164.
- 2025-11-03 — opentelemetry-go PR #7567 merged to prepare OTel Go; pellared declared both opentelemetry-go and opentelemetry-go-contrib ready. A terraform-provider-github limitation (integrations/terraform-provider-github#2746) was raised; trask said it need not block, pointing to open-telemetry/admin#346.
- 2025-12-11 — confirmation for Go and Go Contrib at v1.39.0.

**Current status of sig-security#164: closed (completed)**
- The GitHub feature went GA on 2025-10-28, after which pellared proposed adding GitHub Immutable Releases to `sig-security/docs/recommendations.md`.
- 2026-01-07 — trask renamed the issue from "Enable immutable releases where possible" to "Recommend immutable releases"; pellared took the assignment.
- 2026-01-28 — cross-referenced by sig-security PR #219 (the recommendations change), and the issue was closed the same day by reyang. Last updated 2026-01-28T22:16:50Z.
- Other cross-references in the timeline show the effort spread beyond Go: opentelemetry-dotnet PR #6646 and issue #6748, opentelemetry-ebpf-instrumentation issue #13.

So the narrower "enable it in Go repos" goal landed at v1.39.0, and the broader issue was reframed as an org-wide recommendation and closed as completed once that recommendation was merged.

**Sources cited**
- `opentelemetry/issues/sig-security-164.md` (SRC-ISSUE-03) — Issue: Recommend immutable releases, open-telemetry/sig-security#164
- `opentelemetry/meeting-notes/entry-3479655348.md` (SRC-NOTE-06) — OpenTelemetry Go SIG meeting notes, 2025-10-30
