**Source ID**: SRC-SLACK-06

# Slack Thread: Docker Image Size Optimization
**Channel**: #releases
**Thread opened**: 2026-06-25
**Last activity**: 2026-08-12

---

**[2026-06-25 09:35] Diana**: @Evan, I just pulled the latest `cipherdoc` image. It's 2.1GB! That's way too big for a local runtime deployment. Reopening the Docker packaging task.

**[2026-08-01 09:30] Evan**: Whoa, 2.1GB, and we still haven't closed out the CVE verification either. Looks like the full Ubuntu base is a big part of the bloat. I'll put together a multi-stage build plan targeting somewhere around 450MB.

**[2026-08-01 09:33] Diana**: That'd get it onto standard dev laptops without eating all the disk space. Let's aim for that.

**[2026-08-01 10:04] Evan**: Multi-stage build plan is in place. Stripping out the build-time dependencies from the final artifact.

**[2026-08-04 13:11] Evan**: The multi-stage split alone still leaves the base layer too large. Swapping from `ubuntu:22.04` to `alpine:latest` as the base. Had some issues with `glibc` vs `musl`, but `gcompat` seems to fix it.

**[2026-08-07 15:21] Evan**: Alpine swap didn't get us all the way there either. Just removed the unused OCR and runtime packages we aren't shipping in this build.

**[2026-08-12 09:00] Diana**: Checked the size and ran the CVE scan. We're still over the ~450MB target, and the CVE verification is still failing.

**[2026-08-12 09:10] Evan**: Yeah, not where we need to be yet. There's still fluff in the Python site-packages layer, and I need to chase down what's tripping the CVE scan.

**[2026-08-12 09:13] Diana**: Reopened status stands until both the size and the CVE check are clean. I'll keep tracking it against the release checklist.
