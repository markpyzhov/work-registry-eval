# Corpus 2 Event Ledger

**Evaluator artifact.** Reconstructed from the evaluator package's frozen Sources
and `manifest.md`, then extended with the three dated Comments applied to final Work
State.

- **As-of:** `2026-02-27T17:20:46Z`
- **Comment extension:** `CMT-2026-03-001` through `CMT-2026-03-003` are recorded only under their affected work items.
- **Scope:** Every dated record after the as-of is excluded. `Collected` and `Updated` remain provenance/capture metadata, not events.
- **Done convention used:** merged establishes code integration; release completion additionally requires release evidence. Issue closure, an explicitly approved meeting decision, and a closed milestone have their manifest meanings.
- **Ledger shape:** 15 work items; 654 unique in-window raw source-event records in the appendix. The rollup below groups only duplicate mechanical records and points to the complete inventory.

## Work-item rollup

### W-01 — otelgin MultipartForm cleanup

- **Primary references:** `opentelemetry-go-contrib#5946` and PR `#6609`; **owner:** no owner is identified.
- **Sources:** `SRC-ISSUE-01`, `SRC-PR-01`, `SRC-NOTE-04`.
- **Material sequence:** the issue was opened 2024-07-25; PR `#6609` was opened 2025-01-13; the issue marked a duplicate on 2025-07-02; the 2025-10-16 meeting recorded the instrumentation cleanup options and that it needed addressing; the PR remained open at the as-of.
- **As-of state:** unresolved/open. The Sources do not establish which cleanup option was adopted.
- **Comment event (2026-03-08):** `CMT-2026-03-002` records automatic `MultipartForm.RemoveAll()` as the adopted method and local completion, with publication still pending.
- **Final Work State:** complete locally using `RemoveAll()`; final commits remain unpushed and the GitHub issue/PR remain open.
- **Flags:** cross-source current state; unresolved/abstention candidate.

### W-02 — otelhttp error recording and stabilization

- **Primary reference:** `opentelemetry-go-contrib#7254`; **owner:** XSAM opened it; Robert was assigned a clarification action in the meeting notes.
- **Sources:** `SRC-ISSUE-02`, `SRC-NOTE-06`, `SRC-MILE-02`, `SRC-MILE-04`.
- **Material sequence:** opened 2025-04-23; placed in `v1.39.0` on 2025-09-18; the 2025-10-30 meeting described it as a possible otelhttp stabilization blocker and assigned a semconv/interpretation document; moved from `v1.39.0` to `v1.40.0` on 2025-12-04; closed 2026-01-13.
- **As-of state:** closed/completed in the issue, with no release claim beyond the evidence provided.
- **Flags:** cross-source current state; dependency on semantic-convention interpretation.

### W-03 — OSS-Fuzz monitoring and notification path

- **Primary reference:** `opentelemetry-go#7549`; **owner:** pellared opened it; Robert had the meeting action for the mailing list.
- **Sources:** `SRC-ISSUE-04`, `SRC-NOTE-06`.
- **Material sequence:** opened 2025-10-06; transferred 2025-10-29; on 2025-10-30 the SIG chose a maintainers mailing list and a trial period rather than public GitHub filing; the issue received follow-on OSS-Fuzz cross-references on 2025-11-03 and 2025-11-04.
- **As-of state:** open. Public automatic issue filing was deferred, not approved.
- **Comment event (2026-03-05):** `CMT-2026-03-001` records the Go-maintainers mailing-list and trial-monitoring path as complete while public automatic filing remains deferred.
- **Final Work State:** mailing-list/trial work complete; public automatic GitHub filing deferred.
- **Flags:** supersession/decision; meeting-note-only blocker/deferral.

### W-04 — `OTEL_EXPERIMENTAL_CONFIG_FILE` support

- **Primary reference:** `opentelemetry-go-contrib#8059`; **owner:** codeboten opened it; Alex had the meeting action.
- **Sources:** `SRC-ISSUE-05`, `SRC-NOTE-05`.
- **Material sequence:** opened 2025-10-22; the 2025-10-23 meeting rejected short-term SDK-level support in favor of a contrib `otelconf` prototype; a linked implementation PR appeared 2025-10-30; closed 2025-12-04.
- **As-of state:** closed/completed. The Sources do not establish that the earlier SDK-level option shipped.
- **Flags:** supersession/decision; cross-source current state.

### W-05 — otelgrpc stabilization versus restoring the deprecated interceptor

- **Primary reference:** `opentelemetry-go-contrib#8078`; **owner:** nicholasngai opened it.
- **Sources:** `SRC-ISSUE-06`, `SRC-NOTE-06`.
- **Material sequence:** the restoration request was closed as not planned on 2025-10-31; the 2025-10-30 meeting separated that request from a longer otelgrpc stabilization path, which depended on RPC semantic conventions and gRPC engagement and was not expected that year.
- **As-of state:** restoration request closed/not planned; module-stabilization timing unresolved.
- **Flags:** supersession/dependency; abstention candidate.

### W-06 — release signing / immutable-release practice

- **Primary reference:** `sig-security#164`; **owner:** trask opened it; Robert had the Go SIG action.
- **Sources:** `SRC-ISSUE-03`, `SRC-NOTE-06`.
- **Material sequence:** opened 2025-08-27; the 2025-10-30 meeting decided to enable signature releases and update release documentation; renamed 2026-01-07; closed 2026-01-28.
- **As-of state:** closed/completed issue. The Sources do not prove a particular later release artifact was signed.
- **Comment event (2026-03-11):** `CMT-2026-03-003` records broader immutable/signature-release enablement as deferred pending release-tooling and asset-upload confirmation.
- **Final Work State:** deferred/not done; issue closure is not delivery completion.
- **Flags:** cross-source current state; abstention candidate for implementation proof.

### W-07 — Ecosystem Explorer project proposal

- **Primary reference:** `open-telemetry/community#3000`; **owner:** jaydeluca.
- **Sources:** `SRC-PR-02`, `SRC-NOTE-06`.
- **Material sequence:** opened and made ready for review 2025-09-19; the 2025-10-30 meeting required semantic-convention alignment, Weaver compatibility, and validation/schema work; merged and closed 2025-12-01.
- **As-of state:** merged proposal. The Sources do not establish delivery of the separate Explorer implementation.
- **Flags:** cross-source current state; abstention candidate.

### W-08 — SDK log Record mutation fix

- **Primary reference:** `opentelemetry-go#7403`; **owner:** pellared.
- **Sources:** `SRC-PR-03`, `SRC-MILE-02`, `SRC-REL-01`, `SRC-NOTE-04`.
- **Material sequence:** opened 2025-09-23; milestone assignment 2025-09-25; the 2025-10-16 meeting requested review; merged later that day; `v1.39.0` was published 2025-12-08 and names `#7403`.
- **As-of state:** merged and released in `v1.39.0`.
- **Flags:** cross-source current state; merged-versus-released contrast.

### W-09 — concurrent sum performance

- **Primary reference:** `opentelemetry-go#7427`; **owner:** dashpole.
- **Sources:** `SRC-PR-04`, `SRC-NOTE-02`, `SRC-MILE-02`, `SRC-REL-01`.
- **Material sequence:** opened 2025-09-29; the 2025-10-02 meeting accepted the sync.Map/atomic approach and ordered counter work ahead of histogram/fixed-size work; merged 2025-10-07; assigned to `v1.39.0` 2025-10-14; the release published 2025-12-08 names `#7427`.
- **As-of state:** merged and released in `v1.39.0`.
- **Flags:** cross-source current state; dependency/sequence evidence.

### W-10 — histogram-reservoir optimization

- **Primary reference:** `opentelemetry-go#7443`; **owner:** dashpole.
- **Sources:** `SRC-PR-05`, `SRC-NOTE-02`, `SRC-NOTE-03`, `SRC-NOTE-04`, `SRC-MILE-02`, `SRC-MILE-03`.
- **Material sequence:** opened 2025-10-02; the 2025-10-02 meeting sequenced it after counter work; the 2025-10-09 meeting recorded a race concern; the 2025-10-16 meeting described the simpler per-measurement-lock approach; moved from `v1.39.0` to `v1.40.0` 2025-12-04; merged 2025-12-15.
- **As-of state:** merged, but no `v1.40.0` release Source is included, so release completion is not established.
- **Flags:** supersession; merged-but-unreleased.

### W-11 — fixed-bucket histogram optimization

- **Primary reference:** `opentelemetry-go#7474`; **owner:** dashpole.
- **Sources:** `SRC-PR-06`, `SRC-NOTE-02`, `SRC-NOTE-03`, `SRC-NOTE-07`, `SRC-MILE-02`, `SRC-MILE-03`.
- **Material sequence:** opened 2025-10-08; the 2025-10-02 meeting placed fixed-size work after counter work; the 2025-10-09 meeting listed it for review; the 2025-11-20 meeting said it could slip safely; moved from `v1.39.0` to `v1.40.0` 2025-12-04; merged 2025-12-11.
- **As-of state:** merged, with no included `v1.40.0` release Source proving release completion.
- **Flags:** dependency/sequence; merged-but-unreleased.

### W-12 — otelgin context-save/restore data-race PR

