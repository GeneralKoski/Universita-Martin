# Proprietà globali della rete (Modulo 5)

Fonte: `Proprietà Globali della Rete - Modulo 5.pdf`, versione ricaricata dal docente il 22/10/2026 (131 pagine; la prima era di 117)

## Componenti connesse

### Componente connessa
- Un sottoinsieme $S \subseteq V$ è una **componente connessa** se ogni nodo in $S$ è **raggiungibile** da ogni altro nodo in $S$ e **nessun nodo** di $S$ è connesso a nodi fuori da $S$
- Rete **connessa**: una sola componente. Rete **disconnessa**: due o più componenti, isolate tra loro (figura: la stessa rete prima e dopo la rimozione di alcuni link, che la spezza in più pezzi)

### Componente gigante (GCC)
- Nelle reti reali grandi esiste quasi sempre una componente che contiene la **maggioranza dei nodi**: la **componente gigante** (*giant connected component*, GCC), cioè la componente connessa con il maggior numero di nodi
- Taglia, con $c_j$ la componente connessa $j$:

$$GC = \max_j |c_j|$$

- Spesso si usa il valore **normalizzato** sul numero di nodi $N$:

$$S = \frac{\max_j |c_j|}{N} \in (0, 1]$$

- Esempio delle slide: rete di 38 nodi connessa → $S = 38/38 = 1$; dopo la frammentazione la GCC ha 24 nodi → $S = 24/38 \approx 0{,}63$
- **Misura di funzionalità del sistema**: nell'analisi di **robustezza** si rimuovono nodi e si segue $S$ in funzione della frazione rimossa
  - Figura (doi 10.3389/fphy.2022.823564): proporzione di nodi nella GCC vs proporzione di nodi rimossi. Il **random attack** fa crollare la GCC solo verso l'83% di rimozioni, il **viral attack** verso il 34%, il **targeted attack** già verso il 21%
  - Figura (Physica A, S0378437114005603): reti ER ($N=500$, $p=0{,}008$), CM ($N=500$, $\alpha=2{,}5$, $\langle k \rangle = 3{,}8$) e BA ($N=500$, $m=2$) attaccate con varie strategie (First, Sec, F+S, Comb, Bet; Bet = betweenness, le altre non sono spiegate nelle slide). Nella ER la GCC cala gradualmente fino a circa 0,4-0,5 di nodi rimossi; nelle reti **eterogenee** (CM, BA) le strategie migliori la distruggono già con circa il 10% dei nodi

### Grafi orientati: WCC e SCC
- **Componente debolmente connessa** (*Weakly Connected Component*, WCC): sottoinsieme **massimale** di nodi che risultano connessi **ignorando la direzione** degli archi. I nodi possono stare nella stessa WCC pur **non essendo reciprocamente raggiungibili** seguendo le frecce
- **Componente fortemente connessa** (*Strongly Connected Component*, SCC): sottoinsieme massimale di nodi in cui **ogni nodo è raggiungibile da qualsiasi altro seguendo la direzione** degli archi. Per ogni coppia $i, j$ nella stessa SCC devono esistere

$$i \rightsquigarrow j \quad \text{e} \quad j \rightsquigarrow i$$

  dove $\rightsquigarrow$ indica l'esistenza di un **cammino orientato**
- Esempio delle slide (7 nodi; archi $4\to1$, $1\to2$, $2\to4$, $2\to3$, $3\to4$, $4\to5$, $3\to6$, più un ciclo orientato fra 5, 6 e 7): una sola WCC $\{1,\dots,7\}$, ma due SCC: $\{1,2,3,4\}$ e $\{5,6,7\}$. Dal primo gruppo si arriva al secondo (archi $4\to5$, $3\to6$) ma non si torna indietro
- Altra figura (Wikipedia): grafo $a \dots h$ con le SCC ombreggiate $\{a,b,e\}$, $\{c,d,h\}$, $\{f,g\}$; algoritmo citato: **Kosaraju**

### Applicazioni delle SCC
1. **Reti stradali con sensi unici**: nodi = incroci, archi = strade percorribili in una direzione. Una WCC può comprendere tutta una città; una SCC identifica le zone in cui ci si può spostare tra tutti gli incroci **e tornare al punto di partenza**. Applicazione: navigazione e accessibilità stradale
2. **World Wide Web**: nodi = pagine, archi = hyperlink. Due pagine nella stessa WCC possono non essere reciprocamente raggiungibili; la SCC individua gruppi di pagine tra cui si naviga **in entrambe le direzioni**, anche per percorsi diversi. Applicazione: struttura del Web, motori di ricerca
3. **Reti di distribuzione con flussi direzionali**: nodi = serbatoi o stazioni, archi = collegamenti che permettono un flusso in una direzione. La SCC individua nodi reciprocamente raggiungibili con percorsi consentiti. Applicazione: circolazione e **ridondanza dei percorsi**, purché la direzione degli archi rappresenti davvero i flussi possibili
4. **Dipendenze software**: nodi = moduli, archi = dipendenze dirette. Una SCC identifica gruppi di moduli con **dipendenze circolari**, anche indirette, che complicano manutenzione, test e aggiornamenti

### LWCC e LSCC
- **LWCC** (*Largest Weakly Connected Component*, in figura anche **GWCC**): la WCC con il maggior numero di nodi; può contenere nodi non reciprocamente raggiungibili

$$LWCC = \max_j (n_j), \qquad n_j = \text{numero di nodi della componente } j$$

- **LSCC** (*Largest Strongly Connected Component*; le slide la intitolano "Largest Strongest Connected Component", il termine corretto è *strongly*): la SCC con il maggior numero di nodi. Tutti i suoi nodi sono reciprocamente raggiungibili seguendo le frecce
- Esempio (10 nodi, i 7 di prima più $8 \to 9$ e il nodo isolato 10): LWCC = $\{1,\dots,7\}$; LSCC = $\{1,2,3,4\}$, poi SCC $\{5,6,7\}$ e $\{10\}$. (La figura etichetta $\{8, 9\}$ come una SCC, ma c'è solo l'arco $8 \to 9$: da 9 non si torna a 8, quindi le SCC sono $\{8\}$ e $\{9\}$ separate; $\{8,9\}$ è invece una WCC)
- Esperimento in R/igraph: random graph orientato $N=500$, $p=0{,}02$, rimozione casuale (**errore**) vs **attacco**:

