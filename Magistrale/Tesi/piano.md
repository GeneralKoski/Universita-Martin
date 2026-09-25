# Piano - cosa resta da fare

Unico piano della tesi, dal 25/09/2026. Sostituisce `piano-autunno-2026.md` e
`piano-implementazione.md`, che avevano ormai quasi tutto spuntato: la loro
ultima versione è nel commit `5f9b080` di questo repository, e si rilegge con

```
git show 5f9b080:Magistrale/Tesi/piano-autunno-2026.md
git show 5f9b080:Magistrale/Tesi/piano-implementazione.md
```

Nell'archivio `risultati/` e nel diario di Koskidex ricorrono i loro nomi: i
**Task A-F** sono di `piano-autunno-2026.md`, le **Fasi 0-4** e i Task *n.m* di
`piano-implementazione.md`.

La domanda di tesi, le scelte e il perché stanno in [appunti.md](appunti.md).
L'indice dei capitoli, con lo stato di ogni sezione e il materiale che la
sostiene, sta in [indice.md](indice.md) e in `latex/capitoli/`.
Quello che non è sviluppo (persone da trovare, test da far fare, decisioni,
relatore) è raccolto anche in [da-fare-a-mano.md](da-fare-a-mano.md): per ora il
lavoro va avanti sullo sviluppo.

## Dove siamo (25/09/2026)

| Cosa | Stato | Dove |
|---|---|---|
| Impianto di valutazione (metriche, esecutore, pool, archivio) | fatto | Koskidex `internal/eval`, `scripts/`; `risultati/README.md` |
| Difetto 0, recupero congiuntivo | chiuso e misurato | `Settings.RetrievalMode`; `eval/DIARIO.md` |
| Difetto 1, niente IDF (BM25) | chiuso e misurato: con stopword e frequenza mescolata SciFact 0,6757 contro 0,6789 di BEIR (99,5%), NFCorpus 0,3062 contro 0,3218 (95%) | `Settings.ScoringMode`, `Settings.Stemmer`, `Settings.BM25Expansion` |
| Corpus pubblico degli albi pretori, 10.018 atti | importato in Documentale ed esportabile | Koskidex `eval/corpora/c3-albo/SOURCE.md` |
| Koskidex completo rispetto al contratto di Documentale (F1-F7) | fatto: 24 insiemi su 24 uguali a Elasticsearch | `risultati/esperimenti/2026-09-23_cause-divergenza/` |
| Innesto in Documentale, motore scelto da `SEARCH_BACKEND` | fatto: dall'app 24/24 insiemi uguali, ricerca 2,7 ms contro 22 | Documentale `67cf954`, `2a03310`; `risultati/esperimenti/2026-09-25_innesto-parita/` |
| Ricerca per numero e comune in Documentale | dal 2% entro 10 in produzione al 92% primo, con due impostazioni di Koskidex | `risultati/esperimenti/2026-09-25_refusi-numeri/` |
| Difetti 2 e 3 (ibrido e fusione) | chiusi e misurati: con il recupero congiuntivo l'unione vale +0,62 su SciFact; il peso del vettore va scelto per tipo di query | qui sotto, sezione 5 |
| Query e giudizi sul corpus di dominio | assenti | qui sotto, sezioni 1 e 2 |

## Regole

Valgono per tutto quello che segue. Se ne salta una, i numeri diventano
contestabili e non c'è modo di rimediare dopo.

1. **Ogni modifica che cambia i risultati sta dietro un campo di `Settings`**,
   con il comportamento di oggi come default.
2. **`TestBaselineRankingIsFrozen` passa a default**, senza toccare il test.
3. **Ogni modifica ha la sua voce in `eval/DIARIO.md`**, e la sezione *Prima di
   misurare* si committa **prima** di lanciare la valutazione, in un commit a
   parte.
