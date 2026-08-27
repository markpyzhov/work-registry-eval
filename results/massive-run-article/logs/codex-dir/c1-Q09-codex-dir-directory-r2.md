# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

As of 9/22, WS‑04 is P0/in progress. Beyond Docker/Windows, four compliance items remain:

- **T016/CIPH‑26 audit trail — Active/reopened; release hold.** CLI audit records fail the defined hash+redaction-map JSON schema, so they cannot serve as release evidence. **Engineering search alone: no**—implement schema alignment, then QA validation must pass. [WS‑04](c1/work-states/WS-04-policy.md); [CIPH‑26](c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md); [pre-release audit](c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md).

- **T030/CIPH‑40 license review — Reopened/active; P0 Legal gate.** The replacement PDF parser is AGPL, creating whole-bundle copyleft exposure. **No**—an Apache/MIT candidate search is necessary but Legal must approve the shipped dependency set; the record explicitly says search alone cannot close it. [WS‑04](c1/work-states/WS-04-policy.md); [CMT‑2026‑08‑002](c1/work-states/comments/2026-08.md).

- **T019/CIPH‑29 offline auth — Blocked.** Air-gapped key rotation requires network; approved USB-token/HQ-HSM escrow is not yet built. **No**—requires implementation and offline validation (and potentially requirement/design action), not research alone. [WS‑04](c1/work-states/WS-04-policy.md); [CIPH‑29](c1/med-synth/tasks/CIPH-29-Offline-Mode-Authentication.md).

- **T014/CIPH‑24 manual review — Active.** Quarantine/UI path tested, but 90% threshold integration remains incomplete. **No**—finish integration and testing. [CIPH‑24](c1/med-synth/tasks/CIPH-24-Manual-Review-Threshold.md).

T039 a11y is superseded, not a hold.
