# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

The Go SIG's decision on the OTelConf RC support PR:

**Decision (SIG meeting 2025-11-20, notes posted 2025-11-26):** Merge the OTelConf RC support PR **as-is**, pending normal review. The change requests Alex Boten had raised do **not** need to be addressed in that PR — since the module is `0.x`, breaking changes are acceptable later. Separately, the SIG decided to **track the experimental API structure question (e.g. an `x` submodule to isolate experimental APIs) under the `1.40.0` milestone**, rather than let it hold up the release. A related principle was agreed: avoid exposing public API that is known to be removed immediately, and a `WithExperimentalFeatures`-style flag was judged likely unhelpful.

**Why it mattered:** the next Go release was described as blocked on the RC support module, which simply needed reviews.

**Action items assigned:**
- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module and add it to the `1.40` milestone.
- **SIG reviewers** — review the OTelConf RC support PR.

**Status caveat:** the package records the decision but not the delivery. The RC PR itself, its merge event, and Alex's tracking issue are not present in the frozen Sources, so the final outcome cannot be confirmed from this material. WS-04 remains `in_progress` with `T001` unchecked.

Files supporting these claims:
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (SRC-NOTE-07 — the meeting note with the decision and action items)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` (authoritative Work State: `T001`, blockers, decisions, "Done / Evidence: None established")
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (coverage row: "OTelConf RC / experimental API (SIG topic) — decision recorded; delivery not in Sources")

Note: this is distinct from the contrib `otelconf` `OTEL_EXPERIMENTAL_CONFIG_FILE` work tracked in `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (issue `#8059`, PR `#8106`), which was a different SIG topic and not the release blocker.
