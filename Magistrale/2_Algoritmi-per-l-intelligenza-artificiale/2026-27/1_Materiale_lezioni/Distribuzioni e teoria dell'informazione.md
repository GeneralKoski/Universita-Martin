# Distribuzioni e teoria dell'informazione

Fonte: `Distribuzioni e teoria dell'informazione.pdf`

Lezioni del 25/09, 28/09 e 02/10/2026. Il pacco di slide è in 69 pagine.

## DNA come informazione (slide 2-7)
- Il genoma di una cellula è memorizzato nel **DNA** (o RNA). Visto come sequenza di caratteri (ignorando la struttura 3D), contiene elementi strutturali a livello di informazione:
  - **regioni trascrizionali** (i geni)
  - **regioni di regolazione** (promotori, inibitori, co-fattori)
  - **hotspot di ricombinazione**
  - regioni dedicate alla **topologia strutturale**
  - regioni legate a fattori evolutivi senza caratterizzazione funzionale diretta (le meno studiate)
- Il DNA è un nastro scritto nell'alfabeto nucleotidico di 4 simboli $\{A, C, G, T\}$. Le stringhe di lunghezza $n$ sono $4^n$: per $n = 100$ sono $4^{100} > 10^{60}$. I genomi reali vanno da migliaia a miliardi di caratteri, quindi lo spazio esplorabile dall'evoluzione è di fatto infinito.
- **Paradosso evolutivo:** si suppone che i primi proto-genomi fossero RNA, con il DNA adottato dopo. La macromolecola non è solo memoria ma parte attiva: la cellula è un **sistema di calcolo** il cui attore principale è il DNA. Il DNA codifica gli altri elementi della cellula ma ha bisogno che siano già presenti (e compatibili) per esprimersi: è nato prima il genoma o la cellula?
- Il DNA **trasmette l'informazione alla progenie** e riassume la storia evolutiva della specie. Il genoma è soggetto a due forze:
  - **strette regole organizzative** per rappresentare l'informazione delle funzioni primarie
  - **adattabilità**, che si manifesta come processo di mutazione (spesso) randomico
- **Darwin:** tre fattori dell'evoluzione, **ereditarietà**, **variabilità**, **selezione naturale**. La variabilità (esplorazione) avviene soprattutto nella procreazione (ricombinazione) ma anche per alterazioni casuali ed errori di copia. Flusso **bidirezionale** dell'informazione tra specie e individuo.

## Basi della teoria dell'informazione (slide 8-10)
- **Cifrario di Cesare:** cifrario a sostituzione (a scorrimento). Nella slide è datato "settimo secolo A.C.", probabile refuso.
- **Rottura di Al-Kindi:** in un testo abbastanza lungo di una data lingua ogni lettera ha una frequenza caratteristica, quindi si rompe il cifrario confrontando le frequenze dei caratteri. Considerato uno dei primi esempi di teoria dell'informazione.
- **Curva di Zipf:** si ordinano gli elementi di una distribuzione per frequenza (cioè si calcola il **rango**) e si rappresenta frequenza vs rango. Esempio in slide: parole della lingua araba, curva decrescente molto ripida nei primi ranghi.
- **Variabile** $X$ e suo **intervallo di variabilità** $\hat{X}$ = insieme dei valori che $X$ può assumere.
- **Distribuzione discreta** di $n$ occorrenze su $k$ oggetti: dice come le $n$ occorrenze si distribuiscono sui $k$ oggetti. È **di probabilità** se la somma dei valori assegnati è 1 (probabilità invece di molteplicità).

## Informazione ed entropia (slide 11-14)
- **Informazione** di $x \in \hat{X}$ con probabilità $p(x)$:
$$I(x) = \log_2\frac{1}{p(x)} = -\log_2 p(x)$$
- **Sorgente informativa:** coppia $(X, p)$, con $p$ funzione di probabilità su tutti i valori di $X$.
- **Probabilità vs frequenza:** la probabilità è un concetto **a priori** (il modello della sorgente), la frequenza è **a posteriori** (conteggio su ciò che si è osservato). Il disegno in slide: istogramma di probabilità su A, C, G, T accanto all'istogramma delle frequenze osservate in una sequenza generata.
- **Entropia** di una sorgente:
$$H(X, p) = -\sum_{x \in \hat{X}} p(x) \log_2 p(x)$$
  È l'**informazione media** della sorgente: media dell'informazione pesata con la probabilità di ogni valore.
