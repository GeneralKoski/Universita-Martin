# Il carico su un'altra macchina

**Domanda.** Sul Mac Koskidex nel container risponde in 0,89 ms di p50 contro
i 6,32 di Elasticsearch come lo usa l'app, e regge circa sette volte le
ricerche al secondo (4.054 contro 571) sulle stesse 4 CPU. Quel rapporto è una
proprietà dei due motori o del Mac? Rifaccio le stesse misure sul fisso di
Martin, con i due motori accesi nella stessa sessione.

Scritto il 29/09/2026 sul fisso, prima di preparare i motori e prima di ogni
misura. Rimanda a `2026-09-28_carico` per il metodo (richieste come l'app,
400 query in tre famiglie, cache di Koskidex aggirata con gli spazi in coda,
misure una alla volta e sotto carico) e prende i numeri del Mac da lì per
Elasticsearch e da `2026-09-29_accenti` (il "dopo", Koskidex `df6f62b`) per
Koskidex. Il motore di Koskidex qui è `0e914f5`: da `df6f62b` sono cambiati
solo il diario e un `SOURCE.md`, nessun file del motore.

## La macchina

In `macchina.md`. Windows 11 nativo; Docker Desktop con il motore Linux in
WSL2. Il client (`scripts/carico`) e Koskidex nativo girano su Windows, fuori
da WSL2, come sul Mac girano fuori dalla VM.

**Le CPU dei container.** Sul Mac la VM di Docker ha 4 CPU, e ogni motore sotto
carico le ha tutte per sé (le misure non si sovrappongono). Qui la VM di WSL2
ne ha 12 (i thread del Ryzen): per avere le stesse 4 CPU ogni container parte
con `--cpus 4`. Non è identico: sul Mac sono 4 core fisici del M2, qui un tetto
di 4 CPU di tempo su 6 core con due thread ciascuno.

## Il metodo

Quello di `2026-09-28_carico/esegui.sh`, nella versione `esegui.sh` di questa
cartella: verifica, riposo, una alla volta, sotto carico (1-32 client, 20 s per
livello dopo 5 di riscaldamento), stesse query e stesso seme. Restano fuori le
copie da 50.000 e 100.000 documenti e il profilo: la domanda è il rapporto fra
i motori all'albo vero.

- **MySQL 8.4.10** in Docker con il dump esatto del database `albo` (id
  originali), dal bundle privato del Mac; controllati 10.018 documenti e
  10.018 versioni, id da 1 a 10.045.
- **Elasticsearch 9.1.0**, `doc-tesi-es` sulla 9201, heap 1 GB, riempito
  dall'app (`app:export-to-elastic-search`) con il branch
  `martin/tesi-magistrale` di Documentale.
- **Koskidex** nel container `kosk-carico` (alpine, binario per Linux) sulla
  7713 e nativo (Windows) sulla 7714, riempiti dall'app con
  `KOSKIDEX_PROFILO=consigliata`.
- **La memoria del nativo** non si campiona: `scripts/carico` la legge con
  `ps -o rss`, che su Windows non c'è. Per il nativo contano solo tempi e
  capacità.

## Prima di misurare

1. **Tempi una alla volta simili al Mac**: il p50 di Koskidex nel container fra
   0,6 e 1,3 ms (Mac 0,89), quello di Elasticsearch come l'app fra 4,4 e 8,2 ms
   (Mac 6,32, cioè ±30%). Dipendono soprattutto dal singolo core; la rete di
   Docker su Windows passa da WSL2 e può aggiungere qualcosa.
2. **Capacità del nativo nella zona del Mac**: il massimo di ricerche al secondo
   fra 4.000 e 8.000 (Mac 6.526 su 8 core; qui 6 core e 12 thread, che si
   dividono con il client).
3. **Il rapporto di capacità fra i motori regge**: il massimo di Koskidex nel
   container diviso quello di Elasticsearch come l'app sta entro il 30% di
   quello del Mac (7,10), cioè fra 4,97 e 9,23.
4. **Il rapporto dei p50 regge**: p50 di Elasticsearch come l'app diviso quello
   di Koskidex nel container entro il 30% del Mac (7,09), cioè fra 4,96 e
   9,21.

## Esito