- **Primary reference:** `opentelemetry-go-contrib#8014`; **owner:** nicksherron.
- **Sources:** `SRC-PR-07`, `SRC-NOTE-04`.
- **Material sequence:** opened and made ready for review 2025-10-14; the 2025-10-16 meeting treated the underlying context behavior as intentional and recommended explicitly passing context to spawned goroutines; closed 2025-10-17.
- **As-of state:** closed without a merge event in the supplied Source.
- **Flags:** supersession/decision. (Corrected 2026-07-24: **not** an abstention item — the closure rationale is stated in `SRC-PR-07` (dmathieu 2025-10-17 comment, per the SIG decision on `#4588`) and captured in the material sequence above, so the closure reason is Source-supported and answerable by every arm.)

### W-13 — temporality-selector configuration approach

- **Primary reference:** recurring SIG topic; **owner:** Tyler was assigned feedback/closure follow-up.
- **Sources:** `SRC-NOTE-01`, `SRC-NOTE-03`, `SRC-NOTE-04`, `SRC-REL-01`.
- **Material sequence:** on 2025-09-25 the proposed string selector had no recent activity and might leave the milestone; on 2025-10-09 the SIG rejected custom selector parsing in favor of the full OpenTelemetry configuration format; on 2025-10-16 the prior PR was described as API pollution and slated for closure; `v1.39.0` later lists the selector functions themselves as released.
- **As-of state:** the Sources support a distinction between released selector functions and rejection of the custom parsing/configuration approach; they do not establish a broader product conclusion.
- **Flags:** strongest supersession/temporality candidate.

### W-14 — OTelConf RC support and experimental API structure

- **Primary reference:** recurring SIG topic; **owner:** Alex had the tracking-issue action.
- **Sources:** `SRC-NOTE-07`.
- **Material sequence:** on 2025-11-20 the release was blocked on RC support review; the SIG decided to merge the RC PR as-is after normal review and to track experimental API structure under `1.40.0`.
- **As-of state:** decision recorded; the referenced PR and its final delivery are not in the package.
- **Flags:** single-source fact; abstention candidate.

### W-15 — runtime-tracer/profiling API proposal

- **Primary reference:** recurring SIG topic; **owner:** Nico Hertz.
- **Sources:** `SRC-NOTE-08`.
- **Material sequence:** on 2025-11-27 the SIG decided not to merge the large public-API change without issue discussion, to keep the existing PR as a draft/proof of concept, and to begin with a smaller disablement change.
- **As-of state:** deferred pending a documented issue and smaller proposal.
- **Flags:** single-source fact; meeting-note-only deferral.

## Candidate strata and unresolved cases

The rollup yields a ceiling of 15 potential scored items without writing question wording:

| Stratum | Candidate work items | Depth |
| --- | --- | ---: |
| Single-source fact | W-14, W-15 | 2 |
| Cross-source current state | W-01, W-02, W-04, W-07, W-08, W-09 | 6 |
| Supersession/dependency | W-03, W-05, W-10, W-11, W-12, W-13 | 6 |
| **Total potential scored items** |  | **14** |

The supersession/dependency stratum is above the minimum of three. The original unscored abstention set was W-01 (cleanup choice), W-05 (stabilization timing), W-06 (signed artifact proof), W-07 (Explorer delivery), and W-14 (RC PR delivery). These cases have a useful known boundary but no supported final answer beyond that boundary. (Corrected 2026-07-24: **W-12 removed** from the abstention set — the `#8014` closure rationale is stated in `SRC-PR-07`, so it is Source-supported and answerable, not an abstention.) (Corrected 2026-07-27: **W-06 re-characterized** — the record supports v1.39.0, while only final Work State supplies the later deferral. Active expected answers for all A-items are stated directly in the two arm-specific keys.)

## Complete raw-event appendix

The following is the complete in-window dated-event inventory. It preserves the 26 source-creation records, five duplicated `merged_at` headers (for traceability, as in the manifest), 140 discussions, 118 reviews, 139 inline review comments, 225 timeline records, and one release publication: **654 records**. The 15 post-window timeline records are excluded under the manifest rule and are not reproduced here.

### SRC-ISSUE-04 — `work-registry/opentelemetry/issues/opentelemetry-go-7549.md` (15 records)

- `2025-10-06T17:08:06Z` — **source-created** — source created
- `2025-10-07T14:44:09Z` — **discussion** — **MrAlias** — 2025-10-07T14:44:09Z
- `2025-10-09T03:53:40Z` — **discussion** — **trask** — 2025-10-09T03:53:40Z
- `2025-10-15T17:22:55Z` — **discussion** — **lmolkova** — 2025-10-15T17:22:55Z
- `2025-10-29T15:08:30Z` — **timeline** — transferred** by dashpole
- `2025-10-29T15:09:30Z` — **discussion** — **dashpole** — 2025-10-29T15:09:30Z
- `2025-10-29T16:38:40Z` — **discussion** — **mx-psi** — 2025-10-29T16:38:40Z
- `2025-10-30T16:13:50Z` — **discussion** — **dashpole** — 2025-10-30T16:13:50Z
- `2025-10-30T16:15:16Z` — **discussion** — **mx-psi** — 2025-10-30T16:15:16Z
- `2025-11-03T09:39:05Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-03T12:42:36Z` — **discussion** — **pellared** — 2025-11-03T12:42:36Z
- `2025-11-03T15:04:05Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/google/oss-fuzz/pull/14233
- `2025-11-03T16:34:10Z` — **timeline** — referenced** by AdamKorcz
- `2025-11-04T08:03:05Z` — **timeline** — cross-referenced** by dmathieu ← https://github.com/google/oss-fuzz/pull/14240
- `2025-11-04T17:25:21Z` — **timeline** — referenced** by DavidKorczynski

### SRC-ISSUE-01 — `work-registry/opentelemetry/issues/opentelemetry-go-contrib-5946.md` (22 records)

- `2024-07-25T03:50:39Z` — **source-created** — source created
- `2024-07-25T03:50:39Z` — **timeline** — labeled** by zacklpx `area: instrumentation`
- `2024-07-25T03:50:39Z` — **timeline** — labeled** by zacklpx `bug`
- `2024-07-25T03:50:39Z` — **timeline** — labeled** by zacklpx `instrumentation: otelgin`
- `2024-11-21T12:21:58Z` — **timeline** — cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/4588
- `2025-01-11T11:28:03Z` — **discussion** — **Yiling-J** — 2025-01-11T11:28:03Z
- `2025-01-12T13:54:25Z` — **discussion** — **dmathieu** — 2025-01-12T13:54:25Z
- `2025-01-13T02:11:01Z` — **discussion** — **akats7** — 2025-01-13T02:11:01Z
- `2025-01-13T13:45:45Z` — **timeline** — cross-referenced** by Yiling-J ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/6609
- `2025-07-02T08:06:05Z` — **timeline** — marked_as_duplicate** by dmathieu
- `2025-07-02T08:06:06Z` — **timeline** — cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7541
- `2025-07-02T08:35:01Z` — **discussion** — **flc1125** — 2025-07-02T08:35:01Z
- `2025-07-02T08:58:39Z` — **discussion** — **akats7** — 2025-07-02T08:58:39Z
- `2025-07-02T09:37:44Z` — **discussion** — **zihuyishi** — 2025-07-02T09:37:44Z
- `2025-07-02T09:40:40Z` — **discussion** — **akats7** — 2025-07-02T09:40:40Z
- `2025-07-02T10:01:01Z` — **discussion** — **flc1125** — 2025-07-02T10:01:01Z
- `2025-07-02T10:06:33Z` — **discussion** — **akats7** — 2025-07-02T10:06:33Z
- `2025-07-02T15:23:47Z` — **discussion** — **flc1125** — 2025-07-02T15:23:47Z
- `2025-07-02T15:30:57Z` — **timeline** — cross-referenced** by flc1125 ← https://github.com/golang/go/issues/74455
- `2025-07-03T13:24:52Z` — **discussion** — **flc1125** — 2025-07-03T13:24:52Z
- `2025-11-03T09:18:09Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2026-01-16T17:41:03Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8419

### SRC-ISSUE-02 — `work-registry/opentelemetry/issues/opentelemetry-go-contrib-7254.md` (32 records)

