# 07 - Introduction to abstract interpretation (Abstract semantics)

Fonte: `07 - Introduction to abstract interpretation (Abstract semantics).pdf`

Nella slide di copertina la lezione è numerata "Lecture 8". Alcune slide (Kleene sul CFG, richiamo della collecting semantics, valori dell'analisi dei segni) sono state svolte alla lavagna e nel PDF sono vuote o contengono solo le equazioni. Le brevi integrazioni sono segnate come **[aggiunta]**.

## Concrete semantics
- La semantica **concreta** e la **collecting semantics** del linguaggio **IMP** sono già state introdotte (la slide rimanda a "lecture 2").
- Parlando di **abstract semantics** si vuole codificare la collecting semantics sui **CFG** (control flow graph), non sul codice sorgente.
- La semantica di `while` e `if` è codificata **direttamente nel CFG** (e nel calcolo di punto fisso sul CFG).

## Esempio guida
Programma:

```c
1 x = 0;
2 while (x < 100)
3   if (x < 50)
4     x = x + 2;
5   else
6     x = x + 10;
```

CFG con i punti di interesse $x_1, \dots, x_6$ (stato in **entrata** di ogni blocco):

```
         x1
   [ int x = 0 ]
         |
         x2                 x6
   [  x < 100  ] --false--> [ exit ]
     ^   | true      ^
     |   x3          |
     |  [ x < 50 ]   |
     |  true/  \false|
     | x4        x5  |
  [x = x + 2]  [x = x + 10]
     |______|    |___|
   (entrambi tornano a x < 100)
```

- Archi `true` in verde, `false` in rosso. Da `x = x + 2` e `x = x + 10` partono i due archi all'indietro verso la guardia `x < 100`.
- **Obiettivo**: inferire lo stato di entrata/uscita per ogni punto di programma $x_i$ (punto di interesse dell'analisi).

## Come si costruiscono le equazioni
- **Entry state** di un blocco: **upper bound** (lub) degli stati di uscita dei blocchi che puntano a esso.
- **Primo blocco**: lo stato (o gli stati) di entrata dati.
- **Exit state**: l'applicazione della semantica (collecting) dello statement contenuto nel blocco allo stato di entrata.
- `while`, `if` e la **concatenazione** di statement sono codificati nella struttura del CFG.
- Quindi basta esprimere la semantica **solo per assegnamenti ed espressioni booleane**.

### Sistema di equazioni concreto
Costruito passo per passo nelle slide:

$$\begin{aligned}
x_1 &= I \\
x_2 &= [\![ \texttt{x = 0} ]\!] x_1 \cup [\![ \texttt{x = x + 2} ]\!] x_4 \cup [\![ \texttt{x = x + 10} ]\!] x_5 \\
x_3 &= [\![ \texttt{x < 100} ]\!] x_2 \\
x_4 &= [\![ \texttt{x < 50} ]\!] x_3 \\
x_5 &= [\![ \texttt{x >= 50} ]\!] x_3 \\
x_6 &= [\![ \texttt{x >= 100} ]\!] x_2
\end{aligned}$$

- $I$ è l'insieme degli stati iniziali. Le guardie booleane agiscono da **filtri**: $[\![ b ]\!] X$ tiene solo gli stati di $X$ che rendono vera $b$. Il ramo `false` di una guardia usa la negazione ($\texttt{x >= 50}$ per $\neg(\texttt{x < 50})$).
- (Errore nella slide: da pagina 14 a 18 la sesta equazione diventa $x_6 = [\![ \texttt{x > 100} ]\!] x_2$; quella giusta è $[\![ \texttt{x >= 100} ]\!] x_2$, negazione di $\texttt{x < 100}$, come nella slide 13 e nella versione astratta più avanti. Con $>$ lo stato $x = 100$ sparirebbe, ed è proprio quello con cui si esce dal ciclo.)

### Least solution e indecidibilità
- Dati gli $m$ nodi di un CFG, si vuole risolvere il sistema

$$F = \{ x_i = f_i(x_1, \dots, x_m) \mid i = 1, 2, \dots, m \}$$

- calcolando la **least solution** di $F$ come **limite di una Kleene iteration** su $\langle \wp(\mathbb{Z}), \subseteq, \cap, \cup, \mathbb{Z}, \emptyset \rangle$ (precisamente sul prodotto di $m$ copie, una per punto di programma):

$$x^{\mathsf{lfp}(F)} = \left(x_1^{\mathsf{lfp}(F)}, \dots, x_m^{\mathsf{lfp}(F)}\right)$$

- **Undecidable!**: in generale questo punto fisso non è calcolabile (la Kleene iteration su $\wp(\mathbb{Z})$ può non terminare).

## Kleene iterations on CFG (esempio)
- Slide svolta alla lavagna.
- **[aggiunta]** Partendo da tutti i $x_i = \emptyset$ e $x_1 = I$, a ogni iterazione si ricalcola ogni equazione: $x_2$ cresce come $\{0\}, \{0, 2\}, \{0, 2, 4\}, \dots$ fino a $\{0, 2, \dots, 48, 50, 60, 70, 80, 90, 100\}$, e il punto fisso dà $x_6 = \{100\}$. Qui le iterazioni sono finite perché il programma ha un solo input, ma in generale (input ignoti, cicli illimitati) la catena può non stabilizzarsi.

## Fixpoint computation
- In generale la least fixpoint solution sul dominio concreto $C$ **non è calcolabile in modo finito**. L'idea è calcolare un **abstract fixpoint** su un dominio astratto $A$ che **approssima correttamente** quello concreto.
- Si vorrebbe:
  - calcolare $\alpha(\mathsf{lfp}(F))$
  - **senza** calcolare $\mathsf{lfp}(F)$.
- Più avanti si introducono **due teoremi** che permettono di farlo (Kleenian e Tarskian fixpoint approximation, sotto).
- Il primo passo è **spostare il calcolo da $C$ ad $A$**.

## Abstract semantics
- Poiché l'analisi statica si fa sui CFG, basta ragionare su **assegnamenti** ed **espressioni booleane**, che sono le sole espressioni/statement che compaiono nel CFG.
- Sintassi di IMP:

$$\begin{aligned}
e &::= x \mid n \mid e_1 \ \mathrm{op}_a \ e_2 \\
b &::= \mathbf{true} \mid \mathbf{false} \mid \neg b_1 \mid b_1 \ \mathrm{op}_b \ b_2 \mid e_1 \ \mathrm{op}_c \ e_2 \\
s &::= x := e; \mid \mathbf{skip} \mid s_1\ s_2 \mid \mathbf{if}\ b\ \mathbf{then}\ s_1\ \mathbf{else}\ s_2 \mid \mathbf{while}\ b\ \mathbf{do}\ s_1
\end{aligned}$$

  dove $n \in \mathbb{Z}$, $\mathrm{op}_a \in \{+, -, *, \div\}$, $\mathrm{op}_b \in \{\&\&, \|\}$, $\mathrm{op}_c \in \{==, >, <, \ge, \le\}$.

### Con il sign abstract domain
- "Quick recall" della collecting semantics di IMP, poi la sua versione sui segni (svolta alla lavagna).
- **[aggiunta]** L'idea: ogni operazione concreta su insiemi di valori viene sostituita da una sui segni, es. $+ \mathbin{+^\sharp} + = +$, $+ \mathbin{+^\sharp} - = \top$, $- \mathbin{*^\sharp} - = +$, $0 \mathbin{*^\sharp} s = 0$ (per $s \neq \bot$); le guardie filtrano lo stato astratto (es. $[\![ \texttt{x < 0} ]\!]^\sharp$ su $x \mapsto +$ dà $\bot$).
- Si sono **astratti i calcoli**, passando da un dominio concreto a uno astratto, **ma bisogna garantire la soundness** della semantica astratta.

## Soundness delle operazioni astratte
**Definizione.** Siano $C$ e $A$ in GC via $\alpha$ e $\gamma$, $f : C \to C$ un'operazione concreta e $f^\sharp : A \to A$ una sua astrazione. $f^\sharp$ è **sound** se

$$\forall c \in C .\ \alpha(f(c)) \sqsubseteq_A f^\sharp(\alpha(c))$$

o equivalentemente

$$\forall a \in A .\ f(\gamma(a)) \sqsubseteq_C \gamma(f^\sharp(a))$$

- (Errore nella slide: la prima formula è scritta $\forall c \in C .\ \alpha(f(x)) \sqsubseteq_A f^\sharp(\alpha(x))$, quantificando su $c$ ma usando $x$; va letta con la stessa variabile.)
- **[aggiunta]** L'equivalenza vale grazie alla GC (e alla monotonia di $f$ e $f^\sharp$).

### Diagramma
Due coppie di reticoli (forma a clessidra, $\top$ in alto e $\bot$ in basso):
- **(a) BACKWARD**: a sinistra il concreto, $x \xrightarrow{f} f(x)$; entrambi astratti con $\alpha$. A destra $\alpha(x) \xrightarrow{f^\sharp} f^\sharp(\alpha(x))$, e $\alpha(f(x))$ sta **sotto** $f^\sharp(\alpha(x))$ (segmento rosso). Formula: $\alpha(f(x)) \sqsubseteq_A f^\sharp(\alpha(x))$.
- **(b) FORWARD**: a destra l'astratto, $x \xrightarrow{f^\sharp} f^\sharp(x)$; entrambi concretizzati con $\gamma$. A sinistra $\gamma(x) \xrightarrow{f} f(\gamma(x))$, e $f(\gamma(x))$ sta **sotto** $\gamma(f^\sharp(x))$. Formula: $f(\gamma(a)) \sqsubseteq_C \gamma(f^\sharp(a))$.
- **[aggiunta]** I nomi backward/forward riprendono quelli usati per la completeness ($\alpha \circ f = f^\sharp \circ \alpha$ è la backward completeness, $f \circ \gamma = \gamma \circ f^\sharp$ la forward): la soundness è la versione con $\sqsubseteq$ al posto di $=$.

## Best correct approximation
- Fra tutte le astrazioni $f^\sharp$ sound di $f$, **qual è la migliore?**

**Definizione.** Siano $C$ e $A$ in GC via $\alpha$ e $\gamma$ e $f : C \to C$ un'operazione concreta. La **best correct approximation** $f^{\mathsf{bca}} : A \to A$ è

$$f^{\mathsf{bca}} = \alpha \circ f \circ \gamma$$

- **Purtroppo può non essere calcolabile.** Perché? (domanda lasciata aperta nella slide)
- **[aggiunta]** Perché richiede di applicare $f$ a $\gamma(a)$, che in generale è un insieme **infinito** (es. $\gamma(+) = \{1, 2, 3, \dots\}$), e poi di astrarre il risultato: si passa di nuovo dal concreto, che è proprio ciò che si vuole evitare. In pratica si scrivono a mano operatori astratti sound, possibilmente uguali alla bca.

## Sign analysis
Sullo stesso CFG, le equazioni astratte si ottengono sostituendo ogni semantica concreta con quella astratta, l'unione con il **join** $\sqcup$ e lo stato iniziale con la sua astrazione:

$$\begin{aligned}
x_1 &= \alpha(I) \\
x_2 &= [\![ \texttt{x = 0} ]\!]^\sharp x_1 \sqcup [\![ \texttt{x = x + 2} ]\!]^\sharp x_4 \sqcup [\![ \texttt{x = x + 10} ]\!]^\sharp x_5 \\
x_3 &= [\![ \texttt{x < 100} ]\!]^\sharp x_2 \\
x_4 &= [\![ \texttt{x < 50} ]\!]^\sharp x_3 \\
x_5 &= [\![ \texttt{x >= 50} ]\!]^\sharp x_3 \\
x_6 &= [\![ \texttt{x >= 100} ]\!]^\sharp x_2
\end{aligned}$$

- Dati gli $m$ nodi del CFG si risolve il sistema

$$F^\sharp = \{ x_i = x_i \sqcup f_i^\sharp(x_1, \dots, x_m) \mid i = 1, 2, \dots, m \}$$

  calcolando la least solution di $F^\sharp$ come limite di una Kleene iteration **su un dominio astratto $A$**:

$$x^{\sharp\,\mathsf{lfp}(F^\sharp)} = \left(x_1^{\sharp\,\mathsf{lfp}(F^\sharp)}, \dots, x_m^{\sharp\,\mathsf{lfp}(F^\sharp)}\right)$$

- (Errore nella slide: l'apice è scritto $\mathsf{lfp}(F)$; trattandosi della soluzione del sistema astratto è $\mathsf{lfp}(F^\sharp)$.)
- Il termine $x_i \sqcup \dots$ rende le iterate crescenti per costruzione (ogni nuovo valore contiene il precedente).
- **[aggiunta]** Esito atteso con i segni: $x = 0$ dà $0$, poi $0 \mathbin{+^\sharp} + = +$ e il join $0 \sqcup +$; con il reticolo base $\{-, 0, +\}$ questo è $\top$, con una variante che ha $\ge 0$ si ottiene $x \ge 0$ in tutti i punti dopo l'assegnamento. Le guardie con costanti positive non riescono a escludere nulla con i soli segni.

## Fixpoint transfer
- **Chi garantisce** che $\mathsf{lfp}(F^\sharp)$ sia un'approssimazione sound di $\mathsf{lfp}(F)$?
  - caso **esatto**: $\alpha(\mathsf{lfp}(F)) = \mathsf{lfp}(F^\sharp)$;
  - caso **approssimato**: $\alpha(\mathsf{lfp}(F)) \sqsubseteq \mathsf{lfp}(F^\sharp)$.

## Kleenian fixpoint approximation
**Teorema.** Se $f : C \to C$ è **continua** sul complete lattice $\langle C, \sqsubseteq_C, \sqcup_C, \sqcap_C, \bot_C, \top_C \rangle$, $f^\sharp : A \to A$ è un'astrazione **sound** di $f$ nel dominio astratto $\langle A, \sqsubseteq_A, \sqcup_A, \sqcap_A, \bot_A, \top_A \rangle$, e la successione $\{ (f^\sharp)^i(\bot_A) \mid i \in \mathbb{N} \}$ ha un **limite** $x \in A$, allora $x$ è un'approssimazione sound di $\mathsf{lfp}(f)$:

$$\mathsf{lfp}(f) \sqsubseteq_C \gamma(x)$$

- In particolare, a **ogni passo** $i$, $(f^\sharp)^i(\bot_A)$ è un'approssimazione sound di $f^i(\bot_C)$.
- Il teorema garantisce la **soundness, non l'optimality** (il limite può essere più grande di $\alpha(\mathsf{lfp}(f))$).
- (Errore di notazione nella slide: le iterate sono scritte $f_i^\sharp(\bot_A)$, $f_i^\sharp(\bot_a)$ e $f_i(\bot_C)$; si intende l'$i$-esima iterata $(f^\sharp)^i$ e $f^i$, non le funzioni $f_i$ delle singole equazioni, e $\bot_a$ sta per $\bot_A$.)

## Tarskian fixpoint approximation
**Teorema.** Dati un complete lattice $\langle C, \sqsubseteq_C, \sqcup_C, \sqcap_C, \bot_C, \top_C \rangle$, una funzione **monotona** $f : C \to C$ e un'astrazione sound $f^\sharp : A \to A$ di $f$ nel dominio astratto $\langle A, \sqsubseteq_A, \sqcup_A, \sqcap_A, \bot_A, \top_A \rangle$, allora **qualsiasi post-fixpoint** $a$ di $f^\sharp$, cioè tale che $f^\sharp(a) \sqsubseteq_A a$, è un'astrazione sound di $\mathsf{lfp}(f)$:

$$\mathsf{lfp}(f) \sqsubseteq_C \gamma(a)$$

- Il teorema sfrutta due fatti:
  - la **caratterizzazione di Tarski**: $\mathsf{lfp}(f)$ è il **più piccolo post-fixpoint** di $f$;
  - ogni post-fixpoint astratto di un'astrazione sound rappresenta, via $\gamma$, un **post-fixpoint concreto**, quindi una sovra-approssimazione di $\mathsf{lfp}(f)$.
- **[aggiunta]** Il passaggio: $f(\gamma(a)) \sqsubseteq_C \gamma(f^\sharp(a)) \sqsubseteq_C \gamma(a)$ (soundness, poi monotonia di $\gamma$), quindi $\gamma(a)$ è un post-fixpoint di $f$ e contiene $\mathsf{lfp}(f)$. Qui "post-fixpoint" ha il significato di Cousot ($f(x) \sqsubseteq x$); altri testi lo chiamano pre-fixpoint.
- A differenza del teorema kleeniano non serve la continuità né arrivare al limite: basta trovare un qualsiasi $a$ con $f^\sharp(a) \sqsubseteq_A a$.

## Da ricordare
- La collecting semantics si codifica sul CFG: entry state = lub delle uscite dei predecessori, exit state = semantica dello statement del blocco; `while`, `if` e sequenza sono nella struttura del grafo, quindi la semantica serve solo per assegnamenti e guardie.
- Il sistema $F = \{x_i = f_i(x_1, \dots, x_m)\}$ ha come soluzione $\mathsf{lfp}(F)$ via Kleene su $\wp(\mathbb{Z})$: in generale **indecidibile**.
- Obiettivo: calcolare (un'approssimazione di) $\alpha(\mathsf{lfp}(F))$ senza calcolare $\mathsf{lfp}(F)$, spostando il calcolo da $C$ ad $A$.
- $f^\sharp$ è sound se $\alpha \circ f \sqsubseteq f^\sharp \circ \alpha$, equivalentemente $f \circ \gamma \sqsubseteq \gamma \circ f^\sharp$.
- **Best correct approximation**: $f^{\mathsf{bca}} = \alpha \circ f \circ \gamma$, la migliore fra le sound, ma spesso non calcolabile ($\gamma(a)$ infinito).
- Sistema astratto: $F^\sharp = \{x_i = x_i \sqcup f_i^\sharp(x_1, \dots, x_m)\}$ con $\cup \to \sqcup$, $I \to \alpha(I)$, $[\![\cdot]\!] \to [\![\cdot]\!]^\sharp$.
- Fixpoint transfer esatto $\alpha(\mathsf{lfp}(F)) = \mathsf{lfp}(F^\sharp)$, approssimato $\alpha(\mathsf{lfp}(F)) \sqsubseteq \mathsf{lfp}(F^\sharp)$.
- **Kleene**: $f$ continua, $f^\sharp$ sound, limite $x$ delle iterate da $\bot_A$ ⇒ $\mathsf{lfp}(f) \sqsubseteq_C \gamma(x)$; soundness, non optimality.
- **Tarski**: $f$ monotona, $f^\sharp$ sound, $f^\sharp(a) \sqsubseteq_A a$ ⇒ $\mathsf{lfp}(f) \sqsubseteq_C \gamma(a)$.
