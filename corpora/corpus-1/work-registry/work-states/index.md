# Work State Index

**As-of Timestamp**: 2026-09-22T12:00:00Z

| Area | Description | Priority |
|---|---|---|
| [WS-01-engine](./WS-01-engine.md) | Detection and redaction engine core capabilities | P0 |
| [WS-02-api](./WS-02-api.md) | REST API and Batch CLI processing layers | P1 |
| [WS-03-ops](./WS-03-ops.md) | Packaging, Release gating, and Security | P0 |
| [WS-04-policy](./WS-04-policy.md) | Regulatory Compliance, Privacy, and Audits | P0 |
| [WS-05-performance](./WS-05-performance.md) | Benchmarking, Optimization, and Memory Profiling | P1 |
| [WS-06-platforms](./WS-06-platforms.md) | Platform Compatibility and User Interfaces | P2 |
| [WS-07-storage](./WS-07-storage.md) | Data Persistence, Encryption, and Node Sync | P1 |

## Key Blockers and Active Items
- **Blocked**: T007 (upstream `pdfminer.six` #992), T019 (offline auth in air-gapped env), T024 (high-latency handshake timeouts), T036 (upstream High-DPI scaling), T037 (async I/O race).
- **Active / Reopened**: T005 (Docker size/CVE), T008 (OCR), T011 (release gates), T014 (OCR quarantine), T016 (audit logs), T022 (quota buffer), T029 (Windows — held on code-signing), T030 (license search), T031 (large-file memory leak).
- **Deferred**: T009 (REST auth to v1.1).
- **Superseded**: T039 (a11y audit folded into preview UI).
