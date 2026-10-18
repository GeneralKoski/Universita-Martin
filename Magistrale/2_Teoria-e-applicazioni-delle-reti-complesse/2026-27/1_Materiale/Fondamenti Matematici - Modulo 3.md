# Fondamenti matematici (Modulo 3)

Fonte: `Fondamenti Matematici - Modulo 3.pdf`

## Cos'è un grafo
- Un **grafo** è una coppia $G = (V, E)$:
  - $V = \{v_1, v_2, \dots, v_n\}$ è l'insieme dei **nodi** (o vertici), con $|V| = n$
  - $E \subseteq V \times V$ è l'insieme degli **archi** (o link), con $|E| = m$
- $V \times V$ è il **prodotto cartesiano**: l'insieme di tutte le **coppie ordinate** possibili di nodi, $n^2$ coppie
  - Esempio con $V = \{A, B, C\}$: $V \times V = \{(A,A), (A,B), (A,C), (B,A), (B,B), (B,C), (C,A), (C,B), (C,C)\}$, cioè $3^2 = 9$ coppie
  - Le coppie del tipo $(A, A)$ sono gli **autoanelli** (self-loop), che compaiono più avanti nelle liste di adiacenza
- Esempio guida delle slide: 4 nodi $v_1, \dots, v_4$ con archi $(v_1,v_3), (v_3,v_4), (v_2,v_4), (v_2,v_3)$

## Grafo non orientato e orientato
- Un arco è una coppia di nodi $(v_i, v_j)$
- **Grafo non orientato** (non diretto, indiretto): la coppia è **non ordinata**, $(v_i, v_j) \equiv (v_j, v_i)$
- **Grafo orientato** (diretto): la coppia è **ordinata**, $(v_i, v_j) \neq (v_j, v_i)$; l'arco va da $v_i$ a $v_j$
- Confronto sullo stesso disegno:
  - non orientato: $(v_1,v_3), (v_3,v_4), (v_2,v_4), (v_2,v_3)$
  - orientato: $(v_1,v_3), (v_3,v_4), (v_4,v_2), (v_3,v_2)$, più $(v_4,v_3)$: in un grafo orientato $(v_3,v_4)$ e $(v_4,v_3)$ sono **due archi distinti** (doppia freccia nel disegno)

### Reti reali non orientate: amicizie di Facebook
- $V$ = utenti, $E$ = amicizie
- L'amicizia è **simmetrica** (se A è amico di B, B è amico di A), quindi il grafo è **non orientato**
- $V = \{Marco, Sara, Luca, Anna, Paolo\}$, $n = 5$
- $E = \{(Marco,Sara), (Marco,Luca), (Marco,Anna), (Marco,Paolo), (Sara,Luca), (Sara,Anna), (Anna,Paolo)\}$, $m = 7$

### Reti reali orientate: Instagram
- $V$ = utenti, $E$ = "seguiti"
- Seguire **non è simmetrico** (se A segue B non è detto che B segua A), quindi il grafo è **orientato**
- $V = \{Marco, Giulia, Luca, Anna\}$, $n = 4$
- $E = \{(Marco,Giulia), (Giulia,Marco), (Luca,Marco), (Marco,Anna), (Giulia,Anna), (Luca,Giulia)\}$, $m = 6$
- $(Marco, Giulia)$ si legge "Marco segue Giulia"; $(Marco,Giulia)$ e $(Giulia,Marco)$ sono due archi distinti (seguito reciproco)

### Esempi: non orientate vs orientate
| Non orientate | Orientate |
|---|---|
| Rete elettrica (power grid italiana) | Food web (chi mangia chi) |
| Co-autori in ambito scientifico | Citazioni scientifiche |
| PPI network (interazioni proteina-proteina) | Rete stradale (Montpellier, grafo orientato: sensi unici) |

- **Esercizio proposto**: costruire una tabella di reti reali divise in non orientate e orientate, indicando per ciascuna il significato di nodi e legami

