**Source ID**: [SRC-PR-05]

# Pull Request: Optimize histogram reservoir (open-telemetry/opentelemetry-go#7443)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/pull/7443  
**Author**: dashpole  
**Created**: 2025-10-02T13:56:40Z · **Updated**: 2025-12-15T15:00:11Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: merged (2025-12-15T14:59:34Z)  
**Branch**: `optimize_histogram_reservoir` → `main`  
**Changes**: +173 / -61 across 8 files  
**Labels**: —  
**Milestone**: v1.40.0

---

## Description

This improves the concurrent performance of the histogram reservoir's Offer function by 4x (i.e. 75% reduction).

Accomplish this by locking each measurement, rather than locking around the entire storage.  Also, defer extracting the trace context from context.Context until collection time. This improves the performance of Offer, which is on the measure hot path.  Exemplars are often overwritten, so deferring the operation until Collect reduces the overall work.

```
                           │   main.txt   │              hist.txt              │
                           │    sec/op    │   sec/op     vs base               │
FixedSizeReservoirOffer-24    211.4n ± 3%   177.5n ± 3%  -16.04% (p=0.002 n=6)
HistogramReservoirOffer-24   200.85n ± 2%   47.41n ± 2%  -76.40% (p=0.002 n=6)
geomean                       206.1n        91.73n       -55.48%
```

Benchmarks for Measure:
```
                                                                                 │  main.txt   │             histres.txt             │
                                                                                 │   sec/op    │    sec/op     vs base               │
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/0-24                 436.7n ± 4%   114.8n ±  5%  -73.72% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/10-24                472.2n ± 2%   169.7n ±  8%  -64.08% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/0-24               431.0n ± 2%   116.3n ±  2%  -73.01% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/10-24              470.9n ± 1%   171.0n ±  5%  -63.70% (p=0.002 n=6)
```

I explored using a []atomic.Pointer[measurement], but this had similar performance while being much more complex (needing a sync.Pool to eliminate allocations).  The single-threaded performance was also much worse for that solution.  See https://github.com/open-telemetry/opentelemetry-go/compare/main...dashpole:optimize_histogram_reservoir_old.

## Discussion (9)

**codecov[bot]** — 2025-10-02T13:58:33Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 86.2%. Comparing base ([`c15644d`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/c15644d64e72535afcedcb50628b381743b676dc?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)) to head ([`95f44c1`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/95f44c1d82272c369fcd986ec808e2891edc80e6?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)).
:warning: Report is 1 commits behind head on main.

<details><summary>Additional details and impacted files</summary>