- **Prop. 1 (equipartizione):** $H$ è massima quando $p$ è **uniforme**, $p(x) = \frac{1}{n}$ per ogni $x$, con $|\hat{X}| = n$.
- **Esempio: albero di decisione.** A deve indovinare un numero fra 1 e 4 pensato da B, distribuzione uniforme (albero binario con 4 foglie nel disegno):
$$-\sum_{i=1}^{4} \frac14 \log_2\frac14 = -\sum_{i=1}^{4}\left(\frac14\log_2 1 - \frac14\log_2 4\right) = \sum_{i=1}^{4} \frac14 \log_2 4 = \log_2 4 = 2$$
  Nella slide il primo termine è scritto $\log_2(x_i)$ invece di $\log_2 p(x_i)$: refuso.
- **Prop. 1.1:** con base del logaritmo $n$ (e $n$ valori equiprobabili) l'entropia massima vale 1:
$$H = -\sum_{i=1}^{n} \frac1n \log_n \frac1n = -\frac{n \log_n \frac1n}{n} = -(\log_n 1 - \log_n n) = \log_n n = 1$$
  In generale quindi $H_{max} = \log_b n$ in base $b$.

## Stringhe e genomi (slide 15-19)
- **Alfabeto** $\Gamma$; **stringa** $\alpha = a_1 a_2 \dots a_n$ con $a_i \in \Gamma$; **lunghezza** $|\alpha| = n$; **stringa vuota** $\lambda$.
- $\alpha[i]$ = carattere in posizione $i$ ($1 \le i \le |\alpha|$). $\alpha[i, j]$ = **sottostringa** da $i$ a $j$ inclusi, lunga $j - i + 1$.
- **Prefisso:** $\alpha[1, i]$. **Suffisso:** $\alpha[i, |\alpha|]$.
- **Fattori** di un genoma $G \in \Gamma^*$ (tutte le sottostringhe):
$$D(G) = \{G[i, j] : 1 \le i \le j \le |G|\}$$
- **Posizioni** di $\alpha \in D(G)$: $pos_G(\alpha) = \{i : G[i, j] = \alpha\}$. **Molteplicità:** $mult_G(\alpha) = |pos_G(\alpha)|$.
- Classificazione delle parole:
  - **hapax:** $mult_G(\alpha) = 1$
  - **repeat:** $mult_G(\alpha) > 1$
  - **repeat massimale:** $\forall x \in \Gamma,\ mult_G(\alpha x) = 1$ (come scritto in slide: ogni estensione a destra non è più un repeat)
  - **hapax minimale:** $\alpha = a_1 \dots a_n$ hapax con $mult_G(a_1 \dots a_{n-1}) > 1$ (togliendo l'ultimo carattere torna un repeat)
  - **nullomero:** $mult_G(\alpha) = 0$, cioè $\alpha \notin D(G)$
- **Elongazione** di $\alpha$: $\alpha x$ con $x \in \Gamma$. Elongazione **in $G$**: $\alpha x \in D(G)$.
- **Memer:** parola $\alpha$ tale che $\forall x \in \Gamma,\ \alpha x \in D(G)$ (tutte le elongazioni compaiono in $G$).
- **k-mer:** fattori di lunghezza $k$, $D_k(G) = \{\alpha \in D(G) : |\alpha| = k\}$. Fondamentali in bioinformatica, es. ricostruibilità e analisi dei genomi tramite **NGS**.

Esempio di verifica (non nelle slide): $G = ACGTACGA$, $k = 2$. I 2-mer in posizione sono $AC, CG, GT, TA, AC, CG, GA$ ($|G| - k + 1 = 7$). $mult(AC) = mult(CG) = 2$ (repeat), $GT, TA, GA$ hapax, $|D_2(G)| = 5$, quindi $16 - 5 = 11$ nullomeri di lunghezza 2.

## Distribuzioni (slide 20-22)
- **Distribuzione** $\phi : A \mapsto B$: funzione che dice come gli elementi del dominio $A$ si distribuiscono sugli elementi del codominio $B$.
- **Discreta:** dominio discreto.
- **Di molteplicità:** codominio $\mathbb{N}$, rappresenta una quantità. Da una distribuzione originaria $\phi' : A' \to B$ (matite $\to$ colori), la distribuzione di molteplicità $\phi''$ mappa $B$ in $A'' \subseteq \mathbb{N}$ con $\sum_{x \in B} \phi''(x) = |A'|$. Esempio in slide: 3 matite blu e 2 verdi, $Blu \mapsto 3$, $Verde \mapsto 2$.
- **Di frequenza:** codominio $\mathbb{R}$ e $\sum_{x \in A} \phi(x) = 1$ (in slide scritto $\phi(A)$, refuso). Da una $\phi_M$ di molteplicità si normalizza:
$$\phi_F(x) = \frac{\phi_M(x)}{\sum_{y \in A} \phi_M(y)}$$
- **Di probabilità:** distribuzione di frequenza i cui valori rappresentano probabilità.

## Distribuzioni genomiche (slide 23-31)
Una distribuzione è un **punto di vista** su un fenomeno: cattura una sola proprietà quantitativa. Si raggruppano per tipo di **dominio**.

**Dominio = k-mer**
- **Molteplicità di parola:** $\alpha \in \Gamma^k \mapsto mult_G(\alpha)$, oppure su $D_k(G)$ o su $D(G)$.
- **Frequenza di parola:**
$$\alpha \in D_k(G) \mapsto \frac{mult_G(\alpha)}{|G| - k + 1}$$
  ($|G| - k + 1$ = numero di posizioni in cui inizia un k-mer).
- Grafici: molteplicità dei 16 dinucleotidi del cromosoma umano 22 (tutti fra circa 1,6 e 2,7 milioni tranne **CG**, nettamente il più basso, circa 0,6 milioni) con heatmap; heatmap per tutti i cromosomi umani e confronto Homo sapiens vs Escherichia coli per $k = 1 \dots 6$ (numeri nelle figure poco leggibili).

**Dominio = rango**
- **Curva di Zipf:** $i = rank(\alpha) : \alpha \in D_k(G) \mapsto mult_G(\alpha)$, ranghi ottenuti ordinando i k-mer per molteplicità decrescente.

**Dominio = molteplicità**
- **Co-molteplicità:** per ogni valore $m_i$, quante parole hanno quella molteplicità. Con $M(G) = \{m_i : \exists \alpha \in D(G),\ mult_G(\alpha) = m_i\}$:
$$m_i \in M(G) \mapsto |\{\alpha \in D(G) : mult_G(\alpha) = m_i\}|$$
  Analogo ristretto ai k-mer con $M_k(G)$ e $D_k(G)$.

**Dominio = lunghezza di parola**
- **Lunghezza di parola:** $k \mapsto |D_k(G)|$
- **Hapax:** $k \mapsto |H_k(G)|$, $H_k(G) = \{\alpha \in D_k(G) : mult_G(\alpha) = 1\}$
- **Repeat:** $k \mapsto |R_k(G)|$, $R_k(G) = \{\alpha \in D_k(G) : mult_G(\alpha) > 1\}$
- Grafici su cromosoma 22: la distribuzione della lunghezza di parola cresce con $k$ e satura (valore evidenziato per $k = 14$ circa 23,5 milioni); la co-molteplicità è mostrata in scala log sull'asse delle molteplicità.

## Indici statistici (slide 32-37)
**Momento** di ordine $k$: valore atteso della $k$-esima potenza di $X$. Si assume $X$ con valori $x_1, \dots, x_n$ e probabilità $p_1, \dots, p_n$.
- **1° momento, media:** $E[X] = \sum_i p_i x_i$
- **2° momento:** $E[X^2] = \sum_i p_i x_i^2$
- **Varianza:** $var(X) = E[(X - \mu)^2] = \sum_i p_i (x_i - \mu)^2$. Formula utile per il calcolo iterativo:
$$var(X) = E[X^2] - (E[X])^2$$
  Dimostrazione: $\sum_i p_i (x_i - \mu)^2 = \sum_i p_i x_i^2 + \sum_i p_i \mu^2 - 2\mu \sum_i p_i x_i = E[X^2] + \mu^2 - 2\mu^2 = E[X^2] - (E[X])^2$
- **Deviazione standard:** $sd(X) = \sqrt{var(X)}$, quanto in media ci si discosta dalla media.
- **Coefficiente di variazione:** $\dfrac{sd(X)}{|\mu|}$
- **3° momento, skewness** (asimmetria):
$$\gamma_1 = E\left[\left(\frac{X - \mu}{\sigma}\right)^3\right] = \frac{E[X^3] - 3\mu E[X^2] + 3\mu^2 E[X] - \mu^3}{\sigma^3} = \frac{E[X^3] - 3\mu\sigma^2 - \mu^3}{\sigma^3} = \frac{E[(X - \mu)^3]}{(E[(X - \mu)^2])^{3/2}}$$
  Disegni: skewness **negativa** = coda lunga a sinistra, **positiva** = coda lunga a destra.
- **4° momento, kurtosis** (allungamento o appiattimento della coda):
$$Kurt[X] = E\left[\left(\frac{X - \mu}{\sigma}\right)^4\right] = \frac{E[(X - \mu)^4]}{(E[(X - \mu)^2])^2}$$
  In slide il denominatore è scritto $(E[X - \mu)^3])^2$: refuso, per coerenza con la definizione è $\sigma^4 = (E[(X - \mu)^2])^2$.