## Grafo binario e grafo pesato
### Grafo binario (non pesato)
- $G = (V, E)$: ogni arco **esiste o non esiste**
- Rappresentazione **più semplice**: cattura la **struttura delle connessioni** ma non la loro **intensità**
- È definito dalla **matrice di adiacenza** $A$:

$$A_{ij} = \begin{cases} 1 & \text{se } (v_i, v_j) \in E \\ 0 & \text{altrimenti} \end{cases}$$

- Esempio delle slide (6 nodi, non orientato): archi A-B, A-C, A-D, A-E, B-D, B-E, C-F, D-F, E-F; la matrice è simmetrica, la diagonale è indicata con "-"

### Grafo pesato
- $G = (V, E, W)$ aggiunge una **funzione peso** $W : E \to \mathbb{R}$: a ogni arco è attribuito un valore numerico
- Rappresentazione **più complessa**: cattura la struttura e anche l'**eterogeneità delle connessioni** (nel disegno lo spessore dell'arco è proporzionale al peso)
- È definito dalla **matrice dei pesi** $W$:

$$W_{ij} = \begin{cases} w_{ij} \in \mathbb{R} & \text{se } (v_i, v_j) \in E \\ 0 & \text{altrimenti} \end{cases}$$

- Esempio delle slide (pentagono $u, v, x, y, z$): $u$-$v$ = 4.1, $u$-$x$ = 1.7, $u$-$z$ = 3.1, $v$-$x$ = 0.3, $x$-$y$ = 1.2, $y$-$z$ = 5; matrice simmetrica con 0 dove l'arco manca

$$W = \begin{pmatrix} 0 & 4.1 & 1.7 & 0 & 3.1 \\ 4.1 & 0 & 0.3 & 0 & 0 \\ 1.7 & 0.3 & 0 & 1.2 & 0 \\ 0 & 0 & 1.2 & 0 & 5 \\ 3.1 & 0 & 0 & 5 & 0 \end{pmatrix} \quad (\text{ordine } u, v, x, y, z)$$

### Esempi: binarie vs pesate
- **Binarie**: amicizie di Facebook (c'è o non c'è), rete aerea come semplice esistenza di una rotta
- **Pesate**: food web con un peso su ogni arco (es. lince → orso grizzly 0.3; la slide non dice cosa misuri il peso), rete aerea con pesi diversi a seconda della domanda:
  - numero di voli
  - distanza in km
  - numero di passeggeri
  - prezzo medio dei biglietti
- La stessa rete può avere **pesi con significati diversi**: la scelta del peso cambia l'analisi (ripreso nel Modulo 4 con proximity vs remoteness)
- **Esercizio proposto**: tabella di reti reali binarie e pesate, con significato di nodi, legami e **pesi**

## Grafo bipartito
- $G = (U, V, E)$ è **bipartito** se:
  - $U = \{u_1, \dots, u_n\}$ e $V = \{v_1, \dots, v_n\}$ sono **due insiemi di nodi disgiunti**: $U \cap V = \emptyset$
  - $E \subseteq U \times V$: **ogni arco connette un nodo di $U$ con un nodo di $V$**
  - non esistono legami $(u_i, u_j)$ né legami $(v_i, v_j)$
- Esempi reali dalle slide:
  - **Film** ($U$) e **attributi** ($V$: registi, sceneggiatori, compositori): un arco collega un film al suo regista, sceneggiatore, compositore (es. *La dolce vita* - Fellini, Nino Rota, Flaiano, Pinelli)
  - **Ingredienti** ($U$) e **molecole aromatiche** ($V$): ogni composto aromatico è collegato agli ingredienti che lo contengono (flavor network)
  - **Specie di insetti** ($U$, impollinatori diurni e notturni) e **specie vegetali** ($V$): ogni insetto è collegato alle piante che impollina