```r
library(igraph)
set.seed(42)
n <- 500
p <- 0.02
G <- erdos.renyi.game(n, p, type = "gnp", directed = TRUE)
```

  - Sotto attacco la **LSCC crolla prima** (circa 0,5-0,6 di nodi rimossi) della LWCC (circa 0,65-0,7); con la rimozione casuale la LWCC resta quasi intera fino a 0,8 mentre la LSCC comincia a calare verso 0,7
- **Se la direzione dei link è importante, nell'analisi di robustezza bisogna considerare la SCC** (rif. *Optimal dismantling of directed networks*, Nature Communications 2026: nelle reti orientate la SCC gigante cattura la raggiungibilità mutua che sostiene la funzionalità del sistema)

## Distanze: diametro e distanza media

### Motivazione e distanza tra nodi
- Nel Modulo 4 la distanza $d_{ij}$ serviva per closeness e betweenness; ora si guarda la rete **nel suo insieme**: qual è la distanza **massima** possibile? quanto sono distanti i nodi **in media**? Sono le prime due proprietà globali che descrivono la **comunicazione strutturale** della rete
- **Distanza** $d_{ij}$: lunghezza del **cammino minimo** (*shortest path*) tra $i$ e $j$. Esempio: tra $i$ e $j$ esistono un cammino di 6 link e uno di 4 link → $d_{ij} = 4$

### Diametro
- Il **diametro** è la distanza massima tra qualsiasi coppia di nodi:

$$D = \max_{i,j} d_{ij}$$

- Risponde a: nel **caso peggiore**, quanti passi servono per andare da un nodo a qualsiasi altro? Misura l'**estensione massima** della rete, quanto è "larga" nella sua dimensione più sfavorevole
- Esempio (transportgeography.org): 7 nodi, archi 1-2, 1-3, 1-6, 2-4, 4-6, 3-5, 5-6, 5-7. La **Shimbel distance** è la matrice delle lunghezze dei cammini minimi:

| v | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|
| **1** | 0 | 1 | 1 | 2 | 2 | 1 | 3 |
| **2** | 1 | 0 | 2 | 1 | 3 | 2 | **4** |
| **3** | 1 | 2 | 0 | 3 | 1 | 2 | 2 |
| **4** | 2 | 1 | 3 | 0 | 2 | 1 | 3 |
| **5** | 2 | 3 | 1 | 2 | 0 | 1 | 1 |
| **6** | 1 | 2 | 2 | 1 | 1 | 0 | 2 |
| **7** | 3 | **4** | 2 | 3 | 1 | 2 | 0 |

  → $D = \max_{i,j} d_{ij} = d_{2,7} = 4$

### Diametro nei grafi disconnessi
- Se la rete non è connessa esistono coppie con $d_{ij} = \infty$, quindi $D = \max_{i,j} d_{ij} = \infty$ se si considerano anche le coppie non raggiungibili
- Soluzioni pratiche:
  - calcolare il diametro sulla **componente connessa più grande** (la scelta abituale)
  - considerare solo le **coppie raggiungibili**, prendendo il massimo delle distanze finite
  - studiare **separatamente** il diametro delle diverse componenti

### Eccentricità
- **Eccentricità** del nodo $i$: distanza massima da $i$ verso qualsiasi altro nodo

$$ecc(i) = \max_j (d_{ij})$$

- È il raggio dell'**anello più esterno** raggiungibile da $i$ (figura: anelli concentrici di distanza crescente attorno a $i$), cioè la distanza topologica dell'anello più esterno rispetto al nodo
- (Aggiunta: il diametro è la massima eccentricità, $D = \max_i ecc(i)$; la minima eccentricità è il **raggio** del grafo)

### Distanza e diametro pesati
- In una rete pesata $d^w_{ij}$ è la lunghezza del cammino minimo **pesato** (somma dei pesi lungo il cammino)
- Esempio delle slide: il cammino evidenziato vale $d^w_{ij} = 4 + 2 + 1 + 1 + 4 + 3 = 15$. (Errore nella slide: con i pesi della figura il cammino lungo il bordo inferiore, $1 + 1 + 1 + 4 + 3 = 10$, è più corto, quindi $d^w_{ij} = 10$. Il cammino di 4 link evidenziato in blu, cioè il cammino minimo binario, pesa invece $4 + 8 + 4 + 3 = 19$: il cammino con meno hop non è in generale quello di peso minimo)
- **Diametro pesato**: $D^w = \max_{i,j} d^w_{ij}$
- Significato dei pesi, distinzione cruciale:
  - pesi = **costi/distanze** (*remoteness*): si usano direttamente $w_{ij}$
  - pesi = **forza/intensità** (*proximity*, es. flussi): prima si trasformano in lunghezze con $w'_{ij} = 1/w_{ij}$, così un legame forte diventa "corto"
- Esempio binario vs pesato (Wikipedia): nella stessa rete $D = 5$ (numero di archi) tra due nodi esterni, mentre $D^w = 28$ (somma delle lunghezze, $11 + 1 + 2 + 2 + 12$) tra un'altra coppia di nodi: le coppie che realizzano il diametro possono cambiare

### Distanza media
- **Distanza media**: media delle lunghezze dei cammini minimi tra tutte le coppie di nodi

$$\bar{d} = \frac{1}{n(n-1)} \sum_{i \neq j} d_{ij}$$

- $n(n-1)$ = numero di **coppie ordinate** di nodi distinti. Nelle reti binarie conta il numero medio di **hop**
- Versione **pesata**, con $d^w_{ij}$ calcolato su $w_{ij}$ (remoteness) o su $w'_{ij} = 1/w_{ij}$ (proximity):

$$\overline{d^w} = \frac{1}{n(n-1)} \sum_{i \neq j} d^w_{ij}$$

### Grafi non connessi: distanze infinite
- Esempio: grafo di 10 nodi con 3 componenti (5, 3 e 2 nodi). La matrice delle distanze ha valori finiti dentro ogni componente e **Inf** tra nodi di componenti diverse, quindi $\bar d$ e $D$ diventano infiniti
- **Esperimento**: random graph $N = 1000$ al variare di $p$, con $\bar d$ e $D$ calcolati sulla **componente connessa più grande** (LCC):

```r
p_values <- c(0, 0.0005, 0.001, 0.0015, 0.002, 0.003, 0.004,
              0.005, 0.006, 0.007, 0.008, 0.009, 0.01, 0.02, 0.05, 0.1)
gcc_nodi <- which(comp$membership == which.max(comp$csize))
G_gcc    <- induced_subgraph(G, gcc_nodi)
d_media  <- mean_distance(G_gcc, directed = FALSE)
diam     <- diameter(G_gcc, directed = FALSE)
```

  (`comp` non è definito nelle slide: è il risultato di `components(G)`)

