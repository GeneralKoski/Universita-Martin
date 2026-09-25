# Risultati - l'archivio da cui escono numeri e grafici della tesi

Ogni numero e ogni grafico della tesi deve venire da un file di questa cartella.
Se un numero non ha un file qui, non esiste.

## Le regole

1. **Un file per esecuzione, mai sovrascritto e mai modificato a mano.** Il nome
   comincia con l'ora UTC dell'esecuzione: `2026-09-24T105340Z_<nome>.json`. Due
   esecuzioni nello stesso secondo diventano `...105341Z_<nome>.json` e
   `...105341Z-2_<nome>.json`: il contatore sta accanto all'ora, così il nome resta
   sempre in coda e `*_<nome>.json` trova tutte le esecuzioni.
2. **Ogni file dice da dove viene**, nel blocco `config`: il commit del codice,
   se c'erano modifiche non committate (`modifiche_non_committate`), il corpus
   (con la sua impronta SHA-256 quando è un file), ogni impostazione. Un numero
   prodotto da codice non committato non si rifà dal commit: il file lo dichiara,
   e per la tesi valgono solo quelli con `false`.
3. **I tempi sono in millisecondi, come numeri**, nel blocco `timings` o nel
   campo `ms` di ogni query. Stanno separati dalle metriche: le latenze cambiano
   a ogni esecuzione e le metriche no, e mescolarle renderebbe inutile il
   confronto fra due file.
4. **Solo identificativi, mai titoli.** Gli oggetti degli atti degli albi
   pretori possono contenere nomi di persone, e questa cartella sta in un
   repository pubblico. Per vedere un titolo si risale dal `doc-NNNN` al corpus,
   che resta fuori da git.
5. **Solo esecuzioni vere.** I controlli fatti mentre si scrive codice si lanciano
   con `TESI_RISULTATI=` vuota: non sono misure, e non devono finire qui.
6. **Si archivia da solo.** Gli strumenti scrivono qui se è impostata
   `TESI_RISULTATI` (è nel `~/.zshrc`); se non lo è, stampano
   `RISULTATO NON ARCHIVIATO` invece di tacere.

## Cosa c'è

| Cartella | Cosa contiene | Da dove viene |
|---|---|---|
| `koskidex-beir/` | valutazioni di Koskidex sulle collezioni pubbliche SciFact e NFCorpus: nDCG@10, Recall@100, MRR@10 per query, query a vuoto, tempi | `scripts/evaluate` di Koskidex |
| `valutazioni-albo/` | valutazioni sul corpus degli albi, stesso formato di `koskidex-beir/`: Koskidex in memoria e, con `-rankings`, i rapporti dei motori passati dall'app, contati dallo stesso codice | `scripts/evaluate -archivio valutazioni-albo` di Koskidex |
| `confronto/` | le stesse query su Elasticsearch (il codice di produzione di Documentale) e su Koskidex, sullo stesso corpus: ranking, latenza per query, tempi di indicizzazione | `app:eval-run-queries` di Documentale (col motore scelto da `SEARCH_BACKEND`), `scripts/compare` di Koskidex, `strumenti/indicizza-elasticsearch.sh`, `strumenti/indicizza-koskidex.sh` |
| `query/` | i file di query usati, così ogni esecuzione si rifà con le stesse | scritti a mano, vedi sotto |
| `esperimenti/` | esperimenti una tantum, con dati, codice per rifarli e spiegazione | una sottocartella per esperimento |
| `strumenti/` | script che non stanno in nessuno dei due progetti | |
| `macchina.md` | la macchina su cui sono stati misurati i tempi | |

### I comandi

```bash
# Koskidex su una collezione pubblica (da ~/Desktop/Progetti-personali/Koskidex)
go run ./scripts/evaluate -collection scifact -run bm25 -mode any -scoring bm25 [-analyzer english]

# Koskidex sul corpus esportato da Documentale
go run ./scripts/compare -corpus eval/corpora/c3-albo/beir-metadata/corpus.jsonl \
  -queries "$TESI_RISULTATI/query/confronto-24.txt"

# Elasticsearch con la query di produzione (da Documentale/apps/laravel)
DB_HOST=127.0.0.1 DB_PORT=33061 DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root \
  TELESCOPE_ENABLED=false php -d memory_limit=1G artisan app:eval-run-queries \
  "$TESI_RISULTATI/query/confronto-24.txt" --label=albo-metadata

# Costo della ricerca per sottostringa: aggiunge la configurazione con substring_match
go run ./scripts/compare -corpus eval/corpora/c3-albo/beir-metadata/corpus.jsonl \
  -queries "$TESI_RISULTATI/query/sottostringhe-20.txt" -sottostringa

# Le stesse query dall'app, su Koskidex innestato (serve un Koskidex in ascolto)
SEARCH_BACKEND=koskidex KOSKIDEX_HOST=http://localhost:7711 DB_HOST=127.0.0.1 DB_PORT=33061 \
  DB_DATABASE=albo DB_USERNAME=root DB_PASSWORD=root TELESCOPE_ENABLED=false \
  php -d memory_limit=1G artisan app:eval-run-queries "$TESI_RISULTATI/query/confronto-24.txt" --label=albo-metadata

# Valutazione sul corpus degli albi (da Koskidex; la collezione in
# eval/corpora/c3-albo/known-item-auto/ ha corpus, query e qrels come link):
# Koskidex in memoria, oppure il rapporto di un motore passato dall'app
go run ./scripts/evaluate -corpora eval/corpora/c3-albo -collection known-item-auto \
  -archivio valutazioni-albo -run any-bm25 -mode any -scoring bm25
go run ./scripts/evaluate -corpora eval/corpora/c3-albo -collection known-item-auto \
  -archivio valutazioni-albo -run app-elasticsearch -rankings <rapporto di app:eval-run-queries>

# Foglio di annotazione col pool di Koskidex più i ranking di Elasticsearch
go run ./scripts/pool -corpus <corpus.jsonl> -queries <queries.jsonl> -out giudizi.tsv \
  -run <rapporto di app:eval-run-queries>

# Un atto per intero, quando l'estratto del foglio non basta (vedi ../istruzioni-annotazione.md)
python3 "$TESI_RISULTATI/strumenti/mostra-atto.py" <corpus.jsonl> doc-0123

# Indicizzazione da indice vuoto, cronometrata, col comando dell'app
"$TESI_RISULTATI/strumenti/indicizza-elasticsearch.sh" albo albo-metadata
"$TESI_RISULTATI/strumenti/indicizza-koskidex.sh" albo albo-metadata http://localhost:7711
```

