# Generazione di Istanze Sudoku - Note sulla Specifica

## Punto 1 della consegna (chiarito con il docente)

Il testo del progetto 19 contiene la frase:

> "Implement a MiniZinc model using linear constraints for capacity and cost."

Era un residuo di copia-incolla dal progetto 18 (Transit Line Frequency Optimization). Il Prof. Dal Palù ha confermato via email: *"Ignora pure quella riga."*

Il punto 1 va quindi inteso come "modello MiniZinc che decide la soddisfacibilità del Sudoku via `alldifferent`", senza alcun termine di ottimizzazione lineare aggiuntivo.

## Dataset di Riferimento

La specifica del progetto rimanda al Kaggle Sudoku Dataset pubblico:

- https://www.kaggle.com/datasets/rohanrao/sudoku

Contiene soluzioni complete di Sudoku e viene usato come sorgente di griglie complete valide da cui derivare i puzzle. Questo evita di spendere tempo del solver solo per generare nuove griglie complete e rende gli esperimenti più riproducibili. Il modello `sudoku_generate_full_grid.mzn` resta disponibile come fallback e come verifica autonoma della correttezza strutturale.

## Deliverable

La consegna finale è un unico file zip contenente:

- Uno o più modelli MiniZinc
- Lo script di orchestrazione usato per gestire la pipeline di generazione
- Il dataset e le istanze di benchmark generate
- I risultati sperimentali
- Un report scritto di 6-10 pagine

Il report descrive i modelli, le scelte implementative, la strategia di unicità, la strategia di rimozione degli indizi e i risultati sperimentali.

## Vincoli Sperimentali

La specifica del progetto richiede:

- Controlli di unicità sui puzzle generati
- Minimizzazione del numero di indizi
- Un confronto tra diverse strategie
- Un limite di 5 minuti per ogni test di benchmark
- Un'analisi che colleghi il tempo di generazione al numero di indizi rimanenti
