# Which release confirmed immutable releases working for Go and Go Contrib, and what is the current status of the broader work in `sig-security#164`?

<!-- RESPONSE_START -->

Immutable releases were confirmed working in **v1.39.0** for both OTel Go and OTel Go Contrib. `[SRC-ISSUE-03]`

The broader `sig-security#164` work is **in progress overall**, but its immutable/signature-release enablement task (`T002`) is **deferred—not done**. It awaits confirmation that release tooling and artifact-upload ordering are safe; the GitHub issue’s closure is historical, not proof of delivery. `[WS-03, T002; CMT-2026-03-003]`
