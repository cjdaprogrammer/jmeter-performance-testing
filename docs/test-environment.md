# Test Environment

## Local setup

| Component | Recorded setup |
|---|---|
| OS | Windows 10/Windows environment |
| Shell | PowerShell |
| Java | OpenJDK 21 |
| Apache JMeter | 5.6.3 |
| Python | 3.11 |
| API framework | FastAPI |
| ASGI server | Uvicorn |
| Test framework | pytest |
| API target | `http://127.0.0.1:8000` |

Confirm the exact OS and runtime versions on the machine before publishing if you want the table to be fully reproducible.

## Start the API

```powershell
.\.venv\Scripts\Activate.ps1
python -m uvicorn app.main:app
```

Keep the server terminal open during the JMeter run.

## Verify the API

Open another PowerShell terminal:

```powershell
Invoke-RestMethod "http://127.0.0.1:8000/health"
```

Expected health payload from the application setup: `status` should be `healthy`.

## Run JMeter

Use the CLI commands in the root README. Run tests sequentially, and use a new `.jtl` filename and empty HTML output directory for every run.

## Reproducibility notes

- Do not run unrelated heavy workloads during measurements.
- Keep the same API code and JMeter plan across compared profiles.
- Record any application restart, code change, machine load, or unexpected warning.
- The API currently uses in-memory storage; restart resets task state.
