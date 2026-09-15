# Lunedì 21 settembre - Aula G

Due potenziali relatori di fila, stessa aula.

| Ora | Corso | Docente |
|---|---|---|
| 08:30 - 10:30 | Programmazione Dichiarativa | **Dal Palù** (quello del 30L in Constraint Programming) |
| 10:30 - 12:30 | Algoritmi per l'Intelligenza Artificiale | **Bonnici** |

Non devo decidere lunedì. Devo uscire con: risposte sui dati, un'idea di chi è interessato, e un canale aperto con almeno uno dei due.

Due minuti a testa, alla fine della lezione. Non il discorso completo in corridoio.

---

## La domanda che vale per ogni traccia

Prima del metodo, prima dell'argomento, sempre questa:

> **Quanti dati ci sono, in che stato sono, e sono già disponibili oggi o devono ancora arrivare?**

Se la risposta è vaga, la traccia è da evitare qualunque sia l'argomento. Una tesi su dati che arrivano a marzo quando mi laureo a luglio non si finisce.

Corollario da chiedere subito dopo, se i dati sono di un altro gruppo: **chi è il referente e quanto è reattivo.**

---

## 08:30 - Dal Palù

Mi conosce, mi ha dato 30L con esposizione. È la conversazione a basso rischio: le domande scomode le posso fare a lui.

### Come aprire

> "Professore, sto iniziando a guardarmi intorno per la tesi. Ho visto le sue proposte e ce ne sono due che mi interessano. Le posso rubare due minuti?"

### Le tre domande strutturali

Queste valgono per tutto il resto dell'anno, e me le risponde sinceramente proprio perché mi conosce.

1. **Quelle proposte sono di dimensione tirocinio o tesi?** La pagina si intitola "Tirocini interni/esterni", e ho bisogno di sapere se il tirocinio confluisce nella tesi o se sono due cose separate.
2. **Che cosa considera un contributo sufficiente per una tesi magistrale?** Chiederlo esplicitamente evita di scoprirlo a giugno.
3. **Accetta tesi costruite su un sistema aziendale?** Nella sua lista c'è già la proposta ESG con tirocinio esterno, quindi il precedente c'è.

### Le tracce che mi interessano, in ordine

**1. Impronte digitali - metriche di similarità selettiva su grafi.** È la prima da chiedere.

- Esistono collezioni pubbliche utilizzabili, o servono dati suoi?
- Che cosa intende per "similarità selettiva": è già definita o è parte del lavoro definirla?
- **Bonnici potrebbe entrarci come secondo relatore?** Lui fa ricerca di sottografi e similarità su grafi, e ce l'ho in aula due ore dopo.

Perché la metto per prima: dati pubblici quindi nessun corpus da costruire, protocolli di valutazione già codificati quindi riproducibile, ed è metodologicamente quello che voglio fare, cioè definire una misura e costruire il modo di valutarla.

**2. Stazione Spaziale - pattern su immagini DWS.**

- Quante immagini, e la campagna è conclusa?
- Chi è il referente di Fisica e quanto è disponibile?
- Il riconoscimento dei pattern è supervisionato? Cioè esistono etichette, o vanno costruite?

### Cosa proporre di mio

Solo se la conversazione va bene e c'è spazio. Non forzarla.

L'aggancio giusto per lui non è il motore di ricerca, è **Documentale**: estrazione di metadati da documenti con un LLM, schemi definiti a runtime dall'utente e validati, correzione umana su ogni campo. È applicazione di modelli a dati reali in azienda, che è roba che nella sua lista c'è.

---

## 10:30 - Bonnici

Non mi conosce. Qui serve essere più precisi in meno parole, e ho il vantaggio di sapere già le risposte strutturali.

### Come aprire

> "Professore, mi interessa la tesi su temi di recupero dell'informazione. Ho visto la sua proposta sul RAG chatbot e ho anche un progetto mio che va in quella direzione. Le posso mandare due pagine o passare a ricevimento?"

Essere trasparente: **"ne sto parlando anche con il professor Dal Palù"**. L'ambiente è piccolo, scoprirlo dopo è peggio.

### Cosa chiedere

**Sul RAG chatbot per Telegram:**

