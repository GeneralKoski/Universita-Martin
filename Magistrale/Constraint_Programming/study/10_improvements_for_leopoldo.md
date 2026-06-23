# Migliorie post-consegna (per l'orale di Leopoldo)

Tre estensioni prese dalla sezione "Possible extensions / Limitations" del report, implementate in `scripts/sudoku_pipeline.py`. Tutto gira nel venv del progetto: `.venv/bin/python` (creato con `python3 -m venv .venv && .venv/bin/pip install minizinc`).

## 1. Backend `minizinc-api` (MiniZinc-Python) — risultato negativo ma onesto

Il report ipotizzava: "integrate MiniZinc-Python to cut the subprocess overhead". Implementato come terzo backend:

```
.venv/bin/python scripts/sudoku_pipeline.py check --input data/generated/demo_puzzle.json --backend minizinc-api --method counting
.venv/bin/python scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output /tmp/x.json --backend minizinc-api --strategy random --seed 7
```

**Misura (stessa run, seed 7, stesso puzzle prodotto):**

| Backend | Tempo totale | Per check |
|---|---|---|
| `minizinc` (subprocess) | 15.4 s | ~0.19 s |
| `minizinc-api` | 27.7 s | ~0.34 s |

**Finding**: l'ipotesi del report era sbagliata sul componente dominante. `minizinc-python` *non* incorpora libminizinc: avvolge la CLI, quindi flattening + spawn del processo avvengono comunque a ogni solve, più l'overhead asyncio della libreria. Il costo dominante è la **flattening per-check**, non la gestione del sottoprocesso da Python. La soluzione vera sarebbe un solver persistente o binding diretti a Gecode (il report già lo diceva: "or Gecode directly").

**Da dire all'orale**: "We implemented the proposed extension and measured it: it was ~1.8× *slower*. The lesson is that minizinc-python wraps the CLI rather than embedding the compiler, so the per-check flattening cost remains. Negative results are still results — the experiment falsified our own hypothesis about where the overhead was."

## 2. Backtracking sulla rimozione: `--optimize-attempts N`

Attacca la limitation "minimum clue count far from the theoretical limit of 17". Strategia *add-one-remove-many* (plateau escape):

1. dopo la passata greedy, si **ri-aggiunge** un indizio rimosso (scelto a caso) — l'unicità è preservata per costruzione;
2. si rilancia una passata di rimozione greedy **in un nuovo ordine casuale**;
3. se la passata rimuove ≥2 celle il netto è negativo (meno clue) → si tiene; altrimenti rollback.

```
.venv/bin/python scripts/sudoku_pipeline.py generate --source data/solved/sample_solutions.json --output /tmp/x.json --backend python --strategy random --seed 7 --optimize-attempts 100
```

**Risultati finali (benchmark su 50 griglie, 100 attempts, backend python, ~30 s/griglia):**

| Configurazione | Media | Min | Max |
|---|---|---|---|
| Solo greedy | 24.5 | 22 | 27 |
| Greedy + optimization | **22.1** | **20** | 25 |

**47/50 run migliorate**, guadagno medio 2.4 clue, nuovo minimo **20** — mai raggiunto dal greedy puro in 1500 run del benchmark. Tutti i puzzle verificati `unique`. Il JSON di output ha un campo `optimization` con before/after/attempts/checks. Dati: `results/optimization_benchmark.csv`.