- `2025-04-23T02:21:22Z` — **source-created** — source created
- `2025-04-23T02:21:22Z` — **timeline** — labeled** by XSAM `area: instrumentation`
- `2025-04-23T02:21:22Z` — **timeline** — labeled** by XSAM `bug`
- `2025-04-23T02:21:22Z` — **timeline** — labeled** by XSAM `instrumentation: otelhttp`
- `2025-04-23T02:22:14Z` — **timeline** — renamed** by XSAM "otelhttp: Cannot record error when producing new semantic convention" → "otelhttp: Cannot record error for spans when producing new semantic convention"
- `2025-04-23T08:03:12Z` — **discussion** — **dmathieu** — 2025-04-23T08:03:12Z
- `2025-04-23T16:07:50Z` — **discussion** — **XSAM** — 2025-04-23T16:07:50Z
- `2025-04-24T18:26:30Z` — **discussion** — **XSAM** — 2025-04-24T18:26:30Z
- `2025-06-10T14:53:31Z` — **timeline** — cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/7456
- `2025-06-11T12:24:35Z` — **discussion** — **pellared** — 2025-06-11T12:24:35Z
- `2025-06-12T17:03:33Z` — **discussion** — **dashpole** — 2025-06-12T17:03:33Z
- `2025-06-13T07:21:05Z` — **discussion** — **pellared** — 2025-06-13T07:21:05Z
- `2025-06-16T07:32:18Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7470
- `2025-06-16T07:40:13Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6903
- `2025-06-16T07:44:04Z` — **discussion** — **pellared** — 2025-06-16T07:44:04Z
- `2025-08-03T20:45:58Z` — **discussion** — **XSAM** — 2025-08-03T20:45:58Z
- `2025-08-04T15:12:11Z` — **discussion** — **pellared** — 2025-08-04T15:12:11Z
- `2025-08-05T06:38:55Z` — **discussion** — **XSAM** — 2025-08-05T06:38:55Z
- `2025-08-05T06:40:03Z` — **discussion** — **pellared** — 2025-08-05T06:40:03Z
- `2025-08-05T06:50:03Z` — **discussion** — **XSAM** — 2025-08-05T06:50:03Z
- `2025-09-18T16:17:38Z` — **timeline** — milestoned** by MrAlias → v1.39.0
- `2025-10-16T20:42:15Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/semantic-conventions/pull/2296
- `2025-11-03T09:39:05Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-03T13:34:57Z` — **discussion** — **pellared** — 2025-11-03T13:34:57Z
- `2025-11-03T14:23:56Z` — **timeline** — cross-referenced** by dmathieu ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8107
- `2025-11-03T14:55:36Z` — **discussion** — **dashpole** — 2025-11-03T14:55:36Z
- `2025-11-03T15:00:09Z` — **discussion** — **pellared** — 2025-11-03T15:00:09Z
- `2025-12-04T18:17:39Z` — **timeline** — demilestoned** by MrAlias → v1.39.0
- `2025-12-04T18:17:39Z` — **timeline** — milestoned** by MrAlias → v1.40.0
- `2025-12-19T13:23:07Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/semantic-conventions/pull/3228
- `2026-01-12T17:33:42Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8386
- `2026-01-13T15:23:09Z` — **timeline** — closed** by pellared

### SRC-ISSUE-05 — `work-registry/opentelemetry/issues/opentelemetry-go-contrib-8059.md` (12 records)

- `2025-10-22T21:25:29Z` — **source-created** — source created
- `2025-10-22T21:25:30Z` — **timeline** — labeled** by codeboten `enhancement`
- `2025-10-22T21:25:42Z` — **timeline** — labeled** by github-actions[bot] `area: file-config`
- `2025-10-22T21:27:48Z` — **timeline** — renamed** by codeboten "[Feature]: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable" → "otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable"
- `2025-10-23T17:18:25Z` — **discussion** — **codeboten** — 2025-10-23T17:18:25Z
- `2025-10-30T21:39:26Z` — **timeline** — referenced** by codeboten
- `2025-10-30T21:40:31Z` — **timeline** — cross-referenced** by codeboten ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8106
- `2025-11-03T09:30:28Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-24T19:47:10Z` — **timeline** — referenced** by codeboten
- `2025-11-27T17:50:35Z` — **timeline** — referenced** by codeboten
- `2025-12-04T18:32:17Z` — **discussion** — **dashpole** — 2025-12-04T18:32:17Z
- `2025-12-04T23:38:10Z` — **timeline** — closed** by MrAlias

### SRC-ISSUE-06 — `work-registry/opentelemetry/issues/opentelemetry-go-contrib-8078.md` (14 records)

- `2025-10-27T23:28:07Z` — **source-created** — source created
- `2025-10-28T08:36:24Z` — **discussion** — **dmathieu** — 2025-10-28T08:36:24Z
- `2025-10-28T20:02:57Z` — **discussion** — **dashpole** — 2025-10-28T20:02:57Z
- `2025-10-28T20:40:37Z` — **discussion** — **nicholasngai** — 2025-10-28T20:40:37Z
- `2025-10-29T08:35:31Z` — **discussion** — **dmathieu** — 2025-10-29T08:35:31Z
- `2025-10-29T16:28:55Z` — **discussion** — **nicholasngai** — 2025-10-29T16:28:55Z
- `2025-10-29T17:37:26Z` — **discussion** — **MrAlias** — 2025-10-29T17:37:26Z
- `2025-10-29T17:38:42Z` — **discussion** — **nicholasngai** — 2025-10-29T17:38:42Z
- `2025-10-29T18:06:47Z` — **discussion** — **MrAlias** — 2025-10-29T18:06:47Z
- `2025-10-29T18:51:27Z` — **discussion** — **dashpole** — 2025-10-29T18:51:27Z
- `2025-10-30T08:46:26Z` — **discussion** — **dmathieu** — 2025-10-30T08:46:26Z
- `2025-10-31T09:47:48Z` — **discussion** — **dmathieu** — 2025-10-31T09:47:48Z
- `2025-10-31T09:47:48Z` — **timeline** — closed** by dmathieu
- `2025-11-03T09:39:05Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648

### SRC-ISSUE-03 — `work-registry/opentelemetry/issues/sig-security-164.md` (19 records)

