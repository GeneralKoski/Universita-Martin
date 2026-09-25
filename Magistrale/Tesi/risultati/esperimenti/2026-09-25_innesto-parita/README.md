# L'innesto dal vivo: stesse query, dall'app, sui due motori

**Domanda.** Con Koskidex innestato in Documentale dietro `SearchBackend`
(Documentale `2a03310`), l'app trova gli stessi documenti con Koskidex e con
Elasticsearch? E quanto costano indicizzazione e ricerca, passando dall'app?

**Metodo.** Tutto dal codice dell'app, nessuna scorciatoia:

- indicizzazione dei 10.018 atti degli albi col comando dell'app
  (`app:export-to-elastic-search`) da indice vuoto, su ciascun motore:
  `strumenti/indicizza-elasticsearch.sh` e `strumenti/indicizza-koskidex.sh`;
- le 24 query di `query/confronto-24.txt` con `app:eval-run-queries`, tre
  esecuzioni per motore, cambiando solo `SEARCH_BACKEND`;
- Koskidex compilato dal commit indicato (versione letta da `/health`), su una
  cartella dati nuova; Elasticsearch 9.1.0 locale.

Script: `confronta.py`, che rifiuta rapporti da codice non committato.

## Risultato

| | Koskidex | Elasticsearch |
|---|---|---|
| insiemi identici sulle 24 query | **24 / 24** | |
| top 10 identici | 7 / 24 (solo le query con 0-2 risultati) | |
| ricerca, ms mediana per query | **2,7** | 22,0 |
| indicizzazione di 10.018 atti | 1.870 ms | 1.714 ms |

**L'innesto è fedele.** Passando dall'app, Koskidex con le impostazioni di
compatibilità trova esattamente i documenti di Elasticsearch su tutte le query.
Quello che cambia è l'ordine, ed è l'oggetto della tesi: il punteggio di
Koskidex (euristico) non è quello di Elasticsearch (BM25).

**La prima misura ha trovato un difetto.** Con Koskidex `c522467` l'indicizzazione
costava 31,8 secondi (`confronto/2026-09-25T072111Z_albo-metadata-indicizzazione-koskidex.json`):
2,6 ms a documento, costanti, perché ogni documento sincronizzava il WAL, e su
macOS una sincronizzazione è un `F_FULLFSYNC`. Corretto in Koskidex `f583d03`
(una sincronizzazione per richiesta): da 31,8 a 1,9 secondi. Il primo esito,
`2026-09-25T072143Z_esito.json`, è stato preso con la versione lenta: stessi
insiemi, tempi di ricerca simili (2,6 ms di mediana).

Leggere i tempi con le avvertenze del README dell'archivio: Elasticsearch gira
nella macchina virtuale Docker, Koskidex nativo; entrambi i tempi di ricerca
includono il viaggio HTTP da PHP, e l'indicizzazione include l'avvio di PHP e
la lettura degli atti da MySQL.

File d'esito: `2026-09-25T072346Z_esito.json` (Koskidex `f583d03`). Rapporti:
`confronto/2026-09-25T072328Z`, `072328Z-2`, `072329Z` (Koskidex) e `072340Z`,
`072341Z`, `072342Z` (Elasticsearch); indicizzazione
`confronto/2026-09-25T072327Z` (Koskidex) e `072339Z` (Elasticsearch).
