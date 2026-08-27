# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

Beyond Docker and Windows, two compliance/audit items still held v1.0.0 on 2026-09-22:

| Item | Current status | Concrete defect/risk | Can engineering search alone close it? |
|---|---|---|---|
| **T016 / CIPH-26 — Audit-trail logging** | **Active/reopened; release hold.** | CLI-emitted audit records do not validate against the defined JSON schema (which must pair each SHA-256 input hash with its redaction map). That makes the audit trail unusable as release evidence. | **No.** It requires correcting the emitted records and Diana’s verification/clearance—not investigation alone. |
| **T030 / CIPH-40 — Third-party license compliance** | **Active/reopened; Legal P0 gate.** | The candidate replacement PDF parser is AGPL-licensed. Shipping it would trigger whole-bundle copyleft and is incompatible with the distribution model. | **No—explicitly not.** Finding an Apache/MIT alternative is necessary, but Legal must also clear the replacement; the authoritative state says engineering library search alone cannot close it. |

I excluded other unfinished compliance tasks because the authoritative work state does not identify them as current v1.0.0 release holds. In particular, the manual-review workflow is active, while the accessibility audit is superseded.  
Records: `WS-04` (2026-09-22), `SRC-MEET-10`, `SRC-CU-CIPH-26`, `SRC-CU-CIPH-40`, `SRC-SLACK-40`.
