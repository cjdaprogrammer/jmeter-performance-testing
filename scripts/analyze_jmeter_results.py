import csv
import math
from pathlib import Path
from collections import defaultdict

RESULTS = Path("results")
FILES = [
    "baseline-20-loops.jtl",
    "load-5-users-20-loops.jtl",
    "load-10-users-20-loops.jtl",
    "load-25-users-20-loops.jtl",
]

def percentile(values, p):
    values = sorted(values)
    if not values:
        return 0
    position = (len(values) - 1) * p
    lower = math.floor(position)
    upper = math.ceil(position)
    if lower == upper:
        return values[lower]
    return values[lower] + (values[upper] - values[lower]) * (position - lower)

def load_samples(filename):
    path = RESULTS / filename
    with path.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        raise ValueError(f"No samples found in {path}")
    return rows

def summarize(rows):
    elapsed = [int(row["elapsed"]) for row in rows]
    failures = sum(row["success"].strip().lower() != "true" for row in rows)
    starts = [int(row["timeStamp"]) for row in rows]
    ends = [int(row["timeStamp"]) + int(row["elapsed"]) for row in rows]
    duration = (max(ends) - min(starts)) / 1000
    return {
        "samples": len(rows),
        "errors": failures,
        "error_pct": failures / len(rows) * 100,
        "avg": sum(elapsed) / len(elapsed),
        "min": min(elapsed),
        "p90": percentile(elapsed, 0.90),
        "p95": percentile(elapsed, 0.95),
        "p99": percentile(elapsed, 0.99),
        "max": max(elapsed),
        "duration": duration,
        "throughput": len(rows) / duration if duration > 0 else 0,
    }

print("JMeter Performance Results")
print("=" * 115)

for filename in FILES:
    rows = load_samples(filename)
    overall = summarize(rows)
    print(f"\nTEST: {filename}")
    print(
        f"Samples={overall['samples']} | Errors={overall['errors']} "
        f"({overall['error_pct']:.2f}%) | Duration={overall['duration']:.2f}s"
    )
    print(
        f"Avg={overall['avg']:.2f} ms | Min={overall['min']} ms | "
        f"P90={overall['p90']:.2f} ms | P95={overall['p95']:.2f} ms | "
        f"P99={overall['p99']:.2f} ms | Max={overall['max']} ms | "
        f"Throughput={overall['throughput']:.2f} samples/sec"
    )
    print(f"P95 target <= 500 ms: {'PASS' if overall['p95'] <= 500 else 'FAIL'}")

    grouped = defaultdict(list)
    for row in rows:
        grouped[row["label"]].append(row)

    print("\n  Endpoint breakdown:")
    print("  {:<25} {:>7} {:>8} {:>9} {:>9} {:>9} {:>9}".format(
        "Sampler", "Samples", "Errors", "Avg(ms)", "P95(ms)", "P99(ms)", "Max(ms)"
    ))
    for label, samples in grouped.items():
        result = summarize(samples)
        print("  {:<25} {:>7} {:>8} {:>9.2f} {:>9.2f} {:>9.2f} {:>9}".format(
            label[:25], result["samples"], result["errors"],
            result["avg"], result["p95"], result["p99"], result["max"]
        ))