4. **Ogni numero della tesi viene da un file di `risultati/`**, scritto dagli
   strumenti (`TESI_RISULTATI` nel `~/.zshrc`), mai sovrascritto, con commit e
   stato dell'albero. I controlli di sviluppo girano con `TESI_RISULTATI=`
   vuota, così non finiscono nell'archivio.
5. **Rilevanza e prestazioni si misurano separate**: dati seminati vanno bene per
   latenza e memoria, mai per la rilevanza.
6. **Koskidex resta a zero dipendenze esterne** oltre `golang.org/x/text`, test
   e valutazione compresi.
7. **Su Documentale si lavora solo sul branch `martin/tesi-magistrale`.**
   `ElasticsearchService` resta com'è, `operator => and` compreso: è il baseline
   di produzione.
8. **Il corpus non si committa**: contiene nomi di persone, pubblici per legge ma
   da non ripubblicare. Nel repo vanno gli script che lo riscaricano e i file
   con gli id; negli esempi della tesi, nomi anonimizzati.
9. **Elasticsearch solo in locale** (`localhost:9201`): il cluster in cloud del
   `.env` non risponde più.

## La catena di valutazione

```
fetch-albo.py -> app:import-albo-corpus        (Documentale, corpus nel DB)
app:export-eval-corpus  -> corpus.jsonl         (formato BEIR)
query (known-item)      -> queries.jsonl
scripts/pool            -> giudizi.tsv          <- qui si annota
scripts/pool -sheet     -> qrels/test.tsv
scripts/evaluate        -> nDCG@10, Recall@100, MRR@10
app:eval-run-queries    -> ranking del motore configurato, con gli id del corpus
```

Due decisioni sul pooling che contano più del codice:

- **il foglio è ordinato per id del documento**, mai per posizione né per
  configurazione: chi annota in ordine di ranking finisce per confermarlo;
- **un grado vuoto è un errore, non uno zero**: la conversione si ferma e dice
  quale riga manca.

Il recall misurato così resta un limite superiore: un documento che nessuna
configurazione pesca non viene mai giudicato.

## Da fare

In ordine. Le sezioni 1-4 non dipendono dai vettori e si fanno per prime.

### 1. Rendere il metro difendibile, prima di annotare

Rifare i giudizi perché il pool era incompleto è l'unico lavoro davvero buttato.

- [x] Istruzioni di annotazione (25/09/2026, [istruzioni-annotazione.md](istruzioni-annotazione.md)):
      raccolta delle known-item umane con l'atto nascosto prima di scrivere,
      bisogno informativo scritto e committato prima di aprire il pool, scala
      0-2 con i casi dubbi, tempi per sessione, secondo annotatore su query
      intere (almeno 150 righe) con kappa semplice e pesato
- [x] **Strumenti per le known-item umane** (25/09/2026): campione di 160 atti
      in quattro lotti da 40, metà per fonte; una pagina HTML per lotto che
      mostra, nasconde, registra i tempi e scarica il file da rimandare;
      l'importatore che costruisce la collezione e rifiuta file che non
      corrispondono al lotto. Provati con un browser automatico su tutti i 160
      atti (`risultati/query/known-item-umane/`)
- [ ] Lo strumento che calcola il kappa: da scrivere quando ci sono i giudizi
      del pool, non prima
- [x] `scripts/pool -run <rapporto>` unisce al pool i ranking di
      `app:eval-run-queries` (Koskidex `5e771dd`), e rifiuta query non eseguite,
      id fuori dal corpus e rapporti di altro formato
- [x] Il pool cresce davvero: sulle 24 query del confronto, a profondità 10,
      Elasticsearch porta 87 documenti che nessuna configurazione di Koskidex
      aveva, da 428 a 515

### 2. Le query, che nessun log produrrà

Documentale non ha più utenti: le query vanno fabbricate, e in tesi va scritto
con questa parola. Le due famiglie misurano cose diverse e restano separate.

