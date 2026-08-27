# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, storage quota monitoring (CIPH-32) is **Active (Reopened)**, assigned to Evan. [SRC-CU-CIPH-32]

It had been marked complete after Diana verified that writes halted at the configured 500 MB floor. Later, production-like batches began hitting that hard halt before completing useful work, showing the fixed cutoff was too aggressive and lacked a soft buffer. [SRC-SLACK-23; SRC-GDOC-36]

The monitor is being refactored to tolerate a **10% buffer above quota** rather than stopping immediately at the hard limit. A re-test reported no premature halts on the previously failing batch profiles, but the task remains reopened. [SRC-SLACK-23; SRC-CU-CIPH-32]
