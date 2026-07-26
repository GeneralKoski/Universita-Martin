# 10 - Simulazione d'esame

> **Scritto: giovedì 17 settembre 2026.** Da calendario (`../README.md`): 1ª simulazione nella settimana 31 ago - 6 set, 2ª e 3ª fra l'11 e il 16 settembre, dopo l'orale di LIC.

Quando arrivi qui, hai studiato tutto. Ora alleni la **resistenza** e la **gestione del tempo**.

## Risorsa principale
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` (48 pp.) - tracce risolte degli anni passati
- 📂 `Appunti_colleghi/Zip_appunti/NICOLODI REVISIONI 1.pdf` (18 pp.)

## Tracce più rappresentative

Non tutte le tracce valgono uguale. Dal censimento in [`00_ANATOMIA_ESAME.md`](00_ANATOMIA_ESAME.md):

- **I Esonero, 3 maggio 2022** (foto in `Appunti_colleghi/Zip_appunti/parziale/`) - la più vicina al formato attuale: Floyd-Warshall parziale, TSP 1-albero, una dimostrazione sul rilassamento, una modellazione applicata (sostituzione macchinari → cammino minimo + Dijkstra), un set covering, più una dimostrazione facoltativa sulle condizioni di ottimalità lagrangiane.
- **13 luglio 2005** - BFS a livelli, Floyd-Warshall parziale, MST, zaino 0-1 con duale lagrangiano completo. Copre da sola quasi tutto il blocco grafi.
- **9 febbraio 2006** - Floyd-Warshall con due cicli negativi + zaino 0-1 con `L*(μ)` a tratti e grafico.

## Modalità (da scheda ufficiale + indicazioni colleghi)
- **Scritto**: risoluzione esercizi (algoritmi sui grafi + formulazione PI)
- **Orale**: argomenti teorici + applicazioni
- Per studenti di Scienze Informatiche (6 CFU): probabilmente **un esercizio in meno** rispetto ai gestionali (9 CFU)
- Argomenti divisi in 2 macro-categorie:
  1. Algoritmi sui grafi (BFS/DFS, Bellman, Dijkstra, Floyd–Warshall, MST)
  2. Programmazione intera & ottimizzazione combinatoria

## Strategia di esecuzione
1. Stampare 2-3 tracce d'esame complete dal PDF degli esami risolti
2. **Coprire le soluzioni**, mettere un timer (90-120 min, come l'esame reale)
3. Risolvere e poi confrontare con la soluzione svolta

## Per l'orale (ripasso definizioni e dimostrazioni)
- Teorema di Eulero
- Lemma BFS (livelli ↔ distanza geometrica)
- Principio di ottimalità di Bellman + dimostrazione
- Unicità soluzione equazioni Bellman + dimostrazione
- Correttezza Dijkstra (lemma + dimostrazione, ruolo di ℓ ≥ 0)
- Formula ricorsiva di Floyd–Warshall (giustificazione)
- Lemma fondamentale degli MST + dimostrazione
- Proprietà 1, 2, 3 dei rilassamenti
- Dualità debole (definizione + criterio di ottimalità)

## Domande tipiche di apertura orale
- "Mi parli del problema dei cammini minimi e di quale algoritmo usare in che condizioni"
- "Cos'è un rilassamento e a cosa serve?"
- "Differenza tra rilassamento lineare e rilassamento lagrangiano"
- "Mi disegni un grafo e formuli il TSP"

## Tempo stimato: 2-3 sessioni di simulazione complete (~6-8 ore)
