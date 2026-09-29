#!/usr/bin/env python3

import argparse
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path
from typing import List, Optional, Tuple

Grid = List[List[int]]


def read_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(data, handle, indent=2)
        handle.write("\n")


def format_grid(grid: Grid) -> str:
    rows = []
    for r in range(9):
        blocks = [" ".join(str(grid[r][c]) if grid[r][c] else "." for c in range(s, s + 3)) for s in (0, 3, 6)]
        rows.append(" | ".join(blocks))
        if r in (2, 5):
            rows.append("- - - + - - - + - - -")
    return "\n".join(rows)


def validate_grid(grid: Grid, allow_zero: bool) -> None:
    if len(grid) != 9 or any(len(row) != 9 for row in grid):
        raise ValueError("La griglia deve essere 9x9")
    for row in grid:
        for value in row:
            if allow_zero:
                ok = 0 <= value <= 9
            else:
                ok = 1 <= value <= 9
            if not ok:
                raise ValueError("Valori non validi nella griglia")


def copy_grid(grid: Grid) -> Grid:
    return [row[:] for row in grid]


def find_empty(grid: Grid) -> Optional[Tuple[int, int]]:
    best: Optional[Tuple[int, int]] = None
    best_len = 10
    for r in range(9):
        for c in range(9):
            if grid[r][c] != 0:
                continue
            choices = candidate_values(grid, r, c)
            if not choices:
                return (r, c)
            if len(choices) < best_len:
                best = (r, c)
                best_len = len(choices)
                if best_len == 1:
                    return best
    return best


