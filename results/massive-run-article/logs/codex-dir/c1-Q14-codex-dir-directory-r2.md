# As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

<!-- RESPONSE_START -->

As of Sep. 22, T005 Docker and T029 Windows remain red, so T011 is still under the existing security-gate hold. The added calendar constraint makes that hold time-bound: if neither is green by Oct. 15, the release is a hard no-ship—not merely delayed. Docker still misses its ~450MB target with CVE verification failing; Windows remains blocked on an Authenticode certificate. The earlier completed security audit does not lift this release hold. [WS-03](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/work-states/WS-03-ops.md:26) [Sep. 22 brief](/Users/markpyzhov/VSCodeProjects/corpuses-arms/c1/briefs/2026-09-22-daily-brief.md:7)