| $p$ | grado medio | n. componenti | taglia GCC | dist. media | diametro |
|---|---|---|---|---|---|
| 0 | 0,000 | 1000 | 1 | NA | NA |
| 0,0005 | 0,458 | 771 | 9 | 2,667 | 5 |
| 0,001 | 0,952 | 524 | 69 | 8,556 | 21 |
| 0,0015 | 1,552 | 278 | 620 | **11,672** | **31** |
| 0,002 | 1,886 | 189 | 744 | 9,538 | 25 |
| 0,003 | 3,034 | 49 | 948 | 6,222 | 13 |
| 0,004 | 4,046 | 22 | 979 | 5,053 | 11 |
| 0,005 | 5,120 | 6 | 995 | 4,398 | 8 |
| 0,006 | 5,982 | 3 | 998 | 4,055 | 8 |
| 0,007 | 7,158 | 1 | 1000 | 3,735 | 7 |
| 0,008 | 7,874 | 1 | 1000 | 3,579 | 7 |
| 0,009 | 9,146 | 1 | 1000 | 3,365 | 6 |
| 0,01 | 9,976 | 1 | 1000 | 3,259 | 5 |
| 0,02 | 20,010 | 1 | 1000 | 2,639 | 4 |
| 0,05 | 49,600 | 1 | 1000 | 2,031 | 3 |
| 0,1 | 99,458 | 1 | 1000 | 1,900 | 3 |

- Grafico: la distanza media sale bruscamente subito dopo $p = 1/n$ (linea rossa), ha il picco a $p = 0{,}0015$ e poi decresce
- **Se distanza media o diametro fossero misure di funzionalità, il comportamento sarebbe non coerente**: con $p$ piccolissimo la rete è quasi tutta frammentata ma la LCC è minuscola e ha distanze brevi, quindi sembrerebbe "più efficiente" di una rete molto più connessa
- **Rimozione di nodi** su random graph (errore vs attacco): la taglia della GCC cala in modo monotono (sotto attacco crolla verso 0,5-0,55 di nodi rimossi), mentre distanza media e diametro della GCC **prima crescono e poi crollano** quando la GCC si frammenta. Stesso problema: una rete distrutta apparirebbe "migliorata"

### Grafi orientati e pesati: matrici delle distanze
- Nei grafi orientati gli shortest path devono **rispettare la direzione** degli archi
- Grafo di esempio (6 nodi), edge list: $A\to B = 4$, $A\to C = 2$, $B\to C = 5$, $B\to D = 10$, $C\to E = 3$, $E\to D = 4$, $D\to F = 11$
- **Matrice dei pesi**: righe = nodi di partenza, colonne = destinazione, valori = pesi degli archi orientati, zeri = assenza di arco
- **Binaria e non diretta**:

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0 | 1 | 1 | 2 | 2 | 3 |
| **B** | 1 | 0 | 1 | 1 | 2 | 2 |
| **C** | 1 | 1 | 0 | 2 | 1 | 3 |
| **D** | 2 | 1 | 2 | 0 | 1 | 1 |
| **E** | 2 | 2 | 1 | 1 | 0 | 2 |
| **F** | 3 | 2 | 3 | 1 | 2 | 0 |

  (Aggiunta: $\bar d = 50/30 \approx 1{,}667$)
- **Binaria e diretta**: la matrice non è più simmetrica e compaiono gli $\infty$ (es. da B non si raggiunge A, da D si raggiunge solo F); riga A: 0, 1, 1, 2, 2, 3; riga E: $\infty, \infty, \infty$, 1, 0, 2
- **Pesata e non diretta, pesi = costi**:

| | A | B | C | D | E | F |
|---|---|---|---|---|---|---|
| **A** | 0 | 4 | 2 | 9 | 5 | 20 |
| **B** | 4 | 0 | 5 | 10 | 8 | 21 |
| **C** | 2 | 5 | 0 | 7 | 3 | 18 |
| **D** | 9 | 10 | 7 | 0 | 4 | 11 |
| **E** | 5 | 8 | 3 | 4 | 0 | 15 |
| **F** | 20 | 21 | 18 | 11 | 15 | 0 |

  es. $d_{AD} = 9$ via $A \to C \to E \to D$ ($2 + 3 + 4$), non l'arco diretto più "corto" in hop $A - B - D$ ($4 + 10 = 14$)
