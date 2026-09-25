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

## Esito

`2026-09-25T094842Z_esito.json`, da `analizza.py`, sulle valutazioni di Koskidex
`2fd4721` (albero pulito) contro le basi archiviate da `f449b02`. Le basi,
rifatte su `2fd4721` come controllo di sviluppo non archiviato, danno gli
stessi 0,8331, 0,6694 e 0,3049.

| BM25, frequenza mescolata | known-item MRR@10 | atto primo | SciFact nDCG@10 | NFCorpus nDCG@10 |
|---|---|---|---|---|
| `any` (base) | 0,833 | 231 | 0,6694 | 0,3049 |
| `all` | 0,960 | 281 | (difetto 0) | |
| `any` + `2<-25% 9<-3` | 0,889 | 255 | **0,2556** (169 a vuoto) | **0,2268** (100 a vuoto, erano 24) |
| `any` + coordinazione | **0,944** | **275** | 0,6422 | 0,2935 |

**Atto primo per lunghezza della query** (known-item):

| | 2 termini (150) | 3-4 termini (106) | 5 o più (44) |
|---|---|---|---|
| `any` | 123 | 76 | 32 |
| `all` | 140 | 98 | 43 |
| `minimum_should_match` | 140 | 83 | 32 |
| coordinazione | 140 | 97 | 38 |

`minimum_should_match` rende congiuntive le query di due termini, e lì fa
quanto `all`; ma da tre termini ne lascia cadere uno, e spesso è il numero: 28
dei 45 fallimenti perdono contro un atto senza numero. La coordinazione fa
quasi quanto `all` su tutte le lunghezze, senza togliere niente.

### Le previsioni

1. `minimum_should_match`, known-item almeno 0,93: **smentita**, 0,889.
2. `minimum_should_match`, SciFact giù di più di 0,02: **confermata, e di
   molto**: da 0,6694 a 0,2556, 169 query a vuoto.
3. `minimum_should_match`, NFCorpus giù di meno di 0,02: **smentita**, giù di
   0,078, le query a vuoto da 24 a 100.
4. Coordinazione, known-item almeno 0,93: **confermata**, 0,944.
5. Coordinazione, SciFact e NFCorpus entro 0,01: **smentita**, SciFact giù di
   0,027 e NFCorpus di 0,011.

### Cosa vuol dire

**Non c'è un'impostazione unica.** `minimum_should_match` col valore della
documentazione è inservibile su tutte e tre: un vincolo sul numero di termini
che va bene per due parole è sbagliato per dodici. La coordinazione è il
compromesso migliore, perché chiude quasi tutto il divario sulle known-item
senza lasciare query a vuoto, ma costa 2,7 punti su SciFact: premia chi ha più
parole della query, e sulle frasi in lingua naturale le parole meno importanti
contano quanto le altre. È la ragione per cui Lucene l'ha tolta con BM25.

Resta la strada della sezione 5 del piano: riconoscere il tipo di query
(identificativa o in lingua naturale) e scegliere recupero e fusione di
conseguenza. Tutte e due le impostazioni restano spente per default.
