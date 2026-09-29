# TODO - cosa manca alla tesi

L'unico elenco di cosa resta da fare, dal 25/09/2026. I vecchi file di lavoro
(`piano.md`, `indice.md`, `appunti.md`, `da-fare-a-mano.md`) sono stati tolti:
la loro ultima versione è nel commit `ab4af30`, e si rilegge con
`git show ab4af30:Magistrale/Tesi/piano.md`.

## Dove sta cosa

- `latex/` - la tesi. Capitoli 1-7 e 9 e le quattro appendici sono scritti per
  intero, da rileggere; il capitolo 8 è ancora vuoto e si regge sulle
  known-item umane (deciso il 28/09/2026).
- `risultati/` - l'archivio di ogni misura, con le sue regole nel README; un
  README per esperimento in `risultati/esperimenti/`.
- `istruzioni-annotazione.md` - il protocollo per chi raccoglie le query e per
  chi giudica. Resta perché lo leggono le persone e lo citano gli strumenti e
  l'appendice B.
- Koskidex, `eval/DIARIO.md` - ogni modifica al ranking, con le previsioni
  scritte prima.

## Da fare a mano (Martin)

In quest'ordine dove c'è un ordine. Importazioni, commit e misure li fa Claude:
basta mettere i file nelle cartelle indicate e dirlo.

- [ ] **Rileggere i capitoli** in `latex/` (il PDF è `latex/tesi.pdf`): il testo
      è in prima persona e a tuo nome, e va controllato che sia tuo.
- [ ] **Known-item umane: è su queste che si regge il capitolo 8.** Arrivati
      i lotti 1 e 2 (28/09); ne manca almeno uno, meglio due. Quattro persone che non sappiano come funzionano i
      motori (non informatici), **un lotto diverso a testa**: i file
      `risultati/query/known-item-umane/pagine/raccolta-lotto-1.html` ... `-4`,
      40 atti ciascuno. Bastano tre persone. Mandarli **in privato** (contengono
      il testo degli atti, con nomi di persone), farsi rimandare il `.json` che
      la pagina scarica alla fine, copiarlo così com'è in
      `risultati/query/known-item-umane/risposte/`. Martin non compila le
      pagine: le sue query misurerebbero lui. Istruzioni per chi raccoglie nella
      parte 1 di `istruzioni-annotazione.md`.
- [x] ~~I 24 bisogni, i giudizi del pool, il secondo annotatore~~: il 28/09
      i bisogni li ha scritti Claude e Martin li ha rivisti, i 905 giudizi li ha
      dati il modello, e Martin ha giudicato un campione di 178 righe (c03,
      c10, c19, c21). Kappa pesato 0,370: i giudizi del modello non bastano da
      soli, e il 28/09 Martin ha deciso di **non giudicare il resto del pool**:
      il capitolo 8 si regge sulle known-item umane.
- [ ] **Confermare la configurazione consigliata** (`KOSKIDEX_PROFILO=consigliata`
      in Documentale): nessun default cambia, il profilo accende le tre
      correzioni del capitolo 6. Da confermare con il relatore.
- [ ] **Dicembre 2026**: riproporre la tesi a Bonnici e Dal Palù, a progetti
      d'esame consegnati. Portare il PDF e le domande: cosa considerano un
      contributo sufficiente, che dimensione si aspettano, se va bene un corpus
      pubblico al posto dei dati aziendali, se l'impianto di valutazione va bene.
      Titolo, tre proposte:
      1. *Ritrovare un atto: difetti di recupero di un motore di ricerca
         leggero, misurati in un sistema documentale*
      2. *Dal motore alla produzione: valutazione e correzione del recupero di
         un motore di ricerca senza dipendenze in un documentale*
      3. *Koskidex in Documentale: cosa costa, in pertinenza, un motore di
         ricerca piccolo*
- [ ] **Gennaio 2027**: guardare le tracce ufficiali e chiudere sul relatore.
- [ ] **I ringraziamenti** (`latex/capitoli/ringraziamenti.tex`): solo tuoi.

## Da fare poi (Claude), quando arrivano le cose di Martin

**Il pool delle 24 query, dopo la decisione del 28/09:**

- [x] Giudizi del modello, campione di Martin, kappa: esito in
      `esperimenti/2026-09-28_giudice-llm/` (kappa pesato 0,370, sotto 0,40).
