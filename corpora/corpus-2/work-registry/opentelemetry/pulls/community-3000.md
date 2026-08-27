**Source ID**: [SRC-PR-02]

# Pull Request: Project Proposal: Ecosystem Explorer (open-telemetry/community#3000)

**Canonical URL**: https://github.com/open-telemetry/community/pull/3000  
**Author**: jaydeluca  
**Created**: 2025-09-19T10:11:57Z · **Updated**: 2025-12-02T08:40:24Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: merged (2025-12-01T19:04:18Z)  
**Branch**: `instrumentation-docs` → `main`  
**Changes**: +251 / -0 across 2 files  
**Labels**: area/project-proposal  
**Milestone**: —

---

## Description

This PR contains a project proposal for a new standalone "ecosystem explorer" documentation website.

POC can be seen here: https://jaydeluca.github.io/instrumentation-explorer/

Note: This project proposal is dependent on identifying collaborators for the staffing bit. We will use this project proposal doc to socialize the effort in hopes of finding people interested in participating.

Related:
- https://github.com/open-telemetry/opentelemetry.io/issues/7740
- https://github.com/open-telemetry/opentelemetry-java-instrumentation/issues/13468
- https://github.com/orgs/open-telemetry/projects/153?query=sort%3Aupdated-desc+is%3Aopen



## Discussion (16)

**jaydeluca** — 2025-09-19T12:34:33Z

> Is the Collector intentionally out of scope? From the discussions I have had with @svrnm it seems like this should be similar enough (instead of libraries we would be talking about components), so I feel like it would be a good idea to include it as well

@mx-psi yes and no. It's not _entirely_ left out of the scope (see [here](https://github.com/open-telemetry/community/pull/3000/files#diff-9f98d0309d3d9caafc8b541e0eb2fe512726fecb18f94a4d0831952c6b29a2d4R102-R105)), I have added evaluating the feasibility of this approach for both the collector and javascript as within scope, but I personally cannot commit to doing all the legwork for those as well. If we were to commit to a more concrete deliverable for those two projects, I think we will need a larger team.

Do you think the language I used around this isn't clear, or do you think it should be changed?

---

**mx-psi** — 2025-09-19T12:38:35Z

> > Is the Collector intentionally out of scope? From the discussions I have had with @svrnm it seems like this should be similar enough (instead of libraries we would be talking about components), so I feel like it would be a good idea to include it as well
> 
> @mx-psi yes and no. It's not _entirely_ left out of the scope (see [here](https://github.com/open-telemetry/community/pull/3000/files#diff-9f98d0309d3d9caafc8b541e0eb2fe512726fecb18f94a4d0831952c6b29a2d4R102-R105)), I have added evaluating the feasibility of this approach for both the collector and javascript as within scope, but I personally cannot commit to doing all the legwork for those as well. If we were to commit to a more concrete deliverable for those two projects, I think we will need a larger team.
> 
> Do you think the language I used around this isn't clear, or do you think it should be changed?

I guess my concern is with the naming, maybe something like "Ecosystem Documentation", and "Ecosystem explorer" would make people think that the Collector is (potentially) included, the current naming seems more focused on language libraries

---

**jaydeluca** — 2025-09-19T12:39:50Z

>  guess my concern is with the naming, maybe something like "Ecosystem Documentation", and "Ecosystem explorer" would make people think that the Collector is (potentially) included, the current naming seems more focused on language libraries

Ah yes, that makes sense, I can update. Thanks @mx-psi 

---

**svrnm** — 2025-09-19T14:26:38Z

@jaydeluca can you add a section about the existing registry, how this project and the registry are related to each other, for me it would be totally fine to say that this is going to replace the registry eventually.

---

**thompson-tomo** — 2025-10-01T03:14:12Z

So I have come here from the comment in the backstage channel.

Thinking about this what are the thoughts about building a backstage plugin to add support for open telemetry in a similar fashion to api's (https://github.com/backstage/backstage/blob/master/plugins/api-docs/README.md). We could then use backstage rather than building a tool for the ecosystem explorer.

I would see the development steps as being:
- introducing the telemetry section to list the signals and show the definitions in backstage
- Allow components (libraries) to define what signals they produce and link it to the definition just like they can for apis.
- Provide a way to show technology specific docs ie oracledb which provides descriptive info and the corresponding signals.

I also think it would be beneficial to ensure that weaver can be used to generate the file to add to the ecosystem Explorer so that as a user has one tool to use.

