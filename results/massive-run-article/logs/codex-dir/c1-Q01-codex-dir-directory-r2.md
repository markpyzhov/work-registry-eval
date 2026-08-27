# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

**No-go — CipherDoc is not ready to ship v1.0.0 as of the 2026-09-22 snapshot.** T011 remains active under a security-gate hold. Its two mandatory acceptance gates are explicitly unmet, and additional release holds/dependencies remain unresolved. [CIPH-21](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md:12) [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:31)

Open release gates/holds:

- **T005 / CIPH-15 — Docker packaging, size, and CVE verification.** It is reopened/active: image exceeds the GA ~450 MB target and CVE verification is failing. The CISO also distinguishes an 800 MB, CVE-clean RC threshold from the ~450 MB GA threshold. [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:29)
- **T029 / CIPH-39 — Windows Authenticode code-signing.** Windows builds remain held because unsigned binaries trigger SmartScreen until a certificate is procured. [WS-06](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md:36)
- **T016 / CIPH-26 — audit-log schema alignment.** CLI-emitted records do not match the defined schema; Diana cannot clear the audit gate, and the pre-release review calls this a release blocker. [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:50) [pre-release audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:13)
- **T036 / CIPH-46 — High-DPI redaction-coordinate correctness.** The pre-release gate review leaves this upstream block open; current QA reports 5–10 px drift and nested Form XObject failures in 12% of the MedFirst pilot corpus. [pre-release audit](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:8) [WS-06](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md:39)
- **T030 / CIPH-40 — AGPL license compliance.** This is an unresolved P0 hard Legal gate: the candidate parser’s AGPL exposure applies whole-bundle copyleft, and an engineering library search alone cannot close it. [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:51) [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:56)
- **T031 / CIPH-41 — large-file/OOM pilot path.** The MedFirst clinic workstation OOM on a 4.7 GB PDF is explicitly a pilot blocker tied to the T011 release gate; severe memory leakage above 2 GB remains under repair. [WS-05](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md:33)
- **T006 legacy-JSON migration — MedFirst cutover dependency.** Although the YAML loader task is complete, the three legacy pilot policies still must auto-migrate; the Work State explicitly makes that migration a T011 release dependency. [WS-01](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md:34)

The hard release-board condition is especially decisive: **no ship after 2026-10-15 unless both T005 and T029 are green**. At the snapshot date, neither is green. [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:34)

Not counted as generic-v1 release gates: T009 is deliberately deferred to v1.1, while T007, T019, T024, T022, and T037 are open work/blockers but the final Work States do not designate them as v1.0.0 ship gates.
