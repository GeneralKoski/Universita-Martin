#!/usr/bin/env python3

import argparse
import csv
import json
import random
from pathlib import Path


def parse_grid(text: str) -> list[list[int]]:
    text = text.strip()
    if len(text) != 81 or any(ch not in "123456789" for ch in text):
        raise ValueError("Ogni soluzione deve contenere esattamente 81 cifre 1..9")
    values = [int(ch) for ch in text]
    return [values[row * 9 : (row + 1) * 9] for row in range(9)]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estrae un sottoinsieme di soluzioni complete dal Kaggle Sudoku Dataset"
    )
    parser.add_argument("--input", default="data/raw/sudoku.csv")
    parser.add_argument("--output", default="data/solved/sample_solutions.json")
    parser.add_argument("--limit", type=int, default=50)
    parser.add_argument("--seed", type=int, default=42)
    args = parser.parse_args()

    project_root = Path(__file__).resolve().parents[1]
    input_path = project_root / args.input
    output_path = project_root / args.output

    rng = random.Random(args.seed)
    reservoir: list[str] = []
    seen: set[str] = set()
    total_rows = 0

    with input_path.open("r", encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        if "solution" not in (reader.fieldnames or []):
            raise ValueError("CSV Kaggle non valido: colonna 'solution' mancante")
        for row in reader:
            total_rows += 1
            solution = row["solution"].strip()
            if solution in seen:
                continue
            if len(reservoir) < args.limit:
                reservoir.append(solution)
                seen.add(solution)
                continue
            idx = rng.randint(0, total_rows - 1)
            if idx < args.limit:
                old = reservoir[idx]
                seen.discard(old)
                reservoir[idx] = solution
                seen.add(solution)

    grids = [parse_grid(solution) for solution in reservoir]
    payload = {
        "source": "Kaggle Sudoku Dataset (rohanrao/sudoku)",
        "raw_file": str(input_path.relative_to(project_root)),
        "seed": args.seed,
        "count": len(grids),
        "grids": grids,
    }
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")

    print(
        f"Estratte {len(grids)} griglie complete da {input_path} "
        f"e salvate in {output_path}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
