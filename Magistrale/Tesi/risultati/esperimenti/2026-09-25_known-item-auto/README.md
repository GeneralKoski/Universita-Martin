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

**Aggiunto dopo la misura: il controllo della causa.** Visto il risultato di
Elasticsearch, `controllo-campi.py` rifà le stesse query sull'Elasticsearch
locale con un'unica differenza: ogni parola è un `multi_match` `best_fields` a
sé, con gli stessi refusi, lo stesso `prefix_length` e gli stessi pesi, e tutte
restano obbligatorie. Cade solo il vincolo che tutte le parole stiano nello
stesso campo. Il rapporto ha il formato dell'app e si valuta con lo stesso
codice. `analizza.py` riassume tutti i run e controlla la parità dei due
motori passati dall'app.

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

## Esito

`2026-09-25T084208Z_esito.json`, da `analizza.py` al commit `936886a`, sulle
valutazioni in `valutazioni-albo/` (Koskidex `f6810d0`, Documentale `2a03310`,
Elasticsearch 9.1.0, tutto da codice committato).

**Chi cerca un atto per numero e comune, in Documentale, non lo trova.**

| run | MRR@10 | atto primo | atto entro 10 | Recall@100 | a vuoto |
|---|---|---|---|---|---|
| Elasticsearch, dall'app | 0,017 | 1,3% | 2,0% | 0,02 | 211 (70%) |
| Koskidex innestato, dall'app | 0,018 | 1,7% | 2,0% | 0,02 | 211 (70%) |
| Elasticsearch, parole in campi diversi (controllo) | 0,534 | 36,3% | 96,0% | 1,00 | 0 |
| Koskidex piatto, `all` + euristico (baseline) | 0,975 | 95,7% | 99,7% | 1,00 | 0 |
| Koskidex piatto, `any` + euristico | 0,975 | 95,7% | 99,7% | 1,00 | 0 |
| Koskidex piatto, `any` + BM25 | 0,709 | 61,7% | 90,3% | 1,00 | 0 |

Elasticsearch torna vuoto su sette query su dieci, e sulle 89 in cui risponde
qualcosa l'atto giusto c'è solo in 6. Il controllo dice perché: con la stessa
query, gli stessi refusi e le stesse parole obbligatorie, ma ciascuna libera di
stare in un campo diverso, **l'atto giusto torna in tutte e 300** (Recall@100 da
0,02 a 1,00). La causa è `best_fields` con `operator and`: il numero sta in
`additional_data`, il comune in `subjects`, e nessun campo li ha tutti e due.

### Le previsioni

1. Elasticsearch entro i primi 10 in meno del 20% delle query, più della metà a
   vuoto: **2,0% e 70%, confermata.**
2. Koskidex innestato con gli stessi insiemi di Elasticsearch su almeno il 95%
   delle query: **300 su 300, confermata.** La parità regge su una famiglia di
   query che il confronto del 25/09 non conteneva, difetto compreso: Koskidex
   con le impostazioni compatibili riproduce anche gli errori di
   Elasticsearch, com'è giusto che sia.
3. Koskidex piatto entro i primi 10 in più del 70% delle query: **99,7%, 99,7%
   e 90,3%, confermata.**
4. BM25 e l'euristico a meno di 0,05 di MRR@10: **smentita, e nel verso che il
   README metteva in conto.** BM25 perde 0,27: mette l'atto primo nel 61,7%
   delle query contro il 95,7%, e in 29 query lo lascia oltre il decimo posto,
   contro una. È lo stesso segno di `ordinanza 187`
   (`2026-09-23_numero-atto/`), ora su 300 query invece che su due, e il
   perché resta da capire (sezione 3 del piano).

### Cosa non dice

Il controllo trova l'atto ma lo ordina male: primo solo nel 36% delle query.
Non è misurato perché. Un indizio è che i refusi di Elasticsearch ammettono una
modifica sui numeri di tre o quattro cifre, e `315` combacia con `316` e `305`,
come `187` con `18` e `17` nel caso dell'ordinanza, ma resta un'ipotesi.

Koskidex innestato con `all_terms_in_one_field` spento, cioè con le parole
libere di stare in campi diversi come fa Koskidex di suo, non è stato misurato:
la riga piatta ci si avvicina, ma ha un campo solo e i refusi spenti.

### Cosa vuol dire per la tesi

È il secondo difetto di recupero di Documentale in produzione, dopo le
elisioni, e questa volta sulla ricerca più identificativa che un documentale
abbia. Non dipende dal numero ma da come la query combina i campi. E dice una
cosa sul lavoro di compatibilità: arrivare alla parità con Elasticsearch
vuol dire ereditarne i difetti, e la parità è il punto di partenza da cui
misurare le correzioni, non il traguardo.
