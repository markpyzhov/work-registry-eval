# Did the OTelConf RC support PR that the SIG agreed to merge actually ship in a release?

<!-- RESPONSE_START -->

## Answer: No — and the package cannot show that it did

The SIG did agree to merge it, but nothing in this project package establishes that the OTelConf RC support PR was merged, let alone that it landed in a release.

**The decision (2025-11-20 SIG call)**
- "Merge OTelConf RC support PR as-is (pending normal review)" and track the experimental API structure (possible `x` submodule) under the `1.40.0` milestone. The next Go release was described as *blocked* on the RC support module, whose PR still needed reviews. Action items: Alex Boten to open a tracking issue for the experimental API structure (add to `1.40` milestone), and SIG reviewers to review the RC support PR — both recorded unchecked.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/meeting-notes/entry-3581463689.md` (SRC-NOTE-07, lines 26–30, 87–88, 94–95)

**The authoritative current state**
- `T001` (OTelConf RC / experimental API) is still an **unchecked** task; "Sources do not include that issue or the RC PR itself"; "Final merge/delivery of that PR is not in the package"; Done/Evidence is explicitly "None established in the frozen Sources"; and the Next Update Needed line names "Presence of the OTelConf RC PR outcome" as the missing piece. WS-04 status is `in_progress`, last updated 2025-11-27.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-04-release-process.md` (lines 16, 20, 24, 31, 37)
- The index summarizes the item as "OTelConf RC / experimental API (SIG topic) — Release Process — **decision recorded; delivery not in Sources**", and lists it among active/open items.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (lines 16, 30, 41)
- The registry's final Work State runs through 2026-03-11 (source cutoff 2026-02-27), so this gap is not just a stale snapshot — no later correction changed it. The 2026-03 comments file contains corrections for WS-03 and WS-05 only, none touching WS-04.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/comments/2026-03.md`

**Release evidence checked**
- The only release Source in the package is opentelemetry-go `v1.39.0` (published 2025-12-08). Its Added/Changed/Fixed sections contain no OTelConf/RC entry.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/releases/release-v1.39.0.md` (SRC-REL-01)
- The `v1.40.0` milestones (go: milestone/76; contrib: milestone/34) are both closed with 0 open items, but there is **no `v1.40.0` release Source** in the package to confirm contents, and the index notes other items are "merged but unreleased… no `v1.40.0` release Source".
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-13661613.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/milestones/milestone-14282228.md`, `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/index.md` (line 43)

**Adjacent item, don't confuse it**
- A different otelconf item — `OTEL_EXPERIMENTAL_CONFIG_FILE` support, contrib issue `#8059` — was closed 2025-12-04 by MrAlias after being cross-referenced to PR `#8106` (cross-reference by codeboten, 2025-10-30). But `#8106` itself is not in the Sources and its merge/release is likewise not established.
  `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/opentelemetry/issues/opentelemetry-go-contrib-8059.md` (lines 49, 65), `/Users/markpyzhov/VSCodeProjects/corpuses-arms/c2/work-states/WS-05-contrib.md` (lines 31, 49, 54, 62)

**Bottom line:** the merge decision is on record, but the package holds no PR record, no merge event, and no release note showing OTelConf RC support shipping. Answering "yes, it shipped" would go beyond the evidence available here.