- `2025-08-27T13:31:30Z` — **source-created** — source created
- `2025-09-16T12:52:39Z` — **discussion** — **pellared** — 2025-09-16T12:52:39Z
- `2025-09-17T18:01:37Z` — **discussion** — **pellared** — 2025-09-17T18:01:37Z
- `2025-10-14T14:58:10Z` — **discussion** — **pellared** — 2025-10-14T14:58:10Z
- `2025-10-23T02:38:58Z` — **discussion** — **trask** — 2025-10-23T02:38:58Z
- `2025-10-27T09:21:42Z` — **discussion** — **pellared** — 2025-10-27T09:21:42Z
- `2025-10-31T01:23:11Z` — **timeline** — cross-referenced** by trask ← https://github.com/open-telemetry/opentelemetry-dotnet/pull/6646
- `2025-11-03T09:39:05Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-03T10:30:37Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/pull/7567
- `2025-11-03T10:38:17Z` — **discussion** — **pellared** — 2025-11-03T10:38:17Z
- `2025-11-04T06:03:36Z` — **timeline** — referenced** by pellared
- `2025-11-07T00:20:03Z` — **discussion** — **trask** — 2025-11-07T00:20:03Z
- `2025-12-03T10:14:03Z` — **timeline** — cross-referenced** by martincostello ← https://github.com/open-telemetry/opentelemetry-dotnet/issues/6748
- `2025-12-11T17:43:19Z` — **discussion** — **pellared** — 2025-12-11T17:43:19Z
- `2025-12-11T17:47:55Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/issues/13
- `2026-01-07T18:19:16Z` — **discussion** — **pellared** — 2026-01-07T18:19:16Z
- `2026-01-07T18:28:05Z` — **timeline** — renamed** by trask "Enable immutable releases where possible" → "Recommend immutable releases"
- `2026-01-28T11:30:57Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/sig-security/pull/219
- `2026-01-28T22:16:50Z` — **timeline** — closed** by reyang

### SRC-NOTE-01 — `work-registry/opentelemetry/meeting-notes/entry-3389930076.md` (1 records)

- `2025-10-10T12:53:12Z` — **source-created** — source created

### SRC-NOTE-02 — `work-registry/opentelemetry/meeting-notes/entry-3389972183.md` (1 records)

- `2025-10-10T13:03:41Z` — **source-created** — source created

### SRC-NOTE-03 — `work-registry/opentelemetry/meeting-notes/entry-3390010099.md` (1 records)

- `2025-10-10T13:10:44Z` — **source-created** — source created

### SRC-NOTE-04 — `work-registry/opentelemetry/meeting-notes/entry-3479584781.md` (1 records)

- `2025-11-03T09:18:08Z` — **source-created** — source created

### SRC-NOTE-05 — `work-registry/opentelemetry/meeting-notes/entry-3479626706.md` (1 records)

- `2025-11-03T09:30:26Z` — **source-created** — source created

### SRC-NOTE-06 — `work-registry/opentelemetry/meeting-notes/entry-3479655348.md` (1 records)

- `2025-11-03T09:39:04Z` — **source-created** — source created

### SRC-NOTE-07 — `work-registry/opentelemetry/meeting-notes/entry-3581463689.md` (1 records)

- `2025-11-26T14:02:28Z` — **source-created** — source created

### SRC-NOTE-08 — `work-registry/opentelemetry/meeting-notes/entry-3974113940.md` (1 records)

- `2026-02-27T17:20:46Z` — **source-created** — source created

### SRC-MILE-01 — `work-registry/opentelemetry/milestones/milestone-11866121.md` (1 records)

- `2024-11-08T11:22:34Z` — **source-created** — source created

### SRC-MILE-02 — `work-registry/opentelemetry/milestones/milestone-13145551.md` (1 records)

- `2025-06-25T19:56:24Z` — **source-created** — source created

### SRC-MILE-03 — `work-registry/opentelemetry/milestones/milestone-13661613.md` (1 records)

- `2025-09-11T17:31:20Z` — **source-created** — source created

### SRC-MILE-04 — `work-registry/opentelemetry/milestones/milestone-14282228.md` (1 records)

- `2025-12-04T18:13:58Z` — **source-created** — source created

### SRC-PR-02 — `work-registry/opentelemetry/pulls/community-3000.md` (70 records)

- `2025-09-19T10:11:57Z` — **source-created** — source created
- `2025-09-19T11:58:43Z` — **inline-review** — **svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:58:43Z
- `2025-09-19T11:59:42Z` — **inline-review** — **svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:59:42Z
- `2025-09-19T11:59:55Z` — **inline-review** — **svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:59:55Z
- `2025-09-19T12:00:51Z` — **inline-review** — **svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T12:00:51Z
- `2025-09-19T12:01:36Z` — **inline-review** — **svrnm** on `projects/instrumentation-documentation.md` (line 205) — 2025-09-19T12:01:36Z
- `2025-09-19T12:02:17Z` — **review** — **svrnm** — CHANGES_REQUESTED — 2025-09-19T12:02:17Z
- `2025-09-19T12:02:37Z` — **timeline** — cross-referenced** by svrnm ← https://github.com/open-telemetry/community/pull/2246
- `2025-09-19T12:29:51Z` — **review** — **mx-psi** — COMMENTED — 2025-09-19T12:29:51Z
- `2025-09-19T12:34:33Z` — **discussion** — **jaydeluca** — 2025-09-19T12:34:33Z
- `2025-09-19T12:38:35Z` — **discussion** — **mx-psi** — 2025-09-19T12:38:35Z
- `2025-09-19T12:39:50Z` — **discussion** — **jaydeluca** — 2025-09-19T12:39:50Z
- `2025-09-19T14:24:14Z` — **timeline** — renamed** by jaydeluca "Project Proposal: Instrumentation Documentation" → "Project Proposal: Ecosystem Explorer"
- `2025-09-19T14:26:38Z` — **discussion** — **svrnm** — 2025-09-19T14:26:38Z
- `2025-09-19T14:31:52Z` — **timeline** — ready_for_review** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-09-19T14:31:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-10-01T03:14:12Z` — **discussion** — **thompson-tomo** — 2025-10-01T03:14:12Z
- `2025-10-01T15:17:00Z` — **timeline** — labeled** by svrnm `area/project-proposal`
- `2025-10-01T19:08:52Z` — **discussion** — **jaydeluca** — 2025-10-01T19:08:52Z
- `2025-10-01T19:11:49Z` — **discussion** — **trask** — 2025-10-01T19:11:49Z
- `2025-10-03T15:12:52Z` — **timeline** — cross-referenced** by trask ← https://github.com/open-telemetry/community/issues/3049
- `2025-10-03T16:48:39Z` — **timeline** — cross-referenced** by jaydeluca ← https://github.com/open-telemetry/opentelemetry-java-instrumentation/issues/13468
- `2025-10-06T05:26:18Z` — **discussion** — **thompson-tomo** — 2025-10-06T05:26:18Z
- `2025-10-06T10:17:57Z` — **discussion** — **jaydeluca** — 2025-10-06T10:17:57Z
- `2025-10-06T11:52:52Z` — **discussion** — **thompson-tomo** — 2025-10-06T11:52:52Z
- `2025-10-29T12:16:22Z` — **inline-review** — **mx-psi** on `projects/ecosystem-explorer.md` — 2025-10-29T12:16:22Z
- `2025-10-29T12:16:48Z` — **inline-review** — **mx-psi** on `projects/ecosystem-explorer.md` (line 179) — 2025-10-29T12:16:48Z
- `2025-10-29T12:17:34Z` — **review** — **mx-psi** — COMMENTED — 2025-10-29T12:17:34Z
- `2025-10-29T12:22:11Z` — **timeline** — cross-referenced** by mx-psi ← https://github.com/open-telemetry/opentelemetry-collector/issues/14096
- `2025-10-30T15:07:24Z` — **inline-review** — **vitorvasc** on `projects/ecosystem-explorer.md` (line 197) — 2025-10-30T15:07:24Z
- `2025-10-30T15:07:24Z` — **review** — **vitorvasc** — COMMENTED — 2025-10-30T15:07:24Z
- `2025-11-03T09:39:05Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-05T12:06:07Z` — **timeline** — cross-referenced** by mx-psi ← https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/44057
- `2025-11-06T20:51:53Z` — **timeline** — review_requested** by jaydeluca
- `2025-11-10T15:29:30Z` — **discussion** — **jack-berg** — 2025-11-10T15:29:30Z
- `2025-11-18T07:54:04Z` — **discussion** — **svrnm** — 2025-11-18T07:54:04Z
- `2025-11-18T07:55:05Z` — **inline-review** — **svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:55:05Z
- `2025-11-18T07:55:05Z` — **review** — **svrnm** — COMMENTED — 2025-11-18T07:55:05Z
- `2025-11-18T07:58:54Z` — **inline-review** — **svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:58:54Z
- `2025-11-18T07:58:54Z` — **review** — **svrnm** — COMMENTED — 2025-11-18T07:58:54Z
- `2025-11-18T07:59:07Z` — **inline-review** — **svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:59:07Z
- `2025-11-18T07:59:07Z` — **review** — **svrnm** — COMMENTED — 2025-11-18T07:59:07Z
- `2025-11-18T08:00:13Z` — **inline-review** — **svrnm** on `projects/ecosystem-explorer.md` (line 109) — 2025-11-18T08:00:13Z
- `2025-11-18T08:00:13Z` — **review** — **svrnm** — COMMENTED — 2025-11-18T08:00:13Z
- `2025-11-19T10:48:10Z` — **timeline** — cross-referenced** by svrnm ← https://github.com/open-telemetry/opentelemetry.io/issues/2614
- `2025-11-20T18:33:12Z` — **inline-review** — **svrnm** on `projects/ecosystem-explorer.md` — 2025-11-20T18:33:12Z
- `2025-11-20T18:33:12Z` — **review** — **svrnm** — COMMENTED — 2025-11-20T18:33:12Z
- `2025-11-20T19:18:34Z` — **review** — **svrnm** — APPROVED — 2025-11-20T19:18:34Z
- `2025-11-20T19:24:07Z` — **review** — **trask** — APPROVED — 2025-11-20T19:24:07Z
- `2025-11-20T20:54:14Z` — **review** — **maryliag** — APPROVED — 2025-11-20T20:54:14Z
- `2025-11-21T10:32:49Z` — **review** — **mx-psi** — APPROVED — 2025-11-21T10:32:49Z
- `2025-11-21T15:57:47Z` — **review** — **jack-berg** — APPROVED — 2025-11-21T15:57:47Z
- `2025-11-30T14:38:07Z` — **discussion** — **thompson-tomo** — 2025-11-30T14:38:07Z
- `2025-12-01T08:20:26Z` — **discussion** — **svrnm** — 2025-12-01T08:20:26Z
- `2025-12-01T18:24:54Z` — **review** — **tedsuo** — APPROVED — 2025-12-01T18:24:54Z
- `2025-12-01T18:36:48Z` — **discussion** — **trask** — 2025-12-01T18:36:48Z
- `2025-12-01T19:04:18Z` — **merged-header** — merged_at header; duplicate of its timeline event
- `2025-12-01T19:04:18Z` — **timeline** — closed** by trask
- `2025-12-01T19:04:18Z` — **timeline** — merged** by trask
- `2025-12-02T08:40:24Z` — **discussion** — **svrnm** — 2025-12-02T08:40:24Z
- `2025-12-02T08:42:03Z` — **timeline** — cross-referenced** by svrnm ← https://github.com/open-telemetry/community/issues/3175
- `2025-12-04T11:17:32Z` — **timeline** — cross-referenced** by svrnm ← https://github.com/open-telemetry/community/pull/3128
- `2026-01-20T22:34:11Z` — **timeline** — cross-referenced** by jaydeluca ← https://github.com/open-telemetry/community/issues/3230

### SRC-PR-03 — `work-registry/opentelemetry/pulls/opentelemetry-go-7403.md` (54 records)

