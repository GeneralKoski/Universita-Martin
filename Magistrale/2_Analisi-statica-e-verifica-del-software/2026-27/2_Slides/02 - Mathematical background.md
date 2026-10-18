# 02 - Mathematical background

Fonte: `02 - Mathematical background.pdf`

Lezione 2 del corso **Static analysis and software verification** (Vincenzo Arceri, UniPR): il bagaglio matematico (insiemi, ordini, reticoli, funzioni, catene, punti fissi) su cui poggiano dataflow analysis e abstract interpretation.

## Notazione insiemistica
- Definizione informale di **set** (insieme): *"A set is a collection of well defined and distinct objects, considered as an object in its own right"*.
- Dato un insieme $S$:
  - appartenenza: $s \in S$
  - **subset** (sottoinsieme): $S_1 \subseteq S_2 \triangleq \forall s \in S_1 \implies s \in S_2$
  - **union** (unione): $S_1 \cup S_2 = \{s \mid s \in S_1 \lor s \in S_2\}$
  - **intersection** (intersezione): $S_1 \cap S_2 = \{s \mid s \in S_1 \land s \in S_2\}$
- Analogia **insiemi ≈ logica**:
  - sottoinsieme ≈ implicazione
  - unione ≈ disgiunzione (or)
  - intersezione ≈ congiunzione (and)

## Partial order
Un **partial order** (ordine parziale) $\sqsubseteq$ su un insieme $X$ è una relazione:
- **Reflexive** (riflessiva): $\forall x \in X \implies x \sqsubseteq x$
- **Anti-symmetric** (antisimmetrica): $\forall x, y \in X .\ x \sqsubseteq y \land y \sqsubseteq x \implies x = y$
- **Transitive** (transitiva): $\forall x, y, z \in X .\ x \sqsubseteq y \land y \sqsubseteq z \implies x \sqsubseteq z$

**Esempio** (informale): $\leq$ su $\mathbb{Z}$.
- Ogni intero è uguale a sé stesso, quindi è minore o uguale a sé stesso (riflessività).
- Se $i_1 \leq i_2$ e $i_2 \leq i_1$, allora $i_1$ e $i_2$ sono lo stesso intero (antisimmetria).
- Se $i_1 \leq i_2$ e $i_2 \leq i_3$, allora $i_1 \leq i_3$ (transitività).

## Powerset
- Il **powerset** (insieme delle parti) di $X$ è l'insieme di tutti i sottoinsiemi di $X$, indicato con $\wp(X)$. (Nella slide c'è scritto "the powerset of $S$ ... subsets of $X$": è un refuso, l'insieme è sempre $X$.)
- Esempi:
  - $\wp(\varnothing) = \{\varnothing\}$, che **non** è $\varnothing$
  - $\wp(\mathbb{Z}) = \{\varnothing, \{0\}, \{1\}, \{0,1\}, \dots, \mathbb{Z}\}$
- Cardinalità: $|X| = n \implies |\wp(X)| = 2^n$
  - $|\wp(\varnothing)| = 1$
  - $|\wp(\{0,1\})| = 4$

### $\subseteq$ su $\wp(X)$ è un ordine parziale
- riflessivo: $\forall X_1 \in \wp(X) .\ X_1 \subseteq X_1$
- antisimmetrico: $\forall X_1, X_2 \in \wp(X) .\ X_1 \subseteq X_2 \land X_2 \subseteq X_1 \Rightarrow X_1 = X_2$
- transitivo: $\forall X_1, X_2, X_3 \in \wp(X) .\ X_1 \subseteq X_2 \land X_2 \subseteq X_3 \Rightarrow X_1 \subseteq X_3$

Un insieme $X$ dotato di un ordine parziale $\sqsubseteq$ è un **poset** (partially ordered set), indicato con $\langle X, \sqsubseteq \rangle$.

