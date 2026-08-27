# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, T022 / CIPH-32 is **reopened and active**; verification of the quota-monitor buffer refactor remains pending. *(WS-07, S4)*

It was reopened on 2026-09-15 after production-like batches hit the **500 MB hard halt before doing useful work**—showing the flat cutoff was too aggressive. *(SRC-SLACK-23)*

The monitor is being changed from that hard 500 MB cutoff to a **10% buffer tolerance above quota**. Production planning also sets the free-disk baseline at **2 GB, not 500 MB**. Bob refactored the loop; a September 18 retest reported no premature halts, with final refactor verification still needed. *(WS-07; SRC-SLACK-23; SRC-CU-CIPH-32)*
