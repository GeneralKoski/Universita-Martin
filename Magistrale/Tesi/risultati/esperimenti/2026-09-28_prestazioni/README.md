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
