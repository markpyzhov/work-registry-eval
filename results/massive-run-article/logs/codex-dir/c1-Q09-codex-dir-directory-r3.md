# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

As of 9/22, compliance/audit remains a P0 hold.

- Audit trail: CLI records fail the defined schema, so release evidence is invalid until fixed and QA-verified. (`SRC-CU-CIPH-26`, `SRC-MEET-10`)
- License: AGPL parser remains in scope; whole-bundle copyleft is a hard Legal gate. Engineering search alone cannot close it—adopt/rescan, then Legal sign-off. (`CMT-2026-08-002`)
- Offline auth: air-gapped rotation is blocked; approved split-escrow design is not yet implemented. (`CMT-2026-08-001`, `SRC-CU-CIPH-29`)
- Residual privacy: Sentry crash-reporting has not been audited for opt-out compliance, so full privacy/air-gap compliance cannot be claimed. (`SRC-GDOC-51`)

Evidence: [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:39), [audit task](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md:11), [Legal comment](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md:13).
