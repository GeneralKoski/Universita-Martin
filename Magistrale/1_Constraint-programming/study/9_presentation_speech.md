# Oral Presentation - Word-for-Word Speech

## Opening

> "The project we chose is Sudoku Instance Generation With Uniqueness Guarantee. The goal is to produce 9×9 puzzles that have exactly one solution, using as few clues as possible.
>
> The interesting part is the distinction between two things. Solving a Sudoku is a classic constraint satisfaction problem. But generating a good puzzle is a procedure built on top of that CSP. So the talk is really about how we used constraint programming as the engine, and wrapped a generation algorithm around it."

---

## §1 - Introduction

> "Let me start with the goal. A good puzzle has three properties. First, it has to be a legal Sudoku. Second, it must have exactly one solution. And third, having as few clues as possible, because fewer clues makes a cleaner and harder puzzle.
>
> A Sudoku solver is the default constraint programming example. What makes generation different is this uniqueness requirement. For any partial puzzle, we have to decide if it has exactly one solution, and that's the key point: uniqueness is *not* one of the constraints of the problem. It's a property we check from the outside, by running the solver and looking at how many solutions come out."

### §1.1 - What I built and the languages

> "Concretely, we built three things. One: a set of MiniZinc models that solve a Sudoku and check uniqueness (that's the CP core). Two: a uniqueness checker, in two variants, which I'll explain. Three: a Python pipeline that drives the whole thing.
>
> So two languages. **MiniZinc** for the constraint model and **Python** as the orchestrator.
>
> In fact we have interchangeable backends for the checks. One calls **MiniZinc** as a subprocess, using Gecode. The other is a small **pure-Python** solver. We added it because there are eighty-plus uniqueness checks per puzzle, and MiniZinc has a per-call overhead of about 200 milliseconds, so the Python backend keeps the experiments fast. They give the same answers; MiniZinc is the trustworthy one, Python is the fast one. There's also a third backend through the MiniZinc-Python library - I'll come back to it in the extensions, because what we measured there was a surprise."

⚡ *"Why is this relevant to the course?"* → "Because it exercises exactly what we studied: the `alldifferent` global constraint, search heuristics, redundant constraints, and the distinction between solving and generating."

---

## §2 - The MiniZinc Models

> "Let's start with the base model first. We have 81 decision variables, one per cell, each declared `var 1..9`. The clues come in as a parameter: zero means empty, one to nine means fixed.
>
> There's a constraint that associates a cell to its clue, but only where the clue is greater than zero.
>
> Then the real Sudoku rules. Three families of `alldifferent` constraints: nine for the rows, nine for the columns, nine for the blocks.
>
> And this is an important modelling choice. We used  the `alldifferent` constraint instead of writing all the pairwise 'not equal' constraints by hand. The reason is propagation since `alldifferent` is propagated with Régin's matching algorithm, which gives full arc consistency in polynomial time. The pairwise version only gives bounds consistency, and it misses failures arc consistency would catch."

⚡ *"Explain arc consistency versus bounds consistency."* → "Arc consistency removes any value with no support in a related variable. Classic example: three cells that all have domain {1,2}. That's already a contradiction - three cells, two values. Arc consistency on `alldifferent` catches it immediately. Pairwise checks pairs only, no single pair looks wrong, so it misses it."

> "Now, the other model files are the *same base model* with one small change each. Let me go through them quickly."

### §2.1 - Search annotation

> "First, the search annotation. We used `int_search` with `first_fail` and `indomain_min`, in complete mode.
>
> `first_fail` means: always pick the variable with the smallest domain next. So, fail high in the tree, where cutting branches is cheap.
>
> `indomain_min` tries the smallest value first.
>
> `complete` means exhaustive depth-first search.
>
> One variant file swaps the first_fail with `dom_w_deg`. That's an adaptive fail-first: the score is domain size over weighted degree, and constraint weights grow each time a constraint fails. So the search learns from its own conflicts."

### §2.2 - Redundant constraints

