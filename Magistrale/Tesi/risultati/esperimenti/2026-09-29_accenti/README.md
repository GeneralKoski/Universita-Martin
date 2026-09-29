# L'ultima allocazione grande: la catena che toglie gli accenti

**Domanda.** Dopo `2026-09-28_allocazioni` Koskidex alloca 0,081 MB a ricerca
nel profilo a 8 client, e la prima voce è `transform.Chain` di
golang.org/x/text con il 35% dei byte. È tutta in `removeAccents`, chiamata da
`Tokenize` per ogni testo: a ogni chiamata ricrea la catena NFD, togli i segni
diacritici, NFC, e la catena alloca due buffer intermedi da 4 KB l'uno. Riusando
la catena, e saltandola del tutto sui testi che sono solo ASCII (per i quali è
l'identità), **senza cambiare un solo risultato**, quanto cambiano allocazioni,
tempi e capacità?

Scritto il 29/09/2026, prima di scrivere il codice e di misurare il "prima".

## L'intervento

Uno, in un commit di Koskidex, senza impostazione perché non deve cambiare
nulla. `removeAccents` restituisce la stringa com'è se ogni byte è ASCII (NFD,
togliere i segni e NFC non toccano un testo ASCII); altrimenti prende una catena
da un `sync.Pool`, la usa con `transform.String` (che la azzera prima di
cominciare) e la rimette nel pool. La catena non è sicura fra goroutine, e il
pool ne dà una a testa.

Il guadagno atteso è marginale: è l'ultima voce grande delle allocazioni, non
un collo di bottiglia dei tempi. Il profilo del "dopo" di
`2026-09-28_allocazioni` mette il 55% dei campioni CPU nelle chiamate di rete.

## Come si verifica che i risultati non cambiano

Come in `2026-09-28_allocazioni`, con i suoi strumenti:

- i test di Koskidex, `TestBaselineRankingIsFrozen` compreso, senza toccarli,
  più un test nuovo che confronta `removeAccents` con l'implementazione di
  prima (tenuta nel test) su stringhe ASCII, italiane con accenti, lettere con
  più segni, caratteri composti e scomposti, UTF-8 non valido e stringhe
  casuali, anche da più goroutine insieme sotto `-race`;
- le impronte di `scripts/carico -modo risposte` (identificativi e punteggi
  byte per byte) sulle 429 query di `query-verifica.jsonl` più le 400, a
  10.018 e a 100.000 documenti (`../2026-09-28_prestazioni/identita.sh` con
  `ESPERIMENTO=2026-09-29_accenti`);
- `scripts/evaluate` su SciFact, NFCorpus e le known-item automatiche, nelle
  tre configurazioni di confronto: metriche per query identiche. Qui
  l'indice si ricostruisce, quindi si prova anche il lato dell'indicizzazione.

## Le misure

`../2026-09-28_allocazioni/misura.sh prima|dopo` con
`ESPERIMENTO=2026-09-29_accenti`: il motore del commit corrente di Koskidex,
"prima" al commit di partenza (`51d4988`) e "dopo" all'intervento, sulla
stessa macchina nella stessa sessione. Stesse misure di
`2026-09-28_allocazioni`: una ricerca alla volta nel container e nativo, sotto
carico da 1 a 32 client nel container e nativo, una alla volta a 100.000
documenti nel container, il profilo a 8 client.

**I dati.** Docker è stato azzerato il 28/09 da una pulizia del disco, e con
lui i dati dei motori. Il 29/09 il database dell'app è stato ricostruito e
verificato (l'esportazione ha la stessa impronta di prima, e le ricerche
dall'app di Elasticsearch e di Koskidex sulle known-item automatiche danno gli
stessi ranking archiviati il 25 e il 28/09). Il container e il nativo partono
da una stessa cartella di dati, riempita dall'app con
`KOSKIDEX_PROFILO=consigliata` dal motore del "prima", invece che da due
indicizzazioni separate come in `2026-09-28_carico`: prima e dopo leggono gli
stessi byte, che è quello che conta per il confronto.

## Prima di misurare

I numeri di riferimento sono il "dopo" di `2026-09-28_allocazioni`; le
previsioni si controllano contro il "prima" rimisurato.

1. **Nessun risultato cambia**: impronte uguali per tutte le 429 query a
   10.018 e a 100.000 documenti, metriche di `evaluate` uguali nelle 9
   combinazioni, test che passano.
2. **Allocazioni per ricerca** nel profilo a 8 client: almeno il 25% in meno
   (da circa 0,081 MB).
3. **`transform.Chain` esce dalle allocazioni**: dopo, meno di 1 KB a ricerca
   (prima circa 28 KB, il 35% di 0,081 MB). La soglia è sul valore assoluto
   della voce e non sulla sua quota: la previsione 3 di
   `2026-09-28_allocazioni` è stata smentita proprio perché la quota si misura
   su un totale che scende con lei.
4. **Capacità nativa** (8 core): il massimo di ricerche al secondo cambia fra
   -3% e +15% (da circa 6.400): un guadagno, se c'è, piccolo.
5. **Una alla volta a 10.018 documenti** nel container: il p50 non peggiora di
   più del 5% (da circa 0,92 ms).