- [x] **Known-item automatiche** (25/09/2026): 300 query `<numero> <comune>`
      in `risultati/query/known-item-auto/`. Elasticsearch in produzione trova
      l'atto entro i primi 10 nel **2%** delle query e torna vuoto nel 70%,
      perché numero e comune stanno in campi diversi; Koskidex piatto lo trova
      nel 99,7%. Koskidex innestato: stessi insiemi di Elasticsearch, 300 su 300
      (`risultati/esperimenti/2026-09-25_known-item-auto/`). `scripts/evaluate
      -rankings` valuta i rapporti dell'app con lo stesso codice delle metriche
- [ ] **Known-item umane**: trovare almeno tre persone che non conoscano i
      motori, un lotto da 40 atti ciascuna; mandare la pagina del lotto, farsi
      rimandare il file, copiarlo in `risposte/` e lanciare
      `importa-raccolta.py`
- [ ] Secondo annotatore (Leopoldo) su query intere estratte a caso dal foglio
      annotato, almeno 150 righe, e Cohen's kappa riportato comunque, anche se
      basso (parte 3 delle istruzioni)
- [ ] Prima di annotare il corpus di dominio, sentire il relatore (sezione 7)

### 3. Misure che mancano sul lessicale già fatto

- [x] **Elisioni in produzione** (25/09/2026): **4.033 atti su 10.018 (40,3%)**
      hanno almeno una parola che la ricerca di quella parola non trova, perché
      nell'atto compare solo elisa. La ricerca ne salva il 2,3%, il filtro
      `elision` di Elasticsearch ne recupera il 99,4%
      (`risultati/esperimenti/2026-09-25_elisioni/`)
- [x] **Elisioni con Koskidex innestato** (25/09/2026, Koskidex `ddf344f`,
      Documentale `9998939`): con `KOSKIDEX_ELISION=true` (spento per default)
      Koskidex recupera **le stesse coppie** del filtro di Elasticsearch, il
      99,4%, e restano le stesse 36. Senza, perde le stesse 5.775 della
      produzione. Nessuna delle 24 query del confronto perde un atto, 8 ne
      guadagnano; le 300 known-item restano identiche. Sugli accenti la parità
      non vale: in 20 parole Koskidex trova di più, perché li toglie
      (`risultati/esperimenti/2026-09-25_elisioni-koskidex/`)
- [x] **BM25 e la ricerca per numero d'atto** (25/09/2026): sulle 300
      known-item BM25 fa MRR@10 0,709 contro 0,975 dell'euristico. In 61 dei
      115 fallimenti vince un atto che combacia solo per prefisso (`190` con
      `1900129`): BM25 pesa l'espansione con l'IDF del termine trovato, raro,
      invece che con quello del termine cercato. Senza prefisso 0,854, con
      `k1 = 0,3` 0,900, con `b = 0` solo 0,731
      (`risultati/esperimenti/2026-09-25_bm25-numeri/`)
- [x] **Il peso delle espansioni in BM25** (25/09/2026, Koskidex `f449b02`):
      `Settings.BM25Expansion = "blended"`, la frequenza documentale più alta
      fra i termini trovati, come Lucene per le fuzzy. Known-item MRR@10 da
      0,709 a 0,833; e **SciFact da 0,6197 a 0,6694, NFCorpus da 0,2810 a
      0,3049**: le espansioni per prefisso costavano fino a cinque punti anche
      sulle collezioni pubbliche. Insiemi identici. Dettagli nella voce del
      diario di Koskidex
- [x] **Quanto del guadagno delle stopword (voce E1) veniva dalle espansioni**
      (25/09/2026): quasi tutto. Col prefisso spento le stopword portano
      SciFact da 0,6634 a 0,6664, contro 0,6197 a 0,6641 col prefisso acceso;
      `of` compare in 173 query su 300 e porta 26 espansioni di frequenza
      mediana 2 (`risultati/esperimenti/2026-09-25_stopword-espansioni/`)
