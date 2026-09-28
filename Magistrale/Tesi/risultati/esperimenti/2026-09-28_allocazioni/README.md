# Le allocazioni che restano: i candidati con refuso

**Domanda.** Dopo `2026-09-28_prestazioni` Koskidex alloca 0,44 MB a ricerca
nel profilo a 8 client, e l'86% viene da una riga sola: in `fuzzyCandidates`
la mappa che toglie i doppioni dai termini che condividono un bigramma con la
parola cercata, dimensionata sulla somma delle liste dei bigrammi (migliaia di
termini per i bigrammi comuni). Quasi tutti quei termini vengono poi scartati
subito, perché la loro lunghezza è troppo lontana da quella della parola o non
hanno il prefisso esatto. Togliendo i doppioni solo fra i termini che passano
quei controlli economici, **senza cambiare un solo risultato**, quanto
cambiano allocazioni, tempi e capacità?

Scritto il 28/09/2026, dopo `2026-09-28_prestazioni` e prima di scrivere il
codice e di misurare il "prima".

## L'intervento

Uno, in un commit di Koskidex, senza impostazione perché non deve cambiare
nulla. `fuzzySearchTermsLocked` passa a `fuzzyCandidates` un filtro puro,
lo stesso di prima del calcolo della distanza (non è la parola stessa; è
un'estensione per prefisso, oppure ha il prefisso esatto e una lunghezza entro
la distanza ammessa); `fuzzyCandidates` toglie i doppioni solo fra i termini
che lo passano, con una mappa piccola. Il filtro dipende solo dal termine,
quindi filtrare prima o dopo aver tolto i doppioni dà gli stessi termini
nello stesso ordine, e i termini trovati restano gli stessi, nello stesso
ordine, anche con `stable_term_order` spenta.

Restano fuori, e restano gli sviluppi di `2026-09-28_prestazioni`: la scansione
del vocabolario per le parole corte con un refuso (la mappa si percorre, non
si alloca) e l'indice compatto (cambia il formato su disco).

## Come si verifica che i risultati non cambiano

Come in `2026-09-28_prestazioni`, con i suoi strumenti:

- i test di Koskidex, `TestBaselineRankingIsFrozen` compreso, senza toccarli,
  più un test nuovo che confronta i termini trovati con il percorso di prima,
  su un vocabolario di migliaia di parole casuali cercate intere, troncate e
  con un refuso, con distanza 0, 1 e 2, prefisso esatto di 0, 1 e 2 lettere,
  con e senza estensione per prefisso;
- le impronte di `scripts/carico -modo risposte` (identificativi e punteggi
  byte per byte) sulle 429 query di `query-verifica.jsonl` più le 400, a
  10.018 e a 100.000 documenti (`../2026-09-28_prestazioni/identita.sh` con
  `ESPERIMENTO=2026-09-28_allocazioni`);
- `scripts/evaluate` su SciFact, NFCorpus e le known-item automatiche, nelle
  tre configurazioni di confronto: metriche per query identiche.

## Le misure

`misura.sh prima|dopo`: il motore del commit corrente di Koskidex, "prima" al
commit di partenza (`6f64947`) e "dopo" all'intervento, sulla stessa macchina
nella stessa sessione. Una ricerca alla volta nel container e nativo, sotto
carico da 1 a 32 client nel container e nativo, una alla volta a 100.000
documenti nel container, il profilo a 8 client. Il "prima" si rimisura invece
di prendere il "dopo" di `2026-09-28_prestazioni`: da allora il motore ha
avuto altri commit (tutti a impostazione spenta) e la macchina non è la
stessa ora per ora.

## Prima di misurare

I numeri di riferimento sono il "dopo" di `2026-09-28_prestazioni`; le
previsioni si controllano contro il "prima" rimisurato.

1. **Nessun risultato cambia**: impronte uguali per tutte le 429 query a
   10.018 e a 100.000 documenti, metriche di `evaluate` uguali nelle 9
   combinazioni, test che passano.
2. **Allocazioni per ricerca** nel profilo a 8 client: almeno il 60% in meno
   (da circa 0,44 MB).
