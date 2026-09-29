# Specifiche Algoritmiche e Laboratorio

Dettagli e peculiarità da impiegare nello sviluppo vero e proprio (script `.m`) per implementare le macchine dei progetti.

---

## 1. Logiche di Lavoro: Coda di Servizio

La stabilità e la consistenza della simulazione _markoviana_ impongono di simulare un processo a tempi variabili:

- **Loop ad Eventi:** Il sistema in Matlab (es. `CODA.m`) solitamente genera l'evento di avanzamento temporale selezionando il più piccolo tempo prossimo al compimento $t_{new} = \min([t_{arrivoprossimo}, t_{fineservizio}, t_{maxsimulazione}])$.
- **Check dei Limiti Coda (Sala Attesa):** Per i sistemi dotati di limite `N_max`, ogni volta che avviene un "gestisci arrivo", bisogna implementare il controllo per far accumulare il count del cliente solo qualora l'incremento di `Q` rimanga nei vincoli spaziali.
- **Valutazione della Matrice ed Estrazione Statica:** Creando manualmente (tramite indici logici o blocchi diagonali) l'intera **Matrice di Markov**, occorre estrarne gli autovalari col comando `[V, D] = eig(Matrice)`. Individuata la colonna legata all'autovalore rigorosamente uguale a $1$, il versore scalato e normalizzato equivarrà esattamente in via teorica alla probabilità stazionaria limitata.

---

## 2. Ingegneria: Algoritmo di Percolazione Hoshen-Kopelman (HK)

Il cuore dell'efficienza nella teoria della percolazione bidimensionale.

- **Non Backtracking ("Non si volta mai"):**
  Diversamente dal `CercaCluster` predefinito nel corso, che se trova un "1" si fionda usando uno stack in tutte e quattro le direzioni finché non ha mappato tutto ricorsivamente, l'algoritmo **HK** si sposta col puntatore del loop come una testina di stampa ($i \to N$, da sinistra a destra, dall'alto al basso).
- **Controllo Esclusivo Sopra e Sinistra (Top-Left):**
  Ogni interazione del sito $s_{k}$ necessita di un controllo solo col sito in sua adiacenza superiore e sinistra (visto che destra e bottom non sono state ancora inizializzate né vagliate).
- **Array delle Etichette e Albero Capi:**
  Se _Top_ e _Left_ hanno due colori/cluster labels diversi, il sistema unisce localmente i cluster associando il numero primario del cluster (solitamente usando una root union tree) per tracciare storicamente l'equivalenza senza rifare la mappa.

### Metriche Richieste dal Docente:

Per i codici di Percolazione occorrerà scrivere script di wrapper che:

1. Validano il corretto operato di HK, sputando in output identiche mappe cromatiche/labeling di _CercaCluster_.
2. Plottano i **Tempi di esecuzione**: un grafico `plot()` che illustri l'execution time mantenendo costante la $p_{col}$ e scansionando $L$ (taglia). E un secondo grafico che fissa invece la dimensione a $L$ molto grandi e fa variare gradualmente la $p_{col}$ per mostrare che l'efficienza non collassa in zona limitrofa alla congiunzione critica.
