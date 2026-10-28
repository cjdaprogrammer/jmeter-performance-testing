\# TaskFlow API — Performance Test Report



\## 1. Test Overview



\*\*Project:\*\* TaskFlow API Performance Testing  

\*\*Tool:\*\* Apache JMeter 5.6.3  

\*\*Target:\*\* Local TaskFlow FastAPI application  

\*\*Test type:\*\* API baseline and concurrent-load testing  

\*\*Execution:\*\* Local Windows environment  

\*\*Workload:\*\* 1, 5, 10, and 25 virtual users, with 20 iterations per user  

\*\*Primary objective:\*\* Evaluate API response times, successful request completion, and observed behavior as concurrent load increases.



\## 2. Test Scope



The test plan covers six API operations:



\- `GET Health Check`

\- `GET List Tasks`

\- `POST Create Task`

\- `GET Task by ID`

\- `PUT Update Task`

\- `DELETE Task`



Each workload exercises the six operations. The recorded sample totals match the configured workload sizes.



\## 3. Acceptance Criteria



The following project-defined criteria were used:



\- \*\*P95 response time:\*\* less than or equal to 500 ms.

\- \*\*Sample error rate:\*\* 0% for the recorded test runs.

\- \*\*Functional execution:\*\* all six sampler groups complete without recorded JMeter sample failures.



These are project acceptance criteria for this local test, not universal performance standards.



\## 4. Summary of Results



| Virtual users | Samples | Average response time | P95 | P99 | Errors | Throughput\* |

|---:|---:|---:|---:|---:|---:|---:|

| 1 | 120 | 3.83 ms | 5 ms | 26.39 ms | 0 (0%) | 197.69 samples/sec |

| 5 | 600 | 1.69 ms | 3 ms | 4 ms | 0 (0%) | 74.21 samples/sec |

| 10 | 1,200 | 2.19 ms | 4 ms | 6 ms | 0 (0%) | 66.63 samples/sec |

| 25 | 3,000 | 1.71 ms | 3 ms | 4 ms | 0 (0%) | 104.08 samples/sec |

| \*\*Total\*\* | \*\*4,920\*\* | — | — | — | \*\*0 (0%)\*\* | — |



\\\*Throughput is calculated by the project's Python analyzer using the interval from the earliest sample start to the latest sample completion. It may differ from the throughput reported by the JMeter dashboard.



\### Acceptance results



\- All four workloads met the project-defined P95 target of 500 ms.

\- All 4,920 recorded samples succeeded.

\- No JMeter sample errors were recorded in these four local test runs.

\- The generated P95 chart is available at `docs/screenshots/p95-response-time.png`.



\## 5. Endpoint-Level Observations



\### Baseline: 1 virtual user



Each of the six samplers recorded 20 samples with no errors.



The health-check sampler had an average response time of 7.05 ms, P95 of 8.50 ms, P99 of 76.90 ms, and maximum of 94 ms. This indicates an isolated higher-latency observation worth investigating in a repeat run.



The other five operations had maximum response times between 4 and 30 ms.



\### Concurrent load: 5 virtual users



Each sampler recorded 100 samples with no errors. Endpoint P95 values ranged from 2 to 3 ms.



The update-task sampler had a maximum response time of 45 ms, although its P95 was 3 ms. This is another isolated high-latency observation to monitor in subsequent runs.



\### Concurrent load: 10 virtual users



Each sampler recorded 200 samples with no errors. Endpoint P95 values ranged from 3 to 4 ms.



The health-check and list-tasks samplers had maximum response times of 52 ms and 30 ms, respectively. The remaining operations also showed occasional higher maximums than their P95 values.



\### Concurrent load: 25 virtual users



Each sampler recorded 500 samples with no errors. All six endpoint P95 values were 3 ms.



The highest observed endpoint maximum was 41 ms for the health-check sampler. These results are encouraging for the tested workload, but do not establish capacity under longer or heavier production-like traffic.



\## 6. Analysis and Interpretation



The measured P95 response times were between 3 and 5 ms across all four workloads. Each result is below the project's 500 ms threshold.



The error rate remained at 0% across all 4,920 samples. The results show that the local API completed the recorded test requests successfully under the workloads tested.



Throughput was not monotonic as virtual-user count increased. The analyzer reported 197.69 samples/sec for the one-user baseline, 74.21 for five users, 66.63 for ten users, and 104.08 for 25 users. These values are influenced by the test duration, workload execution, and the analyzer's timing calculation; they should not be interpreted as proof of linear scalability.



The one-user health-check maximum of 94 ms and the 45 ms update-task maximum in the five-user run are examples of latency spikes that are not reflected by P95 alone. Repeating the tests would help determine whether these observations are reproducible.



\## 7. Limitations



\- Testing was performed against a local development environment, not a production deployment.

\- The API uses in-memory storage, so the results do not represent database-backed performance.

\- The test runs were relatively short and do not demonstrate long-duration stability or endurance.

\- CPU, memory, network, and application-resource utilization were not included in the reported measurements.

\- A zero JMeter sample-error rate does not by itself prove that every business rule or returned response body is correct; functional assertions should also be validated.

\- Percentiles are calculated by the project's Python script using linear interpolation. Minor differences from JMeter's dashboard statistics may occur.

\- The 500 ms P95 threshold is a project-defined acceptance criterion.



\## 8. Recommendations



1\. Repeat the baseline and concurrent-load tests to check whether the observed latency spikes recur.

2\. Run a longer steady-state test and a gradual ramp-up test.

3\. Monitor application CPU and memory while tests execute.

4\. Add database-backed testing once persistent storage is integrated.

5\. Compare the Python analyzer's results with JMeter's HTML dashboard and document any calculation differences.

6\. Add explicit response-code and response-body assertions for each API operation.

7\. Increase concurrency gradually to identify where latency, errors, or resource consumption begin to deteriorate.



\## 9. Conclusion



The four recorded local workloads produced 4,920 successful JMeter samples with no recorded sample errors. All four workloads met the project's P95 response-time target of 500 ms.



The results provide a useful baseline for this API and demonstrate a repeatable performance-testing workflow with raw JTL data, automated analysis, and a generated response-time chart. Further testing with longer durations, resource monitoring, and persistent storage is needed before making broader scalability or production-readiness claims.



