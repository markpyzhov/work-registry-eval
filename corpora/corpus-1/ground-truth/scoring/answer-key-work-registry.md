# Corpus 1 — Work Registry answer key

Use for `workrag` and `directory`. Final Work State is authoritative.

## Q01 — Release readiness

**Verdict:** Not ready to ship v1.0.0.

**Required facts:**

- `SRC-SLACK-06`, `SRC-CU-CIPH-15` — T005 is reopened.
- `SRC-SLACK-06` — The image measured 2.1GB, above the ~450MB target.
- `SRC-SLACK-06`, `SRC-CU-CIPH-15` — CVE verification is failing.
- `SRC-CU-CIPH-39` — T029 is open.
- `SRC-SLACK-37`, `SRC-CU-CIPH-39` — T029 code signing is unresolved.
- `SRC-CU-CIPH-26` — T016 is open.
- `SRC-GDOC-11`, `SRC-CU-CIPH-26` — T016 has an audit-schema mismatch.
- `SRC-CU-CIPH-40` — T030 is open.
- `SRC-SLACK-40`, `SRC-CU-CIPH-40` — T030's candidate parser is AGPL.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — T011 is held on T005 and T029.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — Stale completion claims do not clear current gates.

**Optional:** `WS-03` — 2026-10-15 no-ship deadline (Q01 does not ask for the deadline).

**Incorrect if:**

- Ship/go verdict.
- Fewer than three of T005, T029, T016, and T030.

## Q02 — Docker supersession

**Verdict:** T005 is Active (Reopened), not complete.

**Required facts:**

- `SRC-GDOC-06` — Completed June 16.
- `SRC-SLACK-06` — Reopened June 25.
- `SRC-SLACK-06` — The 2.1GB result triggered the reopen.
- `SRC-GDOC-06`, `SRC-SLACK-06` — June 25 supersedes June 16.
- `SRC-SLACK-06` — Still above ~450MB.
- `WS-03` — RC size limit: no more than 800MB.
- `WS-03` — RC requires clean CVE verification.
- `WS-03` — GA: approximately 450MB.
- `SRC-SLACK-06` — CVE verification still failing.

**Incorrect if:**

- Complete or release-ready.

## Q03 — Large-file chunking

**Verdict:** T031 is Active (Reopened).

**Required facts:**

- `SRC-SLACK-44` — Merged/marked done August 16.
- `SRC-SLACK-43` — Reopened August 18.
- `SRC-SLACK-43` — Buffers remained retained after each chunk.
- `SRC-SLACK-43` — The retained buffers caused leaks on files over 2GB.
- `SRC-CU-CIPH-41` — Charlie owns the buffer-release refactor.

**Optional:** `WS-05` — MedFirst OOM on a 4.7GB file and 8GB workstation.

**Incorrect if:**

- Still complete.
- Wrong owner.

## Q04 — Storage quota

**Verdict:** T022 is Active (Reopened).

**Required facts:**

- `SRC-SLACK-23`, `SRC-GDOC-36` — The 500MB hard halt was completed August 6.
- `SRC-SLACK-23`, `SRC-GDOC-36` — T022 reopened September 15.
- `SRC-SLACK-23`, `SRC-GDOC-36` — The 500MB halt was too aggressive.
- `SRC-CU-CIPH-32` — 10% buffer refactor underway.

**Optional:** `WS-07` — Current production baseline: 2GB free disk.

**Incorrect if:**

- Completed.

## Q05 — License gate

**Verdict:** T030 is Active (Reopened); license gate not cleared.

**Required facts:**

- `SRC-SLACK-40`, `SRC-CU-CIPH-40` — Candidate replacement parser is AGPL.
- `SRC-SLACK-40` — AGPL is a distribution dealbreaker.
- `SRC-MEET-08`, `SRC-CU-CIPH-40` — Charlie is seeking an Apache- or MIT-licensed alternative.
- `WS-04` — Legal: whole-bundle copyleft.
- `WS-04` — P0 Legal gate.
- `WS-04` — Engineering search alone cannot close the gate.

**Incorrect if:**

- License review complete.

## Q06 — Release-gate order and ownership

**Verdict:** T011 waits on T005 and T029; T016 and T030 also remain open.

**Required facts:**

- `SRC-CU-CIPH-15` — T005's listed assignee is Evan.
- `SRC-SLACK-06` — Evan owns the T005 image/CVE action.
- `SRC-CU-CIPH-39` — T029's listed assignee is Evan.
- `SRC-SLACK-37` — Alice owns T029 certificate procurement.
- `SRC-CU-CIPH-26` — T016's listed assignee is Diana.
- `SRC-CU-CIPH-26`, `SRC-MEET-08` — Diana owns T016 schema verification.
- `SRC-CU-CIPH-40` — T030's listed assignee is Diana.
- `SRC-CU-CIPH-40`, `SRC-MEET-08` — Charlie owns the T030 parser search.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — The earlier “only T005 remains” claim is stale.

