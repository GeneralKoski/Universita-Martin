# 03 - Modeling programs

Fonte: `03 - Modeling programs.pdf`

## Programma di partenza e obiettivo
Il filo conduttore della lezione è questo programma:

```c
1 i = read();
2 if (i != 0)
3   j = 5 / i;
4 else
5   j = 0;
6 return;
```

- **Goal**: certificare che il programma è **safe** rispetto alla **division by zero** (divisione per zero).
- Idea: calcolare i **possibili valori** di ogni variabile, **per ogni program point** (punto di programma) e **per tutte le possibili esecuzioni**.
- Convenzione delle tabelle: il valore associato al punto $k$ è lo stato **prima** di eseguire l'istruzione $k$ (il punto 4, `else`, non compare).

## Posets in static analysis
- Il dominio dei valori di una variabile intera è $\langle \wp(\mathbb{Z}), \subseteq \rangle$, che è anzi un **lattice** (reticolo) $\langle \wp(\mathbb{Z}), \subseteq, \cup, \cap \rangle$.
- Tabella dei valori costruita passo passo:

| Program point | Valori |
|---|---|
| 1 | $i = \emptyset$ |
| 2 | $i = \{\dots, -1, 0, 1, \dots\} = \mathbb{Z}$ (dopo `read()` può valere qualunque intero) |
| 3 | $i = \{\dots, -1, 1, \dots\} = \mathbb{Z} \setminus \{0\}$ |
| 5 | $i = \{0\}$ |
| 6 | $i = \mathbb{Z}$, $j = \{-5, -2, -1, 0, 1, 2, 5\}$ |

### Come si calcola il punto 6: unione (join)
- Il punto 6 ha due predecessori: l'uscita del punto 3 e l'uscita del punto 5.
  - output pp 3: $j = \{-5, -2, -1, 0, 1, 2, 5\}$, cioè $5/i$ con $i \in \mathbb{Z}\setminus\{0\}$ e divisione intera troncata (5/1=5, 5/2=2, 5/3=5/4=5/5=1, 5/k=0 per k>5, e simmetrici per i negativi).
  - output pp 5: $j = \{0\}$.
- Il valore al punto 6 è l'**unione** $\cup$ dei due contributi: $\{-5,-2,-1,0,1,2,5\} \cup \{0\} = \{-5,-2,-1,0,1,2,5\}$.
- Una build intermedia mostra al punto 6 $j = \{\dots,-1,0,1,\dots\}$: anche questo è un sovrainsieme corretto, ma meno preciso. Il calcolo giusto è l'unione.

### Come si calcolano i punti 3 e 5: intersezione (filtro)
- Serve l'altra operazione del reticolo, l'intersezione $\cap$ (cerchiata nella slide).
- $\mathsf{filter}(i \mathrel{!=} 0) = \{\dots, -1, 1, \dots\}$, e il punto 3 si ottiene filtrando il punto 2:

