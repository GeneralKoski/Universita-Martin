# Centralità dei nodi (Modulo 4)

Fonte: `Centralità dei nodi - Modulo 4.pdf`

## Chi è il più importante?
- Le misure di **centralità** assegnano a ogni nodo un punteggio di importanza; "importante" dipende dalla domanda:
  - quale persona in una rete sociale ha più **influenza sulla diffusione** di una notizia?
  - quale **router** di Internet, se si guastasse, causerebbe il maggior danno alla **connettività globale**? (Wang & Chen 2003)
  - quale **pagina web** merita di apparire prima nei risultati di Google? (PageRank)
- Ogni misura formalizza un'idea diversa di importanza: numero di contatti (degree), controllo dei flussi (betweenness), vicinanza a tutti (closeness), importanza dei vicini (eigenvector, PageRank), intensità dei legami (strength)

### Grafo d'esempio usato in tutto il modulo
- 9 nodi, 13 archi (non orientato): 8-5, 8-7, 8-6, 5-7, 5-6, 7-6, 7-9, 5-4, 6-4, 4-3, 3-1, 3-2, 1-2
- Struttura: un blocco denso {5, 6, 7, 8} con la foglia 9 attaccata a 7, il nodo 4 come **ponte** verso il triangolo {1, 2, 3}
- Versione orientata (per in/out-degree): $5\to8$, $6\to8$, $8\to7$, $5\to7$, $5\to6$, $7\to6$, $7\to9$, $4\to5$, $4\to6$, $3\to4$, $1\to3$, $2\to3$, $1\to2$

## Degree centrality (grado del nodo)
- **Grado** $k_i$ = **numero di primi vicini** = **numero di link** del nodo $i$

$$DC_i = k_i = \sum_j A_{ij}$$

- Esempio sul grafo d'esempio:

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $k_i$ | 2 | 2 | 3 | 3 | 4 | 4 | 4 | 3 | 1 |

- Massimo grado: 5, 6, 7 ($k = 4$), evidenziati in rosso; somma dei gradi $= 26 = 2m$
- **Nodi di alto grado = molte connessioni = hub**. Esempio: rete del traffico aereo (3200 aeroporti, 60000 rotte), hub Heathrow, Dubai, Atlanta, Istanbul

### In-degree (grado entrante)
- $k_i^{in}$ = numero di link **entranti** nel nodo $i$
- Con la convenzione $A_{ij} = 1$ quando $i \to j$ è la **somma della colonna $i$** della matrice di adiacenza:

$$k_i^{in} = \sum_j A_{ji}$$

- Esempio sul grafo orientato:

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $k_i^{in}$ | 0 | 1 | 2 | 1 | 1 | 3 | 2 | 2 | 1 |

- Massimo: nodo 6 ($k^{in} = 3$); il nodo 1 non riceve archi
- Interpretazioni:
  - **food web** (African animal food web, frecce da preda a predatore): alto in-degree = **consumatore generalista**; basso in-degree = dipende da **poche specie preda**
  - **rete di citazioni**: alto in-degree = **molte citazioni** = **articoli fondamentali** (es. Watson & Crick 1953, struttura del DNA, *Nature* 171)

### Out-degree (grado uscente)
- $k_i^{out}$ = numero di link **uscenti** dal nodo $i$ = **somma della riga $i$** della matrice di adiacenza (stessa convenzione):

$$k_i^{out} = \sum_j A_{ij}$$

- Esempio sul grafo orientato:

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $k_i^{out}$ | 2 | 1 | 1 | 2 | 3 | 1 | 2 | 1 | 0 |

- Massimo: nodo 5 ($k^{out} = 3$); il nodo 9 non ha archi uscenti
- $\sum_i k_i^{in} = \sum_i k_i^{out} = m = 13$
- Esempio matriciale (6 nodi, archi $1\to2$, $1\to3$, $2\to4$, $3\to4$, $3\to5$, $4\to6$, $5\to5$, $5\to6$): righe = nodi di partenza, colonne = nodi di destinazione; la riga 1 è $(0,1,1,0,0,0)$, quindi $k_1^{out} = 2$, la colonna 4 ha due 1, quindi $k_4^{in} = 2$
- Interpretazione: in una rete di contatti epidemici i nodi con molti link uscenti sono quelli che **infettano più individui** (super-spreader), anche tra sotto-reti diverse (città)

### Pro e contro della degree
| ✓ Pro | |
|---|---|
| Semplicità computazionale | $O(n)$, calcolabile in tempo reale anche su reti con miliardi di nodi |
| Interpretabilità immediata | Significato intuitivo, comprensibile senza matematica |
| Ottima per contagio diretto | È la misura più rilevante quando il processo si propaga per contatto diretto (epidemie, diffusione virale) |
| Robustezza al rumore | Aggiungere o togliere un arco cambia il grado di 1: effetto piccolo e prevedibile |

| ✗ Contro | |
|---|---|
| Visione puramente locale | Cieca alla struttura globale, ignora la posizione nella rete |
| Non distingue la qualità dei vicini | Tutti i vicini valgono uguale: essere amico di un influencer vale come qualunque altra amicizia |
| Non cattura ruoli strutturali | Un ponte tra due comunità con basso grado ha alta importanza strutturale, invisibile alla degree |
| Limitata per reti pesate | Ignora i pesi degli archi, servono altre misure (strength) |

