# 10 - Statically analyzing R vectors

Fonte: `10 - Statically analyzing R vectors.pdf`

Non è una lezione del prof ma il **seminario** tenuto il 28/10/2026 da **Manuel Di Agostino** (Università di Parma), titolo "Statically reasoning about R vectors - Designing an abstract domain for a real language". Presenta l'articolo *Towards Statically Reasoning about R Vectors* (M. Di Agostino, F. Sihler, V. Arceri, O. Gerstl, M. Tichy; NSAD '26, pp. 18-25, doi:10.1145/3840563.3843708), scritto fra Parma e Ulm. Il PDF ha 164 pagine ma le slide sono 54: quasi tutte sono costruite per build incrementali (gli esempi di codice partono con `# ?` e si svelano una riga alla volta, le definizioni compaiono un punto alla volta). Qui sono raggruppate e citate con il numero stampato in basso (n/54). Due numeri sono ripetuti su slide diverse (47: selezione negativa e logica; 49: update negativo e logico) e i titoli di sezione non sono numerati. Le integrazioni sono segnate come **[aggiunta]**, gli errori sono segnalati dove compaiono.

## Struttura del seminario **[aggiunta]**
Utile come modello per il seminario d'esame: il percorso è dichiarato già nella roadmap (slide 2), **R → μR → Domain → Operators → Validation**, e le 54 slide si dividono in otto parti.

| Parte | Slide | Ruolo nel racconto |
|---|---|---|
| 1. From S to R | 3-6 | contesto: perché R conta e perché mancano strumenti |
| 2. Why R resists static analysis | 7-16 | il **problema**: ogni feature di R spiegata con un esempio eseguibile |
| 3. Analysis problem and soundness contract | 17-21 | obiettivo formale, soundness, related work, requisiti |
| 4. The μR language | 22-28 | **idea**: un linguaggio nucleo con semantica concreta precisa |
| 5. The abstract domain | 29-39 | **formalizzazione** del dominio: elementi, ordine, join, meet, widening, γ, assenza di GC |
| 6. Abstract operators | 40-49 | operatori astratti, ognuno con un esempio numerico |
| 7. Implementation and validation | 50-52 | **risultati**: prototipo in flowR, tre test, 61 programmi |
| 8. Conclusions and open problems | 53-54 | **limiti**: cosa è dimostrato, cosa solo testato, cosa manca |

- Ogni slide della parte 2 chiude con una riga "**→ The analysis must know: ...**"; queste righe vengono raccolte nel *design brief* (slide 21), che diventa la lista dei requisiti del dominio. Così il dominio della parte 5 appare come risposta a richieste già motivate, non come scelta arbitraria.
- Un **running example** di quattro righe (slide 28) viene fissato prima del dominio, con la promessa che la parte astratta dovrà predirlo senza eseguirlo.
- Ogni definizione formale è seguita subito da un esempio con numeri piccoli e controllabili a mano.
- Il **risultato negativo** (non esiste una connessione di Galois) è presentato come contributo, con controesempio esplicito.
- La chiusura distingue con onestà ciò che è **dimostrato** da ciò che è **solo empirico**, e classifica i problemi aperti per natura (dominio, semantica, ingegneria).

## 1. Da S a R (slide 3-6)
Una timeline che si allunga di slide in slide, ognuna con un riquadro sul modo di lavorare dell'epoca.
- **1976 → 1988, Batch (Fortran)**: S nasce ai Bell Labs nel 1976; nel 1988 esce S3 (*The New S Language*). Prima di S il ciclo era edit → submit → queue → print, **in ore**:

```fortran
      PROGRAM ANALYSIS
      READ (5, *) N, (X(I), I = 1, N)
      CALL MEAN(X, N, AVG)
      WRITE (6, *) AVG
      STOP
      END
C     unit 5 = card reader
C     unit 6 = line printer
```

- **Interactive (S)**: "S: an interactive environment for statisticians". Il ciclo diventa type → see → adjust, **in secondi**:

```r
x <- c(3.1, 4.2, 5.0)
mean(x)          # whole column
plot(x, y)
lm(y ~ x1 + x2)  # formula
```

- **1976 → 1996, Pipeline (R)**: R rilasciato pubblicamente nel 1993, GPL e primo articolo nel 1995-96. "R: a free S, built by statisticians". Dal file alla figura in un'unica espressione:

```r
read.csv("cars.csv") |>
  subset(speed > 10) |>
  transform(time = dist / speed) |>
  plot(time ~ speed, data = _)
```

- **[aggiunta]** L'esempio è illustrativo, non d'epoca: la pipe nativa `|>` esiste da R 4.1 (2021) e il segnaposto `_` da R 4.2 (2022).
- **1976 → 2026**: 1997-2000 CRAN, GNU, R 1.0.0; nel 2026 **25.500+ pacchetti** (25.529 su CRAN al 25 ottobre 2026). Messaggio: "The ecosystem grew faster than the tooling". Fonti delle date: R. Ihaka, *R: Past and Future History* (1998); R FAQ §3.3.1.
- **The tooling gap** (slide 6): quattro cause convergono in "**R runs in production, without production tooling**":
  - correttezza verificata con **grafici e test**;
  - **nessuna comunità** che costruisce strumenti (J. Fox, The R Journal 1(2), 2009);
  - licenza **GPL**: nessun vendor ha incentivo a investire;
  - crescita trainata da **esperti di dominio**, non da informatici.

## 2. Perché R resiste all'analisi statica (slide 7-16)

### Everything is a vector (slide 7)
- `TRUE` è un *logical* di lunghezza 1, `3` o `3.14` un *double* di lunghezza 1, `c(1L, 2L, 3L)` un *integer* di lunghezza 3, `"hello"` un *character* di lunghezza 1. **Non esiste un tipo scalare.**
- `NA` segue la stessa regola: è la **sentinella del valore mancante**, occupa una posizione e **si propaga**.

```r
length(NA)          # 1          one element, and it is missing
c(1, 2, NA)         # [1, 2, NA] NA occupies position 3
mean(c(1, 2, NA))   # NA         and it propagates
```

### NA is not NULL (slide 8)
- **NA**: il valore è *sconosciuto*; è un elemento, sta in una posizione, ogni operazione su di esso dà NA.
- **NULL**: *non c'è* valore; non è un elemento, non ha posizione, sparisce dal vettore e la lunghezza cala.

```r
x <- c(1, NA, 3)
length(x)        # 3
sum(x)           # NA

y <- NULL
length(y)        # 0
c(1, NULL, 3)    # [1, 3]
```

- `NULL` è il vettore vuoto e `c()` ne è il letterale.
- → L'analisi deve sapere: **quanto è lungo il valore e cosa c'è in ogni posizione.**

### Silent coercion (slide 9-10)
- Gli elementi di un vettore devono avere **lo stesso tipo**, con la gerarchia logical ≺ integer ≺ double ≺ character. Se i tipi sono mescolati, gli elementi vengono promossi al **least upper bound**, senza errori né warning e senza che il sorgente dica `character`:

```r
c(TRUE, "hello")     # ["TRUE", "hello"]
c(NA, "hello")       # [NA, "hello"]   NA esiste una volta per tipo, non è la stringa "NA"
c(TRUE, 3L, 2.5)     # [1.0, 3.0, 2.5]  double
1L + TRUE            # 2L               integer
```

