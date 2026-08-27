# As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

<!-- RESPONSE_START -->

## As of 2026-09-22 — CipherDoc tasks in **Blocked** status

Five tasks carry ClickUp status **Blocked** as of that date. Two are blocked by external/upstream third-party code; three are blocked by internal design/implementation defects in CipherDoc's own code.

### Upstream / external blocks (2)

**CIPH-17 — Fix Coordinate/Offset Drift in Multi-Page PDFs** (Priority High)
- **Assignee: Charlie**
- **Root cause:** Redaction masks drift out of alignment with target text across multi-page PDFs. Debugging traced it to a whitespace-handling defect inside the third-party `pdfminer.six` parser. The fix exists only as upstream PR/issue **#992**, which remains unmerged with no maintainer movement (rechecked 2026-09-10, still unmerged). The team evaluated forking `pdfminer.six` to land the fix locally and **rejected** it as too much long-term maintenance risk, so the task is deliberately parked pending an upstream merge with no local workaround adopted. Alice flagged this as a real risk to the v1.0 timeline.
- Sources: SRC-CU-CIPH-17; SRC-SLACK-07 (#cipherdoc, 2026-06-26 → 2026-09-10).

**CIPH-46 — Correct high-DPI PDF coordinate scaling** (Priority Normal)
- **Assignee: Charlie**
- **Root cause:** Coordinate misalignment on high-DPI/4K displays. The scaling-math error was traced to a known bug in the upstream rendering library (`pdf-lib-core`) in how it handles coordinates for nested Form XObjects when a parent transform is applied. The defect sits deep in that library's C++ core and cannot be patched locally; Charlie opened an upstream issue and the maintainers have not responded. A PDF-flattening workaround was floated but rejected as it would inflate file size and risk losing text layers. Blocked 2026-09-10 by Diana; the team decided to leave it blocked and document it as a known issue affecting a small subset of complex documents.
- Sources: SRC-CU-CIPH-46; SRC-SLACK-58 (2026-09-10); SRC-GDOC-49 / DOC-2049 (2026-09-10).

### Internal blocks (3)

**CIPH-34 — Authenticated handshake for multi-site node sync** (Priority High) — *newly blocked on 2026-09-22*
- **Assignee: Bob**
- **Root cause:** Internal. The zero-trust node-replication handshake passed nominal-latency validation on a single LAN segment, but over a simulated high-latency link it **times out and never completes the exchange**, degrading as the link slows. Bob attributes it to the AES-256 output-path pipeline adding per-packet overhead that pushes the exchange past the timeout window — the handshake does more work per round trip than the design budgets for. The team explicitly rejected simply bumping timeouts ("bumping timeouts just hides it"), so it stays blocked pending changes in the encryption path or a redesigned handshake. Diana left the high-latency repro in place for re-testing.
- Sources: SRC-CU-CIPH-34 (blocked 2026-09-22 by Diana); SRC-MEET-11 Fireflies "Handshake Protocol Deep Dive" (2026-09-22); SRC-SLACK-27 (2026-08-08 → 2026-09-22).

**CIPH-47 — Async job scheduler for concurrent batch API work** (Priority Normal)
- **Assignee: Bob**
- **Root cause:** Internal. A concurrent I/O race between the new async workers and the existing multi-threaded batch worker pool. Multiple workers append to the same shared results manifest concurrently, interleaving writes and corrupting the JSON; workers then retry/serialize around the corrupted-write recovery path, cutting batch throughput by roughly **10%** versus the sync baseline. Confirmed by concurrency testing on 2026-08-25; Alice ruled a 10% hit "not shippable" and held all further async work.
- Sources: SRC-CU-CIPH-47 (blocked 2026-08-25 by Diana); SRC-SLACK-61 (2026-08-25); SRC-GDOC-50 / DOC-2050 (2026-09-04 retrospective).

**CIPH-29 — Offline auth with key rotation for air-gapped installs** (Priority High)
- **Assignee: Diana** (task record) — note the diagnostic work and the local auth mock were run by Bob
- **Root cause:** Internal design flaw, not a vendor issue. The chosen key-rotation flow **assumes at least a brief network connection** to finish the handshake, so rotation cannot complete on a genuinely air-gapped site. Bob confirmed this against a local auth mock with the network denied and stated explicitly it is "the design," not a bug in the mock. No resolution has been found; the open question is whether the design changes or the offline requirement is relaxed.
- Sources: SRC-CU-CIPH-29 (blocked 2026-08-05 by Alice); SRC-SLACK-17 (2026-08-04/05); SRC-MEET-07 Weekly Sync (2026-08-05); SRC-GDOC-13 / DOC-2013.

### Summary table

| Task | Title | Assignee | Block type | Root cause |
|---|---|---|---|---|
| CIPH-17 | Coordinate/offset drift, multi-page PDFs | Charlie | **Upstream/external** | `pdfminer.six` whitespace bug; PR #992 unmerged; fork rejected |
| CIPH-46 | High-DPI PDF coordinate scaling | Charlie | **Upstream/external** | `pdf-lib-core` XObject transform bug in C++ core; maintainers unresponsive |
| CIPH-34 | Authenticated handshake, multi-site node sync | Bob | **Internal** | Handshake times out under high latency; AES-256 per-packet overhead exceeds round-trip budget |
| CIPH-47 | Async job scheduler, batch API | Bob | **Internal** | Concurrent I/O race on shared results manifest vs. multi-thread pool; ~10% throughput regression |
| CIPH-29 | Offline auth with key rotation | Diana | **Internal** | Rotation design assumes a network connection; cannot complete air-gapped |

### Caveats worth noting
- **CIPH-34 was blocked on 2026-09-22 itself** (Diana's "Handshake Timeout Block" entry and the same-day Fireflies deep dive), so it is included as of that date.
- Two other tasks involve the word "blocked" but are **not** in Blocked status and are excluded: **CIPH-39** (Windows builds — status **Active**; unsigned binary blocked by Defender/SmartScreen pending a code-signing certificate, assignee Evan) and **CIPH-21** (Release v1.0 Gates — status **Active**, under a security-gate hold pending T005 Docker CVE work and T029 Windows signing, assignee Evan).
- CIPH-34's internal classification rests on the team's own diagnosis (handshake design plus in-house AES-256 pipeline overhead); no external vendor or third-party component is implicated in the retrieved sources.
