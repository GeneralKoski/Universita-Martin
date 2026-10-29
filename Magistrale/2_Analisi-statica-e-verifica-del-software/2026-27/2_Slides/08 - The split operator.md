# 08 - The split operator

Fonte: `08 - The split operator.pdf`

Il deck non è una lezione ma la presentazione di un articolo di ricerca del gruppo di Parma: *Speeding up Static Analysis with the Split Operator*, di **Vincenzo Arceri, Greta Dolcetti, Enea Zaffanella** (University of Parma), presentato a **SOAP 2023, Orlando** (**[aggiunta]** SOAP è il workshop ACM SIGPLAN *State Of the Art in Program Analysis*, co-locato con PLDI 2023). Molte slide sono solo figure (poliedri, CFG, tabella e grafici sperimentali): qui sono descritte a parole. La numerazione interna salta da 19 a 21 (manca la slide 20, nel PDF ci sono 22 pagine). Le integrazioni sono segnate come **[aggiunta]**. Poiché all'esame il seminario è la presentazione di un articolo, in fondo c'è anche la struttura dell'articolo letta come modello (problema, idea, formalizzazione, risultati, limiti).

## Outline
- Filtering an Abstract Element.
- The Split Operator: formalizzazione, esempi, implementazione.
- Experimental Evaluation.
- Conclusion and Future Works.

## Filtering an abstract element
$$\mathsf{filter} : \mathbb{A} \times \mathsf{Pred} \to \mathbb{A}$$

- Il **filter** è un operatore astratto comune a tutti i domini: dato un elemento astratto e un predicato (una guardia), restituisce l'elemento astratto ristretto agli stati che soddisfano il predicato.
- Serve a **modellare il flusso di controllo**: le guardie di `if` e `while`. È lo stesso $[\![ b ]\!]^\sharp$ visto nel deck 07 (le guardie del CFG agiscono da filtri) e il "filtro" $\cap$ sulle guardie del deck 03.
- È adottato da molti tool: **Crab, IKOS, LiSA, MOPSA**, ...
- **[aggiunta]** Sui poliedri un test lineare $\sum_i \alpha_i x_i \le \beta$ è **esatto**: basta aggiungere il vincolo al sistema (Miné, tutorial, §5.3.3). Un test non lineare o un $\neq$ si approssima con l'identità.

### Esempio: il problema
Figura: un `if (i < 50) do_this(i); else do_that(i);` con l'elemento astratto $A$ in entrata.

```
          A
          |
  copy ---+--- copy
   |              |
   A              A
   | filter(i < 50)     | filter(i >= 50)
   v                    v
 A_{i<50} -> do_this(i)   A_{i>=50} -> do_that(i)
```

- L'elemento $A$ viene **copiato due volte** e su ogni copia si chiama `filter`, una volta con il predicato e una con il complemento. Le frecce rosse nella figura evidenziano le due copie e le due chiamate.
- Il risultato è **corretto e preciso**, ma inefficiente:
  - **replicated work**: le due chiamate rifanno gran parte dello stesso calcolo;
  - **overheads** delle copie;
  - **two invocations** dell'operatore.

## The split operator
$$\mathsf{split} : \mathbb{A} \times \mathsf{Pred} \to \mathbb{A} \times \mathbb{A}$$

- Fa il filtro **sul predicato e sul suo complemento nello stesso momento** e restituisce la coppia (ramo then, ramo else).
- **[aggiunta]** La specifica è semplicemente
$$\mathsf{split}(A, c) = \big(\mathsf{filter}(A, c),\ \mathsf{filter}(A, \neg c)\big)$$
  quindi il risultato è identico a quello delle due chiamate separate: l'operatore cambia il **costo**, non la **precisione**, e la soundness discende da quella di `filter`.
