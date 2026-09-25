# La configurazione consigliata di Koskidex in Documentale

**Domanda.** Ogni correzione misurata finora è dietro un interruttore spento
per default, così il baseline resta quello di partenza. Per il confronto finale
serve però una configurazione sola, con un nome, da mettere contro
Elasticsearch: quella che le misure giustificano. Messe insieme, le correzioni
danno quello che davano una per una?

## La proposta

Nessun default cambia. In Documentale una variabile,
`KOSKIDEX_PROFILO=consigliata`, fa partire gli interruttori dal valore
consigliato invece che da quello di produzione; ogni variabile singola continua
a vincere sul profilo. Dentro ci sono solo le correzioni misurate **dall'app,
sul corpus di dominio**:

| interruttore | produzione | consigliata | perché |
|---|---|---|---|
| `KOSKIDEX_ALL_TERMS_IN_ONE_FIELD` | acceso | **spento** | con i numeri esatti l'atto è primo in 275 known-item su 300, da 5 (`2026-09-25_refusi-numeri/`) |
| `KOSKIDEX_TYPOS_ON_NUMBERS` | acceso | **spento** | come sopra: nessuna delle due correzioni basta da sola |
| `KOSKIDEX_ELISION` | spento | **acceso** | recupera le stesse coppie parola-atto del filtro di Elasticsearch, il 99,4% delle 5.775 perse (`2026-09-25_elisioni-koskidex/`) |

**Fuori, per ora, e cosa li deciderà:**

- **I vettori** (`KOSKIDEX_EMBEDDER_MODEL=bge-m3`, `KOSKIDEX_HYBRID_MODE=union`).
  Sulle collezioni piatte l'unione col recupero congiuntivo vale +0,62 su
  SciFact senza perdere sulle known-item (`2026-09-25_ibrido-congiuntivo/`), ma
  dall'app, sul corpus di dominio, se ne sa solo che non cambia gli insiemi
  col re-ranking. Li decidono i giudizi del pool delle 24 query.
- **BM25 con la frequenza mescolata**: misurato solo con Koskidex piatto;
  Documentale non lo espone, e il punteggio di Koskidex innestato resta quello
  che dà gli stessi insiemi di Elasticsearch. Lo decidono anch'essi i giudizi.
- **Stopword e stemmer italiani, `b` sui documenti lunghi**: aspettano le
  known-item umane.
- **Coordinazione e `minimum_should_match`**: misurati, nessuna impostazione
  unica regge (`2026-09-25_recupero-intermedio/`). Restano spenti.

## Come si misura

Koskidex `10c48bd` (quello di oggi) su un indice vuoto, riempito dall'app con
`KOSKIDEX_PROFILO=consigliata` e nessun'altra variabile di Koskidex; si
rileggono le impostazioni dell'indice. Poi `app:eval-run-queries` sulle 300
known-item automatiche e sulle 24 query del confronto, e `scripts/evaluate
-rankings -top 10` sulle known-item, come in `2026-09-25_refusi-numeri/`. Il
riferimento è la riga "parole libere, numeri esatti" di quell'esperimento
(Koskidex `ae1c4b9`, senza elisione) e i suoi rapporti del confronto.

## Prima di misurare

Scritto e committato prima di toccare il codice di Documentale.

1. **Le impostazioni dell'indice** sono `all_terms_in_one_field: false`,
   `disable_on_numbers: true` e i 21 articoli elisi, il resto uguale
   all'indice di produzione.
2. **Known-item**: MRR@10 entro 0,005 da 0,950, l'atto primo in 275 query ± 3,
   entro 10 in almeno 298, nessuna query a vuoto. Le query `<numero> <comune>`
   non hanno elisioni; l'elisione cambia solo qualche parola dei documenti, e
   quindi al più qualche lunghezza.
3. **Le 24 query**: nessuna perde un documento rispetto a "parole libere,
   numeri esatti", perché l'elisione aggiunge soltanto corrispondenze; almeno
   una ne guadagna; `ordinanza 187` e `determina 1223` restano con il solo
   atto giusto.

Se la 2 non tiene, le correzioni interagiscono, e la configurazione consigliata
va misurata come un tutto e non come somma di pezzi.

## Esito
