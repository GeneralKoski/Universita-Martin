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

## Esito

Da `2026-09-28T093314Z_esito.json` (marcato con modifiche non committate per i
file di risultato non tracciati della cartella; rifatto il 29/09 con il
controllo corretto, stessi numeri e stessi esiti letti:
`2026-09-29T074830Z_esito.json`) (tutte le esecuzioni, l'ultima per
etichetta) e dai profili `profilo/2026-09-28T093154Z_*`. Koskidex `ffa38ab`
nei motori, strumenti da `c70bbcd`; Elasticsearch 9.1.0. Nessun errore in
nessuna esecuzione; la verifica dice che gli spazi in coda non cambiano il
risultato di nessuna delle 400 query, su nessuno dei due motori.

**Una ricerca alla volta**, 400 query per 5 passate, ms:

| | p50 | p95 | p99 |
|---|---|---|---|
| Elasticsearch, come l'app | 6,32 | 17,66 | 24,26 |
| Elasticsearch, senza `_source` | 6,77 | 19,60 | 26,09 |
| Koskidex nel container, cache aggirata | **2,12** | 12,36 | 18,31 |
| Koskidex nel container, con la cache (passate 2-5) | 0,29 | 0,38 | 0,72 |
| Koskidex nativo, cache aggirata | 1,78 | 12,43 | 17,43 |

