# Il riordino su meno candidati

**Domanda.** In `2026-09-28_reranker` il cross-encoder riordina i primi cento
candidati e costa da 5 a 12 secondi a query: troppo per una ricerca dal vivo.
Il costo cresce con il numero di coppie da leggere. Riordinando solo i primi
venti o trenta, quanto del guadagno resta, e quanto scende il costo?

Scritto il 29/09/2026, prima dello script e prima di qualunque misura. Da
`2026-09-28_reranker` conosco i numeri del riordino sui cento, la recall@100
del primo stadio e quanti atti stavano fra l'11° e il 100° posto (16 con LA,
12 con A sulle umane; 13 con LA sulle automatiche); non ho guardato quanti
stavano fra l'11° e il 20° o il 30°, né la recall@20 o @30.

## Metodo

Nessun primo stadio nuovo: `strumenti/riordina.py --k 20` e `--k 30` sui
primi stadi già archiviati in `2026-09-28_reranker/primo-stadio/` (salvati con
`-top 100`), con lo stesso modello (`BAAI/bge-reranker-v2-m3`, `max_length`
512, MPS, fp32), poi `scripts/evaluate -rankings -top 10` con gli stessi
giudizi. Il riordino dei primi k restituisce solo quei k: per MRR@10 non conta,
perché k è almeno dieci.

- known-item umane, LA e A (104 query);
- known-item automatiche, LA (300 query).

SciFact e NFCorpus restano fuori: la domanda è se il riordino si può usare in
Documentale, e lì contano le schede degli atti.

`analizza.py` riporta per ogni caso MRR@10 con k 20, 30 e 100 (il 100 da
`2026-09-28_reranker`), la recall@k del primo stadio e la mediana del tempo di
riordino.

## Prima di misurare

1. **Umane, LA**: con k 30 MRR@10 almeno 0,61, con k 20 almeno 0,60 (primo
   stadio 0,559, k 100 0,633). Buona parte degli atti recuperati dal riordino
   sui cento stava subito sotto il decimo posto.
2. **Umane, A**: con k 20 MRR@10 entro 0,01 da k 100 (0,641). I vettori hanno
   già portato in alto quasi tutti gli atti.
3. **Automatiche, LA**: con k 20 MRR@10 almeno 0,93 (primo stadio 0,833, k 100
   0,953).
4. **Il costo scala con k**: la mediana del tempo di riordino con k 20 sta fra
   il 15% e il 25% di quella con k 100, per ciascuno dei tre casi.
5. **Resta lento per l'uso dal vivo**: con k 20 la mediana è comunque almeno
   0,8 secondi a query sulle umane, centinaia di volte Koskidex.
