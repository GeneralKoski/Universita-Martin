# Fra `all` e `any`: recupero intermedio e coordinazione

**Domanda.** Sulle known-item BM25 perde contro l'euristico solo perché il
recupero è disgiuntivo: un atto senza il numero che ripete il nome del comune
somma più dell'atto giusto, e con `all` BM25 fa 0,976 contro 0,975
(`2026-09-25_known-item-divario/`). Ma `all` su SciFact è il difetto 0, 290
query su 300 a vuoto. Esiste un'impostazione unica che vada bene per le query
identificative e per quelle in lingua naturale?

## Metodo

Due varianti, ciascuna con un precedente e con un valore scelto prima di
misurare, non cercato sui dati:

- **`Settings.MinimumShouldMatch`**, con la sintassi di `minimum_should_match`
  di Elasticsearch, e il valore d'esempio della sua documentazione:
  **`2<-25% 9<-3`**. Fino a 2 termini li vuole tutti; da 3 a 9 tutti meno il
  25% arrotondato per difetto; oltre 9 tutti meno 3. Conta solo con
  `RetrievalMode = "any"`.
- **`Settings.Coordination`**, il fattore `coord` della `ClassicSimilarity` di
  Lucene (tolto in Lucene 7 insieme al passaggio a BM25): il punteggio del
  documento moltiplicato per la quota di termini della query che contiene. Non
  toglie documenti, cambia solo l'ordine.

Tutte e due spente per default. Base di confronto: BM25, recupero `any`,
frequenza mescolata, nessuna analisi, i numeri già archiviati.

| | known-item MRR@10 | SciFact nDCG@10 | NFCorpus nDCG@10 |
|---|---|---|---|
| `any`, frequenza mescolata (base) | 0,833 | 0,6694 | 0,3049 |
| `all`, frequenza mescolata | 0,960 | (difetto 0: quasi tutte a vuoto) | |

Lunghezza delle query in termini, guardata prima di misurare perché decide
dove morde `minimum_should_match`: SciFact mediana 12 (214 query su 300 con 10
o più), NFCorpus mediana 2 (101 query di un termine solo), known-item mediana
2,5 (150 di due termini).

Misure con `scripts/evaluate` sulle tre collezioni, una variante alla volta,
e i primi dieci id salvati per le known-item.

## Prima di misurare

Scritto e committato prima di scrivere il codice.

1. **`minimum_should_match`, known-item: MRR@10 almeno 0,93.** Le 150 query di
   due termini diventano congiuntive; quelle più lunghe quasi.
2. **`minimum_should_match`, SciFact: nDCG@10 scende di più di 0,02.** Con 12
   termini ne vuole 9: le stopword e le espansioni aiutano a soddisfarli, ma
   non abbastanza.
3. **`minimum_should_match`, NFCorpus: scende, di meno di 0,02.** Le query di
   un termine non cambiano; quelle di due diventano congiuntive.
4. **Coordinazione, known-item: MRR@10 almeno 0,93.** L'atto senza il numero,
   con metà dei termini, perde metà del punteggio.
5. **Coordinazione, SciFact e NFCorpus: entro 0,01 dalla base**, in un verso o
   nell'altro.

Se tengono la 4 e la 5 e non la 2, la coordinazione è l'impostazione unica
cercata; se no, la risposta è la scelta per tipo di query (piano, sezione 5).
