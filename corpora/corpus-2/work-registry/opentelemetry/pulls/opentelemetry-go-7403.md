**Source ID**: [SRC-PR-03]

# Pull Request: sdk/log: Fix AddAttributes, SetAttributes, SetBody on Record to not mutate input (open-telemetry/opentelemetry-go#7403)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/pull/7403  
**Author**: pellared  
**Created**: 2025-09-23T17:31:54Z · **Updated**: 2025-10-16T19:07:47Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: merged (2025-10-16T19:07:08Z)  
**Branch**: `fix-7364` → `main`  
**Changes**: +722 / -74 across 5 files  
**Labels**: pkg:SDK, area:logs  
**Milestone**: v1.39.0

---

## Description

Fixes #7364

The allocations happen only when necessary.
This is when deduplication happens or data is truncated because of the limits.

```
goos: linux
goarch: amd64
pkg: go.opentelemetry.io/otel/sdk/log
cpu: 13th Gen Intel(R) Core(TM) i7-13800H
                                              │    old.txt    │                new.txt                 │
                                              │    sec/op     │    sec/op      vs base                 │
AddAttributes/Single/NoLimits-20                 57.91n ± 19%    29.12n ±  5%   -49.71% (p=0.000 n=10)
AddAttributes/Single/AllowDuplicates-20          24.21n ±  2%    24.46n ± 17%    +1.05% (p=0.011 n=10)
AddAttributes/Unique/NoLimits-20                 174.6n ±  8%    184.2n ±  7%    +5.47% (p=0.027 n=10)
AddAttributes/Unique/AllowDuplicates-20          69.79n ± 22%    67.83n ±  9%    -2.81% (p=0.019 n=10)
AddAttributes/Deduplication/Enabled-20           144.5n ±  4%    165.8n ±  4%   +14.71% (p=0.000 n=10)
AddAttributes/NestedDeduplication/Enabled-20     439.2n ±  2%    792.4n ± 11%   +80.41% (p=0.000 n=10)
AddAttributes/NestedDeduplication/Disabled-20   162.60n ±  1%    86.84n ±  5%   -46.59% (p=0.000 n=10)
AddAttributes/Deduplication/Disabled-20          68.15n ±  8%    67.59n ±  8%         ~ (p=0.190 n=10)
AddAttributes/CountLimit/Hit-20                  629.1n ±  4%    621.0n ±  7%         ~ (p=0.325 n=10)
AddAttributes/CountLimit/NotHit-20               914.6n ±  7%    944.2n ± 13%         ~ (p=0.393 n=10)
AddAttributes/ValueLimit/Hit-20                  133.5n ±  2%    162.1n ±  2%   +21.43% (p=0.000 n=10)
AddAttributes/ValueLimit/NotHit-20               115.8n ±  9%    131.2n ±  8%   +13.26% (p=0.000 n=10)
SetAttributes/Single/NoLimits-20                 59.38n ±  2%    28.89n ± 22%   -51.36% (p=0.000 n=10)
SetAttributes/Single/AllowDuplicates-20          24.19n ±  1%    24.30n ±  2%         ~ (p=0.867 n=10)
SetAttributes/Unique/NoLimits-20                 179.8n ±  2%    200.7n ±  6%   +11.66% (p=0.000 n=10)
SetAttributes/Unique/AllowDuplicates-20          72.65n ±  6%    71.91n ±  6%         ~ (p=0.218 n=10)
SetAttributes/Deduplication/Enabled-20           143.9n ±  6%    188.5n ± 12%   +30.96% (p=0.000 n=10)
SetAttributes/Deduplication/Disabled-20          77.68n ± 12%    69.20n ±  8%   -10.92% (p=0.008 n=10)
SetAttributes/NestedDeduplication/Enabled-20     443.7n ± 11%    770.8n ±  7%   +73.75% (p=0.000 n=10)
SetAttributes/NestedDeduplication/Disabled-20   172.60n ±  4%    91.73n ± 11%   -46.85% (p=0.000 n=10)
SetAttributes/CountLimit/Hit-20                  629.1n ±  2%    631.3n ±  7%         ~ (p=0.971 n=10)
SetAttributes/CountLimit/NotHit-20               909.2n ±  8%    866.4n ±  7%         ~ (p=0.143 n=10)
SetAttributes/ValueLimit/Hit-20                  135.5n ±  2%    150.2n ±  5%   +10.85% (p=0.000 n=10)
SetAttributes/ValueLimit/NotHit-20               121.7n ±  7%    137.2n ±  6%   +12.65% (p=0.001 n=10)
SetAttributes/Overwrite/Existing-20              176.0n ±  5%    184.1n ±  2%    +4.60% (p=0.005 n=10)
SetBody/Simple/NoLimits-20                       13.54n ±  1%    13.34n ±  2%    -1.48% (p=0.027 n=10)
SetBody/Simple/WithLimits-20                     13.46n ± 11%    13.91n ±  9%         ~ (p=0.541 n=10)
SetBody/UniqueMap/NoLimits-20                    216.2n ±  8%    183.8n ±  3%   -14.94% (p=0.000 n=10)
SetBody/UniqueMap/AllowDuplicates-20             12.89n ±  1%    12.75n ±  1%    -1.05% (p=0.001 n=10)
SetBody/Deduplication/Enabled-20                 113.5n ±  2%    164.4n ±  4%   +44.85% (p=0.000 n=10)
SetBody/Deduplication/Disabled-20                12.93n ± 41%    12.74n ±  1%    -1.51% (p=0.000 n=10)
SetBody/NestedDeduplication/Enabled-20           206.4n ±  2%    493.4n ±  2%  +139.05% (p=0.000 n=10)
SetBody/NestedDeduplication/Disabled-20          12.93n ±  1%    12.98n ± 11%         ~ (p=0.515 n=10)
SetBody/ValueLimit/Hit-20                        86.22n ±  1%   110.25n ±  3%   +27.87% (p=0.000 n=10)
SetBody/ValueLimit/NoHit-20                      85.52n ±  8%   104.25n ±  1%   +21.91% (p=0.000 n=10)
geomean                                          104.2n          107.1n          +2.84%

                                              │   old.txt    │            new.txt             │
                                              │     B/op     │    B/op     vs base            │
AddAttributes/Single/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Single/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Unique/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Unique/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Deduplication/Enabled-20            0.0 ± 0%     128.0 ± 0%  ? (p=0.000 n=10)
AddAttributes/NestedDeduplication/Enabled-20      0.0 ± 0%     312.0 ± 0%  ? (p=0.000 n=10)
AddAttributes/NestedDeduplication/Disabled-20   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Deduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/CountLimit/Hit-20                 208.0 ± 0%     208.0 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/CountLimit/NotHit-20              640.0 ± 0%     640.0 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/ValueLimit/Hit-20                 0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/ValueLimit/NotHit-20              0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Single/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Single/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Unique/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Unique/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Deduplication/Enabled-20            0.0 ± 0%     128.0 ± 0%  ? (p=0.000 n=10)
SetAttributes/Deduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/NestedDeduplication/Enabled-20      0.0 ± 0%     312.0 ± 0%  ? (p=0.000 n=10)
SetAttributes/NestedDeduplication/Disabled-20   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/CountLimit/Hit-20                 208.0 ± 0%     208.0 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/CountLimit/NotHit-20              640.0 ± 0%     640.0 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/ValueLimit/Hit-20                 0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/ValueLimit/NotHit-20              0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Overwrite/Existing-20             0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Simple/NoLimits-20                      0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Simple/WithLimits-20                    0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/UniqueMap/NoLimits-20                   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/UniqueMap/AllowDuplicates-20            0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Deduplication/Enabled-20                  0.0 ± 0%     128.0 ± 0%  ? (p=0.000 n=10)
SetBody/Deduplication/Disabled-20               0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/NestedDeduplication/Enabled-20            0.0 ± 0%     280.0 ± 0%  ? (p=0.000 n=10)
SetBody/NestedDeduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/ValueLimit/Hit-20                       0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/ValueLimit/NoHit-20                     0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
geomean                                                    ²               ?                ²
¹ all samples are equal
² summaries must be >0 to compute geomean

                                              │   old.txt    │            new.txt             │
                                              │  allocs/op   │ allocs/op   vs base            │
AddAttributes/Single/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Single/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Unique/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Unique/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Deduplication/Enabled-20          0.000 ± 0%     1.000 ± 0%  ? (p=0.000 n=10)
AddAttributes/NestedDeduplication/Enabled-20    0.000 ± 0%     5.000 ± 0%  ? (p=0.000 n=10)
AddAttributes/NestedDeduplication/Disabled-20   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/Deduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/CountLimit/Hit-20                 1.000 ± 0%     1.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/CountLimit/NotHit-20              1.000 ± 0%     1.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/ValueLimit/Hit-20                 0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
AddAttributes/ValueLimit/NotHit-20              0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Single/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Single/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Unique/NoLimits-20                0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Unique/AllowDuplicates-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Deduplication/Enabled-20          0.000 ± 0%     1.000 ± 0%  ? (p=0.000 n=10)
SetAttributes/Deduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/NestedDeduplication/Enabled-20    0.000 ± 0%     5.000 ± 0%  ? (p=0.000 n=10)
SetAttributes/NestedDeduplication/Disabled-20   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/CountLimit/Hit-20                 1.000 ± 0%     1.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/CountLimit/NotHit-20              1.000 ± 0%     1.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/ValueLimit/Hit-20                 0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/ValueLimit/NotHit-20              0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetAttributes/Overwrite/Existing-20             0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Simple/NoLimits-20                      0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Simple/WithLimits-20                    0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/UniqueMap/NoLimits-20                   0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/UniqueMap/AllowDuplicates-20            0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/Deduplication/Enabled-20                0.000 ± 0%     1.000 ± 0%  ? (p=0.000 n=10)
SetBody/Deduplication/Disabled-20               0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/NestedDeduplication/Enabled-20          0.000 ± 0%     4.000 ± 0%  ? (p=0.000 n=10)
SetBody/NestedDeduplication/Disabled-20         0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/ValueLimit/Hit-20                       0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
SetBody/ValueLimit/NoHit-20                     0.000 ± 0%     0.000 ± 0%  ~ (p=1.000 n=10) ¹
geomean                                                    ²               ?                ²
¹ all samples are equal
² summaries must be >0 to compute geomean
```