## Cammino minimo e distanza
- Un **cammino** (path) è una sequenza di nodi distinti in cui ogni coppia consecutiva è collegata da un arco
- Il **cammino minimo** (shortest path) tra due nodi è quello con il **numero minimo di collegamenti** necessari per raggiungere un nodo partendo dall'altro
- La **distanza** $d_{ij}$ è la **lunghezza del cammino minimo** tra $i$ e $j$
- Esempio: tra $i$ e $j$ esistono un cammino di 4 link e uno di 6 link; il minimo è quello da 4, quindi $d_{ij} = 4$
- Possono esistere **più cammini minimi** con la stessa lunghezza tra la stessa coppia (conta per la betweenness)

### Algoritmo BFS (Breadth-First Search)
- Calcola la distanza $d_{ij}$: il numero minimo di archi da attraversare per andare da $i$ a $j$
- È il metodo naturale ed efficiente su un **grafo non pesato**: esplora la rete a "strati" (prima i vicini a distanza 1, poi quelli a distanza 2, ...)
- Complessità: $O(n) + O(m) = O(n + m)$, il tempo cresce in proporzione alla dimensione della rete (da una sorgente verso tutti i nodi)
- Riferimento: Moore (1959), *The shortest path through a maze*

### Applicazioni
- Il percorso più breve tra località (rete stradale spagnola)
- Il percorso con il minor numero di intermediari (rete sociale): veloce diffusione delle informazioni tra individui
- Il minimo numero di aeroporti in un viaggio
- La prossimità nella rete di interazioni proteiche

## Betweenness centrality (intermedietà)
- La betweenness $g(i)$ del nodo $i$:

$$g(i) = \sum_{s \neq i \neq t,\ s \neq t} \frac{\sigma_{st}(i)}{\sigma_{st}}$$

- $\sigma_{st}$ = numero totale di cammini minimi tra $s$ e $t$
- $\sigma_{st}(i)$ = numero di cammini minimi tra $s$ e $t$ che **passano per $i$**
- Ogni coppia contribuisce con la **frazione** dei suoi cammini minimi che passa per $i$: se ci sono due cammini minimi e solo uno passa per $i$, il contributo è $1/2$
- Interpretazione: quanto un nodo sta "in mezzo" ai flussi della rete. Alta betweenness = **broker**, **collo di bottiglia**, **ponte** tra comunità (in figura il nodo arancio che collega tre gruppi)
- Esempio sul grafo d'esempio:

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $g(i)$ | 0 | 0 | 12 | 15 | 6 | 6 | 7 | 0 | 0 |
| normalizzata | 0 | 0 | 0.43 | 0.54 | 0.21 | 0.21 | 0.25 | 0 | 0 |

- Il **nodo 4** è il massimo (in rosso) pur avendo solo grado 3: tutte le $3 \times 5 = 15$ coppie fra {1, 2, 3} e {5, 6, 7, 8, 9} passano per lui
- Il nodo 3: le $2 \times 6 = 12$ coppie fra {1, 2} e gli altri sei nodi; il nodo 7: le 7 coppie che hanno 9 come estremo
- I nodi 5, 6, 7 hanno il grado massimo ma betweenness molto più bassa del 4: **degree e betweenness misurano cose diverse**
- (Le slide non dicono come sono normalizzati i valori della seconda riga: sono divisi per il numero di coppie non ordinate che escludono $i$, $(n-1)(n-2)/2 = 28$, es. $15/28 = 0.54$. Inoltre i valori grezzi 15, 12, ... contano **ogni coppia una sola volta**; la somma su $s \neq t$ come scritta nella formula conta le coppie ordinate, cioè $(s,t)$ e $(t,s)$ separatamente, e darebbe il doppio. Verificato con NetworkX.)

### Degree vs betweenness
- Figura "albero di stelle": tre hub rosa con molte foglie (alto grado) collegati da un nodo azzurro centrale con grado 3 ma **massima betweenness**, perché ogni cammino tra stelle diverse passa per lui
- Rete sociale (Mike, Bob, Emma, Jill, John, Shane, Leah, Liz, Allen, Lisa): **Liz** ha pochi link ma è il **network broker** tra il gruppo denso e la coda Allen-Lisa
- Figura con nodi colorati dal rosso (minimo) al blu (massimo): i nodi centrali hanno betweenness alta, quelli periferici bassa
- I **bridge** tra comunità (nodi blu che collegano tre gruppi) hanno betweenness alta

### Esempio reale: C. elegans
- Rete di associazione funzionale tra geni di *Caenorhabditis elegans* (nematode lungo circa 1 mm, vive nel suolo in regioni temperate, organismo modello in biologia); nodi = geni, link = associazioni funzionali
- Colore = comunità, dimensione = betweenness: i nodi grandi hanno **alta betweenness perché connettono regioni funzionalmente differenti** della rete (esempio dalla documentazione NetworkX)

### Algoritmo di Brandes
- Calcolare la betweenness ingenuamente costa $O(n^3)$: bisogna trovare tutti i cammini minimi tra tutte le coppie
- **Brandes** (2001): per ogni nodo sorgente basta **una singola BFS** più una fase di **accumulo all'indietro** per calcolare il contributo di quella sorgente a tutte le betweenness
- Costo: $O(nm)$, la stessa complessità di fare una BFS da ogni nodo

### Pro e contro della betweenness
| ✓ Pro | |
|---|---|
| Cattura il flusso globale | Considera l'intera struttura: identifica broker, colli di bottiglia e connettori tra comunità |
| Formalizza i legami deboli | Evidenzia i ponti strutturali tra comunità, segue l'intuizione di Granovetter |
| Fondamentale per la robustezza | Rimuovere i nodi con alta betweenness è tra le strategie di attacco più efficaci, misura di riferimento in cybersecurity |
| Valida per reti non scale-free | Resta informativa quando i gradi sono simili tra loro, dove la degree discrimina poco |
| Base per community detection | L'algoritmo di Girvan-Newman si basa sul calcolo iterativo della betweenness degli **archi** |