- Implementato nella libreria di poliedri **PPLite** (sviluppata a Parma da Zaffanella).
- **Obiettivo**: migliorare l'efficienza.
- Stesso esempio con split: da $A$ una sola chiamata `split(i < 50)` produce $A_{i<50}$ (verso `do_this(i)`) e $A_{i \ge 50}$ (verso `do_that(i)`). Corretto e preciso, **niente lavoro replicato, niente overhead, una sola invocazione**.

## Splitting polyhedra on linear constraints
Le slide 6-11 mostrano cosa fa split sui **poliedri**, sempre a partire dal quadrato

$$P \equiv \{0 \le x_0 \le 3,\ 0 \le x_1 \le 3\}$$

Nelle slide 6-8 sono disegnati anche i punti a coordinate intere (variabili intere), nelle slide 9-11 solo i vertici.

### Vincolo obliquo: $c \equiv (2x_0 + 2x_1 \le 5)$ (slide 6)
- Tre pannelli: $P$; $P$ con la retta tratteggiata $c$; il risultato dello split.
- Risultato sugli interi:
  - $P_{\mathrm{then}}$ (blu): $x_0 + x_1 \le 2$, il triangolo con i punti $(0,0), (1,0), (2,0), (0,1), (1,1), (0,2)$;
  - $P_{\mathrm{else}}$ (rosso): $x_0 + x_1 \ge 3$, il resto del quadrato.
- Fra i due poliedri resta una striscia vuota attorno alla retta $c$: nessun punto intero ha $2x_0 + 2x_1 \in (4, 6)$, cioè $2x_0 + 2x_1 = 5$ è impossibile sugli interi.
- **[aggiunta]** Da $2x_0 + 2x_1 \le 5$ si passa a $x_0 + x_1 \le 2$ con il **rafforzamento sugli interi**: si divide per il MCD dei coefficienti ($2$) e si arrotonda il termine noto, $\lfloor 5/2 \rfloor = 2$. Il complemento $2x_0 + 2x_1 > 5$ diventa $x_0 + x_1 \ge 3$. È la tecnica descritta nel tutorial di Miné, §5.3.9 (*Handling Integers*).

### Uguaglianza interna: $c \equiv (x_0 = 2)$ (slide 7)
- $P_{\mathrm{then}}$ (blu) è il segmento $x_0 = 2,\ 0 \le x_1 \le 3$.
- $P_{\mathrm{else}}$ (rosso) è **tutto $P$**: il complemento $x_0 \neq 2$, cioè $x_0 \le 1 \vee x_0 \ge 3$, **non è convesso**, e il più piccolo poliedro che lo contiene è $P$ stesso.
- **[aggiunta]** È lo stesso limite dei filtri $\neq$ con gli intervalli (deck 03: il filtro $i \mathrel{!=} 0$ non toglie lo 0 da $[-1, 1]$): un dominio convesso non può "bucare" un insieme.

### Uguaglianza sul bordo: $c \equiv (x_0 = 3)$ (slide 8)
- Ora la retta coincide con un **lato** di $P$.
- $P_{\mathrm{then}}$ (blu) è il segmento $x_0 = 3,\ 0 \le x_1 \le 3$, disegnato spostato a destra per leggibilità.
- $P_{\mathrm{else}}$ (rosso) è $0 \le x_0 < 3$, che sugli interi diventa $0 \le x_0 \le 2$: la striscia fra $x_0 = 2$ e $x_0 = 3$, evidenziata in rosso scuro, viene tolta. Qui il complemento è convesso e lo split guadagna precisione rispetto al caso precedente.

