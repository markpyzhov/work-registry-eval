# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

Beyond Docker/CVE and Windows signing, the remaining v1.0.0 compliance/audit holds are:

| Item | Current status | Concrete defect/risk | Can engineering search alone close it? |
|---|---|---|---|
| Audit-trail logging (CIPH-26) | **Active; release blocker.** | CLI-generated audit records fail the defined JSON schema, undermining the SHA-256-hash/redaction-map audit trail as release evidence. | **Yes, in principle**—fix the record/schema mismatch and re-validate the emitted records. [SRC-CU-CIPH-26; SRC-MEET-10] |
| Third-party license compliance (CIPH-40) | **Active (Reopened).** | The shipped PDF parsing/rasterization dependency chain still contains AGPL/copyleft software, unacceptable for the distribution model; the attempted replacement was also AGPL. | **No.** Search is only the first step: a suitable Apache/MIT alternative must be selected, integrated, and the full dependency tree re-audited. OCR model-data provenance is also still unverified. [SRC-CU-CIPH-40; SRC-GDOC-41] |
| High-DPI PDF coordinate scaling (T036/CIPH-46) | **Blocked; treated as a pre-release gate.** | On scaled displays—especially complex PDFs with nested Form XObjects—preview/redaction coordinates misalign due to upstream rendering-library scaling math. | **No.** No safe local fix exists; closure requires an upstream correction or an accepted remediation/alternative-renderer decision. [SRC-MEET-10; SRC-GDOC-49; SRC-SLACK-58] |

One additional unresolved **privacy-compliance limitation** is Sentry/Electron crash reporting: CLI telemetry opt-out is verified, but the crash reporter has not been audited to confirm it honors opt-out or needs a separate minidump-disable hook. The dataset does **not** explicitly label this a v1.0.0 release gate, but it does say full opt-out/air-gapped privacy compliance cannot yet be claimed. Engineering search alone would not close it; it needs a behavior audit and possibly an implementation change. [SRC-GDOC-51]