A nice thing I forsee is that we could potentially focus the sem conv specification section of the website on defining the base signals and the informative info is captured in the eco system Explorer.

---

**jaydeluca** — 2025-10-01T19:08:52Z

> Thinking about this what are the thoughts about building a backstage plugin to add support for open telemetry in a similar fashion to api's (https://github.com/backstage/backstage/blob/master/plugins/api-docs/README.md). We could then use backstage rather than building a tool for the ecosystem explorer.

Thanks for raising this @thompson-tomo, it is something we also considered and explored a bit.

I think the main concern is the tradeoff in complexity. Backstage brings a lot of functionality, but it also requires provisioning infrastructure, ongoing upgrades, and database maintenance. In my experience, it often needs a dedicated team to keep it running smoothly. For our use case, much of that extra functionality isn't really essential, and could actually slow us down.

The initial POC focused on a static-site approach which is much simpler to operate, has _almost_ no ongoing maintenance burden, and still meets our immediate needs. Personally, I'd much prefer a solution that requires as little operational overhead as possible.

---

**trask** — 2025-10-01T19:11:49Z

+1 on optimizing for low operational overhead since that's an area where we struggle as an Open Source project

---

**thompson-tomo** — 2025-10-06T05:26:18Z

I am all for a lower operational overhead but I do get worried when I see suggestions to build something as that can create tech debt especially when it is not a key part of the organisation business/objective. Hence suggestion to use an established product.

With the objective of low operational effort and static site generation in mind, we should be exploring how weaver can be contribute to the solution.

What I could foresee is:

- User defines a weaver registry file which imports signals from the sem conv registry
- User refines the imported signals based on what they are implementing
- User defines either a seperate implementation metadata file or adds it to the registry file. TBD
- Weaver codegen runs ie `weaver implementation generate` for the refined signals and metadata. This would produce boilerplate code which is used in the implementation and exports a yaml definition file (resolved schema).
- the exported yaml could be added to the eco-system which is proceeded by `weaver implementation describe` to emit the static content.

All of that would be reusable especially if the repo/package readme could also be generated in the same manner.

---

**jaydeluca** — 2025-10-06T10:17:57Z

@thompson-tomo who is a "user" in your example? This project is specifically aimed at creating documentation for java instrumentation (and possibly the collector and other languages as a stretch goal). There are over 250 instrumentations in the java project, and at this time none of them use weaver to define their attributes. I have experimented with introducing weaver to the project in order to generate metrics/attributes for an instrumentation, but as of this time, there are no existing plans by the SIG to rewrite everything in that repo to use weaver (that I am aware of).

I am all for integrating weaver where it makes sense, but if we are saying we need to convert that repo to use weaver before we move ahead with this project, I fear it would be a very long time before we could deliver anything useful. There's also a significant number of things involved here that go beyond just documenting the attributes that I don't think weaver helps with.

Are you perhaps suggesting a pattern for non-official-opentelemetry instrumentations to be included in the ecosystem, as opposed to thinking about the existing OpenTelemetry instrumentation? Or do you think every language will soon refactor all OpenTelemetry instrumentations to use weaver?

