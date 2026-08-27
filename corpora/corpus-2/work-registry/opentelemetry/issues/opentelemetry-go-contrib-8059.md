**Source ID**: [SRC-ISSUE-05]

# Issue: otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable (open-telemetry/opentelemetry-go-contrib#8059)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go-contrib/issues/8059  
**Author**: codeboten  
**Created**: 2025-10-22T21:25:29Z · **Updated**: 2026-04-03T11:34:34Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: closed (completed)  
**Labels**: enhancement, area: file-config  
**Milestone**: untracked

---

## Description

### Component

Config

### Problem Statement

As per the spec:

> Setting the [OTEL_EXPERIMENTAL_CONFIG_FILE](https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/configuration/sdk-environment-variables.md#declarative-configuration) environment variable (for languages that support it) provides users a convenient way to initialize OpenTelemetry components without needing to learn language-specific configuration details or use a large number of environment variables. The pattern for accessing the configured components and installing into instrumentation will vary by language. For example, the usage in Java might resemble:

https://github.com/open-telemetry/opentelemetry-specification/blob/main/specification/configuration/sdk.md#via-otel_experimental_config_file

### Proposed Solution

Open to suggestions of how this should be implemented to align w/ the rest of the Go SDK implementation

### Alternatives

_No response_

### Prior Art

_No response_

### Additional Context

_No response_

## Discussion (2)

**codeboten** — 2025-10-23T17:18:25Z

After discussing it at the 23-OCT SIG call, the decision is in the short term to include this in an `init` function in the otelconf package that will automatically configure the SDK components

---

**dashpole** — 2025-12-04T18:32:17Z

> in the short term to include this in an init function in the otelconf package

Out of curiosity, what is the long-term plan?

## Timeline

- 2025-10-22T21:25:30Z · **labeled** by codeboten `enhancement`
- 2025-10-22T21:25:42Z · **labeled** by github-actions[bot] `area: file-config`
- 2025-10-22T21:27:48Z · **renamed** by codeboten "[Feature]: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable" → "otelconf: add support for OTEL_EXPERIMENTAL_CONFIG_FILE variable"
- 2025-10-30T21:39:26Z · **referenced** by codeboten
- 2025-10-30T21:40:31Z · **cross-referenced** by codeboten ← https://github.com/open-telemetry/opentelemetry-go-contrib/pull/8106
- 2025-11-03T09:30:28Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-24T19:47:10Z · **referenced** by codeboten
- 2025-11-27T17:50:35Z · **referenced** by codeboten
- 2025-12-04T23:38:10Z · **closed** by MrAlias
- 2026-04-03T11:34:34Z · **milestoned** by pellared → untracked