### Come lavora split sulla rappresentazione (slide 9-11)
- Slide 9: $P$ con i soli 4 vertici, come poliedro razionale.
- Slide 10, $c \equiv (2x_0 + 2x_1 \le 5) \to P_{\mathrm{then}} = \mathsf{filter}(P, c)$, in quattro passi:
  1. $P$ e la retta $c$;
  2. i vertici vengono **classificati**: $(0,0)$ soddisfa $c$ (blu), $(3,0)$, $(0,3)$, $(3,3)$ la violano (rossi);
  3. si calcolano i **nuovi vertici sulla retta**, combinando coppie di vertici adiacenti che stanno da parti opposte: $(0, 2.5)$ e $(2.5, 0)$ (il punto grigio sulla retta indica il calcolo dell'intersezione);
  4. $P_{\mathrm{then}}$ è il triangolo $(0,0), (2.5,0), (0,2.5)$.
- Slide 11, $\neg c \equiv (2x_0 + 2x_1 \ge 5)$: stessi quattro passi con i colori invertiti. $(0,0)$ è l'unico vertice che viola $\neg c$, e i **nuovi vertici sono gli stessi** $(0, 2.5)$ e $(2.5, 0)$. $P_{\mathrm{else}}$ è il pentagono $(0,2.5), (0,3), (3,3), (3,0), (2.5,0)$.
- (Errore nella slide 11: la didascalia dice $P_{\mathrm{then}} = \mathsf{filter}(P, \neg c)$, ma il risultato del filtro sul complemento è $P_{\mathrm{else}}$, come scrive la figura stessa.)
- (Imprecisione nella slide 11: la negazione esatta di $2x_0 + 2x_1 \le 5$ è $2x_0 + 2x_1 > 5$, **stretta**. Con poliedri chiusi si usa la chiusura $\ge 5$, che è una sovra-approssimazione sound (Miné, §5.3.8); la retta $c$ finisce così in entrambi i rami. PPLite supporta anche i poliedri NNC, che rappresentano il vincolo stretto in modo esatto; sugli interi si ottiene $x_0 + x_1 \ge 3$ come nella slide 6.)
- **[aggiunta]** La morale delle due slide è il **lavoro replicato**. Nella **double description** (vincoli + generatori, Miné §5.3.1-5.3.2) aggiungere un vincolo vuol dire scorrere i generatori, classificarli per segno rispetto all'iperpiano e generare i nuovi vertici combinando le coppie adiacenti (un passo dell'algoritmo di Chernikova). Per $c$ e $\neg c$ la classificazione è la stessa a segni invertiti e i vertici sull'iperpiano sono identici: due `filter` fanno due volte il calcolo, `split` lo fa una volta sola e distribuisce i generatori fra i due risultati.

## Implementazione
### Clam/Crab
- Sono moduli del framework **SeaHorn**.
- **Crab**: libreria C++ di analisi statica; contiene domini astratti e motori di punto fisso; ha una propria rappresentazione intermedia, **CrabIR**.
- **Clam**: front-end di Crab, traduce $\texttt{C} \to \texttt{LLVM} \to \texttt{CrabIR}$.

### Modifiche in Crab
- Nel **componente dei domini astratti**:
  - un nuovo metodo per lo split;
  - la chiamata a una funzione ad hoc di **PPLite**;
  - la gestione delle **implementazioni di default non ottimizzate**, per i domini che non hanno uno split nativo (**[aggiunta]** presumibilmente copia + due `filter`, cioè il comportamento di prima).
- Nel **motore di approssimazione del punto fisso**:
  - un nuovo statement astratto, `split`;
  - gli **invarianti memorizzati sugli archi** invece che sui nodi.

### Esempio: CFG di Crab con e senza split
Programma: `void foo() { int i=0; while (i<50) i=bar(i); }`

**Default CFG** (invarianti $\langle pre, post \rangle$ su ogni nodo):

```
entry: i.0 = 0
   |
while.cond: <------------------------+
   |                      \          |
__@bb_5:                __@bb_6:     |
assume(i.0 <= 49)       assume(-i.0 <= -50)
   |                        |        |
while.body:             while.end:   |
call:int32 = call bar(i.0:int32)     |
i.0 = call  -------------------------+
```

- La guardia `i < 50` diventa **due blocchi** `assume`, uno per ramo: `assume(i.0 <= 49)` e `assume(-i.0 <= -50)`, cioè $i \ge 50$ (sugli interi $i < 50 \iff i \le 49$). Ognuno ha la sua coppia $\langle pre, post \rangle$; i tre nodi evidenziati in rosso (`while.cond` e i due `assume`) sono quelli che cambiano.

