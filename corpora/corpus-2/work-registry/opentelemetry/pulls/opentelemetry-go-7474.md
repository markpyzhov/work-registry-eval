**Source ID**: [SRC-PR-06]

# Pull Request: Use sync.Map and atomics for fixed bucket histograms (open-telemetry/opentelemetry-go#7474)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/pull/7474  
**Author**: dashpole  
**Created**: 2025-10-08T14:31:21Z · **Updated**: 2025-12-11T16:56:31Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: merged (2025-12-11T16:56:04Z)  
**Branch**: `optimize_syncmap_histogram` → `main`  
**Changes**: +560 / -201 across 7 files  
**Labels**: —  
**Milestone**: v1.40.0

---

## Description

Implement a lockless histogram using atomics, and use a sync.Map for attribute access.  This improves performance by ~2x.

The design is very similar to https://github.com/open-telemetry/opentelemetry-go/pull/7427, but with one additional change to make the histogram data point itself atomic:

* For cumulative histograms, which do not use a hot/cold limitedSyncMap, we use a hot/cold data point.  This way, we maintain the keys in the sync map, but still ensure that collection gets a consistent view of measure() calls.

Parallel benchmarks:
```
                                                                       │  main.txt   │              hist.txt              │
                                                                       │   sec/op    │   sec/op     vs base               │
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/10-24     274.5n ± 2%   125.2n ± 5%  -54.42% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/10-24   274.1n ± 2%   132.5n ± 2%  -51.65% (p=0.002 n=6)
geomean                                                                  274.3n        128.8n       -53.05%
```

zero memory allocations before and after this change for Measure().  Omitted for brevity

Benchmarks for collect:
```
                                                    │   main.txt    │               hist.txt               │
                                                    │    sec/op     │    sec/op     vs base                │
Collect/NoView/Int64Histogram/1/Attributes/0-24       1.799µ ±  60%    1.702µ ± 6%         ~ (p=1.000 n=6)
Collect/NoView/Int64Histogram/1/Attributes/1-24       973.7n ±  28%   1720.0n ± 5%   +76.65% (p=0.002 n=6)
Collect/NoView/Int64Histogram/1/Attributes/10-24      881.0n ±  17%   1710.0n ± 5%   +94.09% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/0-24      996.1n ±  14%   1781.5n ± 4%   +78.85% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/1-24      1.029µ ±  67%    1.733µ ± 3%   +68.42% (p=0.009 n=6)
Collect/NoView/Int64Histogram/10/Attributes/10-24     1.533µ ±  18%    1.708µ ± 4%         ~ (p=0.240 n=6)
Collect/NoView/Float64Histogram/1/Attributes/0-24     1.222µ ± 120%    1.733µ ± 4%         ~ (p=0.065 n=6)
Collect/NoView/Float64Histogram/1/Attributes/1-24     893.3n ±   8%   1733.0n ± 4%   +94.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/10-24    860.7n ±   2%   1732.0n ± 5%  +101.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/0-24    852.5n ±   4%   1758.0n ± 3%  +106.22% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/1-24    853.8n ±   3%   1725.0n ± 3%  +102.04% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/10-24   843.4n ±   2%   1755.0n ± 4%  +108.10% (p=0.002 n=6)
geomean                                               1.028µ           1.732µ        +68.46%

                                                    │  main.txt  │               hist.txt               │
                                                    │    B/op    │     B/op      vs base                │
Collect/NoView/Int64Histogram/1/Attributes/0-24       336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Int64Histogram/1/Attributes/1-24       336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Int64Histogram/1/Attributes/10-24      336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/0-24      336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/1-24      336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/10-24     336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/0-24     336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/1-24     336.0 ± 0%    2130.5 ± 0%  +534.08% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/10-24    336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/0-24    336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/1-24    336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/10-24   336.0 ± 0%    2131.0 ± 0%  +534.23% (p=0.002 n=6)
geomean                                               336.0        2.081Ki       +534.21%

                                                    │  main.txt  │             hist.txt              │
                                                    │ allocs/op  │ allocs/op   vs base               │
Collect/NoView/Int64Histogram/1/Attributes/0-24       5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Int64Histogram/1/Attributes/1-24       5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Int64Histogram/1/Attributes/10-24      5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/0-24      5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/1-24      5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Int64Histogram/10/Attributes/10-24     5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/0-24     5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/1-24     5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/1/Attributes/10-24    5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/0-24    5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/1-24    5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
Collect/NoView/Float64Histogram/10/Attributes/10-24   5.000 ± 0%   6.000 ± 0%  +20.00% (p=0.002 n=6)
geomean                                               5.000        6.000       +20.00%
```

