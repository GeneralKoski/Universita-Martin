# Le espansioni come sinonimi: nessuna regola di parità

**Domanda.** Con `bm25_expansion: blended` ogni espansione di una parola della
query (per prefisso o per refuso) usa la frequenza documentale più alta fra
quelle trovate, ma a un documento se ne accredita una sola: la più vicina, e a
parità di distanza la prima che si incontra. `2026-09-28_ordine-fisso` ha
misurato quanto pesa quella regola di parità arbitraria: 0,0024 di nDCG@10 su
SciFact. Lucene ha un modo di trattare più termini come uno solo, la
`SynonymQuery`: somma le loro frequenze nel documento e usa la frequenza
documentale più alta. Applicato alle espansioni non sceglie nessuna espansione,
e quindi non ha una regola di parità. Che effetto ha sui numeri della tesi?

Scritto il 28/09/2026, prima del codice.

## La correzione

Un valore nuovo di `bm25_expansion`, `synonym`: come `blended` per la frequenza
documentale, ma il TF di un documento per una parola della query è la somma
delle occorrenze di tutte le sue espansioni presenti nel documento, non solo di
quella accreditata. Refusi, match esatti e pesi dei campi restano calcolati come
oggi. `scripts/evaluate -bm25-espansioni synonym`.

## Metodo

`scripts/evaluate` (fuzziness `0`: le espansioni sono quelle per prefisso) su
SciFact, NFCorpus e le known-item automatiche, BM25 `all` e `any`, `blended`
contro `synonym`; su SciFact e NFCorpus anche BM25 `any` con le stopword, la
configurazione dello 0,6757. Ogni configurazione `synonym` anche con
`-ordine-fisso`.

## Prima di misurare

1. **Nessuna regola di parità**: con `synonym` le metriche per query sono le
   stesse con e senza `-ordine-fisso`, in ogni configurazione.
2. **Gli insiemi non cambiano**: stessi candidati per query di `blended` in ogni
   configurazione; cambia solo l'ordine.
3. **SciFact**: con BM25 `any` il nDCG@10 di `synonym` sta fra −0,005 e +0,02
   da quello di `blended`, con e senza stopword. Sommare le varianti di una
   parola (*cell*, *cells*, *cellular*) somiglia a uno stemmer leggero, che su
   SciFact aiuta.
4. **NFCorpus**: con BM25 `any` entro ±0,01 da `blended`, con e senza stopword.
5. **Known-item automatiche**: MRR@10 entro 0,01 da `blended`, con `all` e con
   `any`. Il TF sommato dei codici che cominciano con il numero cercato può
   pesare, ma la frequenza documentale mescolata lo tiene basso.
6. **Il costo**: mediana del tempo per query entro il 5% da `blended`.

## Esito

Da `2026-09-28T111554Z_esito.json` (`analizza.py`), Koskidex `b958ea0`, 24
valutazioni in `evaluate/`.

| | blended | synonym |
|---|---|---|
| SciFact `any`, nDCG@10 | 0,6694 | 0,6667 |
| SciFact `any` con stopword, nDCG@10 | 0,6757 | 0,6734 |
| NFCorpus `any`, nDCG@10 | 0,3049 | 0,3042 |
| NFCorpus `any` con stopword, nDCG@10 | 0,3062 | 0,3046 |
| known-item `all`, MRR@10 | 0,9596 | 0,9596 |
| known-item `any`, MRR@10 | 0,8331 | 0,8356 |

**Sei previsioni su sei confermate**, ma la terza per la ragione sbagliata.

1. **Confermata.** Con `synonym` le metriche per query sono identiche con e
   senza `-ordine-fisso` in tutte e 8 le configurazioni: nessuna regola di
   parità.
2. **Confermata.** Stessi candidati per query di `blended` ovunque.
3. **Confermata dalla soglia, smentita nel verso.** SciFact scende di 0,0028
   (0,0023 con le stopword), dentro la fascia da −0,005 a +0,02; avevo
   previsto che sommare le varianti aiutasse come uno stemmer, e non aiuta.
4. **Confermata.** NFCorpus scende di 0,0007 e 0,0016.
5. **Confermata.** Known-item: `all` identico, `any` +0,0025.
6. **Confermata.** Tempi fra −1,4% e +2,8%.

**Cosa ne segue.** Le due regole senza arbitrio, l'ordine lessicografico
(0,6670) e la somma (0,6667), danno su SciFact quasi lo stesso valore; lo
0,6694 della tesi è quello, un po' più alto, dell'ordine di ingresso
nell'indice. Il 99,5% del riferimento di Lucene con le stopword (0,6757)
diventa il 99,2% (0,6734) con la regola che non sceglie. Nessuna conclusione
della tesi cambia: tutte le differenze di questo esperimento stanno sotto
0,003, la stessa grandezza della regola di parità. `blended` resta il valore
delle misure già fatte; `synonym` è quello da usare dove serve un punteggio che
non dipenda dall'ordine.
