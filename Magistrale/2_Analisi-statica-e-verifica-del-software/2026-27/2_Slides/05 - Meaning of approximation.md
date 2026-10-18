# 05 - Meaning of approximation

Fonte: `05 - Meaning of approximation.pdf`

(Il frontespizio dice "Lecture 6 - Meaning of approximation", mentre il file è il numero 05: è solo una numerazione diversa fra lezioni e file.)

## Approssimazione: l'intuizione
- Sia $Q$ una proprietà e ci chiediamo se $[[P]] \subseteq Q$, cioè se la semantica del programma $P$ (l'insieme dei suoi comportamenti) soddisfa $Q$.
- In generale questa domanda è **undecidable** (indecidibile, per il **Rice's theorem** visto nella lezione 01).
- Si calcola allora un'**approximation** (approssimazione) $[[P]]^\sharp$ di $[[P]]$ tale che:
  - **Soundness**: $[[P]] \subseteq [[P]]^\sharp$ (l'approssimazione contiene tutti i comportamenti reali);
  - **Decidability**: la verifica $[[P]]^\sharp \subseteq Q$ è decidibile.
- La soundness è cruciale perché permette di sfruttare la decidibilità dell'approssimazione:

$$[[P]]^\sharp \subseteq Q \implies [[P]] \subseteq Q$$

- Se invece $[[P]]^\sharp \not\subseteq Q$, **non sappiamo** nulla: il comportamento che viola $Q$ può essere reale oppure introdotto dall'approssimazione (un **false alarm** / **false positive**). Qui si vede la perdita di **completeness**.

## Abstraction
- L'**abstraction** (astrazione) è il processo che sostituisce qualcosa di concreto con una descrizione che riguarda solo alcune proprietà (in generale non tutte):
  - può descrivere **con precisione** alcune proprietà;
  - **non** può descriverle tutte.
- Formalmente, un'astrazione in $\wp(\Sigma)$ di oggetti in $\Sigma$ è un sottoinsieme $A \subseteq \wp(\Sigma)$:
  - gli elementi di $A$ sono le proprietà descritte **esattamente**, senza perdita di precisione;
  - le proprietà che non stanno in $A$ vanno rappresentate tramite altri elementi di $A$, **con perdita di precisione**.

## Objects
Analizzando programmi gli oggetti da considerare sono le parti dello stato della computazione:
- valori: booleani, $\mathbb{Z}$, ecc.
- variabili
- **environments** (ambienti)
- **stacks**
- ...

## Properties
- Una proprietà è l'**insieme degli oggetti che hanno quella proprietà** (visione estensionale).
- Esempi:
  - naturali dispari: $\{1, 3, 5, \dots, 2n+1, \dots\}$
  - interi pari: $\{2z \mid z \in \mathbb{Z}\}$

## The lattice of properties
- L'insieme delle proprietà $\wp(\Sigma)$ degli oggetti $\Sigma$ è un **complete distributive lattice** (reticolo completo distributivo):

$$\langle \wp(\Sigma), \subseteq, \emptyset, \cup, \cap, \neg \rangle$$

  (Nella tupla della slide manca il top $\Sigma$: per completezza sarebbe $\langle \wp(\Sigma), \subseteq, \emptyset, \Sigma, \cup, \cap, \neg \rangle$. Aggiunta: avendo anche il complemento, è in realtà un reticolo booleano completo.)
- Lettura logica:
  - una proprietà è un sottoinsieme di $\Sigma$;
  - $\subseteq$ corrisponde all'**implicazione logica** fra proprietà ($P_1 \subseteq P_2$: chi ha $P_1$ ha anche $P_2$);
  - $\Sigma$ è **true**, $\emptyset$ è **false**;
  - $\cup$ è la **disjunction** (disgiunzione), $\cap$ la **conjunction** (congiunzione), $\neg$ la **negation** (complemento).

## Direction of abstraction
Approssimando una proprietà concreta $P$ con una astratta $P^\sharp$ ci sono due casi:
- **Approximation from below** (dal basso, **under-approximation**): $P^\sharp \subseteq P$
- **Approximation from above** (dall'alto, **over-approximation**): $P \subseteq P^\sharp$
- Si potrebbero considerare anche altre relazioni.
- Le due nozioni sono **duali**; il corso si concentra sulla **seconda** (over-approximation), che è quella che dà la soundness della sezione precedente.

### Approximation from below
- Figura: un'ellisse verde nel piano $(x, y)$ con punti verdi ("Elements in $P$") e alcuni punti marcati da una croce rossa (gli elementi dell'approssimazione, etichetta scritta a mano da leggere come $P^\sharp$). Accanto l'insieme $\{\dots, \langle 19, 77\rangle, \dots, \langle 20, 03\rangle, \langle ?, ?\rangle, \dots\}$.
- Per rispondere a $\langle x, y\rangle \in P$ usando solo $P^\sharp$, con $P^\sharp \subseteq P$:
  - se $\langle x, y\rangle \notin P^\sharp$: **"I don't know"**;
  - se $\langle x, y\rangle \in P^\sharp$: **sì**.

### Approximation from above
- Stessa figura, ma ora l'approssimazione $P^\sharp$ è la regione (l'ellisse) che contiene tutti gli elementi di $P$.
- Per rispondere a $\langle x, y\rangle \in P$ usando solo $P^\sharp$, con $P \subseteq P^\sharp$:
  - se $\langle x, y\rangle \notin P^\sharp$: **no**;
  - se $\langle x, y\rangle \in P^\sharp$: **"I don't know"**.
- Le due tabelline sono speculari: dal basso si possono dare solo risposte "sì" certe, dall'alto solo risposte "no" certe. Nella verifica si usa l'over-approximation: se lo stato d'errore non è in $P^\sharp$, sicuramente non è raggiungibile.

## Un esempio: Sign
- **Programmi**: programmi che manipolano interi.
- **Proprietà**: il segno delle variabili intere.
- **Concrete semantics**: le operazioni standard sugli interi.
- **Abstract semantics**: operazioni astratte, cioè le **regole dei segni**.

### Objects' abstraction
- **Concrete domain**: $\wp(\mathbb{Z})$.
- La proprietà da studiare è il segno delle variabili:
  - $+$ rappresenta gli interi positivi **senza** lo 0;
  - $-$ rappresenta gli interi negativi **senza** lo 0;
  - $0$ rappresenta il singoletto $\{0\}$.
- Figura: il reticolo dei segni (**Sign domain**) a diamante, con $\top$ in cima, $+$, $0$, $-$ al livello intermedio (incomparabili fra loro) e $\bot$ in fondo. $\top$ corrisponde a $\mathbb{Z}$, $\bot$ a $\emptyset$.
- Il dominio dei segni è **contenuto in** $\wp(\mathbb{Z})$: $A = \{\mathbb{Z}, \mathbb{Z}_{>0}, \mathbb{Z}_{<0}, \{0\}, \emptyset\}$.
- Un insieme $X \in \wp(\mathbb{Z})$ è approssimato dal **più piccolo insieme di interi che contiene $X$ e che è rappresentato nel dominio dei segni**. Esempi (aggiunti per chiarezza): $\{1, 5\} \mapsto +$; $\{0\} \mapsto 0$; $\{-1, 0\} \mapsto \top$ (non esiste un elemento "$\leq 0$", quindi si perde precisione); $\emptyset \mapsto \bot$.

### Approximating operators
- La slide mostra le tabelle della somma astratta $\oplus$ e del prodotto astratto $\otimes$ sul dominio $\{\mathbb{Z}, +, -, 0, \emptyset\}$, con la scritta **"wrong"** sotto: le tabelle contengono errori (probabilmente voluti, da scovare). Valori come riportati nella slide (riga $\circ$ colonna):

| $\oplus$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $\emptyset$ |
|---|---|---|---|---|---|
| $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ |
| $+$ | $\mathbb{Z}$ | $+$ | $\mathbb{Z}$ | $+$ | $+$ |
| $-$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $-$ | $-$ | $-$ |
| $0$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $0$ |
| $\emptyset$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $\emptyset$ |

| $\otimes$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $\emptyset$ |
|---|---|---|---|---|---|
| $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $\mathbb{Z}$ | $0$ | $\mathbb{Z}$ |
| $+$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $+$ |
| $-$ | $\mathbb{Z}$ | $-$ | $-$ | $0$ | $-$ |
| $0$ | $0$ | $0$ | $0$ | $0$ | $0$ |
| $\emptyset$ | $\mathbb{Z}$ | $+$ | $-$ | $0$ | $\emptyset$ |

- (Errori nelle tabelle, corretti qui:
  1. **riga/colonna $\emptyset$**: le tabelle trattano $\emptyset$ come elemento neutro, ma l'operazione astratta su $\emptyset$ deve dare $\emptyset$, perché $\{a \circ b \mid a \in \emptyset, b \in Y\} = \emptyset$ (gli operatori sono **strict** su $\bot$). Quindi $X \oplus \emptyset = \emptyset \oplus X = \emptyset$ e $X \otimes \emptyset = \emptyset \otimes X = \emptyset$ per ogni $X$, compresi $\mathbb{Z} \oplus \emptyset$, $0 \oplus \emptyset$, $0 \otimes \emptyset$;
  2. **$- \otimes -$**: la slide dà $-$, ma negativo per negativo è positivo, quindi $- \otimes - = +$.)
- Il resto è corretto: ad esempio $+ \oplus - = \mathbb{Z}$ (il segno della somma non è determinabile: perdita di precisione), $\mathbb{Z} \otimes 0 = 0$ (qui il dominio è preciso), $+ \otimes - = -$.

## Other examples (altri domini astratti)
Le figure mostrano lo stesso insieme di punti concreti (croci rosse nel piano $(x, y)$) approssimato da forme diverse, via via più precise. I numeri delle formule sono illustrativi, presi dalle slide di Cousot, e non vanno letti alla lettera (ad esempio $[20, 03]$ preso sul serio sarebbe un intervallo vuoto).
- **Intervals** (Cousot & Cousot, *Static determination of dynamic properties of programs*, 1976): un rettangolo allineato agli assi, cioè un intervallo per variabile, $x \in [19, 77]$, $y \in [20, 03]$. Non relazionale.
- **Octagons** (Miné, *A New Numerical Abstract Domain Based on Difference-Bound Matrices*, PADO 2001): un ottagono, con vincoli della forma $\pm x \pm y \leq c$, ad esempio $1 \leq x \leq 9$, $x + y \leq 77$, $1 \leq y \leq 9$, $x - y \leq 99$. Relazionale debole, più preciso degli intervalli.
- **Polyhedra** (Cousot & Halbwachs, *Automatic discovery of linear restraints among variables of a program*, POPL 1978): un poliedro convesso, con vincoli lineari arbitrari, ad esempio $19x + 77y \leq 2004$, $20x + 03y \geq 0$. Il più preciso dei tre (inviluppo convesso dei punti), ma più costoso.
- **Simple congruences** (Granger, *Static Analysis of Arithmetical Congruences*, 1989): una griglia di punti (in blu) con le croci rosse sopra, vincoli della forma $x = 19 \bmod 77$, $y = 20 \bmod 99$. Cattura proprietà di regolarità (parità, multipli), non di grandezza.

## Approximating computations
Dopo l'astrazione degli oggetti, la seconda parte della lezione guarda all'astrazione delle **computazioni**. La sequenza di figure (da Cousot) segue sempre lo stesso grafico $x(t)$ in funzione del tempo $t$.

### Possible behaviors
- Figura: più curve colorate continue, le **possible trajectories** (traiettorie possibili) di $x(t)$: ognuna è un'esecuzione del programma.

### Small-step transition semantics
- Figura: le stesse traiettorie rese **discrete**: punti collegati da frecce, un passo di computazione per volta (**possible discrete trajectories**). È la **small-step** (o transition) semantics: ogni freccia è una transizione fra stati.

### Computing on sets
- Figura: a ogni istante discreto gli stati di tutte le traiettorie sono raccolti in un'ellisse grigia (un **insieme di stati**), e frecce rosse collegano un insieme al successivo. Invece di eseguire una traiettoria alla volta, si calcola come evolve l'**insieme** degli stati.

### Computing on set by fixpoint
- Sequenza di figure: si parte dall'insieme degli stati iniziali (prima ellisse), si applica la funzione di transizione per ottenere l'insieme al passo successivo (freccia rossa), e così via finché tutti gli istanti sono coperti. Il risultato è il **fixpoint** (punto fisso) di questa iterazione.

## Where is the approximation?
- Si raccolgono **tutti gli stati che possono comparire su qualche traccia a ogni istante discreto**: questo è **già un'astrazione**.
- Figura: in alto la **trace semantics** (quattro tracce di lunghezze diverse, come sequenze di punti colorati), in basso la **collecting semantics** (per ogni istante un'ellisse con gli stati di tutte le tracce in quell'istante).
- Seconda figura: una **spurious trace** (traccia spuria) in rosso, che salta da una traccia all'altra prendendo uno stato da ciascuna ellisse. Dalla collecting semantics questa traccia sembra possibile, ma non è un'esecuzione reale: raccogliendo gli stati si perdono i legami fra uno stato e il successivo.

## What still we need
- Tracciando **collezioni di stati** invece di singoli stati si hanno **esecuzioni spurie** dovute alla collezione (ma **solo fra stati raggiungibili**).
- Bisogna raccogliere ancora di più: calcolare sui **program points** (punti di programma) invece che sui passi della computazione.

## Collecting semantics (sui program points)
Figure di I. Mastroeni.
- In alto sei tracce di lunghezze diverse sugli istanti discreti $0, \dots, 9$ (**trace semantics**).
- Sotto ogni istante si scrive il program point corrispondente: $1, 2, 3, 4, 2, 3, 4, 2, 3, 4$, cioè un punto iniziale $1$ e un ciclo $2 \to 3 \to 4 \to 2$; le tracce escono in momenti diversi verso il punto $5$ (segnato in rosso a fine traccia).
- Animazione: si costruisce un "contenitore" per ogni program point (1 blu, 2 verde, 3 viola, 4 arancione, 5 rosso). Istante per istante ogni stato viene messo nel contenitore del proprio program point:
  - tempo 0: stati del punto 1;
  - tempi 1, 2, 3: punti 2, 3, poi 4 e 5 (le tracce che escono subito);
  - tempi 4-6: di nuovo 2, 3, 4/5;
  - tempi 7-9: 2/5, 3/5, infine 4.
- Il risultato è la **collecting semantics**: per ogni program point, l'insieme di tutti gli stati che possono trovarsi lì, indipendentemente dal momento e dalla traccia.

## What still we need (2)
- Con la collecting semantics abbiamo raccolto le computazioni, calcolando sui program points invece che sui passi.
- È **ancora indecidibile**: gli insiemi di stati per program point possono essere infiniti.
- Bisogna astrarre ulteriormente: calcolare **proprietà** degli stati raggiungibili in ogni program point.

## Computing on properties
- Figure (da Cousot): si torna al grafico $x(t)$. Al posto dell'ellisse con gli stati esatti, a ogni istante c'è un **rettangolo verde** (un intervallo) che li contiene tutti; il rettangolo successivo si calcola dal precedente (frecce verdi), fino a coprire tutta la traiettoria.
- Dentro i rettangoli compaiono **punti bianchi**: sono stati che nessuna traccia reale raggiunge, ma che l'intervallo include. Sono il rumore introdotto dall'approssimazione dei dati.

## What noise do we add?
- **Collecting semantics**: esecuzioni spurie dovute alla collezione (ma solo su stati raggiungibili).
- **Collecting on properties**: si aggiungono **stati spuri** dovuti all'approssimazione dei dati (i punti bianchi: stati non raggiungibili).

## Semantics as abstractions
Figure (da Cousot): ogni semantica è un'astrazione della precedente.
- **Set of traces** $\xrightarrow{\alpha_1}$ **Trace of sets**: dall'insieme delle tracce a una sequenza di insiemi di stati, uno per istante.
- **Trace of sets** $\xrightarrow{\alpha_2}$ **Trace of intervals**: ogni insieme di stati è sostituito dall'intervallo che lo contiene.
- In alternativa **Trace of sets** $\xrightarrow{\alpha_3}$ **Reachable states**: si dimentica anche il tempo e si tiene un unico insieme con tutti gli stati raggiungibili (un grande rettangolo grigio).

## Summarizing approximations
- Si considerano **proprietà (insiemi) di stati** invece di stati concreti.
- Si passa al calcolo su insiemi, approssimando la trace semantics (la slide dice "We move the computation of sets", da leggere come "we move to the computation on sets").
- Si approssima la computazione calcolando la collecting semantics, cioè la semantica che raccoglie gli stati sui program points.
- La computazione astratta **può ancora non terminare** (e quindi essere indecidibile).
- Si vedrà come risolvere il problema (aggiunta: è il ruolo del **widening** nell'abstract interpretation, nelle lezioni successive).

## Da ricordare
- Schema base: $[[P]] \subseteq Q$ è indecidibile; si calcola $[[P]]^\sharp$ con **soundness** $[[P]] \subseteq [[P]]^\sharp$ e controllo $[[P]]^\sharp \subseteq Q$ decidibile; se vale, $[[P]] \subseteq Q$; altrimenti "non so" (possibile **false alarm**).
- Una proprietà è un insieme di oggetti; $\wp(\Sigma)$ è un reticolo completo con $\subseteq$ = implicazione, $\Sigma$ = true, $\emptyset$ = false, $\cup$ = or, $\cap$ = and, $\neg$ = not.
- Un'astrazione è $A \subseteq \wp(\Sigma)$: gli elementi di $A$ sono rappresentati esattamente, gli altri con perdita di precisione (dal più piccolo elemento di $A$ che li contiene, nel caso dall'alto).
- **Under-approximation** ($P^\sharp \subseteq P$): "sì" certi, altrimenti "non so". **Over-approximation** ($P \subseteq P^\sharp$): "no" certi, altrimenti "non so". Il corso usa l'over-approximation.
- **Sign**: $\top = \mathbb{Z}$, $+$, $0$, $-$, $\bot = \emptyset$; operatori astratti = regole dei segni, strict su $\bot$; $+ \oplus - = \top$ è la tipica perdita di precisione. Le tabelle della slide sono marcate "wrong": errori su $\emptyset$ e su $- \otimes -$.
- Domini numerici in ordine di precisione: **intervals** (non relazionale) < **octagons** ($\pm x \pm y \leq c$) < **polyhedra** (vincoli lineari qualsiasi); **congruences** catturano la regolarità ($x = a \bmod m$).
- Catena di astrazioni delle computazioni: tracce → small-step → insiemi di stati per istante (fixpoint) → **collecting semantics** sui program points (esecuzioni spurie) → proprietà per program point (stati spuri) → reachable states.
- La collecting semantics è ancora indecidibile; anche quella astratta può non terminare: servirà un meccanismo per forzare la convergenza.
