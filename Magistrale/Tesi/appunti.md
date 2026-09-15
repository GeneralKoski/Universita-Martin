# Tesi magistrale - appunti

Raccolta di appunti sulla scelta dell'argomento di tesi. Non è ancora un
progetto: è il diario delle idee valutate e del perché sono state tenute o
scartate.

## Criterio di scelta

Una tesi magistrale non ha bisogno di software che funziona, ha bisogno di:

1. una **domanda** precisa,
2. un **metodo** per rispondere,
3. una **valutazione misurabile** del risultato.

Un progetto grande e ben fatto ma senza domanda resta una tesi progettuale.
Ogni candidato qui sotto è giudicato con questo metro.

## Contesto voto

Dal `CLAUDE.md` del repo: partenza ~102,66 + 3 (in corso) = 105,66. Servono
**4 punti tesi per il 110**, 7 per la lode. Quindi la tesi pesa, e una tesi con
misure e un contributo difendibile vale più di una tesi applicativa.

## Candidati valutati (15 settembre 2026)

Passati in rassegna tutti i repo personali sull'account GitHub `GeneralKoski`.

### Traccia aperta: Koskidex

Motore di ricerca full-text self-hosted scritto in Go (~130k righe), binario
singolo senza dipendenze a runtime. Ha già tolleranza ai refusi, faccette e
ricerca vettoriale.

L'ingegneria c'è. Manca tutta la parte che lo rende una tesi:

- valutazione IR su dataset standard (BEIR, MS MARCO)
- curve **recall@k contro latenza**, non solo "è veloce"
- confronto con Meilisearch / Tantivy / Elasticsearch
- studio della **fusione lessicale + densa**: RRF contro pesatura, dove il
  vettoriale aiuta davvero e dove peggiora i risultati

Quest'ultimo punto è il candidato più forte a diventare *la* domanda di tesi.

### Parcheggiato: gpu-quant-bench

Benchmark di formati e quantizzazioni di un modello 7B su una RTX 3060 (12 GB):
FP16, GGUF Q8_0/Q5_K_M/Q4_K_M, GPTQ 4-bit, AWQ 4-bit, su contesti da 512, 2048
e 8192 token.

È l'unico repo nato già in forma di studio sperimentale, con domanda, variabili
controllate e metriche definite (throughput, TTFT, prefill, VRAM di picco,
perplexity). Il contributo metodologico interessante è riportare **varianza** e
**throttling termico**, che i benchmark pubblicati quasi sempre omettono.

**Non è la tesi.** È lo step 1 di un percorso di studio ML più lungo, descritto
nel repo `ml-notes`. Se in futuro dovesse servire come base di tesi, le
direzioni per irrobustirlo sono: più modelli, una seconda GPU per generalizzare,
valutazione di qualità oltre la perplexity (task downstream, non solo control
prompt letti a mano) e analisi energetica (J/token), che oggi manca ed è
l'angolo più facile da difendere.

### Scartati

| Progetto | Motivo |
|---|---|
| sudoku-instance-generation / Constraint_Programming | Esame del primo anno, già valutato. Fuori discussione. |
| MelaGolfo | Scartato. |
| KalTrack, unidesk, unidesk-mobile, Hydran, PiacenzAdvisor, PizzaGigante, Klipski, Chesso, Automarket, metin, Personal-website | Scartati: product engineering, integrazione o esercizi, nessuna domanda di ricerca. |

## Prossimi passi

- [ ] Approfondire la traccia Koskidex e decidere la domanda precisa
- [ ] Individuare il relatore adatto (area IR / sistemi)
- [ ] Verificare che l'argomento non si sovrapponga a tesi già assegnate

## Nota organizzativa

La tesi sta **tutta qui dentro**, in `Magistrale/Tesi/`: appunti ora, e più
avanti anche il codice e la scrittura. Niente repo separata e niente repo
annidata (git non gestisce le repo dentro le repo). `Universita-Martin` è il
percorso universitario nella sua interezza, e la tesi ne fa parte.