def candidate_values(grid: Grid, row: int, col: int) -> List[int]:
    if grid[row][col] != 0:
        return []
    used = set(grid[row])
    used.update(grid[r][col] for r in range(9))
    br = (row // 3) * 3
    bc = (col // 3) * 3
    for r in range(br, br + 3):
        for c in range(bc, bc + 3):
            used.add(grid[r][c])
    return [value for value in range(1, 10) if value not in used]


def solve_python(grid: Grid, rng: Optional[random.Random] = None) -> Optional[Grid]:
    work = copy_grid(grid)

    def backtrack() -> bool:
        cell = find_empty(work)
        if cell is None:
            return True
        row, col = cell
        values = candidate_values(work, row, col)
        if rng is not None:
            rng.shuffle(values)
        for value in values:
            work[row][col] = value
            if backtrack():
                return True
            work[row][col] = 0
        return False

    return work if backtrack() else None


def count_solutions_python(grid: Grid, limit: int = 2) -> Tuple[int, Optional[Grid]]:
    work = copy_grid(grid)
    found = 0
    first_solution: Optional[Grid] = None

    def backtrack() -> None:
        nonlocal found, first_solution
        if found >= limit:
            return
        cell = find_empty(work)
        if cell is None:
            found += 1
            if first_solution is None:
                first_solution = copy_grid(work)
            return
        row, col = cell
        for value in candidate_values(work, row, col):
            work[row][col] = value
            backtrack()
            work[row][col] = 0
            if found >= limit:
                return

    backtrack()
    return found, first_solution


def solve_excluding_python(grid: Grid, forbidden: Grid) -> Optional[Grid]:
    work = copy_grid(grid)

    def backtrack() -> bool:
        cell = find_empty(work)
        if cell is None:
            if any(work[r][c] != forbidden[r][c] for r in range(9) for c in range(9)):
                return True
            return False
        row, col = cell
        for value in candidate_values(work, row, col):
            work[row][col] = value
            if backtrack():
                return True
            work[row][col] = 0
        return False

    return work if backtrack() else None


def puzzle_status_python(grid: Grid, method: str = "counting") -> dict:
    start = time.time()
    if method == "counting":
        count, solution = count_solutions_python(grid, limit=2)
        elapsed = time.time() - start
        if count == 0:
            status = "unsat"
        elif count == 1:
            status = "unique"
        else:
            status = "multiple"
        return {
            "status": status,
            "solutions_found": count,
            "elapsed_seconds": elapsed,
            "solution": solution,
            "method": "counting",
        }
    if method == "solve-and-block":
        first = solve_python(grid)
        if first is None:
            return {
                "status": "unsat",
                "solutions_found": 0,
                "elapsed_seconds": time.time() - start,
                "solution": None,
                "method": "solve-and-block",
            }
        second = solve_excluding_python(grid, first)
        elapsed = time.time() - start
        if second is None:
            return {
                "status": "unique",
                "solutions_found": 1,
                "elapsed_seconds": elapsed,
                "solution": first,
                "method": "solve-and-block",
            }
        return {
            "status": "multiple",
            "solutions_found": 2,
            "elapsed_seconds": elapsed,
            "solution": first,
            "method": "solve-and-block",
        }
    raise ValueError(f"Metodo di unicità non supportato: {method}")


_MZN_API_CACHE: dict = {}


def minizinc_api_instance(project_root: Path):
    import minizinc

    key = str(project_root)
    if key not in _MZN_API_CACHE:
        solver = minizinc.Solver.load(project_root / "spec" / "gecode_local.msc")
        model = minizinc.Model(project_root / "models" / "sudoku_solver.mzn")
        _MZN_API_CACHE[key] = (solver, model)
    solver, model = _MZN_API_CACHE[key]
    return minizinc.Instance(solver, model)


def minizinc_api_timeout(timeout_seconds: Optional[int]):
    from datetime import timedelta

    return timedelta(seconds=timeout_seconds) if timeout_seconds is not None else None


def grid_from_api_solution(solution) -> Grid:
    return [[int(value) for value in row] for row in solution.grid]


def puzzle_status_minizinc_api_counting(
    project_root: Path, grid: Grid, timeout_seconds: Optional[int]
) -> dict:
    import minizinc

    start = time.time()
    instance = minizinc_api_instance(project_root)
    instance["clues"] = grid
    result = instance.solve(nr_solutions=2, timeout=minizinc_api_timeout(timeout_seconds))
    elapsed = time.time() - start
    solutions = [grid_from_api_solution(item) for item in (result.solution or [])]
    if result.status == minizinc.Status.UNSATISFIABLE:
        status = "unsat"
    elif len(solutions) >= 2:
        status = "multiple"
    elif len(solutions) == 1 and result.status == minizinc.Status.ALL_SOLUTIONS:
        status = "unique"
    else:
        status = "unknown"
    return {
        "status": status,
        "solutions_found": len(solutions),
        "elapsed_seconds": elapsed,
        "solution": solutions[0] if solutions else None,
        "method": "counting",
    }


def puzzle_status_minizinc_api_solve_and_block(
    project_root: Path, grid: Grid, timeout_seconds: Optional[int]
) -> dict:
    import minizinc

    start = time.time()
    timeout = minizinc_api_timeout(timeout_seconds)
    instance = minizinc_api_instance(project_root)
    instance["clues"] = grid
    result = instance.solve(timeout=timeout)
    if result.status == minizinc.Status.UNSATISFIABLE:
        return {
            "status": "unsat",
            "solutions_found": 0,
            "elapsed_seconds": time.time() - start,
            "solution": None,
            "method": "solve-and-block",
        }
    if result.solution is None:
        return {
            "status": "unknown",
            "solutions_found": 0,
            "elapsed_seconds": time.time() - start,
            "solution": None,
            "method": "solve-and-block",
        }
    solution = grid_from_api_solution(result.solution)
    blocking = " \\/ ".join(
        f"grid[{r + 1},{c + 1}] != {solution[r][c]}" for r in range(9) for c in range(9)
    )
    with instance.branch() as child:
        child.add_string(f"constraint {blocking};")
        second = child.solve(timeout=timeout)
    if second.solution is not None:
        status = "multiple"
        solutions_found = 2
    elif second.status == minizinc.Status.UNSATISFIABLE:
        status = "unique"
        solutions_found = 1
    else:
        status = "unknown"
        solutions_found = 1
    return {
        "status": status,
        "solutions_found": solutions_found,
        "elapsed_seconds": time.time() - start,
        "solution": solution,
        "method": "solve-and-block",
    }


def puzzle_status_minizinc_api(
    project_root: Path,
    grid: Grid,
    timeout_seconds: Optional[int],
    method: str = "counting",
) -> dict:
    if method == "counting":
        return puzzle_status_minizinc_api_counting(project_root, grid, timeout_seconds)
    if method == "solve-and-block":
        return puzzle_status_minizinc_api_solve_and_block(project_root, grid, timeout_seconds)
    raise ValueError(f"Metodo di unicità non supportato: {method}")


def board_to_dzn(name: str, grid: Grid) -> str:
    flat = ", ".join(str(value) for row in grid for value in row)
    return f"{name} = array2d(1..9, 1..9, [{flat}]);\n"


def run_minizinc(
    model: Path,
    dzn_text: str,
    timeout_seconds: Optional[int],
    extra_flags: Optional[List[str]] = None,
) -> subprocess.CompletedProcess:
    if shutil.which("minizinc") is None:
        raise RuntimeError("Il comando 'minizinc' non è disponibile nel PATH")
    project_root = model.parents[1]
    solver_config = project_root / "spec" / "gecode_local.msc"
    tmp_dir = project_root / "results"
    tmp_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.NamedTemporaryFile("w", suffix=".dzn", dir=tmp_dir, delete=False, encoding="utf-8") as handle:
        handle.write(dzn_text)
        temp_dzn = handle.name
    try:
        cmd = ["minizinc", "--solver", str(solver_config)]
        if extra_flags:
            cmd.extend(extra_flags)
        cmd.extend([str(model), temp_dzn])
        if timeout_seconds is not None:
            cmd.extend(["--time-limit", str(timeout_seconds * 1000)])
        return subprocess.run(
            cmd,
            text=True,
            capture_output=True,
            check=False,
        )
    finally:
        try:
            os.unlink(temp_dzn)
        except FileNotFoundError:
            pass


def parse_minizinc_grid(output: str) -> Optional[Grid]:
    rows = []
    for raw_line in output.strip().splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("----------") or line.startswith("=========="):
            continue
        if "UNSATISFIABLE" in line or "UNKNOWN" in line or "ERROR" in line:
            continue
        values = [int(token) for token in line.split()]
        if len(values) == 9:
            rows.append(values)
    return rows if len(rows) == 9 else None


def parse_minizinc_grids(output: str) -> List[Grid]:
    grids: List[Grid] = []
    current: List[List[int]] = []
    for raw_line in output.splitlines():
        line = raw_line.strip()
        if not line:
            continue
        if line.startswith("----------"):
            if len(current) == 9:
                grids.append(current)
            current = []
            continue
        if line.startswith("==========") or "UNSATISFIABLE" in line or "UNKNOWN" in line or "ERROR" in line:
            continue
        try:
            values = [int(token) for token in line.split()]
        except ValueError:
            continue
        if len(values) == 9:
            current.append(values)
    if len(current) == 9:
        grids.append(current)
    return grids


def puzzle_status_minizinc_solve_and_block(
    project_root: Path, grid: Grid, timeout_seconds: Optional[int]
) -> dict:
    start = time.time()
    solver_model = project_root / "models" / "sudoku_solver.mzn"
    proc = run_minizinc(solver_model, board_to_dzn("clues", grid), timeout_seconds)
    elapsed = time.time() - start
    if proc.returncode != 0:
        return {
            "status": "unknown",
            "solutions_found": 0,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": None,
            "method": "solve-and-block",
        }
    solution = parse_minizinc_grid(proc.stdout)
    if solution is None:
        return {
            "status": "unsat",
            "solutions_found": 0,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": None,
            "method": "solve-and-block",
        }
    non_unique_model = project_root / "models" / "sudoku_non_unique_check.mzn"
    dzn = board_to_dzn("clues", grid) + board_to_dzn("known_solution", solution)
    second = run_minizinc(non_unique_model, dzn, timeout_seconds)
    if second.returncode == 0 and parse_minizinc_grid(second.stdout) is not None:
        status = "multiple"
        solutions_found = 2
    else:
        status = "unique"
        solutions_found = 1
    return {
        "status": status,
        "solutions_found": solutions_found,
        "elapsed_seconds": time.time() - start,
        "solution": solution,
        "stderr": (proc.stderr + "\n" + second.stderr).strip(),
        "method": "solve-and-block",
    }


def puzzle_status_minizinc_counting(
    project_root: Path, grid: Grid, timeout_seconds: Optional[int]
) -> dict:
    start = time.time()
    solver_model = project_root / "models" / "sudoku_solver.mzn"
    proc = run_minizinc(
        solver_model,
        board_to_dzn("clues", grid),
        timeout_seconds,
        extra_flags=["-a", "-n", "2"],
    )
    elapsed = time.time() - start
    if proc.returncode != 0:
        return {
            "status": "unknown",
            "solutions_found": 0,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": None,
            "method": "counting",
        }
    solutions = parse_minizinc_grids(proc.stdout)
    search_complete = "==========" in proc.stdout
    if not solutions:
        return {
            "status": "unsat",
            "solutions_found": 0,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": None,
            "method": "counting",
        }
    if len(solutions) >= 2:
        return {
            "status": "multiple",
            "solutions_found": 2,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": solutions[0],
            "method": "counting",
        }
    if search_complete:
        return {
            "status": "unique",
            "solutions_found": 1,
            "elapsed_seconds": elapsed,
            "stderr": proc.stderr.strip(),
            "solution": solutions[0],
            "method": "counting",
        }
    return {
        "status": "unknown",
        "solutions_found": 1,
        "elapsed_seconds": elapsed,
        "stderr": proc.stderr.strip(),
        "solution": solutions[0],
        "method": "counting",
    }


def puzzle_status_minizinc(
    project_root: Path,
    grid: Grid,
    timeout_seconds: Optional[int],
    method: str = "solve-and-block",
) -> dict:
    if method == "solve-and-block":
        return puzzle_status_minizinc_solve_and_block(project_root, grid, timeout_seconds)
    if method == "counting":
        return puzzle_status_minizinc_counting(project_root, grid, timeout_seconds)
    raise ValueError(f"Metodo di unicità non supportato: {method}")


def is_valid_solution(grid: Grid) -> bool:
    full = set(range(1, 10))
    for i in range(9):
        if set(grid[i]) != full:
            return False
        if {grid[r][i] for r in range(9)} != full:
            return False
    for br in (0, 3, 6):
        for bc in (0, 3, 6):
            if {grid[r][c] for r in range(br, br + 3) for c in range(bc, bc + 3)} != full:
                return False
    return True


def transform_digit_permutation(grid: Grid, rng: random.Random) -> Grid:
    digits = list(range(1, 10))
    rng.shuffle(digits)
    mapping = {value: digits[value - 1] for value in range(1, 10)}
    return [[mapping[value] for value in row] for row in grid]


def transform_transpose(grid: Grid) -> Grid:
    return [list(row) for row in zip(*grid)]


def transform_rows_in_bands(grid: Grid, rng: random.Random) -> Grid:
    order = []
    for band in (0, 3, 6):
        rows = [band, band + 1, band + 2]
        rng.shuffle(rows)
        order.extend(rows)
    return [grid[r][:] for r in order]


def transform_band_permutation(grid: Grid, rng: random.Random) -> Grid:
    bands = [0, 3, 6]
    rng.shuffle(bands)
    order = [band + offset for band in bands for offset in range(3)]
    return [grid[r][:] for r in order]


def random_symmetry_transform(grid: Grid, rng: random.Random) -> Grid:
    result = transform_digit_permutation(grid, rng)
    result = transform_rows_in_bands(result, rng)
    result = transform_band_permutation(result, rng)
    if rng.random() < 0.5:
        result = transform_transpose(result)
    result = transform_rows_in_bands(result, rng)
    result = transform_band_permutation(result, rng)
    return result


def choose_source_grid(path: Path, rng: random.Random) -> Grid:
    payload = read_json(path)
    boards = payload.get("grids") or payload.get("solutions")
    if not isinstance(boards, list) or not boards:
        raise ValueError("Il file sorgente deve contenere una lista non vuota di griglie")
    grid = rng.choice(boards)
    validate_grid(grid, allow_zero=False)
    return copy_grid(grid)


def iter_positions(strategy: str, rng: random.Random) -> List[Tuple[int, int]]:
    positions = [(r, c) for r in range(9) for c in range(9)]
    if strategy == "random":
        rng.shuffle(positions)
        return positions
    if strategy == "symmetry":
        seen = set()
        ordered = []
        for r, c in positions:
            mirror = (8 - r, 8 - c)
            key = tuple(sorted(((r, c), mirror)))
            if key in seen:
                continue
            seen.add(key)
            ordered.append((r, c))
        rng.shuffle(ordered)
        return ordered
    if strategy == "density":
        return sorted(positions, key=lambda item: abs(item[0] - 4) + abs(item[1] - 4), reverse=True)
    raise ValueError("Strategia non supportata")


def removal_pass(
    puzzle: Grid,
    project_root: Path,
    backend: str,
    timeout_seconds: Optional[int],
    method: str,
    rng: random.Random,
) -> Tuple[int, int]:
    cells = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] != 0]
    rng.shuffle(cells)
    removed = 0
    checks = 0
    for row, col in cells:
        previous = puzzle[row][col]
        puzzle[row][col] = 0
        status = evaluate_puzzle(project_root, puzzle, backend, timeout_seconds, method=method)
        checks += 1
        if status["status"] == "unique":
            removed += 1
        else:
            puzzle[row][col] = previous
    return removed, checks


