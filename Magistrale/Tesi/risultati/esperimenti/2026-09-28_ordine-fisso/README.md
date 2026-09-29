# L'ordine dei termini trovati: da una mappa a un ordine fisso

**Domanda.** Koskidex, in tre punti, visita i termini dell'indice in un ordine
che non decide lui:

1. per una parola corta con un refuso ammesso (quando i bigrammi non bastano a
   garantire di trovare tutti i termini abbastanza vicini) scorre il
   vocabolario, che è una mappa di Go, e una mappa si percorre in un ordine
   diverso a ogni chiamata;
2. con `substring_match` scorre il vocabolario allo stesso modo;
3. negli altri casi i termini arrivano dalle liste dei bigrammi, nell'ordine in
   cui sono entrati nell'indice; ma l'istantanea su disco scrive i documenti in
   ordine di mappa, e dopo un riavvio rientrano in un altro ordine.

L'ordine decide due cose: l'ordine degli highlights e, se un documento contiene
due termini alla stessa distanza dalla parola cercata, quale dei due gli viene
accreditato, cioè TF e df del suo punteggio BM25. Il punteggio euristico non
guarda il termine accreditato, BM25 sì. Quanto di questo arriva ai numeri della
tesi, e un ordine fisso lo toglie?

Scritto il 28/09/2026, prima del codice. Il difetto è stato trovato il 28/09 dal
test di `2026-09-28_prestazioni` (Koskidex `510b9d2`), che ha dovuto escludere
quelle query.

## La correzione

`Settings.StableTermOrder` (`stable_term_order`), spenta per default: accesa,
i termini che una parola trova si visitano in ordine lessicografico, qualunque
sia la strada da cui arrivano, e lo stesso per i termini della ricerca per
sottostringa. L'ordine lessicografico non ha niente di migliore di un altro:
ha di essere sempre lo stesso, come l'ultimo criterio di parità per id.
`scripts/evaluate -ordine-fisso`.

## Metodo

- **Ripetizioni.** `scripts/evaluate` cinque volte per configurazione, spento e
  acceso, su SciFact, NFCorpus e le known-item automatiche dell'albo, nelle tre
  configurazioni di confronto: baseline (legacy, `all`), BM25 `all` e BM25 `any`
  con le espansioni `blended`. Si contano le query con una metrica per query
  (nDCG@10, Recall@100, MRR@10, recuperati, candidati) diversa fra le cinque
  ripetizioni, e si confrontano le medie.
- **Documentale.** Le impronte delle 429 query di `2026-09-28_prestazioni`
  sull'indice dell'app, con l'impostazione accesa, contro quelle "dopo" di
  quell'esperimento.
- **Costo.** Il tempo per query di `scripts/evaluate`, spento contro acceso.

## Prima di misurare

1. **Il punteggio euristico non ne risente**: spento, le cinque ripetizioni del
   baseline danno le stesse metriche per query su tutte e tre le collezioni.
2. **Con BM25 il difetto arriva ai numeri, ma poco**: spento, nelle
   configurazioni BM25 al più 5 query per collezione e configurazione hanno una
   metrica diversa fra le ripetizioni, e le medie coincidono alla quarta
   cifra decimale. Nessun numero della tesi cambia.
3. **Acceso, niente varia**: le cinque ripetizioni danno le stesse metriche per
   query in tutte le nove combinazioni.
4. **Acceso contro spento**: le medie di nDCG@10 differiscono di meno di 0,001
   ovunque; nel baseline coincidono.
5. **Documentale non cambia**: con il punteggio euristico del suo profilo, le
   429 impronte con l'impostazione accesa coincidono con quelle "dopo" di
   `2026-09-28_prestazioni`.
6. **Costa niente**: la mediana del tempo per query, acceso, sta entro il 5% di
   quella spento, in ogni combinazione.
7. **I test**: passano tutti, `TestBaselineRankingIsFrozen` senza toccarlo; con
   l'impostazione accesa il test del percorso veloce confronta tutte le query,
   senza escludere quelle con la scansione del vocabolario, e un indice
   riempito in un altro ordine dà gli stessi risultati.

## Esito

Da `2026-09-28T104229Z_esito.json` (`analizza.py`), Koskidex `c514c77`: 90
valutazioni in `evaluate/` e le impronte `2026-09-28T104225Z_risposte-acceso-10018.json`.

**Cinque previsioni su sei confermate, più la settima**; la smentita è la più
istruttiva.

1. **Confermata.** Spento, il baseline dà le stesse metriche per query in
   tutte e cinque le ripetizioni, su tutte e tre le collezioni.
2. **Confermata, e più di così.** Spento, anche con BM25 nessuna query varia
   fra le ripetizioni, in nessuna combinazione. Il motivo si vede solo
   leggendo `scripts/evaluate`: cerca sempre con fuzziness `0`, quindi la
   scansione del vocabolario per le parole corte con refuso non parte mai, e
   `substring_match` è spento. L'ordine che resta è quello di ingresso dei
   termini nell'indice, che con i documenti caricati sempre nello stesso
   ordine è sempre lo stesso. Nessun numero di `evaluate` nella tesi dipende
   dall'ordine della mappa.
3. **Confermata.** Acceso, nessuna query varia fra le ripetizioni.
4. **Smentita.** Acceso contro spento, otto combinazioni su nove coincidono,
   baseline compreso, ma SciFact con BM25 `any` passa da 0,6694 a 0,6670 di
   nDCG@10 (−0,0024, soglia 0,001). Cambiano 2 query su 300 (1140 e 452): un
   documento pertinente scende dal primo al terzo posto nella 1140 e dal
   primo al secondo nella 452; Recall@100
   identico, MRR@10 da 0,6410 a 0,6371. Non è rumore, perché spento e acceso
   sono stabili ciascuno per conto suo: è l'ordine di ingresso nell'indice,
   deterministico ma arbitrario quanto quello lessicografico, che a parità di
   distanza decide quale espansione per prefisso viene accreditata a un
   documento, e quindi il suo TF. Lo 0,6694 della tesi è uno dei due valori
   che dà una regola di parità arbitraria; la differenza fra i due, 0,0024, è
   quanto quella regola pesa su SciFact.
5. **Confermata.** Su Documentale, con il punteggio euristico del suo profilo,
   le 429 impronte con l'impostazione accesa coincidono con quelle "dopo" di
   `2026-09-28_prestazioni`.
6. **Confermata.** Le mediane del tempo per query stanno fra −1,7% e +3,2%.
7. **Confermata** (`go test ./...` a `c514c77`): tutti i test passano,
   `TestBaselineRankingIsFrozen` senza toccarlo; con l'impostazione accesa il
   test del percorso veloce confronta tutte le 4.200 query, e il test nuovo
   dà gli stessi risultati su un indice riempito in un altro ordine. Senza
   l'impostazione lo stesso test fallisce alle prime chiamate, con due
   documenti che si scambiano di posto.

**Cosa ne segue.** Dove il difetto cambia i punteggi, cioè BM25 con le ricerche
con refuso delle parole corte (come quelle dell'app, fuzziness AUTO) o con
`substring_match`, e dopo ogni riavvio, l'impostazione lo toglie senza costo.
Documentale oggi non ne risente, perché usa il punteggio euristico e non chiede
gli highlights; se passasse a BM25 andrebbe accesa. Una regola di parità più
sensata di quella lessicografica, per esempio sommare le espansioni come fa la
riscrittura "blended" di Lucene invece di accreditarne una sola, cambierebbe
i punteggi e sarebbe un esperimento a sé.