- **[aggiunta]** La gerarchia completa di R ha anche `complex` fra double e character (e `raw` sotto logical); la slide riporta solo i quattro tipi atomici usati nel lavoro. È la stessa idea del lub nei reticoli (deck 02): il tipo di `c(...)` è il join dei tipi degli argomenti in una catena.
- → L'analisi deve sapere: **che tipo può avere ogni elemento.**

### Recycling (slide 11-12)
- Le operazioni sono **element-wise**; se le lunghezze differiscono, il più corto viene **riciclato** fino alla lunghezza del più lungo (per questo `x > 3` funziona senza scrivere `c(3, 3, 3, 3)`):

```r
c(1, 2, 3) + c(3, 2, 1)              # [4, 4, 4]
c(0, 0, 0, 0) + c(1, 2)              # [1, 2, 1, 2]
c(1, 2, 3, 4, 5, 6) + c(10, 20, 30)  # [11, 22, 33, 14, 25, 36]
c(1, 5, 2, 8) > 3                    # [FALSE, TRUE, FALSE, TRUE]
c(1, 5, 2, 8) > c(4, 6)              # [FALSE, FALSE, FALSE, TRUE]
```

- Se la lunghezza maggiore **non è multipla** della minore, R emette un **warning** e calcola comunque:

```r
r <- c(1, 1, 1)
if (runif() >= 0.5) {
  r <- r + c(41, 41, 41, 41)   # [WARN] [1, 1, 1] recycled to [1, 1, 1, 1]
} else {
  r <- r - c(1)                # [1] recycled to [1, 1, 1]
}
# r è [42, 42, 42, 42] oppure [0, 0, 0]
```

- (Imprecisione nelle slide: `runif()` senza argomenti in R dà errore, perché `n` è obbligatorio; va letto `runif(1)`. Vale per tutti gli esempi del deck che usano `runif()` come scelta casuale.)
- → L'analisi deve sapere: **è il ramo preso a decidere la lunghezza, non la sintassi.**

### Attributes e data frame (slide 13-14)
- Ogni oggetto R può avere **attributi**; `dim`, `class` e `names` cambiano ciò che l'oggetto *è*:

```r
x <- 1:10
dim(x) <- c(2, 5)
#      [,1] [,2] [,3] [,4] [,5]
# [1,]    1    3    5    7    9
# [2,]    2    4    6    8   10
```

  I dieci interi sono gli stessi, la forma no: senza `dim` è un vettore integer, con `dim` è una matrice, `x[1, 2]` diventa un indice legale e si applicano `%*%`, `t`, `solve`.
- Un **data frame non è un primitivo**: è una lista con nomi più attributi.

```r
l <- list(1:3, c("a", "b", "c"))
names(l)                       # NULL
names(l) <- c("id", "label")   # the names become the columns
df <- as.data.frame(l)         # adds class and row.names
#   id label
# 1 1      a
# 2 2      b
# 3 3      c
```

- → L'analisi deve sapere: **quali attributi sono presenti, non solo gli elementi.**

### Three indexing modes (slide 15)
Le parentesi sono le stesse, è l'indice a decidere l'operazione:

```r
v <- c(10, 20, 30, 40)
v[c(2, 0, 5)]       # [20, NA]   0 is skipped, 5 is out of bounds
v[c(-1, -3)]        # [20, 40]   positions 1 and 3 are removed
v[c(TRUE, FALSE)]   # [10, 30]   mask recycled to length 4
```

- **positivo**: seleziona per posizione; `0` viene saltato, fuori dai limiti dà `NA`;
- **negativo**: esclude per posizione; tutto ciò che non è elencato resta;
- **logico**: filtra con una maschera, riciclata alla lunghezza del vettore.
- R **rifiuta** indici positivi e negativi mescolati; `0` è ammesso con entrambi.
- **[aggiunta]** Gli indici partono da **1** (indicizzazione 1-based): per questo `0` non indica nessuna posizione.
- → L'analisi deve sapere: **il modo di ogni indice e la lunghezza del risultato.**

### Update (slide 16)
L'assegnamento non è locale: `v[i] <- x` può **far crescere** il vettore.

```r
v <- c(10, 20, 30)
v[5] <- 99                # [10, 20, 30, NA, 99]
v[-2] <- 5                # [5, 20, 5, 5, 5]
v[c(TRUE, FALSE)] <- 0    # [0, 20, 0, 5, 0]
v[0] <- 5                 # unchanged, and no error
```

- oltre la fine: il vettore si allunga e il buco si riempie di `NA`;
- un indice negativo o una maschera riciclata scrive **un valore in molte posizioni**;
- l'indice `0` non scrive niente, e R non protesta.
- → L'analisi deve sapere: **se la lunghezza è ancora nota dopo l'update.**

## 3. Il problema di analisi e il soundness contract (slide 17-21)

