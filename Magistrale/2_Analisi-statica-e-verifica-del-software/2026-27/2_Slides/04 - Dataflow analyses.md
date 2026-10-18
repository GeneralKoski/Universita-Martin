# 04 - Dataflow analyses

Fonte: `04 - Dataflow analyses.pdf`

## Control Flow Graph (CFG)
- Nella **dataflow analysis** (e in altre analisi) i programmi si rappresentano tipicamente come **control flow graph** (CFG, grafo di controllo di flusso).
- Esempio:

```c
1 y = a - b;
2 x = y + b;
3 while (y > a + b)
4   y = y - x * x;
```

```
   [1] y:=a-b
      |
   [2] x:=y+b
      |
+->[3] y>a+b ---no---> (uscita)
|     | yes
|  [4] y:=y-x*x
|     |
+-----+
```

- Ogni statement è un **blocco etichettato** (labeled block); ogni blocco ha uno o due archi uscenti (due solo per le guardie).
- Definizione:
  - i **nodi** sono singoli statement, identificati da $i \in \mathbb{N}$;
  - gli **archi** sono coppie $(i_1, i_2) \in \mathbb{N} \times \mathbb{N}$.
- Dato un CFG $G$:
  - $\mathrm{nodes}(G)$: insieme degli indici di tutti i blocchi di $G$;
  - $\mathrm{stmt}(G, i)$: lo statement contenuto nel blocco $i$ di $G$;
  - $\mathrm{edges}(G) \subseteq \mathbb{N} \times \mathbb{N}$: gli archi.

## Dataflow analyses
- Tecnica tradizionale per le **compiler optimizations** (ottimizzazioni dei compilatori).
- I programmi sono rappresentati come CFG.
- Approccio **basato su equazioni**:
  - relazioni fra gli **entry state** e gli **exit state** (stato in ingresso e in uscita) di ogni blocco;
  - si risolvono le equazioni, ottenendo una **over-approximation** (sovra-approssimazione) della proprietà di interesse.
- La proprietà di interesse è di solito semplice e orientata a ottimizzare l'esecuzione (es. evitare di calcolare due volte la stessa espressione).

## Available expressions
Definizione:

> "For each program point, which expressions **must** have already been computed, and not later modified, on **all paths** to the program point"

(Nelle slide compare il refuso "myst" per "must".)

- Utile per:
  - evitare di ricalcolare due volte la stessa espressione;
  - memorizzarla in un registro temporaneo;
  - ci si concentra sulle espressioni **aritmetiche**.
- Intuizione **gen/kill**:
  - quando $x$ viene assegnata, tutte le espressioni che contengono $x$ non sono più disponibili (**kill**);
  - quando $x$ viene assegnata, le espressioni calcolate diventano disponibili (**gen**). (Precisazione: solo quelle che **non** contengono $x$, come dice la definizione formale più avanti.)

### Esempio (slide 7)
- `x := x + 1`: genererebbe $\{x+1\}$, ma l'assegnamento a `x` uccide le espressioni che contengono `x`, quindi il risultato è $\emptyset$.
- Sequenza con le espressioni disponibili dopo ogni blocco:

| Blocco | Disponibili dopo |
|---|---|
| `x := a+b` | $\{a+b\}$ |
| `y := x+1` | $\{a+b, x+1\}$ |
| `x := y+1` | $\{a+b, y+1\}$ ($x+1$ è uccisa, $y+1$ è generata) |

### Formalizzazione
- Per ogni program point (cioè per ogni blocco) si tiene l'insieme delle espressioni disponibili: lo stato dell'analisi è un elemento di $\wp(AE)$, dove $AE$ è l'insieme delle espressioni aritmetiche del programma.
- $\mathrm{AExp}(e)$: espressioni aritmetiche **non banali** in $e$ (cioè non variabili o costanti singole); $\mathrm{AExp}(b)$: idem nella guardia $b$.
- $\mathrm{FV}(a)$: **free variables** (variabili libere) di $a$.
- Funzioni per l'assegnamento:

