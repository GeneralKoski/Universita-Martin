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

**Aggiunto dopo la prova di sviluppo, prima dell'esecuzione archiviata.** Fra
le parole più colpite sono uscite *isonzo* e *asio*, e vengono dal campo
`subjects`, che l'import riempie con l'ente (*Comune di Vito d'Asio*,
*Gradisca d'Isonzo*). Chi cerca un comune ne scrive probabilmente il nome con
l'apostrofo, e così lo trova. Le coppie la cui forma elisa sta solo in
`subjects` restano nel conteggio principale, e si riportano anche le cifre
senza di loro.

Si riportano: atti con almeno un termine eliso; coppie a rischio, salvate e
perse; atti con almeno una coppia persa; le stesse cifre per Crispiano e per il
Friuli Venezia Giulia; le parole con più atti persi, fra quelle presenti in
almeno 20 atti. A quella soglia restano parole comuni e toponimi, più due nomi
propri: *antonio*, da *Sant'Antonio*, e *andrea*, da *Sant'Andrea* e in due
atti dal cognome *D'Andrea*. Il conteggio di una parola sola non identifica
nessuno, e nell'archivio non finisce nessun titolo.

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

## Esito

`2026-09-25T082835Z_esito.json`, da `conta.py` al commit `8fdfe61` (albero
pulito), Elasticsearch 9.1.0, indice costruito dall'app a Documentale
`2a03310`. Nove secondi in tutto: 507 parole, una query ciascuna, 6,4 ms di
mediana. `id_atti_persi` sono gli id di Documentale, cioè `_id` di
Elasticsearch: `1` è `doc-0001` del corpus.

**Quattro atti su dieci hanno almeno una parola che la ricerca di quella parola
non trova.**

| | atti | % |
|---|---|---|
| atti nell'indice | 10.018 | |
| con almeno un termine eliso | 4.280 | 42,7% |
| con almeno una parola solo elisa (a rischio) | 4.103 | 41,0% |
| **con almeno una coppia persa** | **4.033** | **40,3%** |
| con almeno una coppia persa, escluso il solo nome dell'ente | 3.826 | 38,2% |

| | coppie (atto, parola) |
|---|---|
| a rischio | 5.913 |
| salvate dalla ricerca (refusi, forme vicine) | 138 (2,3%) |
| **perse** | **5.775** |
| perse, escluso il solo nome dell'ente | 5.464 |
| perse che il filtro `elision` recupera | 5.739 (99,4%) |

Per fonte: a Crispiano 195 atti persi su 563 (34,6%), nel Friuli Venezia Giulia
3.838 su 9.455 (40,6%), 3.631 escluso il nome dell'ente. Il difetto non dipende
da una fonte: è la lingua.

Le parole con più atti persi, su quante ne contengono la parola in qualche
forma:

| parola | atti con la parola | persi | quota persa |
|---|---|---|---|
| *art* | 1.406 | 595 | 42% |
| *ambito* | 399 | 228 | 57% |
| *anno* | 916 | 218 | 24% |
| *isonzo* | 230 | 215 | 93% |
| *asio* | 180 | 179 | 99% |
| *area* | 2.731 | 171 | 6% |
| *associazione* | 230 | 170 | 74% |
| *infanzia* | 220 | 168 | 76% |
| *affidamento* | 1.492 | 160 | 11% |
| *intervento* | 353 | 87 | 25% |
| *operatore* | 159 | 83 | 52% |
| *articolo* | 155 | 80 | 52% |
| *atto* | 229 | 80 | 35% |
| *impianto* | 254 | 80 | 32% |
| *interno* | 100 | 80 | 80% |

Chi cerca "infanzia" perde tre atti su quattro di quelli che la nominano,
perché si scrive quasi sempre *scuola dell'infanzia* o *nido d'infanzia*. E
*illuminazione*, l'esempio da cui è partito tutto, è fra le meno colpite: 12
atti su 99.

### Le previsioni

1. Atti con un termine eliso fra il 30% e il 60%: **42,7%, confermata.**
2. La ricerca salva meno del 30% delle coppie: **2,3%, confermata**, e molto
   sotto il limite. I refusi non salvano quasi niente, e le forme vicine (un
   plurale nello stesso atto) sono rare.
3. Il filtro recupera più del 90% delle coppie perse: **99,4%, confermata.** Delle
   36 che restano, 17 sono elisioni fuori dall'elenco degli articoli (13
   *sant'*, 2 *cinquant'*, *quest'*, *tutt'*), 13 sono parole attaccate per
   uno spazio mancante (*...effettidell'art*, *scuoladell'...*), dove il
   prefisso non è più un articolo, 2 sono accenti scritti come apostrofo
   (*conformita'*, *societa'*) davanti alla parola dopo, e 4 sono prefissi
   strani fuori elenco (*del'*, *sa'*, *app'*, *b'*).
4. Almeno cinque parole previste fra le prime venti: **sei, confermata**
   (*anno*, *area*, *intervento*, *impianto*, *ufficio*, *acquisto*). Non
   previste: *art* (i rinvii normativi, *dell'art. 36*), *ambito*,
   *associazione*, *infanzia*, e i due toponimi degli enti. *impegno* e
   *incarico*, previste, perdono poco: 46 atti su 1.697 e 60 su 327, perché
   compaiono spesso anche a sé (*impegno di spesa*).
5. Più di un atto su dieci con una coppia persa: **quattro su dieci,
   confermata**, e il margine è tale che il difetto va descritto come una
   proprietà del sistema su testo italiano, non come un caso limite.

### Da non leggere come perdita

`coppie_in_piu_nel_controllo_fuori_dalle_coppie_a_rischio` vale 5.141, ma non
sono atti persi. Sono atti che l'indice di controllo trova per una parola che
non vi compare: il filtro rende raggiungibile una forma vicina, e i refusi fanno
il resto. Il caso più grosso è *arte*, 575 coppie: dopo il filtro *dell'art.*
diventa *art*, che dista un refuso da *arte*. Sono in buona parte rumore della
ricerca con refusi, e nessuna cifra di perdita li conta.

### Cosa vuol dire per la tesi

È un difetto di recupero di Documentale in produzione, misurato sul codice di
produzione e con la causa confermata: aggiungere il filtro `elision` con gli
articoli italiani recupera il 99,4% delle coppie perse. In Elasticsearch la
correzione è una riga di mapping più una reindicizzazione. In Koskidex, con
`tokenizer: "standard"` il comportamento è lo stesso di Elasticsearch per
costruzione; col tokenizer predefinito l'apostrofo spezza il termine e il
difetto non c'è.

Un limite da scrivere accanto al numero: una coppia persa è una ricerca di una
parola sola che non trova un atto. Quanto conti per gli utenti dipende da
quanto spesso quelle parole si cercano, e query vere non ce ne sono.

## Come si rifà

```
TESI_RISULTATI=... python3 conta.py
```

Serve l'Elasticsearch locale su `localhost:9201` con l'indice dell'app, e il
MySQL locale (`doc-tesi-mysql`, database `albo`) per sapere da quale fonte viene
ogni atto. Lo script crea e poi cancella l'indice temporaneo
`elisioni-controllo`.
