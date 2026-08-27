# Event Ledger

| Event ID | Date | Actor | Item | Type | Why/Trigger | Resulting Status | Dependencies | Evidence |
|---|---|---|---|---|---|---|---|---|
| E001 | 2026-06-01 | Alice | T001 | Task Create | | Open | | SRC-CU-CIPH-11, SRC-MEET-01 |
| E002 | 2026-06-03 | Charlie | T001 | Code Commit | | Active | | SRC-SLACK-01 |
| E003 | 2026-06-05 | Diana | T001 | Review | | Completed | | SRC-CU-CIPH-11 |
| E048 | 2026-07-14 | Charlie | T001 | Release evidence archive of completed core engine | Release checklist prep needs frozen engine completion evidence for T011 | Completed | | SRC-CU-CIPH-11 |
| E004 | 2026-06-02 | Alice | T002 | Task Create | | Open | | SRC-CU-CIPH-12 |
| E005 | 2026-06-06 | Charlie | T002 | Implementation | | Active | T001 | SRC-SLACK-02, SRC-GDOC-01 |
| E006 | 2026-06-08 | Diana | T002 | Test Pass | | Completed | | SRC-GDOC-07 |
| E049 | 2026-07-14 | Diana | T002 | Post-completion financial-regex suite recheck | Confirm completed detection patterns remain green before HIPAA pattern merge work | Completed | | |
| E007 | 2026-06-04 | Alice | T003 | Task Create | | Open | | SRC-CU-CIPH-13 |
| E008 | 2026-06-09 | Bob | T003 | Implementation | | Active | | SRC-GDOC-02 |
| E009 | 2026-06-12 | Bob | T003 | Completion | | Completed | | SRC-CU-CIPH-13 |
| E050 | 2026-07-15 | Bob | T003 | Batch CLI binary packaged to release artifact store | Release packaging needs the completed CLI binary as a durable artifact | Completed | | SRC-CU-CIPH-13 |
| E010 | 2026-06-10 | Alice | T004 | Task Create | | Open | | SRC-CU-CIPH-14 |
| E011 | 2026-06-14 | Bob | T004 | Initial API | | Active | | SRC-SLACK-03 |
| E012 | 2026-06-17 | Diana | T004 | Security Check | | Completed | | SRC-GDOC-08 |
| E051 | 2026-07-15 | Diana | T004 | FastAPI security-audit status reconfirmed for release pack | T011 release evidence pack requires current Completed security check | Completed | | SRC-CU-CIPH-14 |
| E013 | 2026-06-11 | Evan | T005 | Task Create | | Open | | SRC-CU-CIPH-15 |
| E014 | 2026-06-16 | Evan | T005 | Dockerfile | | Completed | | SRC-GDOC-06 |
| E015 | 2026-06-25 | Diana | T005 | Reopen (Size/CVE) | | Active (Reopened) | | SRC-SLACK-06 |
| E052 | 2026-08-01 | Evan | T005 | Multi-stage Dockerfile redesign toward ~450MB target | Reopen found image at 2.1GB with outstanding CVE verification | Active (Reopened) | | SRC-SLACK-06 |
| E053 | 2026-08-04 | Evan | T005 | Swap Ubuntu base image for Alpine | Multi-stage plan still left base layer too large | Active (Reopened) | | SRC-SLACK-06 |
| E054 | 2026-08-07 | Evan | T005 | Remove unused OCR and runtime packages from image | Alpine swap alone did not reach size target | Active (Reopened) | | SRC-SLACK-06 |
| E055 | 2026-08-12 | Diana | T005 | Size/CVE verification still failing target | Measured image remains above ~450MB; CVE verification still outstanding | Active (Reopened) | | SRC-SLACK-06 |
| E176 | 2026-06-25 | Evan | T005 | Comment: dual RC/GA release gates | RC requires ≤800MB and CVE-clean; GA requires approximately 450MB | Active (Reopened) | | CMT-2026-06-002 |
| E016 | 2026-06-15 | Alice | T006 | Task Create | | Open | | SRC-CU-CIPH-16 |
| E017 | 2026-06-18 | Charlie | T006 | Decision: JSON | | Active | | SRC-MEET-02 |
| E018 | 2026-06-20 | Alice | T006 | Decision: YAML | | Active | | SRC-SLACK-04, SRC-GDOC-03 |
| E019 | 2026-06-22 | Charlie | T006 | Implementation | | Completed | | SRC-CU-CIPH-16 |
| E175 | 2026-06-21 | Alice | T006 | Comment: legacy-policy migration requirement | MedFirst requires migration of three legacy JSON policies; Evan owns the converter | Completed | T011 | CMT-2026-06-001 |
| E020 | 2026-06-19 | Bob | T007 | Task Create | | Open | | SRC-CU-CIPH-17 |
| E021 | 2026-06-23 | Charlie | T007 | Debugging | | Active | | SRC-SLACK-05 |
| E022 | 2026-06-26 | Charlie | T007 | Blocked (PdfMiner) | | Blocked | | SRC-SLACK-07 |
| E056 | 2026-08-05 | Charlie | T007 | Upstream pdfminer.six PR #992 still unmerged | Coordinate drift remains blocked on whitespace fix; no upstream merge yet | Blocked | | SRC-SLACK-07 |
| E057 | 2026-08-20 | Charlie | T007 | Local pdfminer fork rejected for maintenance risk | Evaluated forking the whitespace fix locally; team declined long-term fork ownership | Blocked | | SRC-SLACK-07 |
| E058 | 2026-09-10 | Charlie | T007 | Leave T007 blocked pending upstream merge | Unresolved review: no safe local path; wait on pdfminer.six #992 | Blocked | | SRC-SLACK-07 |
| E177 | 2026-06-27 | Charlie | T007 | Comment: maintainer ETA and Legal gate | Upstream #992 is not expected before mid-October; pre-normalization also requires written Legal sign-off | Blocked | | CMT-2026-06-003 |
| E023 | 2026-06-24 | Alice | T008 | Task Create | | Open | | SRC-CU-CIPH-18 |
| E024 | 2026-06-28 | Charlie | T008 | Tesseract POC | | Active | | SRC-GDOC-04 |
| E025 | 2026-07-05 | Charlie | T008 | Ongoing Work | | Active | | SRC-MEET-03 |
| E059 | 2026-08-02 | Charlie | T008 | Profile identifies page-serial Tesseract loop as bottleneck | Ongoing OCR work showed unacceptable per-page latency under serial execution | Active | | |
| E060 | 2026-08-10 | Charlie | T008 | Implement per-page multiprocessing pool for OCR fallback | Bottleneck check required parallel page processing | Active | | |
| E061 | 2026-08-25 | Charlie | T008 | Retune OCR confidence thresholds after multiprocessing | Parallel OCR changed score distributions versus serial POC | Active | | |
| E062 | 2026-09-12 | Diana | T008 | Begin wiring OCR fallback output into scan pipeline | Multiprocessing path ready enough for scan integration; parallelization still Active | Active | | |
| E026 | 2026-06-27 | Bob | T009 | Task Create | | Open | | SRC-CU-CIPH-19 |
| E027 | 2026-06-30 | Alice | T009 | Defer to v1.1 | | Deferred | | SRC-SLACK-08 |
| E063 | 2026-08-05 | Bob | T009 | Capture v1.1 auth requirements while deferred | v1.0 scope is local-network-only; document deferred REST auth needs for later | Deferred | | SRC-SLACK-08, SRC-CU-CIPH-19 |
| E064 | 2026-08-20 | Alice | T009 | Confirm deferral stands for v1.0 release scope | Release planning rechecked auth; keep Deferred to post-v1.0.0 | Deferred | | SRC-SLACK-08 |
| E178 | 2026-07-02 | Bob | T009 | Comment: MedFirst contractual deadline | REST authentication remains deferred for v1.0 but carries the recorded renewal deadline | Deferred | | CMT-2026-07-001 |
| E028 | 2026-07-02 | Diana | T010 | Task Create | | Open | | SRC-CU-CIPH-20 |
| E029 | 2026-07-06 | Diana | T010 | Scan Report | | Active | | SRC-GDOC-09 |
| E030 | 2026-07-10 | Bob | T010 | Patch Applied | | Completed | | SRC-SLACK-09 |
| E065 | 2026-07-15 | Diana | T010 | Post-patch CVE/CORS verification confirms hold | Confirm Completed security patch remains effective for release evidence | Completed | | SRC-SLACK-09, SRC-CU-CIPH-20 |
| E179 | 2026-07-10 | Bob | T010 | Comment: external attestation | RedByte pen-test attestation is part of the completed security evidence pack | Completed | | CMT-2026-07-002 |
| E031 | 2026-07-08 | Evan | T011 | Task Create | | Open | | SRC-CU-CIPH-21 |
| E032 | 2026-07-12 | Evan | T011 | Checklist Draft | | Active | T001..T006,T010 | SRC-GDOC-05 |
| E066 | 2026-08-01 | Evan | T011 | Prerequisite audit against open packaging and Windows gates | Checklist draft incomplete while T005 slim-down and T029 signing remain open | Active | | |
| E067 | 2026-08-15 | Evan | T011 | Draft release notes while gates remain open | Prerequisite audit showed gates unmet; notes drafted in parallel, checklist still Active | Active | | |
| E068 | 2026-09-15 | Diana | T011 | Security gate hold on Docker slim-down and Windows code-signing | Release blocked until T005 image/CVE work and T029 Defender/SmartScreen signing clear | Active | T005, T029 | SRC-MEET-10 |
| E184 | 2026-09-15 | Diana | T011 | Comment: hard release deadline | No ship after 2026-10-15 if T005 and T029 are not green | Active | T005, T029 | CMT-2026-09-002 |
| E033 | 2026-07-09 | Bob | T012 | Task Create | | Open | | SRC-CU-CIPH-22 |
| E034 | 2026-07-09 | Bob | T012 | Bug Discovery | | Active | | SRC-SLACK-13 |
| E035 | 2026-07-11 | Bob | T012 | Parity Confirm | | Completed | T003, T004 | SRC-SLACK-10 |
| E069 | 2026-07-20 | Bob | T012 | Document CLI-API parity confirmation for release pack | T011 evidence pack needs Completed parity record tied to T003/T004 | Completed | T003, T004 | SRC-SLACK-10, SRC-CU-CIPH-22 |
| E036 | 2026-06-05 | Alice | T013 | Task Create | | Open | | SRC-CU-CIPH-23 |
| E037 | 2026-06-10 | Alice | T013 | Policy Matrix | | Active | | SRC-GDOC-10 |
| E038 | 2026-06-12 | Alice | T013 | Completion | | Completed | | SRC-CU-CIPH-23 |
| E070 | 2026-07-18 | Alice | T013 | Archive signed policy matrix in compliance folder | Compliance pack needs Completed export-vs-review policy on record | Completed | | SRC-CU-CIPH-23 |
| E039 | 2026-06-25 | Diana | T014 | Task Create | | Open | | SRC-CU-CIPH-24 |
| E040 | 2026-06-28 | Diana | T014 | Threshold Logic | | Active | | SRC-SLACK-11 |
| E071 | 2026-08-06 | Diana | T014 | Implement quarantine folder for OCR below 90% confidence | Threshold logic requires a durable quarantine destination for low-confidence pages | Active | | SRC-SLACK-11 |
| E072 | 2026-08-20 | Diana | T014 | Design quarantine metadata (confidence, page, reason) | Quarantine folder alone lacked reviewable context for manual review | Active | | SRC-SLACK-11 |
| E073 | 2026-09-05 | Charlie | T014 | Add visual UI indicators for quarantined pages | Reviewers needed in-UI markers tied to quarantine metadata | Active | | SRC-SLACK-11 |
| E074 | 2026-09-18 | Diana | T014 | End-to-end quarantine test; 90% threshold still integrating | UI and metadata path exercised; confidence-threshold integration remains Active | Active | | SRC-SLACK-11, SRC-CU-CIPH-24 |
| E041 | 2026-06-08 | Alice | T015 | Task Create | | Open | | SRC-CU-CIPH-25 |
| E042 | 2026-06-12 | Bob | T015 | Fail-Closed Req | | Active | | SRC-SLACK-12 |
| E043 | 2026-06-15 | Bob | T015 | Completion | | Completed | | SRC-CU-CIPH-25 |
| E075 | 2026-07-16 | Diana | T015 | QA validates fail-closed (no output file; secure temp deletion) | Confirm Completed fail-closed behavior before encryption and offline gates rely on it | Completed | | SRC-CU-CIPH-25, SRC-SLACK-12 |
| E044 | 2026-07-08 | Diana | T016 | Task Create | | Open | | SRC-CU-CIPH-26, SRC-GDOC-11 |
| E045 | 2026-07-11 | Bob | T016 | Loader Refactor | | Active | | SRC-CU-CIPH-26 |
| E076 | 2026-08-05 | Bob | T016 | Add SHA-256 hash of input streams to audit records | Audit design requires input hash alongside redaction map | Active | | SRC-CU-CIPH-26 |
| E077 | 2026-08-15 | Bob | T016 | Define companion JSON audit schema (hash + redaction map) | Hash streaming needed a stable schema before CLI wiring | Active | | SRC-CU-CIPH-26 |
| E078 | 2026-09-10 | Bob | T016 | Wire audit-log generation into CLI path | Schema defined; CLI must emit companion JSON for release gate | Active | | SRC-CU-CIPH-26 |
| E079 | 2026-09-18 | Diana | T016 | Audit verify finds CLI schema vs log-record mismatch | CLI integration emitted records inconsistent with schema; remains Active release blocker | Active | | SRC-CU-CIPH-26 |
| E046 | 2026-06-12 | Alice | T017 | Task Create | | Open | | SRC-CU-CIPH-27, SRC-MEET-04 |
| E047 | 2026-06-16 | Charlie | T017 | Completion | | Completed | | SRC-CU-CIPH-27 |
| E080 | 2026-07-17 | Alice | T017 | Record overlapping-policy union rule in compliance pack | Completed conflict-resolution rule needed as durable compliance evidence | Completed | | SRC-CU-CIPH-27 |
| E081 | 2026-08-01 | Diana | T017 | Regression-check conflict resolution against HIPAA pattern updates | T020 pattern work must not break Completed overlapping-policy merge | Completed | | SRC-CU-CIPH-27 |
| E082 | 2026-08-01 | Alice | T018 | Task Create | Open air-gapped local runtime packaging workstream | Open | | SRC-CU-CIPH-28 |
| E083 | 2026-08-02 | Evan | T018 | Study static linking options for local runtime binary | Need offline-capable binary without dynamic cloud/runtime deps | Active | | SRC-SLACK-14, SRC-GDOC-12 |
| E084 | 2026-08-04 | Evan | T018 | Statically compile local runtime binary | Static-link study selected full static compile path | Active | | SRC-SLACK-15 |
| E085 | 2026-08-05 | Diana | T018 | Verify static binary runs without external shared libs | Confirm static compile meets air-gap packaging requirement | Completed | | SRC-SLACK-15, SRC-CU-CIPH-28 |
| E086 | 2026-08-01 | Alice | T019 | Task Create | Offline-mode authentication required for air-gapped deployments | Open | | SRC-CU-CIPH-29 |
| E087 | 2026-08-02 | Diana | T019 | Design key-rotation flow for offline auth | Auth design needs rotation without assuming always-on network | Active | | SRC-SLACK-16, SRC-GDOC-13 |
| E088 | 2026-08-04 | Bob | T019 | Build local auth mock for air-gap testing | Key-rotation design needs a testable local mock | Active | | SRC-SLACK-17 |
| E089 | 2026-08-05 | Alice | T019 | Block: key rotation fails without network in air-gap | Local mock showed rotation cannot complete offline; no resolution yet | Blocked | | SRC-SLACK-17, SRC-CU-CIPH-29, SRC-MEET-07 |
| E180 | 2026-08-05 | Alice | T019 | Comment: split escrow approved | InfoSec approved USB-token plus HQ-HSM escrow; T019 remains blocked until implementation | Blocked | | CMT-2026-08-001 |
| E090 | 2026-08-01 | Alice | T020 | Task Create | HIPAA identifier coverage gap versus current PII patterns | Open | | SRC-CU-CIPH-30 |
| E091 | 2026-08-03 | Charlie | T020 | Enumerate HIPAA identifiers for pattern update | Compliance requires expanding detection beyond financial PII | Active | | SRC-SLACK-18, SRC-GDOC-14 |
| E092 | 2026-08-05 | Charlie | T020 | Update regex dictionary with HIPAA identifiers | Identifier enumeration ready for dictionary merge | Active | | SRC-SLACK-19 |
| E093 | 2026-08-08 | Diana | T020 | Merge HIPAA regex dictionary into detection engine | Dictionary update complete; merge depends on completed financial detection | Completed | T002 | SRC-SLACK-19, SRC-CU-CIPH-30, SRC-GDOC-34 |
| E094 | 2026-08-01 | Alice | T021 | Task Create | Local-at-rest encryption required for redacted outputs | Open | | SRC-CU-CIPH-31 |
| E095 | 2026-08-03 | Bob | T021 | Evaluate crypto libraries for local AES-256 | Need library choice compatible with offline runtime | Active | | SRC-SLACK-20, SRC-GDOC-15 |
| E096 | 2026-08-05 | Bob | T021 | Implement AES-256 encryption pipeline for outputs | Crypto eval selected AES-256-at-rest path | Active | | SRC-SLACK-21 |
| E097 | 2026-08-07 | Diana | T021 | Crypto sign-off on AES-256 pipeline | Pipeline ready; depends on Completed fail-closed deletion behavior | Completed | T015 | SRC-SLACK-21, SRC-CU-CIPH-31, SRC-GDOC-35 |
| E098 | 2026-08-02 | Alice | T022 | Task Create | Storage quota needed to prevent disk exhaustion on large batches | Open | | SRC-CU-CIPH-32 |
| E099 | 2026-08-04 | Evan | T022 | Implement disk-usage monitor loop | Quota policy requires live disk monitoring | Active | | SRC-SLACK-22, SRC-GDOC-16 |
| E100 | 2026-08-06 | Diana | T022 | Verify monitor halts writes at configured quota | Initial monitor behavior accepted as meeting quota requirement | Completed | | SRC-SLACK-23, SRC-GDOC-36 |
| E101 | 2026-09-15 | Evan | T022 | Reopen: 500MB hard halt too aggressive in practice | Production-like batches tripped halt before useful work finished | Active (Reopened) | | SRC-SLACK-23 |
| E102 | 2026-09-18 | Bob | T022 | Refactor monitor for 10% buffer tolerance above quota | Reopen root cause was hard 500MB halt without soft buffer | Active (Reopened) | | SRC-SLACK-23, SRC-CU-CIPH-32 |
| E185 | 2026-09-15 | Evan | T022 | Comment: production quota baseline | Retarget the 10% buffer refactor to a 2GB-free production baseline | Active (Reopened) | | CMT-2026-09-003 |
| E103 | 2026-08-02 | Alice | T023 | Task Create | Reviewers need visual redaction preview overlay | Open | | SRC-CU-CIPH-33 |
| E104 | 2026-08-04 | Diana | T023 | Build UI overlay shell for redaction preview | Preview requires coordinate-aligned overlay on document pages | Active | | SRC-SLACK-24, SRC-GDOC-17 |
| E105 | 2026-08-06 | Charlie | T023 | Add redaction highlighting driven by YAML config regions | Overlay shell needs engine coordinates from YAML-based config | Active | T006 | SRC-SLACK-25 |
| E106 | 2026-08-08 | Diana | T023 | Preview overlay accepted as complete | Highlighting and overlay meet visual review requirement | Completed | | SRC-SLACK-25, SRC-CU-CIPH-33, SRC-GDOC-37 |
| E107 | 2026-08-04 | Alice | T024 | Task Create | Distributed zero-trust node sync for multi-site local deployments | Open | | SRC-CU-CIPH-34 |
| E108 | 2026-08-06 | Bob | T024 | Implement node replication handshake prototype | Sync requires authenticated handshake between nodes | Active | | SRC-SLACK-26, SRC-GDOC-18, SRC-GDOC-38 |
| E109 | 2026-08-08 | Bob | T024 | Validate handshake under nominal latency | Prototype needs correctness check before wide rollout | Active | | SRC-SLACK-27 |
| E110 | 2026-09-22 | Diana | T024 | Block: handshake timeouts on high-latency networks | Validation failed under high latency; depends on encryption path but remains Blocked | Blocked | T021 | SRC-SLACK-27, SRC-CU-CIPH-34, SRC-MEET-11 |
| E186 | 2026-09-22 | Diana | T024 | Comment: Singapore field constraint | Field trial fails at 180ms RTT with the 5s prototype; planning requires a 30s timeout budget | Blocked | T021 | CMT-2026-09-004 |
| E111 | 2026-08-05 | Alice | T025 | Task Create | Ephemeral OCR temp files must not persist after failures | Open | | SRC-CU-CIPH-35 |
| E112 | 2026-08-07 | Charlie | T025 | Trace OCR temp-file creation sites | Need inventory of temp paths before cleanup hooks | Active | | SRC-SLACK-28, SRC-GDOC-19 |
| E113 | 2026-08-09 | Charlie | T025 | Add cleanup hooks on OCR failure and completion | Temp-file trace identified unmanaged paths | Active | | SRC-SLACK-29 |
| E114 | 2026-08-11 | Diana | T025 | Confirm secure deletion of ephemeral OCR temps | Cleanup hooks verified; temp files removed after failure/completion | Completed | | SRC-SLACK-29, SRC-CU-CIPH-35, SRC-GDOC-40 |
| E115 | 2026-08-01 | Alice | T026 | Task Create | Batch throughput needs multi-threading on local hardware | Open | | SRC-CU-CIPH-36 |
| E116 | 2026-08-03 | Charlie | T026 | Design worker pool for local batch processing | Need pool model compatible with CLI batch tool | Active | | SRC-SLACK-30, SRC-GDOC-20 |
| E117 | 2026-08-05 | Charlie | T026 | Integrate worker pool into batch CLI pipeline | Pool design ready for wiring into completed CLI batch path | Active | | SRC-SLACK-31 |
| E118 | 2026-08-07 | Diana | T026 | Core multi-thread batch test passes | Integration verified against completed batch CLI (T003) | Completed | T003 | SRC-SLACK-31, SRC-CU-CIPH-36 |
| E119 | 2026-08-04 | Alice | T027 | Task Create | Strict offline air-gapped mode must be testable | Open | | SRC-CU-CIPH-37 |
| E120 | 2026-08-06 | Diana | T027 | Build offline test harness with network denied | Air-gap claim needs reproducible offline execution | Active | | SRC-SLACK-32, SRC-GDOC-21, SRC-GDOC-46 |
| E121 | 2026-08-08 | Diana | T027 | Execute offline batch under harness | Harness ready; run full batch with network blocked | Active | | SRC-SLACK-33 |
| E122 | 2026-08-10 | Diana | T027 | Offline sign-off with noted 45s remote licence-check hang | Batch completed offline; preliminary only—not a compliance certification; hang recorded | Completed | T021 | SRC-SLACK-33, SRC-CU-CIPH-37, SRC-GDOC-47 |
| E123 | 2026-08-05 | Alice | T028 | Task Create | Bare-metal performance benchmarks required for release claims | Open | | SRC-CU-CIPH-38 |
| E124 | 2026-08-07 | Evan | T028 | Author bare-metal benchmark scripts | Need repeatable scripts for local node performance | Active | | SRC-SLACK-34, SRC-GDOC-22 |
| E125 | 2026-08-09 | Evan | T028 | Blocked on missing dedicated benchmark environment | Scripts ready but target bare-metal node not provisioned | Blocked | | SRC-MEET-05 |
| E126 | 2026-08-11 | Evan | T028 | Benchmark node set provisioned; rerun scripts | Environment block cleared; node available | Active | | SRC-SLACK-35 |
| E127 | 2026-08-12 | Diana | T028 | Publish bare-metal benchmark results | Rerun complete; publish depends on completed multi-threading baseline | Completed | T026 | SRC-SLACK-35, SRC-CU-CIPH-38 |
| E128 | 2026-08-08 | Alice | T029 | Task Create | Windows OS compatibility required for release gate | Open | | SRC-CU-CIPH-39 |
| E129 | 2026-08-10 | Evan | T029 | Fix Windows backslash path handling | Windows builds failed on path separators | Active | | SRC-SLACK-36, SRC-GDOC-23 |
| E130 | 2026-08-12 | Evan | T029 | Produce Windows build artifact | Path fix unblocked Windows packaging attempt | Active | | SRC-SLACK-38 |
| E131 | 2026-09-02 | Evan | T029 | Windows Defender/SmartScreen blocks unsigned build | Win build exists but code-signing certificate still missing; remains Active | Active | | SRC-SLACK-37, SRC-CU-CIPH-39, SRC-GDOC-39 |
| E132 | 2026-08-08 | Alice | T030 | Task Create | License compliance review before release | Open | | SRC-CU-CIPH-40 |
| E133 | 2026-08-09 | Diana | T030 | Audit third-party licenses in dependency tree | Need inventory before approving release dependencies | Active | | SRC-SLACK-39, SRC-GDOC-24 |
| E134 | 2026-08-11 | Evan | T030 | Swap PDF parser library after initial audit | Audit flagged problematic license on prior parser choice | Completed | | SRC-SLACK-41 |
| E135 | 2026-08-12 | Diana | T030 | Reopen: replacement parser is AGPL | Library swap introduced restrictive AGPL; not acceptable for intended distribution | Active (Reopened) | | SRC-SLACK-40 |
| E136 | 2026-08-15 | Charlie | T030 | Search for Apache/MIT alternative PDF parser | AGPL finding requires non-copyleft replacement; still unresolved | Active (Reopened) | | SRC-SLACK-41, SRC-CU-CIPH-40, SRC-MEET-08, SRC-GDOC-41 |
| E181 | 2026-08-12 | Diana | T030 | Comment: hard Legal gate | Legal determined AGPL creates whole-bundle copyleft risk; engineering search alone cannot close the P0 gate | Active (Reopened) | | CMT-2026-08-002 |
| E137 | 2026-08-12 | Alice | T031 | Task Create | Large-file chunking needed for multi-GB documents | Open | | SRC-CU-CIPH-41 |
| E138 | 2026-08-14 | Charlie | T031 | Implement stream chunking for large PDF loads | Memory pressure on large files requires chunked reads | Active | | SRC-SLACK-42, SRC-GDOC-25 |
| E139 | 2026-08-16 | Charlie | T031 | Merge stream-chunking implementation | Chunking implementation ready for mainline | Completed | | SRC-SLACK-44, SRC-GDOC-42 |
| E140 | 2026-08-18 | Bob | T031 | Reopen: 2GB+ files still leak memory | Completed chunking retained buffers; leaks observed on 2GB+ inputs | Active (Reopened) | | SRC-SLACK-43 |
| E141 | 2026-08-20 | Charlie | T031 | Refactor stream buffer release after each chunk | Reopen root cause was buffers not released between chunks | Active (Reopened) | | SRC-SLACK-44, SRC-CU-CIPH-41 |
| E182 | 2026-08-18 | Bob | T031 | Comment: MedFirst pilot OOM | A 4.7GB PDF exhausted an 8GB workstation; T031 remains a pilot blocker | Active (Reopened) | T011 | CMT-2026-08-003 |
| E142 | 2026-08-10 | Alice | T032 | Task Create | Auditable redaction-profile schema export required | Open | | SRC-CU-CIPH-42 |
| E143 | 2026-08-12 | Bob | T032 | Design exportable redaction-profile schema | Compliance needs machine-readable profile export | Active | | SRC-SLACK-45, SRC-GDOC-26 |
| E144 | 2026-08-14 | Bob | T032 | Implement schema export API endpoint | Schema design ready; expose via REST API | Active | | SRC-SLACK-46 |
| E145 | 2026-08-16 | Diana | T032 | Verify schema export against REST API contract | Export API must match completed REST endpoints | Completed | T004 | SRC-SLACK-47, SRC-CU-CIPH-42, SRC-GDOC-43 |
| E146 | 2026-08-15 | Alice | T033 | Task Create | Memory-leak profiling needed after large-file work | Open | | SRC-CU-CIPH-43 |
| E147 | 2026-08-17 | Bob | T033 | Identify leak hotspots in PDF loader | Profiling requested after T031 reopen signals | Active | | SRC-SLACK-48, SRC-GDOC-27 |
| E148 | 2026-08-19 | Bob | T033 | Blocked: standard profiler unavailable in offline lab | Identification stalled without approved offline profiler tooling | Blocked | | SRC-MEET-06 |
| E149 | 2026-08-21 | Charlie | T033 | Switch to tracemalloc-based offline profiling | Profiler block cleared by using stdlib tracemalloc | Active | | SRC-SLACK-49 |
| E150 | 2026-08-23 | Bob | T033 | Patch PDF loader leaks found via tracemalloc | Tracemalloc located retained buffers; patch depends on T031 chunking path | Completed | T031 | SRC-SLACK-49, SRC-CU-CIPH-43, SRC-GDOC-44 |
| E151 | 2026-08-10 | Alice | T034 | Task Create | Custom CSV redaction dictionary support requested | Open | | SRC-CU-CIPH-44 |
| E152 | 2026-08-12 | Bob | T034 | Implement CSV dictionary loader | Users need to supply org-specific terms via CSV | Active | | SRC-SLACK-50, SRC-GDOC-28 |
| E153 | 2026-08-14 | Charlie | T034 | Wire CSV terms into detection matcher | Loader needs matcher integration with existing regex engine | Active | | SRC-SLACK-52 |
| E154 | 2026-08-16 | Diana | T034 | Rule test passes for CSV dictionary matches | Matcher wired; depends on completed financial detection baseline | Completed | T002 | SRC-CU-CIPH-44, SRC-GDOC-45, SRC-SLACK-51 |
| E155 | 2026-08-12 | Alice | T035 | Task Create | Electron GUI wrapper for CLI requested for desktop users | Open | | SRC-CU-CIPH-45 |
| E156 | 2026-08-14 | Evan | T035 | Scaffold Electron shell around CLI | Desktop users need GUI entry without rewriting engine | Active | | SRC-SLACK-53, SRC-GDOC-29 |
| E157 | 2026-08-16 | Bob | T035 | Build IPC bridge from Electron UI to CLI batch tool | Scaffold needs IPC to completed batch CLI | Active | T003 | SRC-SLACK-54 |
| E158 | 2026-08-18 | Diana | T035 | Package test of Electron+CLI wrapper succeeds | IPC bridge works; desktop pack accepted | Completed | | SRC-SLACK-55, SRC-CU-CIPH-45, SRC-MEET-09, SRC-GDOC-48 |
| E159 | 2026-08-15 | Alice | T036 | Task Create | High-DPI PDF coordinate alignment defects reported | Open | | SRC-CU-CIPH-46 |
| E160 | 2026-08-17 | Charlie | T036 | Reproduce misalignment on 4K displays | Need reproducible high-DPI failure before fix attempt | Active | | SRC-SLACK-56, SRC-GDOC-30 |
| E161 | 2026-08-19 | Charlie | T036 | Derive scaling math against preview overlay coordinates | 4K repro shows scale factor error relative to Completed preview UI | Active | T023 | SRC-SLACK-57 |
| E162 | 2026-09-10 | Diana | T036 | Block: upstream rendering library scaling math wrong | Scaling math points to upstream library bug; no local fix yet | Blocked | | SRC-SLACK-58, SRC-CU-CIPH-46, SRC-GDOC-49 |
| E183 | 2026-09-10 | Diana | T036 | Comment: expanded Form XObject scope | Nested Form XObjects affect 12% of the pilot corpus, extending the blocker beyond 4K scaling | Blocked | | CMT-2026-09-001 |
| E163 | 2026-08-18 | Alice | T037 | Task Create | Async batch API scheduler for higher throughput | Open | | SRC-CU-CIPH-47 |
| E164 | 2026-08-20 | Bob | T037 | Implement async job scheduler for batch API | Sync batch path saturates under concurrent jobs | Active | | SRC-SLACK-59, SRC-GDOC-31 |
| E165 | 2026-08-22 | Bob | T037 | Add async processing workers to scheduler | Scheduler shell needs workers for concurrent jobs | Active | | SRC-SLACK-60 |
| E166 | 2026-08-25 | Diana | T037 | Block: concurrent I/O race cuts throughput ~10% | Async workers regress throughput via race; depends on multi-thread pool | Blocked | T026 | SRC-SLACK-61, SRC-CU-CIPH-47, SRC-GDOC-50 |
| E167 | 2026-08-18 | Alice | T038 | Task Create | Telemetry must support CLI opt-out for privacy | Open | | SRC-CU-CIPH-48 |
| E168 | 2026-08-20 | Diana | T038 | Design telemetry opt-out flag semantics | Privacy policy requires explicit local opt-out | Active | | SRC-SLACK-62, SRC-GDOC-32 |
| E169 | 2026-08-22 | Bob | T038 | Implement CLI opt-out flag | Opt-out design ready for CLI flag wiring | Active | | SRC-SLACK-63 |
| E170 | 2026-08-24 | Diana | T038 | Network trace confirms no telemetry when flag set | Flag implementation verified; no outbound telemetry with opt-out | Completed | | SRC-SLACK-64, SRC-CU-CIPH-48, SRC-GDOC-51 |
| E171 | 2026-08-20 | Alice | T039 | Task Create | Accessibility a11y audit of UI surfaces | Open | | SRC-CU-CIPH-49 |
| E172 | 2026-08-21 | Diana | T039 | Keyboard navigation test on preview surfaces | a11y audit starts with keyboard access | Active | | SRC-SLACK-65, SRC-GDOC-33 |
| E173 | 2026-08-22 | Diana | T039 | Screen-reader trial on preview overlay | Keyboard pass followed by screen-reader check | Active | | SRC-SLACK-66 |
| E174 | 2026-08-24 | Alice | T039 | Supersede a11y audit; preview overlay overhaul covers styling | Completed visual preview overhaul (T023) natively addresses styling/a11y scope | Superseded | T023 | SRC-SLACK-67, SRC-CU-CIPH-49 |
