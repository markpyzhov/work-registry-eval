**Source ID**: [SRC-ISSUE-03]

# Issue: Recommend immutable releases (open-telemetry/sig-security#164)

**Canonical URL**: https://github.com/open-telemetry/sig-security/issues/164  
**Author**: trask  
**Created**: 2025-08-27T13:31:30Z · **Updated**: 2026-01-28T22:16:50Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: closed (completed)  
**Labels**: —  
**Milestone**: —

---

## Description

https://github.blog/changelog/2025-08-26-releases-now-support-immutability-in-public-preview/

## Discussion (9)

**pellared** — 2025-09-16T12:52:39Z

I tested it on my side-project

Check: https://github.com/goyek/goyek/releases/tag/v2.3.0 and notice the "Immutable" text and icon as well as 
"Release attestation (json)" in the release assets .

Testing:

```
$ gh release verify v2.3.0 --repo goyek/goyek
Resolved tag v2.3.0 to sha1:580d400496e680ca42e42e5101f591dc1e6a747c
Loaded attestation from GitHub API
✓ Release v2.3.0 verified!
```

> [!CAUTION]
> It is not possible to add/edit/remove release assets (artifacts) after the release is published. 
> This is great, but maybe some repositories add the assets after the release is already published. The release process must be checked for the repositories before enabling the feature.

> [!IMPORTANT]
> This command cannot be used to verify the source code zip file or tarball for a release, since these assets are only created when a download is requested.


Docs:
- https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/immutable-releases
- https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/preventing-changes-to-your-releases
- https://docs.github.com/en/code-security/supply-chain-security/understanding-your-software-supply-chain/verifying-the-integrity-of-a-release



---

**pellared** — 2025-09-17T18:01:37Z

I also checked with my other side-project where releases are done by a GitHub workflow: https://github.com/golang-templates/seed/releases/tag/v0.22.0 where there also some assets:

```
$ gh release verify v0.22.0 --repo golang-templates/seed
Resolved tag v0.22.0 to sha1:530c65eeab67c878796dfe194057b7c475f8b9ae
Loaded attestation from GitHub API
✓ Release v0.22.0 verified!

Assets
NAME                             DIGEST                                                                 
seed_0.22.0_checksums.txt        sha256:c5d061763b8b72e23a6cacc0d2500fcd8fa98e6b1ceb931f589dfbbc194c590e
seed_0.22.0_darwin_amd64.tar.gz  sha256:a6972badaa8f8c78042499f42e524d8c3d82d5c046e38c91f7f50abd60cb25f7
seed_0.22.0_linux_amd64.tar.gz   sha256:1dfa16bc64b1c8bc76ad5a1da6aed4ed0d9ddb11fe51bfe81e0707d8bd0acbe7
seed_0.22.0_windows_amd64.zip    sha256:4a3d08e7745348c3292ede8cfd85570c1addcc355988188c40ebbc73a9184e37

$ wget https://github.com/golang-templates/seed/releases/download/v0.22.0/seed_0.22.0_linux_amd64.tar.gz

$ gh release verify-asset v0.22.0 seed_0.22.0_linux_amd64.tar.gz --repo golang-templates/seed
Calculated digest for seed_0.22.0_linux_amd64.tar.gz: sha256:1dfa16bc64b1c8bc76ad5a1da6aed4ed0d9ddb11fe51bfe81e0707d8bd0acbe7
Resolved tag v0.22.0 to sha1:530c65eeab67c878796dfe194057b7c475f8b9ae
Loaded attestation from GitHub API

✓ Verification succeeded! seed_0.22.0_linux_amd64.tar.gz is present in release v0.22.0
```



---

**pellared** — 2025-10-14T14:58:10Z

Related issue: https://github.com/ossf/scorecard/issues/4823

---

**trask** — 2025-10-23T02:38:58Z

> as well as "Release attestation (json)" in the release assets

Does this replace the need to attest individual artifacts, e.g. #79?

---

**pellared** — 2025-10-27T09:21:42Z

> > as well as "Release attestation (json)" in the release assets
> 
> Does this replace the need to attest individual artifacts, e.g. [#79](https://github.com/open-telemetry/sig-security/issues/79)?

I think it can replace it.

---

**pellared** — 2025-11-03T10:38:17Z

Preparing OTel Go for enabling the immutable releases:
- https://github.com/open-telemetry/opentelemetry-go/pull/7567

EDIT: Merged. We are ready for enabling imutable released for https://github.com/open-telemetry/opentelemetry-go and https://github.com/open-telemetry/opentelemetry-go-contrib

Related:
- https://github.com/integrations/terraform-provider-github/issues/2746

@trask, is it a blocker?


---

**trask** — 2025-11-07T00:20:03Z

> @trask, is it a blocker?

it doesn't need to block, let's do something like this: https://github.com/open-telemetry/admin/pull/346

---

**pellared** — 2025-12-11T17:43:19Z

I can confirm that it worked for Go (https://github.com/open-telemetry/opentelemetry-go/releases/tag/v1.39.0) and Go Contrib (https://github.com/open-telemetry/opentelemetry-go-contrib/releases/tag/v1.39.0).

In the meantime the feature went GA: https://github.blog/changelog/2025-10-28-immutable-releases-are-now-generally-available/

I propose to add GitHub Immutable Release to https://github.com/open-telemetry/sig-security/blob/main/docs/recommendations.md.

---

**pellared** — 2026-01-07T18:19:16Z

@trask, you can assign me. I also  suggest changing the title to "Recommend immutable releases"

## Timeline

- 2025-10-31T01:23:11Z · **cross-referenced** by trask ← https://github.com/open-telemetry/opentelemetry-dotnet/pull/6646
- 2025-11-03T09:39:05Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-03T10:30:37Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/pull/7567
- 2025-11-04T06:03:36Z · **referenced** by pellared
- 2025-12-03T10:14:03Z · **cross-referenced** by martincostello ← https://github.com/open-telemetry/opentelemetry-dotnet/issues/6748
- 2025-12-11T17:47:55Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-ebpf-instrumentation/issues/13
- 2026-01-07T18:28:05Z · **renamed** by trask "Enable immutable releases where possible" → "Recommend immutable releases"
- 2026-01-28T11:30:57Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/sig-security/pull/219
- 2026-01-28T22:16:50Z · **closed** by reyang

