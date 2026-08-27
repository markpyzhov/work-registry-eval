# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, **CIPH-32/T022 is reopened and active**; its quota-monitor buffer refactor still needs verification. (`WS-07`, last updated 2026-09-22)

It was reopened on September 15 after **production-like batches hit the 500 MB hard halt before doing useful work**—the flat cutoff had no soft buffer. (`SRC-SLACK-23`)

The change underway is a **10% buffer tolerance above quota** instead of an immediate 500 MB hard halt. Operations is also setting the production free-disk baseline to **2 GB, not 500 MB**. (`SRC-SLACK-23`; `SRC-CU-CIPH-32`; `CMT-2026-09-003`)