- `2025-09-23T17:31:54Z` — **source-created** — source created
- `2025-09-23T17:38:27Z` — **discussion** — **codecov[bot]** — 2025-09-23T17:38:27Z
- `2025-09-23T19:58:07Z` — **timeline** — ready_for_review** by pellared
- `2025-09-23T19:58:08Z` — **timeline** — review_requested** by pellared
- `2025-09-23T19:58:08Z` — **timeline** — review_requested** by pellared
- `2025-09-23T19:58:08Z` — **timeline** — review_requested** by pellared
- `2025-09-23T19:58:08Z` — **timeline** — review_requested** by pellared
- `2025-09-23T19:58:08Z` — **timeline** — review_requested** by pellared
- `2025-09-23T19:58:37Z` — **discussion** — **pellared** — 2025-09-23T19:58:37Z
- `2025-09-24T11:28:01Z` — **timeline** — review_requested** by pellared
- `2025-09-24T11:28:31Z` — **review** — **copilot-pull-request-reviewer[bot]** — COMMENTED — 2025-09-24T11:28:31Z
- `2025-09-25T13:22:51Z` — **inline-review** — **flc1125** on `sdk/log/record.go` — 2025-09-25T13:22:51Z
- `2025-09-25T13:30:28Z` — **review** — **flc1125** — COMMENTED — 2025-09-25T13:30:28Z
- `2025-09-25T13:32:40Z` — **discussion** — **pellared** — 2025-09-25T13:32:40Z
- `2025-09-25T13:32:57Z` — **timeline** — convert_to_draft** by pellared
- `2025-09-25T17:08:16Z` — **timeline** — milestoned** by pellared → v1.39.0
- `2025-09-25T18:15:45Z` — **inline-review** — **pellared** on `sdk/log/record.go` — 2025-09-25T18:15:45Z
- `2025-09-25T18:15:45Z` — **review** — **pellared** — COMMENTED — 2025-09-25T18:15:45Z
- `2025-09-25T18:29:23Z` — **discussion** — **pellared** — 2025-09-25T18:29:23Z
- `2025-09-25T18:30:26Z` — **timeline** — ready_for_review** by pellared
- `2025-09-25T18:36:45Z` — **timeline** — convert_to_draft** by pellared
- `2025-09-25T18:44:28Z` — **timeline** — ready_for_review** by pellared
- `2025-09-25T18:50:17Z` — **timeline** — review_requested** by pellared
- `2025-09-25T20:00:58Z` — **discussion** — **pellared** — 2025-09-25T20:00:58Z
- `2025-09-25T20:04:04Z` — **timeline** — labeled** by pellared `area:logs`
- `2025-09-25T20:04:04Z` — **timeline** — labeled** by pellared `pkg:SDK`
- `2025-09-26T07:44:49Z` — **review** — **dmathieu** — APPROVED — 2025-09-26T07:44:49Z
- `2025-09-29T16:37:11Z` — **inline-review** — **MrAlias** on `sdk/log/record.go` (line 222) — 2025-09-29T16:37:11Z
- `2025-09-29T16:37:35Z` — **review** — **MrAlias** — COMMENTED — 2025-09-29T16:37:35Z
- `2025-09-29T18:29:03Z` — **inline-review** — **pellared** on `sdk/log/record.go` (line 222) — 2025-09-29T18:29:03Z
- `2025-09-29T18:29:03Z` — **review** — **pellared** — COMMENTED — 2025-09-29T18:29:03Z
- `2025-09-29T19:58:01Z` — **inline-review** — **MrAlias** on `sdk/log/record.go` (line 222) — 2025-09-29T19:58:01Z
- `2025-09-29T19:58:01Z` — **review** — **MrAlias** — COMMENTED — 2025-09-29T19:58:01Z
- `2025-09-29T20:02:50Z` — **inline-review** — **pellared** on `sdk/log/record.go` (line 222) — 2025-09-29T20:02:50Z
- `2025-09-29T20:02:51Z` — **review** — **pellared** — COMMENTED — 2025-09-29T20:02:51Z
- `2025-09-30T18:10:12Z` — **timeline** — convert_to_draft** by pellared
- `2025-10-01T10:35:21Z` — **inline-review** — **pellared** on `sdk/log/record.go` (line 222) — 2025-10-01T10:35:21Z
- `2025-10-01T10:35:21Z` — **review** — **pellared** — COMMENTED — 2025-10-01T10:35:21Z
- `2025-10-01T10:39:23Z` — **timeline** — ready_for_review** by pellared
- `2025-10-01T10:43:30Z` — **discussion** — **pellared** — 2025-10-01T10:43:30Z
- `2025-10-01T10:48:07Z` — **timeline** — review_requested** by pellared
- `2025-10-16T18:35:17Z` — **inline-review** — **dashpole** on `sdk/log/record.go` (line 222) — 2025-10-16T18:35:17Z
- `2025-10-16T18:35:17Z` — **review** — **dashpole** — COMMENTED — 2025-10-16T18:35:17Z
- `2025-10-16T18:35:28Z` — **review** — **dashpole** — APPROVED — 2025-10-16T18:35:28Z
- `2025-10-16T19:02:46Z` — **inline-review** — **pellared** on `sdk/log/record.go` (line 222) — 2025-10-16T19:02:46Z
- `2025-10-16T19:02:46Z` — **review** — **pellared** — COMMENTED — 2025-10-16T19:02:46Z
- `2025-10-16T19:06:43Z` — **discussion** — **pellared** — 2025-10-16T19:06:43Z
- `2025-10-16T19:07:08Z` — **merged-header** — merged_at header; duplicate of its timeline event
- `2025-10-16T19:07:08Z` — **timeline** — merged** by pellared
- `2025-10-16T19:07:09Z` — **timeline** — closed** by pellared
- `2025-10-16T19:07:17Z` — **timeline** — head_ref_deleted** by pellared
- `2025-11-03T09:18:09Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-12-05T18:12:13Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7676
- `2025-12-08T16:30:52Z` — **timeline** — referenced** by MrAlias

### SRC-PR-04 — `work-registry/opentelemetry/pulls/opentelemetry-go-7427.md` (81 records)

- `2025-09-29T14:36:56Z` — **source-created** — source created
- `2025-09-29T14:38:36Z` — **discussion** — **codecov[bot]** — 2025-09-29T14:38:36Z
- `2025-09-29T16:28:51Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7423
- `2025-09-29T19:49:42Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T14:50:14Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T14:57:29Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T15:11:55Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T15:43:45Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T15:45:33Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T15:47:47Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7380
- `2025-09-30T15:47:54Z` — **timeline** — ready_for_review** by dashpole
- `2025-09-30T15:47:54Z` — **timeline** — review_requested** by dashpole
- `2025-09-30T15:47:55Z` — **timeline** — review_requested** by dashpole
- `2025-09-30T15:47:55Z` — **timeline** — review_requested** by dashpole
- `2025-09-30T15:47:55Z` — **timeline** — review_requested** by dashpole
- `2025-09-30T15:47:55Z` — **timeline** — review_requested** by dashpole
- `2025-09-30T15:51:05Z` — **discussion** — **dashpole** — 2025-09-30T15:51:05Z
- `2025-09-30T15:51:45Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-09-30T15:52:02Z` — **timeline** — labeled** by dashpole `area:metrics`
- `2025-09-30T16:05:30Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7189
- `2025-10-01T16:32:02Z` — **timeline** — referenced** by dashpole
- `2025-10-02T14:09:53Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-02T14:15:56Z` — **discussion** — **dashpole** — 2025-10-02T14:15:56Z
- `2025-10-02T17:55:27Z` — **inline-review** — **MrAlias** on `CHANGELOG.md` — 2025-10-02T17:55:27Z
- `2025-10-03T00:03:10Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-03T00:03:10Z
- `2025-10-03T13:59:27Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-03T14:35:48Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-03T14:43:41Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-03T15:10:13Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:10:13Z
- `2025-10-03T15:14:24Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:14:24Z
- `2025-10-03T15:14:31Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T15:14:31Z
- `2025-10-03T15:23:10Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-03T15:23:10Z
- `2025-10-03T15:23:10Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T15:23:10Z
- `2025-10-03T15:25:53Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:25:53Z
- `2025-10-03T15:25:53Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T15:25:53Z
- `2025-10-03T15:27:00Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:27:00Z
- `2025-10-03T15:27:00Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T15:27:00Z
- `2025-10-03T15:32:21Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:32:21Z
- `2025-10-03T15:32:21Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T15:32:21Z
- `2025-10-03T16:00:07Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:00:07Z
- `2025-10-03T16:00:07Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T16:00:07Z
- `2025-10-03T16:01:55Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-03T16:02:38Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:02:38Z
- `2025-10-03T16:02:39Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T16:02:39Z
- `2025-10-03T16:32:39Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:32:39Z
- `2025-10-03T16:32:39Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T16:32:39Z
- `2025-10-03T17:34:52Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7443
- `2025-10-04T03:16:00Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-04T03:16:18Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-04T03:16:18Z
- `2025-10-04T03:16:18Z` — **review** — **dashpole** — COMMENTED — 2025-10-04T03:16:18Z
- `2025-10-04T03:16:29Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-04T03:16:29Z
- `2025-10-04T03:16:30Z` — **review** — **dashpole** — COMMENTED — 2025-10-04T03:16:30Z
- `2025-10-04T03:49:03Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-06T18:08:05Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T18:08:05Z
- `2025-10-06T18:08:05Z` — **review** — **MrAlias** — COMMENTED — 2025-10-06T18:08:05Z
- `2025-10-06T18:19:39Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T18:19:39Z
- `2025-10-06T18:19:39Z` — **review** — **dashpole** — COMMENTED — 2025-10-06T18:19:39Z
- `2025-10-06T19:17:53Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-06T19:21:01Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-06T19:21:43Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T19:21:43Z
- `2025-10-06T19:21:43Z` — **review** — **dashpole** — COMMENTED — 2025-10-06T19:21:43Z
- `2025-10-06T20:59:53Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-06T21:01:38Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-07T00:04:26Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-07T00:04:26Z
- `2025-10-07T00:04:45Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-07T00:04:45Z
- `2025-10-07T00:26:04Z` — **review** — **MrAlias** — APPROVED — 2025-10-07T00:26:04Z
- `2025-10-07T07:21:57Z` — **review** — **dmathieu** — APPROVED — 2025-10-07T07:21:57Z
- `2025-10-07T13:40:23Z` — **merged-header** — merged_at header; duplicate of its timeline event
- `2025-10-07T13:40:23Z` — **timeline** — closed** by dashpole
- `2025-10-07T13:40:23Z` — **timeline** — merged** by dashpole
- `2025-10-08T14:31:22Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7474
- `2025-10-08T19:23:19Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7478
- `2025-10-09T17:25:37Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7037
- `2025-10-10T13:10:45Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-10-14T14:40:27Z` — **timeline** — milestoned** by MrAlias → v1.39.0
- `2025-11-09T19:52:08Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/issues/7592
- `2025-12-05T18:12:13Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7676
- `2025-12-08T16:30:51Z` — **timeline** — referenced** by MrAlias
- `2025-12-11T16:56:05Z` — **timeline** — referenced** by dashpole
- `2025-12-16T08:23:15Z` — **timeline** — referenced** by dmathieu
- `2026-01-16T17:11:30Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796

### SRC-PR-05 — `work-registry/opentelemetry/pulls/opentelemetry-go-7443.md` (95 records)

