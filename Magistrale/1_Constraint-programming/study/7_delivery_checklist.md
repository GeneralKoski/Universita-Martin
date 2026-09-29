# Recap Consegna - Progetto 19: Sudoku Instance Generation

Stato del progetto rispetto ai punti della consegna ufficiale. Da rileggere prima dell'orale per avere pronte le risposte sui requisiti.

## Obiettivi generali (dal testo del progetto)

| Requisito | Stato | Dove |
|---|---|---|
| Griglie 9×9 con **≥1 soluzione** | ✅ | `sudoku_solver.mzn` (alldifferent) |
| **Esattamente una** soluzione (unicità) | ✅ | `sudoku_non_unique_check.mzn` + counting |
| **Meno clue possibili** | ✅ | loop greedy `generate_puzzle` |
| Generate **e validate via modello MiniZinc** | ✅ | entrambi i modelli sono MiniZinc |
| Dataset **Kaggle** | ✅ | `import_kaggle_solutions.py` (reservoir sampling) |

## I 4 punti numerati della consegna

| # | Punto | Stato | Note |
|---|---|---|---|
| **1** | "MiniZinc model con linear constraints for capacity and cost" | ✅ *chiarito* | Residuo copia-incolla dal progetto 18 (Transit Line Frequency Optimization). Il Prof. Dal Palù ha confermato via email: ignorare. Il modello reale è il CSP con `alldifferent`. Documentato in `project/sudoku_instance_generation/03_spec_notes.md`. |
| **2** | Misurare **tempo vs clue richiesti** | ✅ | report §6.4 + `plot_time_vs_clues.png` |
| **3** | Valutare **strategie diverse per testare l'unicità** | ✅ | counting vs solve-and-block (report §3.1/§3.2) + le 3 strategie di rimozione (random/symmetry/density) |
| **4** | Report **6-10 pagine** + zip con programmi/dataset/report | ✅ | report = 9 pagine; zip pronto |

## Stato complessivo

```
✅ Codice           completo (5 modelli MiniZinc + pipeline Python)
✅ Report           9 pagine, dentro il range 6-10
✅ Zip consegna     pronto (sudoku_instance_generation.zip)
✅ Esperimenti      120 run (20 griglie × 3 strategie × 2 metodi)
✅ Studio codice    completato (cap. 1 modelli + cap. 2 funzioni Python)
⏳ Studio teoria    documento 3 (3_oral_theory_notes.md) da ripassare
⏳ Rilettura report da fare una volta prima del 12 giugno
```

## L'unico punto delicato da avere pronto all'orale

Il **punto 1** ("linear constraints for capacity and cost"). Risposta pronta:

> *"Era un residuo di copia-incolla dal progetto 18 (Transit Line Frequency Optimization); lei ha confermato via email di ignorarlo. Il Sudoku non ha dimensioni di capacità o costo - è un problema di pura soddisfazione, modellato con `alldifferent`."*