[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443/graphs/tree.svg?width=650&height=150&src=pr&token=8efTmh4kvf&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@           Coverage Diff           @@
##            main   #7443     +/-   ##
=======================================
- Coverage   86.2%   86.2%   -0.1%     
=======================================
  Files        302     302             
  Lines      21973   21971      -2     
=======================================
- Hits       18949   18947      -2     
  Misses      2643    2643             
  Partials     381     381             
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [sdk/metric/exemplar/fixed\_size\_reservoir.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Ffixed_size_reservoir.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9maXhlZF9zaXplX3Jlc2Vydm9pci5nbw==) | `94.7% <100.0%> (ø)` | |
| [sdk/metric/exemplar/histogram\_reservoir.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Fhistogram_reservoir.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9oaXN0b2dyYW1fcmVzZXJ2b2lyLmdv) | `90.9% <100.0%> (-1.7%)` | :arrow_down: |
| [sdk/metric/exemplar/storage.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7443?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Fstorage.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9zdG9yYWdlLmdv) | `100.0% <100.0%> (ø)` | |
</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**bboreham** — 2025-10-13T14:23:19Z

On further reflection, I fixed the copying issue before running the benchmark, so it is perhaps reasonable that less racy code runs slower.

Would be good if the tests and/or linter detected the issue.  I note that `NoCopy` was removed from `atomic.Value` here: https://github.com/golang/go/issues/21504.

---

**dashpole** — 2025-10-15T01:08:33Z

I also see slightly worse results, but agree it is definitely better to be correct.  I'll work on a test.

---

**dashpole** — 2025-10-15T15:40:05Z

I added a ConcurrentSafe test, and verified that it fails (quite spectacularly) with the previous atomic.Value implementation.

---

**dashpole** — 2025-10-15T16:31:22Z

The concurrent safe test found another race condition around my usage of sync.Pool, which i'm looking into

---

**dashpole** — 2025-10-15T20:08:23Z

The other race had to do with my usage of sync.Pool.  After Collect loaded an element, that element could be placed into the sync.Pool by a subsequent store() that replaced the measurement, and then modified by another store() that retrieved it from the sync.Pool.  I worked out a way to fix this, but it made the performance around ~45ns.  In the end, I decided to just lock around each measurement, since that has the same parallel performance, is much more simple and readable, and has better single-threaded performance.

---

**dashpole** — 2025-12-11T17:24:14Z

I put the Measure benchmarks in the description.  Not as good of an improvement as I had expected, so i'll have to dig into that more...

---

**dashpole** — 2025-12-11T19:04:33Z

@dmathieu if you have the chance to review, this is related to other optimization PRs.

---

**dashpole** — 2025-12-11T20:43:53Z

I figured out why the benchmark results were so poor: The benchmark was recording all observations in a single bucket, and each bucket has its own lock, so there were effectively no parallelism gains.  I switched the benchmark to record observations in different buckets, and that shows that this is a ~70% performance improvement when exemplars are being recorded.

## Reviews (19)

**MrAlias** — COMMENTED — 2025-10-03T16:04:21Z

**dashpole** — COMMENTED — 2025-10-03T16:12:33Z

**MrAlias** — COMMENTED — 2025-10-03T16:34:09Z

**dashpole** — COMMENTED — 2025-10-03T17:34:51Z

**dashpole** — COMMENTED — 2025-10-03T20:12:48Z

**MrAlias** — COMMENTED — 2025-10-03T22:44:49Z

**dashpole** — COMMENTED — 2025-10-04T03:45:24Z

**MrAlias** — APPROVED — 2025-10-07T15:50:33Z

**bboreham** — COMMENTED — 2025-10-12T21:22:58Z

**dashpole** — COMMENTED — 2025-10-15T01:06:50Z

**bboreham** — APPROVED — 2025-10-15T16:23:32Z

lgtm

**dashpole** — COMMENTED — 2025-10-15T20:05:58Z

**bboreham** — APPROVED — 2025-10-16T10:31:14Z

Much simpler now.

**dashpole** — COMMENTED — 2025-10-16T12:37:15Z

**MrAlias** — COMMENTED — 2025-11-06T21:30:53Z

Overall, looks good to me. Just testing cleanup.

**dashpole** — COMMENTED — 2025-11-20T16:11:59Z

**MrAlias** — COMMENTED — 2025-12-11T17:06:00Z

**MrAlias** — APPROVED — 2025-12-11T18:33:50Z

**dmathieu** — APPROVED — 2025-12-15T10:46:18Z

## Review Comments (27)

**MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T15:57:03Z

```suggestion
	// Ctx is the context active when a measurement was made.
```

**MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:04:03Z

This will potentially return measurements from the next collection cycle. There is no lock guarding additions here.

What about implementing an similar hot/cold storage?

**dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:12:32Z

There is still a global ordering for Offer vs Collect calls.  Consider a histogram with a single bucket.  Each Offer call that updates the atomic.Value prior to the Load() call in Collect can be considered to have happened in the previous collection interval.  Each Offer call that updates the atomic.Value after the Load() call can be considered to have happened in the next collection interval.  That principle still holds true for histograms with multiple buckets.

I don't think the complexity of hot/cold storage is necessary (at least not for histogram reservoirs)

**MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T16:34:09Z

I think that works for a single bucket. But for the case of multiple buckets this could report values for subsequent buckets that occurred after a "collection cycle" for a previous bucket ended. I don't think a collection cycle is defined on a per-bucket basis, right?

**dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T17:34:51Z

The race that this allows is the following:

```golang
// Record a measurement in bucket A
myHist.Record(ctx, 1)
// Record a measurement in bucket B
myHist.Record(ctx, 10000)
```

In this case, it is possible for the measurement in bucket B to be included in a collection interval, but the measurement in bucket A is not included.  That would happen if we collect bucket A, then measure to buckets A and B, then collect bucket B.

A similar case exists for https://github.com/open-telemetry/opentelemetry-go/pull/7427 as well.  Doing:

```golang
// Record a measurement with attribute set a
myCounter.Add(ctx, 1, a)
// Record a measurement with attribute set b
myCounter.Add(ctx, 10000, b)
```

The above can result in the add to attribute set `b` being included in collect, but attribute set `a` is not, since we do not globally prevent measurements during collection, and we don't iterate over attribute sets in a predictable order.

The second race (with different attribute sets) seems worse than the exemplar case, IMO, and I think both are acceptable.

**dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-03T20:12:48Z

Another other race that already exists in the SDK today is recording on two different instruments:

```golang
// Record a measurement on counter a
counterA.Add(ctx, 1)
// Record a measurement on counter b
counterB.Add(ctx, 10000)
```

Since we lock at the instrument level, it is possible today for collect to include the increment to counterB, but not the increment to counterA.

**MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-03T22:44:49Z

Gotcha. Let's stick with your current approach 👍

Can you add a comment explaining the potential inconsistency and that it is a decision made after considering the disadvantages/benefits and alternatives?

**dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-04T03:45:24Z

I opened https://github.com/open-telemetry/opentelemetry-go/pull/7453 to discuss and make sure everyone is on the same page.  I also added a comment here.

**MrAlias** on `sdk/metric/exemplar/storage.go` — 2025-10-07T15:50:17Z

```suggestion
	// Ctx is the active context when a measurement was made.
```

**bboreham** on `sdk/metric/exemplar/storage.go` — 2025-10-12T20:38:18Z

The type of `val` is `atomic.Value`, so this line seems to violate:
```
// Once [Value.Store] has been called, a Value must not be copied.
```

**bboreham** on `sdk/metric/exemplar/storage.go` — 2025-10-12T21:21:19Z

```suggestion
	measurements []atomic.Pointer[measurement]
```
Uses half the bytes and makes the code neater.  Unfortunately when I tried it, the benchmark ran slower (43ns instead of 37ns). This has to be some weird artefact.

**dashpole** on `sdk/metric/exemplar/storage.go` — 2025-10-15T01:06:50Z

Good catch.

**bboreham** on `sdk/metric/exemplar/reservoir_test.go` — 2025-10-15T16:22:27Z

Maybe a little bit of comment around why 5 and 2 are good numbers?

**dashpole** on `sdk/metric/exemplar/reservoir_test.go` — 2025-10-15T20:05:58Z

I reduced it to 2 and 1, and documented them.

**bboreham** on `sdk/metric/exemplar/fixed_size_reservoir.go` (line 132) — 2025-10-16T10:25:31Z

drive-by: I think this (and all similar code) should be `len` not `cap`.
In the current code they are always the same, but it's a slight jar when reading it to wonder what was intended.

**bboreham** on `sdk/metric/exemplar/storage.go` (line 62) — 2025-10-16T10:30:55Z

I couldn't figure out why this changed, and I don't see it mentioned in the PR or commit description.

**dashpole** on `sdk/metric/exemplar/storage.go` (line 62) — 2025-10-16T12:37:15Z

Added to the description

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:10:56Z

nit: use explicit parameter passing to improve clarity for older Go versions that the loop var is captured safely.

```suggestion
			go func(interation int) {
				ctx, ts, val, attrs := generateOfferInputs[N](t, iteration+1)
				r.Offer(ctx, ts, val, attrs)
				wg.Done()
			}(i)
```

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:17:30Z

It is possible, and likely, this will validate an empty slice. Running `Collect` concurrently and then running after done will ensure both races and exemplars are checked.

```suggestion
 
        // Also test concurrent Collect calls
        wg.Add(1)
        go func() {
            var dest []Exemplar
            r.Collect(&dest)
            wg.Done()
        }()
        
        wg.Wait()
        
        // Final collect to validate state
        var dest []Exemplar
        r.Collect(&dest)
        assert.NotEmpty(t, dest)
        for _, e := range dest {
            validateExemplar[N](t, e)
        }
```

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:18:27Z

This looks unused.

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 215) — 2025-11-06T21:19:32Z

