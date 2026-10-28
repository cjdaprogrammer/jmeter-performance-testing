# TaskFlow API — Performance Analysis

## 1\. Objective

Evaluate the response times and reliability of the TaskFlow API
under four local workloads using Apache JMeter.

## 2\. Test environment and scope

* API: TaskFlow FastAPI application
* Target: http://127.0.0.1:8000
* Load tool: Apache JMeter
* Workloads: 1, 5, 10, and 25 virtual users
* Iterations: 20 loops per virtual user
* Test scenarios: health check, list tasks, create task,
retrieve task, update task, and delete task
* Storage: in-memory
* Result source: raw JTL CSV files in the results directory

## 3\. Overall results

|Workload|Samples|Average (ms)|p95 (ms)|p99 (ms)|Errors|Estimated throughput (samples/s)|
|-|-:|-:|-:|-:|-:|-:|
|1 user|120|3.83|5.00|26.39|0 (0.00%)|197.69|
|5 users|600|1.69|3.00|4.00|0 (0.00%)|74.21|
|10 users|1,200|2.19|4.00|6.00|0 (0.00%)|66.63|
|25 users|3,000|1.71|3.00|4.00|0 (0.00%)|104.08|

The throughput values above are calculated from the earliest sample
start to the latest sample completion in each JTL file. They may differ
from JMeter dashboard throughput because measurement windows can differ.

## 4\. Acceptance criteria

Proposed criterion:

* Overall p95 response time must be at or below 500 ms.

Result:

* All four workloads met this proposed criterion based on the
calculated overall p95 values.
* All 4,920 samples across the four runs were successful.
* The observed error rate was 0.00% in each run.

These results apply only to the tested local environment and workload.

## 5\. Endpoint observations

* All six samplers recorded zero failed samples at every workload.
* The 1-user health-check sampler recorded a 94 ms maximum and
a 76.90 ms p99. This is an isolated latency spike worth further
investigation; its cause is not established by these results.
* At 25 users, each sampler recorded 500 samples, and the endpoint P95 values were approximately 3 ms in the recorded output.
* No consistent increase in throughput was observed at every step
between workload levels.

## 6\. Limitations

* The API was tested over localhost, avoiding real network latency.
* The application uses in-memory storage rather than a production
database.
* The tests do not establish production capacity or a maximum safe
concurrency level.
* The runs were short and do not establish endurance stability.
* The proposed 500 ms threshold is a project-defined target, not
an externally validated service-level objective.
* Percentiles were calculated from raw elapsed times using linear
interpolation. Small differences from JMeter dashboard percentiles
may occur if its calculation method differs.

## 7\. Recommendations

1. Repeat the tests to assess run-to-run variability.
2. Investigate the health-check latency spike and compare repeated runs.
3. Run a controlled stepped-load test with longer steady-state periods.
4. Monitor API process CPU and memory during load tests.
5. Add database-backed testing before drawing conclusions about
database or production performance.
6. Compare JMeter dashboard metrics with this raw-JTL analysis.

## 8\. Conclusion

The tested local API completed 4,920 samples across four workloads
without recorded failures. All four runs met the proposed overall
p95 threshold of 500 ms. Further sustained and monitored testing is
required before making claims about production capacity or scalability.

## P95 Response-Time Visualization

![TaskFlow API P95 response time by load](screenshots/p95-response-time.png)

The chart compares the 95th-percentile response time across four local test workloads. All four recorded P95 values were below the project-defined target of 500 ms.

| Concurrent users | P95 response time | Target result |
|---:|---:|---|
| 1 | 5 ms | Pass |
| 5 | 3 ms | Pass |
| 10 | 4 ms | Pass |
| 25 | 3 ms | Pass |

**Interpretation:** The observed P95 response times remained low across these short test runs. The results do not establish production capacity or guarantee performance under longer tests, different environments, or sustained traffic.