def post_optimize(
    puzzle: Grid,
    solution: Grid,
    project_root: Path,
    backend: str,
    timeout_seconds: Optional[int],
    method: str,
    rng: random.Random,
    attempts: int,
    max_readd: int = 1,
) -> dict:
    """Iterated local search on the clue removal.

    Each attempt re-adds `k` removed clues (a perturbation), then runs a fresh
    greedy removal pass and keeps the result only if the clue count strictly
    improves. With `max_readd > 1` the neighbourhood is variable: `k` grows from
    1 up to `max_readd` as consecutive attempts stall (diversification) and
    resets to 1 after every improvement (intensification).
    """
    clues_before = sum(1 for row in puzzle for value in row if value != 0)
    successful = 0
    checks = 0
    stall = 0
    for _ in range(attempts):
        empties = [(r, c) for r in range(9) for c in range(9) if puzzle[r][c] == 0]
        if not empties:
            break
        k = min(max_readd, len(empties), 1 + stall)
        before = sum(1 for row in puzzle for value in row if value != 0)
        snapshot = copy_grid(puzzle)
        for row, col in rng.sample(empties, k):
            puzzle[row][col] = solution[row][col]
        _, pass_checks = removal_pass(puzzle, project_root, backend, timeout_seconds, method, rng)
        checks += pass_checks
        after = sum(1 for row in puzzle for value in row if value != 0)
        if after < before:
            successful += 1
            stall = 0
        else:
            for r in range(9):
                puzzle[r][:] = snapshot[r][:]
            stall += 1
    return {
        "attempts": attempts,
        "successful": successful,
        "uniqueness_checks": checks,
        "max_readd": max_readd,
        "clues_before": clues_before,
        "clues_after": sum(1 for row in puzzle for value in row if value != 0),
    }