### I formati

**`koskidex-beir/*.json`** - `mean_ndcg@10`, `mean_recall@100`, `mean_mrr@10`,
`zero_results`, `per_query` (una riga per query con le tre metriche, `retrieved`,
`candidates`, `relevant`), `timings` (`index_ms`, `elapsed_ms`, `per_query_ms`
per id di query), `config`.

**`confronto/*_koskidex.json`** - JSON compatto. `configurazioni` (etichetta,
modalità di recupero, punteggio, `sottostringa`, `termini` cioè la dimensione
del vocabolario, `index_ms`; `sottostringa` e `termini` ci sono dai rapporti
del 24/09 ore 11:22 UTC in poi), `query` (per ogni query e ogni
configurazione: `ids` e `punteggi` dei primi risultati, al massimo 1.000,
`trovati` cioè il totale, `ms`), `config`. Il limite sta in
`config.risultati_conservati_per_query`: nessuna metrica guarda oltre le prime
100 posizioni, e gli insiemi congiuntivi del corpus albo restano sotto i 500.

**`confronto/*_elasticsearch.json`** e **`confronto/*_albo-metadata-koskidex.json`**
(prodotti da `app:eval-run-queries`) - `query` (per ogni query: `ids`, `ms`),
`config` (`motore`, versione del motore, indice, documenti indicizzati). Da non
confondere con `*_beir-metadata-koskidex.json`, che sono di `scripts/compare` e
interrogano Koskidex in memoria, senza l'app.

**`confronto/*_indicizzazione-{elasticsearch,koskidex}.json`** - `timings.index_ms`,
`documenti_indicizzati`, `config` (comando esatto, database, indice).

### Le query

`query/confronto-24.txt` - 24 query scritte a mano il 23/09/2026 per il
confronto fra i due motori, in quattro famiglie: corte (1-2 parole), medie (3-4),
in linguaggio naturale (6-9), per numero d'atto e con refusi. Servono a vedere se
i motori trovano le stesse cose, **non** a misurare la pertinenza: non hanno
giudizi di rilevanza, e nessun nDCG va calcolato su di loro.

`query/sottostringhe-20.txt` - 20 frammenti di parola scritti a mano il
24/09/2026 per misurare il costo della ricerca per sottostringa (Task F6):
radici di parole frequenti negli albi (`delib`, `determ`, `manut`...), un
numero (`2024`) e un frammento comunissimo (`zione`) come caso peggiore. Si
usano con `scripts/compare -sottostringa`.

