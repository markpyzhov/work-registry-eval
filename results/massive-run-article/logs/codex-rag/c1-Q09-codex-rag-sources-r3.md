# Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

<!-- RESPONSE_START -->

Beyond Docker and Windows packaging, these items remain open as of 2026-09-22:

| Item | Current status | Concrete defect / risk | Can engineering search alone close it? |
|---|---|---|---|
| Audit-trail logging (CIPH-26) | **Active; release blocker.** | CLI-emitted audit records fail the defined JSON schema, so the required hash/redaction-map trail is not valid release evidence. | **No.** Engineering can fix the emitter, but closure requires schema-validation re-test and audit-gate clearance. |
| High-DPI PDF rendering (CIPH-46) | **Blocked; release gate remains open.** | An upstream renderer miscalculates coordinates for nested Form XObjects under parent transforms; redaction/preview alignment fails on affected high-DPI documents. | **No.** There is no safe local fix; it needs an upstream correction or a deliberate alternative/remediation decision. |
| Third-party license audit (CIPH-40) | **Active (Reopened), high priority.** | The replacement PDF parser is also AGPL, leaving restrictive copyleft in the shipped dependency set; the original Ghostscript issue was therefore not actually resolved. | **No.** Finding candidates is insufficient—an acceptable Apache/MIT alternative must be validated, adopted, and the full dependency tree re-audited. |
| Tesseract model provenance | **Open, lower priority within the license audit.** | `eng.traineddata` came from a community repo; its training-corpus provenance has not been verified as public-domain/CC0. | **No.** Requires provenance evidence, not just a codebase search. |
| Electron/Sentry opt-out path | **Privacy compliance incomplete.** CLI/API opt-out is verified, but full air-gapped/opt-out compliance cannot yet be claimed. | Sentry has not been audited to confirm it honors `CIPHER_TELEMETRY=0` or whether minidump uploads need a separate disable hook. | **No.** It needs third-party behavior verification and possibly a configuration/change, not search alone. |

The audit-log mismatch and high-DPI defect are explicitly called out as release holds in the pre-release audit. The license and privacy items remain unresolved compliance gaps; the sources do not explicitly label them as additional T011 checklist gates.  

Citations: SRC-MEET-10; SRC-CU-CIPH-26; SRC-GDOC-49; SRC-SLACK-58; SRC-CU-CIPH-40; SRC-GDOC-41; SRC-GDOC-51.
