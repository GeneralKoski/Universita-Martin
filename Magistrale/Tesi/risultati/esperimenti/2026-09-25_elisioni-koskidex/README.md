# Le elisioni con Koskidex innestato

**Domanda.** `2026-09-25_elisioni/` ha misurato che la ricerca di produzione di
Documentale non trova 5.775 coppie (atto, parola) su 5.913 a rischio, in 4.033
atti, perché la parola nell'atto compare solo elisa (*scuola dell'infanzia*,
mai *infanzia*), e che il filtro `elision` di Elasticsearch ne recupera il
99,4%. Koskidex innestato copia il tokenizer standard per avere gli stessi
insiemi, e con lui il difetto. Due domande:

1. Koskidex innestato perde **le stesse** coppie di Elasticsearch?
2. Con `KOSKIDEX_ELISION` acceso (Koskidex `Settings.ElisionArticles`, gli
   articoli dell'analizzatore `italian` di Elasticsearch) le recupera come il
   filtro di Elasticsearch, e cosa cambia per le altre query?

## Metodo

- Koskidex `76162dc` (analisi italiana `ddf344f`), compilato e avviato su una
  cartella dati nuova, porta 7711. Documentale `9998939` (flag
  `KOSKIDEX_ELISION`). Elasticsearch 9.1.0 locale con l'indice dell'app
  `search-documents-local`.
- **Quattro indici Koskidex**, ciascuno ricreato da vuoto e riempito dall'app con
  `strumenti/indicizza-koskidex.sh`, cambiando solo l'ambiente:

  | indice | `KOSKIDEX_ELISION` | campi | refusi sui numeri |
  |---|---|---|---|
  | `search-documents-elis0` | spento | campo unico (produzione) | sì (produzione) |
  | `search-documents-elis1` | acceso | campo unico | sì |
  | `search-documents-lib0` | spento | parole libere | no |
  | `search-documents-lib1` | acceso | parole libere | no |

  I primi due sono la configurazione di parità con Elasticsearch, gli ultimi
  due quella migliore misurata finora (`2026-09-25_refusi-numeri/`, atto primo
  in 275 known-item su 300). Dopo l'indicizzazione le impostazioni di ogni
  indice si rileggono da Koskidex e finiscono nell'esito.
- **Le coppie**, come in `conta.py`: i termini veri dell'indice di
  Elasticsearch (`_mtermvectors`), le parole di almeno tre lettere che in un
  atto compaiono solo dopo un apostrofo. Le stesse 507 parole.
- **Quattro motori per ogni parola**, cercata da sola:
  1. Elasticsearch di produzione, con la query di
     `ElasticsearchService::fuzzySearch` (la stessa di `conta.py`);
  2. l'indice di controllo di `conta.py`, lo stesso mapping più il filtro
     `elision`, creato e cancellato dallo script;
  3. Koskidex `elis0` e 4. Koskidex `elis1`, con la richiesta di
     `KoskidexClient::searchIds` di Documentale: `GET /indexes/{indice}/search`
     con `q`, `limit=10000`, `ids_only=true`, `fuzziness=AUTO`. Si replica la
     richiesta invece di passare da `app:eval-run-queries` per la stessa
     ragione di `conta.py`: nell'archivio finiscono solo conteggi e id, non
     507 parole accanto agli atti che le contengono (fra le rare ci sono
     cognomi, *D'Andrea*).
- **Gli effetti sulle altre query**, dall'app con `app:eval-run-queries`: le 24
  del confronto su `elis0` ed `elis1`, le 300 known-item su `lib0` e `lib1`,
  valutate con `scripts/evaluate -rankings -top 10`. Nelle 300 known-item 14
  query hanno un apostrofo, nel nome del comune (*Vito d'Asio*); nelle 24
  nessuna.

**Dichiarato.** Il codice di Koskidex (`ddf344f`, `76162dc`) e di Documentale
(`9998939`) è stato committato prima di questo README, non dopo come negli
esperimenti precedenti. Non è stata fatta nessuna misura prima: le sole
esecuzioni sono state di sviluppo, una su SciFact per controllare che le
opzioni nuove lascino identica la run di base, e una prova di funzionamento
delle opzioni italiane sulle known-item di cui ho letto solo la configurazione
registrata, non le metriche.

## Prima di misurare

Scritto e committato prima di costruire gli indici e lanciare le query.

1. **Koskidex `elis0` e Elasticsearch di produzione danno lo stesso insieme per
   almeno 500 parole su 507.** La parità è stata 24 su 24 e 300 su 300. Le
   differenze possibili vengono dagli accenti: Koskidex li toglie ed
   Elasticsearch no, e fra le parole elise ce ne sono di accentate.
2. **Le coppie perse da `elis0` sono quelle di Elasticsearch**: lo stesso numero
   a meno dell'1% (5.775 ± 58).
3. **`elis1` recupera almeno il 99% delle coppie che `elis0` perde**, e quelle
   che restano sono le stesse forme fuori elenco trovate con Elasticsearch
   (*sant'*, parole attaccate per uno spazio mancante, accenti scritti come
   apostrofo).
4. **`elis1` e l'indice di controllo di Elasticsearch danno lo stesso insieme per
   almeno 480 parole su 507** (95%). Meno che nella 1, perché il filtro cambia
   anche quali termini sono a un refuso da quali, e lì gli accenti contano di
   più.
5. **I documenti in più**, trovati da `elis1` per una parola che nel documento
   non compare elisa (il rumore dei refusi, *art* a un refuso da *arte*), sono
   fra 4.600 e 5.700, cioè entro il 10% dei 5.141 di Elasticsearch.
6. **Nessuna delle 24 query del confronto perde un documento** passando da
   `elis0` a `elis1`, e almeno una ne guadagna. Il filtro sostituisce un
   termine eliso con la parola, non ne toglie: un documento può uscire solo se
   era trovato per un refuso sulla forma elisa, ed è raro.
7. **Sulle 300 known-item, con le parole libere, l'MRR@10 cambia di meno di
   0,01** fra `lib0` e `lib1`, e l'atto entro i primi dieci non scende sotto le
   299 query. Almeno 280 delle 286 query senza apostrofo hanno gli stessi primi
   dieci.

Se la 1 cade, prima di leggere il resto va capita la causa: vorrebbe dire che
la parità misurata su 324 query non vale sulle parole singole.

## Come si rifà

```
# Koskidex dal commit indicato, su una cartella nuova
go build -o /tmp/koskidex-tesi . && /tmp/koskidex-tesi -port 7711 -data-dir <cartella nuova>

# I quattro indici, dall'app (da Magistrale/Tesi/risultati)
for c in "elis0 false true true" "elis1 true true true" "lib0 false false false" "lib1 true false false"; do
  set -- ${=c}
  KOSKIDEX_INDEX_NAME=search-type-$1 KOSKIDEX_ELISION=$2 KOSKIDEX_ALL_TERMS_IN_ONE_FIELD=$3 \
    KOSKIDEX_TYPOS_ON_NUMBERS=$4 strumenti/indicizza-koskidex.sh albo albo-$1 http://localhost:7711
done

# Le query dall'app e le valutazioni: vedi l'esito
TESI_RISULTATI=... python3 analizza.py
```