- [x] **Il divario che resta sulle known-item** (25/09/2026): non viene dalle
      espansioni ma dal recupero disgiuntivo. In 36 dei 69 fallimenti vince un
      atto senza il numero che ripete il nome del comune; con `all` BM25 fa
      0,976 contro 0,975 dell'euristico (288 atti primi contro 287). Le due
      correzioni previste non servono
      (`risultati/esperimenti/2026-09-25_known-item-divario/`)
- [x] **Recupero intermedio** (25/09/2026, Koskidex `2fd4721`): nessuna
      impostazione unica. `minimum_should_match` `2<-25% 9<-3` porta le
      known-item a 0,889 ma SciFact a 0,2556 (169 query a vuoto); la
      coordinazione di Lucene porta le known-item a 0,944 ma costa 0,027 su
      SciFact. Spente tutte e due; resta la scelta per tipo di query della
      sezione 5 (`risultati/esperimenti/2026-09-25_recupero-intermedio/`)
- [ ] **Decidere i default** di `BM25Expansion` e degli altri interruttori
      misurati: cambiarli cambia il baseline, e va deciso a parte, con il
      relatore
- [x] **Documentale e la ricerca per numero e comune** (25/09/2026): Koskidex
      innestato con `KOSKIDEX_ALL_TERMS_IN_ONE_FIELD=false` (Documentale
      `0c6cacf`, acceso per default) trova l'atto entro i primi 10 nel 93%
      delle query invece del 2%, ma primo solo nel 38%: in 154 casi su 185 lo
      scavalca un atto con **il numero a un refuso** (`1109` per `1209`)
      (`risultati/esperimenti/2026-09-25_koskidex-campi-liberi/`)
- [x] **Niente refusi sui termini numerici** (25/09/2026, Koskidex
      `ae1c4b9`, Documentale `ab52f4f`): `TypoTolerance.DisableOnNumbers`, come
      `disableOnNumbers` di Meilisearch. Con le parole libere e i numeri
      esatti l'atto è **primo in 275 known-item su 300** (erano 5 in
      produzione), entro 10 in 299; `ordinanza 187` e `determina 1223` danno
      solo l'atto giusto. Con il campo unico le query a vuoto salgono dal 70% al
      95% (`risultati/esperimenti/2026-09-25_refusi-numeri/`). Le collezioni
      pubbliche non si misurano: la valutazione piatta spegne i refusi
- [ ] **`b` sui documenti lunghi**: rimisurarlo sui soli 563 atti di Crispiano
      col testo intero. 0,75 è tarato su collezioni di articoli, e nel corpus
      misto le schede corte schiacciano la lunghezza media
- [ ] **Scheda contro testo intero** sugli stessi 563 atti, una misura per
      variante: è la domanda del corpus (quanto guadagna il recupero quando al
      posto della scheda c'è il documento), e mescolare le due fonti in un
      indice solo dà una risposta falsa

### 4. Analisi lessicale italiana

- [x] **I tre stadi dell'analizzatore `italian` di Elasticsearch** (25/09/2026,
      Koskidex `ddf344f`): `Settings.ElisionArticles` con gli articoli di
      Lucene, `ItalianStopWords()` (Snowball), `Settings.Stemmer =
      "italian_light"` (`ItalianLightStemmer`, uguale a Lucene sulle 35.494
      parole del suo vocabolario di prova). Tutti spenti per default; in
      `scripts/evaluate` `-analyzer italian-stopwords|italian-stemmer|italian`,
      `-tokenizer standard`, `-elisione` (`76162dc`)
- [x] Elisioni misurate (sezione 3)
- [ ] **Stopword e stemmer italiani da misurare** sulle known-item umane: quelle
      automatiche sono un numero e un comune e non li mettono alla prova. Voce
      di diario e ipotesi prima, come sempre
