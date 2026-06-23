# Oral Presentation Script — Speaker Notes

How to use: keep this next to the report during the oral. For each report section, the bullets are **what to say out loud, in English**, while you scroll the report. The goal is to sound clear and complete so the professor has no reason to interrupt. The ⚡ lines are the likely follow-up question + a one-line answer, in case he does.

Opening line:

> *"This project is about generating 9×9 Sudoku instances that have exactly one solution, with as few clues as possible. The key point is the distinction between solving — which is a CSP — and generating, which is a procedure built on top of the CSP."*

---

## §1 — Introduction

- The goal: generate Sudoku instances that are (1) admissible, (2) uniquely solvable, (3) with the fewest possible clues.
- A Sudoku *solver* is the classic CP example; *generation* adds a layer — we need to decide, for a partial puzzle, whether it has exactly one solution.
- This uniqueness check is **not** a CP constraint of the problem — it's built on top of the base CSP.
- Three components: (1) a MiniZinc model, (2) a uniqueness checker in two variants, (3) a Python pipeline for iterative clue removal.

⚡ *"Why is this relevant for the course?"* → It exercises `alldifferent`, search heuristics, redundant constraints, and the solving-vs-generating distinction.

---

## §2 — Modelling Sudoku

- 81 decision variables, `var 1..9`, one per cell. `clues` is a parameter: `0` = empty, `1..9` = fixed.
- The bridging constraint pins `grid[i,j] = clues[i,j]` only where `clues > 0` (the `where` filter).
- Three families of `alldifferent`: 9 rows + 9 columns + 9 blocks = 27 constraints.
- **Key modelling choice**: `alldifferent` instead of pairwise `!=`. The global constraint is propagated with Régin's matching algorithm → **arc consistency** in polynomial time. Pairwise `!=` gives only **bounds consistency** and misses many failures.

⚡ *"Explain the difference AC vs BC."* → AC prunes any value with no support in a related variable; pairwise `!=` only checks pairs, so e.g. three cells all with domain `{1,2}` is a contradiction AC catches and pairwise does not.

### §2.1 Search annotation

- `int_search(vars, first_fail, indomain_min, complete)`.
- `first_fail` = pick the smallest-domain variable → fail-first principle, fail high in the tree where pruning is cheap. Fits Sudoku because domains are very heterogeneous after the clues.
- `indomain_min` = smallest value first (conservative default). `complete` = exhaustive DFS, the only mode that can *prove* uniqueness.
- Variant `dom_w_deg`: adaptive fail-first, score = `|domain| / weighted_degree`; constraint weights grow on each failure, so the search learns from conflicts.

### §2.2 Redundant constraints

- `sum = 45` on rows/columns/blocks. **Implied** by `alldifferent` (1+…+9 = 45) → no change to the solution set, only to propagation.
- Different algebraic semantics (bounds on the sum) → can help, but on 9×9 the gain is marginal because `alldifferent` is already strong. Mainly pedagogical.

### §2.3 Full-grid generation

- Same model with `indomain_random` → different complete grids per run. Used as fallback; main experiments use 50 grids from Kaggle (reservoir sampling).

---

## §3 — Uniqueness Checking

- "Exactly one solution" is about the *number* of solutions, not satisfiability — not a single CP constraint.
- **Complexity framing** (say this, it's strong): the decision problem is NP-complete (Yato & Seta, generalised board); counting all solutions is #P-complete; but we only need "≥2 or not", which is in NP. Both methods stop at 2.

### §3.1 Solve-and-block

- Solve → get S₁ → search for S₂ ≠ S₁ via the blocking constraint `exists(i,j) grid[i,j] != known_solution[i,j]`. UNSAT ⇒ unique.

### §3.2 Solution counting

- Enumerate, stop at 2 (`-a -n 2`). 0 → unsat, 1 + exhausted → unique, ≥2 → multiple. The `limit=2` keeps it in NP.

### §3.3 Timeout handling

- Three outcomes: unique / multiple / unknown. `unknown` is **never** treated as unique — rollback and log. Treating it as unique could accept a non-unique puzzle.

⚡ *"Why is the unique case the worst case?"* → To prove uniqueness you must exhaust the tree (prove no second solution exists); finding is cheap, proving non-existence is expensive.

---

## §4 — Puzzle Generation

- Start from a complete grid, remove cells one by one in the strategy's order; after each removal check uniqueness; if lost → rollback.
- It's **greedy with rollback** — every cell decided once, never reconsidered → *not optimal*.

### §4.2 Removal strategies

- **Random** (baseline), **symmetry-aware** (central mirror `(8-r,8-c)`, removes pairs), **density-aware** (periphery first, Manhattan distance).
- Stress: symmetry-aware is an **aesthetic** heuristic, **not** CP symmetry breaking — the model breaks no symmetries because the clues already do.

⚡ *"Is it optimal?"* → No. To approach the theoretical minimum of 17 clues (McGuire 2012) you'd need backtracking on the removals; my greedy stops around 22-25.

---

## §5 — Pipeline Architecture

- Hybrid: MiniZinc does the CP queries, Python orchestrates removal + logging.
- **Python backend**: pure-Python backtracking + forward checking — fast, runs without MiniZinc (start-up overhead ~400 ms/call matters across 80+ checks per puzzle).
- **MiniZinc backend**: subprocess to Gecode; supports both methods; parses output markers (`----------`, `==========`).

⚡ *"Why both Python and MiniZinc?"* → MiniZinc is the CP reference for correctness; Python is the fast driver for the experiments at scale.

---

## §6 — Experiments

- 20 grids × 3 strategies × 2 methods = 120 runs, seed 42.
- **Clues**: random 24.6 (best), density 25.4, symmetry 27.6 (double-tax of pairs). Absolute min 22.
- **Methods**: counting ~1.8× faster than solve-and-block (reuses search state). Same final clue count — only efficiency differs.
- **Time vs clues**: mild correlation, high variance; cost dominated by ~80 checks/run at ~2-5 ms each.
- Redundant constraints / `dom_w_deg`: marginal on 9×9, expected to matter on larger boards.

---

## §7 — Conclusions

- Random best for clue count; counting faster; separating removal (procedural) from verification (CP) is the key design choice; explicit `unknown` handling is critical for correctness.
- **Limits**: 22 vs 17 (greedy, no removal backtracking); MiniZinc slow for intensive benchmarks (start-up overhead); richer symmetries not explored.
- **Extensions**: larger Kaggle sample, MiniZinc-Python API, difficulty metric, backtracking on removal.

Closing line:

> *"In short: a clean CP core for solving and uniqueness, wrapped in a Python procedure for generation. The interesting CP content is the `alldifferent` propagation, the search heuristics, and turning a #P-style counting question into an NP one by stopping at two solutions."*

---

## If he points at a model file directly

- `sudoku_solver.mzn` → base model (§2).
- `sudoku_solver_redundant.mzn` → +`sum=45` (§2.2).
- `sudoku_solver_dom_w_deg.mzn` → `dom_w_deg` variant (§2.1).
- `sudoku_generate_full_grid.mzn` → `indomain_random` (§2.3).
- `sudoku_non_unique_check.mzn` → blocking constraint (§3.1).

## The one trap question

- *"Where are the linear constraints for capacity and cost (point 1)?"* → That line was a copy-paste residue from project 18; you confirmed by email it should be ignored. Sudoku has no capacity/cost dimension — it's pure satisfaction, modelled with `alldifferent`.