## Indici di dispersione e di diversità (slide 38-43)
- **Indice di dispersione:** quanto i valori di una distribuzione quantitativa distano da un valore centrale (media o mediana). Se la variabile è **nominale** (stati discreti non ordinabili) si chiama **indice di diversità**.
- **Indice di Simpson:** quanti tipi (specie) diversi ci sono in un dataset (comunità). Rappresenta tre aspetti della biodiversità:
  - **ricchezza** (richness): numero di specie diverse
  - **equitabilità:** omogeneità con cui gli individui sono distribuiti fra le specie
  - **dominanza:** quanto una specie domina sulle altre
$$\lambda = \sum_{i=1}^{R} p_i^2$$
  $R$ = ricchezza, $p_i$ = abbondanza (proporzionale) della specie $i$. $\lambda$ = **probabilità che due entità prese a caso siano dello stesso tipo**.
- **Indice di Shannon** (entropia di Shannon, in logaritmo naturale), basato sulla **media geometrica pesata** delle abbondanze proporzionali:
$$H = -\sum_{i=1}^{R} p_i \ln p_i = -\sum_{i=1}^{R} \ln p_i^{p_i} = -\ln(p_1^{p_1} p_2^{p_2} \cdots p_R^{p_R}) = \ln\frac{1}{\prod_{i=1}^{R} p_i^{p_i}}$$
- **Numeri di Hill** (generalizzazione delle misure di diversità): di ordine $q$, reciproco della **media generalizzata** $M_{q-1}$ delle abbondanze proporzionali:
$$^qD = \frac{1}{M_{q-1}} = \frac{1}{\sqrt[q-1]{\sum_{i=1}^{R} p_i\, p_i^{q-1}}} = \left(\sum_{i=1}^{R} p_i^q\right)^{\frac{1}{1-q}}$$
  - $q = 0$: la slide dice "in pratica la media delle abbondanze"; dalla formula risulta $^0D = \sum_i p_i^0 = R$, cioè la ricchezza (formulazione della slide ambigua).
  - $q = 1$: non definita, ma il limite per $q \to 1$ dà l'esponenziale dell'entropia di Shannon:
$$^1D = \frac{1}{\prod_{i=1}^{R} p_i^{p_i}} = e^{-\sum_{i=1}^{R} p_i \ln p_i} = e^{H}$$
  - $q = 2$: inverso dell'indice di Simpson, $^2D = \dfrac{1}{\lambda}$
- **Entropia di Rényi** (generalizza Shannon, $q \neq 1$):
$$^qH = \frac{1}{1-q} \ln\left(\sum_{i=1}^{R} p_i^q\right) = \ln\frac{1}{\sqrt[q-1]{\sum_{i=1}^{R} p_i\, p_i^{q-1}}} = \ln(^qD)$$

Esempio di verifica (non nelle slide): $p = (\frac12, \frac14, \frac14)$, $R = 3$.
- $\lambda = \frac14 + \frac1{16} + \frac1{16} = \frac38$, quindi $^2D = \frac83 \approx 2{,}67$
- $H$ in bit $= \frac12 \cdot 1 + \frac14 \cdot 2 + \frac14 \cdot 2 = 1{,}5$; $^1D = e^{H_{\ln}} = 2^{H_2} = 2^{1{,}5} \approx 2{,}83$
- $^0D = 3$

## Confrontare distribuzioni (slide 44-55)
Riassumere una distribuzione in un solo indice è svantaggioso per i confronti. Si usano misure di:
- similarità/dissimilarità fra **insiemi**
- vicinanza/prossimità in **spazi vettoriali**
- **correlazione** fra variabili
- **divergenza** fra distribuzioni di probabilità

