# Tesi magistrale - appunti

Il diario delle scelte sulla tesi: quali idee sono state valutate, perché è
stata tenuta quella su Koskidex, e cosa è emerso strada facendo. Il lavoro che
resta da fare sta in [piano.md](piano.md).

## Criterio di scelta

Una tesi magistrale non ha bisogno di software che funziona, ha bisogno di:

1. una **domanda** precisa,
2. un **metodo** per rispondere,
3. una **valutazione misurabile** del risultato.

Un progetto grande e ben fatto ma senza domanda resta una tesi progettuale.
Ogni candidato qui sotto è giudicato con questo metro.

## Contesto voto

Dal `CLAUDE.md` del repo: partenza ~102,66 + 3 (in corso) = 105,66. Servono
**4 punti tesi per il 110**, 7 per la lode. Quindi la tesi pesa, e una tesi con
misure e un contributo difendibile vale più di una tesi applicativa.

## Candidati valutati (15 settembre 2026)

Passati in rassegna tutti i repo personali sull'account GitHub `GeneralKoski`.

### Traccia scelta: Koskidex

Motore di ricerca full-text self-hosted scritto in Go (2.850 righe di codice
più 2.060 di test), binario
singolo senza dipendenze a runtime. Ha già tolleranza ai refusi, faccette e
ricerca vettoriale.

L'ingegneria c'è. Manca tutta la parte che lo rende una tesi:

- valutazione IR su dataset standard (BEIR, MS MARCO)
- curve **recall@k contro latenza**, non solo "è veloce"
- confronto con Meilisearch / Tantivy / Elasticsearch
- studio della **fusione lessicale + densa**: RRF contro pesatura, dove il
  vettoriale aiuta davvero e dove peggiora i risultati

Quest'ultimo punto è il candidato più forte a diventare *la* domanda di tesi.

### Parcheggiato: gpu-quant-bench

Benchmark di formati e quantizzazioni di un modello 7B su una RTX 3060 (12 GB):
FP16, GGUF Q8_0/Q5_K_M/Q4_K_M, GPTQ 4-bit, AWQ 4-bit, su contesti da 512, 2048
e 8192 token.

È l'unico repo nato già in forma di studio sperimentale, con domanda, variabili
controllate e metriche definite (throughput, TTFT, prefill, VRAM di picco,
perplexity). Il contributo metodologico interessante è riportare **varianza** e
**throttling termico**, che i benchmark pubblicati quasi sempre omettono.

**Non è la tesi.** È lo step 1 di un percorso di studio ML più lungo, descritto
nel repo `ml-notes`. Se in futuro dovesse servire come base di tesi, le
direzioni per irrobustirlo sono: più modelli, una seconda GPU per generalizzare,
valutazione di qualità oltre la perplexity (task downstream, non solo control
prompt letti a mano) e analisi energetica (J/token), che oggi manca ed è
l'angolo più facile da difendere.

### Scartati

| Progetto | Motivo |
|---|---|
| sudoku-instance-generation / Constraint_Programming | Esame del primo anno, già valutato. Fuori discussione. |
| MelaGolfo | Scartato. |
| KalTrack, unidesk, unidesk-mobile, Hydran, PiacenzAdvisor, PizzaGigante, Klipski, Chesso, Automarket, metin, Personal-website | Scartati: product engineering, integrazione o esercizi, nessuna domanda di ricerca. |

## Decisione presa (15 settembre 2026), confermata il 23 settembre

**Tesi su Koskidex innestato in Documentale.** Il piano operativo sta in
[piano.md](piano.md).

La domanda non è "integro il mio motore nel gestionale", che sarebbe lavoro di
integrazione senza contributo. È che il recupero di Koskidex ha quattro difetti
precisi, verificati leggendo il codice e poi **misurati** (23/09/2026):

