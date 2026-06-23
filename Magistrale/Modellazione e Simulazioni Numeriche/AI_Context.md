# Contesto di Progetto per Assistenti IA (AI Context)

> **Nota per qualsiasi Assistente IA (Claude, ChatGPT, Cursor, Copilot, ecc.):**
> Leggi questo file prima di aiutare l'utente con il codice o la teoria in questa repository.

## 1. Selezione del Progetto d'Esame

L'utente sta affrontando l'esame di _Modellazione e Simulazioni Numeriche_ e tra le varie tracce proposte ha scelto definitivamente il progetto sulla **PERCOLAZIONE** (il progetto alternativo sulle 'Code' va ignorato a meno che non ci siano domande teoriche specifiche).

## 2. Punti Chiave da Tenere a Mente per la Generazione e Assistenza

- **Linguaggio e Strumenti:** Il progetto va sviluppato rigorosamente in **Matlab**.
- **Algoritmica:** Il cuore del codice richiede la riscrittura e il testing dell'algoritmo **Hoshen-Kopelman (HK)** per l'analisi dei cluster su matrici 2D ($L \times L$), sfruttando il metodo "union-find" sulle label ed evitando categoricamente ricorsioni espansive (_no flood-fill retroattivo_).
- **Analisi dei Dati (Tassativo):** Il docente richiede un rigore assoluto nell'errore:
  - Nessun grafico deve essere generato senza l'apporto della deviazione standard appropriata (tramite la funzione `errorbar(..., std_dev / sqrt(N))` per prove indipendenti).
  - L'estrapolazione delle curve va infittita drasticamente nell'area della "_transizione di fase_" ($p \approx 0.5-0.6$) per individuare accuratamente la curva di Heaviside interpolata.
- **Metriche Richieste:** Oltre ai tempi d'esecuzione dell'algoritmo al variare della taglia $L$ o della probabilità $p_{col}$, occorre calcolare le distribuzioni d'appartenenza a cluster (valori di $P_1$) e definire esplicitamente la Media Ridotta della taglia dei Cluster (**RACS**).

## 3. Direttive dell'Utente

Fornire sempre snippet validi in framework Matlab standard locale e mantenere la generazione snella per favorire l'argomentazione (l'utente sosterrà un esame orale partendo da questi file testati sul proprio portatile).