3. **`fuzzyCandidates` esce dalle allocazioni**: dopo, meno del 10% dei byte
   allocati (prima circa l'86%).
4. **Capacità nativa** (8 core): il massimo di ricerche al secondo sale di
   almeno il 5% (da circa 4.100).
5. **Capacità nel container** (4 CPU): il massimo sale di almeno il 5% (da
   circa 2.600).
6. **A 100.000 documenti**, una alla volta nel container, dove le liste dei
   bigrammi sono dieci volte più lunghe: p95 e p99 scendono di almeno il 15%
   (da circa 10,4 e 15,5 ms).
7. **Una alla volta a 10.018 documenti** nel container: il p50 non peggiora di
   più del 5%.

## Esito

Misurato il 28/09/2026: "prima" Koskidex `6f64947`, "dopo" `2e6beff`, stessa
macchina, a mezz'ora di distanza, con gli stessi altri container accesi.
Riassunto in `2026-09-28T113740Z_esito.json` (`analizza.py`); le misure in
`prima/` e `dopo/`, impronte e `evaluate` qui.

**Cinque previsioni su sette.** Le due smentite lo sono per una premessa
sbagliata, non per un effetto più piccolo del previsto.

1. **Confermata.** Impronte uguali per tutte le 429 query a 10.018 e a
   100.000 documenti; metriche di `evaluate` uguali nelle 9 combinazioni; i
   test passano, `TestBaselineRankingIsFrozen` senza toccarlo. Il test nuovo
   confronta 42.420 ricerche di termini con il percorso di prima, ordine
   compreso, e fallisce se si rompe il controllo di lunghezza. L'unico test
   esistente toccato è `TestFuzzyCandidatesComePrima`, per passare `nil` al
   parametro nuovo.
2. **Confermata.** Allocazioni per ricerca da 0,435 a 0,081 MB, l'81% in
   meno.
3. **Smentita.** `fuzzyCandidates` scende dall'86% al 30% dei byte allocati,
   non sotto il 10%. La soglia era sbagliata in partenza: era una quota, e il
   totale è sceso con lei. In valore assoluto la funzione passa da 385 a 25 KB
   a ricerca, il 93% in meno; quello che resta è la mappa e la lista dei
   candidati che passano il filtro (righe 207 e 208), cioè la risposta.
4. **Confermata.** Capacità nativa da 4.090 a 6.376 ricerche al secondo, +56%.
5. **Confermata.** Capacità nel container da 2.622 a 3.779 ricerche al
   secondo, +44%.
6. **Smentita.** A 100.000 documenti p95 da 10,3 a 9,9 ms (-4%) e p99 da 14,7
   a 13,6 (-7%), non -15%. La premessa era sbagliata: la copia da 100.000
   ripete gli stessi testi con identificativi diversi, quindi il vocabolario,
   e con lui le liste dei bigrammi, non cresce. Cresce di dieci volte ciò che
   dipende dai documenti, le liste di posting, e la coda a 100.000 viene da
   lì.
7. **Confermata.** Una alla volta nel container il p50 scende da 1,14 a
   0,92 ms (-19%).

| | prima | dopo |
|---|---|---|
| allocazioni per ricerca | 0,435 MB | **0,081 MB** |
| una alla volta nel container, p50 / p95 / p99 ms | 1,14 / 2,77 / 4,80 | 0,92 / 2,32 / 4,09 |
| nativo, p50 / p95 / p99 ms | 0,79 / 2,32 / 4,38 | 0,60 / 1,96 / 2,58 |
| ricerche al secondo, massimo nel container | 2.622 | **3.779** |
| ricerche al secondo, massimo nativo | 4.090 | **6.376** |
| p99 a 32 client nel container, ms | 43,8 | 32,1 |
| memoria sotto carico nel container, massimo MB | 281 | 195 |
| 100.000 documenti, p95 / p99 ms | 10,3 / 14,7 | 9,9 / 13,6 |

Il "prima" rimisurato coincide con il "dopo" di `2026-09-28_prestazioni`
(2.622 contro 2.614 ricerche al secondo nel container, 0,435 contro 0,44 MB):
i commit intermedi, a impostazioni spente, non hanno cambiato le prestazioni.

**Il profilo dopo.** Il 55% dei campioni CPU è nelle chiamate di sistema della
rete (era il 43%); il motore pesa ancora meno. Delle allocazioni, la prima voce
è ora `transform.Chain` di golang.org/x/text (35%), la catena che toglie gli
accenti, ricreata a ogni testo tokenizzato; poi `fuzzyCandidates` (30%) e
`docsForTermsLocked` (10%). Fra i tempi resta visibile la scansione del
vocabolario per le parole corte con un refuso (`maps.Iter.Next`, 7%).
