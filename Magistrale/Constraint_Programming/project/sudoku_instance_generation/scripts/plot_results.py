#!/usr/bin/env python3

import argparse
import csv
from collections import defaultdict
from pathlib import Path
from statistics import mean

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt


def read_csv(path: Path):
    with path.open("r", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def plot_time_vs_clues(rows, out_path: Path):
    fig, ax = plt.subplots(figsize=(8, 5))
    by_strategy = defaultdict(list)
    for row in rows:
        by_strategy[row["strategy"]].append((int(row["clues"]), float(row["total_seconds"])))
    markers = {"random": "o", "symmetry": "s", "density": "^"}
    for strategy, points in by_strategy.items():
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        ax.scatter(xs, ys, label=strategy, marker=markers.get(strategy, "o"), alpha=0.7, s=40)
    ax.set_xlabel("Remaining clues")
    ax.set_ylabel("Total generation time (seconds)")
    ax.set_title("Generation time vs remaining clues, by strategy")
    ax.legend()
    ax.grid(True, alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_strategy_comparison(rows, out_path: Path):
    by_strategy = defaultdict(list)
    for row in rows:
        by_strategy[row["strategy"]].append(int(row["clues"]))
    strategies = sorted(by_strategy.keys())
    means = [mean(by_strategy[s]) for s in strategies]
    mins = [min(by_strategy[s]) for s in strategies]
    maxs = [max(by_strategy[s]) for s in strategies]

    fig, ax = plt.subplots(figsize=(7, 5))
    x_pos = range(len(strategies))
    ax.bar(x_pos, means, yerr=[[m - lo for m, lo in zip(means, mins)], [hi - m for m, hi in zip(means, maxs)]],
           capsize=6, color=["#4C72B0", "#DD8452", "#55A467"], alpha=0.85)
    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(strategies)
    ax.set_ylabel("Remaining clues (mean, min-max)")
    ax.set_title("Removal strategy vs final clue count")
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_method_comparison(rows, out_path: Path):
    by_method = defaultdict(list)
    for row in rows:
        by_method[row["method"]].append(float(row["avg_check_seconds"]))
    methods = sorted(by_method.keys())
    means = [mean(by_method[m]) * 1000 for m in methods]

    fig, ax = plt.subplots(figsize=(6, 5))
    ax.bar(methods, means, color=["#4C72B0", "#DD8452"], alpha=0.85)
    ax.set_ylabel("Mean time per uniqueness check (ms)")
    ax.set_title("Method comparison: counting vs solve-and-block")
    ax.grid(True, axis="y", alpha=0.3)
    for i, v in enumerate(means):
        ax.text(i, v, f"{v:.2f} ms", ha="center", va="bottom")
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def plot_optimization(rows, out_path: Path):
    pairs = sorted(
        ((int(row["grid_id"]), int(row["clues_before_opt"]), int(row["clues"])) for row in rows),
        key=lambda item: item[0],
    )
    grid_ids = [p[0] for p in pairs]
    before = [p[1] for p in pairs]
    after = [p[2] for p in pairs]

    fig, ax = plt.subplots(figsize=(max(8, len(grid_ids) * 0.3), 5))
    x_pos = range(len(grid_ids))
    width = 0.4
    ax.bar([x - width / 2 for x in x_pos], before, width, label="greedy only", color="#4C72B0", alpha=0.85)
    ax.bar([x + width / 2 for x in x_pos], after, width, label="greedy + optimization", color="#DD8452", alpha=0.85)
    ax.axhline(17, color="#555", linestyle="--", linewidth=1, label="theoretical minimum (17)")
    ax.set_xticks(list(x_pos))
    ax.set_xticklabels(grid_ids)
    ax.set_xlabel("Grid id")
    ax.set_ylabel("Remaining clues")
    ax.set_ylim(15, None)
    ax.set_title("Clue count before/after removal optimization (random, counting)")
    ax.legend()
    ax.grid(True, axis="y", alpha=0.3)
    fig.tight_layout()
    fig.savefig(out_path, dpi=150)
    plt.close(fig)


def main() -> int:
    parser = argparse.ArgumentParser(description="Genera i grafici dal benchmark CSV")
    parser.add_argument("--input", default="results/full_benchmark.csv")
    parser.add_argument("--optimization-input", default="results/optimization_benchmark.csv")
    parser.add_argument("--output-dir", default="report/assets")
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    csv_path = project_root / args.input
    out_dir = project_root / args.output_dir
    out_dir.mkdir(parents=True, exist_ok=True)

    rows = read_csv(csv_path)
    if not rows:
        print(f"Nessuna riga trovata in {csv_path}")
        return 1

    plot_time_vs_clues(rows, out_dir / "plot_time_vs_clues.png")
    plot_strategy_comparison(rows, out_dir / "plot_strategy_comparison.png")
    plot_method_comparison(rows, out_dir / "plot_method_comparison.png")

    opt_path = project_root / args.optimization_input
    if opt_path.exists():
        plot_optimization(read_csv(opt_path), out_dir / "plot_optimization.png")

    print(f"Grafici salvati in {out_dir}/")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