Collect does get substantially worse, but Measure is expected to be called significantly more often than collect.

## Discussion (7)

**codecov[bot]** — 2025-10-08T14:34:56Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
:x: Patch coverage is `94.85714%` with `9 lines` in your changes missing coverage. Please review.
:white_check_mark: Project coverage is 86.2%. Comparing base ([`b4578c8`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/b4578c886a58a155c5f10b19d7ad6ab51825655e?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)) to head ([`d6c4ded`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/d6c4ded4e9e7bef32973578792909539a33ee4ef?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)).
:warning: Report is 1 commits behind head on main.

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Patch % | Lines |
|---|---|---|
| [sdk/metric/internal/aggregate/atomic.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fatomic.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvYXRvbWljLmdv) | 83.6% | [9 Missing :warning: ](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) |

<details><summary>Additional details and impacted files</summary>



[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474/graphs/tree.svg?width=650&height=150&src=pr&token=8efTmh4kvf&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@          Coverage Diff           @@
##            main   #7474    +/-   ##
======================================
  Coverage   86.1%   86.2%            
======================================
  Files        298     298            
  Lines      21726   21829   +103     
======================================
+ Hits       18722   18818    +96     
- Misses      2627    2635     +8     
+ Partials     377     376     -1     
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [sdk/metric/internal/aggregate/aggregate.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Faggregate.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvYWdncmVnYXRlLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/histogram.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fhistogram.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvaGlzdG9ncmFtLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/sum.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fsum.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvc3VtLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/atomic.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fatomic.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvYXRvbWljLmdv) | `90.0% <83.6%> (-2.8%)` | :arrow_down: |

... and [2 files with indirect coverage changes](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7474/indirect-changes?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)
</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**dashpole** — 2025-11-07T15:19:44Z

> Great work, great to see amazing results! Do you mid benchmarking with allocs too?

Yeah, zero allocs on the Measure() path before and after, so I didn't post it.

---

**MrAlias** — 2025-12-04T18:09:42Z

 @dmathieu @flc1125: would either of you have time to review this? @dashpole is able to answer questions if that helps.

---

**dashpole** — 2025-12-09T16:50:12Z

Not sure why coverage is failing

---

**MrAlias** — 2025-12-09T16:57:34Z

> Not sure why coverage is failing

I think the changes are just exposing an area where we have had coverage overlap. I think this has more to do with how we merge coverage instead of the changes here.

---

**MrAlias** — 2025-12-09T17:10:55Z

Likely worth looking into using [Go 1.20 coverage directory feature](https://go.dev/doc/go1.20#cover) to replace our current approach.

---

**dashpole** — 2025-12-11T16:49:43Z

Seems to have resolved itself.  Now just links are failing (503s from github due to outage).

## Reviews (31)

**MrAlias** — COMMENTED — 2025-10-08T22:17:45Z

**dashpole** — COMMENTED — 2025-10-09T12:40:04Z

**dashpole** — COMMENTED — 2025-10-09T18:29:01Z

**MrAlias** — COMMENTED — 2025-10-10T15:21:23Z

**MrAlias** — COMMENTED — 2025-10-10T16:08:31Z

**dashpole** — COMMENTED — 2025-10-10T18:14:37Z

**dashpole** — COMMENTED — 2025-10-10T18:18:00Z

**dashpole** — COMMENTED — 2025-10-10T18:20:03Z

**dashpole** — COMMENTED — 2025-10-10T19:38:26Z

**dashpole** — COMMENTED — 2025-10-10T19:39:24Z

**dashpole** — COMMENTED — 2025-10-10T19:41:04Z

**dashpole** — COMMENTED — 2025-10-10T19:41:26Z

**dashpole** — COMMENTED — 2025-10-10T20:10:16Z

**dashpole** — COMMENTED — 2025-10-10T20:20:43Z

**dashpole** — COMMENTED — 2025-10-10T20:20:50Z

**MrAlias** — COMMENTED — 2025-10-12T14:42:30Z

**dashpole** — COMMENTED — 2025-10-15T00:52:35Z

**bwplotka** — COMMENTED — 2025-11-07T08:53:56Z

Trying to help a bit with review of this.

Generally looks good, just small things, but also I'm not a maintainer and a bit new to the codebase (I maintain Prometheus client_golang SDK though).

Great work, great to see amazing results! Do you mid benchmarking with allocs too?



**dashpole** — COMMENTED — 2025-11-07T15:22:59Z

**dashpole** — COMMENTED — 2025-11-07T15:23:19Z

**dashpole** — COMMENTED — 2025-11-07T17:16:04Z

**dashpole** — COMMENTED — 2025-11-07T17:21:55Z

**dashpole** — COMMENTED — 2025-11-07T17:30:19Z

**dashpole** — COMMENTED — 2025-11-07T17:30:47Z

**dashpole** — COMMENTED — 2025-11-07T17:31:44Z

**dashpole** — COMMENTED — 2025-11-10T16:17:44Z

**dashpole** — COMMENTED — 2025-11-10T16:24:41Z

**dashpole** — COMMENTED — 2025-11-12T14:59:04Z

**MrAlias** — APPROVED — 2025-12-04T17:44:24Z

**dmathieu** — APPROVED — 2025-12-09T14:41:46Z

**dashpole** — COMMENTED — 2025-12-09T16:07:17Z

## Review Comments (44)

**MrAlias** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-08T22:16:25Z

There are data-races here because these are all stored as 3 separate fields.

What about something like this instead?

```go
// extrema holds the minimum and maximum of a set of values.
type extrema[N int64 | float64] struct {
	min, max N
	set      bool
}

func newExtrema[N int64 | float64](minimum, maximum N) extrema[N] {
	return extrema[N]{min: minimum, max: maximum, set: true}
}

// update updates the extrema with the provided value.
//
// If the current extrema already contains a minimum less than or equal to val,
// no update to minimum is made.
//
// If the current extrema already contains a maximum greater than or equal to
// val, no update to maximum is made.
func (e extrema[N]) update(val N) extrema[N] {
	if !e.set {
		e.min = val
		e.max = val
		e.set = true
		return e
	}

	e.min = min(e.min, val)
	e.max = max(e.max, val)
	return e
}

type atomicExtrema[N int64 | float64] struct {
	p atomic.Pointer[extrema[N]]
}

// eval updates the extrema with the provided value.
//
// If the current extrema already contains a minimum less than or equal to val,
// no update to minimum is made.
//
// If the current extrema already contains a maximum greater than or equal to
// val, no update to maximum is made.
func (e *atomicExtrema[N]) eval(val N) {
	e.store(val, val)
}

// store updates the extrema with the provided minimum and maximum values.
//
// If the current extrema already contains a minimum less than or equal to
// minimum, no update to minimum is made.
//
// If the current extrema already contains a maximum greater than or equal to
// maximum, no update to maximum is made.
func (e *atomicExtrema[N]) store(minimum, maximum N) {
	orig := e.p.Load()
	for orig == nil || minimum < orig.min || maximum > orig.max {
		var n extrema[N]
		if orig == nil {
			n = newExtrema(minimum, maximum)
		} else {
			n = orig.update(minimum).update(maximum)
			if n == *orig {
				// No change, not an extrema.
				return
			}
		}

		if e.p.CompareAndSwap(orig, &n) {
			return
		}
		orig = e.p.Load()
	}
}

// load returns the current extrema values and true if extrema have been set.
// Otherwise, ok will be false.
func (e *atomicExtrema[N]) load() (min, max N, ok bool) {
	v := e.p.Load()
	if v == nil {
		return min, max, false
	}
	return v.min, v.max, true
}
```

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-09T12:40:04Z

I don't think there are actually data races here.  The only time both min and max can be set is on the first write (since otherwise it can't be both less than the min and greater than the max), but for the first write, we don't flip isSet to true until after both have been written.  So as long as readers respect isSet, they won't get inconsistent min and max values.  In all other cases, only min OR max is written, which is atomic.

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-09T18:29:01Z

There is actually a data race if a value of 0 is observed.

**MrAlias** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T15:21:23Z

My testing showed that using an `atomic.Pointer[...]` will require an allocation for each update.

Instead, I think this can be resolved with a lock that is only used on the first set:

```go
import (
	"math"
	"sync"
	"sync/atomic"
)

type atomicN[N int64 | float64] struct {
	val atomic.Uint64
}

func (a *atomicN[N]) Load() (value N) {
	v := a.val.Load()
	switch any(value).(type) {
	case int64:
		value = N(v)
	case float64:
		value = N(math.Float64frombits(v))
	default:
		panic("unsupported type")
	}
	return value
}

func (a *atomicN[N]) Store(v N) {
	var val uint64
	switch any(v).(type) {
	case int64:
		val = uint64(v)
	case float64:
		val = math.Float64bits(float64(v))
	default:
		panic("unsupported type")
	}
	a.val.Store(val)
}

func (a *atomicN[N]) CompareAndSwap(old, new N) bool {
	var o, n uint64
	switch any(old).(type) {
	case int64:
		o, n = uint64(old), uint64(new)
	case float64:
		o, n = math.Float64bits(float64(old)), math.Float64bits(float64(new))
	default:
		panic("unsupported type")
	}
	return a.val.CompareAndSwap(o, n)
}

type atomicMinMax[N int64 | float64] struct {
	mu       sync.Mutex
	set      atomic.Bool
	min, max atomicN[N]
}

func (s *atomicMinMax[N]) init(val N) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if !s.set.Load() {
		defer s.set.Store(true)
		s.min.Store(val)
		s.max.Store(val)
	}
}

func (s *atomicMinMax[N]) Update(val N) {
	if !s.set.Load() {
		s.init(val)
		return
	}

	old := s.min.Load()
	for old > val {
		if s.min.CompareAndSwap(old, val) {
			break
		}
		old = s.min.Load()
	}

	old = s.max.Load()
	for old < val {
		if s.max.CompareAndSwap(old, val) {
			break
		}
		old = s.max.Load()
	}
}
```

**MrAlias** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T15:43:13Z

Whatever solution we do come up with, tests and benchmarks need to be added for it.

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` (line 18) — 2025-10-10T15:44:05Z

Why change the name?

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T15:52:01Z

This is coupling the bin selection too tightly to the binning action. It only allows a single approach to bin selection.

This API should remain where the caller can specify the bin that needs to be incremented instead of having to pass bounds and a value in those bounds. Otherwise, you get things like what is added to the testing below where you need to artificially create bounds and values to get the right index, instead of just passing the index you want.

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T15:55:58Z

Why allocate a new slice here if `hDPts[i].BucketCounts` already has the memory allocated to hold this?

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` (line 113) — 2025-10-10T16:05:36Z

Please preserver these comments.

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T16:08:06Z

This is an odd place for this declaration. Likely the top or bottom of the file would be a better location.

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 18) — 2025-10-10T18:14:37Z

