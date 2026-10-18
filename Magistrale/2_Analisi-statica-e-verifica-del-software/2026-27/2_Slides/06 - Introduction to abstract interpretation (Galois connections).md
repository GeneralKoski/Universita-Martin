# 06 - Introduction to abstract interpretation (Galois connections)

Fonte: `06 - Introduction to abstract interpretation (Galois connections).pdf`

Nella slide di copertina la lezione è numerata "Lecture 7" (la numerazione delle lezioni non coincide con quella dei file).

Diverse slide di esempio (dominio dei segni, prove su constant propagation, automi, esercizio finale) sono vuote nel PDF: sono state svolte alla lavagna. Dove serve per capire il discorso ho aggiunto un breve richiamo, segnato come **[aggiunta]**.

## Concrete domain
- Il **concrete domain** per i valori interi è l'insieme delle parti degli interi:

$$\langle \wp(\mathbb{Z}), \subseteq, \cap, \cup, \mathbb{Z}, \emptyset \rangle$$

  che forma un **complete lattice** (reticolo completo), con ordine $\subseteq$, meet $\cap$, join $\cup$, top $\mathbb{Z}$, bottom $\emptyset$. Un insieme $S$ rappresenta i valori che una variabile $x$ può assumere in un punto di programma.
- Lettura dell'ordine e delle operazioni:
  - $S_1 \subset S_2$: $S_1$ è "**more precise**" (più preciso) di $S_2$.
  - $S_1 \not\subseteq S_2 \wedge S_2 \not\subseteq S_1$: i due insiemi **non sono confrontabili**.
  - $S_1 \cup S_2$: $x$ deve stare in $S_1$ **oppure** in $S_2$.
  - $S_1 \cap S_2$: $x$ deve stare in $S_1$ **e** in $S_2$.
  - $\mathbb{Z}$ (**top element**): $x$ può essere qualsiasi valore ("I don't know").
  - $\emptyset$ (**bottom element**): nessun valore possibile.
- Diagramma di Hasse (parziale) di $\langle \wp(\mathbb{Z}), \subseteq \rangle$ ristretto a $\{-1, 0, 1\}$, con $\mathbb{Z}$ in cima collegato da linee tratteggiate (infiniti altri insiemi):

```
                 Z
           (... tratteggiato ...)
             {-1,0,1}
        {-1,0}  {0,1}  {-1,1}
         {-1}    {0}    {1}
                 Ø
```

- Corrispondenza con l'analisi:
  - **join point** (punto di confluenza del flusso, es. dopo un `if`) → **unione**;
  - condizione $b_1 \wedge b_2$ → **intersezione**;
  - **input dell'utente** → **top** (può essere qualunque valore);
  - **unreachable point** (punto irraggiungibile) → **bottom**.

## Abstract domain
- Esistono molti **abstract domain** (domini astratti), ognuno traccia un tipo diverso di informazione: il segno, l'intervallo, le disuguaglianze lineari, ecc.
- Esiste una **gerarchia** fra domini (il **lattice of abstractions**, ripreso più avanti nel corso).
- I domini si possono **combinare**: **cartesian product** e **reduced product**.
- Fra il dominio concreto $C$ e un dominio astratto $A$ c'è una **relazione formale**, data da due funzioni:
  - **abstraction function** $\alpha : C \to A$
  - **concretization function** $\gamma : A \to C$

## Constant propagation (dalle lezioni precedenti)
- Definizione richiamata: *"For each program point, whether or not a variable has a constant value whenever an execution reaches that point"*, cioè per ogni punto di programma si stabilisce se una variabile ha un valore costante ogni volta che un'esecuzione raggiunge quel punto.
- **[aggiunta]** Il dominio $CP$ è il reticolo piatto $\bot \sqsubseteq n \sqsubseteq \top$ per ogni $n \in \mathbb{Z}$ (le costanti fra loro non confrontabili). Le funzioni standard sono:

$$\alpha(S) = \begin{cases} \bot & S = \emptyset \\ n & S = \{n\} \\ \top & \text{altrimenti} \end{cases} \qquad \gamma(a) = \begin{cases} \emptyset & a = \bot \\ \{n\} & a = n \\ \mathbb{Z} & a = \top \end{cases}$$