### Cosa si vuole sapere (slide 17-18)
**Definizione (collecting semantics).** Uno stato $\sigma$ associa a ogni variabile il vettore che contiene, $\sigma : Var \rightharpoonup \mathcal{V}$, e per ogni etichetta $\ell \in L$ (l'insieme delle etichette del programma)

$$[\![P]\!](\ell) \stackrel{\text{def}}{=} \{\sigma \mid \text{some run of } P \text{ reaches } \ell \text{ in state } \sigma\}$$

- Esempio: dopo `v <- c(10, 20, 30); if (runif() >= 0.5) v <- v * 2` arrivano in fondo due stati, $\{v \mapsto [10, 20, 30]\}$ oppure $\{v \mapsto [20, 40, 60]\}$.
- **Non calcolabile** in generale: decidere $\sigma \in [\![P]\!](\ell)$ equivale a decidere la raggiungibilità, che è indecidibile.
- Si calcola un'approssimazione **flow-sensitive** (uno stato astratto per punto di programma) e **non relazionale** (un insieme di vettori per variabile, senza relazioni fra variabili).
- **[aggiunta]** È la stessa collecting semantics dei deck 03 e 07, con i vettori al posto degli interi.

### The soundness contract (slide 19)
**Definizione (soundness).** Un'analisi è sound se non perde mai un'esecuzione:

$$\forall \ell .\ [\![P]\!](\ell) \subseteq \gamma\big([\![P]\!]^\sharp(\ell)\big)$$

- $\gamma$ può essere **troppo grande**: costa un falso allarme.
- $\gamma$ non può mai essere **troppo piccola**: un'esecuzione fuori da $\gamma$ è un comportamento che l'analisi ha perso.
- Lo stesso obbligo, un livello più giù, sugli **operatori**:

$$c \in \gamma(\nu) \Rightarrow \mathrm{op}(c) \in \gamma\big(\mathrm{op}^\sharp(\nu)\big)$$

- **[aggiunta]** È la forward soundness del deck 07, $f(\gamma(a)) \sqsubseteq_C \gamma(f^\sharp(a))$, scritta elemento per elemento. Notare che è formulata **solo con $\gamma$**: anticipa che in questo dominio $\alpha$ non esiste (slide 38-39).

### Domini e strumenti esistenti (slide 20)
- **FunArray** (Cousot, Cousot, Logozzo, POPL 2011): segmenti uniformi, nessun valore per singola posizione. Il recycling costringe a scegliere: srotolare ogni posizione in un segmento (e la segmentazione si dissolve) o riassumere (e perdere proprio i fatti che il recycling richiede).
- **Giet et al.** (Giet, Ridoux, Rival, SAS 2023, prodotto di astrazioni di shape e di sequenza): fatti sull'intera sequenza; il recycling richiede valori per posizione e non preserva l'ordinamento.
- **flowR** (Sihler, Tichy, PACMPL/OOPSLA 2025): grafi di dataflow e slicing per R, la piattaforma su cui è costruito il prototipo (parte 7); nessun dominio astratto per il contenuto dei vettori.
- **Data frames** (Gerstl, tesi magistrale, Ulm 2025): modella le trasformazioni dei data frame, ma la semantica dei vettori sottostanti resta non modellata.

### The design brief (slide 21)
Messi insieme, i requisiti che qualunque analisi statica dei vettori R deve soddisfare:
- **Length**: quali lunghezze sono possibili, da `NULL` (0) a illimitata.
- **Content**: quale valore e quale tipo può avere ogni elemento.
- **Operations**: quali posizioni sopravvivono a una selezione e se un update fa crescere il vettore.
- **Attributes**: presenti di sicuro, o solo possibilmente.
- **Termination**: la lunghezza può crescere senza limite, quindi l'iterazione deve fermarsi (serve un widening).

## 4. Il linguaggio μR (slide 22-28)

### Perché μR (slide 22)
R reale è molto più largo dei vettori; ogni punto con il suo esempio:

```r
e <- new.env()                          # environments are first-class values
e$x <- 1

f <- function(a, b) a * 10              # arguments are lazy promises
f(10, stop("boom"))   # 100: b unused
f(stop("boom"), 1)    # Error: a used

eval(quote(`+` <- function(a, b) 42))   # metaprogramming rewrites code at run time
1 + 2   # 42

length.foo <- function(x) 42            # every call goes through S3/S4 dispatch
v <- c(1, 2, 3)
class(v) <- "foo"
length(v)   # 42, not 3
```

μR tiene i costrutti che toccano i vettori e lascia il resto:
- `NULL` non è un oggetto speciale: è il **vettore vuoto**;
- un environment non è un valore: è una **mappa piatta** da variabili a vettori.

### Sintassi (slide 23)
`if-else` e `while` sono omessi per brevità.

$$\begin{aligned}
E_{idx} &::= \varepsilon \mid E \\
Atm &::= Var \mid Float \mid Int \mid Bool \mid \texttt{NULL} \\
Bool &::= \texttt{TRUE} \mid \texttt{FALSE} \mid \texttt{NA} \\
\bowtie_{arith} &::= + \mid - \mid * \mid / \qquad
\bowtie_{rel} ::= \ > \mid < \mid == \mid \neq \mid \le \mid \ge \qquad
\bowtie_{log} ::= \texttt{\&} \mid \texttt{|} \qquad
\triangleright ::= \ ! \mid - \\
E &::= Atm \mid \triangleright E \mid e_1 \bowtie_{arith} e_2 \mid e_1 \bowtie_{rel} e_2 \mid e_1 \bowtie_{log} e_2 \mid \texttt{c()} \mid \texttt{c}(E_1, \dots, E_n) \mid Var \leftarrow E \\
&\phantom{::=}\ \mid Var[E_{idx}] \mid Var[[E_{idx}]] \mid Var[E_{idx}] \leftarrow E \mid Var[[E_{idx}]] \leftarrow E \mid \texttt{setAttr}(Var, \{s_1, \dots, s_n\}) \mid \texttt{getAttr}(Var)
\end{aligned}$$

- Le build evidenziano la corrispondenza fra sintassi e operatori semantici: `c(...)` → $\oplus$ (concatenazione), $\bowtie$ → **Recycle**, `v[i]` → **Select**, `v[i] <- e` → **Update**. L'ultima build evidenzia il resto: `[[ ]]`, `setAttr`, `getAttr` e l'indice vuoto $\varepsilon$.
- **[aggiunta]** $\varepsilon$ è l'indice vuoto di `v[]`, che restituisce tutto il vettore (e `v[] <- x` lo sovrascrive tutto mantenendo la lunghezza); `[[ ]]` estrae o scrive un singolo elemento.

### Il vettore concreto (slide 24)
**Definizione.** Un vettore concreto $v \in \mathcal{V}$ è una coppia $([e_1, \dots, e_n], \mathcal{A}) \in (\mathbb{N} \to \mathbb{V}_{Atm}) \times \mathcal{A}$: una mappa **totale** da indici a valori atomici, più un insieme di nomi di attributi. Si scrive $[e_1, \dots, e_n]_{\mathcal{A}}$, e $[e_1, \dots, e_n]$ quando $\mathcal{A} = \emptyset$.
- *Totale* vuol dire che ogni indice ha un valore: **oltre la lunghezza** è `NULL` (il vettore vuoto, non un elemento mancante); **dentro i limiti**, il mancante è `NA`.
- Helper per le letture reali e letterali:

$$v^*(i) \stackrel{\text{def}}{=} \begin{cases} v(i) & \text{if } v(i) \neq \texttt{NULL} \\ \texttt{NA} & \text{otherwise} \end{cases}
\qquad \texttt{c()} \stackrel{\text{def}}{=} [\,] \qquad \texttt{c}(e_1, \dots, e_n) \stackrel{\text{def}}{=} e_1 \oplus \cdots \oplus e_n$$

- $v^*$ è ciò che rende "fuori dai limiti dà `NA`" una definizione invece di un caso speciale.

### Recycle (slide 25)
**Definizione.** $\mathrm{Recycle}(x, y) : \mathcal{V} \times \mathcal{V} \to \mathcal{V} \times \mathcal{V}$ in tre passi:
1. **cast** degli operandi al tipo comune;
2. **length**: $m = \max(|x|, |y|)$, decisa solo dalle lunghezze degli operandi;
3. **content**: $\rho_c$ ripete gli elementi fino a riempire $m$:

$$\rho_c(v, l)(i) \stackrel{\text{def}}{=} v\big(((i - 1) \bmod |v|) + 1\big) \quad \text{for } i \in [1, l], \quad v \neq [\,]$$

- Esempio: $\mathrm{Recycle}([0, 1], [3, 4, 5, 6]) = ([0, 1, 0, 1], [3, 4, 5, 6])$.
- **[aggiunta]** Il $-1$/$+1$ nella formula serve all'indicizzazione 1-based. Il caso $v = [\,]$ è escluso, ma in R esiste: se un operando ha lunghezza 0 il risultato ha lunghezza 0 (`1:3 + integer(0)` dà `integer(0)`), non $\max(|x|, |y|)$. Il modello copre solo operandi non vuoti.

### Select (slide 26)
$\mathrm{Select} : \mathcal{V} \times \mathcal{V}_{Int} \rightharpoonup \mathcal{V}$ è una funzione **parziale**: i tre modi sono disgiunti e R rifiuta un selettore che li mescola.
- **positivo**: tiene le posizioni elencate, nell'ordine dato, **duplicati inclusi**;
- **negativo**: toglie le posizioni elencate, tiene le altre in ordine crescente;
- **logico**: ricicla la maschera a $\max(|v|, |c|)$ e tiene dove è **True**.

**Definizione (positive selection).**

$$\mathrm{Select}(v, c) \stackrel{\text{def}}{=} \bigoplus_{i=1}^{|c|} \sigma_i \qquad
\sigma_i \stackrel{\text{def}}{=} \begin{cases} [v^*(c(i))] & \text{if } c(i) > 0 \\ [\,] & \text{if } c(i) = 0 \\ [\texttt{NA}] & \text{if } c(i) = \texttt{NA} \end{cases}$$

- Lo `0` contribuisce il vettore vuoto (sparisce), un indice oltre la fine dà `NA` grazie a $v^*$.

### Update (slide 27)
$\mathrm{Update}(v, c, v_e) : \mathcal{V} \times \mathcal{V}_{Int} \times \mathcal{V} \rightharpoonup \mathcal{V}$, anch'essa parziale.
- **positivo**: sovrascrive le posizioni elencate in $c$ con i valori di $v_e$; oltre $|v|$ il vettore cresce;
- **negativo**: sovrascrive tutte le posizioni tranne quelle escluse; la lunghezza non cambia;
- **logico**: ricicla la maschera a $\max(|v|, |c|)$ e sovrascrive dove è **True**.

**Definizione (positive update).**

$$\mathrm{Update}(v, c, v_e) \stackrel{\text{def}}{=} r\big(u_1 \mapsto v_e'(1), \dots, u_k \mapsto v_e'(k)\big) \qquad
r = v \oplus \underbrace{[\texttt{NA}, \dots, \texttt{NA}]}_{\max(C - |v|, 0)} \qquad v_e' = \rho_c(v_e, k)$$

con $C = \max\{c(i) \mid c(i) \neq \texttt{NA}\}$ e $u_1, \dots, u_k$ gli elementi non nulli di $c$.
- Prima si allunga $v$ con `NA` fino al massimo indice scritto, poi si ricicla $v_e$ sul numero di posizioni da scrivere e si scrive.
- **[aggiunta]** Verifica su `v <- c(10, 20, 30); v[5] <- 99`: $C = 5$, $r = [10, 20, 30, \texttt{NA}, \texttt{NA}]$, $k = 1$, risultato $[10, 20, 30, \texttt{NA}, 99]$, come nella slide 16.

### Il running example (slide 28)
"Four lines, five operators, one shape":

```r
x <- c(TRUE, 2L, 3.0)          # Cast, then ⊕: [1, 2, 3] double
y <- x + c(10, 20)             # Recycle, then +: [11, 22, 13]
z <- y[c(TRUE, FALSE, NA)]     # Select (logical): [11, NA]
z[c(2, 4)] <- c(50, 100)       # Update (positive): [11, 50, NA, 100]
```

- Deterministico ma non evidente: la parte 5 deve predire esattamente questo senza eseguirlo.
- **[aggiunta]** La seconda riga in R emette anche il warning di lunghezza non multipla (3 contro 2). Nella terza la maschera `NA` produce un `NA` nel risultato, mentre `FALSE` toglie la posizione 2.

## 5. Il dominio astratto (slide 29-39)

### Un prefisso fisso non basta (slide 29)

```r
x <- if (runif() >= 0.5) c(0, 0) else c(0, 0, 1, 100)   # length 2 or 4
```

- Idea ingenua: tracciare le prime due posizioni e riassumere il resto, $\nu = ([2, 4], \langle [0,0][0,0] \rangle, [1, 100], \mathbf{AttrEmpty})$.
- Le posizioni 3 e 4 leggono entrambe $[1, 100]$: si perde che `x[3]` vale 1 e `x[4]` vale 100 **ogni volta che esistono**.
- Soluzione: quando la lunghezza ha un **limite finito**, si traccia **ogni posizione**; il sommario serve solo per $u = +\infty$.

### Raw abstract element (slide 30)
**Definizione.** Un *raw abstract vector* in $\tilde{\mathcal{V}}^\sharp_{\mathcal{B}}$ è una quadrupla

$$\nu = \big([l, u], \langle p_1 \cdots p_k \rangle, s, a\big) \in \mathbf{Itv}_0 \times \mathcal{B}^{\sharp *} \times \mathcal{B}^\sharp \times \mathbf{Attr}^\sharp$$

con l'invariante

$$l \le k \le u \ \wedge\ \big(u \neq +\infty \Rightarrow (s = \bot_{\mathcal{B}^\sharp} \wedge u = k)\big)$$

- $[l, u]$: intervallo delle **lunghezze** possibili; $\langle p_1 \cdots p_k \rangle$: **contenuto noto**, un valore astratto per posizione; $s$: **sommario** delle posizioni oltre la $k$-esima; $a$: attributi astratti.
- Il dominio è **parametrico** nel dominio dei valori $\mathcal{B}^\sharp$; negli esempi $\mathcal{B}^\sharp = \mathbf{Itv}$ (intervalli, il dominio numerico dei deck precedenti).
- **[aggiunta]** Lettura dell'invariante: le posizioni esplicite sono almeno quelle garantite ($l \le k$); se la lunghezza è limitata, ogni posizione possibile è esplicita ($k = u$) e il sommario è vuoto. $\mathbf{Itv}_0$ sono gli intervalli su $\mathbb{N} \cup \{+\infty\}$.
- Esempi con $\gamma_{\mathcal{V}^\sharp_{\mathbf{Itv}}}$:
  - $([1, 2], \langle [1,1][0,0] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \mapsto \{[1], [1, 0]\}$
  - $([1, +\infty], \langle [42,42] \rangle, [42, 42], \mathbf{AttrEmpty}) \mapsto \{[42], [42, 42], [42, 42, 42], \dots\}$
  - $([1, +\infty], \langle [42,42][42,42] \rangle, [42, 42], \mathbf{AttrEmpty}) \mapsto$ lo stesso insieme.

### Una classe, molte tuple (slide 31)
Le ultime due tuple sono lo stesso elemento.

**Definizione (equivalenza e rappresentante minimo).**
- $\nu_1 \equiv \nu_2$ se coincidono su lunghezza $L$, $s$, $a$ e sul contenuto noto fino alla sequenza più corta, e le posizioni in più della più lunga sono uguali a $s$.
- $\nu^\downarrow$ toglie dal contenuto noto le posizioni finali uguali a $s$, tenendone almeno $l$.

### Il dominio astratto (slide 32)
**Definizione.** Il dominio è il reticolo

$$\mathcal{D}_{\mathcal{V}^\sharp_{\mathcal{B}}} = \big\langle \mathcal{V}^\sharp_{\mathcal{B}}, \sqsubseteq, \sqcup, \sqcap, \bot_{\mathcal{V}^\sharp_{\mathcal{B}}}, \top_{\mathcal{V}^\sharp_{\mathcal{B}}} \big\rangle$$

dove $\mathcal{V}^\sharp_{\mathcal{B}} = \{[\nu]_\equiv \mid \nu \in \tilde{\mathcal{V}}^\sharp_{\mathcal{B}}\} \cup \{\bot_{\mathcal{V}^\sharp_{\mathcal{B}}}, \top_{\mathcal{V}^\sharp_{\mathcal{B}}}\}$ e
- $\bot_{\mathcal{V}^\sharp_{\mathcal{B}}} = (\bot_{\mathbf{Itv}_0}, \varepsilon, \bot_{\mathcal{B}^\sharp}, \bot_{\mathbf{Attr}^\sharp})$;
- $\top_{\mathcal{V}^\sharp_{\mathcal{B}}} = (\top_{\mathbf{Itv}_0}, \varepsilon, \top_{\mathcal{B}^\sharp}, \top_{\mathbf{Attr}^\sharp})$.

Ogni elemento è una classe di tuple grezze, più i due elementi speciali. **[aggiunta]** Quozientare per $\equiv$ serve perché $\sqsubseteq$ sia un ordine parziale (antisimmetria) e non solo un preordine, come richiesto per i reticoli del deck 02.

### Order, join, meet (slide 33-35)
- **Order**: $\sqsubseteq$ è contenimento, ogni vettore rappresentato a sinistra è rappresentato a destra.

$$([2,2], \langle [1,1][2,2] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \sqsubseteq ([1,3], \langle [1,1][2,2][3,3] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$$

  e non il contrario: il secondo rappresenta anche $[1]$ e $[1, 2, 3]$.
- **Join**: il più piccolo elemento che contiene entrambi.

$$([2,2], \langle [0,0][0,0] \rangle, \bot, \emptyset) \sqcup ([4,4], \langle [0,0][0,0][1,1][100,100] \rangle, \bot, \emptyset) = ([2,4], \langle [0,0][0,0][1,1][100,100] \rangle, \bot, \emptyset)$$

  (qui $\bot = \bot_{\mathbf{Itv}}$ e $\emptyset = \mathbf{AttrEmpty}$). Le posizioni 3 e 4 restano separate: è proprio l'elemento che il prefisso fisso della slide 29 non sapeva scrivere.
- **Meet**: il più grande elemento contenuto in entrambi.

$$([2,2], \langle [1,1][1,2] \rangle, \bot, \emptyset) \sqcap ([1,+\infty], \langle [1,1][2,2][3,3] \rangle, [-1,-1], \emptyset) = ([2,2], \langle [1,1][2,2] \rangle, \bot, \emptyset)$$

  La posizione 2 tiene solo i valori comuni; la posizione 3 è impossibile perché il primo elemento ha lunghezza 2. Se una posizione non ha valori comuni il meet è $\bot_{\mathcal{V}^\sharp_{\mathcal{B}}}$, ad esempio $([3,3], \langle [1,1][9,9][3,3] \rangle, \dots) \sqcap ([3,3], \langle [1,1][2,2][3,3] \rangle, \dots) = \bot$.

### Widening (slide 36)
`x <- c(x, i)` in un ciclo aggiunge un elemento per iterazione: nessun limite finito, quindi la Kleene iteration non si stabilizza (requisito *Termination* del design brief).

**Definizione (widening).**
- **length**: $[l', u'] = L_1 \mathbin{\nabla_{\mathbf{Itv}_0}} L_2$;
- **content**: $p_1(i) \mathbin{\nabla_{\mathcal{B}^\sharp}} p_2(i)$ fino a $\max(k_1, k_2)$; solo il **prefisso comune** se $u' = +\infty \wedge (u_1 = +\infty \vee u_2 = +\infty)$;
- **summary**: $\bot_{\mathcal{B}^\sharp}$ se $u' \neq +\infty$; altrimenti il widening di $s_1$ con il join di $s_2$ e di ogni posizione tolta dal contenuto noto.

Iterate dell'esempio:

$$\begin{aligned}
x_0 &= ([0, 0], \varepsilon, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \\
x_1 &= x_0 \mathbin{\nabla_{\mathcal{V}^\sharp_{\mathbf{Itv}}}} \nu_1 = ([0, +\infty], \langle [1,1] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \\
x_2 &= x_1 \mathbin{\nabla_{\mathcal{V}^\sharp_{\mathbf{Itv}}}} \nu_2 = ([0, +\infty], \langle [1,1] \rangle, [2, 2], \mathbf{AttrEmpty}) \\
x_3 &= x_2 \mathbin{\nabla_{\mathcal{V}^\sharp_{\mathbf{Itv}}}} \nu_3 = ([0, +\infty], \langle [1,1] \rangle, [2, +\infty], \mathbf{AttrEmpty}) = x_4
\end{aligned}$$

- La lunghezza salta subito a $+\infty$ (widening degli intervalli); il sommario passa da $[2,2]$ a $[2, +\infty]$ e poi è stabile.
- **[aggiunta]** Gli stati $\nu_i$ che arrivano dal corpo del ciclo non sono scritti nella slide. Notare che in $x_1$ si ha $u = +\infty$ ma $s = \bot$: per $\gamma$ le posizioni oltre la prima sono impossibili, quindi $x_1$ rappresenta solo $[\,]$ e $[1]$; la lunghezza illimitata diventa effettiva solo quando il sommario si popola in $x_2$. È il widening del deck sui domini numerici, applicato componente per componente.

### Concretizzazione (slide 37)
**Definizione.** $\gamma_{\mathcal{V}^\sharp_{\mathcal{B}}} : \mathcal{V}^\sharp_{\mathcal{B}} \to \mathcal{P}(\mathcal{V})$:

$$\gamma_{\mathcal{V}^\sharp_{\mathcal{B}}}\big(([l, u], \boldsymbol{p}, s, a)\big) \stackrel{\text{def}}{=} \left\{ [c_1, \dots, c_n]_{\mathcal{A}} \in \mathcal{V} \;\middle|\; \begin{array}{l} n \in \gamma_{\mathbf{Itv}_0}([l, u]),\ \mathcal{A} \in \gamma_{\mathbf{Attr}^\sharp}(a), \\ \forall i \in [1, \min(n, |\boldsymbol{p}|)] : c_i \in \gamma_{\mathcal{B}^\sharp}(p_i), \\ \forall j \in [|\boldsymbol{p}| + 1, n] : c_j \in \gamma_{\mathcal{B}^\sharp}(s) \end{array} \right\}$$

- L'analisi è **concretization-based**: si appoggia solo su $\gamma$, perché a livello di vettore non esiste una migliore astrazione.

### Perché non esiste una connessione di Galois (slide 38-39)
- Una GC darebbe a ogni elemento concreto una **migliore astrazione**, il minimo $d$ con $c \subseteq \gamma(d)$:

$$\alpha_{\mathcal{V}^\sharp_{\mathcal{B}}}(c) = \sqcap \{ d \mid c \subseteq \gamma_{\mathcal{V}^\sharp_{\mathcal{B}}}(d) \}$$

- I due versi di $\alpha(c) \sqsubseteq d \iff c \subseteq \gamma(d)$ (la definizione di GC del deck 06):
  - **Soundness**, $\alpha(c) \sqsubseteq d \Rightarrow c \subseteq \gamma(d)$: con $d = \alpha(c)$ dà $c \subseteq \gamma(\alpha(c))$, quindi $\alpha(c)$ è un upper bound di $c$;
  - **Best abstraction**, $c \subseteq \gamma(d) \Rightarrow \alpha(c) \sqsubseteq d$: ogni upper bound sta sopra $\alpha(c)$, quindi il minimo esiste ed è $\alpha(c)$.
- **Controesempio.** $\mathcal{C} = \{[1], [1, 2], [1, 2, 3], \dots\}$ e, per ogni $i \ge 1$,

$$\nu_i = \big([1, +\infty], \langle [1,1] \cdots [i,i] \rangle, [i + 1, +\infty], \mathbf{AttrEmpty}\big)$$

  - $\mathcal{C} \subseteq \gamma(\nu_i)$ per ogni $i$: le prime $i$ posizioni sono esatte, la coda sta in $[i + 1, +\infty]$;
  - $\nu_{i+1} \sqsubseteq \nu_i$: una posizione esatta in più e un sommario più stretto;
  - ogni upper bound con $k$ posizioni esatte è raffinato da $\nu_{k+1}$: **non c'è minimo**;
  - il meet richiederebbe $\langle [1,1][2,2] \dots \rangle$, che nessuna tupla finita contiene: **niente GC**.
- È un **reticolo non completo**: la catena $\nu_i$ non ha infimo, quindi $\alpha(\mathcal{C})$ non esiste. Un lower bound fissa solo un numero finito di posizioni, e l'infimo dovrebbe rappresentare esattamente $\mathcal{C}$.
- **[aggiunta]** I lower bound della catena sono del tipo $([1, n], \langle [1,1] \cdots [n,n] \rangle, \bot, \dots)$, cioè $\{[1], \dots, [1, \dots, n]\}$: crescono con $n$ senza un massimo. È la stessa situazione dei poliedri convessi (un cerchio non ha una migliore approssimazione poliedrica), dove si usa il framework con sola $\gamma$ di Cousot e Cousot (1992). La soundness del punto fisso resta garantita dal teorema tarskiano del deck 07, che usa solo $\gamma$: ogni post-fixpoint astratto, e il widening garantisce di raggiungerne uno, concretizza in un post-fixpoint concreto.

## 6. Operatori astratti (slide 40-49)

### The operator map (slide 40)
Ogni operatore astratto appartiene a una di tre famiglie:
- **Data movement**: concatenazione e recycling mettono insieme o ripetono vettori;
- **Access**: la selezione legge posizioni, l'update le scrive;
- **Metadata**: la coercizione cambia il tipo, gli attributi annotano il vettore.

Tre problemi generano tutte le difficoltà: lo **zero** come indice viene scartato in silenzio; i valori degli indici sono noti **solo a run time**; un indice **negativo** dice cosa *non* c'è.

### Coercion and attributes (slide 41)
- Il tipo è una componente **finita**, la catena **Bool ≺ Int ≺ Float**, e il dominio tipato è $\mathcal{T} \times \mathcal{V}^\sharp_{\mathcal{B}}$:

$$\tau(\texttt{c(TRUE, 3L, 2.5)}) = (\{\mathbf{Bool}\} \sqcup \{\mathbf{Int}\}) \sqcup \{\mathbf{Float}\} = \{\mathbf{Int}\} \sqcup \{\mathbf{Float}\} = \{\mathbf{Float}\}$$

  Tre argomenti, due join: il tipo astratto è **Float**.
- **[aggiunta]** In μR non c'è `character` (gli atomi sono solo Float, Int, Bool, NULL), quindi la catena si ferma a Float.
- Gli attributi sono una coppia **(MustHave, MayHave)**: $\mathtt{setAttr}^\sharp$ la fissa a $(A, A)$, $\mathtt{getAttr}^\sharp$ la proietta.
- Esempio: `m <- matrix(1:2, nrow = 1)` dà `dim` e `class`:

$$\nu = \big([2, 2], \langle [1,1][2,2] \rangle, \bot_{\mathbf{Itv}}, (\{\mathtt{dim}, \mathtt{class}\}, \{\mathtt{dim}, \mathtt{class}\})\big)$$

- (Imprecisione nella slide: in R `matrix(1:2, nrow = 1)` ha **solo** l'attributo `dim`; `class(m)` restituisce `"matrix" "array"` ma è una classe implicita, non un attributo, e `attributes(m)` mostra solo `$dim`. L'esempio corretto avrebbe $(\{\mathtt{dim}\}, \{\mathtt{dim}\})$.)

### Concatenation (slide 42)
La concatenazione **combina le lunghezze** e concatena i contenuti noti.
- $\nu_1 = ([1, 2], \langle [0,0][1,1] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$, $\nu_2 = ([1, 1], \langle [42,42] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$.
- $\gamma(\nu_1) = \{[0], [0, 1]\}$, $\gamma(\nu_2) = \{[42]\}$; le concatenazioni possibili sono $\{[0, 42], [0, 1, 42]\}$.

$$\nu_1 \oplus^\sharp \nu_2 = ([2, 3], \langle [0,0][1,42][42,42] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$$

- La posizione 2 è il join fra il secondo elemento di $\nu_1$ (se esiste) e il 42 di $\nu_2$ (se $\nu_1$ è lungo 1). **[aggiunta]** La lunghezza è la somma degli intervalli, $[1,2] + [1,1] = [2,3]$.

### Recycling astratto: due incertezze (slide 43-44)
Con $\nu_i = ([l_i, u_i], \langle p_{i1} \cdots p_{i|\boldsymbol{p}_i|} \rangle, s_i, a_i)$:

$$\mathrm{Recycle}^\sharp : \mathcal{V}^\sharp_{\mathcal{B}} \times \mathcal{V}^\sharp_{\mathcal{B}} \to \mathcal{V}^\sharp_{\mathcal{B}} \times \mathcal{V}^\sharp_{\mathcal{B}}$$

- Lunghezza riciclata: $[l', u'] = [\max(l_1, l_2), \max(u_1, u_2)]$.

$$\nu_i' = \left( [l', u'],\ \bigsqcup_{d = l'}^{\max(|\boldsymbol{p}_1|, |\boldsymbol{p}_2|)}{}_{\mathcal{B}^{\sharp *}}\ \rho_f^\sharp(\boldsymbol{p}_i, s_i, l_i, d),\ s_i',\ a_i \right)$$

- Prima incertezza: la **lunghezza obiettivo** $d$ sta in $\gamma_{\mathbf{Itv}}([l', \max(|\boldsymbol{p}_1|, |\boldsymbol{p}_2|)])$ → join su $\rho_f^\sharp$.
- Seconda incertezza: a $d$ fissato, la **lunghezza originale** varia in $[l_i, u_i]$, quindi cambia $i \bmod k$ → join su $\rho_c^\sharp$.
- Esempio (slide 44): riciclare $\boldsymbol{p} = \langle [1,1][2,2] \rangle$ a lunghezza 3, con lunghezza originale 1 o 2:

$$\begin{aligned}
\rho_f^\sharp(\boldsymbol{p}, \bot_{\mathbf{Itv}}, 1, 3) &= \rho_c^\sharp(\boldsymbol{p}, 1, 3) \sqcup_{\mathbf{Itv}^*} \rho_c^\sharp(\boldsymbol{p}, 2, 3) \\
&= \langle [1,1][1,1][1,1] \rangle \sqcup_{\mathbf{Itv}^*} \langle [1,1][2,2][1,1] \rangle = \langle [1,1][1,2][1,1] \rangle
\end{aligned}$$

- **[aggiunta]** Come nel caso concreto, la formula della lunghezza vale per operandi non vuoti: se uno dei due può avere lunghezza 0, in R il risultato può essere vuoto, caso che $[\max(l_1, l_2), \max(u_1, u_2)]$ non copre.

### Selection astratta (slide 45-47)
$\mathrm{Select}^\sharp : \mathcal{V}^\sharp_{\mathcal{B}} \times \mathcal{V}^\sharp_{\mathbf{Itv}} \to \mathcal{V}^\sharp_{\mathcal{B}}$. R vieta indici misti, quindi il segno del selettore sceglie il ramo:
- **Positive** $\mathrm{Select}^\sharp_{pos}$: indici $\ge 0$ o NA, estrae per posizione;
- **Negative** $\mathrm{Select}^\sharp_{neg}$: indici $< 0$, esclude per posizione;
- **Logical** $\mathrm{Select}^\sharp_{log}$: maschera in $\{\texttt{NA}, \texttt{True}, \texttt{False}\}^+$, seleziona dove è vera.

Il selettore viene **filtrato per segno** (*abstract filtering*, la stessa mossa del filtro di una guardia con la condizione del ramo, come $[\![b]\!]^\sharp$ nel deck 07):

$$\boldsymbol{p}_2^+ = \langle p \in \boldsymbol{p}_2 \mid \gamma_{\mathbf{Itv}}(p) \subseteq \mathbb{Z}_{\ge 0} \cup \{\texttt{NA}\} \rangle \qquad
\boldsymbol{p}_2^- = \langle p \in \boldsymbol{p}_2 \mid \gamma_{\mathbf{Itv}}(p) \subseteq \mathbb{Z}_{< 0} \rangle$$

$$\mathrm{Select}^\sharp(\nu_1, \nu_2) = \mathrm{Select}^\sharp_{pos}(\nu_1, \nu_2^+) \sqcup \mathrm{Select}^\sharp_{neg}(\nu_1, \nu_2^-)$$

- (Precisazione: presa alla lettera, la notazione insiemistica scarta una posizione il cui intervallo attraversa lo 0, ad esempio $[-1, 2]$, da entrambi i rami. Il senso del filtro di una guardia è il **meet** con il segno, $p \sqcap \alpha(\mathbb{Z}_{\ge 0})$ e $p \sqcap \alpha(\mathbb{Z}_{<0})$, che non perde esecuzioni.)

**Caso positivo (slide 46).** *AdjustForZeros* gestisce lo zero: toglie gli zeri certi e unisce gli indici che possono finire nella stessa posizione. Una posizione troppo larga da enumerare fa collassare la sorgente a $\mathrm{Squash}(v)$.

$$\begin{aligned}
v &= ([2, 3], \langle [10,10][20,20][30,30] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \\
s &= ([2, 3], \langle [1,2][0,1][1,100] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \\
\mathrm{AdjustForZeros}(s) &= ([1, 3], \langle [1,2][0,100][1,100] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}) \\
\mathrm{Select}^\sharp_{pos}(v, s) &= \big([1, 3], \langle [10,20],\ [10,30] \sqcup \alpha_{\mathbf{Itv}}(\texttt{NA}),\ [10,30] \sqcup \alpha_{\mathbf{Itv}}(\texttt{NA}) \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty}\big)
\end{aligned}$$

- La posizione 1 unisce gli indici 1 e 2: $[10, 20]$. Le posizioni 2 e 3 sono troppo larghe da enumerare: ciascuna è $\mathrm{Squash}(v) \sqcup \alpha_{\mathbf{Itv}}(\texttt{NA})$ (gli indici fino a 100 possono uscire dai limiti).
- **[aggiunta]** La posizione 2 di AdjustForZeros è $[0,1] \sqcup [1,100] = [0, 100]$: se il secondo indice è 0 sparisce e al suo posto scivola il terzo. Lo 0 rimasto nell'intervallo è una sovra-approssimazione sound. La lunghezza scende a $[1, 3]$ perché al più uno zero può sparire.

**Caso negativo (slide 47).** Quando un insieme di posizioni possibilmente cancellate copre un intervallo, i sopravvissuti non si possono elencare uno a uno e collassano a $\mathrm{SquashExcept}(v, \mathrm{MustDeleted})$.
- $v = ([4,4], \langle [10,10][20,20][30,30][40,40] \rangle, \dots)$, $s = ([2,2], \langle [-1,-1][-3,-3] \rangle, \dots)$
- MustDeleted $= \{1, 3\}$, MayDeleted $= \{1, 3\}$, MustNotDeleted $= \{2, 4\}$
- $\mathrm{Select}^\sharp_{neg}(v, s) = ([2,2], \langle [20,20][40,40] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$, come `v[c(-1, -3)]` della slide 15.

**Caso logico (slide 47 bis).**
- $v$ come sopra, $s = ([4,4], \langle \texttt{True}, \texttt{False}, \texttt{NA}, \texttt{True} \rangle, \dots)$
- $\mathrm{Select}^\sharp_{log}(v, s) = ([3,3], \langle [10,10], \alpha_{\mathbf{Itv}}(\texttt{NA}), [40,40] \rangle, \bot_{\mathbf{Itv}}, \mathbf{AttrEmpty})$
- La maschera è riciclata con $\rho_f^\sharp$: True seleziona, False salta, NA dà $\alpha_{\mathbf{Itv}}(\texttt{NA})$; la lunghezza sottrae i False certi.
- Negativo e logico sono entrambi **l'operatore positivo più un insieme di posizioni**: il complemento delle cancellate, o le posizioni dove la maschera è vera.

### Update astratto (slide 48-49)
**Caso positivo e suo costo (slide 48).** L'update è una selezione più una scrittura: stesso filtro, stesso AdjustForZeros.
- selettore **non enumerabile**: collasso a $\mathrm{Squash}(\nu) \sqcup \mathrm{Squash}(v_e)$, lunghezza illimitata;
- **infinito ma enumerabile**: **weak update**, una posizione può essere scritta due volte;
- **finito**: si estende con NA fino al massimo indice, poi si scrive.
- Esempio (le tuple sono abbreviate, senza sommario e attributi): $\nu = ([5,5], \langle [1,1] \cdots [5,5] \rangle)$, $s = ([1,1], \langle [10,10] \rangle)$, $v_e = ([1,1], \langle [42,42] \rangle)$:

$$\mathrm{Update}^\sharp_{pos}(\nu, s, v_e) = \big([10, 10], \langle [1,1] \cdots [5,5]\ \alpha_{\mathbf{Itv}}(\texttt{NA}) \cdots \alpha_{\mathbf{Itv}}(\texttt{NA})\ [42,42] \rangle\big)$$

  Dieci posizioni, quattro NA. Un update all'indice $i$ **materializza $i$ posizioni**, e il widening chiude la coda.
- **[aggiunta]** Strong e weak update come nell'analisi dei puntatori: se la posizione scritta è certa si sostituisce il valore, se è solo possibile si fa il join con il vecchio.

**Caso negativo (slide 49).** Tre insiemi: non aggiornate di sicuro, forse non aggiornate, aggiornate di sicuro. Le ultime si scrivono **strong**; la lunghezza non cambia (`v[-2] <- 5` scrive, non cancella).
- $v = ([4,4], \langle [10,10][20,20][30,30][40,40] \rangle)$, $s = ([1,1], \langle [-2,-2] \rangle)$, $\nu_e = ([1,1], \langle [99,99] \rangle)$
- La slide dà $\mathrm{Update}^\sharp_{neg}(v, s, \nu_e) = ([4,4], \langle [10,10][99,99][30,30][40,40] \rangle)$.
- (Errore nella slide: il risultato scrive la posizione 2, cioè proprio quella esclusa. `v[-2] <- 99` scrive tutte le posizioni **tranne** la 2, come dice la slide stessa e come mostra `v[-2] <- 5` della slide 16. Il risultato corretto è $([4,4], \langle [99,99][20,20][99,99][99,99] \rangle)$, con aggiornate di sicuro $\{1, 3, 4\}$ e non aggiornate di sicuro $\{2\}$.)

**Caso logico (slide 49 bis).** Maschera e valori vengono riciclati: True scrive strong, forse-True weak, False lascia.
- $s = ([4,4], \langle [1,1], [0,0], [1,1], [0,0] \rangle)$, con $[1,1] = \alpha_{\mathbf{Itv}}(\texttt{True})$ e $[0,0] = \alpha_{\mathbf{Itv}}(\texttt{False})$
- $\mathrm{Update}^\sharp_{log}(v, s, \langle [99,99] \rangle) = ([4,4], \langle [99,99][20,20][99,99][40,40] \rangle)$
- L'unico rifiuto: se la maschera può contenere NA e il valore sostitutivo può essere lungo più di 1 ($u_3 \neq 1$), il programma concreto è un errore e l'astratto restituisce $\bot_{\mathcal{V}^\sharp_{\mathcal{B}}}$.
- (Precisazione: in R `x[c(TRUE, NA)] <- c(1, 2)` dà l'errore "NAs are not allowed in subscripted assignments". Ma restituire $\bot$ quando l'errore è solo *possibile* scarterebbe le esecuzioni in cui la maschera non contiene NA o il valore ha lunghezza 1, e non sarebbe sound: a rigore $\bot$ va dato solo quando l'errore è certo, NA presente di sicuro e $l_3 > 1$.)
- Sintesi della slide: "Update is selection plus a write; the difficulty is knowing **where**."

## 7. Implementazione e validazione (slide 50-52)

### Pipeline and visitor (slide 50)
Il dominio è integrato in **flowR**: R Source → Normalized AST → CFG + DFG → **Abstract Analysis** (in arancione, il contributo del lavoro).
- **Worklist fixpoint**: join nei punti di merge, widening $\nabla_{\mathcal{V}^\sharp_{\mathcal{B}}}$ nei cicli (la Kleene iteration sul CFG del deck 07, con widening).
- Il **visitor** scompone lo stato in lunghezza, contenuto noto, sommario, attributi e tipo, poi manda ogni vertice del CFG all'operatore astratto corrispondente.
- Fuori da μR si ricade su $\top_{\mathcal{V}^\sharp_{\mathcal{B}}}$: sound su μR, conservativo altrove.

### Three tests (slide 51)

```r
# Recycling
if (*) v <- c(1, 2, 3) else v <- c(0, 1)
r <- v + c(9, 10, 11)
# r = ([3, 3], <[9, 10], [11, 12], [11, 14]>, ⊥Itv)

# Uncertainty
v <- *; s <- c(1, 2, 3)
x <- s[v]; y <- x[c(1, 2)]
# * = ⊤, y = ([2, 2], <[1, 3] ⊔ α(NA), [1, 3] ⊔ α(NA)>, ⊥Itv)

# Loop
x <- c(1, 2, 3); i <- 1
while (*) { x <- c(x, i); i <- i + 1 }; r <- x
# r = ([3, +∞], <[1, 1], [2, 2], [3, 3]>, [1, +∞] ⊔ α(NA))
```

- **[aggiunta]** Verifica del primo: con `v = [1, 2, 3]` si ottiene $[10, 12, 14]$; con `v = [0, 1]` riciclato a $[0, 1, 0]$ si ottiene $[9, 11, 11]$ (con warning); il join posizione per posizione dà esattamente $\langle [9,10], [11,12], [11,14] \rangle$. Nel terzo il ciclo aggiunge solo valori $i \ge 1$, mai NA: l'$\alpha(\texttt{NA})$ nel sommario è un'imprecisione sound, non un comportamento reale. `*` indica un valore sconosciuto ($\top$).

### What the numbers say (slide 52)
- **61 programmi** in **6 categorie**: 14 Creation, 9 Recycling, 12 Select, 12 Update, 8 Uncertainty, 6 Loops.
- **2 controlli**:
  - il valore astratto calcolato coincide con quello ricavato **a mano** dalle definizioni;
  - dove esiste un'esecuzione concreta, l'esecuzione R reale **sta nella concretizzazione**.
- **Costo**: un update all'indice $i$ materializza $i$ posizioni; il widening chiude la coda.
- **Limiti**: non relazionale; nessuna relazione fra le lunghezze di variabili diverse; nessuna analisi interprocedurale.

## 8. Conclusioni e problemi aperti (slide 53-54)

### Contributions and proof status (slide 53)
- **Costruito**:
  - **μR**: le feature dei vettori analizzate, rese esplicite;
  - un **dominio parametrico**: lunghezza, prefisso noto, sommario, attributi;
  - **operatori astratti**: recycling, selezione, update;
  - un **prototipo in flowR**: 61 programmi, **61/61**.
- **Dimostrato**: ordine parziale e meet; terminazione del widening; recycling e selezione positiva.
- **Solo empirico**: selezione negativa e logica; tutti gli update; attributi.

### Open problems (slide 54)
"Where is each gap: domain, semantics, or engineering?"

| Problema | Natura |
|---|---|
| Relazioni di lunghezza fra variabili: reduced product | dominio |
| Branch sensitivity: stati disgiuntivi nei punti di merge | dominio |
| Analisi interprocedurale con lazy evaluation | semantica |
| Dispatch S3/S4 modellato, non sovra-approssimato | semantica |
| Le dimostrazioni di soundness mancanti | ingegneria |
| Precisione e costo su pacchetti CRAN reali | ingegneria |

- **[aggiunta]** La branch sensitivity si vede nella slide 12: dopo l'`if` il join dà $r = ([3, 4], \langle [0,42][0,42][0,42][42,42] \rangle, \bot, \emptyset)$, perdendo il legame "lunghezza 3 ⇒ tutti 0, lunghezza 4 ⇒ tutti 42" che uno stato disgiuntivo terrebbe.

## Da ricordare
- **Problema**: in R tutto è un vettore, NA (valore mancante, occupa una posizione) è diverso da NULL (vettore vuoto), i tipi si promuovono in silenzio al lub, le operazioni riciclano il più corto, l'indice ha tre modi (positivo con 0 saltato e NA fuori dai limiti, negativo, logico) e l'update può allungare il vettore. Lunghezza e contenuto per posizione dipendono dal ramo eseguito.
- **Obiettivo**: approssimare la collecting semantics, flow-sensitive e non relazionale, con il contratto $\forall \ell .\ [\![P]\!](\ell) \subseteq \gamma([\![P]\!]^\sharp(\ell))$ e, per gli operatori, $c \in \gamma(\nu) \Rightarrow \mathrm{op}(c) \in \gamma(\mathrm{op}^\sharp(\nu))$.
- **μR**: nucleo con NULL = vettore vuoto, environment = mappa piatta; quattro operatori concreti $\oplus$, Recycle, Select, Update, definiti con il vettore come mappa totale e l'helper $v^*$.
- **Elemento astratto**: $([l, u], \langle p_1 \cdots p_k \rangle, s, a)$ con invariante $l \le k \le u \wedge (u \neq +\infty \Rightarrow s = \bot \wedge u = k)$: se la lunghezza è limitata ogni posizione è esplicita, il sommario serve solo per lunghezze illimitate. Dominio parametrico nei valori $\mathcal{B}^\sharp$ (es. Itv), quoziente per $\equiv$.
- Reticolo con $\sqsubseteq$ = contenimento, join e meet posizione per posizione, widening su lunghezza, prefisso comune e sommario.
- **Nessuna connessione di Galois**: la catena $\nu_i$ con sempre più posizioni esatte non ha infimo, il reticolo non è completo e $\alpha$ non esiste; l'analisi è **concretization-based** (solo $\gamma$).
- Operatori astratti: tipo come join nella catena Bool ≺ Int ≺ Float, attributi (MustHave, MayHave), recycling con due join (lunghezza obiettivo e lunghezza originale), selezione divisa per segno con AdjustForZeros, Squash e SquashExcept, update strong o weak.
- **Risultati**: prototipo in flowR, 61 programmi in 6 categorie, 61/61 su entrambi i controlli; dimostrati ordine, meet, widening, recycling e selezione positiva, il resto solo empirico.
- **Limiti**: non relazionale, niente relazioni fra lunghezze, niente interprocedurale, niente disgiunzione ai merge, S3/S4 non modellati, costo proporzionale all'indice scritto.