0. **Il recupero è congiuntivo.** `ParseQuery` in `ranker.go:33` mette ogni
   parola in `MustTerms`: un documento deve contenere **tutti** i termini della
   query. Lucene è disgiuntivo con punteggio, e un documento che ne prende 8 su
   12 si piazza bene. Misurato sulla collezione pubblica SciFact: **290 query su
   300 tornano completamente vuote**, nDCG@10 a 0,0246 contro un riferimento
   BM25 di 0,6789. Non è un bug: l'AND è ragionevole per la barra di ricerca di
   un e-commerce, per cui Koskidex era nato. Ma è il difetto che **viene prima
   degli altri tre**, perché su query vuote nessun miglioramento del punteggio
   può fare niente, ed è il più rilevante per un documentale, dove le query sono
   in lingua naturale e sempre più spesso riscritte da un LLM. Dettagli e prove
   in `Koskidex/eval/DIARIO.md`. **Corretto il 23/09/2026** dietro
   `Settings.RetrievalMode`: SciFact da 0,0246 a 0,4936.
1. **Nessun IDF.** Il punteggio era `(10 - refusi + 2*esatti) * peso_campo`. Il
   campo `Posting.TF` esisteva in `internal/engine/inverted.go:12` con scritto
   `// term frequency (calculated later)` e non era usato da nessuna parte. Un
   termine rarissimo e uno comunissimo pesavano identico. **Corretto il
   23/09/2026** dietro `Settings.ScoringMode`: BM25 con `k1=1,2` e `b=0,75`,
   SciFact a **0,6197** e NFCorpus a **0,2810**, cioè il 91% e l'87% dei
   riferimenti pubblicati.
2. **L'ibrido non è ibrido.** In `ranker.go:203-222` il punteggio vettoriale si
   somma solo ai documenti già trovati dal lessicale: è re-ranking. Un documento
   semanticamente pertinente che il lessicale non pesca non entra mai.
3. **La fusione somma scale incomparabili.** `m.Score += sim * 20.0`, dove il
   lessicale cresce senza limite con la lunghezza della query e il vettoriale è
   fisso a 20. Su una parola il vettore domina, su cinque è rumore.

Ognuno è un capitolo con un risultato numerico, e il baseline è il codice del
23 settembre 2026, congelato in un test e misurato: SciFact 0,0246 e NFCorpus
0,1659 di nDCG@10. Documentale fornisce il corpus e il carico di query reale.

**Stato al 23/09/2026: i difetti 0 e 1 sono chiusi e misurati**, entrambi dietro
un campo di `Settings` con il comportamento vecchio come default, entrambi con
l'ipotesi committata nel diario prima della misura. Restano il 2 e il 3, che
hanno bisogno di embedding e di giudizi di rilevanza (sezioni 2 e 5 del piano).
Il percorso completo del lessicale, da 0,0246 a 0,6197 su SciFact, è già un
capitolo con dentro tre numeri e due sorprese.

**Il difetto 0 è stato trovato misurando, non leggendo il codice**, ed è la
dimostrazione che costruire l'impianto di valutazione prima di toccare il
ranking era la scelta giusta: la tesi stava per essere scritta su tre capitoli
di ottimizzazione del punteggio, su un motore che nel 97% dei casi non
restituiva niente da ottimizzare.

**Il 23/09/2026, guardando Documentale per tutt'altro motivo, il difetto 0 è
saltato fuori una seconda volta.** `ElasticsearchService::fuzzySearch()` ha
`'operator' => 'and'` con accanto il commento *"tutte le parole devono
comparire"*: il motore di produzione è congiuntivo esattamente come lo era
Koskidex. Non è più un difetto del mio progetto personale, è un difetto condiviso
con il sistema che i colleghi usano tutti i giorni, arrivato per la stessa strada
ragionevole in due basi di codice indipendenti. La tesi ne guadagna: la domanda
non è "il mio motore era tarato male", è "il recupero congiuntivo è una scelta
sensata che si rompe quando le query si allungano". Ed è misurabile sul sistema
vero, perché il log delle query di ricerca è stato acceso lo stesso giorno e
registra il numero di risultati: appena avrà raccolto abbastanza, si conta quante
ricerche reali tornano vuote e con quante parole. **Da non correggere prima di
averlo misurato:** è il baseline di produzione.

**E la sera del 23/09/2026 i due motori sono stati messi uno accanto all'altro
sullo stesso archivio.** Quattordici documenti con la forma vera dei dati di
Documentale, indicizzati in Elasticsearch dal codice dell'app e in Koskidex dal
corpus esportato, stesse query, impostazioni allineate alla produzione. Due
risultati:

