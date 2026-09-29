# Tabella di Marcia: Progetto Percolazione

Questa guida contiene il riassunto esatto del _Funzionamento_ del progetto e la _To-Do List_ (le cose da spuntare) da completare prima di presentarti all'esame.

---

## 1. Il Funzionamento del Progetto (Cosa stiamo simulando?)

L'esame richiede di dimostrare che hai capito come l'impostazione logaritmica (il calcolo puro) incroci le transizioni di fase (fenomeni fisici).

- **La Dinamica di Base:** Lavoriamo su un "reticolo quadrato" bidimensionale di grandezza fissa $L \times L$. Ciascuna casella (Sito) ha una probabilità $p_{col}$ di essere "colorata" (attiva).
- **L'Algoritmo di Ricerca (Hoshen-Kopelman):** Piuttosto che usare il classico programma visto a lezione che "cerca i vicini" esplorando tutta la macchia di colore in modo espansivo (il _flood-fill_ col vettore Pila), useremo l'**Algoritmo HK**. HK scorre il reticolo dall'alto in basso, riga per riga. Quando trova un sito attivo, guarda SOLTANTO il suo vicino in Alto e il vicino a Sinistra. Se entrambi sono colorati ma con etichette diverse, capisce che sono lo stesso _Cluster_ unito e usa una matrice in memoria per "fondere" i due destini insieme senza mai avere bisogno di fare "marcia indietro". È super performante!
- **Soglia Geometrica:** Se il reticolo fosse "infinito", esisterebbe un preciso e categorico istante in cui alzando $p_{col}$ la probabilità di creare un "Mega-Raggruppamento" che va da una parete all'altra scatterebbe improvvisamente da Zero a Cento. Poiché i tuoi reticoli saranno sempre limitati sul PC (es. $1000 \times 1000$), questa conversione "zero a cento" non sarà un gradino dritto ma apparirà come una curva morbida sul grafico (una _sigmoide_). L'obiettivo teorico clou è estrapolare la stima perfetta usando indicatori come la taglia media ridotta ($RACS$) su dimensioni $L$ crescenti.

---

## 2. Le Cose da Fare (To-Do List Pre-Esame)

Ecco i passaggi pratici in blocchi che dovrai ultimare da qui alla stesura della Relazione:

### Blocco A: Sviluppo del Codice (Matlab)

- [ ] **1. Ricostruzione dell'algoritmo:** Scrivere la funzione `HK.m`.
- [ ] **2. Validazione Logica:** Scrivere uno script che fa scansionare una scacchiera colorata sia al vecchio algoritmo (visto a lezione) che al tuo `HK.m`. **Obiettivo**: Mostrare che entrambi offrono lo stesso cluster percettivo (numero di siti attivi equivalenti).

### Blocco B: Estrapolazioni Analitiche ed Efficienza (La ciccia del punteggio)

- [ ] **1. Test Velocità (Var. Taglia):** Far generare un grafico del Tempo d'esecuzione ($t$) al variare della taglia del reticolo $L$ (tenendo $p_{col}$ fissa).
- [ ] **2. Test Velocità (Var. Probabilità):** Lanciare lo scanning tenendo $L$ gigante e fisso, infittendo l'avanzamento al variare della densità colore $p_{col}$.
- [ ] **3. Identificazione Soglia (Sigmoide):** Generare la curva statistica di "frequenza_di_percolazione(probabilità)" piazzando un boato di tentativi vicino al range d'inversione (tra 50% e 60% colorato).
- [ ] **4. Apposizione di errorbar:** Tutte le statistiche sopra menzionate vanno presentate col margine minimo di fluttuazione `std/sqrt(N)`.
- [ ] **5. Computo Dimensionale:** Calcolare e tracciare la funzione Media RACS per intercettare il comportamento a "vulcano" (cuspide) proprio dove sta la transizione di fase.

### Blocco C: Verso l'Esame

- [ ] **1. Scrittura:** Impaginate in bella copia (LaTeX o Word in PDF) i grafici e la comparazione prestazionale di HK nel file di `Relazione`.
- [ ] **2. Invio:** Inviare la Relazione d'esame entro il _mezzogiorno in tempo di scadenza_ fissato per la giornata antecedente al colloquio!
- [ ] **3. Collaudo Mac:** Avere la repository, o Matlab installato con i driver pronti, aperto e avviabile sul portatile il giorno della valutazione faccia a faccia, allenandosi in anteprima su possibili domande del Prof riguardo modifiche on the fly (es: "Cambiare una dimensione" / "Far crollare un array").
