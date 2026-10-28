\# TaskFlow API Performance Testing with Apache JMeter



A QA portfolio project demonstrating API functional testing and performance testing using Apache JMeter, FastAPI, and pytest.



\## Project Objectives



\- Test API health and task CRUD endpoints with a reusable JMeter test plan.

\- Execute baseline and concurrent-user performance tests.

\- Generate JMeter HTML dashboards and analyze raw JTL results.

\- Document test scope, acceptance criteria, findings, limitations, and recommendations.

\- Automate performance-result analysis and generate a response-time chart.



\## Technology Stack



\- Apache JMeter 5.6.3

\- Java 21

\- Python 3.11

\- FastAPI and Uvicorn

\- pytest

\- Matplotlib



\## Performance Test Summary



Four workloads were executed against the local TaskFlow API, with 20 loops per virtual user.



| Virtual users | Samples | Average response time | P95 response time | Errors |

|---:|---:|---:|---:|---:|

| 1 | 120 | 3.83 ms | 5 ms | 0 |

| 5 | 600 | 1.69 ms | 3 ms | 0 |

| 10 | 1,200 | 2.19 ms | 4 ms | 0 |

| 25 | 3,000 | 1.71 ms | 3 ms | 0 |

| \*\*Total\*\* | \*\*4,920\*\* | â€” | â€” | \*\*0\*\* |



The project-defined acceptance criterion is an overall P95 response time of 500 ms or less. All four recorded workloads met this criterion.



\### P95 Response-Time Chart



!\[TaskFlow API P95 response time by load](docs/screenshots/p95-response-time.png)



\### Key Observations



\- All 4,920 recorded samples completed successfully in the analyzed runs.

\- The calculated overall P95 response times ranged from 3 to 5 ms.

\- The single-user run included a 94 ms maximum response time for the health-check sampler. Its cause has not been established.

\- Throughput did not increase consistently at every workload level.



These are short-duration measurements against a local API using in-memory storage. They do not establish production capacity or guarantee performance under sustained or distributed load.



\## Repository Structure



```text

jmeter-performance-testing/

â”œâ”€â”€ app/                 # FastAPI application

â”œâ”€â”€ tests/               # pytest API tests

â”œâ”€â”€ test-plans/          # JMeter test plans

â”œâ”€â”€ test-data/           # Optional test data

â”œâ”€â”€ results/             # Local raw JTL results (ignored by Git)

â”œâ”€â”€ reports/             # Local generated dashboards (ignored by Git)

â”œâ”€â”€ docs/

â”‚   â”œâ”€â”€ screenshots/

â”‚   â”‚   â””â”€â”€ p95-response-time.png

â”‚   â”œâ”€â”€ test-plan.md

â”‚   â”œâ”€â”€ performance-test-report.md

â”‚   â”œâ”€â”€ performance-analysis.md

â”‚   â””â”€â”€ test-environment.md

â”œâ”€â”€ scripts/

â”‚   â”œâ”€â”€ analyze\_jmeter\_results.py

â”‚   â””â”€â”€ generate\_performance\_chart.py

â”œâ”€â”€ requirements.txt

â””â”€â”€ README.md

```



\## Setup



Activate your virtual environment in PowerShell:



```powershell

.\\.venv\\Scripts\\Activate.ps1

```



Install dependencies:



```powershell

python -m pip install -r requirements.txt

```



\## Start the API



From the project root:



```powershell

python -m uvicorn app.main:app

```



The API should be available at `http://127.0.0.1:8000`. Keep the API running in its own terminal during JMeter tests.



\## Run Functional API Tests



```powershell

python -m pytest -v

```



The current functional test suite contains 11 tests covering health checks and task CRUD behavior, including missing-resource and invalid-title cases.



\## Run JMeter Tests



The test plan is `test-plans/taskflow-baseline.jmx`.



Example: baseline with one virtual user:



```powershell

\& "$env:USERPROFILE\\Downloads\\apache-jmeter-5.6.3\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -n -t "test-plans\\taskflow-baseline.jmx" -Jthreads=1 -Jrampup=1 -Jloops=20 -l "results\\baseline-20-loops.jtl" -e -o "reports\\baseline-20-loops"

```



Example: 25 virtual users:



```powershell

\& "$env:USERPROFILE\\Downloads\\apache-jmeter-5.6.3\\apache-jmeter-5.6.3\\bin\\jmeter.bat" -n -t "test-plans\\taskflow-baseline.jmx" -Jthreads=25 -Jrampup=30 -Jloops=20 -l "results\\load-25-users-20-loops.jtl" -e -o "reports\\load-25-users-20-loops"

```



The test plan supports configurable thread count, ramp-up, and loop count. Use a unique JTL output file and an empty report directory for each run. The examples assume the default JMeter installation path shown above; adjust it if necessary.



To open a generated dashboard:



```powershell

Start-Process ".\\reports\\load-25-users-20-loops\\index.html"

```



\## Analyze Results and Generate the Chart



After the corresponding JTL files have been generated:



```powershell

python .\\scripts\\analyze\_jmeter\_results.py

python .\\scripts\\generate\_performance\_chart.py

```



The analysis script reports overall and per-sampler metrics. The chart-generation script calculates P95 response times from the raw JTL files and writes `docs/screenshots/p95-response-time.png`.



\## Documentation



\- \[Performance analysis](docs/performance-analysis.md)

\- \[Performance test plan](docs/test-plan.md)

\- \[Performance test report](docs/performance-test-report.md)

\- \[Test environment](docs/test-environment.md)

\- \[JMeter result analysis script](scripts/analyze\_jmeter\_results.py)

\- \[Chart generation script](scripts/generate\_performance\_chart.py)



\## Limitations



\- The API uses in-memory storage, so data resets when the application process restarts.

\- Localhost testing does not represent real network latency or a production deployment.

\- Short runs do not establish endurance stability or maximum safe concurrency.

\- The 500 ms threshold is a project-defined target, not an externally validated service-level objective.

\- Zero recorded sample errors should be evaluated alongside response assertions and per-sampler results.



This project demonstrates a reproducible introduction to API performance testing. Longer-duration, monitored, database-backed, and distributed tests would be needed before drawing conclusions about production scalability.
