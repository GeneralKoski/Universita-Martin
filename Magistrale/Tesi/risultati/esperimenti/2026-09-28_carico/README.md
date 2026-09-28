# Elasticsearch e Koskidex sotto carico: tempi, capacità, memoria

**Domanda.** A parità di atti e di ricerche, quanto costano i due motori sulla
macchina? Tempo di risposta di una ricerca, ricerche al secondo che reggono in
parallelo, memoria a riposo e sotto carico, e come cambia tutto quando l'archivio
cresce. E dove Koskidex spende il suo tempo, cioè cosa conviene migliorare.
È la parte "latenza, memoria, dimensione dell'indice" del capitolo 8.

Scritto il 28/09/2026, prima delle misure.

**Dichiarato.** Oggi, prima di scrivere queste previsioni, ho fatto una misura
informale, non archiviata: il container di Elasticsearch occupa 1,49 GB (heap
fissato a 1 GB), Koskidex nativo 12 MB a vuoto, 138 MB con i 10.018 atti e
176 MB dopo 72 ricerche dall'app; le ricerche di Koskidex dall'app hanno
impiegato fra 5 e 23 ms ciascuna, PHP compreso. I tempi di indicizzazione sono
già nell'archivio (`confronto/`): 1,1-1,7 s per Elasticsearch, 1,8 s per
Koskidex.

## Metodo

**Macchina.** Apple M2, 8 core, 16 GB. Docker Desktop con una VM Linux da 4 CPU
e 8 GB.

**I motori, come li usa Documentale.**

- **Elasticsearch 9.1** nel container `doc-tesi-es` (heap 1 GB), indice
  `search-documents-local` riempito dall'app (`app:export-to-elastic-search`).
- **Koskidex nel container**: lo stesso binario compilato per Linux, in un
  container `alpine` nella stessa VM di Elasticsearch, così le due strade di
  rete e le CPU a disposizione sono le stesse. Indice riempito dall'app con
  `KOSKIDEX_PROFILO=consigliata`, senza vettori (Elasticsearch in Documentale è
  solo lessicale).
- **Koskidex nativo**, sul Mac, come riferimento: quanto costa Docker.

**Le richieste** sono quelle che manda l'app, copiate dal codice:

- Elasticsearch: `multi_match` di `ElasticsearchService::cerca` (best_fields,
  fuzziness AUTO, prefix_length 1, operator and, tie_breaker 0,3, i sei campi
  con i loro pesi), `size` 10.000. Così come la fa l'app, Elasticsearch
  restituisce anche il `_source` di ogni risultato, che l'app poi scarta.
  Per separare il motore dal peso della risposta si misura anche la stessa
  richiesta con `_source: false`.
- Koskidex: `GET /indexes/<indice>/search` con `q`, `limit` 10.000,
  `ids_only`, `fuzziness` AUTO, come `KoskidexClient::search`.

**Le query**: 400 in tre famiglie, lette dai loro file e registrate con
l'impronta: le 300 known-item automatiche, le 24 del confronto, le known-item
umane raccolte finora (76 al 28/09). Il testo delle ultime resta fuori da git.

**La cache di Koskidex.** Il server tiene in una cache le ultime 1.024 risposte,
e non c'è un'impostazione per spegnerla. Ripetere le stesse query misurerebbe
la cache, non il motore. Per misurare il motore ogni richiesta porta un numero
diverso di spazi in coda alla query: il tokenizer li ignora, la chiave della
cache no. Lo strumento verifica, prima di misurare, che con gli spazi i
risultati siano identici. Si misura anche con la cache, cioè richieste
identiche ripetute. Gli stessi spazi vanno anche a Elasticsearch, che per
richieste con `size` maggiore di zero non usa la sua cache delle richieste.

**Le misure**, con `scripts/carico` di Koskidex:

1. **Una ricerca alla volta.** Ogni query cinque volte, in ordine mescolato con
   un seme fisso: tempo della prima passata (a freddo, motore appena
   avviato) e delle successive; p50, p95, p99 per famiglia e per dimensione
   della risposta (sotto 100 risultati, da 100 a 999, da 1.000 in su), byte
   della risposta.
2. **Sotto carico.** 1, 2, 4, 8, 16 e 32 client che mandano ricerche senza
   pause, 20 secondi per livello dopo 5 di riscaldamento, query estratte a
   caso con un seme fisso: ricerche al secondo, p50, p95, p99, errori; CPU e
   memoria dei container (`docker stats`) o del processo (`ps`) campionati
   durante il livello.
3. **Archivio più grande.** Gli stessi atti copiati fino a 50.000 e 100.000
   documenti (id diversi, testo uguale: dati inventati, che per tempi e
   memoria vanno bene e per la pertinenza no), indicizzati nei due motori con
   le stesse impostazioni: memoria, dimensione dell'indice su disco, tempo di
   indicizzazione e la misura 1 con cache spenta.
4. **Dove spende Koskidex.** Profilo CPU e delle allocazioni di Koskidex (pprof)
   durante la misura 2 a 8 client: le funzioni che pesano di più, cioè i punti
   da migliorare.

## Prima di misurare

1. **Una alla volta, cache spenta, richieste come l'app: il p50 di Koskidex
   nel container è minore di quello di Elasticsearch** su tutte le 400 query.
2. **Il `_source` pesa sulle ricerche larghe**: sulle query con almeno 1.000
   risultati, il p50 di Elasticsearch come lo usa l'app è almeno il doppio di
   quello con `_source: false`.
3. **I due motori, senza il peso della risposta, sono vicini**: il p50 di
   Elasticsearch con `_source: false` e quello di Koskidex a cache spenta
   stanno entro un fattore 2.
4. **Con la cache, Koskidex risponde in meno di 1 ms** al p50 a richieste
   ripetute (dal container).
5. **Capacità, stesse 4 CPU, cache spenta**: il massimo di ricerche al secondo
   di Koskidex nel container è almeno 1,5 volte quello di Elasticsearch come
   lo usa l'app.
6. **Memoria sotto carico**: Elasticsearch resta fra 1,3 e 1,8 GB; Koskidex nel
   container non supera i 400 MB.
7. **Coda dei tempi**: a 16 client il p99 di Koskidex nel container resta sotto
   i 100 ms.
8. **Docker costa poco a Koskidex**: il p50 una alla volta del nativo è al più
   il 30% più basso di quello nel container.
9. **Archivio dieci volte più grande (100.000 documenti)**: la memoria di
   Koskidex cresce almeno di 5 volte, quella del container di Elasticsearch
   meno di 1,5 volte; il p50 di Koskidex cresce almeno di 3 volte, quello di
   Elasticsearch meno di 3 volte. Koskidex tiene tutto in memoria ed esamina
   ogni candidato; Elasticsearch ha un heap fisso e salta i documenti con
   strutture su disco.
10. **Il profilo** mette fra le prime cinque funzioni per CPU la
    tokenizzazione o l'espansione dei termini con refusi (fuzziness AUTO) e la
    serializzazione JSON della risposta.