- **Pesata e non diretta, pesi = prossimità/flussi** ($w' = 1/w$): es. $d_{AB} = 0{,}250$, $d_{AC} = 0{,}450$ (via B: $0{,}25 + 0{,}2$, meglio dell'arco diretto $1/2$), $d_{AD} = 0{,}350$, $d_{AF} = 0{,}441$, $d_{DF} = 0{,}091$. (Errore nella slide: nella matrice non orientata compaiono $d_{AE} = 0{,}783$ e $d_{BE} = 0{,}533$, che sono i valori del caso **orientato**; senza direzione si può passare da $D - E$, quindi $d_{AE} = 0{,}25 + 0{,}1 + 0{,}25 = 0{,}600$ e $d_{BE} = 0{,}1 + 0{,}25 = 0{,}350$)
- **Pesata e diretta, costi** (output R `print(D_w)`): riga A: 0, 4, 2, 9, 5, 20; riga B: Inf, 0, 5, 10, 8, 21; riga C: Inf, Inf, 0, 7, 3, 18; riga D: solo $d_{DF} = 11$; riga E: $d_{ED} = 4$, $d_{EF} = 15$
- **Pesata e diretta, prossimità** (`print(round(D_flussi, 3))`, shortest path su $w'_{ij} = 1/w_{ij}$): riga A: 0, 0,25, 0,45, 0,350, 0,783, 0,441; riga B: Inf, 0, 0,20, 0,100, 0,533, 0,191; riga C: Inf, Inf, 0, 0,583, 0,333, 0,674; riga D: solo $d_{DF} = 0{,}091$; riga E: $d_{ED} = 0{,}250$, $d_{EF} = 0{,}341$

## Efficienza

### Efficienza globale
- **Problema**: su reti disconnesse le coppie irraggiungibili hanno $d_{ij} = \infty$ e la distanza media diventa infinita (es. $\sum_{i \neq j} d_{ij} = 1 + 3 + \infty$)
- **Efficienza globale** (Latora e Marchiori, *Efficient Behavior of Small-World Networks*, PRL 87, 198701, 2001): media degli **inversi** delle distanze minime

$$E_{glob} = \frac{1}{n(n-1)} \sum_{i \neq j} \frac{1}{d_{ij}} = \frac{1}{n(n-1)} \sum_{i \neq j} \epsilon_{ij}$$

  con la convenzione naturale $1/\infty = 0$ per le coppie irraggiungibili
- $\epsilon_{ij} = 1/d_{ij}$ = **efficienza tra due nodi**, quanto è "facile" andare da $i$ a $j$. Esempio: due componenti $\{1,\dots,6\}$ e $\{7,\dots,10\}$, $d_{6,8} = \infty$ → $\epsilon_{6,8} = 1/\infty = 0$: le coppie non connesse **contribuiscono 0**
- Interpretazione: nodi vicini ($d_{ij}$ piccolo) comunicano efficientemente ($1/d_{ij}$ grande); nodi distanti contribuiscono poco; irraggiungibili zero
- Nei grafi **binari** (orientati o no) $E_{glob} \in [0, 1]$:
  - $E_{glob} = 1$: tutti i nodi connessi direttamente (distanza 1 per ogni coppia)
  - $E_{glob} = 0$: nessuna coppia connessa

### Efficienza globale pesata

$$E^w_{glob} = \frac{1}{n(n-1)} \sum_{i \neq j} \frac{1}{d^w_{ij}}$$

- **Remoteness**: $d^w_{ij}$ con Dijkstra sui pesi originali. **Proximity**: Dijkstra sui pesi reciprocati $w'_{ij} = 1/w_{ij}$
- Nella versione pesata $E^w_{glob}$ **non è necessariamente compresa tra 0 e 1** (dipende dalla scala dei pesi)

### Distanza media vs efficienza globale

| | Distanza media $\langle d \rangle$ | Efficienza globale $E_{glob}$ |
|---|---|---|
| Formula | $\frac{1}{n(n-1)} \sum d_{ij}$ | $\frac{1}{n(n-1)} \sum \frac{1}{d_{ij}}$ |
| Grafi disconnessi | problematica ($\infty$) | ben definita (0 per coppie irraggiungibili) |
| Interpretazione | distanza tipica | facilità di comunicazione tipica |
| Cresce con | distanze grandi | distanze piccole |
| Riferimento | - | Latora e Marchiori, PRL 2001 |

- **L'efficienza globale non è il reciproco della distanza media**: media degli inversi $\neq$ inverso della media. (Aggiunta: per la disuguaglianza fra media armonica e aritmetica $E_{glob} \geq 1/\bar d$ su reti connesse; nella rete binaria non orientata dell'esempio A-F $\bar d \approx 1{,}667$, $1/\bar d = 0{,}6$, ma $E_{glob} \approx 0{,}711$)
- **Grafo Erdős-Rényi al variare di $p$** (le slide dicono $N = 1000$, ma i grafici sono coerenti con $N \approx 100$: soglia $p_c = 0{,}01 = 1/N$ e grado medio 40 a $p = 0{,}4$, cioè $p(N-1) \approx 40$):
  - **LCC/N**: emerge la componente gigante attorno a $p_c = 0{,}01$, sale a circa 0,8 entro $p \approx 0{,}02$ e arriva a 1 oltre $p \approx 0{,}03$
  - **Diametro della LCC**: picco (circa 15) subito dopo la soglia, poi scende fino a 2
  - **Grado medio**: cresce linearmente con $p$
  - **Distanza media sulla LCC**: picco (circa 5,5) vicino alla soglia, poi scende a circa 1,6
  - **Efficienza globale**: cresce in modo **monotono** fino a circa 0,7: è l'unica delle misure coerente con l'aumento della connettività
- **ER $N = 1000$, $\langle k \rangle = 4$, rimozione casuale di nodi**:
  - LCC/N cala quasi linearmente e si annulla verso il 70-75% di nodi rimossi
  - diametro della LCC: da 10 sale fino a circa 24 (a 0,6-0,65 rimossi), poi crolla a circa 5
  - grado medio della rete residua: da 4 scende linearmente a circa 0,5
  - distanza media della LCC: da circa 5,2 sale a circa 9,4 (a 0,65), poi crolla a circa 2-2,7
  - efficienza globale: da 0,20 scende in modo **monotono** fino a quasi 0
  - Conclusione: diametro e distanza media non sono monotoni durante la frammentazione, l'efficienza sì

### LCC vs efficienza globale
- Figura (Sci. Rep., s41598-019-47119-2): reti reali pesate (Coli, Air) con rimozione di link secondo strategie Rand, First, Str (le ultime due non spiegate nelle slide). La **LCC resta a circa 1** mentre l'**efficienza cala** già dopo poche rimozioni (area rosa = divario): la LCC non vede il degrado funzionale finché la rete non si spezza
- Figura successiva: rete pesata in cui si tolgono i link più forti (o i nodi evidenziati in rosso), con barre TF, Eff, Eff$_{bin}$, LCC (TF non è spiegato nelle slide). LCC e Eff$_{bin}$ restano vicine a 1, mentre l'efficienza **pesata** Eff scende anche sotto 0,5: l'informazione sui pesi rivela danni invisibili alle misure binarie

### Sottografo indotto
- Dato $G = (V, E)$ e $S \subseteq V$, il **sottografo indotto** $G[S]$ è formato dai nodi di $S$ e da **tutti** gli archi del grafo originale che collegano coppie di nodi di $S$:

$$E_S = \{(u, v) \in E \mid u \in S, v \in S\}$$

- Esempio: $G$ con nodi A, B, C, D (archi A-B, A-C, B-C, B-D, C-D), $S = \{A, B, C\}$ → $G[S]$ è il triangolo A-B-C
- **Proprietà fondamentale**: scelti i nodi, il sottografo indotto contiene **necessariamente tutti** gli archi esistenti tra quei nodi (esempio con $S = \{A, B, C, D, E\}$: si toglie solo F con i suoi archi)

### Efficienza locale
- Misura quanto sono ben connessi i **vicini** di un nodo, cioè quanto è efficiente il sottografo che resta intorno a $i$ quando $i$ stesso viene rimosso:

$$E_{loc}(i) = E_{glob}(G_i) = \frac{1}{k_i(k_i - 1)} \sum_{\substack{j, h \in \tau(i) \\ j \neq h}} \frac{1}{d_{jh}(G_i)}$$

  - $G_i$: sottografo **indotto dai vicini** di $i$, **escluso** $i$
  - $k_i$: grado di $i$; $\tau(i)$: insieme dei vicini di $i$
  - (Nelle slide il termine è scritto $d_{ih}(G_i)$, ma $i \notin G_i$: la distanza è tra i due vicini $j$ e $h$, quindi $d_{jh}(G_i)$)