```suggestion
		i = int(e.Value.Float64())
	default:
		t.Fatalf("unexpected value type: %v", e.Value.Type())
```

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 221) — 2025-11-06T21:22:35Z

```suggestion
	}
	if i == 0 {
		t.Fatal("empty exemplar")
	}
```

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` — 2025-11-06T21:24:33Z

magic number

```suggestion
		const goroutines = 2
		
		// Call Offer concurrently with another Offer, and with Collect.
		for i := range goroutines {
```

**MrAlias** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-11-06T21:27:17Z

What about just adding the concurrency test to `ReservoirTest`?

**MrAlias** on `sdk/metric/exemplar/reservoir_test.go` (line 208) — 2025-11-06T21:28:37Z

```suggestion
func validateExemplar[N int64 | float64](t *testing.T, e Exemplar) {
	t.Helper()
```

**dashpole** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-11-20T16:11:59Z

I can if you want to... I prefer having tests for the histogram reservoir in its own file.

**MrAlias** on `sdk/metric/exemplar/histogram_reservoir_test.go` (line 27) — 2025-12-11T17:06:00Z

Gotcah. Let's keep it separate.

## Timeline

- 2025-10-02T13:59:40Z · **head_ref_force_pushed** by dashpole
- 2025-10-02T14:00:03Z · **head_ref_force_pushed** by dashpole
- 2025-10-02T16:38:47Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7447
- 2025-10-02T18:03:34Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-specification/issues/4675
- 2025-10-03T13:20:44Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T13:27:37Z · **ready_for_review** by dashpole
- 2025-10-03T13:27:38Z · **review_requested** by dashpole
- 2025-10-03T13:27:38Z · **review_requested** by dashpole
- 2025-10-03T13:27:38Z · **review_requested** by dashpole
- 2025-10-03T13:27:38Z · **review_requested** by dashpole
- 2025-10-03T13:27:38Z · **review_requested** by dashpole
- 2025-10-04T03:36:32Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7453
- 2025-10-04T03:45:15Z · **head_ref_force_pushed** by dashpole
- 2025-10-04T03:47:24Z · **head_ref_force_pushed** by dashpole
- 2025-10-06T16:03:00Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7458
- 2025-10-07T14:40:19Z · **head_ref_force_pushed** by dashpole
- 2025-10-07T15:22:00Z · **referenced** by dashpole
- 2025-10-10T13:10:45Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-10-15T01:01:40Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T15:38:27Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T20:00:14Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T20:02:58Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T20:08:31Z · **review_requested** by dashpole
- 2025-10-15T20:08:33Z · **review_requested** by dashpole
- 2025-10-15T20:12:05Z · **head_ref_force_pushed** by dashpole
- 2025-10-16T16:23:04Z · **milestoned** by MrAlias → v1.39.0
- 2025-11-20T16:10:01Z · **head_ref_force_pushed** by dashpole
- 2025-12-04T18:10:27Z · **review_requested** by MrAlias
- 2025-12-04T18:10:37Z · **demilestoned** by MrAlias → v1.39.0
- 2025-12-04T18:10:37Z · **milestoned** by MrAlias → v1.40.0
- 2025-12-11T17:22:43Z · **head_ref_force_pushed** by dashpole
- 2025-12-15T14:59:34Z · **merged** by dashpole
- 2025-12-15T14:59:34Z · **closed** by dashpole
- 2025-12-15T14:59:42Z · **head_ref_deleted** by dashpole
- 2026-01-16T17:11:30Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796
- 2026-01-23T14:27:45Z · **referenced** by dashpole
- 2026-02-02T17:06:10Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7859
- 2026-02-02T17:46:36Z · **referenced** by MrAlias
- 2026-03-03T00:46:39Z · **cross-referenced** by ddl-rliu ← https://github.com/flyteorg/flyte/pull/6959
- 2026-03-03T01:00:14Z · **cross-referenced** by ddl-rliu ← https://github.com/flyteorg/flyte/pull/6960