`query/known-item-auto/` - 300 query `<numero> <comune>` generate il
25/09/2026 da `strumenti/known-item-auto.py`, ciascuna da un atto con la coppia
(comune, numero) unica nel corpus, con seme fisso. A differenza delle altre
hanno i giudizi (`qrels/test.tsv`: l'atto di partenza, grado 2), in formato
BEIR insieme a `queries.jsonl`; `queries.txt` è per `app:eval-run-queries`,
`generazione.json` ha i conteggi degli atti esclusi.

`query/known-item-auto-train/` - altre 300 query della stessa forma, seme
20260926, nessun atto in comune con il lotto di test, giudizi in
`qrels/train.tsv`. Servono solo per addestrare chi sceglie la configurazione
per query (`esperimenti/2026-09-25_scelta-per-query/`), mai per valutare.

`query/known-item-umane/` - le known-item scritte da persone, raccolte come
dice la parte 1 di `../istruzioni-annotazione.md`. `campione.json` (da
`strumenti/campione-atti.py`, seme 20260927) ha i quattro lotti di 40 atti, 20
per fonte, con fonte e genere di ogni atto. `strumenti/prepara-raccolta.py`
scrive in `pagine/` una pagina HTML per lotto, da aprire nel browser senza
rete; le pagine contengono il testo degli atti e git le ignora. I file che le
persone rimandano si copiano così come sono in `risposte/`, e
`strumenti/importa-raccolta.py` ricostruisce da tutti `queries.jsonl`,
`qrels/test.tsv`, `queries.txt` e `raccolta.json` (per ogni atto mostrato:
query, soprannome, secondi di lettura e di scrittura, se la pagina è stata
ricaricata, le query vuote con il motivo). Si misura solo a raccolta chiusa.

## Leggere i tempi senza farsi ingannare

- **Elasticsearch e Koskidex non si confrontano alla pari.** Elasticsearch gira
  in una macchina virtuale Docker con 4 CPU e 1 GB di heap, e il suo `ms` è il
  tempo della chiamata a `fuzzySearch` da PHP: include il viaggio HTTP e la
  deserializzazione. Koskidex gira nativo sugli 8 core, nello stesso processo
  che misura. Un grafico che li mette fianco a fianco lo deve scrivere.
- **L'indicizzazione di Elasticsearch** include il caricamento dei documenti da
  MySQL fatto dall'app e l'avvio di PHP; quella di Koskidex è la sola
  costruzione dell'indice in memoria da un file già letto.
- **La prima esecuzione di una serie è a freddo** (cache del sistema, di
  Elasticsearch, della JVM). Per questo le esecuzioni si ripetono, di solito tre.
- I tempi valgono sulla macchina di `macchina.md` e su nessun'altra.

## Registro

Quello che è stato tolto o toccato, perché la regola 1 non valga a metà.

- **23/09/2026, 12 file** in `koskidex-beir/`: prodotti dagli strumenti nuovi
  prima che fossero committati, e marcati `modifiche_non_committate: true`.
  Rifatti da codice committato, metriche identiche.
- **24/09/2026, 3 file** in `confronto/` (Elasticsearch, 23/09 ore 15:56 UTC):
  marcati `sconosciuto` per un difetto della provenienza (un albero pulito
  veniva scambiato per un errore di git). Difetto corretto, esecuzioni rifatte.
- **24/09/2026, 1 file rinominato**: `...105341Z_albo-metadata-elasticsearch-2.json`
  in `...105341Z-2_albo-metadata-elasticsearch.json`, quando il contatore delle
  collisioni è stato spostato accanto all'ora. Contenuto non toccato.
- **24/09/2026, 1 file** in `esperimenti/2026-09-23_numero-atto/` (ore 10:56:23
  UTC): prodotto da una versione dello script che interrogava Elasticsearch una
  volta in più per leggere la versione. Stesse posizioni, rifatto subito dopo.
- **24/09/2026, 3 file** in `confronto/` (Koskidex, 23/09 ore 15:56 UTC):
  12 MB ciascuno, perché salvavano l'intero ranking di ogni configurazione. Rifatti
  nel formato che conserva i primi 1.000 risultati e il totale, e verificati:
  teste dei ranking e totali identici. Da 12 MB a 1 MB.
- **24/09/2026, 1 file** in `esperimenti/2026-09-23_numero-atto/` (ore 10:56:37
  UTC): puntava a uno dei rapporti qui sopra. Rifatto sul rapporto nuovo; un
  primo rifacimento (10:58:31 UTC) riportava come totale gli id conservati invece
  di `trovati`, ed è stato rifatto a sua volta. Stesse posizioni: `2026-09-24T105848Z_esito.json`.
- **24/09/2026, 1 file** in `koskidex-beir/` (`2026-09-24T110812Z_scifact-bm25.json`):
  un controllo di regressione fatto durante lo sviluppo del Task F2, da codice
  non committato. Metriche identiche a quelle committate. Da qui in poi i
  controlli di sviluppo si lanciano con `TESI_RISULTATI=` vuota, e l'archivio
  riceve solo esecuzioni da codice committato.
- **25/09/2026, 1 file** in `esperimenti/2026-09-25_known-item-auto/`
  (`2026-09-25T084137Z_esito.json`): marcato `modifiche_non_committate: true`
  perché `analizza.py` guardava tutta la cartella, e dentro c'era il rapporto
  del controllo appena archiviato e non ancora committato. Il codice era quello
  committato. Il controllo ora guarda solo gli script; analisi rifatta, stessi
  numeri.
- **25/09/2026, 1 file** in `esperimenti/2026-09-25_known-item-divario/`
  (`2026-09-25T094222Z_esito.json`, mai committato): registrava il commit
  `143ef72`, il cui messaggio è stato corretto subito dopo con un amend, e che
  quindi non esiste più nel ramo. Stesso albero; analisi rifatta dal commit
  corretto `4e23f3d`, stessi numeri: `2026-09-25T094258Z_esito.json`.
- **I 12 file più vecchi di `koskidex-beir/`** (ore 11:5x e 14:0x UTC del
  23/09) vengono da prima degli strumenti di misura: hanno le metriche ma non
  hanno né `timings` né `config`. Le stesse configurazioni rifatte dopo hanno
  metriche identiche e i tempi.
