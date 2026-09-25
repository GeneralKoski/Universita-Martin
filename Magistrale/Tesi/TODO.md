# TODO - cosa manca alla tesi

L'unico elenco di cosa resta da fare, dal 25/09/2026. I vecchi file di lavoro
(`piano.md`, `indice.md`, `appunti.md`, `da-fare-a-mano.md`) sono stati tolti:
la loro ultima versione è nel commit `ab4af30`, e si rilegge con
`git show ab4af30:Magistrale/Tesi/piano.md`.

## Dove sta cosa

- `latex/` - la tesi. Capitoli 1-7 e 9 e le quattro appendici sono scritti per
  intero, da rileggere; il capitolo 8 è ancora vuoto.
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
- [ ] **Known-item umane.** Quattro persone che non sappiano come funzionano i
      motori (non informatici), **un lotto diverso a testa**: i file
      `risultati/query/known-item-umane/pagine/raccolta-lotto-1.html` ... `-4`,
      40 atti ciascuno. Bastano tre persone. Mandarli **in privato** (contengono
      il testo degli atti, con nomi di persone), farsi rimandare il `.json` che
      la pagina scarica alla fine, copiarlo così com'è in
      `risultati/query/known-item-umane/risposte/`. Martin non compila le
      pagine: le sue query misurerebbero lui. Istruzioni per chi raccoglie nella
      parte 1 di `istruzioni-annotazione.md`.
- [ ] **I 24 bisogni**, prima dei giudizi: in
      `risultati/query/confronto-24/bisogni.md`, una o due frasi dopo ogni
      `Bisogno:` (cosa cerca chi digita quella query nel documentale di un
      comune, e se serve cosa no), **senza guardare risultati**. Per i refusi,
      com'è scritto nel file (`come «manutenzione strade»`); per le query con un
      numero, cosa conta come quell'atto. Circa un'ora. Poi dirlo a Claude.
- [ ] **I giudizi del pool**, dopo che Claude ha generato la pagina: aprire
      `risultati/query/confronto-24/pagine/giudizi-primo.html` nel browser e
      dare i 905 giudizi. Tasti 0 (non risponde), 1 (parziale), 2 (risponde), T
      per il testo intero, freccia a sinistra per tornare indietro. Sessioni di
      un'ora al massimo, con Pausa quando si smette; 4-5 ore in tutto. Alla fine
      "Scarica il file", metterlo in `risultati/query/confronto-24/risposte/`.
- [ ] **Il secondo annotatore** (Leopoldo o un'altra persona fidata), dopo i
      giudizi: Claude prepara `giudizi-secondo.html` con query intere estratte a
      caso, almeno 150 righe; la persona non vede i giudizi del primo (parte 3
      delle istruzioni). Il suo file va nella stessa cartella `risposte/`.
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

**Quando i 24 bisogni sono scritti:**

- [ ] Committare `bisogni.md`, poi `risultati/strumenti/prepara-giudizi.py` per
      la pagina del primo annotatore.

**Quando arriva il file dei giudizi:**

- [ ] `importa-giudizi.py`: giudizi, sessioni e `qrels/test.tsv`.
- [ ] `prepara-giudizi.py --secondo` per la pagina del secondo annotatore.
- [ ] **Capitolo 8**, con le previsioni scritte prima come sempre: le stesse
      query su Elasticsearch di produzione e su Koskidex nella configurazione
      consigliata e nelle configurazioni del pool; nDCG@10 e Recall@100 per
      famiglia di query; latenza, memoria e dimensione dell'indice; dove un
      motore piccolo è competitivo e dove no, scritto con onestà.
- [ ] Completare con i numeri del capitolo 8: la sezione 9.1, i contributi del
      capitolo 1, la sezione 4.5 (tempo per giudizio, distribuzione dei gradi).
- [ ] Se i giudizi promuovono BM25 o i vettori, misurarli dentro il profilo
      consigliato come un tutto, come in `2026-09-25_configurazione-consigliata/`.

**Quando arriva il file del secondo annotatore:**

- [ ] `importa-giudizi.py`, poi `risultati/strumenti/kappa.py`; kappa e
      disaccordi nella sezione 4.5 e nei limiti (9.2), di quanto cambiano le
      metriche con i giudizi del secondo.

**Quando arrivano i file delle known-item umane:**

- [ ] Le misure sono già pronte, con README e previsioni committati prima dei
      dati, e provate su risposte inventate. A raccolta chiusa, in ordine:
      1. `strumenti/importa-raccolta.py` (collezione, giudizi per fonte,
         `raccolta.json`);
      2. `strumenti/collezioni-umane.py` (le tre collezioni in Koskidex);
      3. `esperimenti/2026-09-25_known-item-umane/esegui.sh`, poi il suo
         `analizza.py` sulle otto valutazioni: Koskidex ed Elasticsearch sulle
         query umane, per fonte (capitolo 8);
      4. `esperimenti/2026-09-25_scelta-umane/analizza.py` su A, B e LT del
         punto 3: la scelta per tipo di query, nel motore entra solo se il
         classificatore batte la regola (sezione 7.5);
      5. `esperimenti/2026-09-25_italiano-umane/esegui.sh` e `analizza.py`:
         stopword e stemmer italiani (sezione 5.6);
      6. `esperimenti/2026-09-25_scheda-testo/esegui.sh` e `analizza.py`:
         scheda contro testo intero, `b` e contesto dei vettori sui soli 563
         atti di Crispiano (sezioni 5.7 e 7.1);
      7. l'esito di ognuna nel suo README, previsione per previsione.
- [ ] La suddivisione dei documenti lunghi in parti, se la previsione 4 di
      `2026-09-25_scheda-testo` tiene (sezione 7.1).
- [ ] Completare la sezione 4.4 con i numeri della raccolta.

**Alla fine:**

- [ ] Titolo e relatore in `latex/tesi.tex` (`\title` e `\advisor`, oggi
      "DA DEFINIRE"), quando sono decisi.
- [ ] Rileggere la tesi intera contro l'archivio: ogni numero con il suo file.

## Si può fare senza aspettare nessuno

- [ ] Decidere come trattare date (`14.01.2026`) e decimali (`3,5`) fuori dalla
      modalità compatibile con Elasticsearch, e misurarlo.
- [ ] Opzionale: un reranker neurale offline (cross-encoder multilingue sui
      primi 100 candidati dei ranking archiviati, rivalutati con
      `scripts/evaluate -rankings`), fuori da Koskidex e Documentale. Dà il
      tetto di quanto vale riordinare; andrebbe nel capitolo 8. Se non si fa,
      resta fra gli sviluppi futuri (9.3), dove è già scritto.

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
   annotazione: contengono nomi di persone. Nel repository vanno gli script e i
   file con gli id.
8. **Un giudizio non si cambia dopo aver visto le metriche.**
