# Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

<!-- RESPONSE_START -->

As of 2026-09-22, ship posture is **red**: release gating remains P0 and dependent workstreams are still in progress.

- Durable completed milestones: security scans/CORS remediation hold after re-scan; the external pen-test attestation is in the release pack. Performance benchmarks reached 500 pages/minute, and the PDF-loader memory fix remained stable through 10,000 documents. [WS-03-ops, `1024f18927beaa06`; WS-05-performance, `18ae303b6edf58b7`]

- Reopened work — **not done**:
  - CIPH-15 Docker packaging was initially completed at ~800MB, then reopened when OCR dependencies pushed it to 2.1GB; it is still above the GA size target and CVE verification is failing.
  - CIPH-41 large-file chunking initially landed, then reopened after severe >2GB-file memory leaks.
  - CIPH-32 storage quota management is reopened/active because it halts processing too aggressively near 500MB free disk. [WS-03-ops, `ddcbe9ec3299f495`, `f0b9411efcd33230`; WS-05-performance, `ec16f901e952ecd9`; WS-07-storage, `bcafdf0ed04b56a6`]

- Durable blockers:
  - Offline authentication/key rotation remains blocked pending implementation of the approved split master-key escrow architecture.
  - License compliance is a Legal P0 gate: the AGPL candidate parser cannot ship in the bundle; an acceptable replacement is still being sought.
  - Zero-trust node sync fails under 180ms RTT; the needed 30s timeout budget is deferred pending encryption-path stabilization. [WS-04-policy, `9e4ee6741c6cd253`; WS-07-storage, `22220ee873af20a8`]

- Escalate before ship:
  1. Release board decision on Docker/CVE and Windows signing: T011 cannot close until both are green, with a hard no-ship after 2026-10-15.
  2. Legal decision and replacement plan for the AGPL parser, plus closure of the audit-log schema mismatch release hold.
  3. Field-readiness decision for high-latency node sync; also treat the large-file OOM and async manifest-write corruption risk as release-critical. [WS-03-ops, `f9c5d923ad85c212`, `f0b9411efcd33230`; WS-04-policy, `917ecd0b3736fd18`; WS-05-performance, `ec16f901e952ecd9`, `93e3e9a1cb4874a8`]