- [ ] Decidere come trattare date (`14.01.2026`) e decimali (`3,5`) fuori dalla
      modalità compatibile con Elasticsearch, e misurarlo

### 5. Difetti 2 e 3: l'ibrido e la fusione

Il difetto 2 è il vettoriale che non porta candidati propri (re-ranking, non
recupero ibrido); il difetto 3 è la fusione `sim * 20.0` contro un lessicale che
cresce con la lunghezza della query. Da tenere distinti dal difetto 0 anche in
tesi. Il piano di dettaglio del 15/09 (Fasi 2 e 3 di `piano-implementazione.md`)
è in `5f9b080`, ma va riscritto contro il codice di oggi: le righe di
`ranker.go` che citava sono cambiate.

- [x] Da dove vengono gli embedding: **modello locale** (25/09/2026), via
      Ollama
- [x] **Modello: `bge-m3`** (Ollama 0.34.4, digest `790764642607`, 1024
      dimensioni, vettori già normalizzati, contesto 8192), multilingue e
      senza prefissi da aggiungere a query e documenti. Nome e digest vanno in
      ogni esito
- [x] **Embedder in Koskidex** (25/09/2026, `5364533`): `Settings.Embedder`,
      spento per default. Calcola `_vector` all'aggiunta dei documenti e il
      vettore della query con `hybrid=true`; cache dei vettori per modello e
      testo in `<data-dir>/embeddings.jsonl`. Dal vivo: 1.000 schede degli albi
      in 51 secondi la prima volta, 0,15 dalla cache
- [x] `scripts/evaluate` con l'embedder e la stessa cache (Koskidex
      `4b7b97b`): `-embedder bge-m3`, cache in `eval/cache/`. Prima volta: 11
      minuti SciFact, 8 NFCorpus, 9 gli albi
- [x] **Vettori dall'app** (25/09/2026, Documentale `2488dfd`):
      `KOSKIDEX_EMBEDDER_MODEL`, `KOSKIDEX_HYBRID_MODE`, `KOSKIDEX_FUSION_MODE`,
      `KOSKIDEX_FUSION_ALPHA`, tutti spenti per default. Provato dal vivo con
      Koskidex `d3ffe17`: i 10.018 atti in 8 minuti con `KOSKIDEX_TIMEOUT=600`
      (col timeout predefinito di 15 s fallirebbe). Il timeout di scrittura di
      Koskidex (60 s) non è scattato, ma un blocco da 1.000 atti ci arriva
      vicino (circa 50 s). Col re-ranking, sulle 24 query: stessi insiemi, ordine
      diverso in 18, mediana da 8,7 a 33 ms (vettore della query più la
      conversione dei vettori a ogni ricerca)
- [ ] Suddivisione dei documenti lunghi in parti: decisa, scritta e misurata
- [x] **Difetto 2** (25/09/2026, Koskidex `f5ce77f`): `Settings.HybridMode`
      (`union`, `vector`), `VectorTopK` 100, re-ranking di default. Il
      re-ranking vale +0,022 su SciFact, +0,024 su NFCorpus, +0,013 sulle
      known-item; l'unione non cambia niente su SciFact (il lessicale `any`
      trova già quasi tutto), su NFCorpus +0,031 di Recall@100 e zero query a
      vuoto. Costo 5-15 ms per query, lineare. 4 previsioni e mezza su 6
      (`risultati/esperimenti/2026-09-25_ibrido-unione/`)
- [x] **Difetto 2 sul recupero congiuntivo** (25/09/2026, Koskidex
      `f16b4c9`): con `all` l'unione vale +0,62 di nDCG@10 su SciFact e +0,14
      su NFCorpus, zero query a vuoto; il re-ranking non può niente. `all` più
      unione tiene le known-item a 0,9579 (contro 0,8464 di `any` più unione)
      perdendo 0,04 su SciFact. 5 previsioni su 5
      (`risultati/esperimenti/2026-09-25_ibrido-congiuntivo/`)