**Incorrect if:**

- T011 closes before T005 and T029.
- T029 or T030 ownership is collapsed.

## Q07 — Blocked inventory

**Verdict:** Blocked: T007, T019, T024, T036, and T037.

**Required facts:**

- `SRC-CU-CIPH-17`, `SRC-SLACK-07` — T007 is blocked on upstream pdfminer #992.
- `WS-01` — T007 also requires Legal sign-off.
- `SRC-CU-CIPH-17` — T007's listed assignee is Charlie.
- `WS-01` — T007 is a mixed external/internal wait.
- `WS-04` — T019 has an approved split-escrow design.
- `WS-04` — The T019 split escrow is not implemented.
- `SRC-CU-CIPH-29` — T019's listed assignee is Diana.
- `WS-04` — T019 is an internal block.
- `SRC-CU-CIPH-34`, `SRC-SLACK-27` — T024 is blocked on high-latency handshake timeouts.
- `SRC-CU-CIPH-34` — T024's listed assignee is Bob.
- `WS-07` — T024 is an internal block.
- `SRC-CU-CIPH-46`, `SRC-SLACK-58` — T036 is blocked on an upstream scaling problem.
- `WS-06` — T036 also affects nested Form XObjects.
- `SRC-CU-CIPH-46` — T036's listed assignee is Charlie.
- `WS-06` — T036 is a mixed external/internal wait.
- `SRC-CU-CIPH-47`, `SRC-SLACK-61` — T037 is blocked on a concurrent I/O race.
- `SRC-CU-CIPH-47` — T037's listed assignee is Bob.
- `WS-05` — T037 is an internal block.

**Optional:**

- `SRC-SLACK-07` — The T007 local fork was rejected.
- `SRC-MEET-11` — T024 has no accepted workaround.
- `SRC-MEET-11` — The simple T024 timeout bump was declined.
- `SRC-CU-CIPH-47`, `SRC-SLACK-61` — T037 causes about 10% throughput loss.
- `WS-07` — The Singapore trial ran at 180ms RTT.
- `WS-07` — High-latency planning uses a 30s budget.
- `WS-04` — Bob is spiking the T019 implementation.

**Incorrect if:**

- Three or fewer durable blockers.
- Reopened Active work classified as Blocked.

## Q08 — Windows release gate

**Verdict:** Working unsigned artifact; release gate not cleared.

**Required facts:**

- `SRC-SLACK-37`, `SRC-CU-CIPH-39` — Defender/SmartScreen flags unsigned binaries.
- `SRC-SLACK-37`, `SRC-CU-CIPH-39` — Authenticode/code-signing certificate missing.
- `SRC-MEET-08`, `SRC-MEET-10` — No firm signing timeline.

**Optional:** `SRC-SLACK-37` — Alice is following up on certificate procurement.

**Incorrect if:**

- Engineering completion treated as release readiness.

## Q09 — Compliance holds

**Verdict:** T016 and T030 remain open.

**Required facts:**

- `SRC-GDOC-11`, `SRC-CU-CIPH-26` — T016 requires input SHA-256 plus a redaction map.
- `SRC-CU-CIPH-26` — T016 CLI output mismatches the schema.
- `SRC-SLACK-40`, `SRC-CU-CIPH-40` — T030 requires adoption of an Apache/MIT replacement so that no restrictive copyleft remains in the shipped dependency set.
- `WS-04` — Legal identified whole-bundle copyleft exposure.
- `WS-04` — T030 is a P0 Legal gate.
- `WS-04` — Engineering search alone cannot close T030.
- `SRC-CU-CIPH-26`, `SRC-MEET-10` — T010 completion does not clear T016.

**Incorrect if:**

- Either gate closed.

## Q10 — Management briefing

**Verdict:** Do not declare v1.0.0 ready.

**Required facts:**

- `SRC-SLACK-06`, `SRC-SLACK-23`, `SRC-SLACK-40`, `SRC-SLACK-43` — Separate durable completions from reopened work.
- `SRC-GDOC-05` — Name at least two durable completions from T001/T002/T003/T004/T006/T010.
- `SRC-SLACK-06`, `SRC-SLACK-23`, `SRC-SLACK-40`, `SRC-SLACK-43` — Name at least three reopened items from T005/T022/T030/T031.
- `SRC-SLACK-07`, `SRC-SLACK-17`, `SRC-MEET-11`, `SRC-SLACK-58`, `SRC-SLACK-61` — Name at least two durable blockers from T007/T019/T024/T036/T037.
- `SRC-SLACK-06`, `SRC-SLACK-40`, `SRC-SLACK-58` — Cover at least three workstreams.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — Escalate at least two of T005/T029/T016/T030.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — Give an actionable do-not-ship recommendation.

