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