| ✗ Contro | |
|---|---|
| Costo computazionale elevato | $O(nm)$ con Brandes, proibitivo su reti con milioni di nodi senza approssimazioni |
| Sensibile al rumore | Un singolo arco modificato può cambiare drasticamente la betweenness di nodi lontani: instabile su dati incompleti |
| Assume cammini minimi | Presuppone che il flusso segua sempre il percorso più breve, non sempre vero nelle reti reali |
| Non distingue tipi di intermediazione | Lo stesso valore può derivare da ruoli strutturali differenti |
| Problemi su grafi disconnessi | Le coppie in componenti diverse non contribuiscono: meno confrontabile in reti frammentate |

## Closeness centrality (centralità di vicinanza)
- La closeness di $i$ è l'**inverso della distanza media** da $i$ a tutti gli altri nodi:

$$C(i) = \frac{n - 1}{\sum_{j \neq i} d_{ij}}$$

- $d_{ij}$ = distanza (cammino minimo) tra $i$ e $j$; $n - 1$ = numero di altri nodi
- $\sum_j d_{ij} / (n-1)$ è la distanza media, $C(i)$ il suo inverso: valori in $(0, 1]$, vale 1 se $i$ è collegato direttamente a tutti
- **Esempio svolto, nodo 5** (passo 1: distanze da 5): $d(5,1) = 3$, $d(5,2) = 3$, $d(5,3) = 2$, $d(5,4) = 1$, $d(5,6) = 1$, $d(5,7) = 1$, $d(5,8) = 1$, $d(5,9) = 2$

$$C(5) = \frac{9 - 1}{3+3+2+1+1+1+1+2} = \frac{8}{14} \approx 0.57$$

- Tutti i nodi del grafo d'esempio:

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $C(i)$ | 0.35 | 0.35 | 0.47 | 0.57 | 0.57 | 0.57 | 0.47 | 0.44 | 0.33 |

- Massimo a pari merito: 4, 5, 6 (in rosso); il ponte 4 è centrale anche qui, il 7 (grado 4) scende a 0.47 perché è lontano dal triangolo
- Figura (networkpages.nl): il nodo nero al centro ha la closeness massima (0.40) e, se rimosso, spezza la rete in due componenti

### Farness (lontananza)
- La **farness** è la **somma delle distanze** da $i$ a tutti gli altri nodi:

$$F(i) = \sum_{j \neq i} d_{ij}, \qquad C(i) = \frac{n-1}{F(i)}$$

- È inversamente legata alla closeness: maggiore la farness, minore la closeness (Bavelas 1950)

### Pro e contro della closeness
| ✓ Pro | |
|---|---|
| Efficienza di accesso globale | Considera le distanze verso tutti i nodi: misura quanto un nodo è vicino al resto della rete |
| Interpretazione intuitiva | Alta closeness = pochi passaggi medi per raggiungere gli altri |
| Ottimale per la diffusione | Individua i nodi ben posizionati per raggiungere rapidamente molte parti della rete (spreader) |
| Considera l'intera rete | A differenza del degree non guarda solo i vicini diretti |

| ✗ Contro | |
|---|---|
| Problematica su grafi disconnessi | Con nodi irraggiungibili alcune distanze sono infinite e la definizione classica non funziona |
| Costo computazionale non banale | $O(n(n+m))$ con BFS, $O(n(m + n \log n))$ con Dijkstra: servono approssimazioni su reti con milioni di nodi |
| Non cattura il controllo del flusso | Un nodo vicino a tutti non è necessariamente un broker: non rileva colli di bottiglia né ponti |
| Poco discriminante su reti dense | Se le distanze medie sono simili, le differenze diventano minime |
| Non considera l'importanza dei nodi raggiunti | Essere vicino a nodi irrilevanti conta quanto essere vicino agli hub |

## Eigenvector centrality (centralità di autovettore)
- La degree è locale: conta solo quanti vicini ha un nodo. Un nodo può avere **poche connessioni ma verso nodi importanti**
- Idea: **l'importanza di un nodo dipende dall'importanza dei suoi vicini**
- Storia: l'idea nasce nel 1949 con il sociologo **John Seeley** (senza formalizzazione completa), **Phillip Bonacich** (1972) la sviluppa rigorosamente; precede sia PageRank sia HITS
- Esempio visivo: due nodi centrali con **lo stesso grado** (4); quello rosso è più importante perché i suoi vicini sono a loro volta hub

### Definizione
- A ogni nodo $i$ si assegna un punteggio $x_i$ proporzionale alla somma dei punteggi dei vicini:

$$x_i \propto \sum_j a_{ij} x_j$$

- $a_{ij}$ = elemento della matrice di adiacenza, $x_j$ = centralità del vicino $j$
- **Problema ricorsivo**: per conoscere l'importanza di un nodo serve quella dei vicini, che dipende dai loro vicini
- Introducendo la costante di proporzionalità $1/\lambda$:

$$x_i = \frac{1}{\lambda} \sum_j a_{ij} x_j \;\Longrightarrow\; \lambda x_i = \sum_j a_{ij} x_j \;\Longrightarrow\; A\mathbf{x} = \lambda \mathbf{x}$$

