**Source ID**: [SRC-PR-04]

# Pull Request: Use sync.Map and atomics to improve sum performance (open-telemetry/opentelemetry-go#7427)

**Canonical URL**: https://github.com/open-telemetry/opentelemetry-go/pull/7427  
**Author**: dashpole  
**Created**: 2025-09-29T14:36:56Z · **Updated**: 2025-10-14T14:40:27Z  
**Collected**: 2026-07-14T14:35:41Z  
**State**: merged (2025-10-07T13:40:23Z)  
**Branch**: `optimize_counter_syncmap` → `main`  
**Changes**: +437 / -121 across 14 files  
**Labels**: area:metrics  
**Milestone**: v1.39.0

---

## Description

Alternative to https://github.com/open-telemetry/opentelemetry-go/pull/7380

This uses a sync.Map and atomics for the sum's counter value.  This intentionally introduces a new race condition that didn't previously exist:
* It is possible for the exemplar to be recorded in the batch of metrics after the add() for cumulative sum aggregations. For cumulative, this isn't a huge issue since exemplars are expected to persist across collection cycles. This is difficult to fix because we can't manage the internal storage of an exemplar.Reservoir (to atomically swap between hot and cold storage).  If we are able to make assumptions about how exemplar reservoirs are managed (i.e. that the number of and order of exemplars returned is always the same), then we could possibly fix this by merging at export time.

### Alternatives Considered

#### RWLock for the map instead of sync.Map

This is significantly less performant.

#### Single sync.Map without hotColdWaitGroup

Deleting keys from the sync.Map concurrently with measurements (during Clear() of the sync.Map) can cause measurements to be made to a counter that has already been read, exported and deleted.  This can produce incorrect sums when delta is used.  Instead, atomically switching writes to a completely empty sync.Map and waiting for writes to the previous sync.Map complete eliminates this issue.

#### Use two sync.Map for cumulative sums

One idea I explored was doing a hot-cold swap for cumulative sums just like we do for delta sums.  We would swap the hot and cold sync.Maps, wait for writes to the cold sync.Map to complete while new writes go to the hot map.  Then, once we are done reading the cold map, we could merge the contents of the cold map back into the new hot map.

This approach has two issues:

* It isn't possible to "merge" one exemplar reservoir into another. This is an issue for persistent exemplars that aren't overwritten in a collection interval.
* We can't keep a consistent set of keys in overflow scenarios.  Measurements that are made to the hot map before the merge of the cold into hot that should have been overflows will be added as new attribute sets.  That, in turn, means we will need to change previously-exported attribute sets to the overflow set, which will cause issues for users.

### Benchmarks