I wanted to align with the names of all other aggregations (sumPoint, lastValuePoint, expoHistPoint).  This also contains more than bucket counts.

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T18:18:00Z

As an alternative, I considered deleting the bin function and test entirely.  It is now a single line, so seems a bit overkill to have a function and unit test for...  AFAIK there are no plans to introduce other binning approaches, right?  Do you want me to rename the function to something else?  E.g. incrementBucket

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T18:20:03Z

I'll move it to the top.  It is only used by the cumulative `measure` and `collect` functions, which is why I had placed it here.

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T19:38:26Z

mostly adopted your solution above.

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` — 2025-10-10T19:39:24Z

I can't use the name "min", so i've used minimum and maximum.  I also needed to return a bool from atomicMinMax.init since it is possible that the min and max are not updated by init

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 113) — 2025-10-10T19:41:04Z

Done in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/62fb19ff404cefa4830abd5521b5c8546336cfe1

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T19:41:26Z

done in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/ebe6c6504a9d6b41b5356225843d3c115f13a03f

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 104) — 2025-10-10T20:10:16Z

Benchmarks in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/0cb7b113287031a78f72c8bc02e32ff8684a7a90

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T20:20:43Z

Done in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/6a1b840edcc948a30fb3b32d57c361d443f4297f

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-10T20:20:50Z

Done in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/6a1b840edcc948a30fb3b32d57c361d443f4297f

**MrAlias** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-12T14:42:30Z

I would be in favor of flattening and removing the function entirely :+1: 

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` — 2025-10-15T00:52:35Z