- [x] **Difetto 3** (25/09/2026, Koskidex `d3ffe17`): `FusionMode` (`rrf`,
      `convex`), `VectorWeight`, `FusionAlpha`. Calibrati su split separati:
      costante migliore 160 su SciFact e NFCorpus, 10 sulle known-item; α 0,5 e
      0,9. Sul test la somma calibrata fa 0,7067 e 0,3441 (da 0,6913 e 0,3340);
      RRF dimezza le known-item. Nessun parametro unico regge i due tipi di
      query. 3 previsioni e mezza su 7
      (`risultati/esperimenti/2026-09-25_fusione/`)
- [ ] **Il peso del vettore per tipo di query**: aggiungerlo alla scelta di
      `2026-09-25_scelta-per-query/` (oggi sceglie fra `any` e `all`, senza
      vettori) e rifarla con l'unione dentro: se `all` più unione regge anche
      sulle known-item umane, la scelta fra `any` e `all` potrebbe non servire
      più
- [x] **Scelta della configurazione per query** (25/09/2026): una regressione
      logistica sceglie fra BM25 `any` e `all` e arriva a 0,0006 dall'oracolo
      (0,6473 contro 0,6479 di media su known-item, SciFact e NFCorpus), mentre
      la regola della cifra perde 0,26 su SciFact. Ma l'oracolo coincide con la
      scelta per collezione, e una regola a due condizioni (cifra e `all` non
      vuoto) fa quanto il classificatore
      (`risultati/esperimenti/2026-09-25_scelta-per-query/`)
- [ ] **Rifare la scelta per query sulle known-item umane**, con lo stesso
      script: è lì che le cifre non bastano a riconoscere il tipo di query. Nel
      motore entra solo se il classificatore batte la regola

### 6. Confronto finale in Documentale

- [x] `fuzzySearchScored` nel contratto `SearchBackend` (25/09/2026,
      Documentale `5dd4460`): la stessa ricerca di `fuzzySearch`, con il
      punteggio del motore accanto a ogni id. `app:eval-run-queries
      --punteggi` lo registra nel rapporto; senza l'opzione il rapporto è
      quello di sempre. Provato dal vivo sulle 24 query: stessi id di
      `fuzzySearch` su Elasticsearch e su Koskidex
- [ ] Vettori nell'indicizzazione di Documentale, se la sezione 5 li porta
- [ ] Stesse query su Elasticsearch e su Koskidex nella configurazione migliore:
      qualità, latenza, memoria, dimensione dell'indice
- [ ] Scriverlo con onestà: dove un motore piccolo e senza dipendenze è
      competitivo e dove no

### 7. Relatore e calendario

- [ ] **Dicembre 2026**: riproporre la tesi a Bonnici e Dal Palù, a progetti
      consegnati. Domande da portare: cosa considerano un contributo sufficiente
      per una magistrale, che dimensione si aspettano, se va bene un corpus
      pubblico al posto dei dati aziendali, se l'impianto di valutazione va bene
      prima di iniziare ad annotare
- [ ] **Gennaio 2027**: guardare se fra le tracce ufficiali c'è qualcosa che
      assorbe o sostituisce la proposta, e chiudere sul relatore
- [ ] Obiettivo: parte tecnica chiusa prima della sessione invernale 2027,
      scrittura dopo, laurea a settembre 2027

## Opzionale, se avanza tempo

Serve alla tesi ma non è necessario. Si fa solo a capitolo 7 chiuso,
altrimenti va fra gli sviluppi futuri.

