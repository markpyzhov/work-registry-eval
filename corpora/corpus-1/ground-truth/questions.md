# Corpus 1 Questions

## Q01

As of the final CipherDoc snapshot on **2026-09-22**, is the toolkit ready to ship v1.0.0? Give a clear go/no-go, name every release gate that is still open, and cite the evidence that keeps each gate from closing.

## Q02

Docker packaging was once treated as finished. As of **2026-09-22**, what is the authoritative status of that work, what earlier completion claim does it supersede, and what concrete size and CVE outcomes still prevent calling the image release-ready?

## Q03

Large-file chunking was merged in mid-August. As of **2026-09-22**, has that completion held? Reconstruct the completion → reopen timeline, the technical root cause, and who owns the next engineering action.

## Q04

Storage quota monitoring was marked done after a hard-halt check. As of **2026-09-22**, what is the current status, what later evidence reopened it, and what buffer change is underway?

## Q05

License compliance looked cleared after a PDF-parser swap, then changed again. As of **2026-09-22**, what is the current license-gate status, what discovery reopened it, and what replacement criteria are in force?

## Q06

For closing the v1.0.0 release checklist as of **2026-09-22**, which dependency gates must go green first, and for each material gate name the listed task assignee versus who owns the immediate next action when those differ?

## Q07

As of **2026-09-22**, which CipherDoc tasks are blocked, and for each is the block upstream/external or internal? State the root cause and the listed task assignee.

## Q08

Windows compatibility produced a working build artifact. As of **2026-09-22**, is the Windows release gate cleared? Separate engineering completion from the remaining release hold and say what still has to happen.

## Q09

Beyond Docker and Windows packaging, which compliance and audit items still hold v1.0.0 as of **2026-09-22**? For each, give current status, the concrete defect or risk, and whether engineering search alone can close it.

## Q10

Write a concise cross-workstream management briefing as of **2026-09-22** covering at least three workstreams: at least two completed milestones that still hold, at least three items of work that were completed then reopened, at least two durable blockers, and the top risks that should escalate before ship. Do not present reopened work as done.

## Q11

On the critical path to clearing the security-gate hold, what are the next actions as of **2026-09-22**, and who owns each next action (not merely the listed task assignee if those differ)?

## Q12

Several streams remain blocked while others are only reopened. As of **2026-09-22**, what work can still advance in parallel, what cannot progress until an external dependency moves, and what release-checklist work is gated on packaging and Windows signing?

## Q13

A clinic batch includes a scanned invoice with no usable native text layer, so OCR runs. Mid-job an unhandled worker exception fires before any export is finalized. OCR confidence on the page being processed was 82%. As of the **2026-09-22** rule set, what must happen to outputs and temps, what crash report is written, how the 90% manual-review rule applies (or does not) to this abort, and which related audit/OCR implementation items are still unfinished?

## Q14

As of the final project snapshot after **2026-09-22**, what hard calendar constraint, if any, now governs shipping v1.0.0 if Docker packaging and Windows signing stay red, and how, if at all, does that change the earlier security-gate hold?

## Q15

For zero-trust node sync field sign-off as of the final project snapshot, is the earlier nominal-latency handshake pass enough? What high-latency field constraint, if any, now applies, and what timeout budget, if any, must planning assume?
