# Istruzioni di annotazione

Scritte il 25/09/2026, prima di darle a chiunque e prima di aver annotato una
riga. Chi annota le legge per intero una volta, e le rilegge a ogni sessione.
Se durante il lavoro una regola si rivela sbagliata o manca un caso, non si
corregge a voce: si cambia questo file, con un commit che dice cosa cambia e da
quale riga dell'annotazione vale, e nel file dei giudizi si annota da dove
vale la nuova regola.

Due lavori diversi, fatti da persone diverse:

1. **raccogliere le query known-item**: si mostra un atto a una persona e le si
   chiede la ricerca che farebbe per ritrovarlo (parte 1);
2. **giudicare il pool**: per ogni query con un bisogno informativo aperto, dire
   quali atti fra quelli trovati dai motori rispondono e quanto (parte 2).

Il secondo annotatore e il kappa sono nella parte 3.

## Parte 1 - Raccogliere le query known-item

**A cosa serve.** Le 300 query automatiche `<numero> <comune>` misurano solo la
ricerca per identificativo. Le query scritte da persone misurano come si cerca
davvero un atto di cui si ricorda il contenuto e non il numero. Il giudizio di
rilevanza arriva gratis: l'atto mostrato è l'unico pertinente, con grado 2.

**Chi le scrive.** Almeno tre persone diverse, nessuna che conosca i motori o
abbia visto i risultati di una ricerca sul corpus. Martin non scrive query: sa
quali parole trovano cosa, e le sue query misurerebbero lui, non i motori.

**Quali atti.** Un campione estratto a caso con un seme fissato e scritto nel
file che lo produce, diviso per fonte (Crispiano col testo intero, Friuli
Venezia Giulia coi soli metadati) e per genere (determina, delibera, ordinanza,
avviso, altro), in proporzione al corpus. Nessuno sceglie gli atti a mano:
sceglierli vuol dire sceglierli facili o difficili.

**Come si fa, per ogni atto.**

1. Si mostra l'atto come lo vedrebbe un impiegato: il titolo e il testo (per
   Crispiano) o la scheda (per il Friuli Venezia Giulia). Senza id, senza
   punteggi, senza dire con che motore verrà cercato.
2. La persona lo legge per il tempo che le serve, poi **l'atto si nasconde**.
3. Le si chiede: *"Fra qualche settimana ti serve di nuovo questo atto. Cosa
   scriveresti nella barra di ricerca per ritrovarlo?"* e si scrive la query
   esattamente come la dice, refusi compresi.
4. Si registra anche se ha usato un numero (di atto, di protocollo, un
   importo): le query con un numero si analizzano a parte, perché su quelle i
   motori si comportano in modo diverso.

L'atto si nasconde prima di scrivere perché altrimenti la query copia il titolo,
e una query copiata dal titolo la trova qualunque motore. Chi cerca un atto a
distanza di settimane ne ricorda l'argomento, qualche parola, raramente il
numero.

**Cosa non si fa.** Non si suggerisce niente, non si chiede di riformulare, non
si prova la query su un motore davanti alla persona, non si scarta una query
perché sembra brutta. Una persona che dice "non saprei cosa scrivere" è un dato:
si registra la query vuota con il motivo.

**Cosa si registra**, una riga per query: id dell'atto, testo della query,
pseudonimo della persona (mai il nome), data, secondi di lettura, se contiene
un numero, note. Il file finisce in `risultati/query/` con la sua provenienza,
come le known-item automatiche.

## Parte 2 - Giudicare il pool

**A cosa serve.** Per una query con un bisogno aperto (`manutenzione strade`,
`concorso`) non esiste un solo atto giusto. I motori trovano ciascuno i suoi
primi dieci; il pool è l'unione, e la persona dice quali rispondono al
bisogno. Da questi giudizi vengono nDCG@10 e Recall@100.

### Prima di aprire il foglio: il bisogno, per scritto

Per ogni query, **prima di vedere un solo risultato**, si scrive in una o due
frasi cosa sta cercando chi la digita in un documentale di un comune. Per
esempio, per `manutenzione strade`: *"atti che dispongono, affidano, pagano o
regolano lavori di manutenzione su strade comunali: sono pertinenti gli
affidamenti, le liquidazioni e le ordinanze di viabilità dovute ai lavori; non
lo sono gli atti che nominano una strada solo come indirizzo."*

Le descrizioni si committano prima di aprire il foglio. È l'unica difesa contro
il giudizio che si adatta ai risultati: senza, il bisogno diventa "quello che i
motori hanno trovato".

### Il foglio