- [x] Scritto nella tesi il 28/09: 4.5 ("Com'è andata": bisogni e giudizi del
      modello, campione di Martin, kappa, regola), appendice B, limiti (9.2).
      Il pool con i giudizi del modello resta al più un confronto secondario,
      dichiarato come tale e con il kappa accanto, mai la base del capitolo 8.

**Quando arrivano i file delle known-item umane:**

- [ ] Le misure sono già pronte, con README e previsioni committati prima dei
      dati, e provate su risposte inventate. Prova generale il 28/09 sulle 76
      query dei primi due lotti, con l'archivio in una cartella temporanea:
      tutti e sei i passi girano, in circa due minuti. **Prima di partire
      accendere Ollama** (`ollama serve`, serve `bge-m3` per A, B, V e
      scheda-testo). A raccolta chiusa, in ordine:
      1. `strumenti/importa-raccolta.py` (collezione, giudizi per fonte,
         `raccolta.json`);
      2. `strumenti/collezioni-umane.py` (le tre collezioni in Koskidex);
      3. `esperimenti/2026-09-25_known-item-umane/esegui.sh`, poi il suo
         `analizza.py` sulle otto valutazioni: Koskidex ed Elasticsearch sulle
         query umane, per fonte. È la base del **capitolo 8**, con le
         previsioni già committate nel suo README: Elasticsearch di
         produzione e Koskidex nella configurazione consigliata; MRR@10, atto
         primo, atto entro i primi dieci, query a vuoto, per fonte e con o
         senza numero; latenza, memoria e indice da
         `2026-09-28_carico` e `2026-09-28_prestazioni`; dove un motore
         piccolo è competitivo e dove no, scritto con onestà;
      4. `esperimenti/2026-09-25_scelta-umane/analizza.py` su A, B e LT del
         punto 3: la scelta per tipo di query, nel motore entra solo se il
         classificatore batte la regola (sezione 7.5);
      5. `esperimenti/2026-09-25_italiano-umane/esegui.sh` e `analizza.py`:
         stopword e stemmer italiani (sezione 5.6);
      6. `esperimenti/2026-09-25_scheda-testo/esegui.sh` e `analizza.py`:
         scheda contro testo intero, `b` e contesto dei vettori sui soli 563
         atti di Crispiano (sezioni 5.7 e 7.1);
      7. `esperimenti/2026-09-28_reranker/esegui.sh umane` e
         `analizza.py umane`: previsioni 4 e 5 del riordino (sezione 8.2),
         qualche minuto a configurazione sulla GPU;
      8. `esperimenti/2026-09-28_date-app/esegui.sh` di nuovo, per il prezzo
         dell'anno da solo sulle query complete (vedi la voce di date-app);
      9. l'esito di ognuna nel suo README, previsione per previsione.
- [ ] La suddivisione dei documenti lunghi in parti, se la previsione 4 di
      `2026-09-25_scheda-testo` tiene (sezione 7.1).
- [ ] Completare la sezione 4.4 con i numeri della raccolta.
- [ ] Completare con i numeri del capitolo 8 la sezione 9.1 e i contributi
      del capitolo 1.
- [ ] Se le known-item umane promuovono BM25 o i vettori, misurarli dentro il
      profilo consigliato come un tutto, come in
      `2026-09-25_configurazione-consigliata/`.

**Alla fine:**

- [ ] Titolo e relatore in `latex/tesi.tex` (`\title` e `\advisor`, oggi
      "DA DEFINIRE"), quando sono decisi.
- [ ] Rileggere la tesi intera contro l'archivio: ogni numero con il suo file.
      Capitoli 1-7 e 9 riletti il 29/09 (vedi sotto): a capitolo 8 scritto
      restano il capitolo 8, le appendici e i numeri nuovi di 4.4, 9.1 e 1.

## Si può fare senza aspettare nessuno

- [x] Scritti nella tesi il 28/09 il carico e il prima e dopo delle
      prestazioni: sezione 8.3 (con il rimando da 3.5), 9.1, 9.2, 9.3 e le tre
      voci nuove del registro delle ipotesi (carico, prestazioni, giudice-llm).
- [x] L'ordine casuale dei termini trovati: `stable_term_order` (Koskidex
      `c514c77`), misurato in `2026-09-28_ordine-fisso` il 28/09, sei
      previsioni su sette; scritto in 5.3 (espansioni), 8.3, 9.3 e nel
      registro. Resta da decidere se accenderla nel profilo consigliato di
      Documentale: oggi non cambia niente (punteggio euristico), servirebbe
      solo passando a BM25.

