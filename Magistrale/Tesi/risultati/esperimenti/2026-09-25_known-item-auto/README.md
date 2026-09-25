# Known-item automatiche: trovare un atto di cui si sa il numero

**Domanda.** Chi sa il numero di un atto e il comune che l'ha emesso lo ritrova?
È la ricerca identificativa più comune in un documentale, e sul corpus degli
albi si può fabbricare senza nessuno che annoti: la query nasce da un atto, e
quell'atto è la risposta giusta. È la prima misura di pertinenza sul corpus di
dominio, e la prima che mette Elasticsearch e Koskidex sotto le stesse metriche.

## Metodo

**Le query** (`strumenti/known-item-auto.py`, uscita in
`query/known-item-auto/`):

- forma: `<numero> <comune>`, per esempio `13605 Fiume Veneto`. Il numero viene
  da `numero_atto` per il FVG e dal nome dell'atto (`Determina N. 1223 ...`) per
  Crispiano; il comune da `subjects`, senza *Comune di*. Tutti i 172 enti del
  corpus sono comuni, quindi la forma è la stessa per tutti;
- si tengono solo gli atti con un numero che contiene almeno una cifra, e la cui
  coppia (comune, numero) è **unica** nel corpus: la numerazione riparte ogni
  anno, e una query che descrive due atti non ha una sola risposta giusta;
- 300 query estratte a caso fra gli atti ammessi, con seme fisso (`20260925`);
- un giudizio per query: l'atto di partenza, grado 2. Gli altri valgono zero.

**I motori**, sulle stesse 300 query:

- **Elasticsearch come lo usa Documentale**, passando dall'app
  (`app:eval-run-queries`, `fuzzySearch`: `best_fields`, `operator and`,
  `fuzziness AUTO`, sei campi pesati);
- **Koskidex innestato**, passando dall'app con `SEARCH_BACKEND=koskidex` e le
  impostazioni compatibili con Elasticsearch;
- **Koskidex piatto**, in memoria con `scripts/evaluate`: titolo e testo in un
  campo solo, refusi spenti, nelle tre configurazioni del pool (`all` +
  euristico, cioè il baseline; `any` + euristico; `any` + BM25).

I ranking dei due motori passati dall'app si valutano con `scripts/evaluate
-rankings`, cioè **con lo stesso codice delle metriche** di Koskidex.

**Le metriche.** Con un solo atto giusto per query: MRR@10 come misura
principale, la quota di query con l'atto al primo posto, Recall@100 (cioè
l'atto trovato entro i primi cento) e le query a vuoto.

**Cosa non misura.** Solo questa forma di query. `determina 1223` senza comune,
o col tipo d'atto, sono altre famiglie, da misurare a parte se servono. E le
query sono fabbricate: dicono se il motore trova un atto di cui si sa il
numero, non come lo cercherebbe una persona.

## Prima di misurare

Scritto e committato prima di scrivere il generatore e di lanciare qualsiasi
motore.

1. **Elasticsearch trova l'atto entro i primi 10 in meno del 20% delle query,
   e più della metà torna vuota.** Con `best_fields` e `operator and` tutte le
   parole devono stare nello stesso campo, ma il numero sta in
   `additional_data` e il comune in `subjects`. Resta trovabile solo un atto il
   cui oggetto contiene sia il numero sia il nome del comune.
2. **Koskidex innestato restituisce gli stessi insiemi di Elasticsearch su almeno
   il 95% delle query**: la parità del 25/09 regge anche su una famiglia di
   query che il confronto non conteneva.
3. **Le tre configurazioni piatte di Koskidex trovano l'atto entro i primi 10 in
   più del 70% delle query**, perché nel testo piatto numero e comune stanno
   insieme.
4. **Fra le configurazioni piatte, BM25 e l'euristico differiscono di meno di
   0,05 di MRR@10.** I documenti che contengono sia il numero sia tutte le
   parole del comune sono pochi, e l'ordine fra pochi candidati conta poco. Da
   ricordare che su `ordinanza 187` BM25 aveva fatto peggio
   (`2026-09-23_numero-atto/`): la previsione può essere smentita in quel verso.

Se la 1 regge, è un secondo difetto di Documentale in produzione, dopo le
elisioni: la ricerca di un atto per numero e comune non funziona, e non per il
numero ma per come la query combina i campi.
