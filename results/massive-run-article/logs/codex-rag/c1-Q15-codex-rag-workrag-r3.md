# For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?

<!-- RESPONSE_START -->

No. The nominal-latency pass is explicitly insufficient for field sign-off.

The current constraint is that the authenticated handshake must complete reliably on high-latency links—not merely on a LAN/nominal RTT. It currently fails at the Singapore field condition of **180 ms RTT**, so T024/CIPH-34 remains blocked pending encryption-path stabilization and a high-latency retest.

Planning must assume a **30-second timeout budget** on high-latency links (replacing the failing 5-second prototype budget). [WS-07/T024; CMT-2026-09-004; SRC-SLACK-27]
