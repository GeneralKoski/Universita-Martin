# Le prestazioni di Koskidex: prima e dopo

**Domanda.** `2026-09-28_carico` ha misurato che Koskidex alloca circa 2 MB a
ricerca (il 43% in `findDocsForToken`, il 25% in `fuzzyCandidates`, il 15% in
`DamerauLevenshtein`) e che quella memoria costa CPU: il lock dell'allocatore,
il garbage collector, più di un core per una ricerca alla volta, un vantaggio
che sotto carico scende da 3 volte a 1,14 e una coda che cresce con l'archivio.
Togliendo quelle allocazioni, **senza cambiare un solo risultato**, quanto
cambiano tempi, capacità e coda?

Scritto il 28/09/2026, dopo le misure di `2026-09-28_carico` (il "prima") e
prima di scrivere il codice.

## Gli interventi

Tre, uno per commit in Koskidex, nessuno dietro un'impostazione perché nessuno
deve cambiare i risultati:

1. **Distanza e candidati senza allocazioni inutili.** `DamerauLevenshtein`
   con tre righe riusate al posto della matrice intera (la stessa ricorrenza,
   la variante con trasposizioni adiacenti); nella raccolta dei candidati con
   refuso la stringa del prefisso esatto calcolata una volta per termine della
   query invece che per ogni termine del vocabolario, e i bigrammi presi come
   sottostringhe invece che convertiti da rune.
2. **Il congiuntivo guidato dal termine più raro.** Con il recupero
   congiuntivo, senza `minimum_should_match`, i documenti candidati si trovano
   intersecando le liste di posting a partire dal termine con meno posting; i
   punteggi si calcolano poi solo sui candidati, **termine per termine nello
   stesso ordine della query di prima**, così le somme in virgola mobile sono
   le stesse bit per bit.

L'indice compatto (id e campi interi) resta fuori: cambia il formato su disco.

## Come si verifica che i risultati non cambiano

- I test di Koskidex, `TestBaselineRankingIsFrozen` compreso, senza toccarli.
- `scripts/carico -modo risposte`: per ogni query l'impronta SHA-256 dei
  risultati come il server li scrive, id e punteggi byte per byte. Prima (motore
  `ffa38ab`) e dopo, sulle 400 query di `2026-09-28_carico` più le 29 di
  `query-verifica.jsonl` (inventate, con gli operatori `-` e `OR`, parole di una
  lettera, numeri, refusi, parole che non esistono), sull'indice dell'app
  (10.018 atti) e sulla copia da 100.000 documenti.
- `scripts/evaluate` prima e dopo su SciFact, NFCorpus e le known-item
  automatiche dell'albo, nelle configurazioni di confronto (baseline, BM25 con
  recupero congiuntivo e disgiuntivo): le metriche per query devono coincidere.

## Il dopo

Le stesse misure di `2026-09-28_carico`, solo per Koskidex, con lo stesso
strumento: una ricerca alla volta nel container e nativo, sotto carico da 1 a
32 client nel container e nativo, la copia da 100.000 documenti, il profilo a
8 client. Elasticsearch non cambia e resta quello del "prima".

## Prima di misurare

1. **Nessun risultato cambia**: tutte le impronte coincidono, a 10.018 e a
   100.000 documenti; le metriche per query di `scripts/evaluate` coincidono; i
   test passano.
2. **Le allocazioni per ricerca scendono di almeno il 60%** nel profilo a 8
   client (da circa 2,3 MB).
3. **Una alla volta, Koskidex nel container**: p50 da 2,12 ms a non più di
   1,5; p95 da 12,4 a non più di 6.
4. **Capacità nel container, stesse 4 CPU**: il massimo da 653 ricerche al
   secondo ad almeno 900, cioè almeno 1,5 volte le 571 di Elasticsearch (la
   previsione 5 di `2026-09-28_carico`, smentita prima, diventa vera).
5. **Coda sotto carico**: a 32 client il p99 nel container da 215 ms a non più
   di 110, al livello di Elasticsearch (103).
6. **A 100.000 documenti**: p95 da 133 ms a non più di 40, p99 da 201 a non
   più di 60.
7. **Memoria**: a riposo invariata entro il 10% (le strutture dell'indice non
   cambiano); sotto carico il massimo nel container da 355 MB a non più di 300.
8. **Con un client solo** la CPU nel container scende dal 116% a non più del
   100%.

## Esito

