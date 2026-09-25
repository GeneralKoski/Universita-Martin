# Le elisioni in produzione

**Domanda.** Quanti atti la ricerca di Documentale non trova perché la parola
cercata, nell'atto, compare solo elisa? Il tokenizer standard di Elasticsearch
tiene insieme *dell'illuminazione* in un termine solo, quindi chi cerca
"illuminazione" non trova un atto che la nomina solo così. Il confronto del
23/09 (`2026-09-23_cause-divergenza/`) l'ha visto su 9 query delle 24, senza
separare le elisioni dalle date. Qui si conta sul corpus intero.

## Metodo

Tutto sull'Elasticsearch locale, sull'indice che l'app ha costruito
(`search-documents-local`, 10.018 atti, i sei campi di metadati del mapping di
produzione: il testo integrale di Crispiano non è indicizzato da
Elasticsearch).

1. **I termini veri dell'indice**, letti con `_mtermvectors`: non una
   ricostruzione del tokenizer, ma quello che Elasticsearch ha scritto.
2. **Termini elisi**: lettere, un apostrofo (`'` o `’`), lettere. La parte dopo
   l'apostrofo è la parola `w`. Si tengono le `w` di almeno tre lettere.
3. **Coppie a rischio**: (atto, `w`) in cui `w` compare nell'atto **solo**
   elisa, mai come termine a sé in nessuno dei sei campi.
4. **Coppie perse**: per ogni `w`, la query di produzione
   (`ElasticsearchService::fuzzySearch`: `best_fields`, `fuzziness AUTO`,
   `prefix_length 1`, `operator and`, stessi pesi) cercando `w` da sola. La
   coppia è persa se l'atto non è fra i risultati. Refusi e forme vicine
   (*impegni* per *impegno*) possono salvarla: per questo si interroga il
   motore invece di contare i termini.
5. **Controllo della causa**: un indice temporaneo con lo stesso mapping più il
   filtro `elision` con gli articoli italiani di Elasticsearch (quelli del suo
   analizzatore `italian`), stessi documenti, stesse query. Un atto perso che lì
   torna è perso per l'elisione e non per altro. Le forme che quell'elenco non
   copre (*quest'*, *sant'*, *quell'*) restano perse anche lì, e si contano a
   parte.

Si riportano: atti con almeno un termine eliso; coppie a rischio, salvate e
perse; atti con almeno una coppia persa; le stesse cifre per Crispiano e per il
Friuli Venezia Giulia; le parole con più atti persi (solo parole comuni, con
almeno 20 atti: niente nomi di persona nell'archivio).

Una coppia persa dice "la ricerca di questa parola da sola non trova l'atto".
Non dice quanto spesso qualcuno la cercherebbe: le query reali non ci sono.

## Prima di misurare

Scritto e committato prima di lanciare `conta.py`.

1. **Atti con almeno un termine eliso: fra il 30% e il 60%.** Il linguaggio
   amministrativo è pieno di *dell'*, *all'*, *l'* (*l'affidamento*,
   *dell'incarico*, *all'albo*), e anche gli oggetti corti del FVG ne hanno.
2. **La ricerca salva meno del 30% delle coppie a rischio.** I refusi da soli
   non bastano: *l'anno* dista due modifiche da *anno*, ma `prefix_length 1`
   vuole la prima lettera uguale, e la prima lettera di un termine eliso è una
   consonante mentre `w` comincia per vocale. Può salvarle solo un'altra forma
   della parola presente nell'atto, come un plurale.
3. **Il filtro `elision` recupera più del 90% delle coppie perse.** Il resto sono
   le forme fuori dall'elenco degli articoli.
4. **Le parole più colpite** fra: *anno*, *incarico*, *impegno*, *acquisto*,
   *ente*, *ufficio*, *area*, *esercizio*, *intervento*, *impianto*. Almeno
   cinque di queste fra le prime venti.
5. **Più di un atto su dieci ha almeno una coppia persa.** Se è così, il difetto
   non è un caso raro ma una proprietà del sistema su testi italiani.

## Come si rifà

```
TESI_RISULTATI=... python3 conta.py
```

Serve l'Elasticsearch locale su `localhost:9201` con l'indice dell'app, e il
MySQL locale (`doc-tesi-mysql`, database `albo`) per sapere da quale fonte viene
ogni atto. Lo script crea e poi cancella l'indice temporaneo
`elisioni-controllo`.
