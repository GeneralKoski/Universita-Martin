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

**Aggiunto dopo la prova di sviluppo, prima dell'esecuzione archiviata.** La
prova ha dato 486 parole su 507 con lo stesso insieme fra `elis0` e la
produzione, sotto le 500 della previsione 1, con le stesse coppie perse. Come
scritto qui sotto, prima di leggere il resto ho cercato la causa, parola per
parola, in locale e senza archiviare niente. Due cause, nessuna di matching:

- in 20 parole Koskidex trova solo **di più**, mai di meno: toglie gli accenti
  ed Elasticsearch no, quindi *identita* trova anche *identità* e *unità* anche
  *unita'*, e un apostrofo rovinato dalla codifica (*allâ*) diventa *alla*, a
  un refuso da *ala*;
- in una, *comunale*, entrambi trovano tutti i 10.018 atti e restituiscono i
  primi 10.000: il tetto ne taglia 18 diversi perché l'ordine è diverso. In
  produzione l'app riceve gli stessi 10.000.

`analizza.py` conta queste due cause per ogni confronto fra motori (parole col
tetto, parole in cui un motore trova solo di più). La previsione 1 resta
com'era, e cade.

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

## Esito

`2026-09-25T105111Z_esito.json`, da `analizza.py` al commit `cfccf06` (albero
pulito). Koskidex compilato da `69035bb`, che rispetto a `76162dc` aggiunge
solo la voce del diario; Documentale `9998939`; Elasticsearch 9.1.0. Rapporti:
`confronto/2026-09-25T104804Z` e `104805Z` (le 24 su `elis0` ed `elis1`),
`104807Z` e `104809Z` (le known-item su `lib0` e `lib1`), valutazioni
`valutazioni-albo/2026-09-25T104815Z_*-lib0` e `-lib1`; indicizzazioni
`confronto/2026-09-25T104750Z`, `104752Z`, `104755Z`, `104757Z` (1,8-2,0 secondi
ciascuna). Undici secondi l'analisi intera.

**Con `KOSKIDEX_ELISION` acceso Koskidex innestato recupera le stesse coppie del
filtro di Elasticsearch, il 99,4%, e non toglie niente alle altre query.**

| 507 parole, 5.913 coppie a rischio | coppie perse | atti con una coppia persa |
|---|---|---|
| Elasticsearch di produzione | 5.775 | 4.033 |
| Koskidex `elis0` (come oggi) | **5.775, le stesse** | 4.033 |
| Elasticsearch col filtro `elision` | 36 | 36 |
| **Koskidex `elis1` (`KOSKIDEX_ELISION=true`)** | **36, le stesse** | **36** |

Le coppie perse non sono solo lo stesso numero: sono le stesse coppie, in
tutti e due i confronti. Le 36 che restano sono le forme fuori elenco già viste
con Elasticsearch: 13 *sant'*, 2 *cinquant'*, *quest'*, *tutt'*, parole
attaccate per uno spazio mancante (*scuoladell'*, *controllodell'*...), accenti
scritti come apostrofo (*conformita'*, *societa'*) e pochi prefissi strani.

Le ricerche costano 1,2 ms di mediana su Koskidex e 6,1 su Elasticsearch, con
o senza elisione (dallo script, senza PHP di mezzo: i tempi dall'app sono in
`2026-09-25_innesto-parita/`).

### Le previsioni

1. `elis0` e la produzione con lo stesso insieme per almeno 500 parole:
   **486, smentita.** Le cause sono quelle trovate nella prova di sviluppo e
   ora contate dallo script: in 20 parole Koskidex trova solo di più, mai di
   meno, perché toglie gli accenti (213 documenti in più, 67 per *unità*); in
   una, *comunale*, il tetto dei 10.000 risultati taglia 18 atti diversi.
   Nessuna parola in cui Elasticsearch trovi qualcosa che Koskidex non trova.
   La parità misurata sulle 324 query vale per il matching; sugli accenti i due
   motori sono diversi, e la differenza è a favore di chi cerca (*identita*
   scritto senza accento trova *identità*).
2. Le coppie perse da `elis0` quelle di Elasticsearch, entro l'1%: **le stesse
   5.775, confermata.**
3. `elis1` ne recupera almeno il 99%, con residui dalle stesse forme: **99,4%,
   le stesse 36 residue di Elasticsearch, confermata.**
4. `elis1` e il controllo con lo stesso insieme per almeno 480 parole: **485,
   confermata**, con le stesse due cause della 1 (21 parole con di più in
   Koskidex, una col tetto).
5. Documenti in più fra 4.600 e 5.700: **5.200, confermata** (5.141 per
   Elasticsearch).
6. Nessuna delle 24 query perde un documento, almeno una ne guadagna: **0 persi,
   65 guadagnati in 8 query, confermata.** *illuminazione pubblica* passa da 62 a
   73 atti, *contributo associazioni* da 17 a 48. I primi dieci cambiano in
   tre query, e solo perché vi entrano atti nuovi: gli altri restano nello
   stesso ordine (controllato a mano sui due rapporti, non dallo script).
7. Sulle known-item con le parole libere l'MRR@10 cambia di meno di 0,01:
   **0,9498 in entrambe, confermata.** Tutte le 300 query hanno gli stessi
   primi dieci, anche le 14 con l'apostrofo nel nome del comune, e l'atto resta
   primo in 275 ed entro dieci in 299.

### Cosa vuol dire per la tesi

Il difetto delle elisioni di Documentale (capitolo 6.2) ha ora una correzione
misurata in tutti e due i motori, con lo stesso effetto: nell'Elasticsearch di
produzione è un filtro nel mapping e una reindicizzazione, in Koskidex innestato
una variabile d'ambiente e una reindicizzazione. Non costa niente alle query
che non ne hanno bisogno.

Resta spenta per default, come tutte: i default si decidono alla fine, con il
relatore (`da-fare-a-mano.md`). Stopword e stemmer italiani sono pronti ma non
misurati: le known-item automatiche, un numero e un comune, non li mettono alla
prova, e aspettano quelle scritte da persone.

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
