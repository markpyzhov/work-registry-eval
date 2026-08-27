# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

As of 2026-09-22, beyond Docker and Windows, these compliance/audit items remain open:

| Item | Current status | Defect or risk | Engineering search alone? |
|---|---|---|---|
| **T016 / CIPH-26 — Audit-trail logs** | **Active/reopened; release hold** | CLI-emitted audit records do not conform to the defined schema, undermining audit evidence. | **No.** Requires implementation correction and verification that emitted records match the schema. |
| **T019 / CIPH-29 — Offline authentication/key rotation** | **Blocked** | In a strictly air-gapped deployment, key rotation cannot complete without centralized/network authority. An InfoSec-approved split escrow design still must be built. | **No.** Requires an implemented and validated escrow/rotation architecture. |
| **T030 / CIPH-40 — License compliance** | **Reopened/active; hard Legal P0 gate** | The candidate PDF parser is AGPL-licensed, creating whole-bundle copyleft exposure; no acceptable replacement is confirmed. | **No.** The work state explicitly says library search alone cannot close it; Legal clearance plus adoption/audit of a compliant dependency set are required. |

The manual-review/OCR workflow (T014) is still active, but the current work state does not identify it as a v1.0.0 release hold. The standalone accessibility audit is superseded.

Records: `WS-04: Regulatory Compliance, Privacy, and Audits` (2026-09-22); `SRC-MEET-10`; `SRC-CU-CIPH-29`; `SRC-CU-CIPH-40`.