## Discussion (7)

**codecov[bot]** — 2025-09-23T17:38:27Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
:white_check_mark: All modified and coverable lines are covered by tests.
:white_check_mark: Project coverage is 86.3%. Comparing base ([`f346dec`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/f346decaf65d275320e1ab4aa25715a2f0595311?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)) to head ([`4e5e8a5`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/4e5e8a5436ac37b03b50cbd85d585b5bf5780a3b?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)).
:warning: Report is 1 commits behind head on main.

<details><summary>Additional details and impacted files</summary>



[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403/graphs/tree.svg?width=650&height=150&src=pr&token=8efTmh4kvf&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@          Coverage Diff           @@
##            main   #7403    +/-   ##
======================================
  Coverage   86.2%   86.3%            
======================================
  Files        294     294            
  Lines      25844   25987   +143     
======================================
+ Hits       22286   22428   +142     
- Misses      3185    3186     +1     
  Partials     373     373            
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [sdk/log/record.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403?src=pr&el=tree&filepath=sdk%2Flog%2Frecord.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL2xvZy9yZWNvcmQuZ28=) | `100.0% <100.0%> (ø)` | |

... and [2 files with indirect coverage changes](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7403/indirect-changes?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)
</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**pellared** — 2025-09-23T19:58:37Z

CC @varkey98

---

**pellared** — 2025-09-25T13:32:40Z

Changing to draft as I think it is not fully fixed (sic!). I need to spend more time on it at least to double check.

---

**pellared** — 2025-09-25T18:29:23Z

> Changing to draft as I think it is not fully fixed (sic!). I need to spend more time on it at least to double check.

Fixed https://github.com/open-telemetry/opentelemetry-go/pull/7403/commits/27bdafeaa3d586cba933fbe6edb0be285a88ccbd

---

**pellared** — 2025-09-25T20:00:58Z

I have asked Claude Sonnet 4 to generate some fuzz tests. I have not checked them in detail, but they look good enough at quick glance. I have run all of them for 10 minutes to have more confidence on the fix.

```go
package log

import (
	"testing"
	"unsafe"

	"go.opentelemetry.io/otel/log"
)

// FuzzRecordAddAttributesMutation fuzzes AddAttributes to ensure no input mutation occurs.
func FuzzRecordAddAttributesMutation(f *testing.F) {
	// Seed with some interesting cases
	f.Add(
		[]byte("key1"),
		[]byte("value1"),
		[]byte("key2"),
		[]byte("value2"),
		[]byte("key3"),
		[]byte("value3"),
		int8(2),
		int8(10),
		false,
	)
	f.Add(
		[]byte("duplicate"),
		[]byte("first"),
		[]byte("duplicate"),
		[]byte("second"),
		[]byte("dup3"),
		[]byte("third"),
		int8(1),
		int8(5),
		false,
	)
	f.Add(
		[]byte("k"),
		[]byte("very long value that exceeds limit"),
		[]byte("k2"),
		[]byte("short"),
		[]byte("k3"),
		[]byte("medium"),
		int8(1),
		int8(3),
		true,
	)
	f.Add(
		[]byte(""),
		[]byte(""),
		[]byte("key"),
		[]byte("value"),
		[]byte("key2"),
		[]byte("value2"),
		int8(0),
		int8(0),
		false,
	)

	f.Fuzz(
		func(t *testing.T, key1, value1, key2, value2, key3, value3 []byte, countLimit, valueLimit int8, allowDupKeys bool) {
			// Convert to valid strings
			k1, v1 := string(key1), string(value1)
			k2, v2 := string(key2), string(value2)
			k3, v3 := string(key3), string(value3)

			// Create test attributes with more than 5 attributes
			attrs := []log.KeyValue{
				log.String(k1, v1),
				log.String(k2, v2),
				log.String(k3, v3),
				log.String(k1+"_dup", v1+"_duplicate"), // Potential duplicate pattern
				log.String("static_key1", "static_value1"),
				log.String("static_key2", "static_value2"),
				log.String(k2+"_variant", v2+"_modified"),
				log.String("final_key", "final_value"),
			}

			// Create deep copies for comparison
			originalAttrs := make([]log.KeyValue, len(attrs))
			copy(originalAttrs, attrs)

			// Capture original slice header info
			originalLen := len(attrs)
			originalCap := cap(attrs)
			originalPtr := unsafe.Pointer(unsafe.SliceData(attrs))

			r := &Record{
				attributeCountLimit:       int(countLimit),
				attributeValueLengthLimit: int(valueLimit),
				allowDupKeys:              allowDupKeys,
			}

			// Call AddAttributes
			r.AddAttributes(attrs...)

			// Verify no mutation occurred
			if len(attrs) != originalLen {
				t.Errorf("AddAttributes mutated slice length: expected %d, got %d", originalLen, len(attrs))
			}

			if cap(attrs) != originalCap {
				t.Errorf("AddAttributes mutated slice capacity: expected %d, got %d", originalCap, cap(attrs))
			}

			if unsafe.Pointer(unsafe.SliceData(attrs)) != originalPtr {
				t.Errorf("AddAttributes mutated slice pointer")
			}

			// Verify element-wise equality
			for i, kv := range attrs {
				if !kv.Equal(originalAttrs[i]) {
					t.Errorf("AddAttributes mutated element %d: expected %v, got %v", i, originalAttrs[i], kv)
				}
			}
		},
	)
}

// FuzzRecordSetAttributesMutation fuzzes SetAttributes to ensure no input mutation occurs.
func FuzzRecordSetAttributesMutation(f *testing.F) {
	// Seed with edge cases
	f.Add([]byte("key"), []byte("value"), []byte("key2"), []byte("value2"), int8(-1), int8(-1), true)
	f.Add([]byte("k1"), []byte("v1"), []byte("k2"), []byte("v2"), int8(0), int8(0), false)
	f.Add(
		[]byte("long_key_name"),
		[]byte("very_long_value_that_might_be_truncated"),
		[]byte("short"),
		[]byte("val"),
		int8(5),
		int8(8),
		true,
	)

	f.Fuzz(func(t *testing.T, key1, value1, key2, value2 []byte, countLimit, valueLimit int8, allowDupKeys bool) {
		k1, v1 := string(key1), string(value1)
		k2, v2 := string(key2), string(value2)

		// Create larger attribute set
		attrs := []log.KeyValue{
			log.String(k1, v1),
			log.String(k2, v2),
			log.String("attr3", "value3"),
			log.String("attr4", "value4"),
			log.String("attr5", "value5"),
			log.String(k1+"_copy", v1), // Potential duplicate content
			log.String("attr7", "value7"),
			log.String("attr8", "value8"),
		}
		originalAttrs := make([]log.KeyValue, len(attrs))
		copy(originalAttrs, attrs)

		// Capture slice metadata
		originalLen := len(attrs)
		originalCap := cap(attrs)

		r := &Record{
			attributeCountLimit:       int(countLimit),
			attributeValueLengthLimit: int(valueLimit),
			allowDupKeys:              allowDupKeys,
		}

		r.SetAttributes(attrs...)

		// Verify no mutation
		if len(attrs) != originalLen {
			t.Errorf("SetAttributes mutated slice length: expected %d, got %d", originalLen, len(attrs))
		}

		if cap(attrs) != originalCap {
			t.Errorf("SetAttributes mutated slice capacity: expected %d, got %d", originalCap, cap(attrs))
		}

		for i, kv := range attrs {
			if !kv.Equal(originalAttrs[i]) {
				t.Errorf("SetAttributes mutated element %d: expected %v, got %v", i, originalAttrs[i], kv)
			}
		}
	})
}

// FuzzRecordSetBodyMutation fuzzes SetBody to ensure no input mutation occurs.
func FuzzRecordSetBodyMutation(f *testing.F) {
	// Seed with different value types
	f.Add([]byte("string_value"), uint8(1), false) // String value
	f.Add([]byte("key1"), uint8(2), false)         // Map value
	f.Add([]byte("item1"), uint8(3), true)         // Slice value

	f.Fuzz(func(t *testing.T, data []byte, valueType uint8, allowDupKeys bool) {
		var body log.Value

		// Create different types of values based on valueType
		switch valueType % 4 {
		case 0:
			body = log.StringValue(string(data))
		case 1:
			body = log.IntValue(len(data))
		case 2:
			// Create a map with potential duplicates
			body = log.MapValue(
				log.String("key1", string(data)),
				log.String("key2", "static"),
				log.String("key1", "duplicate"), // This might trigger deduplication
			)
		case 3:
			// Create a slice
			body = log.SliceValue(
				log.StringValue(string(data)),
				log.IntValue(42),
			)
		}

		// For map values, capture the original state more carefully
		var originalMapKvs []log.KeyValue
		if body.Kind() == log.KindMap {
			originalMapKvs = make([]log.KeyValue, len(body.AsMap()))
			copy(originalMapKvs, body.AsMap())
		}

		r := &Record{
			allowDupKeys: allowDupKeys,
		}

		r.SetBody(body)

		// Verify the original body value wasn't mutated
		if body.Kind() == log.KindMap {
			currentMapKvs := body.AsMap()
			if len(currentMapKvs) != len(originalMapKvs) {
				t.Errorf("SetBody mutated map length: expected %d, got %d", len(originalMapKvs), len(currentMapKvs))
			}

			for i, kv := range currentMapKvs {
				if i < len(originalMapKvs) && !kv.Equal(originalMapKvs[i]) {
					t.Errorf("SetBody mutated map element %d: expected %v, got %v", i, originalMapKvs[i], kv)
				}
			}
		}
	})
}

// FuzzRecordComplex fuzzes complex scenarios with multiple operations.
func FuzzRecordComplex(f *testing.F) {
	// Seed with complex scenarios
	f.Add([]byte("attr1"), []byte("value1"), []byte("attr2"), []byte("value2"),
		[]byte("body_key"), []byte("body_value"), int8(3), int8(10), false)
	f.Add([]byte("large_attr"), []byte("large_value_with_lots_of_content"), []byte("small"), []byte("val"),
		[]byte("body"), []byte("content"), int8(8), int8(15), true)
	f.Add([]byte(""), []byte(""), []byte("empty_test"), []byte("empty_value"),
		[]byte("empty_body"), []byte(""), int8(5), int8(5), false)

	f.Fuzz(func(t *testing.T, key1, val1, key2, val2, bodyKey, bodyVal []byte,
		countLimit, valueLimit int8, allowDupKeys bool,
	) {
		// Create attributes with potential for triggering various code paths
		attrs := []log.KeyValue{
			log.String(string(key1), string(val1)),
			log.String(string(key2), string(val2)),
			log.String(string(key1), "duplicate"), // Potential duplicate
			log.String("complex_attr1", "complex_value1"),
			log.String("complex_attr2", "complex_value2"),
			log.String("complex_attr3", "complex_value3"),
			log.String(string(key2)+"_variant", string(val2)+"_modified"),
			log.String("final_complex_attr", "final_complex_value"),
			log.String(string(key1)+"_second_dup", "another_duplicate"), // Another potential duplicate
		}

		// Create body with nested structure
		body := log.MapValue(
			log.String(string(bodyKey), string(bodyVal)),
			log.Slice("nested",
				log.StringValue("item1"),
				log.IntValue(42),
			),
			log.String(string(bodyKey), "duplicate_body"), // Potential duplicate
		)

		// Deep copy everything for verification
		originalAttrs := make([]log.KeyValue, len(attrs))
		copy(originalAttrs, attrs)

		originalBodyKvs := make([]log.KeyValue, len(body.AsMap()))
		copy(originalBodyKvs, body.AsMap())

		// Capture slice metadata
		originalLen := len(attrs)
		originalCap := cap(attrs)

		r := &Record{
			attributeCountLimit:       int(countLimit),
			attributeValueLengthLimit: int(valueLimit),
			allowDupKeys:              allowDupKeys,
		}

		// Perform multiple operations that might interact
		r.SetAttributes(attrs[:1]...)
		r.AddAttributes(attrs[1:]...)
		r.SetBody(body)

		// Verify no mutations occurred
		if len(attrs) != originalLen {
			t.Errorf("Complex operations mutated attrs length: expected %d, got %d", originalLen, len(attrs))
		}

		if cap(attrs) != originalCap {
			t.Errorf("Complex operations mutated attrs capacity: expected %d, got %d", originalCap, cap(attrs))
		}

		for i, kv := range attrs {
			if !kv.Equal(originalAttrs[i]) {
				t.Errorf("Complex operations mutated attr %d: expected %v, got %v", i, originalAttrs[i], kv)
			}
		}

		// Verify body wasn't mutated
		currentBodyKvs := body.AsMap()
		if len(currentBodyKvs) != len(originalBodyKvs) {
			t.Errorf(
				"Complex operations mutated body length: expected %d, got %d",
				len(originalBodyKvs),
				len(currentBodyKvs),
			)
		}

		for i, kv := range currentBodyKvs {
			if i < len(originalBodyKvs) && !kv.Equal(originalBodyKvs[i]) {
				t.Errorf("Complex operations mutated body element %d: expected %v, got %v", i, originalBodyKvs[i], kv)
			}
		}
	})
}

// FuzzRecordSliceSharing fuzzes scenarios that might cause slice sharing issues.
func FuzzRecordSliceSharing(f *testing.F) {
	f.Add([]byte("key"), []byte("val"), int8(2), int8(5))

	f.Fuzz(func(t *testing.T, keyData, valData []byte, count, valueLen int8) {
		if count < 0 || valueLen < 0 {
			return // Skip negative values for this test
		}

		key, val := string(keyData), string(valData)

		// Create a slice that might be modified with more than 5 attributes
		attrs := make([]log.KeyValue, 0, 15)
		attrs = append(attrs, log.String(key, val))
		attrs = append(attrs, log.String(key+"_2", val+"_2"))
		attrs = append(attrs, log.String(key+"_3", val+"_3"))
		attrs = append(attrs, log.String(key+"_4", val+"_4"))
		attrs = append(attrs, log.String(key+"_5", val+"_5"))
		attrs = append(attrs, log.String(key+"_6", val+"_6"))
		attrs = append(attrs, log.String("sharing_test_1", "sharing_value_1"))
		attrs = append(attrs, log.String("sharing_test_2", "sharing_value_2"))
		attrs = append(attrs, log.String(key+"_duplicate", val)) // Potential duplicate

		// Capture original slice state
		originalAttrs := make([]log.KeyValue, len(attrs))
		copy(originalAttrs, attrs)
		originalLen := len(attrs)

		r := &Record{
			attributeCountLimit:       int(count),
			attributeValueLengthLimit: int(valueLen),
			allowDupKeys:              false, // Enable deduplication
		}

		r.AddAttributes(attrs...)

		// Create a second record and verify the first slice wasn't affected
		r2 := &Record{
			attributeCountLimit:       int(count) + 1,
			attributeValueLengthLimit: int(valueLen) + 1,
			allowDupKeys:              true,
		}

		r2.SetAttributes(attrs...)

		// Verify original slice is unchanged
		if len(attrs) != originalLen {
			t.Errorf("Slice sharing affected length: expected %d, got %d", originalLen, len(attrs))
		}

		for i, kv := range attrs {
			if !kv.Equal(originalAttrs[i]) {
				t.Errorf("Slice sharing affected element %d: expected %v, got %v", i, originalAttrs[i], kv)
			}
		}
	})
}
```

```
$ go test -fuzz=FuzzRecordAddAttributesMutation -fuzztime=10m
fuzz: elapsed: 10m0s, execs: 53488122 (0/sec), new interesting: 14 (total: 96)
PASS

$ go test -fuzz=FuzzRecordSetAttributesMutation -fuzztime=10m
fuzz: elapsed: 10m0s, execs: 53304476 (0/sec), new interesting: 8 (total: 80)
PASS

$ go test -fuzz=FuzzRecordSetBodyMutation -fuzztime=10m
fuzz: elapsed: 10m0s, execs: 55578009 (0/sec), new interesting: 1 (total: 10)
PASS

$ go test -fuzz=FuzzRecordComplex -fuzztime=10m
fuzz: elapsed: 10m0s, execs: 48152261 (0/sec), new interesting: 4 (total: 84)
PASS

$ go test -fuzz=FuzzRecordSliceSharing -fuzztime=10m
fuzz: elapsed: 10m0s, execs: 50531410 (0/sec), new interesting: 8 (total: 101)
PASS
ok      go.opentelemetry.io/otel/sdk/log        600.192s
```

---

**pellared** — 2025-10-01T10:43:30Z

From https://www.githubstatus.com/

>  Update - Customers using GitHub Actions Mac OS runners are experiencing job start delays and failures. We are aware of this issue and actively investigating.
Oct 01, 2025 - 08:17 UTC 

---

**pellared** — 2025-10-16T19:06:43Z

@MrAlias, merging the PR as I am out next week and tomorrow I need to focus on other things :grimacing:  If you find any opportunities to improve the performance then please create an issue or PR. If I remember correctly this was the consensus during the SIG meeting.

## Reviews (12)

**copilot-pull-request-reviewer[bot]** — COMMENTED — 2025-09-24T11:28:31Z

## Pull Request Overview

This PR fixes a concurrency bug in the OpenTelemetry Go SDK where the `AddAttributes`, `SetAttributes`, and `SetBody` methods on the `Record` type were mutating input parameters, causing race conditions when the same input data was used concurrently across multiple goroutines.

- Implements defensive copying to prevent input mutation while maintaining performance optimizations
- Adds comprehensive test coverage for various deduplication and truncation scenarios
- Removes race condition workarounds that were previously skipping tests

### Reviewed Changes

Copilot reviewed 5 out of 5 changed files in this pull request and generated no comments.

<details>
<summary>Show a summary per file</summary>

| File | Description |
| ---- | ----------- |
| sdk/log/record.go | Core fix - adds defensive copying logic and optimization checks to prevent input mutation |
| sdk/log/record_test.go | Extensive test cases added for deduplication, truncation, and edge cases; removes race condition skip |
| sdk/log/race_on_test.go | Removed - no longer needed after fixing the race condition |
| sdk/log/race_off_test.go | Removed - no longer needed after fixing the race condition |
| CHANGELOG.md | Documents the bug fix |
</details>






---

<sub>**Tip:** Customize your code reviews with copilot-instructions.md. <a href="/open-telemetry/opentelemetry-go/new/main/.github?filename=copilot-instructions.md" class="Link--inTextBlock" target="_blank" rel="noopener noreferrer">Create the file</a> or <a href="https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot" class="Link--inTextBlock" target="_blank" rel="noopener noreferrer">learn how to get started</a>.</sub>

**flc1125** — COMMENTED — 2025-09-25T13:30:28Z

😅 Quite profound.

**pellared** — COMMENTED — 2025-09-25T18:15:45Z

**dmathieu** — APPROVED — 2025-09-26T07:44:49Z

**MrAlias** — COMMENTED — 2025-09-29T16:37:35Z

**pellared** — COMMENTED — 2025-09-29T18:29:03Z

**MrAlias** — COMMENTED — 2025-09-29T19:58:01Z

**pellared** — COMMENTED — 2025-09-29T20:02:51Z

**pellared** — COMMENTED — 2025-10-01T10:35:21Z

**dashpole** — COMMENTED — 2025-10-16T18:35:17Z

**dashpole** — APPROVED — 2025-10-16T18:35:28Z

**pellared** — COMMENTED — 2025-10-16T19:02:46Z

## Review Comments (9)

**flc1125** on `sdk/log/record.go` — 2025-09-25T13:22:51Z

```suggestion
	New: func() any { return make(map[string]struct{}) },
```

For such cases, adjusting to a `struct{}` like this might result in lower memory usage.

**pellared** on `sdk/log/record.go` — 2025-09-25T18:15:45Z

https://github.com/open-telemetry/opentelemetry-go/pull/7403/commits/e4604acb0206fe490174bfe11414a37f9d77e15b

**MrAlias** on `sdk/log/record.go` (line 222) — 2025-09-29T16:37:11Z

The replacement algorithm is now iterating `attrs` twice. This seems like a regression and very inefficient.

**pellared** on `sdk/log/record.go` (line 222) — 2025-09-29T18:29:03Z

Only if there is a duplicate. Doing it twice has the same O-performance.
The benchmarks do not show significant overhead. I propose improving the performance in a separate PR.

**MrAlias** on `sdk/log/record.go` (line 222) — 2025-09-29T19:58:01Z

> [...] The benchmarks do not show significant overhead.

<img width="1492" height="37" alt="20250929_125621" src="https://github.com/user-attachments/assets/a719ec85-37b8-4f4c-9007-18573f7fa5d2" />

Are these the wrong benchmark results?

I think we should implement a single-pass algorithm from the start. There isn't much reason to add an inefficient algorithm just to replace it with the efficient one in another PR.

**pellared** on `sdk/log/record.go` (line 222) — 2025-09-29T20:02:50Z

```
AddAttributes/Deduplication/Enabled-20           137.1n ±  4%    230.3n ±  5%   +67.92% (p=0.000 n=10)
AddAttributes/NestedDeduplication/Enabled-20     430.1n ±  1%   1010.0n ±  4%  +134.80% (p=0.000 n=10)
```

I will try to work on it.

**pellared** on `sdk/log/record.go` (line 222) — 2025-10-01T10:35:21Z

Done.
I updated the benchstat results.
It is better after the changes.

```
AddAttributes/Deduplication/Enabled-20           144.5n ±  4%    165.8n ±  4%   +14.71% (p=0.000 n=10)
AddAttributes/NestedDeduplication/Enabled-20     439.2n ±  2%    792.4n ± 11%   +80.41% (p=0.000 n=10)
```


PTAL

**dashpole** on `sdk/log/record.go` (line 222) — 2025-10-16T18:35:17Z

Can you update the description as well?

**pellared** on `sdk/log/record.go` (line 222) — 2025-10-16T19:02:46Z

I already  updated the benchmarks :wink: 

But now I also removed the remark about possible improvements.
If there are any then a follow-up PR is the way to go.

## Timeline

- 2025-09-23T19:58:07Z · **ready_for_review** by pellared
- 2025-09-23T19:58:08Z · **review_requested** by pellared
- 2025-09-23T19:58:08Z · **review_requested** by pellared
- 2025-09-23T19:58:08Z · **review_requested** by pellared
- 2025-09-23T19:58:08Z · **review_requested** by pellared
- 2025-09-23T19:58:08Z · **review_requested** by pellared
- 2025-09-24T11:28:01Z · **review_requested** by pellared
- 2025-09-25T13:32:57Z · **convert_to_draft** by pellared
- 2025-09-25T17:08:16Z · **milestoned** by pellared → v1.39.0
- 2025-09-25T18:30:26Z · **ready_for_review** by pellared
- 2025-09-25T18:36:45Z · **convert_to_draft** by pellared
- 2025-09-25T18:44:28Z · **ready_for_review** by pellared
- 2025-09-25T18:50:17Z · **review_requested** by pellared
- 2025-09-25T20:04:04Z · **labeled** by pellared `pkg:SDK`
- 2025-09-25T20:04:04Z · **labeled** by pellared `area:logs`
- 2025-09-30T18:10:12Z · **convert_to_draft** by pellared
- 2025-10-01T10:39:23Z · **ready_for_review** by pellared
- 2025-10-01T10:48:07Z · **review_requested** by pellared
- 2025-10-16T19:07:08Z · **merged** by pellared
- 2025-10-16T19:07:09Z · **closed** by pellared
- 2025-10-16T19:07:17Z · **head_ref_deleted** by pellared
- 2025-11-03T09:18:09Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-12-05T18:12:13Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7676
- 2025-12-08T16:30:52Z · **referenced** by MrAlias

