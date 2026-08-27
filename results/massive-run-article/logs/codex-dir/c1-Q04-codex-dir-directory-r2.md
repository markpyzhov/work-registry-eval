# Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

<!-- RESPONSE_START -->

As of 2026-09-22, storage quota monitoring (T022/CIPH-32) is **reopened and active**, not done; WS-07 lists it unchecked and calls for buffer-refactor verification. [WS-07-storage](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-07-storage.md)

It was marked done on 2026-08-06 after a test confirmed writes halted at a **500MB** free-space floor. Production-like batches later hit that hard halt before useful work, so Evan reopened it on 2026-09-15. [Storage Quota Halt](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-06-storage-quota-halt.md)

Bob replaced the hard cutoff with a **10% above-quota buffer**; a same-batch retest reported no premature halts. However, capacity planning corrected the production baseline to **2GB free disk**, not 500MB, and requires retargeting thresholds plus clinic-VM re-verification. [September comments](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/comments/2026-09.md)