- **Falliscono sulle stesse identiche query.** Tre su sette, tutte in lingua
  naturale, entrambe le volte zero risultati. Compresa una ricerca sulla
  sicurezza del cantiere di Piacenza a cui corrisponde in archivio un verbale di
  sopralluogo sulla sicurezza del cantiere di Piacenza.
- **Koskidex recupera lo stesso insieme di Elasticsearch su tutte le query che
  Elasticsearch risponde.** È il punto che regge tutto il resto: senza, ogni
  miglioramento misurato su Koskidex si liquida con "stai migliorando il tuo, non
  il nostro". Con, il passaggio da tre query a vuoto a zero è un risultato che
  parla anche di Documentale.

  **Corretto la sera stessa.** Sul corpus vero di 10.018 atti gli insiemi
  coincidono solo su 8 query su 24. Il modello di recupero è lo stesso, ma il
  matching differisce in quattro punti, misurati uno per uno: tutte le parole
  nello stesso campo (Elasticsearch) o sparse sul documento (Koskidex), soglie
  dei refusi diverse, ricerca per prefisso che solo Koskidex fa, prima lettera
  esatta che solo Elasticsearch richiede. Corrette in via sperimentale, le
  query identiche salgono a 15. Su 14 documenti le differenze non avevano
  occasione di vedersi. L'argomento "i miglioramenti valgono anche per
  Documentale" va quindi ricostruito: o Koskidex impara a riprodurre il
  matching di Elasticsearch, o si misura Elasticsearch direttamente, che ora
  gira in locale sullo stesso corpus. **Ricostruito il 25/09/2026** per la
  prima strada: vedi *Koskidex pronto per l'innesto*, qui sotto.

  E il confronto ha trovato una cosa grossa: **in produzione la ricerca per
  numero d'atto è rotta.** `ordinanza 187` mette l'atto giusto al 12° posto su
  85, perché per Elasticsearch `187` ammette un refuso e combacia con `18` e
  `17`. Spenti i refusi, è primo e unico. Dettagli in
  `risultati/esperimenti/2026-09-23_numero-atto/`.

Con `or + BM25` tutte e sette le query rispondono, e il documento giusto è primo
in tutte e sette.

Lo stesso impianto, poche ore dopo, ha fatto scattare una guardia sulla misura di
BM25. Andando a vedere è venuto fuori che a essere sbagliata era la guardia, non
il risultato: `recall@k` non misura il recupero quando i candidati sono molti più
di `k`. Anche questo va in tesi. Un controllo che scatta e costringe a capire
perché vale più di una tabella senza incidenti, e la versione corretta della
guardia è ora un numero registrato in ogni file di risultati.

Tre cose in una tesi sola: progetto personale (Koskidex), progetto aziendale
(Documentale), e il contributo di Martin documentato dai commit.

**Fuori dal perimetro:** `rustann` e gli indici approssimati. La forza bruta
regge il volume di un documentale aziendale, quindi sarebbe una domanda di
ricerca senza un bisogno reale.

**Il vincolo che decide tutto:** non esistono dati di produzione, solo uno
staging. Quindi i giudizi di rilevanza si scrivono a mano *prima* di guardare
cosa risponde il motore. Seedare va bene per misurare latenza e memoria, mai
per misurare la rilevanza: sarebbe circolare.

## Il corpus: l'azienda esce di scena (23/09/2026)

**Dieffetech ha abbandonato Documentale.** Cambia una cosa sola, ma grossa: i
documenti. Non c'è più un archivio di clienti da cui prendere il corpus, né
qualcuno a cui chiedere il permesso di conservare il testo integrale.

Il caso applicativo **resta Documentale**. Il software gira in locale, il
comando di export funziona, il log delle query c'è, il confronto con
Elasticsearch è già stato fatto e dice che Koskidex restituisce lo stesso
insieme di risultati. Quello che si sostituisce è il contenuto, non il sistema.

