# Project Scenario: CipherDoc Toolkit

**Project**: CipherDoc
**Description**: A local-first document privacy toolkit. It detects and redacts sensitive information (like financial data, HIPAA identifiers, and PII) in business documents without relying on external cloud services.
**Timeline**: June 1, 2026 to September 22, 2026.
**As-of Timestamp**: 2026-09-22T12:00:00Z

## Team
- **Alice** (Product Manager)
- **Bob** (Backend/API Developer)
- **Charlie** (Engine/Core Developer)
- **Diana** (Security/QA Engineer)
- **Evan** (DevOps/Release Engineer)

## Workstreams
1. **WS-01: Detection and Redaction Engine**: PDF text layer parsing, coordinate math, visual overlays, and OCR fallback. (Charlie)
2. **WS-02: REST API and Batch Processing**: FastAPI-based REST endpoints, multi-threaded batch processors, and CLI-API configuration parity. (Bob)
3. **WS-03: Local Runtime, Packaging, and Release Operations**: Static linking, multi-stage Docker builds, vulnerability scans, and release gating. (Evan, Diana)
4. **WS-04: Regulatory Compliance, Privacy, and Audits**: Offline mode validation, HIPAA identifier updates, license auditing, telemetry opt-out flags, and JSON audit logging. (Alice, Diana)
5. **WS-05: Performance Benchmarking and System Optimization**: Multiprocessing scalability, performance scripts, file stream chunking, and memory profiling. (Charlie, Bob)
6. **WS-06: External Interfaces and Platform Compatibility**: Preview UI coordinate mapping, air-gapped verification, desktop GUI wrapper, and OS-specific rendering. (Diana, Evan)
7. **WS-07: Data Persistence, Encryption, and Secure Storage**: AES-256 output encryption, storage quota management, distributed node synchronization, and ephemeral file cleaning. (Bob, Charlie)

## Final Status Mix (As of September 22, 2026)

### Completed Tasks
- **T001**: Core Redaction Engine (`WS-01`)
- **T002**: Regex-Based Financial Detection (`WS-01`)
- **T003**: Batch CLI Processing Tool (`WS-02`)
- **T004**: REST API Endpoints (`WS-02`)
- **T006**: YAML-based Configuration Loader (`WS-01`)
- **T010**: Security Vulnerability Patches (`WS-03`)
- **T012**: CLI-API Parity Verification (`WS-02`)
- **T013**: Research Export vs. Internal Review Policies (`WS-04`)
- **T015**: Batch Processing Fail-Closed Strategy (`WS-04`)
- **T017**: Overlapping Policy Conflict Resolution (`WS-04`)
- **T018**: Local Runtime Binary Static Linking (`WS-06`)
- **T020**: PII Pattern Update for HIPAA Compliance (`WS-04`)
- **T021**: AES-256 Local Encryption at Rest (`WS-07`)
- **T023**: Visual Redaction Preview UI Overlay (`WS-06`)
- **T025**: Ephemeral OCR Temp File Cleanup Hooks (`WS-07`)
- **T026**: Multi-threading for Local Batch Processing (`WS-05`)
- **T027**: Strict Offline Air-Gapped Mode Testing (`WS-06`)
- **T028**: Bare-metal Performance Benchmarks (`WS-05`)
- **T032**: Redaction Profile Auditable Schema Export (`WS-04`)
- **T033**: Memory Leak Profiling and PDF Loader Patches (`WS-05`)
- **T034**: Custom CSV Redaction Dictionary Support (`WS-07`)
- **T035**: Electron GUI Desktop Wrapper for CLI (`WS-06`)
- **T038**: Telemetry CLI Opt-Out Privacy Flags (`WS-04`)

### Active / In-Progress Tasks
- **T005**: Docker image size and CVE audit (Reopened; multi-stage refactoring underway to slim image to ~450MB) (`WS-03`)
- **T008**: OCR fallback performance parallelization (Active; optimizing page multiprocessing) (`WS-01`)
- **T011**: Release Gates (Active; held pending Docker slim-down and Windows smart screen code signing) (`WS-03`)
- **T014**: Manual review quarantine logic for low-confidence OCR (Active; integrating 90% confidence threshold) (`WS-04`)
- **T016**: Companion JSON audit log generation (Active; computing SHA-256 hashes of input streams) (`WS-04`)
- **T022**: Storage Quota Management (Reopened/Active; refactoring monitor loop to support a 10% buffer tolerance) (`WS-07`)
- **T029**: Windows OS Compatibility (Active; backslash paths fixed, but blocked on code-signing certificate) (`WS-06`)
- **T030**: License Compliance Review (Reopened/Active; replacement PDF parser has restrictive AGPL license, searching for Apache/MIT alternative) (`WS-04`)
- **T031**: Large File Chunking (Reopened/Active; memory leaks on 2GB+ files require stream buffer release refactoring) (`WS-05`)

### Blocked Tasks
- **T007**: Coordinate drift in multi-page PDFs (Blocked by upstream `pdfminer.six` whitespace Issue/PR #992) (`WS-01`)
- **T019**: Offline Mode Authentication (Blocked; key rotation fails in air-gapped env without net access) (`WS-04`)
- **T024**: Distributed Zero-Trust Node Sync (Blocked; handshake timeouts on high-latency networks) (`WS-07`)
- **T036**: High-DPI PDF Coordinate Alignment (Blocked by upstream rendering scaling library math) (`WS-06`)
- **T037**: Async Batch API Scheduler (Blocked by concurrent I/O race condition reducing throughput by 10%) (`WS-05`)

### Deferred Tasks
- **T009**: REST API Authentication (Deferred to post-v1.0.0; local networking-only initial deployment) (`WS-02`)

### Rejected / Superseded Decisions
- **T006 (JSON format)**: Initial config design rejected in favor of YAML config for inline comments and user-friendliness. (`WS-01`)
- **T039**: Accessibility a11y Audit task superseded by the visual preview Overhaul which natively addresses styling. (`WS-04`)
