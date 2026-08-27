# What did the Go SIG decide about the OTelConf RC support PR that was blocking the next release?

<!-- RESPONSE_START -->

## What the Go SIG decided about the OTelConf RC support PR

At the OpenTelemetry Go SIG meeting on **2025-11-20** (notes posted 2025-11-26 by pellared, `SRC-NOTE-07`), the SIG decided to **merge the OTelConf RC support PR as-is, pending normal review** — i.e. no rework was required before merge, and the PR was to be unblocked by reviews rather than by additional changes.

Supporting rationale recorded in the discussion:
- The next Go release was **blocked on the RC support module**; the PR simply **needed reviews**.
- **Requested changes from Alex (Boten) do not need to be in the current PR** — they can come later.
- The module is **`0.x`**, so **breaking changes are acceptable later**.
- Caveat: **avoid exposing public API known to be removed immediately**.

On the related experimental-API question, the SIG decided to **track the experimental API structure review under the `1.40.0` milestone**. Options discussed: a `WithExperimentalFeatures`-style flag (judged likely unhelpful) versus a dedicated **`x` submodule** to isolate experimental APIs, which aligns with the OTel-wide push for opt-in experimental features.

### Action items from that decision
- **Alex Boten** — open an issue tracking evaluation of the experimental API structure for the OTelConf RC module, and add it to the **`1.40` milestone**.
- **SIG reviewers** — review the OTelConf RC support PR.

### Status / limits of the evidence
Per the authoritative Work State (`WS-04-release-process`, in_progress, owner Tyler Yahn with actions on Alex Boten / Nico Hertz), task `T001` is still **open**: the package contains the decision but **not the RC PR itself, its merge event, or Alex's tracking issue**. The work-state index likewise records the OTelConf RC / experimental API item as "decision recorded; delivery not in Sources," and lists it under active/open blockers. The `v1.40.0` milestones for both `opentelemetry-go` and `opentelemetry-go-contrib` are recorded as closed (120 and 169 closed issues respectively), but neither milestone record ties back to the RC PR.

Note: this is a distinct item from the contrib `otelconf` `OTEL_EXPERIMENTAL_CONFIG_FILE` work (`#8059`, WS-05), which was a separate 2025-10-23 decision to prototype in contrib rather than in the SDK.

### Files cited
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (SRC-NOTE-07 — the decision, discussion, and action items)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` (authoritative current status of `T001`)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (item coverage and open-blocker listing)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-14282228.md` (v1.40.0 milestones)
- `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` and `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8059.md` (the separate contrib `otelconf` item, for disambiguation)