| Insieme $U$ | Insieme $V$ | Arco $(u_i, v_j)$ significa |
|---|---|---|
| Attori | Film | $u_i$ ha recitato in $v_j$ |
| Ricercatori | Articoli | $u_i$ ha scritto $v_j$ |
| Utenti | Prodotti | $u_i$ ha acquistato $v_j$ |
| Ingredienti | Ricette | $u_i$ è usato in $v_j$ |
| Film | Registi / Sceneggiatori / Compositori | $u_i$ è stato diretto / scritto / musicato da $v_j$ |
| Parassiti | Ospiti | $u_i$ infetta $v_j$ |
| Piante | Impollinatori | $u_i$ è impollinata da $v_j$ |
| Geni | Malattie | $u_i$ è associato a $v_j$ |
| Utenti | Canzoni / Film / Serie TV | $u_i$ ha ascoltato / guardato $v_j$ |
| Parole | Documenti | $u_i$ appare in $v_j$ |

## Grafo planare
- Una rete è **planare** se può essere disegnata su un piano senza che nessun link ne attraversi un altro
- Basta che **esista almeno un modo** di disegnarla senza incroci: un disegno con incroci non prova che il grafo non sia planare
- Figura: (A) pentagono, planare; (B) pentagono con tutte le diagonali (grafo completo a 5 nodi), non planare
- Esempi reali:
  - **planari**: reti stradali, ferroviarie (es. rete ferroviaria olandese), power grid, circuiti stampati
  - **non planari**: reti aeree, Internet, reti sociali
- (Aggiunta: le reti stradali e ferroviarie sono planari solo in prima approssimazione, perché ponti e sottopassi creano incroci senza nodo.)

## Grafo multidimensionale (multiplex)
- Un grafo multidimensionale è una tripla $M = (V, D, \varepsilon)$:
  - $V = \{v_1, \dots, v_n\}$: insieme dei nodi, **gli stessi in tutte le dimensioni**
  - $D = \{d_1, d_2, \dots\}$: insieme delle **dimensioni** (o layer)
  - $\varepsilon = \{E^{(1)}, E^{(2)}, \dots, E^{(|D|)}\}$: collezione degli insiemi di archi, **uno per dimensione**, con $E^{(\alpha)} \subseteq V \times V$
  - **non esistono link inter-layer**: ogni arco vive dentro un solo layer
- (Nella slide le dimensioni sono scritte $d_1, \dots, d_n$ e l'ultimo insieme $E^{(D)}$: $n$ è già il numero di nodi e $D$ è un insieme, quindi l'indice corretto è $|D|$.)
- Esempi dalle slide:
  - tre layer con gli stessi 10 nodi e archi diversi (prima, seconda, terza dimensione)
  - trasporti di Londra: layer **bus**, **metro**, **rail** sulle stesse località
  - reti sociali: legami familiari, amicizie (mondo fisico, diffusione di comportamenti/malattie), interazioni Twitter e Facebook (mondo virtuale, diffusione di informazione)
  - batteri del microbioma in tre fasce d'età (neonati 0-2 anni, adulti 18-65, anziani 65+), con link di co-occorrenza dentro ogni layer
