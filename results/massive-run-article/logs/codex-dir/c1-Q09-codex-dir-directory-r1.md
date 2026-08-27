# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

As of 2026-09-22, the non-Docker/non-Windows compliance-and-audit release holds are:

| Item | Current status | Concrete defect/risk | Can engineering search alone close it? |
|---|---|---|---|
| **T016 / CIPH-26 — Compliance audit-trail logging** | **Active/reopened; explicit release hold.** | The CLI emits audit records that do not validate against the defined JSON schema (which must pair each input’s SHA-256 with its redaction map). This makes the audit trail unreliable as release evidence. | **No.** Engineering must reconcile the emitted records/schema, but Diana must then re-verify them before the audit gate can clear. No separate Legal approval is stated. [WS-04-policy.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:50) [CIPH-26-Audit-Trail-Logging.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-26-Audit-Trail-Logging.md:12) [Pre-Release-Audit.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/fireflies/2026-09-15-Pre-Release-Audit.md:19) |
| **T030 / CIPH-40 — Third-party license compliance** | **Reopened/active; P0 hard Legal gate.** | The candidate replacement PDF parser is AGPL-licensed; shipping it risks whole-bundle copyleft exposure under CipherDoc’s distribution model. Closure also requires a clean full dependency-tree audit and adoption of a suitable non-copyleft parser. | **No—explicitly not.** An Apache/MIT alternative search is necessary, but the Legal memo says engineering search alone cannot close the gate; Legal clearance is required. [WS-04-policy.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md:51) [2026-08.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-08.md:16) [CIPH-40-License-Compliance-Review.md](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md:14) |

I excluded other open compliance work such as T019 offline authentication: it remains blocked, but the Sep. 22 record does not identify it as a v1.0.0 release hold.