**Incorrect if:**

- Reopened work presented as complete.
- Blockers omitted.
- Single-workstream briefing.

## Q11 — Critical-path next actions

**Verdict:** T005 and T029 must both clear before T011.

**Required facts:**

- `SRC-SLACK-06`, `SRC-CU-CIPH-15` — Evan owns T005 image/CVE work.
- `SRC-SLACK-37` — Alice owns certificate procurement.
- `SRC-CU-CIPH-39` — Evan remains the listed T029 assignee.

**Optional:**

- `SRC-CU-CIPH-21`, `SRC-MEET-10` — No ordering between T005 and T029 is established.
- `SRC-CU-CIPH-26`, `SRC-MEET-08` — Diana owns T016 schema verification as parallel context.
- `SRC-CU-CIPH-40`, `SRC-MEET-08` — Charlie owns the T030 parser search as parallel context.

**Incorrect if:**

- T011 closes before T005/T029.
- A required order between T005 and T029 asserted.
- Certificate procurement assigned only to Evan.

## Q12 — Parallel work and waits

**Verdict:** Active work can proceed in parallel; T011 still waits on T005/T029.

**Required facts:**

- `SRC-SLACK-06`, `SRC-CU-CIPH-41` — Advancing work: at least one of T005/T008/T014/T016/T022/T030/T031.
- `WS-04` — T019 implementation can advance under the approved split escrow.
- `SRC-SLACK-07` — T007 waits on upstream #992.
- `SRC-SLACK-58` — T036 waits on upstream scaling.
- `SRC-CU-CIPH-21`, `SRC-MEET-10` — The sole-T005 checklist is stale.

**Optional:**

- `WS-04` — Bob is spiking the T019 implementation.
- `WS-04` — T019 remains blocked until the implementation is built.
- `WS-01` — T007 also waits on Legal sign-off.
- `WS-06` — T036 may require an internal Form XObject workaround.
- `WS-07` — T024 is internally blocked.
- `WS-05` — T037 is internally blocked.
- `SRC-MEET-11` — T024 timeout bump remains declined.

**Incorrect if:**

- T007/T036 treated as locally resolvable through rejected paths.
- T007/T036 treated as purely external.
- T024 cleared.
- T011 closes before T005/T029.

## Q13 — Business-rule control

**Verdict:** OCR starts; the exception makes the job fail closed.

**Required facts:**

- `SRC-SLACK-12`, `SRC-CU-CIPH-25` — Abort with no output.
- `SRC-SLACK-12`, `SRC-CU-CIPH-25` — Securely delete temporary files.
- `SRC-SLACK-12`, `SRC-CU-CIPH-25` — Write crash diagnostics to `audit_log.json`.
- `SRC-SLACK-11`, `SRC-CU-CIPH-24` — The manual-review threshold is 90%.
- `SRC-SLACK-11`, `SRC-CU-CIPH-24` — An 82% result normally requires review.
- `SRC-SLACK-12`, `SRC-CU-CIPH-25` — The abort prevents export despite the review threshold.
- `SRC-CU-CIPH-18` — T008 OCR remains unfinished.
- `SRC-CU-CIPH-24` — T014 manual-review workflow remains unfinished.
- `SRC-CU-CIPH-26` — T016 audit logging remains unfinished.

**Optional:**

- `SRC-GDOC-04`, `SRC-MEET-03` — Unusable native text triggers OCR (stated as a
  premise in the question; credit if given, never a `missing_fact`).
- `SRC-GDOC-04`, `SRC-MEET-03` — No 100-byte OCR trigger is established.

**Incorrect if:**

- `.failed` behavior asserted (stale June brief; absent from the final rule set) or a 100-byte trigger asserted.
- Partial export.
- T014 or T016 treated as complete.

## Q14 — Release deadline diagnostic

**Verdict:** Hard no-ship after 2026-10-15 if T005/T029 remain red.

**Required facts:**

- `WS-03` — T005 must clear before 2026-10-15 or shipping stops.
- `WS-03` — T029 must clear before 2026-10-15 or shipping stops.
- `WS-03` — The deadline replaces the earlier undated security-gate hold.

**Incorrect if:**

- Deadline treated as advisory.

## Q15 — High-latency timeout diagnostic

**Verdict:** T024 remains blocked; nominal-latency success is insufficient.

**Required facts:**

- `WS-07` — Singapore failed at 180ms RTT with the 5s prototype.
- `WS-07` — High-latency planning budget: 30s.
- `WS-07` — Nominal-latency pass does not clear field sign-off.
- `SRC-MEET-11` — The earlier simple timeout bump was declined.
- `WS-07` — The 30s budget is a planning requirement, not gate clearance.

**Incorrect if:**

- Nominal success treated as field sign-off.