Misurato il 29/09/2026 fra le 21:05 e le 21:18 (ora italiana) sul fisso,
Windows 11 nativo con Docker in WSL2, Koskidex `0e914f5` nei motori e nello
strumento, Elasticsearch 9.1.0, ogni container dei motori con `--cpus 4`.
Riassunto in `2026-09-29T191821Z_esito.json` (`analizza.py`), che riporta
anche i file del Mac usati per il confronto. Nessun errore in nessuna
esecuzione; la verifica dice che gli spazi in coda non cambiano il risultato
di nessuna query, su nessuno dei due motori.

**Da dichiarare.**

- **Le query sono 428, non 400.** Il README dice 400, come sul Mac, dove le
  known-item umane erano le 76 raccolte fino al 28/09; qui sono le 104 della
  raccolta chiusa, dal bundle. Non l'ho visto prima di misurare. Le famiglie
  e il seme sono gli stessi; le 28 query in più sono known-item umane dei
  lotti chiusi dopo il 28/09.
- **Durante la misura** erano accesi solo MySQL e i due motori. Prima della
  misura Docker aveva avviato da solo tre container di un altro progetto, poi
  rimossi.
- **La memoria del nativo** non c'è, come previsto dal metodo.

**Una ricerca alla volta**, 428 query per 5 passate, ms:

| | fisso, p50 / p95 / p99 | Mac, p50 / p95 / p99 |
|---|---|---|
| Elasticsearch, come l'app | 8,93 / 24,09 / 32,47 | 6,32 / 17,66 / 24,26 |
| Elasticsearch, senza `_source` | 8,88 / 23,20 / 31,59 | 6,77 / 19,60 / 26,09 |
| Koskidex nel container, cache aggirata | **1,46** / 3,62 / 4,83 | 0,89 / 2,28 / 3,01 |
| Koskidex nel container, con la cache | 0,52 / 1,81 / 2,92 | |
| Koskidex nativo, cache aggirata | 0,89 / 2,61 / 4,12 | 0,59 / 1,92 / 2,39 |

**Sotto carico**, massimo di ricerche al secondo (il livello di client dove
cade):

| | fisso | Mac |
|---|---|---|
| Elasticsearch, come l'app | 376 (4 client) | 571 (8) |
| Elasticsearch, senza `_source` | 382 (4) | 583 |
| Koskidex nel container | **2.636** (32) | 4.054 (16) |
| Koskidex nativo | 6.258 (16) | 6.526 (16) |

Elasticsearch satura le sue 4 CPU già a 4 client (CPU del container al
349%, poi 360-367%) e oltre scende a circa 345 ricerche al secondo; Koskidex
nel container arriva al 365% a 8 client e resta a 2.616-2.636. Memoria nel
container sotto carico: Elasticsearch al massimo 1.584 MB, Koskidex 199; a
riposo 1.607 e 144.

**Tre previsioni su quattro.**

1. **Smentita.** Tutti e due i motori sono più lenti che sul Mac, e fuori
   dalle due soglie: Koskidex nel container 1,46 ms di p50 (soglia 0,6-1,3,
   Mac 0,89), Elasticsearch 8,93 ms (soglia 4,4-8,2, Mac 6,32). Anche il
   nativo, fuori da Docker, è a 0,89 contro 0,59: non è solo la rete di WSL2.
   Non ho misurato quanto pesino il core, Windows e la rete ciascuno.
2. **Confermata.** Il nativo arriva a 6.258 ricerche al secondo, contro 6.526
   sul Mac.
3. **Confermata, con margine.** Rapporto di capacità 2.636 / 376 = 7,01,
   contro 7,10 sul Mac (soglia 4,97-9,23).
4. **Confermata.** Rapporto dei p50 8,93 / 1,46 = 6,13, contro 7,08 sul Mac
   (soglia 4,96-9,21).

**Cosa dice.** I tempi assoluti dipendono dalla macchina: sul fisso, con
Docker in WSL2 e un tetto di 4 CPU per container, tutti e due i motori sono
più lenti che sul Mac. Il rapporto fra i due invece regge: Koskidex risponde
in circa un sesto del tempo di Elasticsearch e ne regge circa sette volte le
ricerche al secondo sulle stesse 4 CPU, come sul Mac. Il vantaggio è dei
motori, non del Mac.