Parallel:
```
goos: linux
goarch: amd64
pkg: go.opentelemetry.io/otel/sdk/metric
cpu: AMD EPYC 7B12
                                                                                  │  main24.txt   │            new24_new.txt            │
                                                                                  │    sec/op     │    sec/op     vs base               │
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/0-24                   255.65n ± 13%   68.06n ±  3%  -73.38% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/1-24                   286.70n ±  8%   67.66n ±  4%  -76.40% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/10-24                  287.15n ± 14%   69.90n ±  3%  -75.66% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/0-24                 244.75n ±  9%   68.83n ±  4%  -71.88% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/1-24                 267.20n ± 14%   65.86n ±  3%  -75.35% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/10-24                291.50n ± 13%   66.59n ± 11%  -77.15% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/0-24             247.85n ±  7%   66.06n ±  3%  -73.34% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/1-24             286.75n ± 10%   68.52n ±  2%  -76.10% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/10-24            289.50n ± 20%   67.45n ±  4%  -76.70% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/0-24           246.25n ± 14%   66.69n ±  2%  -72.92% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/1-24           289.55n ±  9%   65.54n ±  5%  -77.36% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/10-24          286.05n ± 14%   67.55n ±  2%  -76.39% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/0-24                      254.8n ± 23%   225.9n ± 17%  -11.32% (p=0.026 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/1-24                      304.4n ± 13%   234.4n ± 19%  -23.01% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/10-24                     308.9n ± 20%   217.6n ± 10%  -29.56% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/0-24                    267.8n ± 14%   220.1n ± 19%  -17.80% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/1-24                    274.1n ± 21%   226.5n ±  5%  -17.38% (p=0.024 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/10-24                   239.0n ± 14%   236.1n ± 18%        ~ (p=0.589 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/0-24                  223.7n ± 11%   234.8n ±  7%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/1-24                  253.9n ± 10%   244.8n ± 11%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/10-24                 272.6n ±  7%   250.0n ± 12%   -8.33% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/0-24                232.6n ±  4%   232.2n ±  8%        ~ (p=0.937 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/1-24                276.7n ± 20%   249.2n ± 11%        ~ (p=0.485 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/10-24               265.9n ± 18%   246.4n ±  9%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/0-24       294.0n ± 11%   269.0n ±  5%   -8.47% (p=0.015 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/1-24       314.6n ± 10%   268.8n ±  6%  -14.54% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/10-24      303.9n ± 11%   285.4n ±  4%        ~ (p=0.180 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/0-24     274.7n ± 13%   262.9n ±  7%        ~ (p=0.145 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/1-24     296.1n ±  6%   288.9n ±  9%        ~ (p=0.180 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/10-24    276.0n ± 14%   299.4n ± 12%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/0-24                     191.4n ±  4%   176.0n ±  3%   -8.05% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/1-24                     223.2n ±  8%   172.8n ±  3%  -22.54% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/10-24                    265.7n ± 19%   172.2n ±  2%  -35.21% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/0-24                   179.4n ± 18%   171.0n ±  3%   -4.74% (p=0.009 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/1-24                   209.1n ± 16%   175.4n ±  5%  -16.07% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/10-24                  222.5n ± 17%   175.6n ±  4%  -21.08% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/0-24               194.4n ± 11%   176.9n ±  5%   -9.03% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/1-24               207.5n ± 13%   175.1n ±  2%  -15.66% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/10-24              243.7n ± 13%   172.6n ±  3%  -29.15% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/0-24             218.3n ± 10%   177.6n ±  2%  -18.67% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/1-24             193.5n ± 10%   176.1n ±  2%   -8.99% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/10-24            192.8n ± 11%   173.7n ±  2%   -9.91% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/0-24                       185.1n ±  9%   204.8n ±  9%  +10.61% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/1-24                       218.8n ± 14%   229.7n ± 16%        ~ (p=0.310 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/10-24                      242.7n ±  8%   209.1n ± 18%  -13.84% (p=0.041 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/0-24                     182.8n ± 42%   255.2n ±  8%  +39.67% (p=0.015 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/1-24                     198.0n ±  7%   280.6n ± 22%  +41.72% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/10-24                    236.3n ± 18%   261.7n ±  8%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/0-24                   223.2n ±  9%   226.9n ±  4%        ~ (p=0.965 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/1-24                   270.1n ± 10%   280.2n ±  6%        ~ (p=0.143 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/10-24                  257.2n ±  7%   252.0n ±  7%        ~ (p=0.485 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/0-24                 277.0n ±  5%   310.4n ± 12%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/1-24                 287.3n ±  9%   271.2n ± 12%        ~ (p=0.699 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/10-24                281.8n ±  9%   316.5n ± 22%  +12.29% (p=0.041 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/0-24        289.1n ±  9%   297.1n ± 12%        ~ (p=0.310 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/1-24        277.8n ±  6%   353.1n ± 11%  +27.11% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/10-24       281.8n ± 11%   352.2n ± 16%  +24.94% (p=0.009 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/0-24      294.1n ±  7%   317.5n ±  9%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/1-24      281.7n ± 10%   332.1n ±  8%  +17.89% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/10-24     238.9n ± 12%   318.1n ±  9%  +33.13% (p=0.002 n=6)
geomean                                                                              251.9n         184.4n        -26.77%
```