**CFG with split stmt**:

```
entry: i.0 = 0
   | <inv>
while.cond: split(i.0 <= 49)
   | <inv_then>   ^ <inv>        \ <inv_else>
while.body:       |              while.end:
call:int32 = call bar(i.0:int32)
i.0 = call  ------+
```

- I due `assume` spariscono: il nodo `while.cond` (in verde) contiene `split(i.0 <= 49)`, e i due risultati vanno sugli archi uscenti come $\langle inv_{\mathrm{then}} \rangle$ e $\langle inv_{\mathrm{else}} \rangle$. Per questo gli invarianti si salvano sugli archi.
- **[aggiunta]** Meno nodi vuol dire meno elementi astratti da memorizzare e meno equazioni nel sistema di punto fisso (deck 07): l'effetto si vede nel grafico della memoria più avanti.

### Note sul prototipo
- In Crab alcuni test vengono già ignorati: **floating point** e **variabili unsigned**.
- Il prototipo ignora anche gli statement `select` (**[aggiunta]** l'istruzione LLVM `select`, cioè l'operatore ternario `c ? a : b` senza salti, che quindi non genera split).

## Experimental evaluation
### Setup
- Confronto fra **PPLite** ed **ELINA** senza split e **PPLite con split**.
- Due benchmark:
  - **WCET analysis** (PAGAI, 39 file);
  - **Linux drivers** (SVCOMP, 7 file).
- Configurazione di Crab: gli statement `switch` sono abbassati (**lowered**) a catene di confronti; **inlining sistematico** delle chiamate di funzione.

### Tempi (slide 18)
Tabella ridotta ("abridged"): le prime 5 righe sono test PAGAI, le ultime 7 i driver Linux. L'unità non è indicata (presumibilmente secondi); **time ratio** = PPLite senza split / PPLite con split, quindi $> 1$ è uno speed-up.

| test | PPLite senza split | ELINA senza split | PPLite con split | time ratio |
|---|---|---|---|---|
| adpcm | 108.2 | (★) 1.6 | 105.9 | 1.02 |
| prog9000 | 31.8 | 241.1 | 42.0 | **0.76** |
| nsichneu | 30.9 | 40.8 | 21.1 | 1.46 |
| decompress | 5.3 | 5.5 | 2.3 | 2.30 |
| filter | 2.5 | 2.3 | 2.5 | 1.00 |
| mmc-host | 487.1 | 435.1 | 412.9 | 1.18 |
| firewire | 98.7 | (★) 92.0 | 22.7 | **4.35** |
| hwmon-abituguru3 | 87.5 | 91.0 | 52.8 | 1.66 |
| media-usb-tm6000 | 23.2 | 22.3 | 12.4 | 1.87 |
| media-pci-ttpci | 12.3 | 12.9 | 10.8 | 1.14 |
| power-bq2415x | 10.1 | 10.9 | 11.6 | 0.87 |
| hid-usb | 8.6 | 10.1 | 6.0 | 1.43 |