- È semplicemente l'**efficienza globale del sottografo dei vicini**, usando solo i collegamenti interni a quel sottografo
- Vicini ben collegati anche senza $i$ → $E_{loc}(i)$ **alta**; se $i$ è **indispensabile** per collegarli → $E_{loc}(i)$ **bassa**
- (Aggiunta: per l'intera rete si usa la media $E_{loc} = \frac{1}{n} \sum_i E_{loc}(i)$, come in Latora e Marchiori; è una misura di tolleranza ai guasti locali)

### Esempio di calcolo: rete binaria e diretta
- Grafo: $A\to B$, $A\to D$, $B\to C$, $B\to E$, $C\to E$, $C\to F$, $D\to B$, $D\to E$, $E\to F$
- Matrice delle distanze minime $d_{ij}$ e somma dei reciproci per riga:

| | A | B | C | D | E | F | $\sum_j 1/d_{ij}$ |
|---|---|---|---|---|---|---|---|
| **A** | 0 | 1 | 2 | 1 | 2 | 3 | $1 + \frac12 + 1 + \frac12 + \frac13 = \frac{10}{3}$ |
| **B** | $\infty$ | 0 | 1 | $\infty$ | 1 | 2 | $\frac52$ |
| **C** | $\infty$ | $\infty$ | 0 | $\infty$ | 1 | 1 | 2 |
| **D** | $\infty$ | 1 | 2 | 0 | 1 | 2 | 3 |
| **E** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | 0 | 1 | 1 |
| **F** | $\infty$ | $\infty$ | $\infty$ | $\infty$ | $\infty$ | 0 | 0 |

- Somma totale $= 71/6 \approx 11{,}833$; coppie ordinate $N(N-1) = 6 \cdot 5 = 30$:

$$E_{glob}(G) = \frac{1}{6 \cdot 5} \cdot \frac{71}{6} = \frac{71}{180} \approx 0{,}394$$

- Da notare: **direzionalità** (l'efficienza da A a B può differire da quella da B ad A), **irraggiungibilità** (contributo zero), **normalizzazione** (il denominatore comprende tutte le 30 coppie ordinate, anche quelle irraggiungibili)

## Distribuzione dei gradi

### Definizione
- Nel Modulo 4 il grado $k_i$ era una misura di centralità (proprietà **locale**); la **distribuzione dei gradi** $P(k)$ descrive come i gradi sono organizzati su tutta la rete (proprietà **globale**):

$$P(k) = \frac{\text{numero di nodi con grado } k}{n} = \frac{N_k}{n}, \qquad \sum_{k=0}^{k_{max}} P(k) = 1$$

- È la **probabilità che un nodo scelto a caso abbia grado $k$**; in pratica è l'**istogramma normalizzato** dei gradi (figura dalla documentazione NetworkX: istogramma non normalizzato, conteggi, vs normalizzato, frequenze)
- Esempio: rete non orientata di 7 nodi, archi A-B, A-C, A-D, B-C, B-E, C-D, C-F, D-G, E-F, F-G ($m = 10$). Gradi: $k_A = 3$, $k_B = 3$, $k_C = 4$, $k_D = 3$, $k_E = 2$, $k_F = 3$, $k_G = 2$

| $k$ | $N_k$ | $P(k)$ |
|---|---|---|
| 0 | 0 | 0 |
| 1 | 0 | 0 |
| 2 | 2 | $2/7 \approx 0{,}286$ |
| 3 | 4 | $4/7 \approx 0{,}571$ |
| 4 | 1 | $1/7 \approx 0{,}143$ |
| Totale | 7 | 1 |

  (La prima versione delle slide riportava $k_B = 2$, quindi $P(2) = P(3) = 3/7$: impossibile, perché la somma dei gradi sarebbe 19, dispari. Corretto nella versione del 22/10)

### Grado medio
- **Grado medio**, la connettività tipica della rete ($m$ = numero di legami, $n$ = numero di nodi):

$$\bar k = \frac{1}{n} \sum_i k_i = \sum_k k \cdot P(k) = \frac{2m}{n}$$

- L'ultima uguaglianza vale **sempre** (rete non orientata): la somma dei gradi è il doppio del numero di archi, perché ogni arco contribuisce 1 al grado di ciascuno dei suoi due estremi

### Lemma della stretta di mano (*handshaking lemma*)
- In un grafo non orientato:

$$\sum_i k_i = 2m$$

- Ogni arco ha esattamente due estremi: sommando i gradi di tutti i nodi ogni arco viene contato **due volte**
- Il nome: in una stanza di $n$ persone, se si sommano le strette di mano ricevute da ciascuno si ottiene il doppio delle strette avvenute, perché ognuna coinvolge due persone
- Conseguenze: $\bar k = 2m/n$, e la somma dei gradi è sempre **pari** (utile per controllare un calcolo a mano)
- Esempio: $\bar k = 2 \cdot \frac27 + 3 \cdot \frac47 + 4 \cdot \frac17 = \frac{20}{7} = \frac{2 \cdot 10}{7} \approx 2{,}857$

### Varianza dei gradi
- Quanto i gradi si discostano dalla media?

$$\sigma_k^2 = \frac{1}{n} \sum_i (k_i - \langle k \rangle)^2 = \langle k^2 \rangle - \langle k \rangle^2$$

  con $\langle k \rangle$ grado medio e $\langle k^2 \rangle$ media dei quadrati dei gradi
- Varianza **alta** → rete **eterogenea**; varianza **bassa** → rete **omogenea** (nodi con grado simile)
- Esempio: 6 nodi, archi A-B, A-C, B-C, B-D, D-E, F isolato. Gradi: A 2, B 3, C 2, D 2, E 1, F 0, quindi $P(0) = P(1) = P(3) = 1/6$, $P(2) = 3/6$

$$\langle k \rangle = \frac{0 + 1 + 2 \cdot 3 + 3}{6} = \frac{10}{6} \approx 1{,}667 \qquad \langle k^2 \rangle = \frac{0^2 + 1^2 + 3 \cdot 2^2 + 3^2}{6} = \frac{22}{6} \approx 3{,}667$$

$$\sigma_k^2 = \frac{22}{6} - \left(\frac{10}{6}\right)^2 = \frac{8}{9} \approx 0{,}889$$

### Poisson vs legge di potenza
- **Distribuzione di Poisson** (reti casuali omogenee), varianza **relativamente contenuta**, un solo picco attorno a $\langle k \rangle$:

$$P(k) = \frac{e^{-\langle k \rangle} \langle k \rangle^k}{k!}$$

- **Legge di potenza** (*power law*, reti eterogenee con **hub**), varianza che **può essere molto elevata**:

$$P(k) \propto k^{-\gamma}, \qquad 1 < \gamma \leq 3 \text{ (range indicato nelle slide)}$$

  (Nelle slide la formula è scritta $P(k) =\propto k^{-\propto}$, mescolando il simbolo di proporzionalità con l'esponente, che nel testo si chiama $\gamma$. Aggiunta: per $\gamma \leq 3$ il secondo momento $\langle k^2 \rangle$, e quindi la varianza, diverge al crescere di $N$, per $\gamma \leq 2$ anche la media; le reti reali scale-free hanno tipicamente $2 < \gamma < 3$)
- Figure: rete omogenea (picco singolo vicino a $\langle z \rangle$) vs rete eterogenea ($D(z) \approx z^{-\gamma}$, molti nodi a basso grado e pochi hub)
- Esempio reale (Barabási, networksciencebook.com, cap. 4):
  - **rete autostradale USA**: distribuzione tipo Poisson, nessuna città ha centinaia di autostrade
  - **rete aerea USA**: legge di potenza, la maggior parte degli aeroporti ha pochi voli, ma Chicago e Los Angeles concentrano centinaia di rotte (hub)
- Figura (doi 10.1088/1751-8121/ad41a6): $P(k)$ di quattro reti
  - **ER**: picco a grado basso (1-2) e coda corta
  - **WS** (Watts-Strogatz): distribuzione molto stretta attorno a 4
  - **BA** (Barabási-Albert): coda lunga fino a circa 60 (asse $P(k)$ logaritmico)
  - **rete sociale**: coda lunga fino a circa 70

## Assortatività

### Motivazione e definizione intuitiva
- $P(k)$ dice come i gradi sono distribuiti, ma **non dice nulla su come si connettono i nodi**: due reti con la stessa $P(k)$ possono avere strutture completamente diverse in termini di **chi si connette con chi**
- Domanda: i nodi tendono a connettersi con nodi **simili in termini di grado**?
- **Rete assortativa**: hub con hub, periferici con periferici: i "simili si attraggono"
- **Rete disassortativa**: hub con nodi periferici e viceversa: i "dissimili si attraggono" (figura: stelle i cui centri sono legati a foglie)
- **Rete neutra**: nessuna preferenza, connessioni casuali rispetto al grado
- Figura (PLoS ONE, 10.1371/journal.pone.0028322): rete disassortativa fatta di stelle separate vs rete assortativa con un nucleo denso di hub

### Coefficiente di assortatività (Newman)

$$r = \frac{Cov(k_i, k_j)}{\sigma_{k_i} \sigma_{k_j}} = \frac{\text{covarianza osservata dei gradi lungo gli archi}}{\text{varianza dei gradi alle estremità degli archi}}, \qquad -1 \leq r \leq 1$$

- $k_i$, $k_j$: gradi dei due estremi di un arco; $\sigma_{k_i}$, $\sigma_{k_j}$: deviazioni standard dei gradi agli estremi
- **Numeratore**: covarianza osservata tra i gradi; **denominatore**: normalizza, trasformando la covarianza in un coefficiente tra $-1$ e $1$
- Formula generale della covarianza: $Cov(X, Y) = \frac{1}{n} \sum_{i=1}^n (x_i - \bar x)(y_i - \bar y)$
- Sugli archi (grafo non orientato, $m$ archi):

$$Cov(k_i, k_j) = \frac{1}{m} \sum_{(i,j) \in E} (k_i - \mu)(k_j - \mu), \qquad \mu = \frac{1}{2m} \sum_{\{i,j\} \in E} (k_i + k_j)$$

- **Attenzione**: $\mu$ è il grado medio **alle estremità degli archi**, non in generale il grado medio $\langle k \rangle$ della rete (i nodi di grado alto compaiono come estremo in più archi, quindi $\mu \geq \langle k \rangle$)
- Denominatore, cioè la varianza dei gradi alle estremità rispetto a $\mu$ (gli estremi sono $2m$):

$$\sigma^2 = \frac{1}{2m} \sum_{(i,j) \in E} \left[(k_i - \mu)^2 + (k_j - \mu)^2\right]$$

  (La prima versione delle slide aveva $\frac{1}{m}$, che darebbe il doppio della varianza; corretto in $\frac{1}{2m}$ nella versione del 22/10)
- Interpretazione:
  - $r > 0$: **assortativa**, nodi con gradi simili tendono a collegarsi
  - $r < 0$: **disassortativa**, nodi con gradi diversi tendono a collegarsi
  - $r \approx 0$: assenza di **correlazione lineare** tra i gradi dei nodi collegati

### Legame con il coefficiente di Pearson
- $r$ è il **coefficiente di correlazione di Pearson** fra i gradi ai due estremi degli archi:

$$\rho = \frac{\sum_i (x_i - \bar x)(y_i - \bar y)}{\sqrt{\sum_i (x_i - \bar x)^2 \cdot \sum_i (y_i - \bar y)^2}}$$

- **Numeratore**: $(x_i - \bar x)$ e $(y_i - \bar y)$ sono gli scarti dalla media (positivi sopra, negativi sotto); la loro somma dei prodotti è la **covarianza** (non normalizzata), che dice se $X$ e $Y$ crescono e decrescono insieme
- **Denominatore**: radice del prodotto delle due **varianze** (non normalizzate); è il massimo valore assoluto che il numeratore può raggiungere, date le variabilità delle due variabili, e garantisce $\rho \in [-1, 1]$
- Figura (Wikipedia): reti con assortatività $A = 0$, $A = 0{,}26$, $A = 0{,}43$

### Esempio numerico
- Rete non orientata di 6 nodi: $\{A-B, A-C, B-C, B-D, C-E, E-D, D-F\}$ (lo stesso grafo degli esempi sulle distanze), $m = 7$. Gradi: $k_A = 2$, $k_B = 3$, $k_C = 3$, $k_D = 3$, $k_E = 2$, $k_F = 1$

| Arco | $k_i$ | $k_j$ | $k_i + k_j$ | $k_i k_j$ | $k_i - \mu$ | $k_j - \mu$ | prodotto |
|---|---|---|---|---|---|---|---|
| A-B | 2 | 3 | 5 | 6 | $-0{,}5714$ | $+0{,}4286$ | $-0{,}2449$ |
| A-C | 2 | 3 | 5 | 6 | $-0{,}5714$ | $+0{,}4286$ | $-0{,}2449$ |
| B-C | 3 | 3 | 6 | 9 | $+0{,}4286$ | $+0{,}4286$ | $+0{,}1837$ |
| B-D | 3 | 3 | 6 | 9 | $+0{,}4286$ | $+0{,}4286$ | $+0{,}1837$ |
| C-E | 3 | 2 | 5 | 6 | $+0{,}4286$ | $-0{,}5714$ | $-0{,}2449$ |
| D-E | 3 | 2 | 5 | 6 | $+0{,}4286$ | $-0{,}5714$ | $-0{,}2449$ |
| D-F | 3 | 1 | 4 | 3 | $+0{,}4286$ | $-1{,}5714$ | $-0{,}6735$ |
| **Totale** | | | **36** | **45** | | | |

- Media dei gradi alle estremità: $\sum \frac{k_i + k_j}{2} = 2{,}5 + 2{,}5 + 3 + 3 + 2{,}5 + 2{,}5 + 2 = 18$, quindi

$$\mu = \frac{36}{14} = \frac{18}{7} \approx 2{,}5714 \quad (\text{mentre } \langle k \rangle = 14/6 \approx 2{,}333)$$

- Sostituzione nella formula, in forma equivalente $r = \dfrac{\frac1m \sum k_i k_j - \mu^2}{\frac1m \sum \frac{k_i^2 + k_j^2}{2} - \mu^2}$ (il 7 al denominatore è $\frac17 \cdot \frac{98}{2}$, con $\sum (k_i^2 + k_j^2) = 98$; il passaggio non è esplicitato nelle slide):

$$r = \frac{\frac{45}{7} - \left(\frac{18}{7}\right)^2}{7 - \left(\frac{18}{7}\right)^2} = \frac{\frac{315 - 324}{49}}{\frac{343 - 324}{49}} = \frac{-9}{19} \approx -0{,}474$$

- **Moderatamente disassortativa**: i nodi di grado elevato si collegano abbastanza spesso a nodi di grado più basso, soprattutto per l'arco $D - F$ (grado 3 con grado 1)

### Reti reali (Newman, *Assortative Mixing in Networks*, PRL 89, 208701, 2002)

| Rete | Nodi ($n$) | $r$ | Tipo |
|---|---|---|---|
| Coautori in fisica | 52.909 | 0,363 | assortativa |
| Coautori in biologia | 1.520.251 | 0,127 | assortativa |
| Coautori in matematica | 253.339 | 0,120 | assortativa |
| Collaborazioni tra attori | 449.913 | 0,208 | assortativa |
| Consiglieri di amministrazione | 7.673 | 0,276 | assortativa |
| Internet | 10.697 | $-0{,}189$ | disassortativa |
| World Wide Web | 269.504 | $-0{,}065$ | debolmente disassortativa |
| Interazioni proteina-proteina | 2.115 | $-0{,}156$ | disassortativa |
| Rete neurale di *C. elegans* | 307 | $-0{,}163$ | disassortativa |
| Food web marina | 134 | $-0{,}247$ | disassortativa |
| Food web d'acqua dolce | 92 | $-0{,}276$ | disassortativa |

- Schema: le reti **sociali** sono assortative, quelle **tecnologiche e biologiche** disassortative

## Coefficiente di clustering

### Triangoli e transitività
- **L'idea più semplice di comunità: il triangolo**. Se A conosce B e B conosce C, è probabile che anche A conosca C: i tre nodi formano un **triangolo**
- I triangoli indicano la presenza di **gruppi fortemente coesi** e sono il "**mattone elementare**" delle comunità
- È la **proprietà transitiva** delle reti sociali (*transitivity coefficient*): "amici di amici sono anche miei amici". Figura: rete a basso clustering (un solo triangolo) vs rete ad alto clustering (molti triangoli)
- **Tripla** centrata su un nodo: il nodo e due suoi vicini
  - **aperta**: i due vicini non sono collegati tra loro
  - **chiusa**: i due vicini sono collegati, e formano un triangolo

### Clustering locale
- Misura quanto i vicini di un nodo sono connessi tra loro: "i miei amici sono anche amici tra loro?"

$$C_i = \frac{\text{triple chiuse centrate su } i}{\text{triple totali centrate su } i} = \frac{T_i}{\frac{k_i (k_i - 1)}{2}} = \frac{2 T_i}{k_i (k_i - 1)}, \qquad 0 \leq C_i \leq 1$$

- Grafi **non orientati e binari**. $T_i$ = numero di triple chiuse centrate su $i$, cioè di **triangoli** che passano per $i$; $\frac{k_i (k_i - 1)}{2}$ = coppie di vicini, cioè triple possibili centrate su $i$
- È la **frazione di triple centrate sul nodo che risultano chiuse**, ovvero la probabilità che due vicini dello stesso nodo siano collegati tra loro
- Esempio: A collegato a B, C, D, E ($k_A = 4$), con i soli archi B-C e D-E fra i vicini ($T_A = 2$):

$$C_A = \frac{2 \cdot 2}{4 \cdot 3} = \frac{4}{12} \approx 0{,}333$$

- Figura (doi 10.1111/j.1939-7445.2008.00004.x): A con tre vicini B, C, D e 0, 1, 2, 3 archi fra loro → $C_A = 0$; $0{,}33$; $0{,}67$; $1$ (le coppie di vicini sono 3)

### Clustering medio della rete
- Media aritmetica dei clustering locali di tutti i nodi:

$$C = \frac{1}{n} \sum_{i=1}^n C_i$$

- Nodi di grado 0 o 1 non hanno coppie di vicini: $C_i$ **non è definito**. Per convenzione si pone $C_i = 0$ oppure si escludono dalla media, e **la scelta cambia il valore** di $C$
- In R: `mean(transitivity(G, type = "local"), na.rm = TRUE)`. `transitivity(type = "local")` restituisce `NaN` per i nodi di grado 0 o 1 e `na.rm = TRUE` li esclude (nelle slide il grafo si chiama `G_att`, quello attaccato, e manca il `mean(`)

### Clustering sotto rimozione di nodi (errore vs attacco)
- **Errore** = rimozione casuale; **attacco** = rimozione mirata (dei nodi più centrali)
- **Grafo casuale** ER ($N = 1000$, $p = 0{,}005$, `erdos.renyi.game(n, p, type = "gnp", directed = FALSE)`): clustering medio iniziale bassissimo, circa $0{,}005$ (aggiunta: un ER ha $C \approx p$). Con 1 simulazione la curva dell'errore è molto rumorosa; con 100 simulazioni resta piatta intorno a $0{,}005$ (banda di variabilità che si allarga oltre il 60-70% di rimozioni), mentre l'attacco porta $C$ a zero già intorno al 40-50%. **Il grafo casuale ha basso clustering**
- **Watts-Strogatz** ($N = 1000$, `sample_smallworld(dim = 1, size = n, nei = 3, p = 0.05)`, 100 simulazioni): clustering iniziale alto, circa $0{,}45$. Sotto errore resta stabile fin quasi al 90%; sotto attacco sale leggermente all'inizio (circa $0{,}48$), poi cala da circa il 30-40% e crolla a zero intorno al 73%

## Funzioni utili per il progetto (aggiunta, non nelle slide)
Le slide mostrano solo il codice R/igraph riportato sopra; queste sono le funzioni corrispondenti per calcolare le stesse misure.

```python
import networkx as nx
max(nx.connected_components(G), key=len)          # nodi della GCC (non orientato)
nx.weakly_connected_components(G)                 # WCC (orientato)
nx.strongly_connected_components(G)               # SCC (orientato)
G.subgraph(nodi)                                  # sottografo indotto
nx.diameter(G), nx.eccentricity(G)                # solo su grafo connesso
nx.average_shortest_path_length(G, weight="w")    # solleva errore se non connesso
nx.global_efficiency(G), nx.local_efficiency(G)   # non orientato e non pesato
nx.degree_histogram(G)                            # conteggi N_k, k = 0..k_max
nx.degree_assortativity_coefficient(G)
nx.clustering(G)                                  # C_i, vale 0 per i nodi di grado 0 o 1
nx.average_clustering(G)                          # media con C_i = 0 per quei nodi
nx.transitivity(G)                                # globale: 3 * triangoli / triple connesse
```

```r
library(igraph)
components(G, mode = "weak")   # oppure mode = "strong"
induced_subgraph(G, nodi)
distances(G)                   # i pesi in E(G)$weight sono trattati come costi
mean_distance(G); diameter(G); eccentricity(G)
global_efficiency(G); average_local_efficiency(G)
degree_distribution(G)
assortativity_degree(G)
transitivity(G, type = "local")    # NaN per i nodi di grado 0 o 1
transitivity(G, type = "global")
```

- Attenzione alla convenzione: `nx.average_clustering` conta come 0 i nodi di grado 0 o 1, `mean(..., na.rm = TRUE)` in R li esclude, quindi sulla stessa rete i due valori possono differire. Nel report va detto quale si è usata

- Per pesi di tipo **prossimità** (flussi, intensità) bisogna passare esplicitamente $1/w$ come pesi delle distanze, altrimenti un legame forte viene trattato come lungo

## Da ricordare per l'orale e il progetto
- **Componente connessa**, **GCC** e la sua versione normalizzata $S = \max_j |c_j| / N$: è la misura base di **funzionalità** nelle analisi di robustezza (attacco casuale vs mirato)
- Grafi orientati: **WCC** (si ignora la direzione) vs **SCC** (raggiungibilità mutua $i \rightsquigarrow j$ e $j \rightsquigarrow i$); LWCC e LSCC. Se la direzione conta (strade, Web, flussi, dipendenze software) la robustezza va valutata sulla **LSCC**, che crolla prima della LWCC
- **Diametro** $D = \max d_{ij}$ (caso peggiore), **eccentricità** $ecc(i) = \max_j d_{ij}$, **distanza media** $\bar d = \frac{1}{n(n-1)} \sum d_{ij}$; su grafi disconnessi sono infiniti e si calcolano sulla LCC
- Pesi: **remoteness** (costi, si usano così) vs **proximity** (intensità, si usa $1/w$); il cammino con meno hop non è per forza quello di peso minimo
- Distanza media e diametro calcolati sulla LCC **non sono monotoni** (crescono e poi crollano durante la frammentazione, hanno un picco vicino alla soglia di percolazione $p = 1/n$): come misure di funzionalità sono **incoerenti**
- **Efficienza globale** $E_{glob} = \frac{1}{n(n-1)} \sum 1/d_{ij}$ (Latora-Marchiori), con $1/\infty = 0$: ben definita anche su reti disconnesse, in $[0, 1]$ nel caso binario, **monotona** sotto rimozione; **non** è il reciproco di $\bar d$. Pesata: può uscire da $[0, 1]$. Rileva il degrado anche quando la LCC resta intatta
- **Sottografo indotto** $G[S]$: tutti gli archi tra i nodi di $S$. **Efficienza locale** = efficienza globale del sottografo indotto dai vicini, senza $i$: alta se i vicini restano collegati senza $i$
- Esempio da saper rifare: efficienza della rete binaria diretta = $71/180 \approx 0{,}394$, con tutte le 30 coppie ordinate al denominatore
- **Distribuzione dei gradi** $P(k) = N_k / n$, $\sum P(k) = 1$; **grado medio** $\bar k = \sum k P(k) = 2m/n$; **varianza** $\sigma_k^2 = \langle k^2 \rangle - \langle k \rangle^2$ (alta = eterogenea)
- **Poisson** (omogenea, autostrade) vs **legge di potenza** $P(k) \propto k^{-\gamma}$ (hub, rete aerea, varianza enorme)
- **Assortatività** $r$ = correlazione di Pearson dei gradi agli estremi degli archi, $-1 \leq r \leq 1$; $\mu$ è il grado medio agli estremi, non $\langle k \rangle$. Esempio: $r = -9/19 \approx -0{,}474$. Reti sociali assortative, tecnologiche e biologiche disassortative
- **Lemma della stretta di mano** $\sum_i k_i = 2m$: da qui $\bar k = 2m/n$ e la somma dei gradi sempre pari
- **Clustering locale** $C_i = \frac{2 T_i}{k_i (k_i - 1)}$ = frazione di triple chiuse centrate su $i$; esempio $C_A = 4/12 \approx 0{,}333$. **Clustering medio** $C = \frac1n \sum C_i$, con la convenzione sui nodi di grado 0 o 1 da dichiarare
- ER ha clustering bassissimo ($\approx p$), WS alto ($\approx 0{,}45$ con `nei = 3`, $p = 0{,}05$); sotto errore il clustering medio regge, sotto attacco crolla
