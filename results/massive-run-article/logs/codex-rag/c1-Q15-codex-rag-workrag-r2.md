# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

No. The nominal-latency pass is not sufficient for field sign-off.

The final Work State keeps CIPH-34 blocked: the handshake must complete reliably under high-latency conditions, not merely on a local/nominal network. It currently times out on slow links, including the 180 ms RTT field scenario, pending encryption-path stabilization and a high-latency retest. (`WS-07`, 2026-09-22; `SRC-CU-CIPH-34`; `SRC-SLACK-27`; `SRC-MEET-11`)

Planning must assume a **30-second timeout budget** for high-latency links. That is a required planning constraint, not evidence that a timeout increase has resolved the issue—the final snapshot explicitly leaves open whether 30 seconds will be sufficient without redesigning the handshake exchange. (`WS-07`, blocker T024 / `CMT-2026-09-004`)
