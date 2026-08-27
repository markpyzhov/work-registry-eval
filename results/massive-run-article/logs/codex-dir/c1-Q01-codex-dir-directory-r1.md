# As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

<!-- RESPONSE_START -->

**No — do not ship v1.0.0.** T011 is still under a security-gate hold; the release board’s hard rule is no ship after 2026-10-15 unless T005 and T029 are green. [WS-03](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md#L31-L35)

Open release gates/explicitly release-blocking holds:

1. **T005 — Docker GA size and CVE clearance.** This compound gate is reopened: the image remains above the ~450 MB GA target and CVE verification is failing/outstanding. (An 800 MB CVE-clean RC threshold exists, but GA is ~450 MB.) [WS-03](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md#L29-L30), [CIPH-15](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-15-Docker-Packaging.md#L12-L17)

2. **T029 — Windows Authenticode signing.** The Windows binary is unsigned because no certificate has been procured; Defender/SmartScreen blocks or warns on it. [WS-06](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md#L35-L40), [CIPH-39](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-39-Windows-Compatibility.md#L11-L23)

3. **T016 — Audit-log schema conformance.** CLI-emitted audit records do not validate against the defined schema, so QA cannot clear the audit gate; the pre-release audit calls it an open release blocker. [CIPH-26](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md#L12-L18), [pre-release audit](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md#L11-L25)

4. **T036 — High-DPI coordinate alignment.** It remains blocked on an upstream rendering-library scaling defect; redaction coordinates drift 5–10 px at 200% scaling, with nested Form XObjects failing in 12% of the MedFirst pilot corpus. It was explicitly still open in the pre-release gate review. [WS-06](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-06-platforms.md#L38-L40), [pre-release audit](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md#L7-L13)

5. **T030 — License-compliance legal gate.** The candidate PDF parser is AGPL; the resulting whole-bundle copyleft exposure is a hard P0 Legal gate, and no acceptable Apache/MIT replacement has been adopted. [WS-04](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md#L50-L56), [CIPH-40](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md#L12-L23)

6. **T031 — large-file memory safety, release-coupled to T011.** A 4.7 GB PDF OOM’d an 8 GB MedFirst clinic workstation; files over 2 GB still leak memory during long batch runs while buffer-release logic is being refactored. [WS-05](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-05-performance.md#L28-L34), [CIPH-41](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-41-Large-File-Chunking.md#L12-L22)

7. **T007 — PDF offset-drift legal/workaround gate.** The upstream `pdfminer.six` fix remains unmerged; a pre-normalization workaround requires written Legal sign-off, and the team rejected maintaining a local fork. The final brief still lists this as the “Legal workaround gate.” [WS-01](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-01-engine.md#L37-L39), [final daily brief](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md#L19-L26)

T005 and T029 are the two formal unmet acceptance gates for CIPH-21; the other five are separately recorded release holds, gates, or T011-coupled blockers in the final snapshot. [CIPH-21](file:///Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-21-Release-v1-Gates.md#L12-L16)
