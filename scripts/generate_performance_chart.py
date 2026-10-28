
import csv
from pathlib import Path

import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
RESULTS_DIR = ROOT / "results"
OUTPUT_DIR = ROOT / "docs" / "screenshots"
OUTPUT_FILE = OUTPUT_DIR / "p95-response-time.png"

TESTS = [
    ("1 user", "baseline-20-loops.jtl"),
    ("5 users", "load-5-users-20-loops.jtl"),
    ("10 users", "load-10-users-20-loops.jtl"),
    ("25 users", "load-25-users-20-loops.jtl"),
]


def percentile(values, percent):
    """Calculate a percentile using linear interpolation."""
    values = sorted(values)

    if not values:
        raise ValueError("Cannot calculate a percentile without samples.")

    position = (len(values) - 1) * percent / 100
    lower = int(position)
    upper = min(lower + 1, len(values) - 1)
    fraction = position - lower

    return values[lower] + (
        values[upper] - values[lower]
    ) * fraction


def read_elapsed_times(path):
    with path.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        required_columns = {"elapsed", "success"}
        if not reader.fieldnames or not required_columns.issubset(
            reader.fieldnames
        ):
            raise ValueError(
                f"{path.name} is missing required JTL columns."
            )

        samples = [
            int(row["elapsed"])
            for row in reader
            if row["elapsed"] and row["success"].lower() == "true"
        ]

    if not samples:
        raise ValueError(f"No successful samples found in {path.name}")

    return samples


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    labels = []
    p95_values = []

    print("P95 Response-Time Analysis")
    print("-" * 45)

    for label, filename in TESTS:
        path = RESULTS_DIR / filename

        if not path.exists():
            raise FileNotFoundError(f"Missing JTL file: {path}")

        elapsed_times = read_elapsed_times(path)
        p95 = percentile(elapsed_times, 95)

        labels.append(label)
        p95_values.append(p95)

        print(
            f"{label:>8}: {p95:.2f} ms "
            f"({len(elapsed_times)} successful samples)"
        )

    # Use Matplotlib's default colors.
    fig, ax = plt.subplots(figsize=(9, 5.5))

    bars = ax.bar(labels, p95_values, width=0.6)

    ax.axhline(
        y=500,
        linestyle="--",
        linewidth=1.5,
        label="Project target: 500 ms",
    )

    ax.set_title("TaskFlow API — P95 Response Time by Load")
    ax.set_xlabel("Concurrent virtual users")
    ax.set_ylabel("P95 response time (ms)")
    ax.set_ylim(bottom=0, top=max(550, max(p95_values) * 1.25))
    ax.grid(axis="y", alpha=0.25)
    ax.set_axisbelow(True)
    ax.legend()

    ax.bar_label(bars, fmt="%.2f ms", padding=3)
    fig.tight_layout()
    fig.savefig(OUTPUT_FILE, dpi=180, bbox_inches="tight")
    plt.close(fig)

    print(f"\nChart saved to: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