- Che dimensione ha in mente? Costruire un RAG sono due settimane, quindi che cosa considera il contributo?
- Il corpus su cui gira è già deciso?
- Gli interessa la parte di **valutazione del recupero separata dalla generazione**, o il valore è nel sistema funzionante?

Se chiede cosa intendo, la risposta breve: quasi tutti i RAG si valutano guardando se la risposta sembra buona, senza mai separare le due metà. Misurare il recupero per conto suo e la generazione per conto suo, e mostrare come si legano, è la cosa che manca. E in una chat le domande non sono autonome ("e quanto costa?" dopo "parlami del contratto Rossi"), quindi la riscrittura della query è obbligata dal mezzo, non un dettaglio.

**Sulle impronte digitali:** se Dal Palù ha aperto alla co-relazione, chiederglielo direttamente.

**Su instance hardness** (misure di bontà degli algoritmi di ML): è la sua traccia più vicina a quello che mi viene naturale. Chiedere che dimensione ha.

---

## Il mio progetto, in sessanta secondi

Da tenere pronto per entrambi, se chiedono.

> Ho scritto un motore di ricerca full-text in Go, senza dipendenze esterne. Rileggendolo ho trovato tre difetti nel ranking che ho messo lì a intuito e che non ho mai potuto valutare, perché un modo di misurare la qualità dei risultati non ce l'ho. Vorrei costruire quel metro e usarlo per correggerli.

I tre difetti, se vuole i dettagli:

1. **Nessun IDF.** Il punteggio è `(10 - refusi + 2*esatti) * peso_campo`. Un termine rarissimo e uno comunissimo pesano uguale. C'è un campo `TF` nel codice annotato "calculated later" che nessuno legge.
2. **L'ibrido non è ibrido.** Il punteggio vettoriale si somma solo ai documenti che il lessicale ha già trovato: è riordinamento, non recupero. Un documento pertinente che il lessicale non pesca non entra mai.
3. **La fusione somma scale incomparabili.** `score += similarità * 20.0`, dove il lessicale cresce senza limite con la lunghezza della query e il vettoriale è fisso a 20. Il 20 l'ho scelto a occhio.

Il banco di prova è un sistema documentale aziendale su cui ho lavorato e che l'azienda mi ha autorizzato a usare.

L'ipotesi che mi interessa verificare: in un documentale una fetta delle ricerche sono identificatori esatti (numero fattura, partita IVA, protocollo), ed è il caso in cui la componente semantica danneggia, perché codici quasi identici sono vicinissimi negli embedding e del tutto distinti per chi cerca. Quindi il peso ottimo fra lessicale e semantico dovrebbe dipendere dal tipo di query.

Il documento lungo è in `piano-implementazione.md`, da portare a ricevimento, non lunedì.

---

## Cosa non fare

- Non fare il pitch completo in corridoio. Due minuti e un aggancio.
- Non presentare lo stesso identico discorso a entrambi come se ciascuno fosse l'unico. Sono temi diversi e vanno presentati diversi.
- Non nascondere che sto parlando con tutti e due.
- Non decidere lunedì.
- Non dire "ho scritto un motore di ricerca". Dire "ho un motore e non so quanto sbaglia".

---

## Dopo, come decido

**Regola sui dati.** Qualunque traccia la cui risposta sulla disponibilità dei dati sia vaga, esce dalla lista. Non importa quanto è bella.

**Regola sul relatore.** Se Dal Palù dice "portamela, ti seguo io", pesa molto. Mi conosce e mi ha già valutato 30L: nessuno dei due fa information retrieval, quindi sulla vicinanza tematica si gioca poco, e su un anno di lavoro il rapporto conta di più.

**La domanda vera**, da farmi a mente fredda e non lunedì a caldo:

> Su quale di questi sarò ancora contento di lavorare l'ottavo mese, alle dieci di sera, dopo una giornata a Codogno?

La tesi la faccio comunque post lavoro, qualunque argomento scelga. Quindi la motivazione non è un fattore secondario, è il fattore.

**Il costo nascosto da ricordare:** il piano su Koskidex richiede di annotare a mano un corpus prima di poter misurare qualsiasi cosa. Sono settimane di sere, e non è codice. Le impronte digitali quel costo non ce l'hanno, perché i dati pubblici sono già annotati. Se scelgo Koskidex, va chiesto al relatore se si può usare in gran parte una collezione pubblica e costruirne a mano solo una piccola di dominio.
