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
