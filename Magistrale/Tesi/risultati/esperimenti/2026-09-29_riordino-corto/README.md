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

## Esito

Misurato il 29/09/2026, Koskidex `0e914f5` per la valutazione,
`bge-reranker-v2-m3` alla stessa revisione di `2026-09-28_reranker`, MPS in
fp32. Riassunto in `2026-09-29T121254Z_esito.json` (`analizza.py`); rapporti
in `riordinati/`, valutazioni in `evaluate/`. I rapporti sulle umane
contengono il testo delle query e restano fuori da git. La colonna k 100 viene
da `2026-09-28_reranker`, gli stessi primi stadi.

MRR@10, con la recall del primo stadio entro k e la mediana del riordino:

| | primo stadio | k 20 | k 30 | k 100 |
|---|---|---|---|---|
| umane, LA | 0,5591 | **0,6242** (recall 0,827, 1,22 s) | 0,6293 (0,856, 1,95 s) | 0,6328 (0,913, 5,30 s) |
| umane, A | 0,6130 | **0,6430** (0,913, 1,28 s) | 0,6388 (0,923, 2,05 s) | 0,6405 (0,971, 5,93 s) |
| automatiche, LA | 0,8331 | **0,9486** (0,983, 1,24 s) | 0,9603 (1,000, 2,46 s) | 0,9528 (1,000, 5,07 s) |

**Cinque previsioni su cinque.**

1. **Confermata.** Umane LA: 0,6293 con k 30 e 0,6242 con k 20, contro 0,6328
   con k 100.
2. **Confermata.** Umane A: 0,6430 con k 20 contro 0,6405 con k 100. Con k 20
   è appena sopra, e la differenza è dentro il rumore di 104 query.
3. **Confermata.** Automatiche LA con k 20: 0,9486 contro 0,9528 con k 100.
4. **Confermata.** La mediana con k 20 è il 23,1%, il 21,5% e il 24,5% di
   quella con k 100.
5. **Confermata.** Con k 20 sulle umane la mediana resta 1,22 s (LA) e 1,28 s
   (A), sopra gli 0,8 s previsti.

**Cosa dice.** Riordinare solo i primi venti dà quasi tutto il guadagno del
riordino sui cento: il tetto si raggiunge già lì, e costa un quarto del
tempo. Non lo rende una ricerca dal vivo: un secondo e passa a query su questo
hardware, centinaia di volte Koskidex. Il risultato vale per i casi misurati,
in cui il primo stadio ha già l'atto quasi sempre nei primi venti (recall 0,83
con LA e 0,91 con A sulle umane); dove non c'è, il riordino non lo recupera.
