# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, CIPH-32 is **Active (Reopened)**, assigned to Evan—not completed. [SRC-CU-CIPH-32]

It was reopened on 2026-09-15 after production-like batches hit the 500 MB hard halt before doing useful work; the fixed cutoff was too aggressive and had no soft buffer. [SRC-SLACK-23]

The monitor is being refactored to tolerate a **10% buffer above quota** instead of stopping at the hard 500 MB limit. Re-testing on the previously failing batch types showed no premature halts, but the task remains reopened while the revised behavior is finalized. [SRC-SLACK-23; SRC-CU-CIPH-32]
