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

Calibrazione `2026-09-25T131533Z_calibrazione.json`, da `calibra.py` al commit
`f288962` (albero pulito), sulle 57 valutazioni di `calibrazione-fusione/`
(Koskidex `d3ffe17`). Esito sul test `2026-09-25T131731Z_esito.json`, da
`analizza.py` allo stesso commit, sulle dieci valutazioni delle 13:16-13:17 UTC
più le tre U del difetto 2. Un primo lancio di `calibra.py` si è fermato sul proprio controllo
prima di stampare un numero: le esecuzioni convesse non registrano
`vettori_k` (`evaluate` lo scrive solo con `-ibrido`), corretto in un commit a
parte.

**La calibrazione**, nDCG@10 (MRR@10 per le known-item) sugli split separati:

| costante della somma | 0 | 5 | 10 | 20 | 40 | 80 | 160 | 320 |
|---|---|---|---|---|---|---|---|---|
| SciFact train | 0,678 | 0,686 | 0,696 | 0,708 | 0,723 | 0,742 | **0,753** | 0,750 |
| NFCorpus dev | 0,276 | 0,297 | 0,303 | 0,313 | 0,321 | 0,326 | **0,326** | 0,320 |
| known-item train | 0,861 | 0,867 | **0,872** | 0,868 | 0,814 | 0,690 | 0,505 | 0,353 |

| α (peso del lessicale) | 0 | 0,2 | 0,4 | 0,5 | 0,6 | 0,8 | 0,9 | 1 |
|---|---|---|---|---|---|---|---|---|
| SciFact train | 0,712 | 0,731 | 0,743 | **0,748** | 0,745 | 0,720 | 0,703 | 0,678 |
| NFCorpus dev | 0,303 | 0,317 | 0,320 | **0,323** | 0,320 | 0,307 | 0,299 | 0,276 |
| known-item train | 0,195 | 0,283 | 0,444 | 0,579 | 0,719 | 0,850 | **0,863** | 0,861 |

**Sul test:**

| | U (somma, 20) | somma calibrata | RRF | convessa 0,5 | convessa calibrata |
|---|---|---|---|---|---|
| SciFact nDCG@10 | 0,6913 | **0,7067** (160) | 0,6866 | 0,7025 | 0,7025 (0,5) |
| NFCorpus nDCG@10 | 0,3340 | 0,3441 (160) | **0,3447** | 0,3416 | 0,3416 (0,5) |
| known-item MRR@10 | 0,8464 | **0,8499** (10) | 0,4623 | 0,5723 | 0,8466 (0,9) |

**Il 20 era sbagliato di un fattore otto per le query in lingua naturale e
giusto, per caso, per quelle identificative. Nessuna fusione con un parametro
unico va bene per tutte e due.** Calibrare la costante vale +0,015 su SciFact e
+0,010 su NFCorpus sul test; la stessa costante, 160, sulle known-item porta
l'MRR da 0,87 a 0,50. RRF, che di parametri non ne ha, fa come la somma
calibrata su NFCorpus e sotto U su SciFact, e dimezza le known-item. La
normalizzazione della convessa non risolve: α 0,5 va bene per le collezioni
pubbliche e sulle known-item fa 0,57, serve 0,9.

La scala che conta non è quella fra SciFact e NFCorpus, query lunghe contro
query corte: lì la costante migliore è la stessa. È quella fra i tipi di
query. Su una query identificativa il vettore non sa niente del numero e va
tenuto basso; su una in lingua naturale va pesato otto volte di più di oggi.
È la stessa divisione di `2026-09-25_scelta-per-query/`, che sceglieva fra
`any` e `all`: il peso del vettore è un secondo parametro da scegliere per tipo
di query, con lo stesso classificatore.

### Le previsioni

1. Costante migliore diversa di almeno quattro volte fra SciFact e NFCorpus:
   **160 su entrambe, smentita.** La lunghezza delle query non sposta la
   costante; il tipo di query sì (10 sulle known-item).
2. α migliori entro 0,2: **0,5 su entrambe, confermata**, ma senza il merito
   che le davo: anche le costanti coincidono.
3. Sulle known-item α almeno 0,8 e costante al più 10: **0,9 e 10,
   confermata.**
4. Trasferire la costante costa più che trasferire α: **nessuna delle due
   costa niente, smentita**, per la stessa ragione della 1.
5. RRF almeno 0,005 sopra U su SciFact e NFCorpus, almeno 0,05 sotto sulle
   known-item: **smentita su SciFact** (-0,0047), confermata su NFCorpus
   (+0,0107) e sulle known-item (-0,384, molto oltre).
6. La convessa calibrata almeno 0,005 sopra U sulle pubbliche, non più di
   0,005 sotto sulle known-item, almeno pari a RRF sulle pubbliche:
   **+0,0112 e +0,0076, +0,0001, confermata; pari a RRF solo su SciFact**
   (su NFCorpus 0,0031 sotto).
7. Le fusioni nuove costano meno di 2 ms in più di U: **costano meno di U**,
   da 1 a 7 ms, confermata. La somma calcola la similarità di ogni candidato
   lessicale e poi scandisce tutti i vettori per i vicini; le fusioni nuove
   scandiscono una volta sola.

### Cosa vuol dire per la tesi

Il difetto 3 c'è ed è misurato: la costante a occhio lasciava sul tavolo
+0,015 e +0,010 di nDCG@10 sulle collezioni pubbliche, e nessuna delle
alternative della letteratura (RRF, somma normalizzata) è indipendente dal tipo
di query. La correzione non è una formula ma una scelta: il peso del vettore
per tipo di query, da aggiungere alla scelta di `2026-09-25_scelta-per-query/`
e da rifare sulle known-item scritte da persone. Tutti i flag restano spenti
per default: i default si decidono alla fine, con il relatore.

