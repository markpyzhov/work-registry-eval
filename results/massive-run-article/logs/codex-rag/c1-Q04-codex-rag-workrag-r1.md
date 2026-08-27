# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, storage quota monitoring (T022/CIPH-32) is **reopened and active**; its buffer-refactor verification is still needed. [WS-07, 2026-09-22]

It was reopened after **production-like batches hit the 500MB hard halt before doing useful work**—evidence that the flat cutoff was too aggressive. [SRC-SLACK-23, 2026-09-15]

The monitor is being changed from the hard 500MB stop to a **10% tolerance above the quota**; the production quota baseline is also being set to **2GB free disk** rather than 500MB. Bob refactored it, and a re-test found no premature halts, pending final verification. [SRC-SLACK-23, 2026-09-18; CMT-2026-09-003; WS-07]