**Nota sui tre numeri di "minimo" (per non confondersi all'orale):**
- **22** = minimo greedy nella prima versione del report (50 run soltanto)
- **21** = minimo greedy ora (benchmark da 500 griglie = 1500 run): è un outlier fortunato che capita 1 volta su 1500 — col campione piccolo non si vedeva, con 1500 run salta fuori. Media e tipico restano 24.4 / 22-23.
- **20** = minimo con l'ottimizzazione (§7.1), metodo diverso che gira dopo il greedy.

Se chiedono "perché il minimo è 21 e non meno": *"it's a rare lucky greedy run, once in 1500 attempts; the typical best is 22-23. The minimum is grid-determined, and pushing lower needs the optimization pass (down to 20) or exact methods."*

**Perché funziona (da dire all'orale)**: la rimozione greedy è order-dependent e si ferma in un minimo locale; ri-aggiungere una cella e ripartire con un ordine diverso permette di uscire dal plateau. È una forma semplice di local search sopra la ricerca CP.

### 1b. Ricerca più forte: variable-neighbourhood e branch-and-bound (§7.4)

Due tentativi di battere la local search base, confrontati su **408 griglie fresche dai 9M Kaggle**:

| Metodo | Media | Min | Tempo |
|---|---|---|---|
| greedy | 24.41 | 21 | — |
| local search (readd 1) | 22.08 | 20 | 49s |
| **VNS (readd ≤3)** | **21.54** | **20** | 51s |
| branch-and-bound (8k nodi) | 21.51 | 20 | 92s |

Comandi: `--optimize-readd 3` (VNS) e `--bnb-nodes 8000` (B&B).

**Due conclusioni oneste:**
- **VNS funziona**: allargare il vicinato (riaggiunge fino a 3 celle) abbassa la media, meglio di v1 su **192 griglie su 408** (~47%), peggio solo su 37.
- **B&B NON serve**: pari a VNS su **396 su 408**, meglio solo su 12, a costo quasi doppio. Lo spazio dei sottoinsiemi è enorme (~81-choose-22), quindi con qualunque budget di nodi la ricerca ne esplora solo una frazione minima. Per arrivare a 17 servono metodi esatti (unavoidable sets, McGuire), non più forza bruta.

**Distribuzione clue VNS (408 griglie):** 20→18, 21→176, 22→191, 23→22, 24→1. Cioè ~98% cade a 20-22; minimo pratico **20** (il 19 visto nel campioncino da 20 griglie era un outlier non riprodotto su scala grande).

È il secondo "negative result" del progetto (come MiniZinc-Python): **misurare prima di credere**. Dati: `results/overnight_comparison.csv`.

## 3. Simmetrie: sottocomando `augment` — griglie complete senza Kaggle

Attacca la limitation "richer Sudoku symmetries were not explored". Trasformazioni che preservano la validità: permutazione delle cifre, permutazione delle righe dentro le bande, permutazione delle bande, trasposizione (che copre il lato colonne) — composte in ordine casuale.

```
.venv/bin/python scripts/sudoku_pipeline.py augment --input data/solved/sample_solutions.json --output /tmp/augmented.json --count 20 --seed 42
.venv/bin/python scripts/sudoku_pipeline.py generate --source /tmp/augmented.json --output /tmp/x.json --backend python --strategy random --seed 3
```

Testato: 20/20 griglie prodotte sono soluzioni valide (validazione interna con `is_valid_solution`, errore se una trasformazione rompe i vincoli) e **nessuna coincide con le griglie sorgente**. L'output è nello stesso formato `{"grids": [...]}`, quindi si usa direttamente come `--source` di `generate`.

**Collegamento d'oro per l'orale**: questa è esattamente la domanda che il prof ha fatto a Martin ("avrebbe senso sfruttare la simmetria per guadagnare tempo?"). Risposta implementata: le simmetrie moltiplicano le griglie complete a costo ~zero (nessuna chiamata al solver), rendendo la pipeline indipendente da Kaggle. Nota onesta: le griglie trasformate sono *imparentate* strutturalmente con l'originale, non campioni indipendenti — per il benchmark statistico Kaggle resta preferibile (ed è richiesto dalla consegna).

## 4. Benchmark esteso (aggiunto dopo)

Il dataset Kaggle ha **9 milioni** di righe (non 1M come diceva la prima versione del report — corretto). Il benchmark principale ora gira su **500 griglie campionate = 3000 run** (~10 min). Frase chiave da orale: "at n=500 the standard error of the mean is below 0.05 clues, so a larger sample would not change any reported figure" — e la prova empirica è in `results/full_benchmark_1000.csv` (1000 griglie, 6000 run, ~20 min):

| Metrica | 500 griglie | 1000 griglie |
|---|---|---|
| Random mean | 24.37 | 24.36 |
| Symmetry mean | 27.51 | 27.63 |
| Density mean | 25.55 | 25.62 |
| Counting mean/check | 2.02 ms | 1.99 ms |
| Solve-and-block mean/check | 3.59 ms | 3.54 ms |

Raddoppiando il campione nessuna cifra si sposta oltre 0.12: le statistiche sono convergenti, il campione non è il fattore limitante. Ottimo esempio di *dimensionamento* di un esperimento.

## Cosa NON è cambiato

- Nessun comportamento esistente è stato toccato: i default restano identici (`--optimize-attempts 0`, backend `python`), quindi tutti i comandi della demo originale producono gli stessi risultati.
- I modelli `.mzn` sono invariati.
