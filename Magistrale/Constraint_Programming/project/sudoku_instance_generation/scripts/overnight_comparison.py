#!/usr/bin/env python3

"""Long-running comparison of the four removal optimisers on many grids.

For each sampled complete grid it records the final clue count reached by:
  - greedy          : plain greedy removal with rollback (baseline)
  - v1              : iterated local search, re-add 1 clue per perturbation
  - vns             : variable-neighbourhood local search, re-add up to 3
  - bnb             : node-bounded branch-and-bound, warm-started from vns

The run is time-bounded (default 10 hours): it keeps processing grids until the
wall-clock budget is spent, then stops and writes a summary. Every grid's row is
flushed to the CSV immediately, so partial results survive an interruption.
"""

import argparse
import csv
import itertools
import json
import random
import signal
import statistics
import sys
import time
from multiprocessing import Pool, cpu_count
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sudoku_pipeline import generate_puzzle, copy_grid

_STOP = {"flag": False}


def _request_stop(signum, frame) -> None:
    _STOP["flag"] = True


def process_grid(task: tuple) -> dict:
    """Run the four optimisers on one grid. Top-level so it is picklable for the pool."""
    idx, grid, seed, project_root_str, attempts, readd, bnb_nodes = task
    project_root = Path(project_root_str)

    def run(**kw):
        t0 = time.time()
        res = generate_puzzle(
            source_grid=copy_grid(grid), backend="python", project_root=project_root,
            strategy="random", timeout_seconds=None, seed=seed, method="counting", **kw,
        )
        return res, round(time.time() - t0, 1)

    base, t0 = run()
    r1, t1 = run(optimize_attempts=attempts, optimize_readd=1)
    r3, t3 = run(optimize_attempts=attempts, optimize_readd=readd)
    rb, tb = run(optimize_attempts=attempts, optimize_readd=readd, bnb_nodes=bnb_nodes)
    return {
        "grid_id": idx,
        "greedy": base["clues"], "v1": r1["clues"], "vns": r3["clues"], "bnb": rb["clues"],
        "t_greedy": t0, "t_v1": t1, "t_vns": t3, "t_bnb": tb,
        "bnb_improvements": rb.get("bnb", {}).get("improvements", 0),
    }


HEADER_BYTES = 16
ROW_BYTES = 164  # "puzzle(81),solution(81)\n"


def kaggle_row_count(path: Path) -> int:
    return (path.stat().st_size - HEADER_BYTES) // ROW_BYTES


def read_solution_grid(fh, row_idx: int) -> list:
    """Read the complete (solution) grid at a given Kaggle row via random seek."""
    fh.seek(HEADER_BYTES + row_idx * ROW_BYTES)
    line = fh.read(163)  # puzzle(81) + "," + solution(81)
    solution = line.split(",")[1]
    return [[int(ch) for ch in solution[r * 9:(r + 1) * 9]] for r in range(9)]


def summarize(rows: list) -> dict:
    summary = {"grids": len(rows)}
    for key in ("greedy", "v1", "vns", "bnb"):
        vals = [int(r[key]) for r in rows]
        dist = {}
        for v in vals:
            dist[v] = dist.get(v, 0) + 1
        summary[key] = {
            "mean": round(statistics.mean(vals), 3),
            "min": min(vals),
            "max": max(vals),
            "stdev": round(statistics.stdev(vals), 3) if len(vals) > 1 else 0.0,
            "distribution": {str(k): dist[k] for k in sorted(dist)},
        }
    summary["bnb_beat_vns"] = sum(1 for r in rows if int(r["bnb"]) < int(r["vns"]))
    summary["vns_beat_v1"] = sum(1 for r in rows if int(r["vns"]) < int(r["v1"]))
    return summary