Removed bin and sum (both 1-line functions) in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/45effea2efa88e4afd62b0942cbae3677a6f2e4b

**bwplotka** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T05:52:15Z

I'd curious how much performance we lose with just using generics for such a low level hot path here. Being in ~100n range means we could have some generic s overhead vs having a two atomic variables with some manual switch typing we do anyway here. 🤔 

See: https://planetscale.com/blog/generics-can-make-your-go-code-slower (old though)

**bwplotka** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T05:53:31Z

You added a benchmark but I didn't see any results posted on PR or anywhere. 

Is this useful benchmark then? Or there is some policy to add benchmarks for all low-level things just in case? (reminds me of YAGNI)

**bwplotka** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T07:59:20Z

Ok I see tha rationales https://github.com/open-telemetry/opentelemetry-go/pull/7474#discussion_r2420920128

Tests are great.

Just 2c, but adding benchmarks without ever planning to use it (realistically) might is same as adding a dead code. They could be added when we want to execute and measure. Is it used anywhere now?


**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T08:01:04Z

First would nice to understand that mem footprint. You benchmark results on a PR don't report allocs. Can we add those?

<img width="1353" height="575" alt="Image" src="https://github.com/user-attachments/assets/897fee3c-eaae-4281-87b5-7bd49dcff5b3" />

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:37:45Z

