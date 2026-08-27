# Corpus 2 — Work Registry answer key

Use for `workrag` and `directory`. Final Work State is authoritative.

## Q-01 — Concurrent sum #7427

**Verdict:** Merged and released in v1.39.0.

**Required facts:**

- `SRC-REL-01` — Released in v1.39.0.
- `SRC-REL-01` — The v1.39.0 release evidence names #7427.

**Optional:**

- `SRC-PR-04` — Merged 2025-10-07.
- `SRC-REL-01` — v1.39.0 was published 2025-12-08.

**Incorrect if:**

- Unreleased.
- Different/later release invented.

## Q-02 — Runtime-tracer/profiling proposal

**Verdict:** Large public-API change deferred.

**Required facts:**

- `SRC-NOTE-08` — Keep PR as draft/proof of concept.
- `SRC-NOTE-08` — Open a documenting issue.
- `SRC-NOTE-08` — Start with a smaller disablement change.

**Incorrect if:**

- Large change approved for merge as-is.

## Q-03 — Histogram reservoir #7443

**Verdict:** Merged; release not established.

**Required facts:**

- `SRC-PR-05` — Merged.
- `SRC-REL-01` — No v1.40.0 release evidence.

**Optional:**

- `SRC-PR-05`, `SRC-MILE-02`, `SRC-MILE-03` — Milestone moved v1.39.0 → v1.40.0 on 2025-12-04.
- `SRC-PR-05` — Merged 2025-12-15.

**Incorrect if:**

- Merge/milestone treated as release.

## Q-04 — otelgin MultipartForm cleanup

**Verdict:** Automatic `MultipartForm.RemoveAll()` adopted; locally complete, publication pending.

**Required facts:**

- `SRC-ISSUE-01` — #5946 remains open.
- `SRC-PR-01` — #6609 remains open.
- `SRC-PR-01`, `WS-05` — #6609 remains unmerged; merge is pending.
- `WS-05` — Automatic `RemoveAll()` selected.
- `WS-05` — Cleanup is complete locally.
- `WS-05` — Publication is pending.

**Incorrect if:**

- Cleanup described only as unresolved, without the selected method and local completion.
- Merge/release claimed.

## Q-05 — Temporality-selector configuration

**Verdict:** Custom parsing rejected; selector functions shipped in v1.39.0.

**Required facts:**

- `SRC-NOTE-01`, `SRC-NOTE-03`, `SRC-NOTE-04` — SDK-specific parsing was rejected.
- `SRC-NOTE-01`, `SRC-NOTE-03`, `SRC-NOTE-04` — The full OpenTelemetry configuration format was selected instead.
- `SRC-REL-01` — The Delta selector function shipped.
- `SRC-REL-01` — The Cumulative selector function shipped.
- `SRC-REL-01` — The LowMemory selector function shipped.

**Incorrect if:**

- Custom parsing shipped.
- Selector functions rejected.

## Q-06 — SDK log Record #7403

**Verdict:** Merged and released in v1.39.0.

**Required facts:**

- `SRC-REL-01` — Released in v1.39.0.
- `SRC-REL-01` — Release notes name #7403.

**Optional:**

- `SRC-PR-03` — Merged 2025-10-16.
- `SRC-REL-01` — v1.39.0 published 2025-12-08.
- `SRC-REL-01` — Release notes identify the non-mutation fix.

**Incorrect if:**

- Unreleased or incomplete.

## Q-07 — OTelConf RC decision

**Verdict:** Merge as-is after review; track experimental API structure under v1.40.0.

**Required facts:**

- `SRC-NOTE-07` — Merge as-is after review.
- `SRC-NOTE-07` — Track structure under v1.40.0.

**Optional:**

- `SRC-NOTE-07` — Alex opens the tracking issue.
- `SRC-NOTE-07` — Reviewers review the RC PR.

**Incorrect if:**

- Decision treated as shipment proof.

## Q-08 — otelhttp #7254

**Verdict:** Closed/completed; named release not established.

**Required facts:**

- `SRC-ISSUE-02` — Closed as completed.

**Optional:**

- `SRC-ISSUE-02`, `SRC-MILE-02`, `SRC-MILE-04` — Moved v1.39.0 → v1.40.0.
- `SRC-ISSUE-02` — Closed 2026-01-13.
- `SRC-ISSUE-02`, `SRC-REL-01` — Closure is not named-release evidence.

**Incorrect if:**

- Issue still open.
- Named release claimed.

## Q-09 — Fixed-bucket histogram #7474

**Verdict:** Merged; release not established.

**Required facts:**

- `SRC-PR-06` — Merged.
- `SRC-REL-01` — No v1.40.0 release evidence.

**Optional:**

- `SRC-PR-06`, `SRC-MILE-02`, `SRC-MILE-03` — Milestone moved v1.39.0 → v1.40.0 on 2025-12-04.
- `SRC-PR-06` — Merged 2025-12-11.

**Incorrect if:**

- Merge/milestone treated as release.

## A-01 — MultipartForm cleanup: selection and status

**Verdict:** Automatic `MultipartForm.RemoveAll()` selected; locally complete, publication pending.

**Required facts:**

- `SRC-ISSUE-01` — #5946 is open.
- `SRC-PR-01` — #6609 is open.
- `SRC-PR-01` — #6609 is unmerged.
- `WS-05` — Automatic `RemoveAll()` selected.
- `WS-05` — Locally complete.
- `WS-05` — Publication is pending.
- `WS-05` — Final commits are unpushed.

**Incorrect if:**

- Abstention or older unresolved state.
- Cleanup asserted merged, published, or #5946/#6609 closed/resolved.

## A-02 — otelgrpc stabilization date

**Verdict:** No completion date established.

**Incorrect if:**

- Definite date named.

## A-03 — Immutable-release evidence and status

**Verdict:** v1.39.0 confirmed; broader enablement deferred/not done.

**Required facts:**

- `SRC-ISSUE-03`, `SRC-REL-01` — Immutable releases are confirmed working for Go and Go Contrib v1.39.0.
- `WS-03` — Broader enablement is deferred/not done.

**Optional:**

- `WS-03` — Deferral is pending release-tooling and asset-upload confirmation.
- `WS-03` — Issue closure is not delivery completion.

**Partial if:**

- Only the confirmed release or only the broader status is correct; no incorrect condition.

**Incorrect if:**

- Broader work called done.
- Another release or artifact invented.

## A-04 — Ecosystem Explorer delivery

**Verdict:** Delivery not established.

**Required facts:**

- `SRC-PR-02`, `SRC-NOTE-06` — Merged PR is a proposal, not implementation delivery.

**Incorrect if:**

- Explorer delivery claimed.

## A-05 — Why #8014 closed

**Verdict:** Proposed fix was incorrect; existing behavior is intentional.

**Required facts:**

- `SRC-PR-07`, `SRC-NOTE-04` — Proposed fix judged incorrect.
- `SRC-PR-07`, `SRC-NOTE-04` — Existing behavior intentional/proper.

**Incorrect if:**

- Abstention or different rationale.
- Merged/accepted.

## A-06 — OTelConf RC shipment

**Verdict:** Shipment not established.

**Required facts:**

- `SRC-NOTE-07` — Merge decision/review actions are not delivery evidence.

**Incorrect if:**

- Shipment claimed.