def optimize_bnb(
    solution: Grid,
    project_root: Path,
    backend: str,
    timeout_seconds: Optional[int],
    method: str,
    rng: random.Random,
    node_budget: int,
    best_puzzle: Grid,
    best_clues: int,
) -> dict:
    """Node-bounded branch-and-bound over the keep/remove decision per cell.

    Each of the 81 cells is decided once, in a randomised order, as keep or
    remove (binary tree, so every clue subset maps to exactly one leaf — no
    permutation blow-up). The "remove" branch is taken only if the puzzle stays
    unique with all undecided cells still present (a sound prune: by
    monotonicity every leaf below would otherwise be non-unique). The bound
    `kept >= best` cuts any branch that can no longer beat the incumbent. A leaf
    is accepted only after a final uniqueness check, because a sequence of
    individually safe removals can still be jointly non-unique.

    The full tree is exponential, so the search is capped at `node_budget`
    nodes and re-run from reshuffled orders (random restarts) until the budget
    is spent, keeping the best incumbent across restarts (warm-started from the
    local-search result).
    """
    state = {
        "best_clues": best_clues,
        "best_puzzle": copy_grid(best_puzzle),
        "nodes": 0,
        "checks": 0,
        "improvements": 0,
    }
    working = copy_grid(solution)

    def is_unique(grid: Grid) -> bool:
        state["checks"] += 1
        return evaluate_puzzle(project_root, grid, backend, timeout_seconds, method=method)["status"] == "unique"

    def dive(order: List[Tuple[int, int]], cap: int) -> None:
        local_nodes = [0]

        def recurse(i: int, kept: int) -> None:
            if local_nodes[0] >= cap or state["nodes"] >= node_budget:
                return
            local_nodes[0] += 1
            state["nodes"] += 1
            if kept >= state["best_clues"]:
                return
            if i == len(order):
                if is_unique(working):
                    clues = sum(1 for row in working for value in row if value != 0)
                    if clues < state["best_clues"]:
                        state["best_clues"] = clues
                        state["best_puzzle"] = copy_grid(working)
                        state["improvements"] += 1
                return
            row, col = order[i]
            value = working[row][col]
            working[row][col] = 0
            if is_unique(working):
                recurse(i + 1, kept)
            working[row][col] = value
            recurse(i + 1, kept + 1)

        recurse(0, 0)

    while state["nodes"] < node_budget:
        order = [(r, c) for r in range(9) for c in range(9)]
        rng.shuffle(order)
        for r in range(9):
            working[r][:] = solution[r][:]
        dive(order, cap=min(node_budget - state["nodes"], 4000))
    return {
        "node_budget": node_budget,
        "nodes_used": state["nodes"],
        "uniqueness_checks": state["checks"],
        "improvements": state["improvements"],
        "best_puzzle": state["best_puzzle"],
        "best_clues": state["best_clues"],
    }