- `2025-10-02T13:56:40Z` — **source-created** — source created
- `2025-10-02T13:58:33Z` — **discussion** — **codecov[bot]** — 2025-10-02T13:58:33Z
- `2025-10-02T13:59:40Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-02T14:00:03Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-02T16:38:47Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7447
- `2025-10-02T18:03:34Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-specification/issues/4675
- `2025-10-03T13:20:44Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-03T13:27:37Z` — **timeline** — ready_for_review** by dashpole
- `2025-10-03T13:27:38Z` — **timeline** — review_requested** by dashpole
- `2025-10-03T13:27:38Z` — **timeline** — review_requested** by dashpole
- `2025-10-03T13:27:38Z` — **timeline** — review_requested** by dashpole
- `2025-10-03T13:27:38Z` — **timeline** — review_requested** by dashpole
- `2025-10-03T13:27:38Z` — **timeline** — review_requested** by dashpole
- `2025-10-03T15:57:03Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T15:57:03Z
- `2025-10-03T16:04:03Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:04:03Z
- `2025-10-03T16:04:21Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T16:04:21Z
- `2025-10-03T16:12:32Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:12:32Z
- `2025-10-03T16:12:33Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T16:12:33Z
- `2025-10-03T16:34:09Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:34:09Z
- `2025-10-03T16:34:09Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T16:34:09Z
- `2025-10-03T17:34:51Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T17:34:51Z
- `2025-10-03T17:34:51Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T17:34:51Z
- `2025-10-03T20:12:48Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T20:12:48Z
- `2025-10-03T20:12:48Z` — **review** — **dashpole** — COMMENTED — 2025-10-03T20:12:48Z
- `2025-10-03T22:44:49Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T22:44:49Z
- `2025-10-03T22:44:49Z` — **review** — **MrAlias** — COMMENTED — 2025-10-03T22:44:49Z
- `2025-10-04T03:36:32Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7453
- `2025-10-04T03:45:15Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-04T03:45:24Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-04T03:45:24Z
- `2025-10-04T03:45:24Z` — **review** — **dashpole** — COMMENTED — 2025-10-04T03:45:24Z
- `2025-10-04T03:47:24Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-06T16:03:00Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7458
- `2025-10-07T14:40:19Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-07T15:22:00Z` — **timeline** — referenced** by dashpole
- `2025-10-07T15:50:17Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-07T15:50:17Z
- `2025-10-07T15:50:33Z` — **review** — **MrAlias** — APPROVED — 2025-10-07T15:50:33Z
- `2025-10-10T13:10:45Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-10-12T20:38:18Z` — **inline-review** — **bboreham** on `sdk/metric/exemplar/storage.go` — 2025-10-12T20:38:18Z
- `2025-10-12T21:21:19Z` — **inline-review** — **bboreham** on `sdk/metric/exemplar/storage.go` — 2025-10-12T21:21:19Z
- `2025-10-12T21:22:58Z` — **review** — **bboreham** — COMMENTED — 2025-10-12T21:22:58Z
- `2025-10-13T14:23:19Z` — **discussion** — **bboreham** — 2025-10-13T14:23:19Z
- `2025-10-15T01:01:40Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-15T01:06:50Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-15T01:06:50Z
- `2025-10-15T01:06:50Z` — **review** — **dashpole** — COMMENTED — 2025-10-15T01:06:50Z
- `2025-10-15T01:08:33Z` — **discussion** — **dashpole** — 2025-10-15T01:08:33Z
- `2025-10-15T15:38:27Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-15T15:40:05Z` — **discussion** — **dashpole** — 2025-10-15T15:40:05Z
- `2025-10-15T16:22:27Z` — **inline-review** — **bboreham** on `sdk/metric/exemplar/reservoir_test.go` — 2025-10-15T16:22:27Z
- `2025-10-15T16:23:32Z` — **review** — **bboreham** — APPROVED — 2025-10-15T16:23:32Z
- `2025-10-15T16:31:22Z` — **discussion** — **dashpole** — 2025-10-15T16:31:22Z
- `2025-10-15T20:00:14Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-15T20:02:58Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-15T20:05:58Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/reservoir_test.go` — 2025-10-15T20:05:58Z
- `2025-10-15T20:05:58Z` — **review** — **dashpole** — COMMENTED — 2025-10-15T20:05:58Z
- `2025-10-15T20:08:23Z` — **discussion** — **dashpole** — 2025-10-15T20:08:23Z
- `2025-10-15T20:08:31Z` — **timeline** — review_requested** by dashpole
- `2025-10-15T20:08:33Z` — **timeline** — review_requested** by dashpole
- `2025-10-15T20:12:05Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-16T10:25:31Z` — **inline-review** — **bboreham** on `sdk/metric/exemplar/fixed_size_reservoir.go` (line 132) — 2025-10-16T10:25:31Z
- `2025-10-16T10:30:55Z` — **inline-review** — **bboreham** on `sdk/metric/exemplar/storage.go` (line 62) — 2025-10-16T10:30:55Z
- `2025-10-16T10:31:14Z` — **review** — **bboreham** — APPROVED — 2025-10-16T10:31:14Z
- `2025-10-16T12:37:15Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/storage.go` (line 62) — 2025-10-16T12:37:15Z
- `2025-10-16T12:37:15Z` — **review** — **dashpole** — COMMENTED — 2025-10-16T12:37:15Z
- `2025-10-16T16:23:04Z` — **timeline** — milestoned** by MrAlias → v1.39.0
- `2025-11-06T21:10:56Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:10:56Z
- `2025-11-06T21:17:30Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:17:30Z
- `2025-11-06T21:18:27Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:18:27Z
- `2025-11-06T21:19:32Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 215) — 2025-11-06T21:19:32Z
- `2025-11-06T21:22:35Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 221) — 2025-11-06T21:22:35Z
- `2025-11-06T21:24:33Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:24:33Z
- `2025-11-06T21:27:17Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-11-06T21:27:17Z
- `2025-11-06T21:28:37Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 208) — 2025-11-06T21:28:37Z
- `2025-11-06T21:30:53Z` — **review** — **MrAlias** — COMMENTED — 2025-11-06T21:30:53Z
- `2025-11-20T16:10:01Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-11-20T16:11:59Z` — **inline-review** — **dashpole** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-11-20T16:11:59Z
- `2025-11-20T16:11:59Z` — **review** — **dashpole** — COMMENTED — 2025-11-20T16:11:59Z
- `2025-12-04T18:10:27Z` — **timeline** — review_requested** by MrAlias
- `2025-12-04T18:10:37Z` — **timeline** — demilestoned** by MrAlias → v1.39.0
- `2025-12-04T18:10:37Z` — **timeline** — milestoned** by MrAlias → v1.40.0
- `2025-12-11T17:06:00Z` — **inline-review** — **MrAlias** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-12-11T17:06:00Z
- `2025-12-11T17:06:00Z` — **review** — **MrAlias** — COMMENTED — 2025-12-11T17:06:00Z
- `2025-12-11T17:22:43Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-12-11T17:24:14Z` — **discussion** — **dashpole** — 2025-12-11T17:24:14Z
- `2025-12-11T18:33:50Z` — **review** — **MrAlias** — APPROVED — 2025-12-11T18:33:50Z
- `2025-12-11T19:04:33Z` — **discussion** — **dashpole** — 2025-12-11T19:04:33Z
- `2025-12-11T20:43:53Z` — **discussion** — **dashpole** — 2025-12-11T20:43:53Z
- `2025-12-15T10:46:18Z` — **review** — **dmathieu** — APPROVED — 2025-12-15T10:46:18Z
- `2025-12-15T14:59:34Z` — **merged-header** — merged_at header; duplicate of its timeline event
- `2025-12-15T14:59:34Z` — **timeline** — closed** by dashpole
- `2025-12-15T14:59:34Z` — **timeline** — merged** by dashpole
- `2025-12-15T14:59:42Z` — **timeline** — head_ref_deleted** by dashpole
- `2026-01-16T17:11:30Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796
- `2026-01-23T14:27:45Z` — **timeline** — referenced** by dashpole
- `2026-02-02T17:06:10Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7859
- `2026-02-02T17:46:36Z` — **timeline** — referenced** by MrAlias

### SRC-PR-06 — `work-registry/opentelemetry/pulls/opentelemetry-go-7474.md` (116 records)