- [ ] **Reranker neurale, offline** (discusso il 25/09/2026). Un cross-encoder
      multilingue (per esempio `bge-reranker-v2-m3`) riordina i primi 100
      candidati dei ranking già archiviati, e `scripts/evaluate -rankings`
      rivaluta. Dà il tetto di quanto vale riordinare, dato il recall del
      primo passaggio, e contrasta il difetto 2: il re-ranking funziona se è
      progettato come stadio (pochi candidati, modello preciso). Circa un
      giorno, con un ambiente Python fuori da Koskidex. Sezione del confronto
      finale (capitolo 8). Niente dentro Koskidex o Documentale: servirebbe un
      servizio a parte e centinaia di millisecondi per ricerca. Sulle
      known-item per numero e comune non si aspetta guadagno

## Parcheggiato

Non serve alla tesi. Si riprende solo se Koskidex va in produzione.

- Documentazione del formato WAL/GOB e runbook di backup e ripristino
- Pacchetti client completi in `examples/` (Laravel, Node.js, Python)
- CSP in nginx (da provare con gli stili inline di Tailwind e Google Fonts)
- HSTS sul reverse proxy TLS
- Limiti di ingegneria: l'istantanea riscrive l'indice intero, tutto sta in
  memoria, niente aggiornamento parziale di un documento

## Materiale per la scrittura

Le scoperte che valgono un paragrafo, con il posto dove sono raccontate per
esteso. Quelle segnate con `5f9b080` stanno nei piani rimossi.

- Il difetto 0 trovato misurando e non leggendo il codice: 290 query su 300 a
  vuoto su SciFact (`eval/DIARIO.md`)
- Lo stesso recupero congiuntivo in Documentale (`operator => and`), arrivato per
  la stessa strada in due basi di codice indipendenti (appunti)
- La ricerca per numero d'atto rotta in produzione: `ordinanza 187` al 12° posto
  su 85 (`risultati/esperimenti/2026-09-23_numero-atto/`)
- La ricerca per numero e comune: due difetti distinti copiati da
  Elasticsearch, il campo unico e i refusi sui numeri, misurati nel quadrato
  due per due. Dal 2% al 92% (`risultati/esperimenti/2026-09-25_refusi-numeri/`)
- Un classificatore che quasi raggiunge l'oracolo, e una regola a due
  condizioni che fa lo stesso: quando il machine learning non serve, e perché
  (`risultati/esperimenti/2026-09-25_scelta-per-query/`)
- "BM25 perde sulla ricerca per numero": falso, perdeva il recupero
  disgiuntivo. A parità di recupero congiuntivo BM25 fa quanto l'euristico
  (`risultati/esperimenti/2026-09-25_known-item-divario/`)
- Le stopword che su SciFact "funzionavano" solo perché spegnevano la ricerca
  per prefisso sulle parole che la usavano peggio: una spiegazione plausibile
  smentita da un controfattuale (`risultati/esperimenti/2026-09-25_stopword-espansioni/`)
- La guardia su `recall@k` che scattava, e a essere sbagliata era la guardia
  (`eval/DIARIO.md`)
- Il corpus misto che fa dire a BM25 "il testo integrale peggiora il recupero",
  falso: è la normalizzazione della lunghezza (Task E2, `5f9b080`)
- `scripts/compare` che leggeva la chiave sbagliata e riduceva l'indice a un
  documento senza un errore (Task E2, `5f9b080`)
- Le quattro differenze di matching fra i due motori, le due ipotesi sui residui
  sbagliate, il difetto dei bigrammi e il tokenizer
  (`risultati/esperimenti/2026-09-23_cause-divergenza/`)
- Il `fsync` per documento trovato dalla prima misura dell'innesto: 31,8 secondi
  contro 1,9 (`risultati/esperimenti/2026-09-25_innesto-parita/`)
- Perché il testo integrale non si fa trascrivere da un LLM: una parafrasi con
  omissioni e invenzioni non è il documento (Task C0, `5f9b080`)
- Il collaudo della catena su 14 documenti inventati, i cui numeri non vanno in
  tesi (Task C2, `5f9b080`)