- (Le figure collegano con linee tratteggiate verticali lo stesso nodo nei vari layer, e l'ultima le chiama "link inter-layer, stesso batterio attraverso le fasce d'età". Non contraddice la definizione solo se le si legge come identità dello stesso nodo fra layer e non come archi; se fossero archi veri, la rete sarebbe un multilayer.)

## Grafo multilayer
- Un grafo multilayer è una quadrupla $\mathcal{M} = (V_M, E_M, V, L)$:
  - $V$: insieme di tutte le **entità** (possono essere diverse tra layer)
  - $L = \{l_1, l_2, \dots, l_d\}$: insieme dei **layer**
  - $V_M \subseteq V \times L$: insieme delle **node-layer tuples**; ogni nodo è la coppia (entità, layer), e $(v, \alpha)$ rappresenta l'entità $v$ nel layer $\alpha$
  - $E_M \subseteq V_M \times V_M$: insieme degli archi, **sia intra-layer sia inter-layer**
- **Differenza chiave dal multidimensionale: esistono link inter-layer**, e un'entità può non comparire in tutti i layer
- Esempio: multi-omica (Trans-OWAS), ogni layer è un livello biologico (genoma, epigenoma, trascrittoma, proteoma, metaboloma, fenoma: geni, RNA, proteine, metaboliti); le connessioni esistono sia dentro lo stesso layer sia tra layer diversi, fino ai fenotipi di pazienti e non pazienti

## Grafo temporale
- Un grafo temporale $G(T)$ è una **sequenza di grafi istantanei**:

$$G(T) = \{G(t_1), G(t_2), G(t_3), \dots, G(t_n)\}$$

- $G(t) = (V, E(t))$ è il grafo attivo all'istante $t$, con $E(t) \subseteq V \times V$ insieme dei link al tempo $t$
- In alternativa: $E \subseteq V \times V \times T$ è l'insieme degli **archi temporali**, ogni arco è una **tripla** $(v_i, v_j, t)$: esiste un legame tra $v_i$ e $v_j$ al tempo $t$
- $T$ è il **dominio temporale**:
  - **discreto**: $T \in \{1, 2, \dots, k\}$ (es. $(v_i, v_j, \text{Monday})$, una rete per ogni giorno della settimana)
  - **continuo**: $T \subseteq \mathbb{R}$
- **Il tempo determina quando un arco è attivo**; i nodi restano gli stessi
- Esempi: contatti tra 5 persone (Ashley, Blake, Casey, Dylan, Elliot) anno per anno dal 2007 al 2016; food web di una laguna che cambia fra stagione fredda (fioriture di *Ulva*) e stagione calda (fioriture di fitoplancton) per effetto dell'eutrofizzazione

## Rappresentazioni di un grafo
### Matrice di adiacenza
- $A$ è una matrice $n \times n$ con $a_{ij} = 1$ se $(v_i, v_j) \in E$, 0 altrimenti
- **Non orientato**: $(v_i,v_j) \equiv (v_j,v_i)$, quindi $a_{ij} = a_{ji}$, **matrice simmetrica**
- Esempio (5 nodi, archi $v_1v_2, v_1v_3, v_1v_4, v_2v_3, v_2v_5, v_3v_4, v_4v_5$):

$$A = \begin{pmatrix} 0&1&1&1&0 \\ 1&0&1&0&1 \\ 1&1&0&1&0 \\ 1&0&1&0&1 \\ 0&1&0&1&0 \end{pmatrix}$$

- **Orientato**: $(v_i,v_j)$ è diverso da $(v_j,v_i)$, quindi in generale $a_{ij} \neq a_{ji}$, matrice **non simmetrica**; la riga $i$ indica gli archi uscenti da $i$
- Esempio (archi $1\to2$, $1\to3$, $3\to2$, $3\to4$, $4\to3$):

$$A = \begin{pmatrix} 0&1&1&0 \\ 0&0&0&0 \\ 0&1&0&1 \\ 0&0&1&0 \end{pmatrix}$$

- Il nodo 2 non ha archi uscenti: la sua riga è tutta zero

### Matrice dei pesi
- $W$ è $n \times n$ con $w_{ij} \in \mathbb{R}$ se $(v_i,v_j) \in E$, 0 altrimenti
- **Non orientato**: $w_{ij} = w_{ji}$. Esempio a 8 nodi: 1-2 = 3, 2-3 = 12, 2-4 = 2.7, 2-5 = 5, 4-5 = 3.5, 4-6 = 3, 6-7 = 3, 6-8 = 8, matrice simmetrica
- **Orientato**: in generale $w_{ij} \neq w_{ji}$ (possono anche coincidere, ma non è richiesto)
- Esempio orientato delle slide: archi $1\to2$ (3), $1\to4$ (8), $2\to3$ (5), $2\to5$ (4), $5\to3$ (7), $5\to4$ (2), $4\to3$ (4)
- (La matrice (b) della slide non corrisponde a questo grafo orientato: è simmetrica, cioè è la matrice della versione non orientata, e usa $\infty$ per gli archi assenti e 0 sulla diagonale, la convenzione delle matrici delle distanze per Dijkstra, non quella "0 altrimenti" appena definita. Con la definizione della slide la matrice corretta è:)

$$W = \begin{pmatrix} 0&3&0&8&0 \\ 0&0&5&0&4 \\ 0&0&0&0&0 \\ 0&0&4&0&0 \\ 0&0&7&2&0 \end{pmatrix}$$

### Liste di adiacenza
- Una lista di adiacenza è una funzione $Adj : V \to 2^V$ che mappa ogni nodo $v_i$ nell'**insieme dei suoi vicini**:

$$Adj(v_i) = \{v_j \in V : (v_i, v_j) \in E\}$$

- $2^V$ è l'insieme delle parti di $V$: a ogni nodo corrisponde un sottoinsieme di nodi
- Esempio non orientato (6 nodi, autoanello sul 5): 1: {2,3}; 2: {1,4}; 3: {1,4,5}; 4: {2,3,6}; 5: {3,5,6}; 6: {4,5}
- Stesso grafo orientato: 1: {2,3}; 2: {4}; 3: {4,5}; 4: {6}; 5: {5,6}; 6: nessuno
- Nei grafi orientati si distinguono liste di adiacenza **uscenti** ed **entranti**
- Esempio Facebook (rete diversa da quella della sezione precedente):

```
Marco → [Sara, Luca]
Sara  → [Marco, Luca, Anna]
Luca  → [Marco, Sara, Paolo]
Anna  → [Sara]
Paolo → [Luca]
```

### Lista di adiacenza pesata
- Ogni vicino è accompagnato dal peso dell'arco. Esempio: rotte aeree tra 4 città

```
Milano → [(Roma, 12), (Parigi, 8),  (Londra, 6)]
Roma   → [(Milano, 12), (Parigi, 5), (Londra, 10)]
Parigi → [(Milano, 8),  (Roma, 5),  (Londra, 24)]
Londra → [(Milano, 6),  (Roma, 10), (Parigi, 24)]
```

- Nella figura ogni città riporta anche $s$ = somma dei pesi dei suoi archi: Milano 26, Roma 27, Parigi 37, Londra 40 (è la **strength**, definita nel Modulo 4)

### Lista dei legami (edge list)
- È la **lista di tutti gli archi**, uno per riga
- Grafo non orientato: $\varepsilon = \{(v_i, v_j) : (v_i, v_j) \in E\}$; esempio: A-B, A-C, A-D, A-E, A-F, E-F, F-G
- Grafo orientato: $\varepsilon = \{(v_i, v_j) : \text{arco da } v_i \text{ a } v_j\}$; poiché $(v_i,v_j) \neq (v_j,v_i)$, **l'ordine conta**
- Esempio orientato (output R, colonne sorgente e destinazione):

```
     [,1] [,2]
[1,] "A"  "B"
[2,] "A"  "C"
[3,] "A"  "F"
[4,] "B"  "C"
[5,] "D"  "E"
[6,] "D"  "F"
[7,] "E"  "F"
```

- (Nella figura accanto non c'è l'arco E → F: la riga 7 non corrisponde al disegno.)

### Lista dei legami pesata
- Grafo pesato: $\varepsilon = \{(v_i, v_j, w_{ij}) : (v_i, v_j) \in E\}$, ogni riga contiene sorgente, destinazione e peso
- Figura (mycodeschool): vertex list + edge list con tre colonne; la domanda "quanto tempo serve per trovare tutti i nodi adiacenti a un nodo dato?" evidenzia il limite della edge list: bisogna scorrere tutte le righe, mentre la lista di adiacenza li dà subito
- (Aggiunta: la matrice di adiacenza occupa $n^2$ celle anche se la rete è sparsa; liste di adiacenza ed edge list occupano spazio proporzionale a $m$, per questo i dataset di reti reali sono di solito distribuiti come edge list.)