- È l'**equazione degli autovalori**: $\mathbf{x}$ è un **autovettore** di $A$ e $\lambda$ il corrispondente **autovalore**
- Significato di $A\mathbf{x} = \lambda\mathbf{x}$: la somma dei punteggi dei vicini di ogni nodo è proporzionale al punteggio del nodo stesso

### Esempio: cammino A - B - C
$$A = \begin{pmatrix} 0&1&0 \\ 1&0&1 \\ 0&1&0 \end{pmatrix}, \quad \mathbf{x} = \begin{pmatrix} x_a \\ x_b \\ x_c \end{pmatrix}, \quad A\mathbf{x} = \begin{pmatrix} x_b \\ x_a + x_c \\ x_b \end{pmatrix}$$

- $(A\mathbf{x})_a = x_b$: l'importanza di A dipende da quella del suo unico vicino B
- $(A\mathbf{x})_b = x_a + x_c$: l'importanza di B dipende dalla somma delle importanze dei suoi due vicini
- $(A\mathbf{x})_c = x_b$: l'importanza di C dipende da quella di B
- (Aggiunta, soluzione: gli autovalori sono $\sqrt{2}, 0, -\sqrt{2}$; l'autovettore dominante è $\mathbf{x} \propto (1, \sqrt{2}, 1)$, quindi B è $\sqrt{2} \approx 1.41$ volte più centrale di A e C.)

### Quale autovettore scegliere: Perron-Frobenius
- Una matrice $n \times n$ ha $n$ autovalori $\lambda_1 \geq \lambda_2 \geq \dots \geq \lambda_n$ e altrettanti autovettori che soddisfano l'equazione: quale usare come centralità?
- (La slide scrive "$n$ autovalori distinti", ma non è detto che siano distinti, e lo stesso "$\geq$" della slide ammette valori uguali. L'ordinamento ha senso perché la matrice di un grafo non orientato è simmetrica e ha autovalori reali.)
- **Teorema di Perron-Frobenius**: per una matrice di adiacenza **non negativa e irriducibile** (grafo connesso), il **massimo autovalore $\lambda_1$ è reale e positivo**, e l'autovettore associato si può scegliere con **tutte le componenti strettamente positive** ed è **unico a meno di un fattore moltiplicativo**
- La **eigenvector centrality** è quindi l'insieme delle componenti dell'**autovettore dominante**, quello associato a $\lambda_1$

### Power iteration
- Metodo numerico: si parte da $\mathbf{x}^{(0)} = (1, \dots, 1)$, si calcola ripetutamente $\mathbf{x} \leftarrow A\mathbf{x}$ e si normalizza, fino alla convergenza (quando le condizioni lo consentono)
- Codice R delle slide (grafo con archi 1-2, 1-3, 2-3, 2-4; normalizzazione per il massimo):

```r
library(igraph)
G <- graph(edges = c(1,2, 1,3, 2,3, 2,4), directed = FALSE)
A <- as_adjacency_matrix(G, sparse = FALSE)
n <- nrow(A)
x <- rep(1, n)
converged <- FALSE
for (iter in 1:100) {
  x_new <- as.vector(A %*% x)
  x_new <- x_new / max(x_new)
  cat(sprintf("%-12s %s\n", as.character(iter),
      paste(sprintf("%-6.3f", x_new), collapse = " ")))
  if (max(abs(x_new - x)) < 1e-6) {
    cat(sprintf("Convergenza raggiunta all'iterazione %d.\n", iter))
    converged <- TRUE
    break
  }
  x <- x_new   # aggiorno DOPO il controllo
}
```

- Iterazioni: start $(1, 1, 1, 1)$; iter 1 $(0.667, 1, 0.667, 0.333)$, cioè $A\mathbf{1} = (2, 3, 2, 1)$ diviso 3; iter 2 $(1, 1, 1, 0.600)$; iter 3 $(0.769, 1, 0.769, 0.385)$; ... **convergenza all'iterazione 36** con $(0.855, 1, 0.855, 0.461)$
- Il nodo 2 (grado 3) vale 1, i nodi 1 e 3 (grado 2, nel triangolo) 0.855, la foglia 4 vale 0.461

### Verifica con igraph
- Grafo d'esempio con nodi A, B, C, D (archi A-B, A-C, B-C, C-D: è lo stesso grafo, con C nel ruolo di hub):

```r
# install.packages("igraph")
library(igraph)
# 2. Eigenvector centrality (metodo integrato)
ec <- eigen_centrality(G)
print(ec$vector)
#         A         B         C         D
# 0.8546377 0.8546377 1.0000000 0.4608111

# 3. Verifica manuale con power iteration
A_mat <- as.matrix(as_adjacency_matrix(G))
x <- rep(1, vcount(G))
for (i in 1:100) {
  x <- A_mat %*% x
  x <- x / sqrt(sum(x^2)) }
print(x)        # A 0.5227207  B 0.5227207  C 0.6116285  D 0.2818452

# 4. Autovalori e autovettore dominante
eig <- eigen(A_mat)
print(eig$values)      # 2.1700865  0.3111078 -1.0000000 -1.4811943
print(eig$vectors[,1]) # -0.5227207 -0.5227207 -0.6116285 -0.2818452
```

- Power iteration e calcolo diretto danno **la stessa centralità, a meno di normalizzazione e segno**:
  - `eigen_centrality` scala in modo che il massimo valga 1 ($0.5227/0.6116 = 0.8546$)
  - la power iteration con norma euclidea dà il vettore di norma 1
  - `eigen` restituisce l'autovettore con segno negativo: un autovettore moltiplicato per $-1$ resta un autovettore
- $\lambda_1 = 2.17$ è il massimo autovalore, reale e positivo come previsto da Perron-Frobenius

## PageRank
- Domanda: si può misurare la qualità di una pagina web **non solo dal contenuto ma dalla struttura dei link**?
- Intuizione: **una pagina è importante se molte pagine importanti la linkano**. È una definizione circolare, dello stesso tipo ricorsivo dell'eigenvector centrality, e si risolve con gli autovettori
- Larry Page e Sergey Brin, *The anatomy of a large-scale hypertextual Web search engine*, Computer Networks and ISDN Systems 30 (1998) 107-117 (circa 26000 citazioni)

### Il modello del random surfer
- Un utente naviga il Web a caso; a ogni passo:
  - con probabilità $\alpha$ (tipicamente **0.85**) **segue un link** della pagina corrente
  - con probabilità $1 - \alpha$ si **teletrasporta**: digita una URL a caso e va su una pagina qualsiasi
- Con $\alpha = 0.85$: l'85% delle volte clicca un link, il 15% ignora i link e salta a caso ("moneta truccata")
- **Il PageRank di una pagina $i$ è la probabilità che il surfer si trovi su $i$ in un momento qualsiasi**

### Formula
$$PR(i) = \frac{1 - \alpha}{n} + \alpha \sum_{j \in N^{in}(i)} \frac{PR(j)}{k_j^{out}}$$

- $\alpha$ = **damping factor**, probabilità di seguire un link
- $\frac{1-\alpha}{n}$ = **componente di teletrasporto**: con probabilità $1-\alpha$ il surfer arriva su $i$ da qualsiasi pagina (uniforme sulle $n$ pagine)
- $\alpha \sum_{j \in N^{in}(i)} \frac{PR(j)}{k_j^{out}}$ = **componente di navigazione**: quanto PageRank arriva a $i$ attraverso i link delle altre pagine
  - $N^{in}(i)$ = insieme dei nodi che puntano verso $i$ ($j \to i$)
  - $PR(j)$ = PageRank del nodo $j$ che punta verso $i$
  - $k_j^{out}$ = numero di link uscenti da $j$: il PageRank di $j$ è **diviso equamente** tra i suoi link
- **PageRank come sistema di voto**: ogni nodo distribuisce il proprio prestigio ai nodi che collega, dividendolo tra tutti i link uscenti; un voto da un nodo importante vale più di un voto da un nodo poco importante, e un voto da un nodo che linka poche pagine vale più di uno da un nodo che ne linka molte
- **Proprietà fondamentale**: il PageRank è una **distribuzione di probabilità**, $\sum_{i=1}^{n} PR(i) = 1$
- (La somma vale 1 solo se i dangling node sono gestiti come nella sezione seguente: con la formula base, il PageRank che finisce su un nodo senza link uscenti non viene ridistribuito e la somma scende sotto 1.)

### Dangling node e spider trap
- **Dangling node**: pagina (o nodo di un grafo orientato) **senza archi uscenti**, non linka nessun'altra pagina; il surfer arriva e **rimane bloccato**
- **Spider trap**: gruppo di nodi che si linkano **solo tra loro**, senza archi uscenti verso il resto della rete; il surfer arriva e **non esce mai**, e il gruppo accumula tutto il PageRank (vale senza teletrasporto: è il teletrasporto con probabilità $1-\alpha$ a farlo uscire)
- Correzione per i dangling: il loro PageRank viene **redistribuito uniformemente** su tutti i nodi ($D$ = insieme dei dangling node):

$$PR(i) = \frac{1 - \alpha}{n} + \alpha \sum_{j \in N^{in}(i)} \frac{PR(j)}{k_j^{out}} + \frac{\alpha}{n} \sum_{j \in D} PR(j)$$

### Esempio svolto (Wikipedia / towardsdatascience)
- 11 nodi: B (38.4%), C (34.3%), E (8.1%), D (3.9%), F (3.9%), A (3.3%), cinque nodi viola (1.6% ciascuno); A è dangling
- Dimensione del nodo = importanza, frecce = hyperlink
- **C ha un PageRank altissimo pur ricevendo un solo link**, perché quel link viene da B, la pagina più importante, che linka solo C
- Calcolo con $n = 11$, $\alpha = 0.85$, termine base $\frac{1 - 0.85}{11} = 0.01364$:

$$PR(C) = 0.013636 + 0.85\left[PR(B) + \frac{PR(A)}{11}\right] = 0.013636 + 0.85\left[0.384 + \frac{0.033}{11}\right] \approx 0.3426 = 34.26\%$$

$$PR(A) = 0.013636 + 0.85\left[\frac{PR(D)}{2} + \frac{PR(A)}{11}\right]$$

- B ha un solo link uscente (verso C), quindi passa a C tutto il suo PageRank; $PR(A)/11$ è il termine dangling
- (Nella formula di $PR(A)$ il nodo D ha due link uscenti, ma nel disegno della slide D ha solo la freccia verso A; il secondo link uscente di D non è disegnato.)
- Nella slide di appendice lo stesso grafo è rietichettato (A = 38.4, C = 34.3, B = 8.1, D ed E = 3.9, F = 3.3 dangling, $G_1 \dots G_5$ = 1.6) e sono scritte tutte le equazioni, es.

$$PR(A) = 0.01364 + 0.85\left[5 \cdot \frac{PR(G)}{2} + \frac{PR(B)}{3} + \frac{PR(E)}{2} + PR(C) + \frac{PR(F)}{11}\right], \quad PR(G_i) = 0.01364 + 0.85\,\frac{PR(F)}{11}$$

- I nodi $G_i$ non ricevono link: hanno solo teletrasporto e quota dangling
- Esempio a 14 nodi (A ... N): all'inizio dell'iterazione ogni nodo ha $PR^{(0)}(i) = 1/14 \approx 0.0714$ (distribuzione uniforme), poi si itera fino alla convergenza

### Applicazione: food web (Allesina & Pascual 2009)
- *Googling Food Webs: Can an Eigenvector Measure Species' Importance for Coextinctions?* (PLoS Computational Biology): un algoritmo derivato da PageRank ordina le specie per importanza nelle **coestinzioni**
- Grafico: frazione di specie estinte in funzione della frazione rimossa, per due ordini di rimozione (blu e rosso): con quello blu la rete collassa molto prima
- Tabella su 12 food web (da 25 a 124 specie): confronto tra le strategie che rimuovono per primo il massimo di degree (Max. D), closeness (Max. CLOS), betweenness (Max. BETW), dominatori (Max. DOM), due varianti dell'autovettore (Max. EIG1, Max. EIG2) e un algoritmo genetico (GA)
- Le colonne EIG1/EIG2 coincidono quasi sempre con GA (es. benguela 0.9798, skipwith 1.0000) e superano degree, closeness e betweenness (le slide non spiegano cosa misurino i valori: il confronto è fra colonne)

## Strength centrality (grado pesato)
- **Strength** = **somma dei pesi dei link** verso i primi vicini:

$$s_i = \sum_{j=1}^{n} w_{ij}$$

- $w_{ij}$ = peso dell'arco tra $i$ e $j$, con $w_{ij} = 0$ se l'arco non esiste; in una rete binaria $s_i = k_i$
- Esempio sul grafo d'esempio pesato (8-5: 1, 8-7: 3, 8-6: 2, 5-7: 1, 5-6: 1, 5-4: 1, 7-6: 5, 7-9: 2, 6-4: 1, 4-3: 3, 3-1: 2, 3-2: 1, 1-2: 5):

| Nodo | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
|---|---|---|---|---|---|---|---|---|---|
| $k_i$ | 2 | 2 | 3 | 3 | 4 | 4 | 4 | 3 | 1 |
| $s_i$ | 7 | 6 | 6 | 5 | 4 | 9 | 11 | 6 | 2 |

- Es. $s_7 = 3 + 1 + 5 + 2 = 11$, $s_5 = 1 + 1 + 1 + 1 = 4$: il nodo 5 ha grado massimo ma strength minima fra i nodi del blocco, mentre 1 e 2 (grado 2) superano 5 grazie all'arco forte 1-2 di peso 5
- **Grafi orientati**: come per il grado si distinguono

$$s_i^{in} = \sum_j w_{ji}, \qquad s_i^{out} = \sum_j w_{ij}$$

- Figura: lo stesso grafo a 4 nodi, prima binario e non orientato, poi pesato e orientato, con pesi diversi nelle due direzioni dello stesso legame (es. 0.4 e 0.7 fra B e D)

### Degree vs strength (e le altre misure)
- Figura dalla review di Bellingeri et al. (2023), rete pesata a 7 nodi: 1-2 (1), 2-6 (2), 6-5 (6), 5-7 (1), 2-3 (4), 3-4 (6), 4-5 (8)
- Degree massima: nodi 2 e 5 (grado 3); **strength massima: nodi 4 e 5** ($s_4 = 6 + 8 = 14$, $s_5 = 8 + 6 + 1 = 15$)
- Considerare i pesi cambia la classifica dei nodi: è il messaggio di tutta la seconda parte del modulo

## Distanza pesata
- In un grafo binario $d_{ij}$ conta gli archi; in un grafo pesato bisogna decidere **come i pesi entrano nella distanza**
- Esempio: $i$ e $j$ a distanza binaria 2, ma il cammino diretto può avere archi deboli e quello lungo archi forti: $d_{ij}^w = ?$
- Grafo d'esempio pesato: $i$-L1 (1), L1-L2 (1), L2-b (1), $i$-a (4), a-T (2), T-R (1), T-b (1), R-b (1), a-b (8), b-c (4), c-$j$ (3); il cammino binario minimo è $i$-a-b-c-$j$ (4 link, $d_{ij} = 4$)

### Pesi come distanze o costi (remoteness)
- **Peso più alto = nodi più lontani** (km, tempo, costo, resistenza): la distanza è la somma dei pesi

$$d_{ij}^w = \min_{\text{path } P} \sum_{(i,j) \in P} w_{ij}$$

- Cammini confrontati nelle slide:
  - $i$-a-T-R-b-c-$j$: $4 + 2 + 1 + 1 + 4 + 3 = 15$
  - $i$-a-b-c-$j$ (il cammino minimo binario): $4 + 8 + 4 + 3 = 19$ (la slide scrive 17, ma la somma è 19)
  - $i$-L1-L2-b-c-$j$: $1 + 1 + 1 + 4 + 3 = 10$, **il minimo**
- Il cammino minimo pesato ha 5 archi, uno più del cammino minimo binario: con i pesi il "più corto" cambia

### Pesi come flussi, capacità o vicinanza (proximity)
- **Peso più alto = nodi più vicini** (relazione forte): un arco di peso alto deve contribuire **poco** alla distanza, come se fosse un arco "corto". Si usa l'**inverso del peso**:

$$d_{ij}^w = \min_{\text{path } P} \sum_{(i,j) \in P} \frac{1}{w_{ij}}$$

- Cammini confrontati nelle slide:
  - $i$-a-T-R-b-c-$j$: $\frac{1}{4} + \frac{1}{2} + 1 + 1 + \frac{1}{4} + \frac{1}{3} = \frac{10}{3} \approx 3.33$
  - $i$-L1-L2-b-c-$j$: $1 + 1 + 1 + \frac{1}{4} + \frac{1}{3} = \frac{43}{12} \approx 3.583$
- Le slide concludono che con i pesi come vicinanza vince il cammino da $10/3$ invece di quello che era minimo con i pesi come costi: lo stesso grafo dà cammini minimi diversi a seconda dell'interpretazione dei pesi
- (Il confronto delle slide trascura il cammino attraverso l'arco più forte: $i$-a-b-c-$j$ vale $\frac{1}{4} + \frac{1}{8} + \frac{1}{4} + \frac{1}{3} = \frac{23}{24} \approx 0.958$, molto meno di $10/3$, ed è il vero cammino minimo con pesi come vicinanza, verificato con Dijkstra in NetworkX. Il risultato va anzi a rinforzo dell'idea della slide: l'arco 8, il più "lungo" con i pesi come costi, diventa il più "corto".)

### Proximity vs remoteness nelle reti reali
- Bellingeri M. et al. (2023), *Considering weights in real social networks: A review*, Front. Phys. 11:1152243
- **Proximity**: peso alto = nodi più vicini (capacità, flusso, intensità). **Remoteness**: peso alto = nodi più lontani (costo, distanza, resistenza)
- Reti sociali pesate:

| Rete | Nodi | Peso del link | Tipo |
|---|---|---|---|
| Chiamate telefoniche | Persone | Durata della chiamata | Proximity |
| Co-authorship scientifico | Ricercatori | N. di paper co-firmati | Proximity |
| Email aziendali | Dipendenti | N. di email scambiate | Proximity |
| Amicizia (survey) | Individui | Forza dichiarata dell'amicizia | Proximity |
| Attori cinema (IMDb) | Attori | N. di film insieme | Proximity |
| Bitcoin trust network | Trader | Livello di fiducia | Proximity |
| Rating online dating | Utenti | Voto dato (1-10) | Proximity |
| Reti criminali | Criminali | N. di incontri/collaborazioni | Proximity |
| Face-to-face (sensori) | Individui | Tempo di interazione | Proximity |
| Board of Directors | Manager | N. di comemberships | Proximity |
| Risposta email (lavoro) | Dipendenti | Tempo di risposta | Remoteness |
| Amicizia fisica | Individui | Distanza geografica | Remoteness |
| Amicizia (troubled) | Studenti | Livello di conflitto | Remoteness |
| Relazioni di lavoro | Dipendenti | N. di atti antagonistici | Remoteness |
| Reti epidemiche | Persone | Probabilità di infezione | Proximity |

- Reti non sociali pesate (la stessa rete cambia tipo a seconda del peso scelto):

| Dominio | Rete | Nodi | Peso del link | Tipo |
|---|---|---|---|---|
| Trasporti | Rete aerea | Aeroporti | N. di voli giornalieri | Proximity |
| Trasporti | Rete aerea (percorrenza) | Aeroporti | Tempo di volo | Remoteness |
| Trasporti | Rete stradale | Incroci/città | Distanza chilometrica | Remoteness |
| Trasporti | Rete stradale (capacità) | Incroci/città | N. di corsie × velocità massima | Proximity |
| Biologia | Protein-protein interaction | Proteine | Forza dell'interazione | Proximity |
| Biologia | Rete metabolica | Metaboliti | Costo energetico della reazione | Remoteness |
| Biologia | Co-espressione genica | Geni | Correlazione di espressione | Proximity |
| Ecologia | Food web | Specie | Biomassa trasferita (predazione) | Proximity |
| Ecologia | Rete di impollinazione | Piante/insetti | Frequenza di visita | Proximity |
| Infrastrutture | Power grid | Stazioni | Capacità di trasmissione (MW) | Proximity |
| Infrastrutture | Power grid (resistenza) | Stazioni | Resistenza elettrica del cavo | Remoteness |
| Tecnologia | Internet / router | Router | Banda disponibile | Proximity |
| Tecnologia | Internet (latenza) | Router | Latenza di trasmissione | Remoteness |
| Finanza | Rete interbancaria | Banche | Volume di scambi/prestiti | Proximity |
| Finanza | Rete di rischio | Banche | Spread di rischio / costo prestito | Remoteness |
| Gastronomia | Flavor network | Ingredienti | N. composti aromatici condivisi | Proximity |
| Gastronomia | Recipe network | Ricette | N. ingredienti condivisi | Proximity |

### Algoritmo di Dijkstra
- Calcola la **distanza pesata** $d_{ij}^w$: il peso minimo totale per andare da $i$ a $j$, con **pesi non negativi**
- Dijkstra originale (1959): $O(n^2)$; versione con **heap binario**: $O(m \log n)$
- **BFS minimizza il numero di archi; Dijkstra minimizza la somma delle lunghezze degli archi**

## Betweenness pesata
$$g^w(i) = \sum_{s,t} \frac{\sigma_{st}^w(i)}{\sigma_{st}^w}$$

- $\sigma_{st}^w$ = numero di **cammini minimi pesati** tra $s$ e $t$; $\sigma_{st}^w(i)$ = quanti di essi passano per $i$
- Stessa struttura della binaria, ma i cammini minimi sono calcolati con le distanze pesate (Dijkstra)
- **Passare dalla BC binaria a quella pesata può cambiare radicalmente l'importanza dei nodi**
- Rete a 7 nodi della review, **pesi come distanze** (remoteness):
  - BC binaria massima: nodi **2 e 5** (valori grezzi 6 e 6)
  - BC pesata massima: nodi **2 e 6** (valori grezzi 9 e 6): il cammino 2-6-5 (peso 8) batte 2-3-4-5 (peso 18), quindi i flussi passano per 6 e non più per 3 e 4
- (Le formule delle slide scrivono la somma come $\sum_{s,t=1}^{N}$ senza escludere $s = t$ e $s = i$ o $t = i$: vanno lette con le stesse esclusioni della betweenness binaria.)

## Closeness pesata
- La weighted closeness di un nodo $i$ è l'inverso della distanza media pesata da $i$ a tutti gli altri (la slide scrive "di un nodo $j$", ma è il nodo $i$):

$$C^w(i) = \frac{n - 1}{\sum_{j \neq i} d_{ij}^w}$$

- $d_{ij}^w$ = distanza minima pesata; **più bassa è la distanza media pesata, maggiore la closeness**
- **Esempio svolto, nodo 4** della rete a 7 nodi (pesi come distanze); il percorso scelto deve essere uno **shortest path**:
  - $d_w(4,3) = 6$
  - $d_w(4,5) = 8$
  - $d_w(4,2) = d_w(4,3) + d_w(3,2) = 6 + 4 = 10$
  - $d_w(4,6) = \min(d_w(4,2) + 2,\ d_w(4,5) + 6) = \min(12, 14) = 12$
  - $d_w(4,1) = d_w(4,2) + 1 = 11$
  - $d_w(4,7) = d_w(4,5) + 1 = 9$

$$\sum_{j \neq 4} d_w(4,j) = 6 + 8 + 10 + 12 + 11 + 9 = 56, \qquad C^w(4) = \frac{6}{56} \approx 0.107$$

- **Closeness binaria del nodo 4**: $d(4,3) = 1$, $d(4,5) = 1$, $d(4,2) = 2$ (4-3-2), $d(4,6) = 2$ (4-5-6), $d(4,7) = 2$ (4-5-7), $d(4,1) = 3$ (4-3-2-1)

$$\sum_{j \neq 4} d(4,j) = 11, \qquad C(4) = \frac{6}{11} \approx 0.545$$

- Classifica di tutti i nodi:

| Nodo | Closeness binaria | Rank binario | Closeness pesata | Rank pesato |
|---|---|---|---|---|
| 1 | 0.400 | 6° | 0.154 | 3° |
| 2 | 0.600 | 1° | 0.176 | 1° |
| 3 | 0.545 | 4° | 0.130 | 5° |
| 4 | 0.545 | 4° | 0.107 | 7° |
| 5 | 0.600 | 1° | 0.136 | 4° |
| 6 | 0.600 | 1° | 0.167 | 2° |
| 7 | 0.400 | 6° | 0.122 | 6° |

- **Considerare i pesi modifica le distanze minime e quindi la closeness**: il nodo 4 passa da 4° a ultimo (i suoi archi sono i più "lunghi", 6 e 8), il nodo 1 da 6° a 3° (è attaccato a 2 con un arco corto)
- Le posizioni ex aequo condividono lo stesso rango; valori verificati con NetworkX
- (La figura della review evidenzia per la closeness binaria solo i nodi 2 e 6, ma secondo la tabella anche il nodo 5 vale 0.600 ed è primo a pari merito.)

## Slide di appendice
- Dopo la slide finale ci sono quattro slide di riepilogo:
  - le equazioni complete del PageRank con termine dangling (riportate sopra)
  - due volte la closeness del grafo d'esempio (0.57 per 4, 5, 6)
  - una slide intitolata "Centralità di vicinanza" che riporta invece i valori della **betweenness normalizzata** (0.54 per il nodo 4, 0.43 per il 3, ecc.: è la betweenness, il titolo è sbagliato)

## Funzioni per il progetto (aggiunta)
Le slide mostrano solo codice R/igraph per l'autovettore; questi sono i corrispondenti in NetworkX e igraph delle misure del modulo.

| Misura | NetworkX (Python) | igraph (R) |
|---|---|---|
| Grado / in / out | `G.degree()`, `G.in_degree()`, `G.out_degree()` | `degree(G, mode = "all" / "in" / "out")` |
| Strength | `G.degree(weight="weight")` | `strength(G)` |
| Distanza | `nx.shortest_path_length(G, s, t, weight=...)` | `distances(G)` |
| Betweenness | `nx.betweenness_centrality(G, weight=...)` | `betweenness(G)` |
| Closeness | `nx.closeness_centrality(G, distance=...)` | `closeness(G)` |
| Eigenvector | `nx.eigenvector_centrality(G)` | `eigen_centrality(G)$vector` |
| PageRank | `nx.pagerank(G, alpha=0.85)` | `page_rank(G, damping = 0.85)$vector` |

- In entrambe le librerie il peso usato per cammini minimi, betweenness e closeness è interpretato come **distanza (remoteness)**: se i pesi del dataset sono di tipo proximity (voli, interazioni, co-firme) bisogna prima creare un attributo con $1/w$ e passare quello, altrimenti i nodi "forti" risultano lontani
- `nx.betweenness_centrality` normalizza di default (`normalized=True`), come i valori 0.54, 0.43 delle slide