def generate_puzzle(
    source_grid: Grid,
    backend: str,
    project_root: Path,
    strategy: str,
    timeout_seconds: Optional[int],
    seed: int,
    method: str = "counting",
    optimize_attempts: int = 0,
    optimize_readd: int = 1,
    bnb_nodes: int = 0,
) -> dict:
    rng = random.Random(seed)
    puzzle = copy_grid(source_grid)
    removal_log = []
    positions = iter_positions(strategy, rng)
    index = 0
    while index < len(positions):
        row, col = positions[index]
        if puzzle[row][col] == 0:
            index += 1
            continue
        previous = puzzle[row][col]
        mirror = None
        mirror_prev = None
        if strategy == "symmetry":
            candidate = (8 - row, 8 - col)
            if candidate != (row, col):
                mirror = candidate
                mirror_prev = puzzle[mirror[0]][mirror[1]]
        puzzle[row][col] = 0
        if mirror is not None:
            puzzle[mirror[0]][mirror[1]] = 0
        status = evaluate_puzzle(project_root, puzzle, backend, timeout_seconds, method=method)
        accepted = status["status"] == "unique"
        if not accepted:
            puzzle[row][col] = previous
            if mirror is not None:
                puzzle[mirror[0]][mirror[1]] = mirror_prev
        removal_log.append(
            {
                "row": row + 1,
                "col": col + 1,
                "accepted": accepted,
                "status": status["status"],
                "elapsed_seconds": status["elapsed_seconds"],
            }
        )
        index += 1
    optimization = None
    if optimize_attempts > 0:
        optimization = post_optimize(
            puzzle, source_grid, project_root, backend, timeout_seconds, method, rng,
            optimize_attempts, max_readd=optimize_readd,
        )
    bnb = None
    if bnb_nodes > 0:
        clues_now = sum(1 for row in puzzle for value in row if value != 0)
        bnb_result = optimize_bnb(
            source_grid, project_root, backend, timeout_seconds, method, rng,
            bnb_nodes, best_puzzle=puzzle, best_clues=clues_now,
        )
        bnb = {key: bnb_result[key] for key in ("node_budget", "nodes_used", "uniqueness_checks", "improvements", "best_clues")}
        bnb["clues_before"] = clues_now
        if bnb_result["best_clues"] < clues_now:
            puzzle = bnb_result["best_puzzle"]
    clues = sum(1 for row in puzzle for value in row if value != 0)
    result = {
        "seed": seed,
        "strategy": strategy,
        "backend": backend,
        "method": method,
        "puzzle": puzzle,
        "solution": source_grid,
        "clues": clues,
        "uniqueness_checks": len(removal_log),
        "accepted_removals": sum(1 for item in removal_log if item["accepted"]),
        "removal_log": removal_log,
    }
    if optimization is not None:
        result["optimization"] = optimization
    if bnb is not None:
        result["bnb"] = bnb
    return result