**Il corpus diventa pubblico: albi pretori comunali.** Determine, delibere,
ordinanze, avvisi, liquidazioni - documenti amministrativi italiani della stessa
famiglia di quelli che un documentale aziendale custodisce, pubblicati per
obbligo di legge e riusabili. Due fonti, verificate scaricandole il 23/09/2026:

- **Comune di Crispiano (TA)**, feed RSS, CC BY 4.0: 563 atti da novembre 2025 a
  settembre 2026, 551 col link diretto al PDF, testo nativo estraibile con
  `pdftotext` (2-6 pagine, 5-13 mila caratteri). È il corpus **col testo intero**.
- **Regione Friuli Venezia Giulia**, API Socrata, IODL 2.0: 9.457 atti dal 2011 a
  oggi, 171 enti, 46 tipologie, con `ente`, `tipologia_atto`,
  `ufficio_competente` e `oggetto`. È il corpus **a soli metadati**, e i suoi
  campi sono un `meta_true` già scritto da chi ha pubblicato il dato.

Averle tutte e due trasforma la domanda che era rimasta aperta - *il corpus è
fatto di schede o di documenti?* - da decisione al buio in **esperimento
misurabile**: stesso archivio, stesse query, cambia solo cosa è indicizzato.

Tre conseguenze buone e una scomoda.

- I risultati diventano **riproducibili da un lettore**: le fonti le riscarica chiunque.
- Cade la dipendenza dalle credenziali OpenAI (`gpt-4.1` in `apps/python`, chiave
  che non ho più): il testo lo produce `pdftotext`, e i campi da indovinare nel
  FVG ci sono già.
- Il problema delle query resta, anzi si aggrava: **nessun log si riempirà mai**.
  Vanno fabbricate, e in tesi va scritto con questa parola. La strada è la
  valutazione known-item - si mostra un atto a una persona e le si chiede la
  ricerca che farebbe per ritrovarlo, così il giudizio di rilevanza arriva gratis.
- Gli atti contengono **nomi di persone** (67 su 9.457 oggetti del FVG hanno
  marcatori espliciti, e a Crispiano ci sono le pubblicazioni di matrimonio).
  Sono pubblici per legge, ma il corpus **non si committa**: nel repo vanno gli
  script che lo riscaricano, e in tesi gli esempi si citano anonimizzati.

Il dettaglio, con fonti, licenze e numeri, sta in Koskidex
`eval/corpora/c3-albo/SOURCE.md`.

## Koskidex pronto per l'innesto (25/09/2026)

La regola era: si innesta solo un Koskidex completo. I sette buchi trovati
provandolo contro il contratto di Documentale (Parte F del piano) sono chiusi,
ognuno con test scritti prima e visti fallire. Il più importante per la tesi è
F7: **con le impostazioni di compatibilità, Koskidex restituisce esattamente gli
insiemi di Elasticsearch su tutte e 24 le query del confronto.** Ora l'argomento
"i miglioramenti valgono anche per Documentale" regge: si parte dagli stessi
insiemi, e ogni differenza misurata dopo viene dalla modifica.

Due scoperte fatte per strada, tutte e due materiale di tesi:

- **un difetto di Koskidex**: i refusi che non condividono bigrammi con la
  parola cercata (`atre` contro `arte`) non venivano mai valutati. Corretto;
- **un difetto di Documentale in produzione**: il tokenizer standard di
  Elasticsearch tiene insieme *dell'illuminazione*, quindi chi cerca
  "illuminazione" non trova gli atti con l'elisione. In un corpus italiano non è
  un caso raro. Da contare sul corpus intero.

**L'innesto è fatto lo stesso giorno** (Documentale `67cf954` e `2a03310`):
`KoskidexService` accanto a `ElasticsearchService`, dietro lo stesso contratto
`SearchBackend`, scelto da `SEARCH_BACKEND`. Dal vivo, passando dall'app sui
10.018 atti: 24 insiemi su 24 identici a Elasticsearch, ricerca a 2,7 ms di
mediana contro 22, indicizzazione 1,9 secondi contro 1,7. La prima misura ha
trovato un altro difetto di Koskidex: un `fsync` per documento, 31,8 secondi di
indicizzazione, corretto. Dettagli in
`risultati/esperimenti/2026-09-25_innesto-parita/`.