> "The next variant adds redundant constraints. The sum of each row, column, and block equals forty-five. That's implied by `alldifferent`, because one through nine adds to forty-five. So it doesn't change the solutions at all, only the propagation.
>
> On a 9×9 board the gain is marginal, because `alldifferent` is already strong."

### §2.3 - Full-grid generation

> "And the last model is the same thing with `indomain_random`, which produces a different complete grid every run. We use it to generate complete starting grids from scratch. For the benchmarks, though, we took fifty complete grids from the Kaggle dataset. The point is: the complete grid can come from Kaggle *or* from this model, and the rest of the pipeline is identical."

---

## §3 - Uniqueness Checking

> "Now the uniqueness check.
>
> 'Exactly one solution' is a statement about the *number* of solutions, not about whether a solution exists. So it's not something you can write as a single constraint.
>
> A nice way to frame it: deciding whether a generalised Sudoku has a solution is NP-complete. Counting *all* solutions is even harder since it's #P-complete. But we don't need the full count. We only need to know 'is there a second solution or not'. And that stays in NP because both methods stop at the moment they find a second one."

### §3.1 - Solve-and-block

> "The first method is solve-and-block. We solve the puzzle once, get a solution, call it S1, then add a blocking constraint: the grid must differ from S1 in at least one cell. And I solve again. If that's unsatisfiable, there's no second solution, so the puzzle is unique."

### §3.2 - Solution counting

> "The second method is solution counting. We ask the solver to enumerate solutions, but cap it at two. Zero solutions means unsatisfiable. One solution (with the search exhausted) means unique. Two means not unique. That cap at two is exactly what keeps the problem in NP instead of #P."

### §3.3 - Timeout handling

> "And timeouts. Each check has three outcomes: unique, multiple, or unknown if it times out. The rule is: unknown is *never* treated as unique. If I'm not sure, I roll back the removal and log it. Because treating 'unknown' as 'unique' could ship a puzzle with two solutions - that's the one mistake I really can't make."

⚡ *"Why is the unique case the most expensive?"* → "Because to prove uniqueness you must exhaust the whole search tree - prove no second solution exists anywhere. Finding one is cheap; proving none exists is expensive."

⚡ *"Did you validate the checker?"* → "Yes - we ran it on five real 17-clue puzzles, the proven minimum, from Royle's catalogue. Both methods and both backends correctly call them unique, no false positives. And it's a nice illustration of the difficulty: those checks take up to ~8 seconds each versus ~2 milliseconds for a generation check, because with only 17 clues the tree you must exhaust to prove uniqueness is huge. See report section 6.6."

---

## §4 - Puzzle Generation

> "So how do we actually make a puzzle. We start from a full, complete grid and remove cells one at a time, in an order set by the strategy. After each removal we run the uniqueness check. if still unique, keep going, if that cell broke uniqueness, put it back and move on.
>
> It's greedy with rollback. Each cell is decided once, never reconsidered. Which means not optimal."

### §4.1 - Removal strategies

> "We tried three removal orders. Random, the baseline. Symmetry-aware, which removes cells in mirror pairs around the centre. And density-aware, which removes from the edges first, by Manhattan distance from the centre.
>
> The symmetry-aware strategy is purely aesthetic. It makes the puzzle look nice and symmetric. It's not symmetry breaking in the CP sense, which would mean adding constraints to cut equivalent solutions. Here that's unnecessary, since the fixed clues already destroy every board symmetry."

⚡ *"Is the result optimal?"* → "No. The theoretical minimum for a unique Sudoku is 17 clues - the McGuire result, 2012. The plain greedy stops around 22 to 27; with the post-optimization pass of section 7 we get down to 20. Closing the rest of the gap would need a systematic branch-and-bound on the removals."

---

## §5 - Live Demo

"We could actually run a test right now"

Running commands while explaining what each one does:

```bash
# generate + check (the classic demo)
python3 scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output /tmp/demo.json --backend python --strategy random --seed 7
python3 scripts/sudoku_pipeline.py check --input /tmp/demo.json --backend python --method counting
python3 scripts/sudoku_pipeline.py check --input /tmp/demo.json --backend python --method solve-and-block

# NEW: post-optimization live (24 -> 21 clues in seconds)
python3 scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output /tmp/demo_opt.json --backend python --strategy random --seed 7 --optimize-attempts 20

# NEW: symmetry augmentation (complete grids without Kaggle, instant)
python3 scripts/sudoku_pipeline.py augment --input data/solved/sample_solutions.json --output /tmp/aug.json --count 5 --seed 1
```

---

## §6 - Results

> "Now the experiments. We sampled five hundred grids from the nine-million-row Kaggle dataset, times three strategies, times two methods: three thousand runs, all with seed forty-two so it's reproducible. Why five hundred and not more? Because at that sample size the standard error of the mean is already below 0.05 clues - a bigger sample wouldn't change any reported figure.
>
> On the number of clues: random was actually the best, around 24.4 on average. Density was 25.5. Symmetry was worst at 27.5, as expected since it pays a double tax. The best single greedy run reached 21 clues - but only once in fifteen hundred attempts; the typical best is 22 or 23.
>
> On the methods: solution counting was about 1.8 times faster than solve-and-block, because it reuses the search state instead of restarting. Both give the exact same final clue count, only the speed differs.
>
> On time versus clues: a mild correlation, but a lot of variance. The number of checks is constant - eighty-one per run, one per cell - so the total time really measures how hard the intermediate puzzles were, and that depends more on structure than on the final clue count.
>
> And the redundant constraints and the `dom_w_deg` variant, both marginal on 9×9, as expected. They'd matter more on a larger board."

---

## §7 - Implemented Extensions (NEW - la parte forte)

> "After the first version of the report, we implemented and measured three of the extensions we had proposed. I want to go through them because each one taught us something.

### §7.1 - Backtracking on the removal

> "First, the greedy limit. The greedy pass is order-dependent: it stops at a local minimum. So we added a post-optimization move I'd call *add-one-remove-many*: take a cell we already removed, put its value back - that's always safe, adding a clue can never create a second solution - and then re-run a greedy removal pass over all the clues, in a *new random order*. If that pass removes at least two cells, the net count went down, so we keep it. Otherwise we roll back.
>
> It's a simple local search sitting on top of the CP check. And it works: on the 50-grid sample, 47 runs out of 50 improved. The mean dropped from 24.5 to 22.1 clues, and the best puzzles reached **20 clues**. For comparison: across fifteen hundred plain greedy runs in the benchmark, 20 was never reached - the optimization turns the lucky tail of the greedy into a systematic outcome."

⚡ *"Why does re-adding a clue help?"* → "Because it changes which local minimum the greedy lands in. The removal order determines where greedy gets stuck; re-adding one cell and re-running in a different order lets the search escape the plateau."

⚡ *"Could more attempts reach 17?"* → "No - we tested it. On a sample grid, 20 attempts reach 21 clues and 1000 attempts, fifty times the work, still stop at 21. Two reasons: the minimum clue count is a property of each complete grid - most grids don't even admit a 17-clue puzzle - and getting below 20 needs coordinated multi-cell changes that a single add-one-remove-many move can't make. That's why the next step would be branch-and-bound on the removals, not more iterations."

### §7.2 - The MiniZinc-Python experiment: a negative result

> "Second, we had hypothesised that the MiniZinc-Python API would cut the per-call start-up cost. So we implemented it as a third backend and measured it. Result: it was *slower* - about 0.36 seconds per check versus 0.20 for the plain subprocess, on identical runs producing identical puzzles.
>
> The explanation is that the library *wraps the MiniZinc CLI*, it doesn't embed the compiler. So the flattening - compiling the model to FlatZinc - still happens on every single solve, plus the library's own async overhead. Our hypothesis targeted the wrong component: the dominant cost is flattening, not subprocess management. The real fix would be a persistent solver process or direct Gecode bindings.
>
> I think this is a good example of why you *measure* an optimisation before trusting it. A negative result is still a result."

### §7.3 - Symmetries