def evaluate_puzzle(project_root: Path, grid: Grid, backend: str, timeout_seconds: Optional[int], method: str = "counting") -> dict:
    validate_grid(grid, allow_zero=True)
    if backend == "python":
        return puzzle_status_python(grid, method=method)
    if backend == "minizinc":
        return puzzle_status_minizinc(project_root, grid, timeout_seconds, method=method)
    if backend == "minizinc-api":
        return puzzle_status_minizinc_api(project_root, grid, timeout_seconds, method=method)
    raise ValueError("Backend non supportato")


def cmd_check(args: argparse.Namespace) -> int:
    payload = read_json(Path(args.input))
    grid = payload.get("grid") or payload["puzzle"]
    result = evaluate_puzzle(Path(args.project_root), grid, args.backend, args.timeout, method=args.method)
    print(f"status: {result['status']}  |  solutions: {result.get('solutions_found', '-')}  |  method: {result.get('method', args.method)}  |  time: {result['elapsed_seconds']:.3f}s")
    if result.get("solution"):
        print("solution:")
        print(format_grid(result["solution"]))
    return 0 if result["status"] in {"unique", "multiple", "unsat"} else 1


def cmd_generate(args: argparse.Namespace) -> int:
    source = choose_source_grid(Path(args.source), random.Random(args.seed))
    result = generate_puzzle(
        source_grid=source,
        backend=args.backend,
        project_root=Path(args.project_root),
        strategy=args.strategy,
        timeout_seconds=args.timeout,
        seed=args.seed,
        method=args.method,
        optimize_attempts=args.optimize_attempts,
        optimize_readd=args.optimize_readd,
        bnb_nodes=args.bnb_nodes,
    )
    write_json(Path(args.output), result)
    print(f"saved: {args.output}  |  clues: {result['clues']}  |  strategy: {args.strategy}  |  method: {args.method}")
    if result.get("optimization"):
        opt = result["optimization"]
        print(f"optimization: {opt['clues_before']} -> {opt['clues_after']} clues  |  attempts: {opt['attempts']}  |  successful: {opt['successful']}  |  max_readd: {opt['max_readd']}  |  extra checks: {opt['uniqueness_checks']}")
    if result.get("bnb"):
        b = result["bnb"]
        print(f"bnb: {b['clues_before']} -> {b['best_clues']} clues  |  nodes: {b['nodes_used']}  |  improvements: {b['improvements']}  |  extra checks: {b['uniqueness_checks']}")
    print("puzzle:")
    print(format_grid(result["puzzle"]))
    return 0


