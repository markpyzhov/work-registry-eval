**Source ID**: [SRC-ISSUE-06]

# Issue: Restore deprecated `UnaryClientInterceptor` to maintain backwards compatibility (open-telemetry/opentelemetry-go-contrib#8078)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8078  
**Author**: nicholasngai  
**Created**: 2025-10-27T23:28:07Z · **Updated**: 2025-10-31T09:47:48Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: closed (not_planned)  
**Labels**: —  
**Milestone**: —

---

## Description

Signal boosting [this comment](https://github.com/open-telemetry/opentelemetry-go-contrib/issues/7104#issuecomment-3412968109):

Hey folks! Can we revisit the decision to remove `UnaryClientInterceptor` and friends from this library? Is there any security issue with leaving that API in?

I understand Otel is still in an unstable version, but this change means we are no longer able to upgrade otelgrpc to the latest version anymore. We have a pretty big chain of dependencies internally depending on otel and bumping all of them is not a simple matter. We won’t be able to upgrade otelgrpc until the entire dependency chain which spans across multiple orgs and third-party libraries is up to date.

Is it possible to avoid breaking changes to the API surface even if the module counts as unstable?

## Discussion (11)

**dmathieu** — 2025-10-28T08:36:24Z

cc @dashpole as code owner.

---

**dashpole** — 2025-10-28T20:02:57Z

Can you share more about why you aren't able to migrate to the stats handler?  We [deprecated](https://github.com/open-telemetry/opentelemetry-go-contrib/pull/4534) the interceptors almost 2 years ago, which seems like plenty of time to migrate.

---

**nicholasngai** — 2025-10-28T20:40:37Z

Even if we removed all of our references, references in transitive dependencies still cause compilation errors, and we don’t have control over the timeline at which transitive dependencies remove those code references.

---

**dmathieu** — 2025-10-29T08:35:31Z

That doesn't look like a good reason to me. There will always be unmaintained transitive dependencies that prevent this kind of upgrades.
That's tech debt that needs to be fixed, not kept on our end.

---

**nicholasngai** — 2025-10-29T16:28:55Z

The question is really whether we can rely on otelgrpc to be stable! For now, we are stuck on v0.58.0 because of compilation errors on higher versions introduced by the breaking change. If there is an urgent security patch introduced, we won’t be able to upgrade to it.

Generally, with Golang, we avoid breaking changes aggressively avoid these kinds of things. Does maintaining this interceptor involve significant overhead from the maintainers?

---

**MrAlias** — 2025-10-29T17:37:26Z

Please do not rely on an unstable package as being stable.

---

**nicholasngai** — 2025-10-29T17:38:42Z

Are there plans to make this package stable? Or are we sticking with [ZeroVer](https://0ver.org/) for the forseeable future?

---

**MrAlias** — 2025-10-29T18:06:47Z

> Are there plans to make this package stable?

There is definitely desire among project contributor to progress this package towards stability. But please understand this is an open-source project. It is driven by a the dedicated effort of engineers who donate their time to working on this. That time is valuable and allocated to many efforts.

I'm happy to add the question of stabilization to our weekly SIG meeting happening tomorrow. @nicholasngai I would strongly suggest you attend the meeting tomorrow to discuss your use-case and help motivate allocation of effort for this stabilization. I don't anticipate this stabilization happening within 2025, but I could see us prioritizing it for 2026 if we have community involvement and/or added developer help here.

---

**dashpole** — 2025-10-29T18:51:27Z

It is also worth calling out that we depend on telemetry naming conventions, which are still unstable for gRPC, and prevent us from making the module stable.

---

**dmathieu** — 2025-10-30T08:46:26Z

otelgrpc being unstable, it's kinda as if we were starting from scratch today. If that were the case, we wouldn't implement something that is deprecated in the underlying API, that makes no sense.

Even if we make the package stable today, we still wouldn't implement something that is deprecated. The only case where we'd keep deprecated code is if we were stable and needed to keep backwards compatibility.

---

**dmathieu** — 2025-10-31T09:47:48Z

Closing, as based on yesterday's discussions during the SIG meeting, we have agreement that we won't bring back the interceptor.
Note that nothing prevents you from copying the code as it was before and setting up your own internal module.

## Timeline

- 2025-10-31T09:47:48Z · **closed** by dmathieu
- 2025-11-03T09:39:05Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648