## Termine di paragone: le tesi dei colleghi (24/09/2026)

Il 24 settembre 2026 ho visto le tesi esposte dai colleghi. In confronto,
quello che sto facendo è su un altro piano. Per dare la misura: una tesi
considerata **molto buona** era *"parlo con il chatbot, fa la query al database
e mi estrae l'oggetto che sto cercando"*.

Cosa ne segue, per come lavoro da qui a settembre 2027:

- **il livello c'è già.** Il materiale per una buona tesi esiste (motore,
  confronto con Elasticsearch, difetti misurati in produzione);
- **i tempi non preoccupano.** Il lavoro è in anticipo sul calendario: la
  previsione è di chiudere la parte tecnica prima della sessione invernale
  2027, invece che fra febbraio e luglio come previsto all'inizio;
- **all'esposizione conta farsi capire.** Una commissione abituata a tesi come
  quella del chatbot va portata per mano: prima il problema (chi cerca
  "illuminazione" non trova "dell'illuminazione"), poi i numeri.

## Relatore: stato e tempi

Il 21 settembre 2026 ho agganciato entrambi i potenziali relatori a fine
lezione: **Dal Palù**
(Programmazione Dichiarativa) e **Bonnici** (Algoritmi per l'IA e Laboratorio
di IA). Nessuno dei due discorsi ha chiuso l'argomento, ed era previsto così:
l'obiettivo di quel giorno era aprire un canale, non ottenere un sì.

**La riproposta vera va a dicembre 2026**, per due motivi che si incastrano:

1. **A dicembre ho i progetti dei loro esami.** Laboratorio di IA si esamina con
   un progetto da presentare, Programmazione Dichiarativa con un progetto più
   orale. Arrivare con un lavoro consegnato e valutato da loro vale molto più di
   un discorso in corridoio: è la differenza fra dire "so fare questa cosa" e
   averla già fatta sotto il loro giudizio.
2. **Le tracce di tesi escono verso gennaio.** Presentarsi a dicembre significa
   essere già nella loro testa quando decidono a chi assegnare cosa, invece di
   arrivare quando la lista è già distribuita.

**La leva da non sprecare:** il progetto di Laboratorio di IA deve applicare i
concetti del laboratorio più qualcosa dalla teoria di Algoritmi. Se lo si sceglie
su un terreno vicino al recupero dell'informazione e alla valutazione del
ranking, diventa allo stesso tempo l'esame e la dimostrazione da portare a
Bonnici. Un progetto solo, due scopi. Da valutare quando Bonnici assegna i temi,
senza forzare: se il tema è lontano, si fa il progetto e basta.

**Da chiedere a ricevimento**, a chiunque dei due apra: cosa considera un
contributo sufficiente per una magistrale, che dimensione si aspetta, se va bene
un corpus pubblico al posto dei dati aziendali, e se l'impianto di valutazione
gli va bene prima che inizi ad annotare.

I tempi: sette esami da chiudere fra gennaio e l'estate 2027, ma la parte
tecnica è in anticipo e la previsione è di chiuderla prima della sessione
invernale 2027. Dopo resta la scrittura, per la laurea a settembre 2027.

## Prossimi passi

Stanno in [piano.md](piano.md), con le regole che rendono sicuro toccare il
ranking. La decisione del 23/09/2026 era di **fare le correzioni al ranking
prima della tesi**, a tre condizioni: baseline congelato in un test, ogni
modifica dietro un campo di `Settings` con default sul comportamento attuale, e
ogni modifica annotata in `eval/DIARIO.md` con l'ipotesi scritta *prima* di
misurare. Ha funzionato: i difetti 0 e 1 e l'innesto sono chiusi a settembre
2026, e la misurazione e la scrittura, che sono le parti che non si comprimono,
hanno il tempo che serve.

## Nota organizzativa

La tesi sta **tutta qui dentro**, in `Magistrale/Tesi/`: appunti ora, e più
avanti anche il codice e la scrittura. Niente repo separata e niente repo
annidata (git non gestisce le repo dentro le repo). `Universita-Martin` è il
percorso universitario nella sua interezza, e la tesi ne fa parte.
