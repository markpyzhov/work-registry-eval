**Source ID**: [SRC-ISSUE-04]

# Issue: Monitoring bugs reported by OSS Fuzz (open-telemetry/opentelemetry-go#7549)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/issues/7549  
**Author**: pellared  
**Created**: 2025-10-06T17:08:06Z · **Updated**: 2025-11-03T13:06:55Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: open  
**Labels**: —  
**Milestone**: —

---

## Description

Is the TC triaging/monitoring the bugs reported by OSS Fuzz scans or is the the responsibility of individuals who added fuzz tests?

Notice that  cncf-opentelemetry-tc@lists.cncf.io is used as primary contact in OSS Fuzz: https://github.com/search?q=repo%3Agoogle%2Foss-fuzz%20cncf-opentelemetry-tc%40lists.cncf.io%20&type=code

For reference: https://issues.oss-fuzz.com/issues?q=opentelemetry%20status:new

Related: https://opentelemetry.io/blog/2024/fuzzing-audit-results/

CC @open-telemetry/collector-maintainers @open-telemetry/go-maintainers 

## Discussion (8)

**MrAlias** — 2025-10-07T14:44:09Z

FWIW I can only see the overview of issues. I am not able to get any details about them.

If we want maintainer to be a part of the resolution they will likely need access.

---

**trask** — 2025-10-09T03:53:40Z

> Is the TC triaging/monitoring the bugs reported by OSS Fuzz scans or is it the responsibility of individuals who added fuzz tests?

Makes sense to me for maintainers to own this.

It sounds like google accounts listed in `auto_ccs` have access.

Based on https://github.com/google/oss-fuzz/blob/12dbbede4b4a141c2cd62b504b80aa34f710e0b5/infra/pr_helper.py#L58-L62, I _think_ anyone in the `auto_ccs` can add additional people, so I suspect that @pellared can add other Go maintainers to `auto_ccs`.

Not really sure who should be listed in `primary_contact`. It doesn't really seem to do us any good to have distribution list as `primary_contact` since it seems that only google accounts can authenticate and get access to the details. So maybe just pick the maintainer who initially created the OSS Fuzz setup?

It may also be worth adding `file_github_issue: true`.

---

**lmolkova** — 2025-10-15T17:22:55Z

Discussed on the TC call 10/15:

- TC does not really triage or monitor Fuzz testing issues - TC email distribution list has been setup initially, but TC can't monitor and triage alerts across all repos. Also, TC does not have access to the detailed reports either.
- The general recommendation is to have fuzz testing enabled, but tooling choice, configuration, issue triage would be the responsibility of repo maintainers
- We'd love @open-telemetry/go-maintainers and/or @open-telemetry/collector-maintainers (who currently have this specific tool enabled) to evaluate usefulness and present results on the Spec / Maintainers call

On the access:

We should either setup email lists for each pre-repo maintainer group or report fuzz testing issues on GH. Either way, we need to update [auto_css for each OTel repo](https://github.com/google/oss-fuzz/blob/206656447b213fb04901d15122692d8dd4d45312/projects/opentelemetry/project.yaml#L6) as @trask mentioned above to include Google addresses of maintainers. There is a feature request to support GH groups - https://github.com/google/oss-fuzz/issues/8965, but there is no movement on it in the past years.



---

**dashpole** — 2025-10-29T15:09:30Z

I'm going to move this issue to opentelemetry-go, and we can figure out what changes we want to make to https://github.com/google/oss-fuzz/blob/c42f80f13662510727dcfa7a472c03031c149bc9/projects/opentelemetry-go/project.yaml#L4 to make this integration helpful for us.

---

**mx-psi** — 2025-10-29T16:38:40Z

(Fine with moving this to opentelemetry-go, I will keep lurking to see if we can reuse your solution for the Collector)

---

**dashpole** — 2025-10-30T16:13:50Z

@pellared is going to try and get an email list set up for the opentelemetry-go maintainers, which will be used to notify maintainers of oss-fuzz findings.  I assume we probably want one for the collector maintainers as well @mx-psi?

---

**mx-psi** — 2025-10-30T16:15:16Z

Yes, I think that would make sense

---

**pellared** — 2025-11-03T12:42:36Z

It looks like maintainers needs to add their private Google accounts.

From https://google.github.io/oss-fuzz/getting-started/new-project-guide/#primary:

> you’ll need to use a [Google account](https://support.google.com/accounts/answer/176347?hl=en) to get full access.
>
> Why do you require a Google account for authentication?
>
> Our [ClusterFuzz](https://google.github.io/oss-fuzz/further-reading/clusterfuzz) fuzzing infrastructure and [issue tracker](https://bugs.chromium.org/p/oss-fuzz/issues/list) require a Google account for authentication. Note that an alternate email address associated with a Google account does not work due to appengine api limitations.

@open-telemetry/go-maintainers, you can add your Google account as `auto_ccs` in https://github.com/google/oss-fuzz/blob/master/projects/opentelemetry-go/project.yaml and https://github.com/google/oss-fuzz/blob/master/projects/opentelemetry-go-contrib/project.yaml and sign-in to https://issues.oss-fuzz.com.

However, I also have another proposal:
- https://github.com/google/oss-fuzz/issues/14230

This would be IMO a better integrated and more secure solution. We can wait a couple of days to see if there is any feedback regarding the proposal from the OSS Fuzz team.

## Timeline

- 2025-10-29T15:08:30Z · **transferred** by dashpole
- 2025-11-03T09:39:05Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-03T15:04:05Z · **cross-referenced** by dashpole ← https://github.com/google/oss-fuzz/pull/14233
- 2025-11-03T16:34:10Z · **referenced** by AdamKorcz
- 2025-11-04T08:03:05Z · **cross-referenced** by dmathieu ← https://github.com/google/oss-fuzz/pull/14240
- 2025-11-04T17:25:21Z · **referenced** by DavidKorczynski