$$\mathrm{gen}(x := e) = \{ a \in \mathrm{AExp}(e) \mid x \notin \mathrm{FV}(a) \}$$

$$\mathrm{kill}(x := e) = \{ a \in AE \mid x \in \mathrm{FV}(a) \}$$

- (Correzione: la slide scrive $\mathrm{kill}(x := e) = \{ a \in \mathrm{AExp}(e) \mid x \in \mathrm{FV}(a) \}$. Così si ucciderebbero solo le espressioni contenute in $e$: per esempio `x := 5` non ucciderebbe `x+1`. Vanno uccise tutte le espressioni del programma che contengono $x$, ed è proprio la forma $\{a \in AE \mid \dots\}$ che le slide usano poi negli esempi.)
- (Aggiunta, dal libro di Nielson-Nielson-Hankin: per una guardia $b$ si ha $\mathrm{kill}(b) = \emptyset$ e $\mathrm{gen}(b) = \mathrm{AExp}(b)$; per `skip` entrambi vuoti.)

### Entry and exit states
- Le espressioni disponibili all'ingresso di un blocco sono quelle disponibili all'uscita del blocco precedente.
- Available expressions è un'analisi **forward**: l'informazione si propaga dagli entry agli exit state.

$$\mathrm{entry}(pp) = \mathrm{exit}(\mathrm{predecessor}(pp))$$

  (Vale così solo con un unico predecessore; il caso generale è il join qui sotto.)
- Esempio (slide 10), sequenza `1: x:=a+b`, `2: y:=x+1`, `3: x:=y+1`:
  - $\mathrm{entry}(1) = \emptyset$, $\mathrm{exit}(1) = \{a+b\}$;
  - $\mathrm{entry}(2) = \{a+b\}$, $\mathrm{exit}(2) = \{a+b, x+1\}$;
  - $\mathrm{exit}(3) = \{a+b, y+1\}$.

### Join
- Nel punto in cui due cammini confluiscono conta la parte "on all paths" della definizione.
- Esempio (slide 12-14) con CFG `1: y:=a-b`, `2: x:=y+b`, `3: y>a+b`, `4: y:=y-1` (ciclo 3 → 4 → 3):

$$\mathrm{exit}(2) = \{a-b,\ y+b\} \qquad \mathrm{exit}(4) = \{a-b,\ a+b\}$$

$$\mathrm{entry}(3) = \mathrm{exit}(2) \cap \mathrm{exit}(4) = \{a-b\}$$

- Available expressions è una **must analysis**: se un'espressione risulta disponibile, lo è di sicuro. Per questo al join si usa l'**intersezione**.

### Equazioni generali
Per un blocco $i$ del CFG $G$:

$$\mathrm{entry}(i) = \bigcap \{ \mathrm{exit}(i') \mid (i', i) \in \mathrm{edges}(G) \} \qquad (\mathrm{entry}(1) = \emptyset)$$

$$\mathrm{exit}(i) = \big(\mathrm{entry}(i) \setminus \mathrm{kill}(\mathrm{stmt}(G, i))\big) \cup \mathrm{gen}(\mathrm{stmt}(G, i))$$

Poi si itera fino a raggiungere un punto fisso.

### Esempio: sequenza di tre blocchi (slide 16)
CFG `1: y:=a-b`, `2: x:=y+b`, `3: y:=x+2`:

| Blocco | entry | exit |
|---|---|---|
| 1 | $\emptyset$ | $(\mathrm{entry}(1) \setminus \{a \in AE \mid y \in FV(a)\}) \cup \{a-b\}$ |
| 2 | $\mathrm{exit}(1)$ | $(\mathrm{entry}(2) \setminus \{a \in AE \mid x \in FV(a)\}) \cup \{y+b\}$ |
| 3 | $\mathrm{exit}(2)$ | $(\mathrm{entry}(3) \setminus \{a \in AE \mid y \in FV(a)\}) \cup \{x+2\}$ |

(Soluzione, aggiunta: $\mathrm{exit}(1) = \{a-b\}$, $\mathrm{exit}(2) = \{a-b, y+b\}$, $\mathrm{exit}(3) = \{a-b, x+2\}$, perché `y:=x+2` uccide $y+b$.)