## Soundness (da concreto ad astratto e ritorno)
- Un dominio astratto è **sound** tramite astrazione e concretizzazione. Intuizione:
  1. si parte da un valore **concreto** $c$;
  2. lo si astrae con $\alpha$;
  3. si torna al concreto con $\gamma$;
  4. è sound **se e solo se** il risultato **contiene** quello di partenza: $\gamma(\alpha(c)) \supseteq c$.
- In altre parole l'astrazione può aggiungere valori (perdere precisione) ma non perderne.

### Esempio: sign abstract domain
- Slide di esempio vuota (svolta alla lavagna).
- **[aggiunta]** Dominio dei segni nella versione base: $\bot \sqsubseteq \{-, 0, +\} \sqsubseteq \top$, con $\gamma(-) = \{n < 0\}$, $\gamma(0) = \{0\}$, $\gamma(+) = \{n > 0\}$, $\gamma(\top) = \mathbb{Z}$, $\gamma(\bot) = \emptyset$. Esempio: $\alpha(\{1, 5\}) = +$ e $\gamma(+) = \{1, 2, 3, \dots\} \supseteq \{1, 5\}$; $\alpha(\{-1, 3\}) = \top$ e $\gamma(\top) = \mathbb{Z} \supseteq \{-1, 3\}$. Il corso può usare una variante con più elementi (es. $\le 0$, $\ge 0$, $\neq 0$).

## Soundness: l'altra direzione
- Intuizione:
  1. si parte da un valore **astratto** $a$;
  2. lo si concretizza con $\gamma$;
  3. si torna all'astratto con $\alpha$;
  4. la slide dice "sound iff the result is $\sqsupseteq_A$ (in general, $=$)".
