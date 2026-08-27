# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

Beyond Docker and Windows, the remaining v1.0.0 compliance/audit holds are:

| Item | Current status | Concrete defect / risk | Engineering search alone? |
|---|---|---|---|
| Audit-trail logging (CIPH-26) | **Active; explicit release blocker** | CLI-emitted audit records fail the defined JSON schema, so the SHA-256/input-to-redaction-map evidence is not reliable. | **No.** Engineering can fix it in-house, but must also regenerate records and pass schema verification/QA. |
| Third-party license audit (CIPH-40) | **Active (Reopened); pre-release audit open** | The replacement PDF parser is also AGPL; restrictive copyleft remains unacceptable in the shipped dependency set. The task also has an unverified `eng.traineddata` training-corpus provenance item. | **No.** Finding a candidate is insufficient: it must be adopted, functionally validated, and the dependency tree re-audited. Provenance needs credible external evidence. |
| Telemetry opt-out / Electron crash reporter | **CLI opt-out completed, but full privacy compliance remains unverified** | Sentry’s Electron crash-reporter path has not been audited to confirm it honors the opt-out flag or that minidump uploads are disabled. | **No.** Inspection alone cannot establish behavior; it needs an audit/test and potentially a disable-hook implementation. |

Sources: `SRC-CU-CIPH-26`, `SRC-MEET-10`, `SRC-CU-CIPH-40`, `SRC-GDOC-41`, `SRC-GDOC-51`.

I did not count the AES/PBKDF2-to-Argon2id hardening follow-up or the preliminary offline sign-off as current release-gate holds: the sources explicitly say the former is not a sign-off condition, and the offline test task is Completed, albeit not a regulatory certification.