def summarize_existing(csv_path: Path) -> int:
    with csv_path.open(encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    if not rows:
        print(f"No rows in {csv_path}")
        return 1
    summary = summarize(rows)
    print(json.dumps(summary, indent=2))
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description="Overnight optimiser comparison")
    parser.add_argument("--source", default="data/solved/sample_solutions_1000.json")
    parser.add_argument("--source-raw", default=None, help="sample fresh complete grids by random seek into the 9M-row Kaggle CSV; runs unbounded until stopped")
    parser.add_argument("--output-csv", default="results/overnight_comparison.csv")
    parser.add_argument("--output-json", default="results/overnight_comparison.json")
    parser.add_argument("--hours", type=float, default=48.0, help="safety cap; the run is meant to be stopped on demand (Ctrl-C / SIGTERM), saving partial results")
    parser.add_argument("--attempts", type=int, default=100)
    parser.add_argument("--readd", type=int, default=3)
    parser.add_argument("--bnb-nodes", type=int, default=8000)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--workers", type=int, default=0, help="parallel processes (0 = auto: cpu_count-2; 1 = sequential)")
    parser.add_argument("--summarize-csv", default=None, help="skip the run; just print/save the summary of an existing CSV")
    args = parser.parse_args()

    if args.summarize_csv:
        return summarize_existing(Path(args.summarize_csv))

    signal.signal(signal.SIGINT, _request_stop)
    signal.signal(signal.SIGTERM, _request_stop)

    project_root = Path(__file__).resolve().parents[1]
    budget = args.hours * 3600.0

    raw_mode = args.source_raw is not None
    if raw_mode:
        raw_path = project_root / args.source_raw
        n_rows = kaggle_row_count(raw_path)
        raw_fh = raw_path.open("r", encoding="utf-8")
        rng = random.Random()  # OS-seeded: fresh rows every launch
    else:
        grids = json.loads((project_root / args.source).read_text(encoding="utf-8"))["grids"]

    csv_path = project_root / args.output_csv
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = [
        "grid_id", "greedy", "v1", "vns", "bnb",
        "t_greedy", "t_v1", "t_vns", "t_bnb", "bnb_improvements", "elapsed_total",
    ]
    fh = csv_path.open("w", newline="", encoding="utf-8")
    writer = csv.DictWriter(fh, fieldnames=fieldnames)
    writer.writeheader()
    fh.flush()

    workers = args.workers if args.workers > 0 else max(1, cpu_count() - 2)
    common = (str(project_root), args.attempts, args.readd, args.bnb_nodes)

    def make_tasks():
        if raw_mode:
            while True:  # unbounded: a fresh random Kaggle row each time
                row_idx = rng.randrange(n_rows)
                yield (row_idx, read_solution_grid(raw_fh, row_idx), args.seed * 1000 + row_idx, *common)
        else:
            for i in range(len(grids)):
                yield (i, grids[i], args.seed * 1000 + i, *common)

    label = f"fresh grids from {args.source_raw} (unbounded)" if raw_mode else f"{len(grids)} grids"
    print(f"Running {label} on {workers} worker(s); stop with Ctrl-C / SIGTERM.", flush=True)

    rows = []
    start = time.time()
    done = 0

    def record(row: dict) -> None:
        nonlocal done
        row["elapsed_total"] = round(time.time() - start, 1)
        rows.append(row)
        writer.writerow(row)
        fh.flush()
        done += 1
        print(f"[{done}] elapsed={row['elapsed_total']:.0f}s  grid={row['grid_id']}  greedy={row['greedy']} v1={row['v1']} vns={row['vns']} bnb={row['bnb']}", flush=True)

    def stop_now() -> bool:
        return _STOP["flag"] or (time.time() - start) >= budget

    if workers == 1:
        for task in make_tasks():
            if stop_now():
                break
            record(process_grid(task))
    else:
        batch_size = max(8, workers * 4)
        gen = make_tasks()
        with Pool(workers) as pool:
            while not stop_now():
                batch = list(itertools.islice(gen, batch_size))
                if not batch:
                    break  # finite source exhausted
                for row in pool.imap_unordered(process_grid, batch):
                    record(row)
                    if stop_now():
                        break
                if stop_now():
                    pool.terminate()
                    break

    fh.close()
    if raw_mode:
        raw_fh.close()

    summary = {"hours_requested": args.hours, "elapsed_seconds": round(time.time() - start, 1), "stopped_early": _STOP["flag"], "params": {"attempts": args.attempts, "readd": args.readd, "bnb_nodes": args.bnb_nodes, "seed": args.seed}}
    summary.update(summarize(rows) if rows else {"grids": 0})
    (project_root / args.output_json).write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print(f"\nDone. {len(rows)} grids in {summary['elapsed_seconds']:.0f}s (stopped_early={_STOP['flag']}). Summary: {project_root / args.output_json}", flush=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
