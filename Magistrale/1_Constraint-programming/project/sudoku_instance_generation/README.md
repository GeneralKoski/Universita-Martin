# Sudoku Instance Generation

Generazione di istanze Sudoku 9×9 con soluzione unica e numero minimo di indizi.

## Struttura

- `models/`: modelli MiniZinc
- `scripts/`: pipeline e script di benchmark
- `data/solved/`: griglie complete di partenza (campione Kaggle)
- `data/test/`: istanze di test
- `data/generated/`: puzzle generati
- `results/`: risultati dei benchmark
- `report/report.pdf`: report finale
- `spec/gecode_local.msc`: configurazione del solver Gecode

## Esecuzione

Due backend equivalenti: `python` (autonomo, senza dipendenze) e `minizinc` (richiede `minizinc` e `fzn-gecode` nel `PATH`).

**Verifica unicità di un puzzle**
```bash
python3 scripts/sudoku_pipeline.py check --input data/test/unique_puzzle.json --backend python
```

**Generazione di un puzzle**
```bash
python3 scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output data/generated/puzzle.json --backend python --strategy random --seed 7
```
Strategie: `random`, `symmetry`, `density`. Metodi di unicità (`--method`): `counting`, `solve-and-block`.

**Ottimizzazione post-rimozione** (local search sulla rimozione, abbassa il numero di indizi)
```bash
python3 scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output data/generated/puzzle.json --backend python --strategy random --seed 7 --optimize-attempts 100
```
Varianti più aggressive (vedi §7.4 del report): `--optimize-readd 3` (variable neighbourhood, riaggiunge fino a 3 indizi) e `--bnb-nodes 8000` (branch-and-bound node-bounded). Nei benchmark danno gli stessi clue della versione base a costo maggiore.

**Griglie complete via simmetrie** (senza dataset esterno; l'output è usabile come `--source`)
```bash
python3 scripts/sudoku_pipeline.py augment --input data/solved/sample_solutions.json --output data/solved/augmented_solutions.json --count 20 --seed 42
```

**Benchmark e confronto strategie**
```bash
python3 scripts/benchmark.py --input data/test/benchmark_instances.json --output results/benchmark.json --backend python
python3 scripts/compare_strategies.py --source data/solved/sample_solutions.json --output results/strategy_comparison.json --backend python --seed 7
```

Per usare MiniZinc al posto di Python basta `--backend minizinc`. Il terzo backend `minizinc-api` usa la libreria MiniZinc-Python (`pip install minizinc`).

## Formato dati

JSON. Le griglie sono matrici 9×9; nei puzzle `0` indica una cella vuota, i valori `1..9` gli indizi fissi.
