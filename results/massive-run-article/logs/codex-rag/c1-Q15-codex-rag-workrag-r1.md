# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

No. The nominal-latency pass is explicitly insufficient for field sign-off.

The final state keeps zero-trust node sync blocked: the handshake fails at **180 ms RTT** under high latency, so field sign-off requires a successful high-latency retest. Planning must allow a **30-second timeout budget** for high-latency links, replacing the failing 5-second prototype budget. That budget is still not proven sufficient; encryption-path stabilization and/or handshake redesign may still be needed.  
Records: `WS-07/T024` (final work state, 2026-09-22); `CMT-2026-09-004`; `SRC-MEET-11`.