- [x] Date e importi: `normalize_dates` e `normalize_amounts` (Koskidex
      `c059664`, costo ridotto in `cec3b63`), misurati il 28/09 in
      `2026-09-28_date-importi` su query sintetiche: sei previsioni su otto,
      più una su due per il costo. Scritto nella sezione 6.4 (quarto difetto),
      in 1, 9.1 e nel registro. Esposte in Documentale il 28/09 (`f921ef7`,
      `KOSKIDEX_NORMALIZE_DATES` e `KOSKIDEX_NORMALIZE_AMOUNTS`, spente e fuori
      dal profilo) e misurate dall'app in `2026-09-28_date-app`: sei previsioni
      su otto, scritto in 6.4 e 9.1. Le date vanno normalizzate, gli importi
      no. Restano: i decimali semplici (`3,5` contro `3.5`) non sono toccati;
      una passata scritta a mano al posto delle espressioni regolari se il
      costo contasse (dall'app è +6%).
- [x] Le espansioni come sinonimi (`bm25_expansion: synonym`, Koskidex
      `b958ea0`), misurate il 28/09 in `2026-09-28_espansioni-sinonimo`: sei
      previsioni su sei, nessuna regola di parità, SciFact 0,6667 (0,6734 con
      stopword). Scritto in 5.3 e nel registro; tolto dagli sviluppi futuri.
- [x] Le allocazioni che restavano (Koskidex `2e6beff`, i candidati con
      refuso filtrati prima di togliere i doppioni), misurate il 28/09 in
      `2026-09-28_allocazioni` contro un "prima" rifatto: nessun risultato
      cambia, allocazioni da 0,435 a 0,081 MB a ricerca, capacità nel
      container +44% (3.779 ricerche al secondo), nativa +56%; cinque
      previsioni su sette. Scritto in 8.3, 9.1 e nel registro. Resta, se
      servisse: `transform.Chain` (la catena che toglie gli accenti, ricreata
      a ogni testo) è ora la prima voce delle allocazioni, e la scansione del
      vocabolario per le parole corte con un refuso il 7% della CPU.
- [x] I rapporti dell'app sulle known-item umane (`confronto/*known-item-umane*`)
      contengono il testo delle query: esclusi da git il 28/09, prima che
      stasera ne nasca il primo. I tempi di indicizzazione restano tracciati.
- [ ] Dopo le known-item umane complete: rifare `2026-09-28_date-app/esegui.sh`
      (legge la collezione aggiornata) per il prezzo dell'anno da solo sulle
      query vere; se non costa, `normalize_dates` entra nel profilo
      consigliato insieme alla coppia degli importi (`normalize_amounts` e
      `KOSKIDEX_TYPOS_ON_AMOUNTS=false`, `2026-09-28_importi-esatti`), in
      Documentale e nella tesi (6.4 e 6.5), con la misura del profilo come
      un tutto.
- [x] Gli importi ammettono refusi (trovato in `2026-09-28_date-app`):
      `typo_tolerance.disable_on_amounts` (Koskidex `98701ad`) e
      `KOSKIDEX_TYPOS_ON_AMOUNTS` (Documentale `dad69da`), misurati dall'app
      il 28/09 in `2026-09-28_importi-esatti`: sette previsioni su otto, con
      la normalizzazione MRR@10 degli importi da 0,917 a 0,990; scritto in
      6.4, 9.1 e nel registro.
- [x] L'ultimo taglio di allocazioni in Koskidex, `transform.Chain`: fatto il
      29/09 in `2026-09-29_accenti` (Koskidex `df6f62b`), cinque previsioni su
      cinque, nessun risultato cambiato; allocazioni da 0,078 a 0,052 MB a
      ricerca, capacità nel rumore. Scritto in 8.x e nel registro. Quello che
      resta non si toglie senza cambiare interfacce o formato dell'indice.
- [x] I numeri che stavano solo fuori da `risultati/` (dalla rilettura del
      28/09): il 29/09 `strumenti/numeri-diario.py` li ricalcola dalle
      valutazioni archiviate (lunghezze delle query in 5.1, candidati e le 25
      query che non ne perdono in 5.4) e dal test di Koskidex (35.494 parole in
      5.6), e copia con commit e impronta la prova di AlboPOP (4.3, con nota a
      piè di pagina). Tornano tutti; in 5.1 «termini» è diventato «parole»,
      che è quello che si conta, e in 5.4 le «25 query senza stopword» sono
      quelle che non perdono candidati (le 29 di `stopword-espansioni` usano
      un'altra definizione).
- [x] Rilettura dei capitoli 1-7 e 9 contro l'archivio, il 29/09: circa mille
      numeri, quasi tutti ricalcolati dai JSON. Corretti nel testo i valori
      che non tornavano (fra gli altri 213 → 195 atti e "da 5" → "da 4" in
      6.2-6.3, 22 query vuote su 24 di una parola in 5.1, *of* in 137 query e
      non 173, l'esempio `141 Sacile` al posto di `2 Pradamano`, 0,85 → 0,51 sul
      test in 7.3, quattro arrotondamenti in 7), le frasi con il riferimento
      sbagliato (le 24 query in 6.3 e 6.5, gli importi senza punti in 6.4) e il
      racconto dei difetti (tre sospettati leggendo il codice, il congiuntivo
      trovato misurando: 1, 3, 6, 9). Tolti i tempi dei vettori della prima
      volta e gli 8,7 ms, che non hanno file. Dati un file ai numeri che non ne
      avevano: `numeri-diario.py` esteso (mediane, gradi dei qrels, schede
      distinte, voci del diario copiate), `max-expansions.py`, e rifatti con
      la provenienza gli esiti di numero-atto, innesto-parita, fusione e
      carico, tutti con gli stessi numeri (registro nel README
      dell'archivio).
- [ ] Facoltativa, **da fare al fisso di Martin** (RTX 3060 Ti, 8 GB): il
      costo del riordino di `2026-09-28_reranker` su una GPU da gaming, per
      8.4 ("su un Mac costa 12 s a query, su una scheda consumer circa 2").
      Solo tempi, non metriche: stessi primi stadi archiviati, stesso
      `strumenti/riordina.py` con `--dispositivo cuda`, in fp32 come sul Mac
      e poi in fp16; previsione scritta prima (stima: 4 s a query in fp32,
      1,5-2,5 in fp16 su SciFact). Serve l'ambiente Python con torch per
      CUDA, il modello (2,1 GB), i corpora e i file di `primo-stadio/`
      copiati. Se si fa, un controllo in più: gli ordini riordinati devono
      coincidere con quelli del Mac in fp32, e differire di poco in fp16.
- [ ] Facoltativa, **da fare al fisso di Martin** (Ryzen 5, RTX 3060 Ti):
      rifare `2026-09-28_carico` con tutti e due i motori, Koskidex
      (al commit di `2026-09-28_allocazioni` o successivo) ed Elasticsearch
      come l'app, per vedere se il rapporto misurato sul Mac regge su
      un'altra macchina (sul Mac: capacità 6,6 volte, p50 0,92 contro 6,32
      ms). Tutta CPU, la GPU non serve. Previsioni scritte prima, in un
      esperimento nuovo che rimanda a quello del Mac: tempi per query simili
      (dipendono dal singolo core), capacità nella zona del nativo del Mac
      (dipende dai core), rapporto fra i motori entro il 30% di quello del
      Mac. Da dichiarare il sistema operativo: su Linux Docker gira senza
      macchina virtuale, su Windows passa da WSL2, e sul Mac il nativo va il
      70% più veloce del container. Servono Docker, Go, gli indici o i dati
      (Koskidex copiato, Elasticsearch riempito dall'app) e le 400 query.
- [ ] Reranker neurale offline (`2026-09-28_reranker`, iniziato il 28/09 per
      non restare fermi fino al terzo lotto): cross-encoder
      `bge-reranker-v2-m3` sui primi 100 candidati, fuori da Koskidex e
      Documentale. **Parte BEIR fatta il 28/09**: SciFact 0,676 → 0,723,
      NFCorpus 0,306 → 0,331, known-item automatiche 0,833 → 0,953 (LT 0,960),
      5-12 s a query; previsioni 1, 2, 3, 6 confermate, nel registro e in 8.2.
      Manca la **parte umana** (previsioni 4 e 5), a raccolta chiusa:
      `esegui.sh umane` + `analizza.py umane`, poi i `\dacompletare` di
      "Quanto vale riordinare" in 8.2 e le due righe nel registro.

## Da allineare alla fine

Ogni dato nuovo o che non torna, segnato qui appena si vede, così a capitolo 8
scritto si allineano tesi, README e archivio in un colpo solo. Dal terzo
controllo indipendente del 29/09 (tesi e archivio, in sola lettura):

- [ ] `confronto.tex` tabella `tab:crescita`, riga 10.018: 3,5 e 6,3 MB su
      disco senza file (anche in `carico/README.md`). Archiviare la misura a
      10.018 documenti o togliere le due celle.
- [ ] `sistemi.tex` (query di produzione): i parametri sono cinque, manca
      `tie_breaker: 0.3` (tocca solo il punteggio, non gli insiemi).
- [ ] `confronto.tex` e `appendice-ipotesi.tex`, reranker: il primo stadio è
      "LA con le stopword inglesi" (0,6757 e 0,3062), non LA.
- [ ] `confronto.tex`, memoria sotto carico: a `ffa38ab` 355 MB contro 1.566;
      272 dopo le prime due correzioni, 179 dopo l'ultima.
- [ ] `appendice-ipotesi.tex` in cima: "ogni esperimento con previsioni".
- [ ] `confronto.tex`: "un quinto del tempo, più di sei volte" → "circa un
      settimo, circa sette volte" (numeri dopo `accenti`).
- [ ] README, negli Esito con nota datata: `cause-divergenza` (a `1902826`
      la terza esecuzione cambia anche un'altra testa, legata a
      `stable_term_order`); `elisioni-koskidex` 213 → 195 (213 con i 18 di
      *comunale*); `carico` e `prestazioni` 35.913 ricerche e 2,569 MB;
      `scelta-ibrida` +0,022; `costo-vettori` 23 ms e 8,36 (non 8,7);
      `accenti` p99 14,9; `prestazioni` 1.566; `elisioni-koskidex` 1,1-1,2 e
      6,1-6,3 ms; `recupero-intermedio` la riga `all` da `4ee872c`;
      `date-app` previsione 5 (3 query su 76 hanno una cifra).
- [ ] Dubbi da decidere: `produzione.tex` "275 su 300, da 4" (Koskidex
      innestato partiva da 5, dire contro cosa); `ibrido.tex` NFCorpus
      0,3261 e 0,3263; `contesto-ollama` previsione 1 forse a metà;
      `sistemi.tex:57` "non entra mai" (vero per le query non vuote); 53
      contro 79 oggetti con dati personali (criteri diversi, dirlo);
      `contesto-ollama` 1.409 caratteri senza titolo, 1.662 con;
      `lessicale.tex:221` "meno di 0,003" vale per l'MRR, il nDCG sale di
      0,0033; lotto 2 iniziato alle 18:22Z del 25/09, prima del commit delle
      previsioni (18:39Z), da dire in 4.4.

Dal terzo lotto (29/09):

- [ ] Known-item umane chiuse con tre lotti, 104 query (16 vuote, 4 con un
      numero, mediana 4 parole): aggiornare 4.4, 9.2 ("due lotti su
      quattro"), la voce di Martin qui sopra e il README dell'archivio.

## Regole

Valgono per tutto il lavoro che resta. Se ne salta una, i numeri diventano
contestabili e non c'è modo di rimediare dopo.

1. **Ogni modifica che cambia i risultati sta dietro un'impostazione**, con il
   comportamento di oggi come default. `TestBaselineRankingIsFrozen` passa a
   default senza toccare il test.
2. **Le previsioni prima della misura**: voce in `eval/DIARIO.md` o README
   dell'esperimento, committata prima di lanciare la valutazione.
3. **Ogni numero della tesi viene da un file di `risultati/`**, scritto dagli
   strumenti, mai sovrascritto, con commit e stato dell'albero. I controlli di
   sviluppo girano con `TESI_RISULTATI=` vuota.
4. **Rilevanza e prestazioni si misurano separate**: dati inventati vanno bene
   per latenza e memoria, mai per la rilevanza.
5. **Koskidex resta senza dipendenze** oltre `golang.org/x/text`.
6. **Documentale**: solo il branch `martin/tesi-magistrale`;
   `ElasticsearchService` resta com'è, è il riferimento di produzione;
   Elasticsearch solo in locale (`localhost:9201`).
7. **Il corpus non si committa**, e nemmeno le pagine di raccolta e di
   annotazione, né le risposte delle known-item umane e i file con il testo
   delle query: contengono, o possono contenere, nomi di persone. Nel
   repository vanno gli script, i file con gli id e i riassunti numerici.
8. **Un giudizio non si cambia dopo aver visto le metriche.**
