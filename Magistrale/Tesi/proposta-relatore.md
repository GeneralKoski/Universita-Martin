# Proposta di tesi magistrale

**Studente:** Martin Trajkovski, matricola 397464
**Corso:** Laurea Magistrale in Scienze Informatiche, secondo anno
**Data:** settembre 2026

## La proposta in due righe

Ho scritto un motore di ricerca il cui ranking è un'euristica costruita a intuito, e non ho alcun modo di sapere quanto sbaglia. Vorrei costruire il metro che manca, usarlo per correggere tre difetti che ho già individuato nel codice, e misurare ogni correzione su un sistema documentale reale.

## Cosa esiste già

**Koskidex** è un motore di ricerca full-text che ho scritto in Go: 2.850 righe di codice e 2.060 di test, senza dipendenze esterne oltre `golang.org/x/text`. Ha indice inverso, tolleranza ai refusi con Damerau-Levenshtein e prefissi bigram, faccette, filtri geospaziali, cache LRU, persistenza con write-ahead log e una copertura di test per ogni modulo. È pubblico su GitHub.

**Documentale** è un sistema di gestione documentale sviluppato in azienda, dove ho lavorato direttamente. I documenti vengono caricati, un modello ne estrae i metadati in uno schema definito a runtime, e un utente conferma o corregge ogni campo. Oggi la ricerca passa da Elasticsearch. L'azienda ha autorizzato l'uso del progetto a fini di tesi.

Il primo fornisce il codice su cui intervenire, il secondo il corpus e il carico di query reale su cui misurare.

## Il problema

Rileggendo il codice di Koskidex con occhi critici ho trovato tre difetti precisi. Non sono bug: sono scelte fatte senza un criterio, che funzionano abbastanza da non dare fastidio e che non ho mai potuto valutare.

**1. Il ranking non conosce la rarità dei termini.** Il punteggio lessicale è `(10 - refusi + 2*esatti) * peso_campo`. Non c'è frequenza di termine né frequenza inversa di documento: un termine rarissimo e uno comunissimo pesano identico. Nel codice esiste un campo `Posting.TF` annotato `// term frequency (calculated later)` che non viene letto da nessuna parte (`internal/engine/inverted.go:12`).

**2. La ricerca ibrida non è ibrida.** Quando la query ha termini testuali, il punteggio vettoriale viene sommato solo ai documenti che la parte lessicale ha già trovato (`internal/engine/ranker.go:203-222`). Un documento semanticamente pertinente che il lessicale non ha pescato non entra mai nei risultati. È un riordinamento, non un recupero ibrido, e nella documentazione è descritto in modo fuorviante.

**3. La fusione dei punteggi somma scale incomparabili.** L'istruzione è `m.Score += sim * 20.0`. Il punteggio lessicale si accumula per token e cresce senza limite con la lunghezza della query; quello vettoriale è limitato a 20. Su una query di una parola il contributo semantico domina, su una di cinque è rumore. Il valore 20 l'ho scelto a occhio.

## Quello che manca prima di tutto il resto

Nessuno dei tre difetti si può correggere in modo difendibile, perché **non esiste un modo di misurare se una correzione migliora davvero i risultati**. I benchmark presenti nel progetto misurano la velocità, non la qualità del recupero.

La prima parte del lavoro, e secondo me la più importante, è quindi costruire l'impianto di valutazione: un corpus di documenti, un insieme di query annotate a mano con giudizi di rilevanza, e le metriche standard del settore (nDCG, MRR, richiamo e precisione ai primi k risultati).

Su questo punto c'è un vincolo metodologico che intendo rispettare in modo rigido. Il sistema aziendale ha solo un ambiente di collaudo, quindi non dispongo di dati d'uso reali. Generare i giudizi di rilevanza con lo stesso modello che poi devo valutare sarebbe circolare, quindi **i giudizi vanno scritti a mano prima di osservare le risposte del motore**. Dati generati artificialmente li userei solo per misurare latenza e memoria, mai la rilevanza.

## Cosa propongo di misurare

Ogni correzione è confrontata contro il comportamento attuale, che resta sempre eseguibile come termine di paragone.

| Difetto | Correzione | Misura |
|---|---|---|
| Nessun IDF | BM25 | nDCG@10 e MRR contro il ranking attuale |
| Ibrido che è riordinamento | Recupero per unione | Richiamo@10, per classe di query |
| Costante scelta a occhio | Reciprocal Rank Fusion e pesatura normalizzata | Calibrazione e confronto, per classe di query |

Le query sono divise per classe, e qui sta l'ipotesi che mi interessa di più verificare. In un sistema documentale una parte rilevante delle ricerche sono identificatori esatti: numero di fattura, partita IVA, protocollo. È il caso in cui il contributo semantico è noto per essere dannoso, perché codici quasi identici sono vicinissimi nello spazio degli embedding e del tutto distinti per chi cerca. Mi aspetto che il peso ottimo fra componente lessicale e semantica **dipenda dal tipo di query**, e che una fusione che riconosce il tipo batta una pesatura fissa. Se i dati smentiscono l'ipotesi, è comunque un risultato da riportare.

Il lavoro si chiude sostituendo Elasticsearch con Koskidex in Documentale, mantenendo i due motori affiancati e selezionabili, così da poter eseguire le stesse query su entrambi e confrontarli su qualità, latenza, memoria e dimensione dell'indice.

## Cosa ho deciso di lasciare fuori

Avevo considerato di aggiungere un indice approssimato per la ricerca vettoriale (HNSW con quantizzazione dei prodotti). L'ho escluso: la scansione lineare regge il volume documentale di un'azienda, quindi sarebbe stata una domanda di ricerca senza un bisogno reale dietro. Se la misura di scalabilità dovesse mostrare il contrario, è la prima estensione naturale.

## Cosa chiedo

Un parere sull'impianto, in particolare sulla costruzione del corpus e dei giudizi di rilevanza, che è la parte più costosa e quella che vorrei impostare bene prima di iniziare. Ho già un piano di lavoro dettagliato che posso portare a ricevimento.

Il codice di Koskidex è consultabile: <https://github.com/GeneralKoski/Koskidex>