- `2025-10-08T14:31:21Z` — **source-created** — source created
- `2025-10-08T14:34:56Z` — **discussion** — **codecov[bot]** — 2025-10-08T14:34:56Z
- `2025-10-08T16:15:19Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T16:52:19Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T17:04:16Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T18:22:08Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T18:23:31Z` — **timeline** — ready_for_review** by dashpole
- `2025-10-08T18:23:31Z` — **timeline** — review_requested** by dashpole
- `2025-10-08T18:23:31Z` — **timeline** — review_requested** by dashpole
- `2025-10-08T18:23:31Z` — **timeline** — review_requested** by dashpole
- `2025-10-08T18:23:32Z` — **timeline** — review_requested** by dashpole
- `2025-10-08T18:23:32Z` — **timeline** — review_requested** by dashpole
- `2025-10-08T18:24:59Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T18:37:34Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T18:55:57Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-08T19:23:19Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7478
- `2025-10-08T22:16:25Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-08T22:16:25Z
- `2025-10-08T22:17:45Z` — **review** — **MrAlias** — COMMENTED — 2025-10-08T22:17:45Z
- `2025-10-09T12:40:04Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-09T12:40:04Z
- `2025-10-09T12:40:04Z` — **review** — **dashpole** — COMMENTED — 2025-10-09T12:40:04Z
- `2025-10-09T18:29:01Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-09T18:29:01Z
- `2025-10-09T18:29:01Z` — **review** — **dashpole** — COMMENTED — 2025-10-09T18:29:01Z
- `2025-10-10T13:10:45Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-10-10T15:21:23Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T15:21:23Z
- `2025-10-10T15:21:23Z` — **review** — **MrAlias** — COMMENTED — 2025-10-10T15:21:23Z
- `2025-10-10T15:43:13Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T15:43:13Z
- `2025-10-10T15:44:05Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` (line 18) — 2025-10-10T15:44:05Z
- `2025-10-10T15:52:01Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T15:52:01Z
- `2025-10-10T15:55:58Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T15:55:58Z
- `2025-10-10T16:05:36Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` (line 113) — 2025-10-10T16:05:36Z
- `2025-10-10T16:08:06Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T16:08:06Z
- `2025-10-10T16:08:31Z` — **review** — **MrAlias** — COMMENTED — 2025-10-10T16:08:31Z
- `2025-10-10T18:14:37Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 18) — 2025-10-10T18:14:37Z
- `2025-10-10T18:14:37Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T18:14:37Z
- `2025-10-10T18:18:00Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T18:18:00Z
- `2025-10-10T18:18:00Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T18:18:00Z
- `2025-10-10T18:20:03Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T18:20:03Z
- `2025-10-10T18:20:03Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T18:20:03Z
- `2025-10-10T19:38:13Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-10T19:38:26Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T19:38:26Z
- `2025-10-10T19:38:26Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T19:38:26Z
- `2025-10-10T19:39:24Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T19:39:24Z
- `2025-10-10T19:39:24Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T19:39:24Z
- `2025-10-10T19:41:04Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 113) — 2025-10-10T19:41:04Z
- `2025-10-10T19:41:04Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T19:41:04Z
- `2025-10-10T19:41:26Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T19:41:26Z
- `2025-10-10T19:41:26Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T19:41:26Z
- `2025-10-10T20:10:16Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T20:10:16Z
- `2025-10-10T20:10:16Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T20:10:16Z
- `2025-10-10T20:20:43Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T20:20:43Z
- `2025-10-10T20:20:43Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T20:20:43Z
- `2025-10-10T20:20:50Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T20:20:50Z
- `2025-10-10T20:20:50Z` — **review** — **dashpole** — COMMENTED — 2025-10-10T20:20:50Z
- `2025-10-11T02:01:19Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-12T14:42:30Z` — **inline-review** — **MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-12T14:42:30Z
- `2025-10-12T14:42:30Z` — **review** — **MrAlias** — COMMENTED — 2025-10-12T14:42:30Z
- `2025-10-15T00:52:11Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-15T00:52:35Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-15T00:52:35Z
- `2025-10-15T00:52:35Z` — **review** — **dashpole** — COMMENTED — 2025-10-15T00:52:35Z
- `2025-10-15T20:14:54Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-10-16T16:23:50Z` — **timeline** — milestoned** by MrAlias → v1.39.0
- `2025-10-24T19:58:30Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7535
- `2025-11-07T05:52:15Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T05:52:15Z
- `2025-11-07T05:53:31Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T05:53:31Z
- `2025-11-07T07:59:20Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T07:59:20Z
- `2025-11-07T08:01:04Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T08:01:04Z
- `2025-11-07T08:37:45Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:37:45Z
- `2025-11-07T08:39:07Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T08:39:07Z
- `2025-11-07T08:39:56Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 60) — 2025-11-07T08:39:56Z
- `2025-11-07T08:45:06Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:45:06Z
- `2025-11-07T08:46:38Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 255) — 2025-11-07T08:46:38Z
- `2025-11-07T08:46:47Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:46:47Z
- `2025-11-07T08:51:55Z` — **inline-review** — **bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-07T08:51:55Z
- `2025-11-07T08:53:56Z` — **review** — **bwplotka** — COMMENTED — 2025-11-07T08:53:56Z
- `2025-11-07T15:19:44Z` — **discussion** — **dashpole** — 2025-11-07T15:19:44Z
- `2025-11-07T15:22:59Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 60) — 2025-11-07T15:22:59Z
- `2025-11-07T15:22:59Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T15:22:59Z
- `2025-11-07T15:23:19Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 255) — 2025-11-07T15:23:19Z
- `2025-11-07T15:23:19Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T15:23:19Z
- `2025-11-07T17:16:04Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T17:16:04Z
- `2025-11-07T17:16:04Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T17:16:04Z
- `2025-11-07T17:21:32Z` — **timeline** — cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/issues/7589
- `2025-11-07T17:21:55Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T17:21:55Z
- `2025-11-07T17:21:55Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T17:21:55Z
- `2025-11-07T17:30:19Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T17:30:19Z
- `2025-11-07T17:30:19Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T17:30:19Z
- `2025-11-07T17:30:47Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T17:30:47Z
- `2025-11-07T17:30:47Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T17:30:47Z
- `2025-11-07T17:31:44Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T17:31:44Z
- `2025-11-07T17:31:44Z` — **review** — **dashpole** — COMMENTED — 2025-11-07T17:31:44Z
- `2025-11-10T16:17:44Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-10T16:17:44Z
- `2025-11-10T16:17:44Z` — **review** — **dashpole** — COMMENTED — 2025-11-10T16:17:44Z
- `2025-11-10T16:24:27Z` — **timeline** — head_ref_force_pushed** by dashpole
- `2025-11-10T16:24:40Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-10T16:24:40Z
- `2025-11-10T16:24:41Z` — **review** — **dashpole** — COMMENTED — 2025-11-10T16:24:41Z
- `2025-11-12T14:59:04Z` — **inline-review** — **dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-12T14:59:04Z
- `2025-11-12T14:59:04Z` — **review** — **dashpole** — COMMENTED — 2025-11-12T14:59:04Z
- `2025-12-04T17:44:24Z` — **review** — **MrAlias** — APPROVED — 2025-12-04T17:44:24Z
- `2025-12-04T18:09:42Z` — **discussion** — **MrAlias** — 2025-12-04T18:09:42Z
- `2025-12-04T18:09:56Z` — **timeline** — demilestoned** by MrAlias → v1.39.0
- `2025-12-04T18:09:56Z` — **timeline** — milestoned** by MrAlias → v1.40.0
- `2025-12-09T14:41:46Z` — **review** — **dmathieu** — APPROVED — 2025-12-09T14:41:46Z
- `2025-12-09T16:07:17Z` — **inline-review** — **dashpole** on `CHANGELOG.md` — 2025-12-09T16:07:17Z
- `2025-12-09T16:07:17Z` — **review** — **dashpole** — COMMENTED — 2025-12-09T16:07:17Z
- `2025-12-09T16:50:12Z` — **discussion** — **dashpole** — 2025-12-09T16:50:12Z
- `2025-12-09T16:57:34Z` — **discussion** — **MrAlias** — 2025-12-09T16:57:34Z
- `2025-12-09T17:10:55Z` — **discussion** — **MrAlias** — 2025-12-09T17:10:55Z
- `2025-12-11T16:49:43Z` — **discussion** — **dashpole** — 2025-12-11T16:49:43Z
- `2025-12-11T16:56:04Z` — **merged-header** — merged_at header; duplicate of its timeline event
- `2025-12-11T16:56:04Z` — **timeline** — closed** by dashpole
- `2025-12-11T16:56:04Z` — **timeline** — merged** by dashpole
- `2025-12-11T16:56:08Z` — **timeline** — head_ref_deleted** by dashpole
- `2025-12-16T08:23:14Z` — **timeline** — referenced** by dmathieu
- `2026-01-16T17:11:30Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796
- `2026-02-02T17:06:10Z` — **timeline** — cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7859
- `2026-02-02T17:46:35Z` — **timeline** — referenced** by MrAlias

### SRC-PR-01 — `work-registry/opentelemetry/pulls/opentelemetry-go-contrib-6609.md` (75 records)

