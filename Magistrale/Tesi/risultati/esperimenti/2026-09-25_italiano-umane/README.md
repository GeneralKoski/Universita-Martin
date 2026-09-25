# Stopword e stemmer italiani sulle query umane

**Domanda.** Koskidex ha le stopword italiane di Snowball e lo stemmer leggero
di Savoy (sezione 5.6), mai misurati: le known-item automatiche sono un numero
e un comune e non li mettono alla prova. Sulle query scritte da persone,
servono?

Scritto il 25/09/2026, prima che arrivi una sola risposta.

## Metodo

Koskidex piatto con `scripts/evaluate`, corpus a schede (`beir-metadata`),
BM25 con la frequenza mescolata, refusi spenti, sulle known-item umane. Otto
configurazioni: recupero `any` e `all`, per ciascuno analisi `none`,
`italian-stopwords`, `italian-stemmer` e `italian` (tutte e due). Le due senza
analisi sono LA e LT di `2026-09-25_known-item-umane/`, le stesse esecuzioni.
Metriche come lì: MRR@10, atto primo, entro 10, a vuoto, candidati medi.

Una differenza con Lucene da tenere presente: Koskidex toglie gli accenti prima
di cercare nelle stopword, e *sarà* toglie anche il nome *Sara*.

## Prima di misurare

1. **Con `all`, lo stemmer toglie almeno 5 punti percentuali di query a vuoto e
   porta l'MRR@10 su di almeno 0,02.** Chi scrive *lavoro* non trova l'atto sui
   *lavori*, ed è il recupero congiuntivo a pagarlo.
2. **Con `any`, lo stemmer cambia l'MRR@10 di meno di 0,02.** Il recupero
   disgiuntivo tollera già una parola che non combacia.
3. **Con `any`, le stopword cambiano l'MRR@10 di meno di 0,01.** Su SciFact il
   loro guadagno veniva dalle espansioni per prefisso
   (`2026-09-25_stopword-espansioni/`), che la frequenza mescolata ha già
   corretto.
4. **Con `all`, le stopword cambiano le query a vuoto di meno di 2 punti.**
   *di*, *per*, *il* stanno in quasi ogni scheda: toglierle dalla query non
   rende il congiuntivo più facile.

Nessuna diventa un default: il profilo consigliato cambia solo con una misura
del profilo intero.