$$3 = 2 \cap \mathsf{filter}(i \mathrel{!=} 0) = \mathbb{Z} \cap (\mathbb{Z}\setminus\{0\}) = \{\dots,-1,1,\dots\}$$

  (Nella slide c'è scritto $\mathsf{filter}(x \mathrel{!=} 0)$: la variabile è $i$, non $x$.)
- Analogamente $5 = 2 \cap \mathsf{filter}(i == 0) = \{0\}$.
- Morale: **join** ($\cup$, least upper bound) dove i cammini si riuniscono, **meet/filtro** ($\cap$) sulle guardie dei rami.

## Least upper bound in static analysis
- Stesso programma con input $i \in \{-1, 0, 1\}$, ma ora i valori si rappresentano con **intervalli**:

| Program point | Valori |
|---|---|
| 1 | $i = \emptyset$ |
| 2 | $i = [-1, 1]$ |
| 3 | $i = [-1, 1]$ |
| 5 | $i = [0, 0]$ |
| 6 | $i = [-1, 1]$, $j = [-5, 5]$ |

- Contributi al punto 6: da 3, $j = [-5, 5]$; da 5, $j = [0, 0]$.
- Una build mostra al punto 6 $j = [-10, 5]$: è un **upper bound** di $[-5,5]$ e $[0,0]$, ma non il **least** upper bound. La slide successiva lo corregge in $[-5, 5] = [-5,5] \sqcup [0,0]$, il più piccolo intervallo che li contiene entrambi.
- Lo **stato astratto** (abstract state) è modellato come una **funzione** dalle variabili ai valori astratti, es. $[i \mapsto [-1,1],\ j \mapsto [-5,5]]$.
- (Osservazione aggiunta: al punto 3 l'intervallo resta $[-1,1]$ perché un intervallo non può "bucare" lo 0; il filtro $i \mathrel{!=} 0$ non elimina nulla, quindi con gli intervalli l'analisi non riesce a certificare l'assenza di divisione per zero, mentre con $\wp(\mathbb{Z})$ sì. È la perdita di precisione dell'astrazione.)

## Fixpoints
Programma con un ciclo (la guardia `?` è non deterministica):

```c
1 i = 0;
2 while (?)
3   i++;
4 ...
```

Sistema di equazioni sul valore di `i` in ogni punto:

| Punto | Equazione |
|---|---|
| 1 | $\emptyset$ |
| 2 | $\{0\} \cup [\![ i\text{++} ]\!]\,3$ |
| 3 | $2$ |
| 4 | $2$ |

Il punto 2 (testa del ciclo) riceve sia il valore dopo `i = 0` sia il valore che torna dal corpo dopo `i++`. La soluzione è un **fixpoint** (punto fisso) del sistema.

### Iterazione in $\langle \wp(\mathbb{Z}), \subseteq, \cup, \cap \rangle$
Si parte da $\emptyset$ ovunque e ogni colonna si calcola dalla precedente:

| Punto | it 0 | it 1 | it 2 | it 3 | it 4 |
|---|---|---|---|---|---|
| 1 | $\emptyset$ | $\emptyset$ | $\emptyset$ | $\emptyset$ | $\emptyset$ |
| 2 | $\emptyset$ | $\{0\}$ | $\{0\}$ | $\{0,1\}$ | $\{0,1\}$ |
| 3 | $\emptyset$ | $\emptyset$ | $\{0\}$ | $\{0\}$ | $\{0,1\}$ |
| 4 | $\emptyset$ | $\emptyset$ | $\{0\}$ | $\{0\}$ | $\{0,1\}$ |

- "By **Kleene theorem**, the fixpoint exists, but we cannot compute it in this way...": la catena $\{0\} \subset \{0,1\} \subset \{0,1,2\} \subset \dots$ è infinita, quindi l'iterazione non termina. (Aggiunta: il least fixpoint, cioè $i \in \mathbb{N}$ nei punti 2, 3, 4, è il limite $\bigsqcup_n F^n(\bot)$ per Kleene; la sola esistenza la garantisce già Knaster-Tarski.)

### Iterazione nel dominio dei segni
- Reticolo dei segni: $\langle \{0, +, -, \bot, \top\}, \sqsubseteq, \sqcup, \sqcap, \top, \bot \rangle$, con $\bot$ sotto a $-$, $0$, $+$ e $\top$ sopra.
- Stesse equazioni, con $0$ al posto di $\{0\}$: $2 = 0 \sqcup [\![ i\text{++} ]\!]\,3$, partendo da $\bot$ ovunque.

| Punto | it 0 | it 1 | it 2 | ... | it 4 | it 5 |
|---|---|---|---|---|---|---|
| 1 | $\bot$ | $\bot$ | $\bot$ | ... | $\bot$ | $\bot$ |
| 2 | $\bot$ | $0$ | $\top$ | ... | $\top$ | $\top$ |
| 3 | $\bot$ | $+$ | $\top$ | ... | $\top$ | $\top$ |
| 4 | $\bot$ | $0$ | $\top$ | ... | $\top$ | $\top$ |

- Colonne 4 e 5 uguali: **Fixpoint!** Il dominio è finito, quindi l'iterazione termina.
- (Correzione: alla colonna 1 la slide riporta $3 = +$, che non segue dall'equazione $3 = 2$: con lo stesso schema della tabella su $\wp(\mathbb{Z})$ verrebbe $\bot$, oppure $0$ usando subito il valore nuovo di 2. Il $+$ è il valore di `i` **dopo** `i++`. Il punto fisso finale non cambia: $\top$ in 2, 3, 4.)
- (Osservazione aggiunta: si arriva a $\top$ perché $0 \sqcup + = \top$; il dominio non ha un elemento "$\geq 0$", quindi perde l'informazione che `i` non è mai negativo.)

## IMP
Linguaggio giocattolo del corso:

```
e ::= x | n | e1 opa e2
b ::= true | false | ¬b1 | b1 opb b2 | e1 opc e2
s ::= x := e; | skip | s1 s2 | if b then s1 else s2 | while b do s1
```

dove $n \in \mathbb{Z}$, $\mathrm{op}_a \in \{+, -, *, \div\}$, $\mathrm{op}_b \in \{\&\&, \|\}$, $\mathrm{op}_c \in \{==, >, <, \geq, \leq\}$.

## IMP concrete semantics
- Slide con solo il titolo: nel PDF non c'è contenuto (presumibilmente svolta alla lavagna).

## Trace semantics
- Figura 1: un'esecuzione è una **traiettoria discreta** $x(t)$ nel tempo; la semantica di un programma è l'insieme di tutte le possibili traiettorie ("possible discrete trajectories").
- Figura 2: insieme di tracce a tempo discreto ($0, 1, 2, \dots$) che partono da **initial states**, passano per **intermediate states** e terminano in **final states** (le **finite traces**), oppure non terminano mai (**infinite traces**).
- Serve una struttura di reticolo per la **trace semantics**:
  - una singola esecuzione è una traccia $\tau \in X^\infty$ (aggiunta: $X$ è l'insieme degli stati e $X^\infty$ l'insieme delle sequenze finite e infinite di stati);
  - la semantica concreta si modella con il reticolo $\langle \wp(X^\infty), \subseteq, \cup, \cap \rangle$.
- Come definirla (intuizione):
  - si calcola un singolo passo di computazione, ottenendo un insieme di **partial executions** (esecuzioni parziali);
  - si itera su di esse per calcolare i passi successivi;
  - fino a raggiungere un punto fisso.

## Final partial execution
- **Primo passo**: esecuzioni di lunghezza 1, cioè le tracce fatte dai soli stati iniziali.
- **Passo $i$-esimo**: esecuzioni di lunghezza $i$, unite alle tracce lunghe al più $i-1$.
- Fino a raggiungere un punto fisso.

## Least fixpoint computation
- Dato un programma $P$, la semantica di punto fisso si calcola partendo **dal basso** (least fixpoint):

$$\mathrm{lfp}^{\subseteq}_{\emptyset}\, F_P$$

- Così si ottiene l'insieme delle esecuzioni parziali.
- (Aggiunta, forma standard non presente nella slide: con $I$ stati iniziali e $\to$ relazione di transizione, $F_P(T) = I \cup \{\sigma_0 \dots \sigma_n \sigma' \mid \sigma_0 \dots \sigma_n \in T,\ \sigma_n \to \sigma'\}$; l'iterata $n$-esima da $\emptyset$ contiene le tracce lunghe al più $n$.)

## Example
- Slide con solo il titolo: nel PDF non c'è l'esempio.

## Trace semantics: cosa calcola
- La trace semantics così definita "calcola" tutte le esecuzioni parziali, comprese:
  - **blocking executions** (esecuzioni che si bloccano/terminano);
  - **infinite executions**;
  - **partial executions**.
- (Precisazione: il least fixpoint delle esecuzioni parziali contiene i prefissi finiti delle esecuzioni infinite, non le tracce infinite in sé; queste si recuperano come limiti dei prefissi.)
- In base allo scopo si può **astrarre**:
  - solo le esecuzioni bloccanti;
  - i **valori per ogni program point** (è ciò che si faceva con le tabelle all'inizio della lezione).

## An abstraction of the trace semantics
- Slide con solo il titolo: nel PDF non c'è contenuto.

## Da ricordare
- Un'analisi statica calcola, per ogni program point e per tutte le esecuzioni, un insieme di possibili valori: il dominio concreto naturale è il reticolo $\langle \wp(\mathbb{Z}), \subseteq, \cup, \cap \rangle$.
- **Join** ($\cup$ / $\sqcup$, least upper bound) dove i cammini confluiscono, **filtro** ($\cap$) sulle guardie: $3 = 2 \cap \mathsf{filter}(i \mathrel{!=} 0)$.
- Il lub deve essere il **minimo** dei maggioranti: $[-5,5] \sqcup [0,0] = [-5,5]$, non $[-10,5]$.
- Lo stato astratto è una funzione variabili → valori astratti.
- I cicli generano equazioni ricorsive: la soluzione è un **fixpoint**; su $\wp(\mathbb{Z})$ l'iterazione da $\emptyset$ non termina (catena infinita), su un dominio finito come i segni termina ma perde precisione ($0 \sqcup + = \top$).
- Con gli intervalli il filtro $i \mathrel{!=} 0$ non toglie lo 0 da $[-1,1]$: precisione persa rispetto a $\wp(\mathbb{Z})$.
- IMP: espressioni aritmetiche $e$, booleane $b$, statement $s$ (assegnamento, skip, sequenza, if, while).
- **Trace semantics**: tracce $\tau \in X^\infty$, reticolo $\langle \wp(X^\infty), \subseteq, \cup, \cap \rangle$, esecuzioni parziali come $\mathrm{lfp}^{\subseteq}_{\emptyset} F_P$; da essa si ottengono per astrazione semantiche più semplici (esecuzioni bloccanti, valori per program point).