### Insiemi
- **Jaccard** sui dizionari di k-mer di due genomi:
$$J_k(G_1, G_2) = \frac{|D_k(G_1) \cap D_k(G_2)|}{|D_k(G_1) \cup D_k(G_2)|}$$
- **Jaccard generalizzata** (multiinsiemi, considera le molteplicità), con $D_k(G_1, G_2) = D_k(G_1) \cup D_k(G_2)$:
$$J'_k(G_1, G_2) = \frac{\sum_{\alpha \in D_k(G_1, G_2)} \min(mult_{G_1}(\alpha), mult_{G_2}(\alpha))}{\sum_{\alpha \in D_k(G_1, G_2)} \max(mult_{G_1}(\alpha), mult_{G_2}(\alpha))}$$
- Entrambe a valori in $[0, 1]$.

### Spazi vettoriali
- Un genoma è un vettore le cui **dimensioni sono i k-mer**. Per confrontare due genomi servono le stesse dimensioni: $\Gamma^k$ oppure $D_k(G_1) \cup D_k(G_2)$. Per $k$ piccoli, $\Gamma^k$ permette di confrontare **più genomi** fra loro nello stesso spazio.
- **Coseno** ($A, B \in \mathbb{R}^n$):
$$cos\_sim(A, B) = \frac{\langle A|B \rangle}{\sqrt{\langle A|A \rangle}\sqrt{\langle B|B \rangle}} = \frac{\sum_{i=1}^{n} A[i]B[i]}{\sqrt{\sum_{i=1}^{n} A[i]^2}\sqrt{\sum_{i=1}^{n} B[i]^2}}$$
  In slide $\langle\cdot|\cdot\rangle$ è chiamato "prodotto vettoriale" ma è il prodotto scalare, e nella prima forma mancano le radici al denominatore (presenti nella seconda). Su spazio binario $\{0, 1\}^n$ equivale al **coefficiente di Tanimoto** (così in slide).
- **Minkowski** (metrica in spazio normato), $k \in \mathbb{N}^+$:
$$d_k(A, B) = \left(\sum_{i=1}^{n} |A[i] - B[i]|^k\right)^{\frac1k}$$
  $k = 1$ **Manhattan**, $k = 2$ **Euclidea**.
- **Hamming:** numero di posizioni in cui due vettori differiscono, cioè Manhattan su vettori booleani:
$$h(A, B) = \sum_{i=1}^{n} |A[i] - B[i]|$$
  Normalizzabile dividendo gli addendi per il valore massimo.

