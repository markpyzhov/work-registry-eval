# License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

<!-- RESPONSE_START -->

As of 2026-09-22, T030/CIPH-40 is **reopened and active**: a P0 Legal gate remains open, and viable non-AGPL PDF-parser discovery is still manual triage. [WS-04](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-04-policy.md)

The initial Ghostscript remediation was treated as complete after a parser swap, but follow-up review found the replacement itself AGPL-licensed, so the task was reopened. [Audit report](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/documentation/sources/2026-08-21-License-Compliance-Audit-Report.md) [Reopen thread](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-12-license-agpl-reopen.md)

Charlie’s discovery search targets an Apache 2.0 or MIT parser that satisfies rasterization/parsing needs; candidates then had coverage gaps. Closure additionally requires adoption, a clean full-tree scan, and no restrictive copyleft in shipped dependencies—engineering selection alone does not clear the Legal gate. [CIPH-40](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/tasks/CIPH-40-License-Compliance-Review.md) [Parser-swap thread](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/med-synth/communication/sources/slack/2026-08-11-license-parser-swap.md)
