# TaskFlow API Performance Test Plan

## 1. Purpose

Evaluate basic API behavior and response-time/throughput observations for the TaskFlow API using Apache JMeter. This plan is designed for a reproducible learning and portfolio exercise, not as a production service-level test.

## 2. Scope

The JMeter test plan exercises these endpoints:

| Sampler | Method | Path | Intended check |
|---|---|---|---|
| GET Health Check | GET | `/health` | API health response |
| GET List Tasks | GET | `/tasks` | List endpoint response |
| POST Create Task | POST | `/tasks` | Create a task and extract its ID |
| GET Task By ID | GET | `/tasks/${taskId}` | Retrieve the created task |
| PUT Update Task | PUT | `/tasks/${taskId}` | Update the created task |
| DELETE Task | DELETE | `/tasks/${taskId}` | Delete the created task |

Verify the actual saved `.jmx` file if samplers or assertions have been changed since the runs documented here.

## 3. Workload profiles

| Profile | Threads (virtual users) | Ramp-up | Loops per user | Expected samples |
|---|---:|---:|---:|---:|
| Baseline | 1 | 1 second | 20 | 120 |
| Load 5 | 5 | 10 seconds | 20 | 600 |
| Load 10 | 10 | 20 seconds | 20 | 1,200 |
| Load 25 | 25 | 30 seconds | 20 | 3,000 |

Expected sample counts assume six enabled samplers execute on every loop. If the plan is modified, recalculate the expectation.

## 4. Preconditions

- FastAPI application starts successfully and remains running throughout a run.
- JMeter can reach `http://127.0.0.1:8000`.
- The test plan uses the intended host and port.
- JSON request samplers have the appropriate `Content-Type: application/json` header.
- POST task creation extracts the returned task ID for subsequent GET, PUT, and DELETE samplers.
- Result filenames are unique and dashboard output directories are empty or new.
- Disable heavyweight GUI listeners such as View Results Tree during command-line load runs.

## 5. Assertions and functional checks

The saved plan was configured with response assertions for the task CRUD flow, including expected status codes such as 201 for create, 200 for read/update, and 204 for delete. Confirm the actual assertions in the JMX file before relying on this description. Check the JMeter HTML report's per-sampler error counts and inspect failed samples if any occur.

## 6. Proposed acceptance criteria

These are project-defined targets for this exercise and are not universal industry standards:

- HTTP/JMeter sample error rate: 0%.
- Functional response assertions: all pass.
- p95 response time: no more than 500 ms for the tested workload.
- The application remains responsive for all configured profiles.

Evaluate each criterion using the actual HTML report. Do not claim the p95 target passed until the report's p95 value has been recorded.

## 7. Execution procedure

1. Start the API.
2. Run the 1-user baseline.
3. Run 5-user, 10-user, and 25-user profiles sequentially.
4. Preserve each `.jtl` file and generated HTML dashboard.
5. Record sample count, average, median, p90, p95, p99, throughput, and error rate.
6. Investigate failed samples and unexpected results.
7. Repeat runs if a result is inconsistent or the environment was interrupted.

## 8. Risks and limitations

- Localhost tests exclude network latency between separate client and server machines.
- Short runs can be affected by process startup, OS scheduling, and other local activity.
- In-memory task storage is not equivalent to a persistent production database.
- Low average latency alone does not establish capacity; percentiles, errors, throughput, and system resource use also matter.
