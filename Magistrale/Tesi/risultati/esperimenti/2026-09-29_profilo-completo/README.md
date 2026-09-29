# Il profilo completo, misurato dall'app

**Domanda.** Sulle 104 known-item umane Koskidex innestato con il profilo
consigliato fa 0,432 di MRR@10, e lo stesso motore fuori dall'app fa 0,559 con
BM25 e il recupero disgiuntivo (LA) e 0,613 con in più i vettori (A)
(`2026-09-25_known-item-umane/`). Il limite che resta a Documentale è il
recupero congiuntivo, che però protegge le ricerche per numero d'atto: fuori
dall'app, sulle 300 `<numero> <comune>`, LA fa 0,833 contro 0,960 del
congiuntivo LT. Dentro l'app, con i refusi, i pesi dei campi, l'elisione e i
numeri esatti del profilo, quanto vale portare BM25, il recupero disgiuntivo e
i vettori? E quale profilo tiene insieme le ricerche per contenuto e quelle per
numero?

Scritto il 29/09/2026, prima di toccare il codice di Documentale e prima di
qualunque misura.

## La modifica in Documentale

Nuove variabili, tutte spente per default e **fuori dal profilo consigliato**,
così nessun comportamento di oggi cambia:

- `KOSKIDEX_RETRIEVAL_MODE` (`all` per default, o `any`): il recupero;
- `KOSKIDEX_SCORING` (vuoto per default, cioè il punteggio euristico, o
  `bm25`): con `bm25` l'indice riceve anche `bm25_k1` 1,2, `bm25_b` 0,75 e
  la frequenza mescolata (`bm25_expansion: blended`), perché un
  aggiornamento delle impostazioni che non li passa li lascia a zero;
- `KOSKIDEX_STABLE_TERM_ORDER` (spento per default): i termini trovati in
  ordine lessicografico, che con BM25 decide le statistiche a parità di
  distanza (`2026-09-28_ordine-fisso`);
- `KOSKIDEX_VECTOR_WEIGHT` (vuoto per default, cioè 20): il peso del vettore
  nella somma, solo con un modello di embedding.

Un test di `KoskidexServiceTest` per le variabili nuove, che fallisce prima
della modifica.

## I profili

Tutti dall'app, ciascuno su un indice vuoto riempito dall'app, Koskidex del
commit corrente, `KOSKIDEX_PROFILO=consigliata` più:

| | variabili in più | corrisponde a |
|---|---|---|
| **P0** | nessuna | KC di `2026-09-25_known-item-umane/` |
| **P1** | `NORMALIZE_DATES`, `NORMALIZE_AMOUNTS`, `TYPOS_ON_AMOUNTS=false` | le correzioni di date e importi (`2026-09-28_date-app`, `2026-09-28_importi-esatti`) |
| **P2** | P1 + `RETRIEVAL_MODE=any`, `SCORING=bm25`, `STABLE_TERM_ORDER` | LA dall'app |
| **P3** | P2 + `EMBEDDER_MODEL=bge-m3`, `HYBRID_MODE=union`, `VECTOR_WEIGHT=160` | A dall'app |
| **P4** | P1 + `SCORING=bm25`, `STABLE_TERM_ORDER`, `EMBEDDER_MODEL=bge-m3`, `HYBRID_MODE=union`, `VECTOR_WEIGHT=10` | B dall'app (congiuntivo) |

Stopword e stemmer italiani restano fuori: con il recupero disgiuntivo
spostano l'MRR@10 di meno di 0,011 (`2026-09-25_italiano-umane/`).

## Come si misura

`esegui.sh`: per ogni profilo un Koskidex nativo con una cartella di dati
vuota, l'indice riempito dall'app (`strumenti/indicizza-koskidex.sh`, il tempo
va in `confronto/`), le impostazioni rilette dall'indice, poi dall'app
(`app:eval-run-queries`) le known-item automatiche, le umane, le date e gli
importi sintetici e le 24 del confronto; le prime quattro si valutano con
`scripts/evaluate -rankings -top 10`. `analizza.py` riassume MRR@10, atto
primo, entro dieci, a vuoto e la mediana del tempo di ricerca dall'app per
profilo e collezione, e controlla le previsioni.

## Prima di misurare

1. **P1 non tocca le query umane né quelle per numero**: sulle umane MRR@10
   entro 0,005 da P0, e sulle automatiche MRR@10 almeno 0,950. Date almeno
   0,95 e importi almeno 0,95 di MRR@10 (`date-app` e `importi-esatti`).
2. **P2, le umane**: MRR@10 almeno 0,50 e al più il 3% di query a vuoto. Fuori
   dall'app LA fa 0,559 con l'1% a vuoto; nell'app i refusi aggiungono
   candidati e rumore, e tolgo qualcosa.
3. **P2, le automatiche**: MRR@10 almeno 0,03 sotto P1. Con il recupero
   disgiuntivo un atto che ha solo il comune o solo un numero simile entra fra
   i candidati, come in LA fuori dall'app.
4. **P3, le umane**: almeno 0,03 sopra P2, e l'atto entro dieci in almeno
   l'80% delle query (fuori dall'app A fa +0,054 su LA e l'86%).
5. **P3, le automatiche**: MRR@10 al più 0,80. Un vettore pesato 160 pesa più
   del numero, come fuori dall'app, dove A sulle known-item fa molto peggio di
   LA.
6. **P4**: sulle automatiche MRR@10 almeno 0,94, sulle umane almeno 0,50. È
   la configurazione per gli identificativi, che fuori dall'app non perde sulle
   known-item e sulle frasi umane sta a 0,006 da A.
7. **Le date in P4** almeno 0,95 di MRR@10, come in P1: il recupero
   congiuntivo con le date normalizzate le trova, e il vettore pesato 10 non
   le sposta.

**La regola di scelta**, scritta prima: il profilo da proporre è quello con
l'MRR@10 più alto sulle umane fra quelli che sulle automatiche stanno entro
0,01 da P1 e sulle date e sugli importi sopra 0,95. Se nessuno dei profili
nuovi ci sta, resta P1, e il limite del recupero congiuntivo va scritto come
il prezzo delle ricerche per numero. Il profilo consigliato di Documentale non
cambia qui: lo sceglie la tesi, e lo conferma il relatore.
