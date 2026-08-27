# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

## Cross-workstream briefing — 2026-09-22

**Stable completed milestones**

- **Core safety:** fail-closed batch processing remains completed and QA-validated: failures produce no output and securely remove temporary files. [SRC-CU-CIPH-25]
- **Policy/compliance logic:** overlapping-policy conflict resolution remains completed; its union rule was archived as compliance evidence and regression-checked against the HIPAA pattern update without breakage. [SRC-CU-CIPH-27]

**Completed, then reopened — not done**

- **Release packaging:** Docker packaging is **Active (Reopened)**. The initial Dockerfile was completed, but the 2.1GB image and unresolved CVE review reopened it; the ~450MB target is still unmet. [SRC-CU-CIPH-15]
- **License compliance:** the parser replacement was initially marked complete, then reopened when the replacement was also AGPL-licensed. CIPH-40 remains **Active (Reopened)** pending a suitable Apache/MIT alternative. [SRC-GDOC-41; SRC-CU-CIPH-40]
- **Large-file performance:** stream chunking was merged and called done, then reopened after 2GB+ files leaked memory. Buffer-release refactoring is still active and lacks full-corpus validation. [SRC-GDOC-42; SRC-CU-CIPH-41]

**Durable blockers**

- **Windows releaseability:** a build artifact exists, but the missing code-signing certificate leaves it vulnerable to Defender/SmartScreen blocking at customer sites. This remains a release gate. [SRC-GDOC-39; SRC-MEET-10]
- **High-DPI rendering:** an upstream `pdf-lib-core` coordinate bug breaks complex PDFs with nested Form XObjects; no safe local fix exists and the upstream has not responded. [SRC-SLACK-58; SRC-GDOC-49]
- **Multi-site sync:** authenticated handshake validation times out under high latency; the team explicitly rejected a timeout-bump workaround and left the path blocked on encryption/handshake redesign. [SRC-MEET-11; SRC-CU-CIPH-34]

**Escalate before ship**

1. Obtain and integrate the Windows signing certificate; unsigned pilots may be blocked outright.
2. Keep the release gate closed until Docker size/CVE work and the audit-log schema-versus-emitted-record mismatch clear. [SRC-MEET-10]
3. Make a management decision on high-DPI: accept a documented limitation, fund a rendering-library change, or define a safe workaround.
4. Resolve the AGPL parser replacement before shipping any affected dependency set.
5. Treat multi-site rollout as out of scope for ship unless high-latency handshake acceptance passes.
