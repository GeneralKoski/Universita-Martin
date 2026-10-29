# Benchmarking

Fonte: `Benchmarking.pdf`

## Benchmark e benchmarking
- **Benchmarking** (in italiano **analisi comparativa**): "benchmark something (against something) to judge the quality of something in relation to that of other similar things"
  - "The journal was recently benchmarked against other IT journals."
  - "Projects are assessed and benchmarked against the targets."
- **Benchmark**: "something which can be measured and used as a standard that other things can be compared"
  - è costituito da **uno o più dataset**
  - **reali**: acquisiti misurando eventi realmente accaduti. Rappresentano il mondo reale in modo altamente **veritiero** (a parte gli errori di misura)
  - **sintetici** (o **in silico**): costruiti **artificialmente** seguendo regole specifiche. Possono basarsi su dati reali, ma possono risultare **molto distanti dalla realtà**

## Limiti dei benchmark (Joshi et al. 2008)
I benchmark standardizzati semplificano il confronto fra sistemi, ma architetti e ricercatori incontrano diverse difficoltà, sia nello sviluppo industriale sia nella ricerca:
- un benchmark è solo un **campione** dello spazio "comportamentale" (dei fenomeni) dell'applicazione
- i benchmark sono **rigidi**: misurano le prestazioni in **un singolo punto** di quello spazio
- le suite di benchmark sono **costose** da sviluppare, mantenere e aggiornare: "Designing tomorrow's microprocessors using today's benchmarks built from yesterday's programs" [WEIC97] [YI06]
- i benchmark standardizzati sono **open source**, mentre a volte le applicazioni di interesse sono **proprietarie**

## Caratteristiche chiave di un benchmark (Kistowski et al. 2015)
| Caratteristica | Significato |
|---|---|
| **Rilevanza** | quanto il comportamento del benchmark corrisponde ai comportamenti che interessano a chi usa i risultati |
| **Riproducibilità** | produrre costantemente risultati simili rieseguendo il benchmark con la stessa configurazione di test |
| **Correttezza (fairness)** | permettere a configurazioni diverse di competere sui propri meriti, senza limitazioni artificiali |
| **Verificabilità** | dare garanzie che i risultati siano accurati |
| **Usabilità** | permettere a tutti gli utenti di eseguire il benchmark nei propri ambienti |

## Linee guida per creare un benchmark (Weber et al. 2019)
- Riferimento: L.M. Weber, W. Saelens, R. Cannoodt, C. Soneson, A. Hapfelmeier, P.P. Gardner, A.-L. Boulesteix, Y. Saeys, M.D. Robinson, *Essential guidelines for computational method benchmarking*, Genome Biology 20:125 (2019)
- Contesto (abstract): in biologia computazionale e non solo si deve spesso scegliere fra più metodi per la stessa analisi. Gli studi di benchmarking li confrontano **rigorosamente** su dataset di riferimento ben caratterizzati, per capire i punti di forza di ciascuno e dare raccomandazioni; vanno progettati con cura per essere **accurati, non distorti e informativi**
- Le 10 raccomandazioni ("Summary of guidelines"):
  1. definire **scopo e ambito** del benchmark
  2. includere **tutti i metodi rilevanti**
  3. scegliere (o progettare) **dataset rappresentativi**
  4. scegliere valori dei **parametri** e **versioni del software** appropriati
  5. valutare i metodi con **metriche quantitative** chiave di prestazione
  6. valutare misure **secondarie**: requisiti computazionali, facilità d'uso, procedure di installazione, qualità della documentazione
  7. **interpretare** i risultati e dare raccomandazioni dal punto di vista sia dell'utente sia dello sviluppatore del metodo
  8. **pubblicare** i risultati in un formato accessibile
  9. progettare il benchmark in modo da permettere **estensioni future**
  10. seguire le buone pratiche di **ricerca riproducibile**, rendendo pubblici codice e dati

