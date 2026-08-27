# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, **CIPH-32 is Active (Reopened)**, assigned to Evan. [SRC-CU-CIPH-32]

It was originally marked done after Diana verified that writes stopped at the configured **500 MB floor**. Later, on Sep 15, production-like batches showed that this hard halt triggered before they could do useful work; the flat cutoff had no soft buffer. [SRC-SLACK-23]

The monitor is being refactored to tolerate a **10% buffer above quota** instead of abruptly halting at the 500 MB limit. A Sep 18 retest found no premature halts on the previously failing batch cases, but the task remains reopened. [SRC-CU-CIPH-32; SRC-SLACK-23]