- **Di solito uno speed-up significativo**: il migliore è firewire (4.35, evidenziato in giallo), poi decompress (2.30).
- **Qualche rallentamento**, dovuto alla **fase di finalizzazione**: prog9000 (0.76, evidenziato in rosso) e power-bq2415x (0.87).
- Il simbolo (★) accanto ad alcuni tempi di ELINA non è spiegato nelle slide (rimanda all'articolo).
- **[aggiunta]** Ho ricontrollato i rapporti: tutti coincidono con PPLite senza split / PPLite con split, arrotondati alla seconda cifra.

### Memoria (slide 19)
Due istogrammi a barre, **No Split** (blu) contro **Split** (arancio), su 12 test non etichettati, ordinati per valore crescente.
- **Peak Memory Usage (MB)**: per i test piccoli le barre quasi coincidono, per i grandi il calo è forte. Letture a occhio dei casi più grandi: circa $9700 \to 1100$ MB, $7700 \to 250$ MB, $3300 \to 200$ MB, $1600 \to 600$ MB, $1650 \to 1400$ MB.
- **# CFG Nodes**: lo split riduce sempre il numero di nodi, a occhio fra circa il 13% e il 60% (il massimo passa da circa 26000 a 19700, poi $23700 \to 20500$, $15400 \to 12800$, $9800 \to 6800$, $9000 \to 5600$, $7300 \to 4700$, $2000 \to 750$).
- **[aggiunta]** Il risparmio di memoria è molto più che proporzionale ai nodi tolti: oltre ai nodi `assume` scompaiono le copie degli elementi astratti, e sui poliedri ogni copia può essere grande.

## Conclusion
- **Risultati**:
  - implementazione **prototipale**;
  - miglioramenti **non banali di memoria e tempo**;
  - **nessuna perdita di precisione**.
- **Lavori futuri**:
  - lo split per **altri domini astratti**;
  - l'estensione ad **altri tool**.

## Struttura dell'articolo (modello per il seminario)
- **Problema**: il `filter` sui rami di `if`/`while` si chiama due volte su copie dello stesso elemento, con lavoro duplicato. Su domini costosi come i poliedri pesa.
- **Idea**: un nuovo operatore astratto $\mathsf{split} : \mathbb{A} \times \mathsf{Pred} \to \mathbb{A} \times \mathbb{A}$ che fa entrambi i filtri insieme. Non cambia il dominio, cambia l'**operatore** (è una delle due "soluzioni canoniche" citate nel deck 09).
- **Formalizzazione**: la specifica è la coppia dei due `filter`, quindi soundness e precisione sono le stesse; la parte tecnica è l'algoritmo in PPLite che riusa la classificazione dei generatori e i nuovi vertici.
- **Implementazione**: modifiche al dominio e al motore di punto fisso di Crab (statement `split`, invarianti sugli archi).
- **Valutazione**: PAGAI e driver Linux da SVCOMP; speed-up fino a 4.35, due rallentamenti (0.76 e 0.87), forti risparmi di memoria, meno nodi nel CFG.
- **Limiti** (alcuni dichiarati, altri **[aggiunta]**): prototipo; solo PPLite ha uno split nativo; floating point, unsigned e `select` sono ignorati; i rallentamenti vengono dalla finalizzazione; il guadagno dipende da quante guardie ha il programma e da quanto costa il dominio (sugli intervalli un filtro costa già poco).

## Da ricordare
- $\mathsf{filter} : \mathbb{A} \times \mathsf{Pred} \to \mathbb{A}$ modella le guardie; sui due rami di un `if` si chiama due volte, su due copie.
- $\mathsf{split} : \mathbb{A} \times \mathsf{Pred} \to \mathbb{A} \times \mathbb{A}$, $\mathsf{split}(A, c) = (\mathsf{filter}(A, c), \mathsf{filter}(A, \neg c))$: stesso risultato, una sola invocazione, niente copie.
- Sui poliedri: complemento convesso (vincolo obliquo, uguaglianza sul bordo) dà due pezzi precisi; complemento non convesso (uguaglianza interna) dà $P_{\mathrm{else}} = P$. Sugli interi i vincoli si rafforzano ($2x_0 + 2x_1 \le 5 \Rightarrow x_0 + x_1 \le 2$, complemento $x_0 + x_1 \ge 3$).
- Il guadagno nasce dal lavoro condiviso sui generatori: stessa classificazione, stessi nuovi vertici sull'iperpiano.
- In Crab: nuovo statement `split`, invarianti sugli archi, i due `assume` per ramo spariscono.
- Risultati: speed-up fino a **4.35** (firewire), rallentamenti **0.76** (prog9000) e **0.87** (power-bq2415x) per la finalizzazione; memoria di picco fino a circa $9700 \to 1100$ MB; **nessuna perdita di precisione**.