As of now, I was thinking of including an integration with weaver's live-check to be able to provide a "score card" for each instrumentation, which indicates whether the signals it emits are semconv compliant. If there are other use cases I would love to explore them, but I don't think the example flow you lay applies here (or at least I'm having a hard time understanding how it applies).

> I do get worried when I see suggestions to build something as that can create tech debt especially when it is not a key part of the organisation business/objective.

Could you elaborate on which organization business/objectives you are referring to? Is "OpenTelemetry" the "business" in this sense? Or is it CNCF? Are these objectives documented somewhere? Sorry if this is a stupid question, this is my first time proposing a project and it seems like there might be some additional context I need?

---

**thompson-tomo** — 2025-10-06T11:52:52Z

The User would be the instrumentation author.

> at this time none of them use weaver to define their attributes

I don't actually think that is the case given alot of them would be following semantic conventions & using the semantic conventions package which is/should be generated by weaver.

> there are no existing plans by the SIG to rewrite everything in that repo to use weaver

That is fine, Re-writing is an optional step and could be done incrementally ie switch to generated attributes rather than the package first. It is also perfectly ok, to just have the registry file and not generate any code.

> Are you perhaps suggesting a pattern for non-official-opentelemetry instrumentations to be included in the ecosystem

It would be a process for both official and third party instrumentations to follow.


I agree weaver doesn't do everything needed but what it does do is, enable you to design/document your telemetry. This is where I see it playing a key role.

Put it this way, I see the output of weaver as telemetry version's of an openapi/asyncapi document. This output can either be used to generate a human readable file ie markdown using weaver or it can be used directly in a Web portal.

For me The more tools an author needs to use, the more barriers we are creating especially when they are not integrated and data is needing to be duplicated.

To summarise I feel it is beneficial to be using weaver to document/describe the signals as well as the instrumentation emitting them as they should be sharing significant amounts of data. This way the eco-system Explorer can then focus on presenting and making discoverable the emitted definitions.

---

**jack-berg** — 2025-11-10T15:29:30Z

When I read this proposal, I see this project as a an attempt to build a new registry (registry 2.0). I'm very supportive of this as I've been complaining about various deficiencies of the registry for some time.

Significantly, the proposal is to launch the new effort in parallel to the existing registry, allowing the contributors to iterate quickly and avoid the friction of a bunch of up front data model design work and consensus gathering.

Later, once we've worked out the sharp edges, we can merge registry 1.0 into registry 2.0, and EOL registry 1.0.

Some thoughts:

- The registry already has a data model for capturing meta data about components (schema [here](https://github.com/open-telemetry/opentelemetry.io)), but its insufficient. As you note, there's all sorts of data which is important to capture and visualize for end users, which as of now, is very difficult for users to discover. The key examples being: configuration schema, schema of telemetry emitted, instructions on how to get started.
- The [registry](https://opentelemetry.io/ecosystem/registry/) already has tools for searching for components, and displaying bits of information about them, but its insufficient. More than anything else, the registry is an index of links, requiring the user to follow the link and find installation / configuration / telemetry schema details in the linked website / repository. Except this information is no always available, and when it is, there's no standardization about the display. A richer registry schema would allow a richer / more useful visualization experience.
- The registry already has [tooling](https://github.com/open-telemetry/opentelemetry.io/blob/main/scripts/registry-scanner/index.mjs) for scanning for project repositories and creating / updating registry component entries. The problem is, its all centralized in the `opentelemetry.io` project and standardized, meaning that its only possible to scrape the types of meta data which can scraped from a central script. In his prototype, @jaydeluca has built tooling which leverages domain knowledge specific to the `opentelemetry-java-instrumentation` project, and is therefore able to generate much richer meta data that is captured by the registry today. Any effort for a better registry is probably going to require some coordination between the repos where components live (i.e SDK, instrumentation, contrib, collector, etc) and the `opentelemetry.io` repo. Some shared tooling can / should be centralized in `opentelemetry.io`, but the repos should also work to do a better job of publishing the types of meta data that can't be generated through simple scanner scripts.

---

**svrnm** — 2025-11-18T07:54:04Z

> When I read this proposal, I see this project as a an attempt to build a new registry (registry 2.0). I'm very supportive of this as I've been complaining about various deficiencies of the registry for some time.

It absolutely is! That's why I am in favour of this project so much. The registry has been a building block of our project from day 1, but besides a few cosmetic changes we never lifted it to a proper solution.

> Significantly, the proposal is to launch the new effort in parallel to the existing registry, allowing the contributors to iterate quickly and avoid the friction of a bunch of up front data model design work and consensus gathering.

Yes 🙌 

> Later, once we've worked out the sharp edges, we can merge registry 1.0 into registry 2.0, and EOL registry 1.0.

I can barely wait for it ;) 

>     * The registry already has a data model for capturing meta data about components (schema [here](https://github.com/open-telemetry/opentelemetry.io?rgh-link-date=2025-11-10T15%3A29%3A30Z)), but its insufficient. As you note, there's all sorts of data which is important to capture and visualize for end users, which as of now, is very difficult for users to discover. The key examples being: configuration schema, schema of telemetry emitted, instructions on how to get started.

Yes, we can learn and take from the existing schema, but overall it's insufficient. 

>     * The [registry](https://opentelemetry.io/ecosystem/registry/) already has tools for searching for components, and displaying bits of information about them, but its insufficient. More than anything else, the registry is an index of links, requiring the user to follow the link and find installation / configuration / telemetry schema details in the linked website / repository. Except this information is no always available, and when it is, there's no standardization about the display. A richer registry schema would allow a richer / more useful visualization experience.

The registry as of today does what it was intended to do, provide a quick glance into all the things opentelemetry. but as the project evolved, the registry didn't, and as you lined out it's missing a lot of details and nuances, so this project aims to help with that. 

>     * The registry already has [tooling](https://github.com/open-telemetry/opentelemetry.io/blob/main/scripts/registry-scanner/index.mjs?rgh-link-date=2025-11-10T15%3A29%3A30Z) for scanning for project repositories and creating / updating registry component entries. The problem is, its all centralized in the `opentelemetry.io` project and standardized, meaning that its only possible to scrape the types of meta data which can scraped from a central script. In his prototype, @jaydeluca has built tooling which leverages domain knowledge specific to the `opentelemetry-java-instrumentation` project, and is therefore able to generate much richer meta data that is captured by the registry today. Any effort for a better registry is probably going to require some coordination between the repos where components live (i.e SDK, instrumentation, contrib, collector, etc) and the `opentelemetry.io` repo. Some shared tooling can / should be centralized in `opentelemetry.io`, but the repos should also work to do a better job of publishing the types of meta data that can't be generated through simple scanner scripts.

Those scripts (like most moving pieces of the registry) are hotfixes and bandage, so having having dedicated tooling and people taking care of it, is part of this proposal. I don't think it necessarily belongs into the dotio repo, in my mind we would have a repository who holds all the tooling to crawl that data and makes it accessible to consumers like opentelemetrydotio, but maybe others as well (think https://artifacthub.io/, backstage, CLI tools, etc.)



---

**thompson-tomo** — 2025-11-30T14:38:07Z

As another thought have we considered leveraging [artifact hub](https://artifacthub.io/) from the cncf and potentially just embedding an open telemetry collector plugin category as mentioned is possible in https://artifacthub.io/docs/topics/embedding_artifacts/

---

**svrnm** — 2025-12-01T08:20:26Z

> As another thought have we considered leveraging [artifact hub](https://artifacthub.io/) from the cncf and potentially just embedding an open telemetry collector plugin category as mentioned is possible in [artifacthub.io/docs/topics/embedding_artifacts](https://artifacthub.io/docs/topics/embedding_artifacts/)

Yes, we have considered that, it's one of the potential upstream receivers of this project. 


---

**trask** — 2025-12-01T18:36:48Z

@jaydeluca updating from `main` should resolve the link failure

---

**svrnm** — 2025-12-02T08:40:24Z

🎉 

## Reviews (15)

**svrnm** — CHANGES_REQUESTED — 2025-09-19T12:02:17Z

Thanks for leading this @jaydeluca -- this also replaces https://github.com/open-telemetry/community/pull/2246

**mx-psi** — COMMENTED — 2025-09-19T12:29:51Z

Is the Collector intentionally out of scope? From the discussions I have had with @svrnm it seems like this should be similar enough (instead of libraries we would be talking about components), so I feel like it would be a good idea to include it as well

**mx-psi** — COMMENTED — 2025-10-29T12:17:34Z

**vitorvasc** — COMMENTED — 2025-10-30T15:07:24Z

**svrnm** — COMMENTED — 2025-11-18T07:55:05Z

**svrnm** — COMMENTED — 2025-11-18T07:58:54Z

**svrnm** — COMMENTED — 2025-11-18T07:59:07Z

**svrnm** — COMMENTED — 2025-11-18T08:00:13Z

**svrnm** — COMMENTED — 2025-11-20T18:33:12Z

**svrnm** — APPROVED — 2025-11-20T19:18:34Z

**trask** — APPROVED — 2025-11-20T19:24:07Z

**maryliag** — APPROVED — 2025-11-20T20:54:14Z

**mx-psi** — APPROVED — 2025-11-21T10:32:49Z

**jack-berg** — APPROVED — 2025-11-21T15:57:47Z

**tedsuo** — APPROVED — 2025-12-01T18:24:54Z

## Review Comments (13)

**svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:58:43Z

Personally I would put the extraction and availability of the meta data first, and the web application second. There might be other places&tools where people would want to have that data available.

**svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:59:42Z

even if it would be a small one, I think having a dedicated SIG which is populated from Java&Comms and some other SIGs would be the way forward, and provide clear ownership.

**svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T11:59:55Z

```suggestion
* @svrnm (Severin Neumann)
```

**svrnm** on `projects/instrumentation-documentation.md` — 2025-09-19T12:00:51Z

```suggestion
* @jaydeluca (Grafana Labs)
* @svrnm (Causely)
* Looking for other leads with experience in OpenTelemetry instrumentation and/or web application development
```

I am happy to assist the project to get up to speed, but overall it would be a great opportunity to step up as lead.

**svrnm** on `projects/instrumentation-documentation.md` (line 205) — 2025-09-19T12:01:36Z

We might think about other projects outside of OpenTelemetry that would be interested in consuming this data, e.g. I could imagine that Backstage and similar projects could make use of this data. 

**mx-psi** on `projects/ecosystem-explorer.md` — 2025-10-29T12:16:22Z

I think we can list the Collector SIG here as well

**mx-psi** on `projects/ecosystem-explorer.md` (line 179) — 2025-10-29T12:16:48Z

I'd be happy to be listed as part of the Collector staffing

**vitorvasc** on `projects/ecosystem-explorer.md` (line 197) — 2025-10-30T15:07:24Z

```suggestion
* @jaydeluca (Jay DeLuca - Grafana Labs) - Java ecosystem
* @vitorvasc (Vitor Vasconcellos - Mercado Libre)  

```

**svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:55:05Z

based on the discussions we had, I think this is no longer entirely true?

**svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:58:54Z

```suggestion
1. Metadata Format Definition (Collaborative dependency)
```

"out of scope" might not be the right term here, it's not the primary purpose of the project, and as you have outlined below the goal is to use what exists or to **collaborate** with SIGs as they define their own. 

**svrnm** on `projects/ecosystem-explorer.md` — 2025-11-18T07:59:07Z

```suggestion
2. Metadata Creation (Collaborative dependency)
```

**svrnm** on `projects/ecosystem-explorer.md` (line 109) — 2025-11-18T08:00:13Z

```suggestion
The aim of this project is to create an Ecosystem Explorer web application that provides a user interface to
explore components across the OpenTelemetry ecosystem. The platform will be powered by structured
metadata and documentation extracted directly from instrumentation project source code, maintained through automated
processes.
```

**svrnm** on `projects/ecosystem-explorer.md` — 2025-11-20T18:33:12Z

```suggestion
* @mx-psi (Datadog)
```

cc @mx-psi @jaydeluca 

## Timeline

- 2025-09-19T12:02:37Z · **cross-referenced** by svrnm ← https://github.com/open-telemetry/community/pull/2246
- 2025-09-19T14:24:14Z · **renamed** by jaydeluca "Project Proposal: Instrumentation Documentation" → "Project Proposal: Ecosystem Explorer"
- 2025-09-19T14:31:52Z · **ready_for_review** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-09-19T14:31:53Z · **review_requested** by jaydeluca
- 2025-10-01T15:17:00Z · **labeled** by svrnm `area/project-proposal`
- 2025-10-03T15:12:52Z · **cross-referenced** by trask ← https://github.com/open-telemetry/community/issues/3049
- 2025-10-03T16:48:39Z · **cross-referenced** by jaydeluca ← https://github.com/open-telemetry/opentelemetry-java-instrumentation/issues/13468
- 2025-10-29T12:22:11Z · **cross-referenced** by mx-psi ← https://github.com/open-telemetry/opentelemetry-collector/issues/14096
- 2025-11-03T09:39:05Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-11-05T12:06:07Z · **cross-referenced** by mx-psi ← https://github.com/open-telemetry/opentelemetry-collector-contrib/issues/44057
- 2025-11-06T20:51:53Z · **review_requested** by jaydeluca
- 2025-11-19T10:48:10Z · **cross-referenced** by svrnm ← https://github.com/open-telemetry/opentelemetry.io/issues/2614
- 2025-12-01T19:04:18Z · **merged** by trask
- 2025-12-01T19:04:18Z · **closed** by trask
- 2025-12-02T08:42:03Z · **cross-referenced** by svrnm ← https://github.com/open-telemetry/community/issues/3175
- 2025-12-04T11:17:32Z · **cross-referenced** by svrnm ← https://github.com/open-telemetry/community/pull/3128
- 2026-01-20T22:34:11Z · **cross-referenced** by jaydeluca ← https://github.com/open-telemetry/community/issues/3230
- 2026-05-13T10:59:55Z · **cross-referenced** by kaspernissen ← https://github.com/open-telemetry/community/pull/3435

