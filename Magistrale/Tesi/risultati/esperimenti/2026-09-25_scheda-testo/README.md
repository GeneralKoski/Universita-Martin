# Scheda contro testo intero, sugli atti di Crispiano

**Domanda.** Documentale indicizza la scheda di un atto, non il documento.
Quanto guadagna il recupero quando al posto della scheda c'è il testo intero?
E con documenti lunghi, il $b = 0{,}75$ di BM25 e il troncamento dei vettori
contano? È la domanda delle sezioni 5.7 e 7.1.

Scritto il 25/09/2026, prima che arrivi una sola risposta. Il troncamento dei
vettori a 2.048 token è misurato in `2026-09-25_contesto-ollama/`.

## Metodo

- **Solo Crispiano.** Due corpora dei soli 563 atti di Crispiano, dallo stesso
  export di Documentale: **scheda** (`beir-metadata`) e **testo** (`beir-full`,
  il testo estratto dai PDF). Solo i 563 atti, perché mescolare le due fonti in
  un indice solo cambierebbe lunghezza media e IDF di tutti.
- **Le query**: le known-item umane sugli atti di Crispiano (giudizi
  `qrels/crispiano.tsv`), circa 80. La persona ha letto il testo intero.
- **Le configurazioni**, Koskidex piatto, BM25 con la frequenza mescolata,
  refusi spenti:
  - LA (`any`) e LT (`all`) su scheda e su testo;
  - **sensibilità di $b$**: LA su testo con $b$ 0,25, 0,5 e 1, oltre a 0,75.
    Non si sceglie un valore guardando queste query: si guarda solo quanto
    l'MRR@10 dipende da $b$;
  - A (LA più vettori, unione, peso 160) su scheda, su testo con il contesto
    predefinito (2.048 token) e su testo con `-contesto 8192`.
- **Metriche**: MRR@10, atto primo, entro 10, a vuoto.

## Prima di misurare

1. **Il testo intero porta LA almeno 0,10 di MRR@10 sopra la scheda.**
2. **Con LT, il testo intero toglie almeno 20 punti percentuali di query a
   vuoto.** Sulla scheda una parola letta nel testo non c'è.
3. **Su testo, l'MRR@10 di LA con $b$ 0,75 sta entro 0,02 dal migliore dei
   quattro valori.** Su documenti tutti lunghi la normalizzazione tarata sugli
   articoli va bene.
4. **Su testo, A con il contesto di 8.192 token supera A con il contesto
   predefinito di almeno 0,02.** Quello che sta dopo i primi 2.048 token conta.
5. **Su testo, A supera LA di almeno 0,03.**

Se la 1 tiene, la raccomandazione per Documentale è indicizzare il testo
intero, e la sezione 5.7 lo dice con il suo numero. Se la 4 cade, spezzare i
documenti lunghi in parti (sezione 7.1) non serve a queste query.