def cmd_augment(args: argparse.Namespace) -> int:
    rng = random.Random(args.seed)
    payload = read_json(Path(args.input))
    boards = payload.get("grids") or payload.get("solutions")
    if not isinstance(boards, list) or not boards:
        raise ValueError("Il file sorgente deve contenere una lista non vuota di griglie")
    generated: List[Grid] = []
    for _ in range(args.count):
        source = rng.choice(boards)
        validate_grid(source, allow_zero=False)
        transformed = random_symmetry_transform(source, rng)
        if not is_valid_solution(transformed):
            raise RuntimeError("Trasformazione non valida: la griglia prodotta non è una soluzione Sudoku")
        generated.append(transformed)
    write_json(Path(args.output), {"grids": generated, "source": args.input, "seed": args.seed})
    print(f"saved: {args.output}  |  grids: {len(generated)}  |  source grids: {len(boards)}  |  seed: {args.seed}")
    return 0


def cmd_solve(args: argparse.Namespace) -> int:
    payload = read_json(Path(args.input))
    grid = payload.get("grid") or payload["puzzle"]
    validate_grid(grid, allow_zero=True)
    if args.backend == "python":
        start = time.time()
        solution = solve_python(grid)
        elapsed = time.time() - start
        result = {"solution": solution, "elapsed_seconds": elapsed}
    else:
        status = puzzle_status_minizinc(Path(args.project_root), grid, args.timeout)
        result = {"solution": status.get("solution"), "elapsed_seconds": status["elapsed_seconds"], "status": status["status"]}
    print(f"time: {result['elapsed_seconds']:.3f}s")
    if result.get("solution"):
        print("solution:")
        print(format_grid(result["solution"]))
    return 0 if result.get("solution") else 1


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Pipeline per il progetto Sudoku Instance Generation")
    parser.add_argument(
        "--project-root",
        default=str(Path(__file__).resolve().parents[1]),
        help="Radice del progetto Sudoku",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    solve_cmd = sub.add_parser("solve")
    solve_cmd.add_argument("--input", required=True)
    solve_cmd.add_argument("--backend", choices=["python", "minizinc"], default="python")
    solve_cmd.add_argument("--timeout", type=int, default=None)
    solve_cmd.set_defaults(func=cmd_solve)

    check_cmd = sub.add_parser("check")
    check_cmd.add_argument("--input", required=True)
    check_cmd.add_argument("--backend", choices=["python", "minizinc", "minizinc-api"], default="python")
    check_cmd.add_argument("--method", choices=["counting", "solve-and-block"], default="counting")
    check_cmd.add_argument("--timeout", type=int, default=None)
    check_cmd.set_defaults(func=cmd_check)

    gen_cmd = sub.add_parser("generate")
    gen_cmd.add_argument("--source", required=True)
    gen_cmd.add_argument("--output", required=True)
    gen_cmd.add_argument("--backend", choices=["python", "minizinc", "minizinc-api"], default="python")
    gen_cmd.add_argument("--strategy", choices=["random", "symmetry", "density"], default="random")
    gen_cmd.add_argument("--method", choices=["counting", "solve-and-block"], default="counting")
    gen_cmd.add_argument("--timeout", type=int, default=None)
    gen_cmd.add_argument("--seed", type=int, default=0)
    gen_cmd.add_argument("--optimize-attempts", type=int, default=0)
    gen_cmd.add_argument("--optimize-readd", type=int, default=1, help="max clues re-added per local-search perturbation (>1 = variable neighbourhood)")
    gen_cmd.add_argument("--bnb-nodes", type=int, default=0, help="branch-and-bound node budget (0 = off)")
    gen_cmd.set_defaults(func=cmd_generate)

    aug_cmd = sub.add_parser("augment")
    aug_cmd.add_argument("--input", required=True)
    aug_cmd.add_argument("--output", required=True)
    aug_cmd.add_argument("--count", type=int, default=10)
    aug_cmd.add_argument("--seed", type=int, default=0)
    aug_cmd.set_defaults(func=cmd_augment)

    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
