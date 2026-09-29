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

## Esito

Misurato il 29/09/2026 fra le 12:31 e le 12:49, Koskidex `0e914f5`, Documentale
`fd5fb45`, bge-m3 su Ollama per P3 e P4. Riassunto in
`2026-09-29T104931Z_esito.json` (`analizza.py`); rapporti in `confronto/`,
valutazioni in `evaluate/`. I rapporti sulle umane contengono il testo delle
query e restano fuori da git. Le impostazioni rilette dall'indice di ogni
profilo corrispondono alla tabella dei profili.

MRR@10, con fra parentesi le ricerche a vuoto:

| | automatiche (300) | umane (104) | date (450) | importi (104) | ricerca dall'app, umane | indicizzazione |
|---|---|---|---|---|---|---|
| P0 | 0,9498 | 0,4317 (29,8%) | 0,3153 (50,4%) | 0,9167 | 3,82 ms | 1,8 s |
| P1 | 0,9551 | 0,4317 (29,8%) | 0,9789 (0,7%) | 0,9904 | 3,75 ms | 1,9 s |
| P2 | 0,1468 | 0,5024 (0%) | 0,4781 | 0,7007 | 8,52 ms | 2,0 s |
| P3 | 0,1783 | 0,5758 (0%) | 0,6007 | 0,6674 | 47,62 ms | 488,5 s |
| P4 | **0,9556** | **0,6073 (0%)** | **0,9847** | **0,9904** | 41,94 ms | 476,7 s |

**Sei previsioni su sette, la regola di scelta dà P4.**

1. **Confermata.** P1 lascia le umane a 0,4317 come P0 e porta le automatiche
   a 0,9551, le date da 0,3153 a 0,9789, gli importi da 0,9167 a 0,9904.
2. **Confermata.** P2 sulle umane 0,5024, nessuna ricerca a vuoto: sotto LA
   fuori dall'app (0,559) come avevo previsto, ma sopra KC (0,432).
3. **Confermata, molto di più.** P2 sulle automatiche crolla da 0,9551 a
   0,1468, non di 0,03. Anche le date (0,4781) e gli importi (0,7007) perdono
   molto. La causa non l'ho verificata: nel confronto delle 24 query P2 e P3
   restituiscono tutte le 10.000 risposte in 8 query su 24, P0, P1 e P4 al
   più 449. Con il recupero disgiuntivo una ricerca per numero porta dentro
   ogni atto che ha solo il comune o solo un numero simile, e nell'app il
   punteggio non basta a rimetterli sotto l'atto giusto.
4. **A metà, smentita.** P3 sulle umane sale da 0,5024 a 0,5758 (soglia +0,03
   superata), ma l'atto entro dieci è nel 76,9% delle query, sotto l'80%.
   Dall'app P3 fa 0,576, contro 0,613 di A fuori dall'app.
5. **Confermata.** P3 sulle automatiche 0,1783: il vettore a 160 non le
   salva.
6. **Confermata, con un margine.** P4 sulle automatiche 0,9556 (sopra P1) e
   sulle umane 0,6073, uguale a B fuori dall'app (0,607).
7. **Confermata.** P4 sulle date 0,9847, sopra P1 (0,9789).

**Regola di scelta: ammesso solo P4**, che sulle umane fa 0,6073 contro 0,4317
di P1 e 0,3256 di Elasticsearch di produzione (`2026-09-25_known-item-umane`),
senza toccare le ricerche per numero (automatiche 0,9556, importi 0,9904) e
con le date sopra P1. Il profilo consigliato di Documentale non cambia qui.

**Il prezzo di P4**: la ricerca dall'app passa da circa 3,8 ms di mediana a
circa 42 ms, perché ogni query calcola il suo vettore, e l'indicizzazione dei
10.018 atti da 1,9 s a 476,7 s, perché ogni atto ne calcola uno. Richiede Ollama con bge-m3 raggiungibile
dall'applicazione.

P4 ha impiegato quasi quanto P3 (476,7 contro 488,5 s) nonostante `esegui.sh`
copi per P4 la cache dei vettori degli atti calcolata da P3: non ho verificato
se la cache sia stata usata.

**P2 e P3 restano un risultato negativo utile**: il recupero disgiuntivo, che
fuori dall'app porta LA a 0,559, dentro Documentale è inutilizzabile se non si
protegge la ricerca per numero. La strada che funziona è quella congiuntiva
con i vettori, non quella disgiuntiva.