### Tabella 1: quanto conta ogni principio, compromessi e trappole
Più "+" = principio più centrale per la valutazione.

| Principio | Importanza | Compromesso | Trappole possibili |
|---|---|---|---|
| 1. Scopo e ambito | +++ | quanto deve essere completo il benchmark | ambito troppo ampio: troppo lavoro per le risorse disponibili; troppo stretto: risultati non rappresentativi e forse fuorvianti |
| 2. Scelta dei metodi | +++ | quanti metodi includere | escludere metodi chiave |
| 3. Scelta (o progettazione) dei dataset | +++ | numero e tipi di dataset | soggettività nella scelta (es. dataset non rappresentativi delle applicazioni reali); troppo pochi dataset o scenari di simulazione; simulazioni troppo semplicistiche |
| 4. Parametri e versioni del software | ++ | quanto tuning dei parametri | tuning spinto per alcuni metodi e parametri di default per altri (es. i metodi concorrenti) |
| 5. Criteri di valutazione: metriche quantitative chiave | +++ | numero e tipi di metriche | metriche scelte in modo soggettivo, che non si traducono in prestazioni reali; metriche che danno stime troppo ottimistiche; metodi non confrontabili direttamente su singole metriche (es. se pensati per compiti diversi) |
| 6. Criteri di valutazione: misure secondarie | ++ | numero e tipi di metriche | soggettività delle misure qualitative (facilità d'uso, installazione, documentazione); pesi soggettivi fra più metriche; tempo di esecuzione e scalabilità dipendono da CPU e memoria |
| 7. Interpretazione, linee guida, raccomandazioni | ++ | generalità contro specificità delle raccomandazioni | le differenze fra i metodi migliori possono essere minime; lettori diversi guardano aspetti diversi delle prestazioni |
| 8. Pubblicazione dei risultati | + | risorse da dedicare a risorse online | le risorse online possono non essere più accessibili (o non girare più) dopo qualche anno |
| 9. Estensioni future | ++ | risorse da dedicare all'estensibilità | metodi o dataset aggiunti in futuro possono essere non rappresentativi (es. per richieste degli autori dei metodi) |
| 10. Ricerca riproducibile | ++ | risorse da dedicare alla riproducibilità | alcuni strumenti possono non essere più compatibili o accessibili dopo qualche anno |

## Scelta dei criteri di valutazione delle prestazioni
Albero della figura (Weber et al.):
- **Quantitativi**
  - **con ground truth** (confronto con la verità nota):
    - **target discreto**: true positive rate (TPR), false positive rate (FPR), false discovery rate (FDR), sensitività e specificità, precision e recall, F1 score, Adjusted Rand index, normalized mutual information, curve ROC / TPR-FDR / PR, area sotto ROC / PR, accuratezza di classificazione (supervisionato)
    - **target continuo**: root mean square error, misure di distanza, correlazione di Pearson, somma dei log-rapporti assoluti, log-modulus, cross-entropy, accuratezza di predizione (supervisionato)
    - **target complesso**: similarità fra grafi, fra alberi, fra distribuzioni, metriche ad hoc
  - **senza ground truth**: stabilità, stocasticità, robustezza, confronti con il nullo (null comparisons), tempo di esecuzione, scalabilità, requisiti di memoria
- **Qualitativi**: facilità d'uso, qualità della documentazione, procedure di installazione, disponibilità libera / open source, qualità del codice, uso di unit test, uso di continuous integration

(Aggiunta, non nelle slide: le parti successive su labirinti e grafi planari sono esempi di **generazione di benchmark sintetici**, cioè istanze costruite con regole note per mettere alla prova algoritmi di ricerca di cammini o su grafi, controllandone le proprietà.)

## Algoritmi per generare labirinti
Un labirinto su una griglia è un **grafo**: le celle sono i nodi, i muri abbattuti gli archi. Tutti gli algoritmi seguenti (tranne gli automi cellulari) producono un **albero ricoprente** della griglia: ogni cella è raggiungibile e c'è un solo percorso fra due celle (labirinto "perfetto"). (Aggiunta, non nelle slide; verificato sotto: con 20×20 celle ogni labirinto generato ha 399 = 400 − 1 passaggi ed è un albero.)

### Ricerca in profondità randomizzata (DFS)
- si parte da una scacchiera (grafo) in cui ogni cella ha inizialmente **4 pareti**
- da una cella casuale si sceglie una cella **adiacente casuale non ancora visitata**
- si **rimuove il muro** fra le due celle, si marca la nuova come visitata e la si mette sulla **pila** della DFS
- si continua. Una cella senza vicini non visitati è un **vicolo cieco**: si torna indietro (backtracking) lungo il percorso fino a una cella con un vicino non visitato
- da lì si riprende visitando la nuova cella (si crea un **nuovo incrocio**)
- si continua finché ogni cella è stata visitata

**Versione ricorsiva**, data una cella corrente:
1. marca la cella corrente come visitata
2. finché la cella corrente ha vicini non visitati:
   - scegli uno dei vicini non visitati
   - rimuovi il muro fra la cella corrente e quella scelta
   - richiama la routine ricorsivamente sulla cella scelta

**Versione iterativa**:
1. scegli la cella iniziale, marcala come visitata e mettila nello stack
2. finché lo stack non è vuoto:
   - estrai una cella dallo stack e rendila la cella corrente
   - se la cella corrente ha vicini non visitati:
     - rimetti la cella corrente nello stack
     - scegli uno dei vicini non visitati
     - rimuovi il muro fra la cella corrente e quella scelta
     - marca la cella scelta come visitata e mettila nello stack

(Aggiunta, non nelle slide: la versione ricorsiva su griglie grandi supera il limite di ricorsione di Python, 1000 di default; per questo si usa quella iterativa.)

### Kruskal randomizzato
1. crea l'elenco di tutti i muri e un **insieme per ogni cella**, contenente solo quella cella
2. per ogni muro, in **ordine casuale**: se le due celle divise dal muro appartengono a **insiemi distinti**, rimuovi il muro e **unisci** gli insiemi delle due celle
- (Aggiunta, non nelle slide: è Kruskal per l'albero ricoprente minimo con pesi casuali; gli insiemi si gestiscono con una struttura **union-find**. Unire solo celle di insiemi diversi garantisce l'assenza di cicli.)

### Prim randomizzato
1. inizia con una griglia **piena di muri**
2. scegli una cella, marcala come parte del labirinto e aggiungi i suoi muri all'**elenco dei muri**
3. finché ci sono muri nell'elenco:
   - scegli un muro **casuale** dall'elenco
   - se **solo una** delle due celle che divide è visitata: trasforma il muro in un passaggio, marca la cella non visitata come parte del labirinto e aggiungi i suoi muri all'elenco
   - rimuovi il muro dall'elenco

### Wilson randomizzato
- Genera un **campione imparziale** (labirinto scelto con probabilità **uniforme** fra tutti i possibili) usando **random walk con cancellazione dei cicli** (loop-erased random walk). La slide aggiunge che "serve a non generare troppi vicoli ciechi"
- Il risultato è **indipendente dall'ordine** con cui si visitano le celle non ancora visitate
- Il loop-erased random walk serve a estrarre **alberi ricoprenti** (spanning tree) a caso da un grafo: si fa partire una random walk da un vertice, si ottiene un percorso che può contenere **cicli**, si eliminano i cicli e il percorso diventa un albero
- Per il labirinto si può:
  - lanciare **un'unica** random walk, attendere che visiti tutto il grafo, poi eliminare i cicli
  - lanciare **più** random walk, in modo che quella al passo successivo non visiti le celle delle precedenti, trasformare ogni percorso in un albero e **connettere** gli alberi
- (Precisazione sulla procedura: in Wilson ogni nuova walk parte da una cella fuori dall'albero e **cammina finché non tocca l'albero** già costruito; cancellati i cicli, il percorso viene aggiunto all'albero. Quindi le walk successive non "evitano" le celle precedenti: si fermano quando le raggiungono, ed è così che gli alberi si connettono. Cancellare i cicli di un'unica walk che copre tutto il grafo dà un cammino semplice, non un albero ricoprente; il metodo a walk unica che dà un albero uniforme è **Aldous-Broder**, che tiene per ogni cella l'arco con cui è stata raggiunta la prima volta.)
- (Precisazione su "non generare troppi vicoli ciechi": l'uniformità significa assenza di bias, non pochi vicoli ciechi. Misurato su 30 labirinti 20×20 per algoritmo: DFS 41,8 vicoli ciechi in media, Kruskal 121,6, Wilson 116,3. Chi ne genera pochi, con corridoi lunghi, è la DFS.)

### Divisione ricorsiva
- si parte da un labirinto **senza pareti**, detto **camera**
- si divide la camera in due con una **parete** in posizione casuale, lasciando un **buco** per passare da una parte all'altra
- si procede ricorsivamente sulle due nuove camere

### Automi cellulari
- simili al **Game of Life** di Conway
- una cella **sopravvive** da una generazione all'altra se e solo se ha **da 1 a 5 (o 4) vicini**
- (Aggiunta, non nelle slide: sono le regole "Maze", B3/S12345, e "Mazectric", B3/S1234: una cella morta nasce con esattamente 3 vicini. Diversamente dagli altri metodi non garantiscono un labirinto perfetto né connesso.)

### Criteri per un "buon" labirinto
- rapporto fra numero di celle di cammino e muri
- numero di **vicoli ciechi**
- numero di **percorsi distinti** che portano all'uscita
- lunghezze dei (sotto)percorsi **senza diramazioni**
- **distanza** (del percorso minimo) dall'entrata all'uscita
- ...

(Aggiunta, non nelle slide: misure su 30 labirinti 20×20 per algoritmo, entrata in alto a sinistra e uscita in basso a destra.)

| Algoritmo | Vicoli ciechi (media) | Distanza entrata-uscita (media) |
|---|---|---|
| DFS iterativa | 41,8 | 154,0 |
| Kruskal | 121,6 | 57,1 |
| Wilson | 116,3 | 57,9 |

La DFS fa pochi vicoli ciechi e percorsi lunghi e tortuosi; Kruskal e Wilson molti vicoli ciechi corti e percorsi più brevi. Su un labirinto perfetto c'è un solo percorso verso l'uscita, quindi il criterio "percorsi distinti" ha senso solo per labirinti con cicli.

```python
import random

def labirinto_dfs(R, C, seed=None):
    rnd = random.Random(seed)
    visitate = {(0, 0)}
    stack = [(0, 0)]
    passaggi = set()
    while stack:
        cella = stack.pop()
        r, c = cella
        vicini = [(r + dr, c + dc) for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1))
                  if 0 <= r + dr < R and 0 <= c + dc < C and (r + dr, c + dc) not in visitate]
        if vicini:
            stack.append(cella)
            scelta = rnd.choice(vicini)
            passaggi.add(frozenset((cella, scelta)))
            visitate.add(scelta)
            stack.append(scelta)
    return passaggi
```
I criteri si calcolano mettendo i passaggi in un `networkx.Graph`: vicoli ciechi = nodi di grado 1, distanza = `nx.shortest_path_length(G, entrata, uscita)`, albero = `nx.is_tree(G)`.

## Grafi planari
- Un **grafo planare** si può disegnare nel piano **senza archi che si intersecano**
- La slide dice che "in linea generale non è possibile dimostrare in tempo lineare se un grafo è planare o meno". **Errore nella slide 15**: il test di planarità si fa in **tempo lineare** $O(n)$ (Hopcroft e Tarjan, 1974; in networkx `nx.check_planarity` / `nx.is_planar`). Le disuguaglianze seguenti sono solo condizioni **necessarie**, utili per escludere rapidamente la planarità
- Per un grafo **semplice, connesso e planare** con $n$ nodi ed $e$ archi:
  - se $n \ge 3$: $\;e \le 3n - 6$
  - se $n > 3$ e **non ci sono cicli di lunghezza 3**: $\;e \le 2n - 4$
- Figura: tre disegni di 4 nodi e 6 archi. Il primo è un quadrato con **entrambe le diagonali che si incrociano**; il secondo ha una diagonale interna e l'altra disegnata come **arco esterno**; il terzo è un triangolo con un nodo centrale collegato ai tre vertici
- La didascalia dice "il primo grafo a sinistra non è planare". **Errore nella slide 15**: tutti e tre sono lo **stesso grafo** $K_4$, che è **planare** (il secondo e il terzo lo disegnano senza incroci). Non è planare il primo **disegno**, non il grafo: la planarità è una proprietà del grafo, cioè l'esistenza di almeno un disegno senza incroci
- (Aggiunta, non nelle slide, verificata con networkx: $K_4$ ha $e = 6 \le 3\cdot 4 - 6 = 6$ ed è planare; $K_5$ ha $e = 10 > 9$, quindi non è planare; $K_{3,3}$ ha $e = 9 \le 12$, la prima condizione non basta, ma è bipartito, quindi senza triangoli, e $9 > 2\cdot 6 - 4 = 8$, quindi non è planare. Per il **teorema di Kuratowski** un grafo è planare se e solo se non contiene una suddivisione di $K_5$ o di $K_{3,3}$.)

## Generazione di grafi planari
- Esistono varie tecniche per generare grafi planari con particolari proprietà
- **Triangolazione di Delaunay**: per un insieme di punti $P$ nel piano è una triangolazione $DT(P)$ tale che **nessun punto di $P$ cada dentro il circumcerchio** di alcun triangolo di $DT(P)$
  - **massimizza il più piccolo** fra tutti gli angoli dei triangoli: tende a **evitare i triangoli stretti**
  - figura: punti triangolati con i circumcerchi dei triangoli, ciascuno vuoto di altri punti
  - (Aggiunta, non nelle slide: in Python `scipy.spatial.Delaunay(punti).simplices` dà i triangoli; il grafo risultante è planare. Su 30 punti casuali: 78 archi contro il limite $3n - 6 = 84$, e `nx.is_planar` conferma.)
- Molti algoritmi **non generano da zero**: partono da grafi esistenti e **aggiungono o rimuovono** vertici o archi
- Esempio: Chauhan et al., *Applied Network Science* (2019), **modello a V** per la generazione multilivello di reti planari:
  - **coarsening**: il grafo planare originale viene ridotto in una gerarchia di grafi sempre più grossolani
  - al livello più grossolano si fa **editing e fine tuning**, preservando le similarità delle proprietà a tutti i livelli
  - **uncoarsening**: si ripercorre la gerarchia al contrario, rifinendo fino a ottenere il **grafo planare sintetico**
  - il numero di livelli dipende dalla dimensione della rete in input e dall'input dell'utente

## Aggiunta: nomi nelle librerie
Non nelle slide, solo come riferimento per il progetto e la parte pratica dell'orale.
- **networkx**: `nx.grid_2d_graph(R, C)` (griglia di celle), `nx.is_tree`, `nx.shortest_path_length`, `nx.is_planar`, `nx.check_planarity` (restituisce anche l'immersione planare), `nx.complete_graph`, `nx.complete_bipartite_graph`
- **scipy**: `scipy.spatial.Delaunay`
- per i benchmark: fissare il **seed** (`random.Random(seed)`, `np.random.default_rng(seed)`) è il modo più semplice di garantire la **riproducibilità** delle istanze sintetiche
