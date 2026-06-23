# Funzioni Python chiave — Spiegazioni complete per l'orale

Le 4 funzioni di `scripts/sudoku_pipeline.py` che portano contenuto CP e vanno sapute difendere all'orale. Tutto il resto del file è "glue" (I/O, subprocess, parsing, CLI): da riconoscere, non da studiare.

## Indice

1. [2.2 — `count_solutions_python`](2.2_count_solutions.md) — counting con limite a 2 (unicità)
2. [2.3 — `solve_excluding_python`](2.3_solve_excluding.md) — solve-and-block (cerca S₂ ≠ S₁)
3. [2.5 — `iter_positions`](2.5_iter_positions.md) — le 3 strategie di rimozione
4. [2.6 — `generate_puzzle`](2.6_generate_puzzle.md) — il loop di generazione (greedy + rollback)

## Come si incastrano

```
generate_puzzle (2.6)  ── il motore ──┐
       │                               │
       │ dopo ogni rimozione chiede:   │
       │ "ancora unico?"               │
       ▼                               │
  ┌──────────────┐  ┌────────────────┐ │
  │ counting     │  │ solve-and-block│ │  ← scegli con --method
  │ (2.2)        │  │ (2.3)          │ │
  └──────────────┘  └────────────────┘ │
       ▲                                │
       │ ordine delle celle deciso da ──┘
       │
  iter_positions (2.5)
```

- **2.6** è il motore: rimuove celle una a una.
- **2.5** gli dice in che ordine provarle.
- **2.2 / 2.3** sono i due oracoli di unicità intercambiabili che consulta dopo ogni rimozione.

## Helper condivisi (da conoscere, non da difendere a fondo)

- `candidate_values(grid, r, c)` → i valori legali per una cella = forward checking dell'`alldifferent` su una cella.
- `find_empty(grid)` → sceglie la cella vuota col dominio più piccolo = `first_fail` scritto a mano.
- pattern backtracking: `prova valore → ricorri → undo (rimetti 0)`.