> "Third, symmetries. A valid complete grid stays valid under certain transformations: permuting the nine digits, permuting rows within a band, permuting whole bands, and transposing. We composed these randomly in an `augment` command that turns our fifty Kaggle grids into as many new complete grids as we want - all verified valid, none equal to a source grid, at essentially zero cost because no solver call is involved.
>
> Together with the `indomain_random` full-grid model, this makes the pipeline completely independent from the external dataset. One honest caveat: a transformed grid is structurally *related* to its source, so for statistics the independent Kaggle samples are still preferable - and the assignment asks for them anyway."

⚡ *"Is this symmetry breaking?"* → "No - it's the opposite direction. Symmetry breaking *removes* symmetric branches from the search. Here we *exploit* the symmetries of the solution space to generate new instances. Same group-theoretic structure, used constructively."

### §7.4 - Stronger search: does more machinery help?

> "Finally, we asked whether more sophisticated search beats the simple local search. We tried two things. First, a *variable neighbourhood*: instead of re-adding one clue per perturbation, re-add up to three, escalating when stuck. Second, a node-bounded *branch-and-bound* over the keep/remove decision per cell, warm-started from the local search.
>
> We tested this on 408 fresh grids sampled from the 9-million-row dataset. The result is nuanced and honest. The variable neighbourhood genuinely helps - it lowers the mean from 22.1 to 21.5 and beats the single-cell version on 192 of 408 grids, losing on only 37. But the branch-and-bound does **not** pay off: it ties the variable neighbourhood on 396 of 408 grids and costs nearly twice the time. The reason is that the minimum-clue subset space is astronomically large - order 81-choose-22 - so within any practical node budget the search explores only a sliver. The best we reach is 20 clues, and the distribution is tight: about 98% of grids land at 20, 21, or 22.
>
> The takeaway, again, is that the residual gap to 17 is set by the grid itself; closing it needs an exact unavoidable-set method, not more brute search."

⚡ *"So branch-and-bound was a waste?"* → "As an optimiser, within budget, yes - and that's worth reporting. It confirms the bottleneck is structural, not a matter of search effort. The same honesty as the MiniZinc-Python result: we measured it rather than assuming."

---

## §8 - Conclusions

> "To wrap up. Random removal gave the fewest clues, and the post-optimization - especially the variable-neighbourhood variant - pushed the minimum down to 20 across 408 grids. Solution counting was the faster method, about 1.8 times. The key design decision was separating the two concerns - removal is a procedure, verification is the CP part. And handling 'unknown' explicitly was critical for correctness.
>
> The main remaining limit is 20 versus the theoretical 17 - closing that gap would need a systematic branch-and-bound on the number of clues. And the MiniZinc-Python experiment showed that the per-check flattening, not the subprocess, is the real bottleneck.
>
> If we extended it further, we'd benchmark on a much larger Kaggle sample, add a real difficulty metric, and parameterise the models for 16×16 and 25×25 boards, where the global `alldifferent` should beat its decomposition much more visibly."

## Closing

> "So in one sentence: a clean CP core for solving and checking uniqueness, wrapped in a Python procedure for generation - plus a local search on top that escapes the greedy's local minima, and a measured, honest look at where the real costs are. The constraint-programming content is the `alldifferent` propagation, the search heuristics, and that trick of turning a #P counting question into an NP one by just stopping at two solutions. … Thank you."

---

## Backup - if he points at a specific model file

- `sudoku_solver.mzn` → the base model. §2.
- `sudoku_solver_redundant.mzn` → adds the sum-equals-45 constraints. §2.2.
- `sudoku_solver_dom_w_deg.mzn` → the `dom_w_deg` search variant. §2.1.
- `sudoku_generate_full_grid.mzn` → `indomain_random` for full grids. §2.3.
- `sudoku_non_unique_check.mzn` → the blocking constraint. §3.1.

## Backup - if he points at the new pipeline features

- `--optimize-attempts N` → post-optimization, add-one-remove-many. §7.1.
- `augment` subcommand → symmetry transformations of complete grids. §7.3.
- `--backend minizinc-api` → MiniZinc-Python backend, the negative result. §7.2.
- `results/optimization_benchmark.csv` / `results/minizinc_api_comparison.json` → raw data of §7.