### Esercizi (domande della slide, senza soluzione)
1. $\supseteq$ su $\wp(X)$ è un ordine parziale?
2. L'inverso di un ordine parziale è un ordine parziale?
3. Altri esempi di poset?

(Aggiunta mia, risposte brevi: 1 e 2 sì, perché riflessività, antisimmetria e transitività restano vere scambiando i due lati della relazione; $\supseteq$ è proprio l'inverso di $\subseteq$. Per la 3: $\langle \mathbb{Z}, \geq \rangle$, $\langle \mathbb{N}, \mid \rangle$ con la divisibilità, le stringhe con l'ordine di prefisso.)

## Hasse diagrams
- Sono **solo una rappresentazione grafica dei poset**.
- Dato $\langle X, \sqsubseteq \rangle$, una linea che collega $x$ (sotto) e $y$ (sopra) significa che:
  - $x \sqsubset y$
  - $\nexists z \in X .\ x \sqsubset z \sqsubset y$ (non c'è nulla in mezzo: si disegnano solo le relazioni "immediate", il resto si ricava per transitività)
- Più in alto $\implies$ più grande; un livello più in alto $\implies$ "immediatamente" più grande.
- **Poset inverso**: il diagramma ruotato di 180°.

**Esempi** (slide "Hasse diagrams - Examples"):
- A sinistra un frammento di $\langle \wp(\mathbb{Z}), \subseteq \rangle$: in basso $\varnothing$, sopra $\{-1\}, \{0\}, \{1\}$, poi $\{-1,0\}, \{0,1\}, \{-1,1\}$, poi $\{-1,0,1\}$; linee tratteggiate salgono fino a $\mathbb{Z}$ in cima (indicano gli infiniti altri sottoinsiemi).
- A destra lo stesso diagramma ruotato di 180° (poset inverso, ordinato da $\supseteq$): $\varnothing$ in cima e $\mathbb{Z}$ in fondo.

## Upper and lower bounds
Dato un poset $\langle X, \sqsubseteq \rangle$ e $S \subseteq X$:
- $s \in X$ è un **upper bound** (maggiorante) di $S$ se $\forall s' \in S .\ s \sqsupseteq s'$
- $s$ è il **least upper bound** (**lub**, minimo dei maggioranti) di $S$ se è un upper bound e $\forall s' \in UB .\ s \sqsubseteq s'$, dove $UB$ è l'insieme degli upper bound di $S$
- $s \in X$ è un **lower bound** (minorante) di $S$ se $\forall s' \in S .\ s \sqsubseteq s'$
- $s$ è il **greatest lower bound** (**glb**, massimo dei minoranti) di $S$ se è un lower bound e $\forall s' \in LB .\ s' \sqsubseteq s$, dove $LB$ è l'insieme dei lower bound di $S$

### Esempio sul diagramma di riferimento
Il diagramma usato in tutte le slide successive (dal basso verso l'alto):

```
            ⊤
           / \
          h   i
         / \ / \
        e   f   g
       / \ / \ / \
      a   b   c   d
       \  |   |  /
          ⊥
```

Archi: $\bot$ sotto $a, b, c, d$; $e$ sopra $a, b$; $f$ sopra $b, c$; $g$ sopra $c, d$; $h$ sopra $e, f$; $i$ sopra $f, g$; $\top$ sopra $h, i$.

- **lub**: con $S = \{f, g, b, c, d\}$ (cerchiato in rosso; il risultato è lo stesso per $\{b, c, d\}$) gli upper bound sono $\{i, \top\}$ (cerchiati in verde) e il lub è $i$ (indicato dalla freccia).
- **glb**: con $S = \{i, f, g\}$ i lower bound sono $\{c, \bot\}$ e il glb è $c$.

### Esercizio
- In $\langle \wp(X), \subseteq \rangle$, con $S_1, S_2 \in \wp(X)$: $S_1 \cup S_2$ è il lub di $\{S_1, S_2\}$?
- In $\langle \wp(X), \subseteq \rangle$, con $S_1, S_2 \in \wp(X)$: $S_1 \cap S_2$ è il glb di $\{S_1, S_2\}$?

(Aggiunta mia: sì a entrambe. $S_1 \cup S_2$ contiene entrambi ed è contenuto in ogni insieme che li contiene entrambi; simmetricamente per $\cap$. È quanto verrà detto nella sezione "Set lattice".)

## Supremum and infimum
- **Supremum**, **top**, **maximum** di $S$: un $x \in S$ tale che $x$ è il lub di $S$.
- **Infimum**, **bottom**, **minimum** di $S$: un $x \in S$ tale che $x$ è il glb di $S$.

(Precisazione: la slide mette sullo stesso piano supremum e maximum. Nell'uso standard il **supremum** è il lub, che può anche non appartenere a $S$, mentre il **maximum** è il lub quando appartiene a $S$; idem per infimum e minimum. La definizione della slide, con $x \in S$, è quella di massimo e minimo.)

Esempi sul diagramma di riferimento:
- $S = \{f, g, b, c, d\}$: **top?** No, $f$ e $g$ sono incomparabili e il lub $i$ non sta in $S$. **bottom?** No, $b, c, d$ sono incomparabili e il glb $\bot$ non sta in $S$.
- $S = \{i, f, g, c\}$: **top** = $i$ (è in $S$ ed è il lub), **bottom** = $c$ (è in $S$ ed è il glb).

## Properties of lub and glb
Dato un poset $\langle X, \sqsubseteq \rangle$:
- $\sqcup$ indica il lub su $X$ (**join**), $\sqcap$ il glb su $X$ (**meet**).
- Se $\sqcup$ / $\sqcap$ esiste, è **unico** (per antisimmetria).
- $\sqcup X$ esiste se e solo se $X$ ha un elemento **top** $\top$, e allora $\sqcup X = \top$.
- $\sqcap X$ esiste se e solo se $X$ ha un elemento **bottom** $\bot$, e allora $\sqcap X = \bot$.

Esempi:
- Poset senza top e bottom: in alto $h, i$; in mezzo $e, f, g$; in basso $b, c$ (archi $h$-$e$, $h$-$f$, $i$-$f$, $i$-$g$, $e$-$b$, $f$-$b$, $f$-$c$, $g$-$c$). Qui $e \sqcup g$ **non esiste** ($e$ sta solo sotto $h$, $g$ solo sotto $i$: nessun upper bound comune) e $e \sqcap g$ **non esiste** ($e$ sta sopra solo $b$, $g$ solo sopra $c$).
- Stesso poset con aggiunti $\top$ sopra $h, i$ e $\bot$ sotto $b, c$: ora $e \sqcup g = \top$ ed $e \sqcap g = \bot$.

## Lattice
Un poset $\langle X, \sqsubseteq \rangle$ è un **lattice** (reticolo) se e solo se:
- $\forall x, y \in X .\ x \sqcup y$ esiste (**join semi lattice**)
- $\forall x, y \in X .\ x \sqcap y$ esiste (**meet semi lattice**)

In un lattice:
$$x \sqsubseteq y \iff x \sqcup y = y \iff x \sqcap y = x$$
cioè **l'ordine parziale induce lub e glb** (e viceversa).

Esempi grafici:
- **Join semi lattice**: $\top$ sopra $b$ e $c$ (esiste $b \sqcup c = \top$, ma non $b \sqcap c$).
- **Meet semi lattice**: $\bot$ sotto $b$ e $c$ (esiste $b \sqcap c = \bot$, ma non $b \sqcup c$).
- **Lattice**: $\bot$ sotto $b, c$ e $\top$ sopra, esistono entrambi.
- Nel poset con $\top$ e $\bot$ della sezione precedente: $e \sqsubseteq h$, infatti $e \sqcup h = h$ ed $e \sqcap h = e$.

## Set lattice
- Le operazioni insiemistiche formano un lattice, indicato con $\langle \wp(X), \subseteq, \cup, \cap \rangle$:
  - poset $\langle \wp(X), \subseteq \rangle$
  - lub $\cup$, glb $\cap$
  - top $X$, bottom $\varnothing$
- Se $X$ è finito, il lattice ha **finite height** (altezza finita).
- Un lattice **non ha necessariamente top e bottom**: ad esempio $\langle \mathbb{Z}, \leq, max, min \rangle$ (catena infinita $\dots \leq -1 \leq 0 \leq 1 \leq \dots$ in entrambe le direzioni).
- Disegno di $\langle \wp(\{-1,0,1\}), \subseteq \rangle$: $\varnothing$ in basso, poi i singoletti $\{-1\}, \{0\}, \{1\}$, poi le coppie $\{-1,0\}, \{0,1\}, \{-1,1\}$, in cima $\{-1,0,1\}$ (un cubo, altezza 3).

## Complete lattice
$\langle X, \sqsubseteq, \sqcup, \sqcap \rangle$ è un **complete lattice** (reticolo completo) se:
- **qualsiasi** sottoinsieme di $X$ (anche infinito) ha un lub in $X$
- ha un elemento bottom

Esempi:
- $\langle \mathbb{Z}, \leq, max, min \rangle$ è un lattice ma **non** è completo (es. $\mathbb{Z}$ stesso, o $\mathbb{N}$, non ha lub).
- $\langle \mathbb{Z} \cup \{-\infty, +\infty\}, \leq, max, min \rangle$ è un complete lattice: catena $-\infty \leq \dots \leq -1 \leq 0 \leq 1 \leq \dots \leq +\infty$.

### Proprietà
- Un complete lattice ha un bottom $\bot$ e un top $\top$ e si indica con $\langle X, \sqsubseteq, \bot, \top, \sqcup, \sqcap \rangle$.
- I lattice **finiti** sono anche completi.
- $\sqcup$ induce $\sqcap$: $\sqcap S = \sqcup \{y \mid \forall x \in S .\ y \sqsubseteq x\}$ (il glb è il lub dei lower bound).
- $\sqcap$ induce $\sqcup$: $\sqcup S = \sqcap \{y \mid \forall x \in S .\ x \sqsubseteq y\}$ (il lub è il glb degli upper bound).
- Esempio sul diagramma di riferimento: $S = \{f, g, c\}$; gli upper bound $\{y : \forall x \in S : x \sqsubseteq y\}$ sono $\{i, \top\}$, il loro glb è $i$, quindi $\sqcup S = i$.

(Nota mia: la richiesta "ha un bottom" è già implicata dalla prima, perché $\sqcup \varnothing = \bot$.)

## Relations
- **Cartesian product** (prodotto cartesiano): $X \times Y = \{(x, y) \mid x \in X \land y \in Y\}$
- Una **relation** (relazione) è $R \subseteq X \times Y$.
- Notazione comune: $x\ r\ y$ per indicare $(x, y) \in r$ (la slide usa $R$ e $r$ per la stessa relazione).
- Un ordine parziale è una relazione.
- Esempi disegnati: il diagramma di Hasse di $\langle \wp(\{0,1\}), \subseteq \rangle$ ($\varnothing$ sotto $\{0\}, \{1\}$, sotto $\{0,1\}$) e una circonferenza nel piano cartesiano: entrambi sono relazioni.

## Functions (or maps)
- Le **functions** (funzioni, o mappe) sono un tipo particolare di relazione:
$$\forall (x, y) \in r .\ \nexists (x', y') \in r .\ x = x' \land y \neq y'$$
  cioè ogni input ha **al più un** output (la slide dice "definite at most once on a input", leggi "defined").
- Notazione comune: $r(x) = y$ per indicare $(x, y) \in r$.
- Un ordine parziale **non** è una funzione (es. in $\wp(\{0,1\})$ l'insieme $\varnothing$ è in relazione con $\{0\}$, $\{1\}$ e $\{0,1\}$).
- Una circonferenza nel piano cartesiano **non** è una funzione (a una $x$ corrispondono due $y$).

### Notazione
- $f : X \to Y$: $X$ è il **domain** (dominio), $Y$ il **co-domain** (codominio).
- $[x_0 \mapsto y_0, x_1 \mapsto y_1, \dots, x_i \mapsto y_i] \approx \{(x_0, y_0), \dots, (x_i, y_i)\}$
- **Update** di una funzione:
$$f[x_n \mapsto y_n](x_j) = \begin{cases} y_n & \text{if } x_j = x_n \\ f(x_j) & \text{otherwise} \end{cases}$$
- $dom([x_0 \mapsto y_0, \dots, x_i \mapsto y_i]) = \{x_0, \dots, x_i\}$
- **Lambda notation**: $\lambda x .\ f(x) \equiv f$

Esempio, $f : \mathbb{Z} \to \mathbb{N}$:
- $f = [-1 \mapsto 1, 1 \mapsto 1] = \{(-1, 1), (1, 1)\}$
- $f' = f[2 \mapsto 2] = \{(-1, 1), (1, 1), (2, 2)\}$ (aggiunge un punto)
- $f'' = f'[1 \mapsto 2] = \{(-1, 1), (1, 2), (2, 2)\}$ (sovrascrive un punto)
- $dom(f) = \{-1, 1\}$, $dom(f') = dom(f'') = \{-1, 1, 2\}$
- $\lambda x .\ |x| = \{(i, |i|)\}$

## Monotone, embedding, isomorphism
Siano $\langle X, \sqsubseteq_X \rangle$ e $\langle Y, \sqsubseteq_Y \rangle$ due poset e $f : X \to Y$:
- $f$ è **monotone** (monotona) se: $x_1 \sqsubseteq_X x_2 \implies f(x_1) \sqsubseteq_Y f(x_2)$
- $f$ è un **order embedding** se: $x_1 \sqsubseteq_X x_2 \iff f(x_1) \sqsubseteq_Y f(x_2)$
- $f$ è un **isomorphism** (isomorfismo) se è:
  - un order embedding
  - **surjective** (suriettiva): $\forall y \in Y, \exists x \in X .\ f(x) = y$

Tre esempi disegnati verso la catena $a \sqsubseteq b \sqsubseteq c$:
1. Da un rombo ($0$ in basso, $1$ e $2$ incomparabili, $3$ in alto) con $0 \mapsto a$, $1 \mapsto b$, $2 \mapsto b$, $3 \mapsto c$: **monotona ma non embedding** ($f(1) \sqsubseteq f(2)$ ma $1 \not\sqsubseteq 2$).
2. Dalla catena $0 \sqsubseteq 1 \sqsubseteq 2$ con $0 \mapsto a$, $1 \mapsto c$, $2 \mapsto c$: **monotona ma non embedding** ($f(2) \sqsubseteq f(1)$ ma $2 \not\sqsubseteq 1$) e non suriettiva ($b$ non è raggiunto).
3. Dalla catena $0 \sqsubseteq 1 \sqsubseteq 2$ con $0 \mapsto a$, $1 \mapsto b$, $2 \mapsto c$: **isomorfismo**.

(Le slide non etichettano i tre disegni: la classificazione è mia, ricavata dalle definizioni.)

### Esempi
- $f : \langle \mathbb{Z}, \leq \rangle \to \langle \mathbb{Z}, \leq \rangle$, $f(x) = x + 1$: monotona, order embedding, suriettiva (quindi isomorfismo). Il disegno mostra le frecce $-1 \mapsto 0$, $0 \mapsto 1$, ecc.
- $f : \langle \wp(\mathbb{Z}), \subseteq \rangle \to \langle \mathbb{Z}, \leq \rangle$, $f(X) = max(X)$: monotona, ma **non** un embedding. Nel disegno $\{1\}, \{0,1\}, \{-1,1\}, \{-1,0,1\}$ vanno tutti in $1$: ad esempio $f(\{0,1\}) \leq f(\{-1,1\})$ vale senza che $\{0,1\} \subseteq \{-1,1\}$.
  (Correzione: così com'è, $max$ non è una funzione totale su $\wp(\mathbb{Z})$, perché $max(\varnothing)$ e $max$ di insiemi illimitati superiormente, come $\mathbb{Z}$, non sono definiti. L'esempio regge restringendosi ai sottoinsiemi finiti non vuoti, oppure usando come codominio $\mathbb{Z} \cup \{-\infty, +\infty\}$ con $max(\varnothing) = -\infty$ e $sup$ al posto di $max$.)

## Join/meet preserving functions
Siano $\langle X, \sqsubseteq_X, \sqcup_X, \sqcap_X \rangle$, $\langle Y, \sqsubseteq_Y, \sqcup_Y, \sqcap_Y \rangle$ e $f : X \to Y$:
- $f$ è **join preserving** se $f(x_1 \sqcup_X x_2) = f(x_1) \sqcup_Y f(x_2)$
- $f$ è **meet preserving** se $f(x_1 \sqcap_X x_2) = f(x_1) \sqcap_Y f(x_2)$
- Una funzione join o meet preserving è **monotona**, ma il viceversa non vale necessariamente.

(Aggiunta mia, il perché: se $x_1 \sqsubseteq x_2$ allora $x_1 \sqcup x_2 = x_2$, quindi $f(x_2) = f(x_1) \sqcup f(x_2)$, cioè $f(x_1) \sqsubseteq f(x_2)$.)

## Chains
Sia $\langle X, \sqsubseteq \rangle$ un poset:
- $S$ è una **chain** (catena) se e solo se $\forall x, y \in S .\ x \sqsubseteq y \lor y \sqsubseteq x$ (tutti gli elementi sono totalmente ordinati).
- **Ascending chain** (catena ascendente): successione $(l_n)_{n \in \mathbb{N}}$ tale che $i \leq j \implies l_i \sqsubseteq l_j$.
- Esempi di catene in $\langle \wp(\mathbb{Z}), \subseteq \rangle$ (slide): $\{\varnothing\}$, $\{\{\varnothing\}, \{0,1\}\}$, $\{\{0\}, \{-1,0,1\}\}$.
  (Correzione: il secondo esempio va letto $\{\varnothing, \{0,1\}\}$. Scritto come nella slide, $\{\varnothing\}$ è l'insieme che contiene l'insieme vuoto, non è un sottoinsieme di $\mathbb{Z}$, e non è contenuto in $\{0,1\}$, quindi non sarebbe una catena.)

## Ascending Chain Condition (ACC)
- Un poset soddisfa la **ACC** se ogni catena ascendente *infinita* non è strettamente crescente, cioè **si stabilizza** dopo un numero finito di passi:
$$\exists k \geq 0 .\ \forall j \geq k .\ l_k = l_j$$
- $\langle \wp(X), \subseteq \rangle$: se $X$ è finito soddisfa la ACC, altrimenti no.
- $\langle \mathbb{Z}, \leq \rangle$ non la soddisfa.
- $\langle \mathbb{N}, \leq \rangle$ non la soddisfa ($0 \leq 1 \leq 2 \leq \dots$).
- $\langle \mathbb{N}, \geq \rangle$ la soddisfa (salire in $\geq$ vuol dire scendere nei naturali, e prima o poi ci si ferma).
- Tutti i poset finiti soddisfano la ACC.
- Anche alcuni poset infiniti la soddisfano (es. $\langle \mathbb{N}, \geq \rangle$).

(La ACC è ciò che garantisce la terminazione delle iterazioni di punto fisso nelle analisi.)

## Continuous maps
Siano $\langle X, \sqsubseteq_X, \sqcup_X, \sqcap_X \rangle$, $\langle Y, \sqsubseteq_Y, \sqcup_Y, \sqcap_Y \rangle$ e $f : X \to Y$. $f$ è **continuous** (continua) se per ogni **chain** $C \subseteq X$ tale che $\sqcup_X C$ esiste:
- $\sqcup_Y f(C)$ esiste
- $\sqcup_Y f(C) = f(\sqcup_X C)$

Serve per dimostrare proprietà sull'esistenza dei punti fissi (vedi Kleene). Esempio nella slide: $f = 2 * x$ da $\langle \mathbb{Z}, \leq \rangle$ a $\langle \mathbb{Z}, \leq \rangle$.

## Fixpoints
- Sia $f : X \to X$: $x$ è un **fixpoint** (punto fisso) di $f$ se $f(x) = x$.
- $Fix(f) = \{x \mid f(x) = x\}$ è l'insieme di tutti i punti fissi di $f$.
- Dato $\langle X, \sqsubseteq \rangle$:
  - $x \in Fix(f)$ è il **least fixpoint** (**lfp**) se $\forall y \in Fix(f) .\ x \sqsubseteq y$
  - $x \in Fix(f)$ è il **greatest fixpoint** (**gfp**) se $\forall y \in Fix(f) .\ x \sqsupseteq y$

Esempio su $\langle \wp(\{-1, 0, 1\}), \subseteq \rangle$:
$$f(X) = \begin{cases} X \setminus \{1\} & \text{if } 1 \in X \\ X \cup \{-1\} & \text{otherwise} \end{cases}$$
- Se $1 \in X$, $f(X) \neq X$; altrimenti $f(X) = X$ solo se $-1 \in X$. Quindi $Fix(f) = \{\{-1\}, \{-1, 0\}\}$ (cerchiati in rosso nella slide).
- $lfp(f) = \{-1\}$, $gfp(f) = \{-1, 0\}$.

(Nota mia: questa $f$ non è monotona, es. $\{0\} \subseteq \{0,1\}$ ma $f(\{0\}) = \{-1, 0\} \not\subseteq \{0\} = f(\{0,1\})$; l'esempio serve solo a illustrare lfp e gfp.)

## Iterations
Sia $f : X \to X$. Gli **iterates** (iterate) di $f$ a partire da $x \in X$ sono:
- $f^0(x) = x$
- $f^{n+1}(x) = f(f^n(x))$

- Se $X$ è finito: $\forall k > |X| .\ \exists n \leq |X| .\ f^k(x) = f^n(x)$, cioè la sequenza prima o poi raggiunge un **fixpoint o un loop** (ciclo).
- Se $X$ è infinito, le iterazioni potrebbero essere infinite.

## Knaster-Tarski fixpoint theorem
Sia $\langle X, \sqsubseteq, \sqcup, \sqcap \rangle$ un lattice e $f : X \to X$ una funzione **monotona**. Allora:
- $\langle Fix(f), \sqsubseteq, \sqcup, \sqcap \rangle$ è un **complete lattice** (in particolare lfp e gfp esistono)
- $lfp(f) = \sqcap \{l \mid l \sqsupseteq f(l)\}$
- $gfp(f) = \sqcup \{l \mid l \sqsubseteq f(l)\}$

(Correzioni: 1) il teorema richiede che $X$ sia un **complete lattice**, non un lattice qualsiasi: su $\langle \mathbb{Z}, \leq \rangle$, che è un lattice, la funzione monotona $x \mapsto x + 1$ non ha punti fissi. 2) Una build della slide scrive $gfp(f) = \sqcup \{l \mid l \sqsupseteq f(l)\}$; la versione giusta, con $l \sqsubseteq f(l)$, compare nella slide successiva.)

Diagramma: il reticolo fra $\bot$ e $\top$, con due regioni ovali sovrapposte:
- in alto (blu) $\{l : f(l) \sqsubseteq l\}$, gli elementi che $f$ fa scendere (o lascia fermi);
- in basso (giallo) $\{l : f(l) \sqsupseteq l\}$, gli elementi che $f$ fa salire (o lascia fermi);
- l'intersezione (verde) è $Fix(f)$; il suo punto più basso è $lfp(f)$, il glb della regione blu, e il suo punto più alto è il gfp, il lub della regione gialla.

## Kleene fixpoint theorem
Sia $\langle X, \sqsubseteq, \bot, \top, \sqcup, \sqcap \rangle$ un complete lattice e $f : X \to X$ una funzione **continua**. Allora $f$ ha un punto fisso, calcolabile come:
$$\bigsqcup_{n \geq 0} f^n(\bot)$$

(Precisazione: quello ottenuto è il **least** fixpoint, $lfp(f) = \bigsqcup_{n \geq 0} f^n(\bot)$; la slide dice solo "a fixpoint". Aggiunta mia: la sequenza $\bot \sqsubseteq f(\bot) \sqsubseteq f^2(\bot) \sqsubseteq \dots$ è una catena ascendente; se il reticolo soddisfa la ACC si stabilizza in un numero finito di passi, ed è così che le analisi calcolano davvero il punto fisso.)

## Da ricordare
- **Partial order** = riflessivo + antisimmetrico + transitivo; un insieme con un ordine parziale è un **poset** $\langle X, \sqsubseteq \rangle$. Esempio canonico: $\langle \wp(X), \subseteq \rangle$.
- **Hasse diagram**: una linea fra $x$ e $y$ (più in alto) significa $x \sqsubset y$ senza elementi in mezzo; il poset inverso è il diagramma ruotato di 180°.
- **Upper/lower bound**, **lub** ($\sqcup$, join) e **glb** ($\sqcap$, meet): se esistono sono unici; $\sqcup X$ esiste se e solo se c'è un $\top$.
- **Lattice**: ogni coppia ha join e meet; $x \sqsubseteq y \iff x \sqcup y = y \iff x \sqcap y = x$. Un lattice può non avere $\top$ e $\bot$ ($\langle \mathbb{Z}, \leq, max, min \rangle$).
- **Complete lattice**: ogni sottoinsieme ha lub (e quindi glb); ha sempre $\bot$ e $\top$. $\langle \wp(X), \subseteq, \cup, \cap \rangle$ e $\mathbb{Z} \cup \{\pm\infty\}$ lo sono, $\mathbb{Z}$ no. I lattice finiti sono completi.
- **Funzioni**: relazioni con al più un output per input; notazione $[x \mapsto y]$, update $f[x \mapsto y]$, $dom$, $\lambda$.
- **Monotone** ($\Rightarrow$), **order embedding** ($\Leftrightarrow$), **isomorphism** (embedding + suriettiva). Join/meet preserving implica monotona, non il viceversa.
- **Chain** = sottoinsieme totalmente ordinato; **ACC** = ogni catena ascendente si stabilizza. Vale per poset finiti e per $\wp(X)$ con $X$ finito, non per $\langle \mathbb{N}, \leq \rangle$ e $\langle \mathbb{Z}, \leq \rangle$.
- **Continuous**: preserva i lub delle catene.
- **Fixpoint**: $f(x) = x$; lfp e gfp sono il minimo e il massimo di $Fix(f)$.
- **Knaster-Tarski**: $f$ monotona su complete lattice $\Rightarrow$ $Fix(f)$ è un complete lattice, $lfp(f) = \sqcap \{l \mid f(l) \sqsubseteq l\}$, $gfp(f) = \sqcup \{l \mid l \sqsubseteq f(l)\}$.
- **Kleene**: $f$ continua su complete lattice $\Rightarrow$ $lfp(f) = \bigsqcup_{n \geq 0} f^n(\bot)$, calcolabile per iterazione da $\bot$ (finita se vale la ACC).
