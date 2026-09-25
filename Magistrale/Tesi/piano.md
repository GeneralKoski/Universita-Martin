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
| Difetti 2 e 3 (ibrido e fusione) | aperti | qui sotto, sezione 5 |
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
- [ ] Lo strumento che estrae il campione di atti da mostrare (seme fissato,
      per fonte e per genere) e quello che calcola il kappa: da scrivere quando
      arrivano le persone, non prima
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
- [ ] **Known-item umane**, trenta o quaranta, da persone diverse: si mostra un
      atto e si chiede la ricerca che farebbero per ritrovarlo
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
- [ ] **Quanto del guadagno delle stopword (voce E1) veniva dalle espansioni**:
      una stopword corta è un prefisso larghissimo (`a`, `the` con `theory`).
      Contarlo sulle query di SciFact
- [ ] **Il divario che resta sulle known-item** (0,833 contro 0,975): una
      penalità per i match non esatti anche in BM25, o il prefisso solo oltre
      una lunghezza minima del termine. Ognuna con la sua voce nel diario prima
      di misurarla
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

Oggi Koskidex ha solo lo stemmer Porter inglese.

- [ ] Stopword e stemmer italiani dietro `Settings.Stemmer`, con voce di diario
      e ipotesi prima di misurare
- [ ] Decidere come trattare elisioni, date (`14.01.2026`) e decimali (`3,5`)
      fuori dalla modalità compatibile con Elasticsearch, e misurarlo

### 5. Difetti 2 e 3: l'ibrido e la fusione

Il difetto 2 è il vettoriale che non porta candidati propri (re-ranking, non
recupero ibrido); il difetto 3 è la fusione `sim * 20.0` contro un lessicale che
cresce con la lunghezza della query. Da tenere distinti dal difetto 0 anche in
tesi. Il piano di dettaglio del 15/09 (Fasi 2 e 3 di `piano-implementazione.md`)
è in `5f9b080`, ma va riscritto contro il codice di oggi: le righe di
`ranker.go` che citava sono cambiate.

- [ ] Decidere **prima** da dove vengono gli embedding: un modello locale è una
      dipendenza, un servizio esterno una chiamata in rete. La chiave OpenAI di
      `apps/python` non c'è più. Koskidex non li genera, li riceve in `_vector`
- [ ] Suddivisione dei documenti lunghi in parti: decisa, scritta e misurata
- [ ] `Settings.HybridMode`, vuoto = re-ranking di oggi; nel ramo ibrido il
      vettoriale aggiunge documenti ai candidati
- [ ] Test che fallisce oggi: un documento pertinente solo semanticamente deve
      comparire
- [ ] Costo della scansione di tutti i vettori (O(n)): misurato, non dato per
      buono
- [ ] Fusione: RRF contro pesatura normalizzata, calibrazione, e fusione che
      dipende dal tipo di query (identificativa o in lingua naturale)

### 6. Confronto finale in Documentale

- [ ] `fuzzySearchScored` nel contratto `SearchBackend`, per avere i punteggi di
      entrambi i motori
- [ ] Vettori nell'indicizzazione di Documentale, se la sezione 5 li porta
- [ ] Stesse query su Elasticsearch e su Koskidex nella configurazione migliore:
      qualità, latenza, memoria, dimensione dell'indice
- [ ] Scriverlo con onestà: dove un motore piccolo e senza dipendenze è
      competitivo e dove no

### 7. Relatore e calendario

- [ ] Scegliere il progetto di Laboratorio di IA guardando se può fare da
      dimostrazione per Bonnici
- [ ] **Dicembre 2026**: riproporre la tesi a Bonnici e Dal Palù, a progetti
      consegnati. Domande da portare: cosa considerano un contributo sufficiente
      per una magistrale, che dimensione si aspettano, se va bene un corpus
      pubblico al posto dei dati aziendali, se l'impianto di valutazione va bene
      prima di iniziare ad annotare
- [ ] **Gennaio 2027**: guardare se fra le tracce ufficiali c'è qualcosa che
      assorbe o sostituisce la proposta, e chiudere sul relatore
- [ ] Obiettivo: parte tecnica chiusa prima della sessione invernale 2027,
      scrittura dopo, laurea a settembre 2027

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
