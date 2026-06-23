# Domande "Killer" per l'Esame di Modellazione e Simulazioni Numeriche

Questo documento raccoglie le domande concettuali più insidiose che il professore potrebbe farti riguardo al progetto sulla Percolazione e all'Algoritmo di Hoshen-Kopelman.

---

### 1. Il "Mistero" della Soglia 0.59
> **Domanda:** *"Lei ha trovato che la soglia è circa 0.59 su reticolo quadrato. Se avessimo usato degli esagoni (nido d'ape), la soglia cambierebbe? E la forma delle curve (es. la pendenza della S)?"*

- **Risposta chiave:** Sì, la soglia $p_c$ cambierebbe (per gli esagoni è circa 0.70). Tuttavia, la **forma** delle curve e gli **esponenti critici** (come la velocità con cui diverge il RACS) resterebbero identici.
- **Concetto teorico:** **Universalità**. La geometria specifica del reticolo influenza il valore numerico della soglia, ma la fisica della transizione (classe di universalità) dipende solo dalla dimensione spaziale (2D).

### 2. L'efficienza di Hoshen-Kopelman vs Flood-Fill
> **Domanda:** *"Perché l'algoritmo HK è così tanto più veloce del Flood-Fill proprio vicino alla soglia critica? Cosa succede fisicamente ai cluster in quel punto?"*

- **Risposta chiave:** Vicino alla soglia i cluster diventano "frattali", cioè molto ramificati e grandi quanto tutto il sistema. Il Flood-Fill, essendo ricorsivo, deve tenere in memoria tutta la "storia" dell'esplorazione del cluster, saturando la RAM (Stack Overflow).
- **Concetto teorico:** **Complessità Algoritmica**. HK legge solo una riga alla volta e gestisce le fusioni tramite Union-Find, rendendo il tempo di calcolo proporzionale solo al numero di siti ($O(L^2)$) e indipendente dalla forma dei cluster.

### 3. Il campionamento Monte Carlo e l'indipendenza
> **Domanda:** *"Perché per ogni valore di p deve generare N=1000 matrici diverse da zero? Non basterebbe generarne una enorme?"*

- **Risposta chiave:** Una singola matrice è solo una "realizzazione" statistica. Per stimare una **probabilità**, dobbiamo mediare su molti eventi indipendenti e privi di correlazione.
- **Concetto teorico:** **Legge dei Grandi Numeri**. Solo mediando su un numero $N$ elevato di campioni indipendenti possiamo garantire che la nostra media campionaria sia una stima corretta del valore teorico di equilibrio.

### 4. Il significato fisico del picco del RACS
> **Domanda:** *"Perché il RACS mostra un picco (il 'vulcano') esattamente sulla soglia e poi crolla drasticamente?"*

- **Risposta chiave:** Il RACS calcola la dimensione media di tutti i cluster *escluso* quello gigante. Proprio sulla soglia, i cluster "piccoli" si fondono tra loro diventando enormi, ma un istante dopo vengono "mangiati" dal cluster infinito che percola.
- **Concetto teorico:** **Divergenza della Lunghezza di Correlazione**. Tipico delle transizioni di fase: una grandezza fluttua violentemente o "esplode" proprio nel punto di transizione prima che il sistema si ordini stabilmente.

### 5. Effetti di Taglia Finita (L)
> **Domanda:** *"Se usasse una griglia L=10 invece di L=100, la sua curva a S diventerebbe più verticale o più piatta?"*

- **Risposta chiave:** Diventerebbe molto più **piatta** e "sfumata".
- **Concetto teorico:** **Finite-Size Scaling**. Il "salto" netto (funzione di Heaviside) previsto dalla teoria esiste solo nel limite termodinamico ($L \to \infty$). Più il sistema è piccolo, più i bordi influenzano il risultato e "arrotondano" la transizione.

---
> [!TIP]
> **Consiglio per l'orale:** Se non sai rispondere subito, prendi tempo dicendo: *"Questo fenomeno è legato al comportamento critico del sistema vicino alla soglia..."*. Ti darà quei 5 secondi per far mente locale sui pilastri teorici.
