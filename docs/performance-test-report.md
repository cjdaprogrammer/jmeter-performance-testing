# TaskFlow API Performance Test Report

## 1. Summary

Apache JMeter 5.6.3 was used to execute a local API workload against the TaskFlow FastAPI application. Four extended runs were completed with 1, 5, 10, and 25 virtual users and 20 loops per user.

The console summaries reported zero sample errors for all four runs. These are preliminary observations from a local development environment. Detailed p90/p95/p99 figures must be copied from the generated HTML dashboards before latency acceptance is declared.

## 2. Environment

- Operating system: Windows (local development machine)
- Java: OpenJDK 21 (reported during setup)
- Apache JMeter: 5.6.3
- API framework: FastAPI
- Server: Uvicorn
- Test plan: `test-plans/taskflow-baseline.jmx`
- Target: local API at `http://127.0.0.1:8000`

Update this section if the test setup changed during execution.

## 3. Workload and console results

| Virtual users | Ramp-up | Loops/user | Samples | Average (ms) | Min (ms) | Max (ms) | Throughput (requests/s) | Errors |
|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 1 s | 20 | 120 | 3 | 1 | 94 | 164.2 | 0 (0.00%) |
| 5 | 10 s | 20 | 600 | 1 | 0 | 45 | 73.2 | 0 (0.00%) |
| 10 | 20 s | 20 | 1,200 | 2 | 0 | 52 | 65.9 | 0 (0.00%) |
| 25 | 30 s | 20 | 3,000 | 1 | 0 | 41 | 103.5 | 0 (0.00%) |

The values above are the rounded values reported by JMeter's console summary. The 4,920 samples are the sum of the four separate runs; they are not one continuous test.

## 4. Findings

1. **Sample errors:** All four console summaries reported 0.00% errors.
2. **Observed throughput:** The 25-user run reported 103.5 requests/second. Throughput was not monotonic across the profiles: the 5- and 10-user runs reported lower throughput than the 1-user baseline.
3. **Response times:** Console averages were 1–3 ms after rounding, with maximums from 41 to 94 ms. The reported minimum of 0 ms reflects millisecond-level measurement/rounding and should not be interpreted as literally zero processing time.
4. **Interpretation limits:** Short local runs and in-memory application state are not enough to establish production capacity or predict performance under real network, database, and traffic conditions.

## 5. Acceptance criteria status

| Criterion | Target | Current evidence | Status |
|---|---|---|---|
| JMeter sample error rate | 0% | Console summaries show 0.00% in all four runs | Met at console-summary level; also verify dashboard assertions |
| Functional assertions | All pass | User reports HTML reports show 100% passed | Reported passed; retain report evidence |
| p95 response time | <= 500 ms | Detailed p95 values have not been transcribed into this report | Pending detailed dashboard review |

Do not change the p95 status to Pass until the relevant dashboard values have been checked.

## 6. Recommendations

- Transcribe average, median, p90, p95, p99, throughput, and error percentage from each dashboard's Statistics table.
- Inspect per-sampler results to confirm every CRUD request and assertion behaved as expected.
- Repeat each profile at least once under consistent conditions and compare results.
- Monitor CPU and memory during runs if practical.
- Consider adding a longer steady-state duration, explicit think time only if it matches the intended usage model, and a documented ramp-up/hold/stop pattern.
- For more realistic performance testing, consider moving the API and load generator to separate machines and adding persistent database storage in a later project iteration.

## 7. Artifacts

Expected result files:

- `results/baseline-20-loops.jtl`
- `results/load-5-users-20-loops.jtl`
- `results/load-10-users-20-loops.jtl`
- `results/load-25-users-20-loops.jtl`

Expected HTML dashboards:

- `reports/baseline-20-loops/index.html`
- `reports/load-5-users-20-loops/index.html`
- `reports/load-10-users-20-loops/index.html`
- `reports/load-25-users-20-loops/index.html`

Confirm each artifact exists before publishing the repository.

## 8. Conclusion

The current JMeter executions completed without sample errors in the console summaries and provide an initial comparison across four concurrency profiles. The results support a claim that a basic local API performance test suite has been implemented and executed. Detailed percentile values, repeatability checks, and environment limitations should be included before making stronger claims about latency or capacity.
