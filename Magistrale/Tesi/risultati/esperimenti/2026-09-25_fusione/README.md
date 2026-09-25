# Difetto 3: fondere scale incomparabili

**Domanda.** Koskidex fonde lessicale e vettore con `punteggio + sim * 20`. Il
punteggio lessicale (BM25) cresce con la lunghezza della query e con la
collezione, la similarità coseno sta fra -1 e 1, e il 20 è una costante messa a
occhio. In `2026-09-25_ibrido-unione/` questa fusione ha già dato +0,022 su
SciFact e +0,024 su NFCorpus: il 20 è giusto per caso, o una fusione che non
dipende dalle scale fa meglio? E una costante unica può andare bene per
collezioni diverse?

## Metodo

- **Tre fusioni** in Koskidex, dietro `Settings.FusionMode`, con quella di oggi
  come default:
  - vuoto (**S**, somma, oggi): lessicale + `sim * VectorWeight`, e
    `Settings.VectorWeight` vuoto vale 20, cioè il codice di oggi;
  - `rrf` (**RRF**): Reciprocal Rank Fusion, `1/(60 + posizione lessicale) +
    1/(60 + posizione vettoriale)`, con la costante 60 di Cormack, Clarke e
    Büttcher (2009), la stessa predefinita di Elasticsearch;
  - `convex` (**C**): ciascuna lista normalizzata min-max sui propri
    candidati, poi `α · lessicale + (1 - α) · vettore`, come la
    `relativeScoreFusion` di Weaviate; `Settings.FusionAlpha`, vuoto vale 0,5,
    come il `semanticRatio` predefinito di Meilisearch.
  - In tutte e due le fusioni nuove i candidati sono l'unione (i lessicali più
    i 100 più vicini, come `HybridMode = union`), e un documento assente da
    una lista prende zero da quella lista.
- **Stessa base del difetto 2**: BM25 `any`, frequenza mescolata, nessuna
  analisi, refusi spenti, `bge-m3` digest `790764642607` dalla cache, i 100
  più vicini. Il confronto è con **U**, l'unione con la somma di oggi
  (SciFact 0,6913, NFCorpus 0,3340, known-item 0,8464).
- **Calibrazione su split separati, mai sul test**: SciFact train (809 query),
  NFCorpus dev (324), known-item train (300, `known-item-auto-train`, nessun
  atto in comune con il test). Due griglie, fissate qui:
  - la costante della somma, `VectorWeight` ∈ {0, 5, 10, 20, 40, 80, 160, 320};
  - il peso della fusione convessa, `α` ∈ {0; 0,1; ...; 1}.
  Il valore migliore di ciascuna griglia, per collezione, si misura poi una
  volta sul test. Le esecuzioni di calibrazione vanno in un archivio a parte,
  `calibrazione-fusione/`.
- **Sul test**, per collezione: S con la costante calibrata, RRF, C con α 0,5,
  C con α calibrato.

**Aggiunto dopo le ipotesi, prima di vedere un solo numero della
calibrazione.** A parità di metrica vince il valore più vicino al predefinito
del motore (20 per la costante, 0,5 per α): la calibrazione non sposta il
comportamento di oggi senza un guadagno. U sul test è quella già archiviata
col difetto 2 (Koskidex `f5ce77f`): con il codice delle fusioni (`d3ffe17`)
una prova di sviluppo su SciFact la riproduce identica, metriche e primi dieci.
Script: `calibra.py` sceglie i valori, `analizza.py` confronta sul test.

## Prima di misurare

Scritto e committato prima di scrivere il codice.

1. **Nessuna costante unica**: la costante migliore della somma differisce
   almeno di un fattore 4 fra SciFact e NFCorpus, più alta su SciFact, dove le
   query sono lunghe (mediana 12 termini) e BM25 dà punteggi grandi, che su
   NFCorpus (mediana 2).
2. **La normalizzazione rende i pesi confrontabili**: l'α migliore di SciFact e
   quello di NFCorpus distano al più 0,2.
3. **Sulle known-item il lessicale deve dominare**: α migliore almeno 0,8 e
   costante migliore al più 10.
4. **Trasferire la costante costa più che trasferire α**: sulla calibrazione di
   NFCorpus, usare la costante migliore di SciFact perde più nDCG@10 che usare
   l'α migliore di SciFact.
5. **RRF sul test**: supera U di almeno 0,005 di nDCG@10 su SciFact e su
   NFCorpus, e perde almeno 0,05 di MRR@10 sulle known-item, dove la
   posizione vettoriale dell'atto giusto è pessima (il solo vettore fa 0,18) e
   RRF la pesa quanto quella lessicale.
6. **C con α calibrato sul test**: almeno 0,005 sopra U su SciFact e NFCorpus,
   e non più di 0,005 sotto U sulle known-item; su SciFact e NFCorpus almeno
   pari a RRF.
7. **Costo**: la mediana del tempo per query delle fusioni nuove supera quella
   di U di meno di 2 ms.

Se cadono la 1 e la 2 insieme, le scale non sono il problema: il 20 andrebbe
bene ovunque, e il difetto 3 si ridimensiona a una costante da scegliere.

## Esito
