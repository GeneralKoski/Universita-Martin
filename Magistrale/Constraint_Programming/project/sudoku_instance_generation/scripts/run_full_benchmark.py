#!/usr/bin/env python3

import argparse
import csv
import json
import random
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sudoku_pipeline import generate_puzzle, copy_grid, validate_grid


def main() -> int:
    parser = argparse.ArgumentParser(description="Benchmark completo: strategie x metodi su N griglie")
    parser.add_argument("--source", default="data/solved/sample_solutions.json")
    parser.add_argument("--output-csv", default="results/full_benchmark.csv")
    parser.add_argument("--output-json", default="results/full_benchmark.json")
    parser.add_argument("--backend", choices=["python", "minizinc", "minizinc-api"], default="python")
    parser.add_argument("--optimize-attempts", type=int, default=0)
    parser.add_argument("--optimize-readd", type=int, default=1)
    parser.add_argument("--bnb-nodes", type=int, default=0)
    parser.add_argument("--num-grids", type=int, default=20)
    parser.add_argument("--strategies", nargs="+", default=["random", "symmetry", "density"])
    parser.add_argument("--methods", nargs="+", default=["counting", "solve-and-block"])
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--timeout", type=int, default=None)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    source_path = project_root / args.source
    payload = json.loads(source_path.read_text(encoding="utf-8"))
    grids = payload.get("grids", [])
    if len(grids) < args.num_grids:
        print(f"Solo {len(grids)} griglie disponibili, ne servono {args.num_grids}", file=sys.stderr)
        return 1
    rng = random.Random(args.seed)
    selected = rng.sample(grids, args.num_grids)

    rows = []
    raw_results = []
    total = len(selected) * len(args.strategies) * len(args.methods)
    counter = 0
    start_total = time.time()
    for grid_idx, grid in enumerate(selected):
        validate_grid(grid, allow_zero=False)
        for strategy in args.strategies:
            for method in args.methods:
                counter += 1
                run_seed = args.seed * 1000 + grid_idx
                t0 = time.time()
                result = generate_puzzle(
                    source_grid=copy_grid(grid),
                    backend=args.backend,
                    project_root=project_root,
                    strategy=strategy,
                    timeout_seconds=args.timeout,
                    seed=run_seed,
                    method=method,
                    optimize_attempts=args.optimize_attempts,
                    optimize_readd=args.optimize_readd,
                    bnb_nodes=args.bnb_nodes,
                )
                elapsed = time.time() - t0
                row = {
                    "grid_id": grid_idx,
                    "strategy": strategy,
                    "method": method,
                    "clues": result["clues"],
                    "uniqueness_checks": result["uniqueness_checks"],
                    "accepted_removals": result["accepted_removals"],
                    "total_seconds": round(elapsed, 4),
                    "avg_check_seconds": round(
                        sum(item["elapsed_seconds"] for item in result["removal_log"]) / max(1, len(result["removal_log"])),
                        6,
                    ),
                }
                if args.optimize_attempts > 0:
                    row["clues_before_opt"] = result["optimization"]["clues_before"]
                    row["opt_checks"] = result["optimization"]["uniqueness_checks"]
                if args.bnb_nodes > 0:
                    row["clues_before_bnb"] = result["bnb"]["clues_before"]
                    row["bnb_checks"] = result["bnb"]["uniqueness_checks"]
                rows.append(row)
                raw_results.append({
                    "grid_id": grid_idx,
                    "strategy": strategy,
                    "method": method,
                    "clues": result["clues"],
                    "uniqueness_checks": result["uniqueness_checks"],
                    "accepted_removals": result["accepted_removals"],
                    "total_seconds": round(elapsed, 4),
                    "puzzle": result["puzzle"],
                })
                print(f"[{counter}/{total}] grid={grid_idx} strategy={strategy} method={method} clues={result['clues']} time={elapsed:.2f}s")
    total_elapsed = time.time() - start_total

    csv_path = project_root / args.output_csv
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    with csv_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    json_path = project_root / args.output_json
    json_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.write_text(
        json.dumps(
            {
                "backend": args.backend,
                "num_grids": args.num_grids,
                "strategies": args.strategies,
                "methods": args.methods,
                "seed": args.seed,
                "total_seconds": round(total_elapsed, 2),
                "results": raw_results,
            },
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )

    print(f"\nDone. CSV: {csv_path} | JSON: {json_path} | total: {total_elapsed:.1f}s")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