- `2025-01-13T13:45:43Z` — **source-created** — source created
- `2025-01-13T13:45:44Z` — **timeline** — review_requested** by Yiling-J
- `2025-01-13T13:45:52Z` — **discussion** — **linux-foundation-easycla[bot]** — 2025-01-13T13:45:52Z
- `2025-01-13T13:45:57Z` — **timeline** — review_requested** by github-actions[bot]
- `2025-01-13T14:15:46Z` — **discussion** — **codecov[bot]** — 2025-01-13T14:15:46Z
- `2025-01-13T14:56:36Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T14:56:36Z
- `2025-01-13T14:59:10Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T14:59:10Z
- `2025-01-13T15:02:32Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T15:02:32Z
- `2025-01-13T15:02:41Z` — **review** — **flc1125** — COMMENTED — 2025-01-13T15:02:41Z
- `2025-01-13T15:27:41Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T15:27:41Z
- `2025-01-13T15:27:41Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-13T15:27:41Z
- `2025-01-13T15:31:16Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-13T15:31:16Z
- `2025-01-13T15:31:16Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-13T15:31:16Z
- `2025-01-13T15:35:44Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T15:35:44Z
- `2025-01-13T15:35:45Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-13T15:35:45Z
- `2025-01-13T16:19:36Z` — **discussion** — **flc1125** — 2025-01-13T16:19:36Z
- `2025-01-13T16:20:13Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-01-13T16:20:13Z
- `2025-01-13T16:20:13Z` — **review** — **flc1125** — COMMENTED — 2025-01-13T16:20:13Z
- `2025-01-14T08:12:17Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gintrace.go` — 2025-01-14T08:12:17Z
- `2025-01-14T08:13:50Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/test/gintrace_test.go` — 2025-01-14T08:13:50Z
- `2025-01-14T08:21:31Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T08:21:31Z
- `2025-01-14T08:21:37Z` — **review** — **dmathieu** — COMMENTED — 2025-01-14T08:21:37Z
- `2025-01-14T14:39:53Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T14:39:53Z
- `2025-01-14T14:39:53Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-14T14:39:53Z
- `2025-01-14T14:55:45Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T14:55:45Z
- `2025-01-14T14:55:45Z` — **review** — **dmathieu** — COMMENTED — 2025-01-14T14:55:45Z
- `2025-01-14T15:29:23Z` — **discussion** — **Yiling-J** — 2025-01-14T15:29:23Z
- `2025-01-14T15:31:10Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T15:31:10Z
- `2025-01-14T15:31:10Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-14T15:31:10Z
- `2025-01-14T16:18:27Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T16:18:27Z
- `2025-01-14T16:18:27Z` — **review** — **dmathieu** — COMMENTED — 2025-01-14T16:18:27Z
- `2025-01-14T17:44:13Z` — **inline-review** — **akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:44:13Z
- `2025-01-14T17:44:13Z` — **review** — **akats7** — COMMENTED — 2025-01-14T17:44:13Z
- `2025-01-14T17:49:47Z` — **inline-review** — **akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:49:47Z
- `2025-01-14T17:49:48Z` — **review** — **akats7** — COMMENTED — 2025-01-14T17:49:48Z
- `2025-01-14T17:50:46Z` — **inline-review** — **dmathieu** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-14T17:50:46Z
- `2025-01-14T17:50:46Z` — **review** — **dmathieu** — COMMENTED — 2025-01-14T17:50:46Z
- `2025-01-19T18:17:34Z` — **inline-review** — **akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-19T18:17:34Z
- `2025-01-19T18:17:46Z` — **review** — **akats7** — COMMENTED — 2025-01-19T18:17:46Z
- `2025-01-20T01:52:04Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-20T01:52:04Z
- `2025-01-20T01:52:04Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-20T01:52:04Z
- `2025-01-22T15:54:04Z` — **timeline** — cross-referenced** by Yiling-J ← https://github.com/golang/go/issues/71382
- `2025-01-27T12:14:50Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-01-27T12:14:50Z
- `2025-01-27T12:14:50Z` — **review** — **Yiling-J** — COMMENTED — 2025-01-27T12:14:50Z
- `2025-07-03T13:24:53Z` — **timeline** — cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/issues/5946
- `2025-11-03T09:18:09Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- `2025-11-03T13:01:49Z` — **discussion** — **flc1125** — 2025-11-03T13:01:49Z
- `2025-11-03T15:41:21Z` — **discussion** — **Yiling-J** — 2025-11-03T15:41:21Z
- `2025-11-04T00:35:28Z` — **discussion** — **flc1125** — 2025-11-04T00:35:28Z
- `2025-11-04T01:19:00Z` — **discussion** — **Yiling-J** — 2025-11-04T01:19:00Z
- `2025-11-10T01:45:42Z` — **discussion** — **akats7** — 2025-11-10T01:45:42Z
- `2025-11-10T01:53:34Z` — **discussion** — **flc1125** — 2025-11-10T01:53:34Z
- `2025-11-10T02:01:52Z` — **discussion** — **akats7** — 2025-11-10T02:01:52Z
- `2025-11-10T04:27:26Z` — **discussion** — **akats7** — 2025-11-10T04:27:26Z
- `2025-11-10T11:58:48Z` — **discussion** — **Yiling-J** — 2025-11-10T11:58:48Z
- `2025-11-10T14:01:14Z` — **inline-review** — **flc1125** on `CHANGELOG.md` — 2025-11-10T14:01:14Z
- `2025-11-10T14:02:13Z` — **review** — **flc1125** — COMMENTED — 2025-11-10T14:02:13Z
- `2025-11-10T14:02:53Z` — **discussion** — **flc1125** — 2025-11-10T14:02:53Z
- `2025-11-10T14:03:40Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 109) — 2025-11-10T14:03:40Z
- `2025-11-10T14:03:40Z` — **review** — **flc1125** — COMMENTED — 2025-11-10T14:03:40Z
- `2025-11-10T14:03:54Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin.go` (line 117) — 2025-11-10T14:03:54Z
- `2025-11-10T14:03:54Z` — **review** — **flc1125** — COMMENTED — 2025-11-10T14:03:54Z
- `2025-11-10T15:21:14Z` — **discussion** — **Yiling-J** — 2025-11-10T15:21:14Z
- `2025-11-10T16:20:02Z` — **review** — **akats7** — APPROVED — 2025-11-10T16:20:02Z
- `2025-11-11T13:20:30Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T13:20:30Z
- `2025-11-11T13:20:30Z` — **review** — **flc1125** — COMMENTED — 2025-11-11T13:20:30Z
- `2025-11-11T13:59:33Z` — **inline-review** — **flc1125** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T13:59:33Z
- `2025-11-11T13:59:33Z` — **review** — **flc1125** — COMMENTED — 2025-11-11T13:59:33Z
- `2025-11-11T14:00:20Z` — **timeline** — cross-referenced** by flc1125 ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8161
- `2025-11-11T15:42:57Z` — **inline-review** — **akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-11T15:42:57Z
- `2025-11-11T15:42:57Z` — **review** — **akats7** — COMMENTED — 2025-11-11T15:42:57Z
- `2025-11-12T01:28:14Z` — **inline-review** — **Yiling-J** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-12T01:28:14Z
- `2025-11-12T01:28:14Z` — **review** — **Yiling-J** — COMMENTED — 2025-11-12T01:28:14Z
- `2025-11-12T10:24:52Z` — **inline-review** — **akats7** on `instrumentation/github.com/gin-gonic/gin/otelgin/gin_test.go` (line 512) — 2025-11-12T10:24:52Z
- `2025-11-12T10:24:52Z` — **review** — **akats7** — COMMENTED — 2025-11-12T10:24:52Z

### SRC-PR-07 — `work-registry/opentelemetry/pulls/opentelemetry-go-contrib-8014.md` (35 records)

- `2025-10-14T04:01:24Z` — **source-created** — source created
- `2025-10-14T04:01:31Z` — **discussion** — **linux-foundation-easycla[bot]** — 2025-10-14T04:01:31Z
- `2025-10-14T04:05:44Z` — **timeline** — ready_for_review** by nicksherron
- `2025-10-14T04:05:44Z` — **timeline** — review_requested** by nicksherron
- `2025-10-14T04:05:44Z` — **timeline** — review_requested** by nicksherron
- `2025-10-14T04:05:53Z` — **timeline** — review_requested** by github-actions[bot]
- `2025-10-14T04:35:20Z` — **discussion** — **flc1125** — 2025-10-14T04:35:20Z
- `2025-10-14T04:43:31Z` — **discussion** — **nicksherron** — 2025-10-14T04:43:31Z
- `2025-10-14T04:56:41Z` — **discussion** — **nicksherron** — 2025-10-14T04:56:41Z
- `2025-10-14T04:58:07Z` — **discussion** — **akats7** — 2025-10-14T04:58:07Z
- `2025-10-14T05:01:16Z` — **discussion** — **flc1125** — 2025-10-14T05:01:16Z
- `2025-10-14T05:06:09Z` — **discussion** — **nicksherron** — 2025-10-14T05:06:09Z
- `2025-10-14T05:09:52Z` — **discussion** — **flc1125** — 2025-10-14T05:09:52Z
- `2025-10-14T05:13:28Z` — **discussion** — **akats7** — 2025-10-14T05:13:28Z
- `2025-10-14T05:13:48Z` — **discussion** — **nicksherron** — 2025-10-14T05:13:48Z
- `2025-10-14T05:19:18Z` — **discussion** — **nicksherron** — 2025-10-14T05:19:18Z
- `2025-10-14T05:23:38Z` — **discussion** — **nicksherron** — 2025-10-14T05:23:38Z
- `2025-10-14T06:05:25Z` — **discussion** — **flc1125** — 2025-10-14T06:05:25Z
- `2025-10-14T06:52:09Z` — **discussion** — **nicksherron** — 2025-10-14T06:52:09Z
- `2025-10-14T06:58:23Z` — **discussion** — **nicksherron** — 2025-10-14T06:58:23Z
- `2025-10-14T07:26:23Z` — **discussion** — **dmathieu** — 2025-10-14T07:26:23Z
- `2025-10-14T07:27:58Z` — **discussion** — **nicksherron** — 2025-10-14T07:27:58Z
- `2025-10-14T07:42:26Z` — **discussion** — **flc1125** — 2025-10-14T07:42:26Z
- `2025-10-14T07:47:23Z` — **discussion** — **nicksherron** — 2025-10-14T07:47:23Z
- `2025-10-14T07:50:11Z` — **discussion** — **codecov[bot]** — 2025-10-14T07:50:11Z
- `2025-10-14T07:52:18Z` — **review** — **akats7** — APPROVED — 2025-10-14T07:52:18Z
- `2025-10-14T07:54:22Z` — **discussion** — **dmathieu** — 2025-10-14T07:54:22Z
- `2025-10-14T08:01:45Z` — **discussion** — **akats7** — 2025-10-14T08:01:45Z
- `2025-10-14T08:34:20Z` — **discussion** — **nicksherron** — 2025-10-14T08:34:20Z
- `2025-10-14T08:42:01Z` — **discussion** — **dmathieu** — 2025-10-14T08:42:01Z
- `2025-10-14T08:48:08Z` — **discussion** — **nicksherron** — 2025-10-14T08:48:08Z
- `2025-10-14T08:59:49Z` — **discussion** — **nicksherron** — 2025-10-14T08:59:49Z
- `2025-10-17T10:41:58Z` — **discussion** — **dmathieu** — 2025-10-17T10:41:58Z
- `2025-10-17T10:41:58Z` — **timeline** — closed** by dmathieu
- `2025-11-03T09:18:09Z` — **timeline** — cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648

### SRC-REL-01 — `work-registry/opentelemetry/releases/release-v1.39.0.md` (2 records)

- `2025-12-08T16:32:32Z` — **source-created** — source created
- `2025-12-08T16:45:46Z` — **release-published** — release published

### Inventory check

- source-created: 26
- merged-header: 5
- discussion: 140
- review: 118
- inline-review: 139
- timeline: 225
- release-published: 1
- **Total: 654**
