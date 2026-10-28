# TaskFlow API Performance Testing with Apache JMeter

A portfolio project demonstrating API functional checks and performance testing with Apache JMeter, FastAPI, and pytest.

## Project objectives

- Exercise TaskFlow API health and task CRUD endpoints with a reusable JMeter test plan.
- Run baseline and concurrent-user tests.
- Generate JMeter HTML dashboards and retain raw `.jtl` results.
- Document workload settings, observed results, limitations, and follow-up recommendations.

## Technology stack

- Apache JMeter 5.6.3
- Java 21
- Python 3.11
- FastAPI and Uvicorn
- pytest

> Update the versions above if your installed versions differ. The recorded test results are from a local Windows environment.

## Repository layout

```text
jmeter-performance-testing/
├── app/                 # FastAPI application
├── tests/               # pytest API tests
├── test-plans/          # JMeter .jmx test plans
├── test-data/           # Optional test data
├── results/             # Raw JMeter .jtl result files
├── reports/             # Generated JMeter HTML dashboards
├── docs/
│   ├── test-plan.md
│   ├── performance-test-report.md
│   └── test-environment.md
├── scripts/             # Optional helper scripts
├── requirements.txt
└── README.md
```

## Start the API

From the project root in PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app
```

The API should be reachable at `http://127.0.0.1:8000`. Keep this terminal running while JMeter executes.

## Run the pytest checks

```powershell
python -m pytest -v
```

## Run JMeter from the command line

The current test plan is `test-plans\taskflow-baseline.jmx`. Adjust the JMeter executable path if you installed it elsewhere.

### Baseline: 1 virtual user

```powershell
& "$env:USERPROFILE\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t "test-plans\taskflow-baseline.jmx" -Jthreads=1 -Jrampup=1 -Jloops=20 -l "results\baseline-20-loops.jtl" -e -o "reports\baseline-20-loops"
```

### 5 virtual users

```powershell
& "$env:USERPROFILE\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t "test-plans\taskflow-baseline.jmx" -Jthreads=5 -Jrampup=10 -Jloops=20 -l "results\load-5-users-20-loops.jtl" -e -o "reports\load-5-users-20-loops"
```

### 10 virtual users

```powershell
& "$env:USERPROFILE\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t "test-plans\taskflow-baseline.jmx" -Jthreads=10 -Jrampup=20 -Jloops=20 -l "results\load-10-users-20-loops.jtl" -e -o "reports\load-10-users-20-loops"
```

### 25 virtual users

```powershell
& "$env:USERPROFILE\Downloads\apache-jmeter-5.6.3\apache-jmeter-5.6.3\bin\jmeter.bat" -n -t "test-plans\taskflow-baseline.jmx" -Jthreads=25 -Jrampup=30 -Jloops=20 -l "results\load-25-users-20-loops.jtl" -e -o "reports\load-25-users-20-loops"
```

Run each command separately. Each `-l` result file should be unique, and each `-o` report directory must not already contain files. If a report directory already exists, choose a new directory name or clear the old generated report after preserving anything you need.

## View a generated dashboard

```powershell
Start-Process ".\reports\load-25-users-20-loops\index.html"
```

Review the Statistics table and dashboard charts. Record average, median, p90, p95, p99, throughput, and error percentage. Do not infer percentiles from the console summary.

## Current recorded results

The console summaries for the extended runs reported:

| Virtual users | Loops/user | Samples | Average (ms) | Min (ms) | Max (ms) | Throughput (requests/s) | Errors |
|---:|---:|---:|---:|---:|---:|---:|---:|
| 1 | 20 | 120 | 3 | 1 | 94 | 164.2 | 0 (0.00%) |
| 5 | 20 | 600 | 1 | 0 | 45 | 73.2 | 0 (0.00%) |
| 10 | 20 | 1,200 | 2 | 0 | 52 | 65.9 | 0 (0.00%) |
| 25 | 20 | 3,000 | 1 | 0 | 41 | 103.5 | 0 (0.00%) |

These values are copied from the JMeter console summaries and are rounded. They are preliminary local-test observations, not a production capacity claim. The single-user run is short, and throughput is not monotonic across load levels. Add the detailed HTML dashboard percentiles before deciding whether latency acceptance criteria were met.

## Important limitations

- The API uses in-memory data, so state resets when the application process restarts.
- Results depend on the local machine, runtime, server process, test data, and workload.
- This is a small local test, not a production-scale or distributed load test.
- A zero JMeter sample-error rate should be checked alongside response assertions and the dashboard's per-sampler results.
- Do not commit secrets, environment files, virtual environments, caches, or unnecessary large generated files.

## Documentation

- [Test plan](docs/test-plan.md)
- [Performance test report](docs/performance-test-report.md)
- [Test environment](docs/test-environment.md)