`scripts/pool` produce `giudizi.tsv` con le colonne `query_id`, `query`,
`doc_id`, `titolo`, `estratto`, `grado`. Si compila solo `grado`.

- **Le righe sono ordinate per id del documento**, non per posizione. Non si
  riordinano: chi annota in ordine di ranking finisce per confermarlo.
- Il foglio non dice quale motore ha trovato quale documento, e non si va a
  cercarlo.
- Se titolo ed estratto non bastano per decidere, si apre l'atto intero:

  ```
  python3 risultati/strumenti/mostra-atto.py <corpus.jsonl> doc-0123
  ```

  Nel dubbio si apre sempre. Giudicare dall'estratto un atto che non si è letto
  è la fonte di errore più comune.

### La scala

| Grado | Significato | Esempio, per `manutenzione strade` |
|---|---|---|
| **2** | risponde al bisogno per intero: è un atto che chi cerca vuole trovare | la determina che affida la manutenzione ordinaria delle strade comunali |
| **1** | pertinente ma parziale: tocca il bisogno e chi cerca lo vorrebbe vedere, ma non basta da solo | la liquidazione di un singolo intervento di rattoppo; l'ordinanza di chiusura di una via per quei lavori |
| **0** | non risponde, anche se contiene le parole della query | un avviso di concorso che nomina "manutenzione" fra le mansioni; un atto con l'indirizzo "strada provinciale" |

Regole per i casi dubbi:

- **Si giudica l'atto, non le parole.** Un atto che contiene tutte le parole
  della query e parla d'altro vale 0; uno che non ne contiene nessuna e risponde
  vale 1 o 2.
- **Un atto e la sua rettifica** si giudicano ciascuno per conto proprio: la
  rettifica di un affidamento di manutenzione è pertinente quanto l'originale.
- **Un comune diverso da quello che si ha in mente** non abbassa il grado, a
  meno che la query nomini un comune.
- **Grado vuoto vuol dire "non l'ho guardato"**, mai "non pertinente".
  `scripts/pool -sheet` si ferma su una riga vuota e dice quale, apposta.
- **Nel dubbio fra due gradi, il più basso**, e una nota nella riga di
  `sessioni.tsv` (sotto). Le note servono a capire, dopo, dove la scala non
  regge.

### Dopo

- **Un giudizio non si cambia dopo aver visto le metriche.** Un errore trovato
  dopo (un atto letto male) si corregge in un file nuovo, con la riga e il
  motivo nel registro di `risultati/README.md`, come ogni altra correzione
  dell'archivio.
- **Tempi.** Per ogni sessione una riga in `sessioni.tsv`, accanto al foglio:
  annotatore, inizio, fine, prima e ultima riga annotata, note. Il tempo per
  giudizio è un numero da tesi: dice quanto costa un corpus di valutazione.
- **Sessioni brevi**, un'ora al massimo: dopo, i giudizi peggiorano senza che
  chi annota se ne accorga.

## Parte 3 - Il secondo annotatore e il kappa

**Perché.** Un solo annotatore misura anche il suo modo di giudicare. Il
secondo dice quanto i giudizi dipendono dalla persona, e quindi quanto sono
solide le differenze fra i motori.

**Come.**

1. Si estraggono a caso, con un seme fissato, alcune query intere dal foglio
   già annotato: le query intere e non righe sparse, perché ogni giudizio si dà
   rispetto a un bisogno, e chi giudica deve vederlo tutto. L'obiettivo è
   almeno 150 righe.
2. Il secondo annotatore (Leopoldo) riceve le descrizioni dei bisogni, queste
   istruzioni e un foglio con la colonna `grado` vuota. **Non vede i giudizi del
   primo e non ne parla con lui** finché non ha finito.
3. Si calcolano il kappa di Cohen sui tre gradi e il kappa pesato linearmente,
   perché fra 1 e 2 si sbaglia di meno che fra 0 e 2, e la percentuale di
   accordo semplice. **Si riportano comunque, anche se bassi.** Un kappa basso
   non si nasconde: si scrive, e si guarda dove sono i disaccordi.
4. Solo dopo, i due discutono i disaccordi. Il risultato della discussione va
   in un file a parte: le metriche della tesi usano i giudizi del primo
   annotatore, e si riporta di quanto cambiano con quelli del secondo e con
   quelli concordati.

## Cosa non si fa mai

- Annotare dopo aver visto le metriche di quella collezione.
- Giudicare in ordine di ranking, o sapendo quale motore ha trovato il
  documento.
- Correggere un giudizio in silenzio.
- Scegliere a mano gli atti da mostrare o le query da tenere.
- Mettere in un file dell'archivio il nome di chi ha scritto una query.