Single-threaded:
```
goos: linux
goarch: amd64
pkg: go.opentelemetry.io/otel/sdk/metric
cpu: Intel(R) Xeon(R) CPU @ 2.20GHz
                                                                               │  main1.txt   │              sync1.txt              │
                                                                               │    sec/op    │    sec/op     vs base               │
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/0                   109.8n ±  7%   113.4n ± 23%        ~ (p=1.000 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/1                   115.0n ±  4%   113.3n ± 20%        ~ (p=0.729 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Counter/Attributes/10                  177.1n ± 34%   110.2n ± 16%  -37.78% (p=0.009 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/0                 110.5n ± 42%   109.2n ± 19%        ~ (p=0.457 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/1                 118.8n ±  2%   118.4n ±  5%        ~ (p=0.619 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Counter/Attributes/10                119.0n ±  2%   116.8n ± 42%        ~ (p=0.699 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/0             106.9n ±  1%   102.5n ±  5%   -4.16% (p=0.030 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/1             117.2n ±  2%   116.9n ±  7%        ~ (p=1.000 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64UpDownCounter/Attributes/10            115.4n ±  1%   115.1n ±  5%        ~ (p=0.937 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/0           109.5n ±  5%   104.2n ±  8%   -4.84% (p=0.041 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/1           118.7n ± 14%   113.8n ± 35%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64UpDownCounter/Attributes/10          116.6n ±  1%   116.8n ±  8%        ~ (p=0.968 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/0                     106.6n ±  4%   109.4n ±  5%        ~ (p=0.093 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/1                     114.7n ±  4%   117.9n ±  4%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Gauge/Attributes/10                    115.2n ±  4%   114.5n ±  1%        ~ (p=0.162 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/0                   109.4n ±  5%   107.5n ±  3%        ~ (p=0.132 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/1                   118.3n ±  2%   117.9n ±  3%        ~ (p=0.589 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Gauge/Attributes/10                  117.7n ±  2%   120.8n ± 14%        ~ (p=0.093 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/0                 96.78n ±  1%   99.37n ±  3%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/1                 103.0n ±  3%   116.5n ± 26%  +13.16% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Int64Histogram/Attributes/10                102.8n ±  1%   107.6n ± 22%   +4.67% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/0               93.95n ± 22%   99.88n ± 18%   +6.32% (p=0.041 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/1               102.7n ±  5%   106.2n ±  6%        ~ (p=0.089 n=6)
SyncMeasure/NoView/ExemplarsDisabled/Float64Histogram/Attributes/10              104.1n ±  4%   108.3n ± 27%   +4.03% (p=0.026 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/0      146.3n ±  1%   154.0n ± 24%   +5.23% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/1      154.8n ±  3%   161.2n ±  2%   +4.20% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialInt64Histogram/Attributes/10     155.5n ±  1%   164.0n ±  4%   +5.43% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/0    145.9n ±  2%   159.7n ± 12%   +9.42% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/1    155.2n ±  0%   164.0n ±  6%   +5.70% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsDisabled/ExponentialFloat64Histogram/Attributes/10   219.3n ± 29%   159.5n ±  3%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/0                    263.6n ± 36%   177.2n ±  1%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/1                    189.1n ±  8%   190.4n ± 12%        ~ (p=0.589 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Counter/Attributes/10                   184.3n ±  3%   189.4n ±  6%        ~ (p=0.065 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/0                  180.7n ±  1%   182.7n ±  2%        ~ (p=0.457 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/1                  192.8n ±  9%   192.0n ±  1%        ~ (p=1.000 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Counter/Attributes/10                 192.3n ±  4%   190.2n ±  4%        ~ (p=0.093 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/0              176.5n ±  2%   181.7n ±  4%   +2.95% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/1              184.0n ±  4%   192.0n ±  1%   +4.32% (p=0.015 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64UpDownCounter/Attributes/10             184.4n ±  1%   195.2n ±  3%   +5.83% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/0            183.0n ±  3%   177.4n ±  5%   -3.06% (p=0.048 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/1            194.4n ±  4%   188.1n ±  5%        ~ (p=0.084 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64UpDownCounter/Attributes/10           193.0n ±  5%   194.1n ±  5%        ~ (p=0.699 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/0                      178.4n ± 14%   185.6n ± 29%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/1                      189.0n ±  8%   193.2n ±  2%        ~ (p=0.132 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Gauge/Attributes/10                     197.7n ±  5%   198.8n ±  2%        ~ (p=0.619 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/0                    185.5n ±  3%   188.8n ±  4%        ~ (p=0.310 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/1                    191.2n ±  3%   190.2n ±  7%        ~ (p=0.732 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Gauge/Attributes/10                   186.8n ±  2%   197.1n ±  6%   +5.54% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/0                  224.2n ±  4%   227.3n ±  2%        ~ (p=0.394 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/1                  232.5n ±  3%   242.5n ±  5%        ~ (p=0.132 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Int64Histogram/Attributes/10                 232.5n ±  3%   237.1n ±  5%   +2.00% (p=0.045 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/0                227.5n ±  2%   238.5n ±  5%   +4.81% (p=0.017 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/1                239.4n ±  8%   250.1n ±  6%        ~ (p=0.240 n=6)
SyncMeasure/NoView/ExemplarsEnabled/Float64Histogram/Attributes/10               241.5n ±  4%   254.0n ±  2%   +5.18% (p=0.004 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/0       231.1n ±  5%   239.2n ±  3%        ~ (p=0.084 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/1       260.2n ± 16%   253.8n ±  4%        ~ (p=0.190 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialInt64Histogram/Attributes/10      234.3n ±  1%   246.8n ±  2%   +5.29% (p=0.002 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/0     221.8n ±  6%   232.0n ±  4%   +4.58% (p=0.037 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/1     228.2n ±  7%   240.6n ±  1%   +5.41% (p=0.041 n=6)
SyncMeasure/NoView/ExemplarsEnabled/ExponentialFloat64Histogram/Attributes/10    228.6n ±  7%   244.7n ±  1%   +7.04% (p=0.015 n=6)
geomean                                                                          158.1n         158.1n         +0.00%
```

