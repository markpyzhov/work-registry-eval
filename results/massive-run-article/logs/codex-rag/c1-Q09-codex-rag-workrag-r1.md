# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

As of 2026-09-22, the compliance/audit track is P0 and still in progress. Beyond Docker and Windows, the remaining v1.0.0 holds are:

| Item | Current status | Concrete defect / risk | Can engineering search alone close it? |
|---|---|---|---|
| **T016 / CIPH-26 — audit-trail logging** | Active/reopened; explicit release hold. | CLI-emitted audit records do not validate against the defined JSON schema, undermining the audit trail as release evidence. | **No.** Engineering must correct the emitted records and QA must verify schema conformance. |
| **T019 / CIPH-29 — offline authentication and key rotation** | Blocked. InfoSec approved split master-key escrow, but implementation is only being spiked. | Key rotation cannot work in a strictly air-gapped deployment without a centralized authority; the approved USB-token + HQ-HSM escrow design must be built and validated. | **No.** It requires architecture implementation and validation, not discovery alone. |
| **T030 / CIPH-40 — third-party license compliance** | Active/reopened; **Legal P0 gate**. | The candidate replacement PDF parser is AGPL-licensed, creating whole-bundle copyleft risk. | **No—explicitly.** The Work State says an engineering library search alone cannot close it; an acceptable replacement must be adopted and the Legal gate cleared. |

T014/CIPH-24 (low-confidence OCR quarantine) is still active, with the 90% threshold integration incomplete, but the records do not label it an explicit release hold, so I have not counted it above.

Evidence: `WS-04-policy.md` records `917ecd0b3736fd18`, `9e4ee6741c6cd253`, and `99fa4c3e7450f6a7`; `CIPH-26` record `a51c2421e2cc50c1`; `CIPH-29` record `6885a2d295abbbe4`; `CIPH-40` record `0e8152f68571421e`.