### Esempio: il CFG con il ciclo (slide 17)
CFG `1: y:=a-b`, `2: x:=y+b`, `3: y>a+b`, `4: y:=y-x*x`:

| Blocco | entry | exit |
|---|---|---|
| 1 | $\emptyset$ | $(\mathrm{entry}(1) \setminus \mathrm{kill}(y := a-b)) \cup \mathrm{gen}(y := a-b)$ |
| 2 | $\mathrm{exit}(1)$ | $(\mathrm{entry}(2) \setminus \mathrm{kill}(x := y+b)) \cup \mathrm{gen}(x := y+b)$ |
| 3 | $\mathrm{exit}(2) \cap \mathrm{exit}(4)$ | $(\mathrm{entry}(3) \setminus \mathrm{kill}(y > a+b)) \cup \mathrm{gen}(y > a+b)$ |
| 4 | $\mathrm{exit}(3)$ | $(\mathrm{entry}(4) \setminus \mathrm{kill}(y := y-x*x)) \cup \mathrm{gen}(y := y-x*x)$ |

Soluzione (aggiunta, calcolata con l'algoritmo della sezione seguente). $AE = \{a-b,\ y+b,\ a+b,\ x*x,\ y-x*x\}$; si parte con tutti gli exit a $AE$.
- $\mathrm{kill}(y := y-x*x) = \{y+b, y-x*x\}$, $\mathrm{gen}(y := y-x*x) = \{x*x\}$ ($y-x*x$ contiene $y$, quindi non è generata); $\mathrm{kill}(x := y+b) = \{x*x, y-x*x\}$.
- Primo giro: $\mathrm{exit}(1) = \{a-b\}$, $\mathrm{exit}(2) = \{a-b, y+b\}$, $\mathrm{entry}(3) = \{a-b,y+b\} \cap AE = \{a-b, y+b\}$, $\mathrm{exit}(3) = \{a-b, y+b, a+b\}$, $\mathrm{exit}(4) = \{a-b, a+b, x*x\}$.
- Secondo giro: $\mathrm{entry}(3) = \{a-b,y+b\} \cap \{a-b,a+b,x*x\} = \{a-b\}$, $\mathrm{exit}(3) = \{a-b, a+b\}$, $\mathrm{exit}(4) = \{a-b, a+b, x*x\}$: invariato, punto fisso.

| Blocco | entry | exit |
|---|---|---|
| 1 | $\emptyset$ | $\{a-b\}$ |
| 2 | $\{a-b\}$ | $\{a-b, y+b\}$ |
| 3 | $\{a-b\}$ | $\{a-b, a+b\}$ |
| 4 | $\{a-b, a+b\}$ | $\{a-b, a+b, x*x\}$ |

### Algoritmo iterativo (worklist)
```
 1: for all i ∈ nodes(G) do
 2:     exit(i) ← AE                       // we know nothing at the beginning
 3: end for
 4: entry(1) ← ∅                           // no expression is available at the entry node
 5: exit(1) ← (entry(1) \ kill(stmt(G,1))) ∪ gen(stmt(G,1))
 6: changed ← nodes(G) \ {1}               // changed contains the nodes to be evaluated
 7: while changed ≠ ∅ do
 8:     pick i ∈ changed
 9:     changed ← changed \ {i}
10:     entry(i) ← AE                      // compute the entry state
11:     for all p such that (p, i) ∈ edges(G) do
12:         entry(i) ← entry(i) ∩ exit(p)
13:     end for
14:     exit(i) ← (entry(i) \ kill(stmt(G,i))) ∪ gen(stmt(G,i))   // compute the exit state
15:     if exit(i) changed then            // update the set of nodes that have to be evaluated again
16:         for all p such that (i, p) ∈ edges(G) do
17:             changed ← changed ∪ {p}
18:         end for
19:     end if
20: end while
```

- `changed` è la **worklist**: i nodi da (ri)valutare. Un nodo torna in lista solo se l'exit di un suo predecessore è cambiato.
- Inizializzare gli exit a $AE$ (l'elemento più alto per $\subseteq$, il $\bot$ del reticolo ordinato con $\supseteq$) è la scelta giusta per una must analysis: l'intersezione poi può solo togliere.
- (Nella slide compaiono sia $G$ sia `cfg` per indicare lo stesso grafo: è lo stesso oggetto.)

## Other dataflow analyses (dal corso di compilatori)
- **Live variables**: "For each program point, which variables **may** be live at the exit from the program point. A variable is live if its content will be read in **some path** starting from the program point."
- **Reaching definitions**: "For each program point, which assignments **may** have been made and not overwritten, when program execution reaches this point along **some path**."
- **Very busy expressions**: "For each program point, which expressions **must** be very busy at the exit from the point. An expression is very busy if it will be always used in **all paths** starting from a label before any of the variables occurring in it are redefined."

### Classificazione
| | **Possible** (may) | **Definite** (must) |
|---|---|---|
| **Forward** | Reaching definitions | Available expressions |
| **Backward** | Live variables | Very busy expressions |

(Nella slide: "Foward" e "Backword", refusi per Forward e Backward.)

- **Possible**: "may", "some paths" (al join si usa $\cup$).
- **Definite**: "must", "all paths" (al join si usa $\cap$).
- **Forward**: "have been", "to the pp" (si propaga dall'entry all'exit).
- **Backward**: "exit", "from the pp" (si propaga dall'exit all'entry, seguendo gli archi al contrario).
- Si può definire un **algoritmo generico** parametrico su kill, gen, modo di unire gli stati ai punti di join, ecc.: è il **monotone framework** (corso di compilatori).

## Lattices in dataflow analyses
Notazione $\langle L, \sqsubseteq, \bot, \top, \sqcup, \sqcap \rangle$:
- Available expressions: $\langle \wp(AE), \supseteq, AE, \emptyset, \cap, \cup \rangle$ (ordine rovesciato: $\bot = AE$, lub $= \cap$).
- Live variables: $\langle \wp(Var), \subseteq, \emptyset, Var, \cup, \cap \rangle$.
- Reaching definitions e Very busy expressions: "..." (lasciati per esercizio).
- I domini di tutte le dataflow analyses sono **complete lattices** (reticoli completi) e devono soddisfare l'**ACC** (ascending chain condition), che garantisce la terminazione dell'iterazione.
- Correttezza e terminazione si possono dimostrare (fuori programma, corso di compilatori).
- Si possono modellare **tutte** le analisi statiche come dataflow analyses? **No**.

## Distributive analyses
- Dati $\langle \wp(X), \subseteq, \emptyset, X, \cup, \cap \rangle$ e $f : \wp(X) \to \wp(X)$, $f$ è **distributiva** se

$$f(x \cup y) = f(x) \cup f(y)$$

  (Nella slide "f is distributive is": va letto "if".)
- "All dataflow analyses are distributive analysis (even when lub is $\cap$)", cioè anche quando il lub è l'intersezione, come in available expressions. (Precisazione: vale per le analisi gen/kill viste sopra, perché $f(S) = (S \setminus \mathit{kill}) \cup \mathit{gen}$ distribuisce sia su $\cup$ sia su $\cap$; constant propagation, qui sotto, è il controesempio.)
- Le analisi distributive sono "facili":
  - tracciano **come** viene eseguita la computazione: variabili assegnate, espressioni calcolate;
  - **non** tracciano **cosa** calcola il programma.
- Tutte le analisi "difficili" non sono distributive, e spesso non si possono formalizzare come dataflow analyses: per questo è stata introdotta l'**abstract interpretation**.

## Constant propagation
> "For each program point, whether or not a variable has a constant value whenever an execution reaches that point."

- **Constant propagation non è un'analisi distributiva.**
- Dominio (reticolo piatto):

$$\mathsf{CP} = \langle \{\bot\} \cup \mathbb{Z} \cup \{\top\}, \sqsubseteq, \sqcup, \sqcap, \bot, \top \rangle$$

```
          ⊤
  / /   |   \ \
... -2 -1 0 1 2 ...
  \ \   |   / /
          ⊥
```

- Controesempio: il blocco $f$ = `x := y + z` ha due predecessori con stati

$$s_0 = [y \mapsto 1,\ z \mapsto -1] \qquad s_1 = [y \mapsto 0,\ z \mapsto 0]$$

- Se fosse distributiva varrebbe $f(s_0 \sqcup s_1) = f(s_0) \sqcup f(s_1)$. Invece:

$$f(s_0 \sqcup s_1) = f([y \mapsto \top, z \mapsto \top]) = [x \mapsto \top,\ y \mapsto \top,\ z \mapsto \top]$$

$$f(s_0) \sqcup f(s_1) = [x \mapsto 0, y \mapsto 1, z \mapsto -1] \sqcup [x \mapsto 0, y \mapsto 0, z \mapsto 0] = [x \mapsto 0,\ y \mapsto \top,\ z \mapsto \top]$$

- Unire prima e applicare dopo perde la correlazione fra $y$ e $z$ ($y + z = 0$ su entrambi i cammini): si ottiene solo $f(s_0 \sqcup s_1) \sqsupseteq f(s_0) \sqcup f(s_1)$, cioè meno precisione.

## Esempio aperto: interval analysis
- La slide chiede: "Is interval analysis a distributive analysis?" (nella slide "distribute"). La risposta non è nel PDF.
- (Risposta aggiunta: no. Con lo stesso blocco `x := y + z` e $s_0 = [y \mapsto [1,1], z \mapsto [-1,-1]]$, $s_1 = [y \mapsto [0,0], z \mapsto [0,0]]$: $f(s_0 \sqcup s_1)$ dà $x \mapsto [0,1] + [-1,0] = [-1,1]$, mentre $f(s_0) \sqcup f(s_1)$ dà $x \mapsto [0,0]$. In più già il lub perde informazione: $[0,0] \sqcup [2,2] = [0,2]$ contiene anche 1.)

## Da ricordare
- **CFG**: nodi = singoli statement etichettati, archi = coppie di etichette; $\mathrm{nodes}(G)$, $\mathrm{stmt}(G,i)$, $\mathrm{edges}(G)$.
- **Dataflow analysis**: nata per le ottimizzazioni dei compilatori, si basa su equazioni fra entry ed exit di ogni blocco, risolte per iterazione fino al punto fisso, e dà una sovra-approssimazione.
- **Available expressions**: forward, must; stato in $\wp(AE)$; $\mathrm{gen}(x := e) = \{a \in \mathrm{AExp}(e) \mid x \notin \mathrm{FV}(a)\}$, $\mathrm{kill}(x := e) = \{a \in AE \mid x \in \mathrm{FV}(a)\}$; $\mathrm{entry}(i) = \bigcap$ degli exit dei predecessori, $\mathrm{exit}(i) = (\mathrm{entry}(i) \setminus \mathrm{kill}) \cup \mathrm{gen}$.
- Algoritmo a **worklist**: exit inizializzati ad $AE$, $\mathrm{entry}(1) = \emptyset$, si rivalutano solo i successori dei nodi il cui exit è cambiato.
- Quadrato delle quattro analisi: reaching definitions (forward/may), available expressions (forward/must), live variables (backward/may), very busy expressions (backward/must). May → $\cup$, must → $\cap$. Il monotone framework le generalizza.
- Reticoli: AE = $\langle \wp(AE), \supseteq, AE, \emptyset, \cap, \cup \rangle$, LV = $\langle \wp(Var), \subseteq, \emptyset, Var, \cup, \cap \rangle$; reticoli completi con ACC, quindi l'analisi termina.
- **Distributività** $f(x \sqcup y) = f(x) \sqcup f(y)$: vale per le analisi gen/kill, che seguono *come* si calcola e non *cosa*. **Constant propagation** e **intervalli** non sono distributive: unendo gli stati prima si perde precisione. Le analisi non distributive richiedono l'**abstract interpretation**.