## Discussion (3)

**codecov[bot]** — 2025-09-29T14:38:36Z

## [Codecov](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?dropdown=coverage&src=pr&el=h1&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) Report
:x: Patch coverage is `96.84211%` with `6 lines` in your changes missing coverage. Please review.
:white_check_mark: Project coverage is 85.7%. Comparing base ([`cfd8570`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/cfd85706984ee977c2fe774f72c13c80ed1750d3?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)) to head ([`dc212da`](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/commit/dc212da41c9208113cf8503c188b580caba26417?dropdown=coverage&el=desc&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)).
:warning: Report is 1 commits behind head on main.

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Patch % | Lines |
|---|---|---|
| [sdk/metric/internal/aggregate/atomic.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fatomic.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvYXRvbWljLmdv) | 91.8% | [4 Missing and 2 partials :warning: ](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) |

<details><summary>Additional details and impacted files</summary>



[![Impacted file tree graph](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427/graphs/tree.svg?width=650&height=150&src=pr&token=8efTmh4kvf&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)

```diff
@@          Coverage Diff           @@
##            main   #7427    +/-   ##
======================================
  Coverage   85.7%   85.7%            
======================================
  Files        285     286     +1     
  Lines      25228   25331   +103     
======================================
+ Hits       21633   21731    +98     
- Misses      3216    3219     +3     
- Partials     379     381     +2     
```

| [Files with missing lines](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?dropdown=coverage&src=pr&el=tree&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | Coverage Δ | |
|---|---|---|
| [sdk/metric/exemplar/fixed\_size\_reservoir.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Ffixed_size_reservoir.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9maXhlZF9zaXplX3Jlc2Vydm9pci5nbw==) | `97.6% <100.0%> (+<0.1%)` | :arrow_up: |
| [sdk/metric/exemplar/histogram\_reservoir.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Fhistogram_reservoir.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9oaXN0b2dyYW1fcmVzZXJ2b2lyLmdv) | `93.3% <100.0%> (+1.0%)` | :arrow_up: |
| [sdk/metric/exemplar/storage.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Fexemplar%2Fstorage.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9leGVtcGxhci9zdG9yYWdlLmdv) | `100.0% <ø> (ø)` | |
| [sdk/metric/internal/aggregate/aggregate.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Faggregate.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvYWdncmVnYXRlLmdv) | `100.0% <100.0%> (ø)` | |
| [...metric/internal/aggregate/exponential\_histogram.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fexponential_histogram.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvZXhwb25lbnRpYWxfaGlzdG9ncmFtLmdv) | `96.6% <100.0%> (ø)` | |
| [...dk/metric/internal/aggregate/filtered\_reservoir.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Ffiltered_reservoir.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvZmlsdGVyZWRfcmVzZXJ2b2lyLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/histogram.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fhistogram.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvaGlzdG9ncmFtLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/lastvalue.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Flastvalue.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvbGFzdHZhbHVlLmdv) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/limit.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Flimit.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvbGltaXQuZ28=) | `100.0% <100.0%> (ø)` | |
| [sdk/metric/internal/aggregate/sum.go](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree&filepath=sdk%2Fmetric%2Finternal%2Faggregate%2Fsum.go&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry#diff-c2RrL21ldHJpYy9pbnRlcm5hbC9hZ2dyZWdhdGUvc3VtLmdv) | `100.0% <100.0%> (ø)` | |
| ... and [1 more](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry) | |

... and [1 file with indirect coverage changes](https://app.codecov.io/gh/open-telemetry/opentelemetry-go/pull/7427/indirect-changes?src=pr&el=tree-more&utm_medium=referral&utm_source=github&utm_content=comment&utm_campaign=pr+comments&utm_term=open-telemetry)
</details>
<details><summary> :rocket: New features to boost your workflow: </summary>

- :snowflake: [Test Analytics](https://docs.codecov.com/docs/test-analytics): Detect flaky tests, report on failures, and find test suite problems.
</details>

---

**dashpole** — 2025-09-30T15:51:05Z

Feel free to review.  I tried to document the code as well as I could.  I plan to present this at the 10/2 SIG meeting so it might be easier to review after that.

---

**dashpole** — 2025-10-02T14:15:56Z

This is ready for review, but tests will fail until it is rebased on https://github.com/open-telemetry/opentelemetry-go/pull/7441

## Reviews (15)

**MrAlias** — COMMENTED — 2025-10-03T15:14:31Z

**dashpole** — COMMENTED — 2025-10-03T15:23:10Z

**dashpole** — COMMENTED — 2025-10-03T15:25:53Z

**dashpole** — COMMENTED — 2025-10-03T15:27:00Z

**MrAlias** — COMMENTED — 2025-10-03T15:32:21Z

**dashpole** — COMMENTED — 2025-10-03T16:00:07Z

**dashpole** — COMMENTED — 2025-10-03T16:02:39Z

**MrAlias** — COMMENTED — 2025-10-03T16:32:39Z

**dashpole** — COMMENTED — 2025-10-04T03:16:18Z

**dashpole** — COMMENTED — 2025-10-04T03:16:30Z

**MrAlias** — COMMENTED — 2025-10-06T18:08:05Z

**dashpole** — COMMENTED — 2025-10-06T18:19:39Z

**dashpole** — COMMENTED — 2025-10-06T19:21:43Z

**MrAlias** — APPROVED — 2025-10-07T00:26:04Z

**dmathieu** — APPROVED — 2025-10-07T07:21:57Z

## Review Comments (18)

**MrAlias** on `CHANGELOG.md` — 2025-10-02T17:55:27Z

```suggestion
- Improve performance of concurrent measurements in `go.opentelemetry.io/otel/sdk/metric`. (#7427)
```

**MrAlias** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-03T00:03:10Z

Passing the temporality only to then parse it below and make a decision here seems like a bad smell. I'm more inclined to refactoring the Sum in some way to better address this and remove the control param being passed here.

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:10:13Z

A pre-increment approach with rollback may address this.

```suggestion
		// Pre-increment, reserve a slot first.
		newLen := s.len[hotIdx].Add(1)
		if s.aggLimit > 0 && newLen >= int64(s.aggLimit) {
			// We exceeded the limit, decrement back and use overflow
			s.len[hotIdx].Add(-1)
			fltrAttr = overflowSet
		}
```

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:14:24Z

Splitting this into a type dedicated to cumulative values seems appropriate. It would have fields like this right?

```suggestion
	values                  sync.Map
	len                     atomic.Int64
```

**dashpole** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-03T15:23:10Z

fair enough.  I felt it was more readable to have it accept the temporality than to pass a bool, but I can work on refactoring.

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:25:53Z

nice.  lgtm

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:27:00Z

yes

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T15:32:21Z

Sorry, didn't make it clear in my suggestion. This needs to change based on pre-increment.

```suggestion
		if loaded {
			// Someone else created this entry while we reserved a slot.
			// Decrement our reserved count since we didn't actually add a new entry.
			s.len[hotIdx].Add(-1)
```

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:00:07Z

Actually, I remembered why I didn't take this approach:  It introduces a new race condition where we can overflow even if we didn't create too many attribute sets.  Worse, we can end up splitting a single attribute set's observations between the attribute set and the overflow set.

Suppose we have an attribute set limit of 2.  We get 2 concurrent measure calls to the empty attribute set.
The first measure call increments len to 1.  Then, before the element is added to the map, the second measure call increments len to 2.  The first measure call will be written to the empty attribute set (correct!).  The second measure call will be written to the overflow set (incorrect!).

IMO, this is worse than the possibility to exceed the attribute limit.

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:02:38Z

Unresolving, and I reverted the suggestion.  I don't think this works.  See https://github.com/open-telemetry/opentelemetry-go/pull/7427#discussion_r2402472887

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-03T16:32:39Z

I see.

Hitting the cardinality limit is an error scenario where we do our best to "handle it gracefully". I'm not sure what the appropriate behavior here is. Correctness is important, but equally important is protecting memory limits the user has asked us to respect.

I'll take another look.

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-04T03:16:18Z

Done in https://github.com/open-telemetry/opentelemetry-go/pull/7427/commits/b71918beccf18f34b3bdab83a2d8eb878eeee66e

**dashpole** on `sdk/metric/internal/aggregate/aggregate.go` — 2025-10-04T03:16:29Z

Fixed in https://github.com/open-telemetry/opentelemetry-go/pull/7427/commits/b71918beccf18f34b3bdab83a2d8eb878eeee66e

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T18:08:05Z

@dashpole thoughts: https://github.com/dashpole/opentelemetry-go/pull/2?

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T18:19:39Z

Thanks.  That inspired me:  I think we can just lock whenever changing the size.  Your PR does that anyways, so it shouldn't have much worse performance.  Plus, changing the size isn't really on the usual hot path.  Let me try something simpler and see how much worse it is...

**dashpole** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-06T19:21:43Z

Implemented in https://github.com/open-telemetry/opentelemetry-go/pull/7427/commits/5485c5b5f5cb2c4f347d1ad12e39c2aadfea0fa4.  I also updated benchmarks, and it is actually a performance improvement over the atomic length!

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-07T00:04:26Z

This can be renamed to `collect` now that the types are split.

```suggestion
func (s *deltaSum[N]) collect(
```

**MrAlias** on `sdk/metric/internal/aggregate/sum.go` — 2025-10-07T00:04:45Z

```suggestion
func (s *cumulativeSum[N]) collect(
```

## Timeline

- 2025-09-29T16:28:51Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7423
- 2025-09-29T19:49:42Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T14:50:14Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T14:57:29Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T15:11:55Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T15:43:45Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T15:45:33Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T15:47:47Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7380
- 2025-09-30T15:47:54Z · **ready_for_review** by dashpole
- 2025-09-30T15:47:54Z · **review_requested** by dashpole
- 2025-09-30T15:47:55Z · **review_requested** by dashpole
- 2025-09-30T15:47:55Z · **review_requested** by dashpole
- 2025-09-30T15:47:55Z · **review_requested** by dashpole
- 2025-09-30T15:47:55Z · **review_requested** by dashpole
- 2025-09-30T15:51:45Z · **head_ref_force_pushed** by dashpole
- 2025-09-30T15:52:02Z · **labeled** by dashpole `area:metrics`
- 2025-09-30T16:05:30Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7189
- 2025-10-01T16:32:02Z · **referenced** by dashpole
- 2025-10-02T14:09:53Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T13:59:27Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T14:35:48Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T14:43:41Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T16:01:55Z · **head_ref_force_pushed** by dashpole
- 2025-10-03T17:34:52Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7443
- 2025-10-04T03:16:00Z · **head_ref_force_pushed** by dashpole
- 2025-10-04T03:49:03Z · **head_ref_force_pushed** by dashpole
- 2025-10-06T19:17:53Z · **head_ref_force_pushed** by dashpole
- 2025-10-06T19:21:01Z · **head_ref_force_pushed** by dashpole
- 2025-10-06T20:59:53Z · **head_ref_force_pushed** by dashpole
- 2025-10-06T21:01:38Z · **head_ref_force_pushed** by dashpole
- 2025-10-07T13:40:23Z · **merged** by dashpole
- 2025-10-07T13:40:23Z · **closed** by dashpole
- 2025-10-08T14:31:22Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7474
- 2025-10-08T19:23:19Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/7478
- 2025-10-09T17:25:37Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7037
- 2025-10-10T13:10:45Z · **cross-referenced** by pellared ← https://github.com/open-telemetry/opentelemetry-go/issues/6648
- 2025-10-14T14:40:27Z · **milestoned** by MrAlias → v1.39.0
- 2025-11-09T19:52:08Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/issues/7592
- 2025-12-05T18:12:13Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/pull/7676
- 2025-12-08T16:30:51Z · **referenced** by MrAlias
- 2025-12-11T16:56:05Z · **referenced** by dashpole
- 2025-12-16T08:23:15Z · **referenced** by dmathieu
- 2026-01-16T17:11:30Z · **cross-referenced** by MrAlias ← https://github.com/open-telemetry/opentelemetry-go/issues/7796
- 2026-03-19T21:37:06Z · **cross-referenced** by dashpole ← https://github.com/open-telemetry/opentelemetry-go/pull/8077
- 2026-06-04T22:57:58Z · **cross-referenced** by sudowork ← https://github.com/open-telemetry/opentelemetry-go/issues/8427

