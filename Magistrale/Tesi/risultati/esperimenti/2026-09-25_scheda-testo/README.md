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

## Esito

Misurato il 29/09/2026 sulle known-item umane dei tre lotti che cercano atti di
Crispiano: **50 query**, non le circa 80 che il Metodo si aspettava con
quattro lotti. Koskidex `cd86102`. Riassunto in `2026-09-29T095003Z_esito.json`
(`analizza.py`), le dieci valutazioni in `valutazioni-albo/2026-09-29T0945*`.
L'esito delle 09:45 (`2026-09-29T094542Z_esito.json`) ha gli stessi numeri
senza la divisione per lunghezza, aggiunta per le ipotesi del diario.
I vettori del testo a 8.192 token vengono dalla cache di
`2026-09-25_contesto-ollama/` (14 vettori nuovi, quelli delle query mai viste
a quel contesto): `embedder` nel `config` è `ollama/bge-m3@8192`.

| | MRR@10 | atto primo | entro 10 | a vuoto |
|---|---|---|---|---|
| scheda, LA | 0,540 | 40% | 80% | 0% |
| scheda, LT | 0,262 | 18% | 40% | 48% |
| scheda, A | **0,613** | 48% | 92% | 0% |
| testo, LA ($b$ 0,75) | 0,463 | 30% | 78% | 0% |
| testo, LT | 0,344 | 22% | 60% | 26% |
| testo, A (2.048 token) | 0,558 | 40% | 88% | 0% |
| testo, A (8.192 token) | 0,515 | 36% | 86% | 0% |
| testo, LA, $b$ 0,25 / 0,5 / 1 | 0,439 / 0,454 / 0,477 | | | |

**Tre previsioni su cinque.**

1. **Smentita.** Il testo intero non porta LA sopra la scheda: la porta
   sotto, da 0,540 a 0,463 (-0,077).
2. **Confermata.** Con LT il testo intero toglie 22 punti di query a vuoto
   (da 24 a 13 su 50), e l'MRR@10 sale da 0,262 a 0,344.
3. **Confermata.** Su testo, $b$ 0,75 sta a 0,014 dal migliore dei quattro
   valori ($b$ 1, 0,477).
4. **Smentita.** A con il contesto di 8.192 token sta sotto A con quello
   predefinito, 0,515 contro 0,558 (-0,044): quello che sta dopo i primi 2.048
   token, su queste query, pesa contro.
5. **Confermata.** Su testo A supera LA di 0,095.

La 1 cade, e con lei la raccomandazione di indicizzare il testo intero: con il
recupero disgiuntivo, e con i vettori, la scheda ritrova l'atto meglio del
testo, anche se la persona ha letto il testo. Il testo intero aiuta solo il
recupero congiuntivo, che è quello di Documentale, perché gli dà più parole in
cui trovare tutte quelle della query: ma anche lì resta sotto la scheda con
LA o con A. La 4 cade, e secondo la regola scritta prima spezzare i documenti
lunghi in parti (sezione 7.1) non serve a queste query.

**Le quattro ipotesi del diario.** Il 23/09, prima di ogni misura, la voce di
Koskidex `eval/DIARIO.md` sul corpus misto aveva scritto quattro ipotesi senza
soglia sulla scheda contro il testo intero, da controllare sui soli atti di
Crispiano con query vere. Si controllano qui, con la divisione per lunghezza
di `analizza.py`: 30 query corte (fino alla mediana, 4 parole) e 20 lunghe.

| MRR@10 (entro 10) | corte, scheda | corte, testo | lunghe, scheda | lunghe, testo |
|---|---|---|---|---|
| LA | 0,525 (80%) | 0,496 (87%) | 0,561 (80%) | 0,414 (65%) |
| LT | 0,437 (67%) | 0,501 (83%) | 0,000 (0%) | 0,109 (25%) |
| A | 0,609 (90%) | 0,593 (87%) | 0,618 (95%) | 0,506 (90%) |

1. *Il testo aumenta il richiamo, con un guadagno piccolo sul nDCG@10.*
   **A metà.** Il richiamo sale con il recupero congiuntivo (LT, atto entro
   dieci dal 40% al 60%), non con quello disgiuntivo (LA, dall'80% al 78%), e
   con LA l'MRR@10 non sale di poco: scende di 0,077.
2. *Il guadagno è più grande sulle query lunghe.* **A metà.** Con LT sì
   (+0,109 sulle lunghe, +0,064 sulle corte); con LA e con A sulle lunghe il
   testo perde di più (-0,147 e -0,112, contro -0,029 e -0,016 sulle corte).
3. *Sulle ricerche per numero d'atto il testo non serve.* **Non misurata.**
   Delle 50 query solo 3 contengono una cifra.
4. *$b$ su un corpus di soli documenti lunghi conta meno.* **Confermata, senza
   soglia.** Fra $b$ 0,25 e 1 l'MRR@10 di LA sta in 0,038 (da 0,439 a 0,477),
   e 0,75 è a 0,014 dal migliore.