```suggestion
	// TODO (#3047): Making copies for counts incurs a large
```
Only for counts?

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T08:39:07Z

Also not sure if this comment is useful. You could always invest more time to improve memory. Here is not that obvious way - you do all you can to only allocate if you need to resize. Maybe it's good enough?

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 60) — 2025-11-07T08:39:56Z

What it is complaining for? What control flag means?

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:45:06Z

```suggestion
			//   counts = (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, +∞)
```

Perhaps? To match the code

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 255) — 2025-11-07T08:46:38Z

How often (if ever) histograms change bucketing? Never during runtime?

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` — 2025-11-07T08:46:47Z

```suggestion
			//   count = (-∞, 0], (0, 5.0], (5.0, 10.0], (10.0, +∞)
```

**bwplotka** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-07T08:51:55Z

Do you have to do it inside lock? s.bounds never change, right?

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 60) — 2025-11-07T15:22:59Z

revive doesn't like boolean arguments to functions.  It considers them "control flags". See https://github.com/mgechev/revive/blob/master/RULES_DESCRIPTIONS.md#flag-parameter.  I'm not sure I agree that they should always be avoided, as it would cause a lot of code duplication...

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 255) — 2025-11-07T15:23:19Z

never during runtime.

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T17:16:04Z

Interesting.  Based on that, generics themselves for concrete types shouldn't have any additional overhead.  The type switching presumably will, though.  I've found that once you are "inside" a generic type, it is really hard to get back to non-generic types.  I will probably leave this refactor as a follow-up, but it is a good point.

**dashpole** on `sdk/metric/internal/aggregate/atomic.go` (line 61) — 2025-11-07T17:21:55Z

Filed an issue: https://github.com/open-telemetry/opentelemetry-go/issues/7589

**dashpole** on `sdk/metric/internal/aggregate/atomic_test.go` (line 55) — 2025-11-07T17:30:19Z

We run benchmarks as part of CI, and also do a diff on push: https://github.com/open-telemetry/opentelemetry-go/blob/main/.github/workflows/benchmark.yml.  Example: https://github.com/open-telemetry/opentelemetry-go/actions/runs/18314631364 from my PR for improving sum measure performance.

So if someone did make a change, we would at least be able to tell if it made performance significantly worse afterwards...

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T17:30:47Z

There are no allocs before or after.  Added to the PR description.

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-07T17:31:44Z

There are allocs for Collect.  I can try to publish the collect benchmarks as well, but I suspect those get worse.

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-10T16:17:44Z

There is no lock :).  But you are right hat we can do this befor eh.hcwg.start()

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 310) — 2025-11-10T16:24:40Z

Done in https://github.com/open-telemetry/opentelemetry-go/pull/7474/commits/219e89e4c701e37a4857cf3e91a7a0acd9945a79

**dashpole** on `sdk/metric/internal/aggregate/histogram.go` (line 44) — 2025-11-12T14:59:04Z

Added to the description

**dashpole** on `CHANGELOG.md` — 2025-12-09T16:07:17Z

```suggestion
- Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)
```

## Timeline

- 2025-10-08T16:15:19Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T16:52:19Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T17:04:16Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T18:22:08Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T18:23:31Z · **ready_for_review** by dashpole
- 2025-10-08T18:23:31Z · **review_requested** by dashpole
- 2025-10-08T18:23:31Z · **review_requested** by dashpole
- 2025-10-08T18:23:31Z · **review_requested** by dashpole
- 2025-10-08T18:23:32Z · **review_requested** by dashpole
- 2025-10-08T18:23:32Z · **review_requested** by dashpole
- 2025-10-08T18:24:59Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T18:37:34Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T18:55:57Z · **head_ref_force_pushed** by dashpole
- 2025-10-08T19:23:19Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7478
- 2025-10-10T13:10:45Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-10-10T19:38:13Z · **head_ref_force_pushed** by dashpole
- 2025-10-11T02:01:19Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T00:52:11Z · **head_ref_force_pushed** by dashpole
- 2025-10-15T20:14:54Z · **head_ref_force_pushed** by dashpole
- 2025-10-16T16:23:50Z · **milestoned** by MrAlias → v1.39.0
- 2025-10-24T19:58:30Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7535
- 2025-11-07T17:21:32Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/issues/7589
- 2025-11-10T16:24:27Z · **head_ref_force_pushed** by dashpole
- 2025-12-04T18:09:56Z · **demilestoned** by MrAlias → v1.39.0
- 2025-12-04T18:09:56Z · **milestoned** by MrAlias → v1.40.0
- 2025-12-11T16:56:04Z · **merged** by dashpole
- 2025-12-11T16:56:04Z · **closed** by dashpole
- 2025-12-11T16:56:08Z · **head_ref_deleted** by dashpole
- 2025-12-16T08:23:14Z · **referenced** by dmathieu
- 2026-01-16T17:11:30Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796
- 2026-02-02T17:06:10Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7859
- 2026-02-02T17:46:35Z · **referenced** by MrAlias
- 2026-03-03T00:46:39Z · **cross-referenced** by ddl-rliu ← https://github.com/flyteorg/flyte/pull/6959
- 2026-03-03T01:00:14Z · **cross-referenced** by ddl-rliu ← https://github.com/flyteorg/flyte/pull/6960
- 2026-03-23T17:24:11Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/8077
- 2026-06-04T22:27:21Z · **referenced** by sudowork
- 2026-06-04T22:57:58Z · **cross-referenced** by sudowork ← https://github.com/open-telemetry/opentelemetry-go/issues/8427