*Nota del 29/09/2026, dal terzo controllo della tesi.* I «circa 2 MB a
ricerca» della Domanda sono, nel file, 2,569 MB su 35.913 ricerche
(`allocazioni.prima` dell'esito qui sotto).

Misurato il 28/09/2026: "prima" il motore `ffa38ab` (le misure di
`2026-09-28_carico`; per le impronte e `evaluate`, `d7eaf9a`, stesso codice del
motore), "dopo" `510b9d2`, cioè i due interventi `60f7a43` (distanza e
candidati) e `510b9d2` (candidati del congiuntivo). Gli interventi sono due,
non tre come dice la prima riga della sezione sopra: il terzo, l'indice
compatto, era già escluso lì sotto. Riassunto in `*_esito.json`
(`analizza.py`).

**Otto previsioni su otto confermate**, quasi tutte con molto margine: le
soglie erano prudenti.

1. **Confermata.** Nessun risultato cambia: le impronte coincidono per tutte le
   429 query a 10.018 documenti e per tutte le 429 a 100.000; le metriche di
   `scripts/evaluate`, medie e per query, coincidono nelle 9 combinazioni; i
   test di Koskidex passano, `TestBaselineRankingIsFrozen` senza toccarlo.
2. **Confermata.** Allocazioni per ricerca nel profilo a 8 client da 2,57 a
   0,44 MB, l'83% in meno (soglia 60%).
3. **Confermata.** Una alla volta nel container: p50 da 2,12 a 1,12 ms, p95 da
   12,36 a 2,74, p99 da 18,31 a 4,79.
4. **Confermata.** Capacità nel container da 653 a 2.614 ricerche al secondo,
   4 volte; Elasticsearch come l'app ne fa 571, quindi 4,6 volte (era 1,14).
5. **Confermata.** A 32 client p99 nel container da 215 a 43 ms, meno della
   metà di Elasticsearch (103).
6. **Confermata.** A 100.000 documenti p95 da 133 a 10,4 ms, p99 da 201 a
   15,5. Elasticsearch alla stessa dimensione: 21,1 e 35,9. La coda che
   cresceva di dieci volte con l'archivio ora cresce di quattro, da un punto
   di partenza più basso, e resta sotto quella di Elasticsearch.
7. **Confermata.** A riposo 154,6 contro 154,3 MB a 10.018 documenti (−0,2%),
   1.213 contro 1.184 a 100.000; sotto carico il massimo nel container da 355
   a 272 MB (Elasticsearch circa 1.566; corretto il 29/09/2026, dal terzo controllo della tesi, il JSON dà 1.565,7).
8. **Confermata.** Con un client la CPU nel container dall'116% all'83%.

| | prima | dopo | Elasticsearch come l'app |
|---|---|---|---|
| una alla volta nel container, p50 / p95 / p99 ms | 2,12 / 12,36 / 18,31 | **1,12 / 2,74 / 4,79** | 6,32 / 17,66 / 24,26 |
| nativo, p50 / p95 / p99 ms | 1,78 / 12,43 / 17,43 | 0,78 / 2,27 / 4,15 | |
| ricerche al secondo, massimo nel container | 653 | **2.614** | 571 |
| p99 a 32 client nel container, ms | 215 | **43** | 103 |
| 100.000 documenti, p50 / p95 / p99 ms | 5,44 / 133 / 201 | **1,72 / 10,4 / 15,5** | 6,95 / 21,1 / 35,9 |
| memoria sotto carico, massimo MB | 355 | 272 | 1.566 |

Il nativo arriva a 4.100 ricerche al secondo (da 975): nel container il
limite sono le 4 CPU della VM, sul Mac gli 8 core.

**Il profilo dopo.** Il lock dell'allocatore (prima il 20% della CPU) e il
garbage collector (7%) escono dalle prime righe; il 43% dei campioni è ora
nelle chiamate di sistema della rete, cioè il motore non è più la parte
lenta della richiesta. Delle allocazioni che restano l'86% è la mappa dei
candidati con refuso in `fuzzyCandidates`, dimensionata sulla somma delle
liste dei bigrammi: è il prossimo punto, se servisse.

**Trovato strada facendo, non corretto.** Con una parola corta e un refuso
ammesso (4 lettere o meno con AUTO) Koskidex non usa i bigrammi ma scorre
tutto il vocabolario, che è una mappa Go: l'ordine dei termini trovati cambia
da una chiamata all'altra. L'ordine degli highlights cambia, e se un
documento contiene due termini alla stessa distanza dalla parola cercata,
quale dei due gli viene accreditato (e quindi TF e df del BM25) dipende dal
caso. Precede questo lavoro; nelle 429 query delle impronte non ha prodotto
differenze, ma il test del percorso veloce ha dovuto escludere quelle query
perché lì il vecchio percorso non è uguale a se stesso.