### Correlazione
- **Pearson:** grado di concordanza del cambiamento di due variabili reali:
$$\rho(X, Y) = \frac{cov(X, Y)}{\sigma_X \sigma_Y}, \qquad cov(X, Y) = E[(X - E[X])(Y - E[Y])] = \frac1n \sum_{i=1}^{n} (x_i - \bar{x})(y_i - \bar{y})$$
  Covarianza $> 0$: variabili **concordanti** (correlate); $< 0$: **discordanti** (anti-correlate). $\sigma_X, \sigma_Y > 0$ sempre, quindi il segno di $\rho$ è quello della covarianza.
- **Spearman:** come Pearson ma sui **ranghi** invece che sui valori.
- **Kendall:** conta le inversioni di rango fra coppie:
$$r = \frac{\#\text{coppie concordanti} - \#\text{coppie discordanti}}{\frac{n(n-1)}{2}}, \qquad \frac{n(n-1)}{2} = \#\text{coppie totali}$$
  La slide parla di "coppie contigue", ma il denominatore conta tutte le coppie.

### Divergenze
- **Kullback-Leibler** di $P$ da $Q$ (stesso dominio $D$): guadagno di informazione nell'usare $P$ invece di $Q$:
$$KL(P \| Q) = \sum_{x \in D} P(x) \log\frac{P(x)}{Q(x)}$$
  **Non simmetrica** ($KL(P\|Q) \neq KL(Q\|P)$) e in generale **senza massimo**. Simmetrizzazione: $\frac{KL(P\|Q) + KL(Q\|P)}{2}$, "tuttavia..." (la slide lascia intendere che non basta, da cui la JSD).
- **Jensen-Shannon:** simmetrica, basata sulla **distribuzione media** $A = \frac{P + Q}{2}$ e non sulla media delle divergenze:
$$JSD(P, Q) = \frac{KL(P \| A) + KL(Q \| A)}{2}$$
  Massimo 1 con logaritmo in base 2, altrimenti (così in slide) nessun limite superiore.
- **f-divergenze:** famiglia che comprende le precedenti; rappresentano la divergenza come media dell'odds ratio (rapporti di probabilità) ponderata da una funzione $f$.
- **Odds:** $\frac{p}{1 - p}$. **Odds ratio** (fattore di rischio vs malattia):
$$OR = \frac{\dfrac{P(malattia|esposti)}{1 - P(malattia|esposti)}}{\dfrac{P(malattia|non\ esposti)}{1 - P(malattia|non\ esposti)}}$$
- **Hellinger** (f-divergenza), a valori in $[0, 1]$:
$$HE(P, Q) = \frac{1}{\sqrt2}\sqrt{\sum_{x \in D}\left(\sqrt{P(x)} - \sqrt{Q(x)}\right)^2}, \qquad HE^2(P, Q) = 1 - \sum_{x \in D}\sqrt{P(x)Q(x)}$$

Esempio di verifica (non nelle slide), asimmetria della KL in base 2: $P = (\frac12, \frac12)$, $Q = (\frac14, \frac34)$.
- $KL(P\|Q) = \frac12\log_2 2 + \frac12\log_2\frac23 \approx 0{,}5 - 0{,}292 = 0{,}208$
- $KL(Q\|P) = \frac14\log_2\frac12 + \frac34\log_2\frac32 \approx -0{,}25 + 0{,}439 = 0{,}189$

## Teoria dell'informazione (slide 56-58)
- La sorgente informativa $(X, p)$ nasce per l'analisi matematica della **comunicazione**, per esprimere la natura probabilistica dell'informazione.
- L'informazione è **funzione inversa della probabilità**: controparte a posteriori dell'incertezza a priori, misura il guadagno di conoscenza dopo l'evento. **Evento più raro = più informativo.**
- $I(E) = \log\frac{1}{P(E)} = -\log P(E)$
- **Additività:** grazie al logaritmo, per eventi indipendenti ($P(E, E') = P(E) \cdot P(E')$) vale $I((E, E')) = I(E) + I(E')$.
- Informazione di una sorgente = entropia, media pesata delle informazioni dei singoli eventi:
$$I((X, p)) = H(X, p) = \sum_{a \in \hat{X}} p(a) I(a) = -\sum_{a \in \hat{X}} p(a) \log p(a)$$
  (in slide scritto $I(p(a))$). Richiamo della proprietà di equipartizione.

## Dall'entropia fisica a quella informazionale (slide 59-64)
- Termine coniato da **R. Clausius** (termodinamica), dal greco "en-tropos", verso interno. **Secondo principio** (sistemi isolati): $\Delta S \ge 0$.
- **Boltzmann** (gas perfetti): $H = \sum_{i=1}^{m} n_i \log_2 n_i$, con $n_i$ numero di molecole nella classe di velocità $i$; è la rappresentazione microscopica dell'entropia di Clausius (così in slide, senza segno meno).
- $S = k \cdot \log_e w$, $k$ costante di Boltzmann, $w$ = numero di **micro-stati** distinguibili associati al macro-stato. Con $V^n$ arrangiamenti di $n$ molecole in $V$ celle, $w$ = modi di dividere $n$ particelle in $m$ classi di velocità:
$$w = \frac{n!}{n_1!\, n_2! \cdots n_m!}$$
- **Derivazione** dell'entropia di Shannon:
  1. $S = k \ln\frac{n!}{n_1! \cdots n_m!}$
  2. Stirling $\ln(n!) \simeq n \ln n$: $S = k n \ln n - k(n_1 \ln n_1 + \cdots + n_m \ln n_m)$
  3. Sostituendo $n_i = n p_i$: $S = k n \ln n - k\sum_i n p_i (\ln n + \ln p_i) = k n \ln n - k n \ln n\,(p_1 + \cdots + p_m) - k n (p_1 \ln p_1 + \cdots + p_m \ln p_m)$
  4. Poiché $p_1 + \cdots + p_m = 1$ i primi due termini si annullano:
$$S = -k \cdot n \sum_{i=1}^{m} p_i \ln p_i$$
  In slide il secondo termine del passo 3 è scritto $k \cdot n \cdot \ln(p_1 + \cdots + p_m)$ e l'ultima sommatoria va fino a $n$: refusi (il passaggio torna solo con $\ln n \cdot (p_1 + \cdots + p_m)$ e indice fino a $m$).
- **Principio:** l'entropia di $(X, p)$ è proporzionale al logaritmo del numero $w$ di sorgenti distinte che danno gli stessi valori di $X$ con la stessa distribuzione $p$; quindi è legata al numero di sorgenti con la stessa entropia, cioè al numero di variabili stocastiche con la stessa distribuzione (le slide a volte dicono "proporzionale al numero", la formula dice al logaritmo del numero).
- **Principio circolare dell'entropia:**
$$H(X, p_x) = c \cdot \log_2 |\mathbb{X}|, \qquad \mathbb{X} = \{(Y, p_y) : \hat{X} = \hat{Y},\ p_x = p_y\}$$
  per una costante $c$. L'entropia è determinata da $p_X$ ma corrisponde anche al numero di modi di realizzare $p_X$. Due spazi:
  - **spazio interno:** insieme degli eventi della sorgente
  - **spazio esterno:** classe delle sorgenti con la stessa distribuzione di probabilità

## Entropia congiunta, informazione mutua, cross-entropia (slide 65-69)
- **Distribuzione congiunta** di $X$ e $Y$, definita su $\hat{X} \times \hat{Y}$: $p_{X,Y} = (p(x, y) \mid x \in \hat{X}, y \in \hat{Y})$.
- **Entropia congiunta:**
$$H(X \times Y, p_{X,Y}) = -\sum_{x \in \hat{X}, y \in \hat{Y}} p(x, y) \log_2 p(x, y)$$
- **Informazione mutua:** KL fra la congiunta $p_{(x,y)}$ e il prodotto delle marginali $p_x \times p_y$ (misura quanto $X$ e $Y$ si discostano dall'indipendenza):
$$I(X, Y) = KL(p_{(x,y)}, p_x \times p_y) = \sum_{x, y} p(x, y) \log\frac{p(x, y)}{p(x)p(y)}$$
  Derivazione:
  1. Si spezza il logaritmo: $= \sum_{x,y} p(x, y) \log\frac{p(x, y)}{p(x)} - \sum_{x,y} p(x, y) \log p(y)$
  2. Bayes: $\frac{p(x, y)}{p(x)} = p(y|x)$; nel secondo termine, sommando su $x$, $\sum_x p(x, y) = p(y)$
  3. $= \sum_{x,y} p(x, y) \log p(y|x) - \sum_y p(y) \log p(y) = H(Y) - H(Y|X)$

  Cioè l'informazione media di $Y$ meno l'informazione media di $Y$ dato $X$. (In slide il passo 2 è motivato con "$\sum_{x} p(x) = 1$".)
- Forme equivalenti:
$$I(X, Y) = H(X) - H(X|Y) = H(Y) - H(Y|X) = H(X) + H(Y) - H(X, Y) = H(X, Y) - H(X|Y) - H(Y|X)$$
  In slide le prime due sono scritte $H(Y) - H(X|Y)$ e $H(X) - H(Y|X)$, con i condizionamenti scambiati: refuso (la slide precedente stessa ricava $H(Y) - H(Y|X)$).
- **Cross-entropia** di $P$ e $Q$ sulla stessa variabile $X$:
$$H(P \| Q) = -E_P[\log_2 Q] = -\sum_{x \in \hat{X}} P(x) \log_2 Q(x) = H(P) + KL(P \| Q)$$
  Numero medio di **bit** per identificare un evento di $\hat{X}$ usando uno schema ottimizzato per $Q$ invece che per la vera $P$.

## Da ricordare per lo scritto
- $I(x) = -\log_2 p(x)$, $H = -\sum p \log_2 p$; massimo per distribuzione uniforme, $H_{max} = \log_2 n$ (vale 1 se la base è $n$). Evento raro = più informazione; additività per eventi indipendenti.
- Probabilità = a priori, frequenza = a posteriori.
- Definizioni su stringhe: $D(G)$, $D_k(G)$, $pos_G$, $mult_G$, hapax, repeat (massimale), hapax minimale, nullomero, elongazione, memer. Frequenza di un k-mer: $mult_G(\alpha) / (|G| - k + 1)$.
- Distribuzioni genomiche classificate per dominio: k-mer (molteplicità/frequenza di parola), rango (Zipf), molteplicità (co-molteplicità), lunghezza $k$ (lunghezza di parola, hapax, repeat).
- $var(X) = E[X^2] - (E[X])^2$ con dimostrazione; skewness = 3° momento standardizzato (asimmetria), kurtosis = 4° (coda); coefficiente di variazione $sd/|\mu|$.
- Simpson $\lambda = \sum p_i^2$ = probabilità che due individui presi a caso siano della stessa specie; Hill $^qD = (\sum p_i^q)^{1/(1-q)}$ con $^1D = e^H$ e $^2D = 1/\lambda$; Rényi $^qH = \ln(^qD)$.
- Jaccard (insiemi) e Jaccard generalizzata (min/max delle molteplicità), entrambe in $[0,1]$. Minkowski: $k=1$ Manhattan, $k=2$ Euclidea; Hamming = Manhattan su booleani; coseno su $\{0,1\}^n$ = Tanimoto.
- Pearson = cov$/(\sigma_X\sigma_Y)$, Spearman = Pearson sui ranghi, Kendall = (concordanti - discordanti)$/\binom{n}{2}$.
- KL non simmetrica e senza massimo; JSD simmetrica tramite la media $A = (P+Q)/2$, massimo 1 in base 2; Hellinger in $[0,1]$; sono f-divergenze.
- Informazione mutua $= KL(p_{x,y} \| p_x p_y) = H(X) + H(Y) - H(X,Y)$; cross-entropia $= H(P) + KL(P\|Q)$.