- (Errore nella slide: la direzione corretta è $\alpha(\gamma(a)) \sqsubseteq_A a$, ed è infatti la proprietà "$\alpha \circ \gamma$ reductive" data poco dopo nelle slide stesse; con una Galois insertion vale l'uguaglianza $\alpha(\gamma(a)) = a$, che è il caso "in general, $=$".)

### Esempio: sign abstract domain
- Slide vuota (lavagna). **[aggiunta]** $\gamma(+) = \{1, 2, 3, \dots\}$ e $\alpha(\{1, 2, 3, \dots\}) = +$: si torna esattamente al punto di partenza.

## Monotonicity
- **$\alpha$ è monotona**: $I_1 \subseteq I_2 \implies \alpha(I_1) \sqsubseteq_A \alpha(I_2)$. Se si astrae qualcosa che rappresenta meno informazione di qualcos'altro, si ottiene qualcosa con meno o la stessa informazione.
- **$\gamma$ è monotona**: $a_1 \sqsubseteq_A a_2 \implies \gamma(a_1) \subseteq \gamma(a_2)$. Se si concretizza qualcosa che rappresenta meno informazione di qualcos'altro, si ottiene qualcosa con meno o la stessa informazione.

### Esempio: sign abstract domain
- Slide vuota (lavagna). **[aggiunta]** $\{1\} \subseteq \{1, 2\}$ e $\alpha(\{1\}) = + \sqsubseteq + = \alpha(\{1, 2\})$; $\{1\} \subseteq \{-1, 1\}$ e $+ \sqsubseteq \top$. Per $\gamma$: $+ \sqsubseteq \top$ e $\gamma(+) \subseteq \mathbb{Z}$.

## Galois Connection (GC)
**Definizione.** Siano $\langle C, \sqsubseteq_C \rangle$ e $\langle A, \sqsubseteq_A \rangle$ due **poset** e $\alpha : C \to A$, $\gamma : A \to C$ due funzioni monotone. Formano una **Galois Connection** se

$$\forall c \in C,\ \forall a \in A .\quad \alpha(c) \sqsubseteq_A a \iff c \sqsubseteq_C \gamma(a)$$

- Si scrive anche $\langle C, \sqsubseteq_C \rangle \overset{\gamma}{\underset{\alpha}{\leftrightarrows}} \langle A, \sqsubseteq_A \rangle$ **[aggiunta, notazione usuale]**.
- Le due direzioni dell'equivalenza:
  - $\alpha(c) \sqsubseteq_A a \implies c \sqsubseteq_C \gamma(a)$: garantisce la **soundness** (ogni astrazione che sta sopra $\alpha(c)$ rappresenta correttamente $c$);
  - $c \sqsubseteq_C \gamma(a) \implies \alpha(c) \sqsubseteq_A a$: garantisce la **best abstraction** ($\alpha(c)$ è la più precisa fra le astrazioni corrette di $c$).
- **[aggiunta]** Con l'equivalenza la monotonia di $\alpha$ e $\gamma$ è in realtà una conseguenza, non un'ipotesi in più.

### Caratterizzazione alternativa
Siano $\langle C, \sqsubseteq_C \rangle$, $\langle A, \sqsubseteq_A \rangle$ poset, $\alpha : C \to A$, $\gamma : A \to C$. Si ha una GC se e solo se valgono **tutte** le proprietà:
1. $\alpha$ e $\gamma$ sono **monotone**;
2. $\gamma \circ \alpha$ è **extensive**: $\forall c \in C .\ c \sqsubseteq_C \gamma(\alpha(c))$ (quando si astrae si perde informazione);
3. $\alpha \circ \gamma$ è **reductive**: $\forall a \in A .\ \alpha(\gamma(a)) \sqsubseteq_A a$ (quando si concretizza non si perde informazione).
- Spesso nel punto 3 vale $=$ (caso della Galois insertion, sotto).

## Constant propagation: prove
- Si dimostra che $\langle \wp(\mathbb{Z}), \subseteq \rangle$ e $CP$ formano una GC verificando i tre punti della caratterizzazione alternativa (monotonia, $\gamma \circ \alpha$ estensiva, $\alpha \circ \gamma$ riduttiva). La prova è svolta alla lavagna.
- **[aggiunta]** Schema con le funzioni date sopra:
  - monotonia: se $S_1 \subseteq S_2$, i casi possibili sono $\emptyset \subseteq$ qualsiasi ($\bot \sqsubseteq$ tutto), $\{n\} \subseteq \{n\}$ ($n \sqsubseteq n$), $\{n\} \subseteq S_2$ con $|S_2| \ge 2$ ($n \sqsubseteq \top$), insiemi con almeno due elementi ($\top \sqsubseteq \top$); per $\gamma$ basta vedere $\emptyset \subseteq \{n\} \subseteq \mathbb{Z}$;
  - estensività: $\gamma(\alpha(\emptyset)) = \emptyset$, $\gamma(\alpha(\{n\})) = \{n\}$, altrimenti $\gamma(\top) = \mathbb{Z} \supseteq S$;
  - riduttività: $\alpha(\gamma(\bot)) = \bot$, $\alpha(\gamma(n)) = n$, $\alpha(\gamma(\top)) = \alpha(\mathbb{Z}) = \top$, quindi vale anzi $\alpha \circ \gamma = id$.

## Galois Insertion (GI)
**Definizione.** Siano $\langle C, \sqsubseteq_C \rangle$, $\langle A, \sqsubseteq_A \rangle$ poset con una GC via $\alpha$ e $\gamma$. Se $\alpha \circ \gamma$ è l'**identità** la GC si chiama **Galois Insertion**.
- In questo caso l'astrazione $\alpha$ è **suriettiva** e la concretizzazione $\gamma$ è **iniettiva**.
- **Ogni GC può essere ridotta a una GI.**
- Quando non si ha una GI, esistono almeno due elementi astratti che rappresentano la **stessa informazione** (stessa concretizzazione); gli elementi ridondanti si possono eliminare con la **domain reduction**.

## Constant propagation: formalizzazione
- La slide ripropone i tre punti (monotonia, $\gamma \circ \alpha$ estensiva, $\alpha \circ \gamma$ riduttiva) da verificare sulla formalizzazione di $CP$, svolta alla lavagna. **[aggiunta]** Dalla prova sopra $\alpha \circ \gamma = id$, quindi $CP$ è una Galois insertion.

## $\gamma \circ \alpha = id$?
- Cioè $\forall v \in C .\ \gamma(\alpha(v)) = v$.
- **(Quasi) mai vero**.
- Vorrebbe dire che **non c'è astrazione**: il dominio astratto è un **isomorfismo** del concreto (diagramma: due reticoli identici, "Concrete" con nodi $o, s, r, t, v, u, z, x, y, w, n$ e "Abstract" con $m, h, i, e, f, g, a, b, c, d, l$, con frecce che collegano ogni nodo al suo corrispondente).
- E il calcolo sul concreto e sull'astratto sarebbe (presumibilmente) lo stesso: quindi **NON è ciò che vogliamo**, perché l'astrazione serve proprio a rendere il calcolo trattabile.

## On the best abstraction
- Ripresa della definizione di GC: la direzione $c \sqsubseteq_C \gamma(a) \implies \alpha(c) \sqsubseteq_A a$ è quella che garantisce la **best abstraction**.
- Può succedere che la GC fra $C$ e $A$ **non esista**, perché **non esiste la best abstraction** di alcuni elementi concreti. Esempio tipico: i **convex polyhedra** (poliedri convessi).

### Esempio: il cerchio con i poliedri
- $P = \{(x, y) \mid x^2 + y^2 \le 1\}$ (il disco unitario).
- Con un poliedro convesso, cioè una congiunzione finita di vincoli $a \cdot x + b \cdot y \le c$, lo si può sovra-approssimare (figura: disco giallo circondato da un quadrato e da varie rette tangenti).
- **Ma si può sempre trovare un'approssimazione migliore**: aggiungendo un'altra retta tangente si ottiene un poligono più stretto. Non esiste quindi un poliedro **minimo** che contenga il disco, cioè non esiste $\alpha(P)$, e non c'è una GC (si lavora solo con $\gamma$).

## On the minimal abstraction: esempio con automi a stati finiti
- Slide vuota (lavagna).
- **[aggiunta]** Il contesto è quello dei **finite state automata** come dominio per insiemi di stringhe: automi diversi riconoscono lo stesso linguaggio, quindi più elementi astratti hanno la stessa concretizzazione (niente GI); scegliendo come rappresentante canonico l'**automa minimo** (deterministico) si eliminano le ridondanze, come nella domain reduction.

## State of constant propagation
- Finora si è parlato di astrazione dei **valori**.
- Ma lo stato dell'analisi è una funzione $\mathbb{V} \mapsto CP$ (da variabili a valori di $CP$): **applicazione pointwise** di $CP$.
- Si è dimostrato che $CP$ forma una GC con $\wp(\mathbb{Z})$; e per gli stati?
- Si può dimostrare che, data un'astrazione dei valori che forma una GC, la sua **applicazione pointwise** (variabile per variabile) è anch'essa una GC.
- **[aggiunta]** Concretamente: $\alpha(\Sigma) = \lambda x .\ \alpha(\{\sigma(x) \mid \sigma \in \Sigma\})$ e $\gamma(\hat\sigma) = \{\sigma \mid \forall x .\ \sigma(x) \in \gamma(\hat\sigma(x))\}$, con l'ordine pointwise sugli stati astratti.

## Esercizio: the sign abstract domain
- Slide finale "Exercise" senza testo: si tratta di definire il dominio dei segni (reticolo, $\alpha$, $\gamma$) e dimostrare che forma una GC (e se è una GI) con $\wp(\mathbb{Z})$, come fatto per constant propagation.

## Da ricordare
- Concreto: $\langle \wp(\mathbb{Z}), \subseteq, \cap, \cup, \mathbb{Z}, \emptyset \rangle$ complete lattice; join point = $\cup$, $b_1 \wedge b_2$ = $\cap$, input utente = top, punto irraggiungibile = bottom.
- Concreto e astratto sono legati da $\alpha : C \to A$ e $\gamma : A \to C$.
- Soundness: $c \subseteq \gamma(\alpha(c))$; nell'altra direzione $\alpha(\gamma(a)) \sqsubseteq_A a$ (con $=$ nelle GI).
- **GC**: $\alpha(c) \sqsubseteq_A a \iff c \sqsubseteq_C \gamma(a)$; "$\Rightarrow$" dà la soundness, "$\Leftarrow$" la best abstraction.
- Caratterizzazione alternativa: $\alpha$, $\gamma$ monotone, $\gamma \circ \alpha$ estensiva, $\alpha \circ \gamma$ riduttiva.
- **GI**: $\alpha \circ \gamma = id$, $\alpha$ suriettiva, $\gamma$ iniettiva; ogni GC si riduce a una GI eliminando gli elementi astratti ridondanti (domain reduction).
- $\gamma \circ \alpha = id$ significa nessuna astrazione (isomorfismo): non è ciò che si vuole.
- La GC può non esistere se manca la best abstraction: poliedri convessi e disco $x^2 + y^2 \le 1$.
- Una GC sui valori, applicata pointwise, dà una GC sugli stati $\mathbb{V} \mapsto CP$.
