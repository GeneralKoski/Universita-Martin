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

## Esito

Misurato il 29/09/2026 sulle 104 known-item umane dei tre lotti, Koskidex
`cd86102`. Riassunto in `2026-09-29T094428Z_esito.json` (`analizza.py`); le sei
valutazioni nuove in `valutazioni-albo/2026-09-29T09442*`, le due senza analisi
sono LA e LT di `2026-09-25_known-item-umane/`.

| | MRR@10 | atto primo | entro 10 | a vuoto | candidati medi |
|---|---|---|---|---|---|
| `any`, nessuna | 0,5591 | 45,2% | 76,0% | 1,0% | 3.081 |
| `any`, stopword | 0,5491 | 43,3% | 78,8% | 1,0% | 1.424 |
| `any`, stemmer | **0,5664** | 45,2% | 77,9% | 1,0% | 3.222 |
| `any`, tutte e due | 0,5613 | 43,3% | 80,8% | 1,0% | 1.609 |
| `all`, nessuna | 0,3462 | 28,8% | 47,1% | 43,3% | 17,0 |
| `all`, stopword | 0,3665 | 29,8% | 51,0% | 39,4% | 17,4 |
| `all`, stemmer | 0,3589 | 28,8% | 49,0% | 39,4% | 20,5 |
| `all`, tutte e due | **0,3829** | 29,8% | 53,8% | 35,6% | 20,9 |

**Due previsioni su quattro.**

1. **Smentita.** Con `all` lo stemmer toglie 3,8 punti di query a vuoto (da
   45 a 41 su 104) e porta l'MRR@10 su di 0,013: nella direzione prevista, ma
   sotto tutte e due le soglie (5 punti e 0,02).
2. **Confermata.** Con `any` lo stemmer sposta l'MRR@10 di +0,007.
3. **Smentita, di un soffio.** Con `any` le stopword tolgono 0,0101 di
   MRR@10 (0,5491 contro 0,5591, dai valori esatti delle due valutazioni),
   appena oltre la soglia di 0,01.
4. **Smentita.** Con `all` le stopword tolgono 3,8 punti di query a vuoto,
   come lo stemmer, non meno di 2. La previsione pensava a parole come *di* e
   *per* presenti in quasi ogni scheda; non ho guardato perché non lo siano,
   ma le schede sono corte e una parola funzionale della query può mancare
   proprio lì.

Le due analisi insieme, con `all`, valgono più di ciascuna: 7,7 punti di
query a vuoto in meno (da 45 a 37) e +0,037 di MRR@10. Con `any` quasi non
contano. Nessuna diventa un default; il recupero congiuntivo è quello di
Koskidex innestato, e un'analisi italiana dentro il profilo consigliato si
potrebbe misurare come un tutto, come in `2026-09-25_configurazione-consigliata/`.