La prima passata, a motore appena riavviato, costa poco in più
(Elasticsearch 7,07 ms di p50, Koskidex 2,17). Il p50 di Koskidex è un terzo di
quello di Elasticsearch, ma la coda no: 68 query su 400 impiegano più di 8 ms,
e sono le query lunghe, piene di parole comuni ("delibera di giunta sul
bilancio di previsione 2026": 20,6 ms contro 16,6).

**Sotto carico**, stesse 4 CPU della VM, cache aggirata:

| client | Elasticsearch come l'app | | Koskidex nel container | |
|---|---|---|---|---|
| | ricerche/s | p99 ms | ricerche/s | p99 ms |
| 1 | 134,6 | 22,8 | 233,3 | 19,2 |
| 4 | 471,7 | 26,6 | 588,9 | 29,1 |
| 8 | **571,1** | 46,5 | **653,0** | 48,5 |
| 16 | 550,4 | 69,6 | 622,6 | 105,0 |
| 32 | 559,4 | 103,1 | 647,2 | 214,6 |

Tutti e due saturano le 4 CPU (Elasticsearch al 385-390%, Koskidex al
377-382%). Con un client solo Koskidex usa già il 116% di CPU: più di un core
per una ricerca alla volta. Koskidex nativo, sugli 8 core del Mac divisi con il
client, arriva a 975 ricerche al secondo.

**Memoria**, MB: a riposo dopo un riavvio, Elasticsearch 1.431 e Koskidex 155
con i 10.018 atti; sotto carico al massimo 1.566 e 355.

**Archivio più grande** (atti copiati, a riposo dopo un riavvio; ricerche una
alla volta):

| documenti | memoria ES | memoria Koskidex | p50 / p99 ES | p50 / p99 Koskidex | disco ES | disco Koskidex | indicizzazione ES / Koskidex |
|---|---|---|---|---|---|---|---|
| 10.018 | 1.431 MB | 155 MB | 6,3 / 24 ms | 2,1 / 18 ms | 3,9 MB* | 6,6 MB* | 1,1-1,7 s / 1,9-2,1 s (dall'app) |
| 50.000 | 1.439 MB | 651 MB | 6,3 / 28 ms | 3,8 / 101 ms | 17,9 MB | 32,8 MB | 2,8 s / 6,2 s |
| 100.000 | 1.433 MB | 1.213 MB | 7,0 / 36 ms | 5,4 / 201 ms | 35,5 MB | 65,6 MB | 5,3 s / 12,9 s |

\* *Corretto il 29/09/2026.* I 3,5 e 6,3 MB scritti qui il 28/09 non avevano
un file (lo ha trovato il terzo controllo della tesi). Misurati di nuovo con
`disco-10018.sh`, con il metodo di `copia.py`, in
`2026-09-29T100953Z_disco-10018.json`: 3.868.374 byte per Elasticsearch
(l'indice dell'app, ricostruito il 29/09 dopo l'azzeramento di Docker) e
6.556.875 per Koskidex (`cd86102`, profilo consigliato; le correzioni dopo
`ffa38ab` non toccano il formato su disco). Koskidex torna con la riga a
50.000, cinque volte tanto; Elasticsearch no, e non ho verificato perché:
l'indice dell'app non è una copia fatta in blocchi da 1.000 come quelli più
grandi, e può essere compattato in segmenti diversi.

Previsione per previsione:

1. **Confermata.** p50 2,12 ms contro 6,32.
2. **Smentita**, e quasi senza materia: con l'operatore `and` solo una query
   su 400 dà più di 1.000 risultati (5 richieste), e lì il p50 è 27,5 ms contro
   22,4, non il doppio. Il `_source` non pesa perché le risposte sono piccole
   (mediana 160 byte).
3. **Smentita.** Senza `_source` Elasticsearch resta a 6,77 ms: il rapporto con
   Koskidex è 3,2, non entro 2. La differenza è nel motore, non nella risposta.
4. **Confermata.** 0,29 ms con la cache.
5. **Smentita.** 653 contro 571 ricerche al secondo, 1,14 volte e non 1,5:
   il vantaggio del p50 si perde sotto carico (vedi il profilo).
6. **Confermata.** Elasticsearch al massimo 1.566 MB, Koskidex 355.
7. **Smentita, di poco.** p99 105 ms a 16 client; a 32 client 215, contro i
   103 di Elasticsearch: sotto carico la coda di Koskidex cresce più in fretta.
8. **Confermata.** Il nativo è il 16% sotto il container (1,78 contro 2,12 ms).
9. **A metà.** La memoria va come previsto: Koskidex ×7,85, Elasticsearch
   ×1,00. Il p50 di Koskidex cresce di ×2,57 invece di almeno ×3; quello di
   Elasticsearch di ×1,10. Ma il p50 nasconde il fatto più importante: la coda
   di Koskidex cresce di dieci volte (p95 da 12 a 133 ms, p99 da 18 a 201),
   quella di Elasticsearch di una volta e mezza. *Aggiunto il 29/09/2026:*
   l'esito di `analizza.py` scrive `smentita`, perché dà un verdetto solo a
   tutta la previsione; la memoria ha tenuto e il p50 no, quindi a metà.
10. **A metà.** L'espansione dei termini con refusi c'è
    (`fuzzySearchTermsLocked`, 16% della CPU cumulata), la serializzazione
    JSON no: non compare fra le prime 40 funzioni. Il profilo dice un'altra
    cosa, sotto.

**Il profilo.** In 35.913 ricerche Koskidex ha allocato 92 GB, 2,57 MB a
ricerca (corretto il 29/09/2026, dal terzo controllo della tesi, da `2026-09-28_prestazioni`, `allocazioni.prima`; qui
c'era «circa 40.000» e «circa 2 MB»): il 43% in `findDocsForToken`, il 25% in `fuzzyCandidates`, il
15% in `DamerauLevenshtein`, l'11% in `SearchScored`. Quella memoria si paga in
CPU: il 20% dei campioni è nel lock dell'allocatore di Go
(`mheap.allocSpan`, `runtime.lock2`) e un altro 7% nel garbage collector. È per
questo che una ricerca alla volta occupa più di un core, che sotto carico il
vantaggio si riduce da 3 volte a 1,14 e che la coda cresce.

**Dove può migliorare Koskidex**, in ordine di peso, con la misura che lo
mostra. Nessuno di questi cambia i risultati:

1. **Non costruire la mappa di tutti i documenti di ogni parola.** Con il
   recupero congiuntivo `findDocsForToken` crea, per ogni termine della query,
   una voce per ogni documento che lo contiene, anche per "di" o "per", e solo
   dopo interseca. Partire dal termine più raro e cercare gli altri solo fra i
   candidati sopravvissuti, come fa Elasticsearch, toglie la parte più grande
   del 43% delle allocazioni e la crescita della coda con l'archivio.
2. **`DamerauLevenshtein` senza matrice nuova a ogni chiamata**: due righe
   riusate, fermandosi appena la distanza supera il massimo ammesso. Il 15%
   delle allocazioni, con risultati identici.
3. **La raccolta dei candidati con refuso** (`fuzzyCandidates`, 25% delle
   allocazioni) può riusare le strutture fra un termine e l'altro. Per le
   parole di 3-4 lettere con un refuso ammesso Koskidex scorre l'intero
   vocabolario (`fuzzy.go`, il ramo senza bigrammi); con `prefix_length` 1,
   come nel profilo consigliato, basterebbe scorrere i termini con la stessa
   iniziale.
4. **Una rappresentazione più compatta dell'indice**: circa 12 KB di memoria
   per documento, con id dei documenti e nomi dei campi come stringhe in ogni
   posting. Con id e campi interi la memoria a 100.000 documenti, oggi 1,2 GB
   e quasi quella di Elasticsearch, scenderebbe di molto. Anche l'indice su
   disco (il doppio di Elasticsearch) e l'indicizzazione in blocco (2,4 volte
   più lenta) ne beneficerebbero.

**Cosa ne segue per Documentale.** Alla dimensione dell'albo (10.018 atti)
Koskidex è più leggero, circa un decimo della memoria, e una ricerca costa un
terzo; sotto carico regge un po' più di Elasticsearch sulle stesse CPU. Con
questa struttura dati il vantaggio si esaurisce verso i 100.000 documenti:
lì la memoria è quasi quella di Elasticsearch e il p99 è più di cinque volte
il suo. I punti 1 e 4 sono la condizione per usarlo su archivi più grandi.

**Limiti.** Il client gira sullo stesso Mac, fuori dalla VM; le connessioni
restano aperte fra una richiesta e l'altra, mentre l'app, in PHP, ne apre in
genere una nuova per ogni ricerca;
Elasticsearch ha l'heap fissato a 1 GB, e con meno memoria si comporterebbe
diversamente; gli atti copiati hanno testi ripetuti, che per tempi e memoria
vanno bene ma allungano le liste di posting delle parole comuni come
succederebbe con un archivio vero dello stesso vocabolario.
