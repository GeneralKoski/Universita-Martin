# Regressione

Fonte: `Regressione.pdf`

Il pacco è di 58 pagine (i numeri di slide qui sotto sono quelli di pagina). Tre blocchi: regressione lineare e polinomiale (slide 2-15), inferenza statistica e selezione del modello (slide 16-48), regressione non lineare e ai quantili (slide 49-58).

## Classificazione vs regressione (slide 2)
- **Classificazione** supervisionata: a ogni pattern $x_i$ del training set è associata un'etichetta $y_i$ (classe); il training apprende un **mapping** dallo spazio dei pattern a quello **discreto** delle etichette
- **Regressione**: i $y_i$ sono **numerici e continui** (in $\mathbb{R}$); il training apprende una **funzione** $f(x) \mapsto y$
- $f$ è controllata da un insieme di **parametri**; se la dipendenza dai **parametri** è lineare (es. nessun parametro elevato a potenza nella definizione di $f$) la regressione si dice **lineare**
- $x$ = variabile **indipendente**, $y$ = variabile **dipendente**
- Si assume che la variabile indipendente sia **esatta** e che la dipendente sia **affetta da errore** (es. imprecisione di misura)

## Regressione lineare semplice (slide 3-6)
- Variabile indipendente **scalare** (una sola) → **simple linear regression** (retta di regressione)
- TS di $n$ dati $(x_1, y_1), \dots, (x_n, y_n)$ con dipendenza
$$y_i = \alpha + \beta \cdot x_i + \varepsilon_i$$
  dove $\varepsilon_i$ è l'**errore di misura** (incognito) del punto $x_i$ e $\alpha, \beta$ sono i parametri da determinare
- Soluzione ai **minimi quadrati** (**Least Square**): la retta $f(x) = \alpha + \beta x$ che minimizza la **somma dei quadrati dei residui**
$$\alpha^*, \beta^* = \arg\min_{\alpha,\beta}\sum_{i=1}^{n}(f(x_i) - y_i)^2 = \arg\min_{\alpha,\beta}\sum_{i=1}^{n}\varepsilon_i^2$$
- Figura (slide 4): quattro punti rossi, retta blu *curve fit*, **residui** $\varepsilon_i$ come segmenti verticali verdi fra punto e retta. (Aggiunta, non nelle slide: i punti sono $(1,6), (2,5), (3,7), (4,10)$ e la retta è $y = 3.5 + 1.4x$, con $RSS = 4.2$.)
- Uguagliando a zero le **derivate parziali** rispetto ad $\alpha, \beta$ si ottengono le **equazioni normali** (2 equazioni, 2 incognite), da cui
$$\beta^* = \frac{\sum_{i=1}^{n}(x_i - \bar{x})(y_i - \bar{y})}{\sum_{i=1}^{n}(x_i - \bar{x})^2} \qquad \alpha^* = \bar{y} - \beta^*\bar{x}$$
  con $\bar{x}, \bar{y}$ medie di $x_i$ e $y_i$
- Servono **almeno due punti**, altrimenti il denominatore si annulla. (Precisazione: servono almeno due $x_i$ **distinti**; con tutti gli $x_i$ uguali il denominatore è zero anche con molti punti.)
- La retta passa sempre per il **baricentro** $(\bar{x}, \bar{y})$ (Aggiunta, non nelle slide: segue da $\alpha^* = \bar{y} - \beta^*\bar{x}$)
- Figura (slide 6): *Predizione Altezza da Peso*, scatter di 18 persone (peso 46-72, altezza 157-179) con la retta di regressione blu. (Aggiunta, non nelle slide: dai dati della tabella $\text{Altezza} \approx 125.2 + 0.72 \cdot \text{Peso}$, $R^2 \approx 0.71$; per 60 kg predice circa 168 cm.)

## Regressione lineare multipla (slide 7-10)
- Variabile indipendente **vettoriale** $\mathbf{x} \in \mathbb{R}^d$ → **multiple linear regression** (iperpiano di regressione; figura 3D: piano che attraversa una nuvola di punti)
- Matrice $\mathbf{X}$ di dimensione $n \times (d+1)$: sulle righe gli $n$ punti del TS, più una **colonna di 1 a destra** (serve per il termine noto)
$$\mathbf{X} = \begin{bmatrix} x_{11} & \cdots & x_{1d} & 1 \\ x_{21} & \cdots & x_{2d} & 1 \\ \vdots & \ddots & \vdots & \vdots \\ x_{n1} & \cdots & x_{nd} & 1 \end{bmatrix} \qquad \mathbf{y} = \begin{bmatrix} y_1 \\ \vdots \\ y_n \end{bmatrix} \qquad \beta = \begin{bmatrix} \beta_1 \\ \vdots \\ \beta_{d+1} \end{bmatrix}$$
  $\mathbf{y}$ ha uno scalare per pattern, $\beta$ ha i $d + 1$ parametri e $\beta_{d+1}$ è il **termine noto**. (Errore nella slide 8: dice che $\mathbf{y}$ è costruito "a partire dai valori della variabile **indipendente**"; $\mathbf{y}$ contiene i valori della variabile **dipendente**.)
- Equazioni: $y_i = \sum_{j=1}^{d+1} x_{ij}\beta_j$ per $i = 1, \dots, n$ (indici riferiti a $\mathbf{X}$), in forma matriciale
$$\mathbf{y} = \mathbf{X}\beta$$
- Per $n > d + 1$ la matrice è rettangolare: sistema **sovradeterminato** (nessuna soluzione esatta in generale). Funzione obiettivo least square:
$$\|\mathbf{y} - \mathbf{X}\beta\|^2$$

### Equazioni normali (slide 10)
$$\nabla_\beta\|\mathbf{y} - \mathbf{X}\beta\|^2 = -2\mathbf{X}^T(\mathbf{y} - \mathbf{X}\beta) = \mathbf{0} \quad \Rightarrow \quad \mathbf{X}^T\mathbf{X}\beta = \mathbf{X}^T\mathbf{y}$$
- Se le colonne di $\mathbf{X}$ sono **linearmente indipendenti**, $\mathbf{X}^T\mathbf{X}$ è invertibile e
$$\hat{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$$
- **Valori predetti**: $\hat{\mathbf{y}} = \mathbf{X}\hat{\beta} = \mathbf{H}\mathbf{y}$ con $\mathbf{H} = \mathbf{X}(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T$ (**hat matrix**): **proiezione ortogonale** di $\mathbf{y}$ sullo spazio generato dalle colonne di $\mathbf{X}$
- **Residui**: $\mathbf{e} = \mathbf{y} - \hat{\mathbf{y}} = (\mathbf{I} - \mathbf{H})\mathbf{y}$, **ortogonali** alle colonne di $\mathbf{X}$ ($\mathbf{X}^T\mathbf{e} = \mathbf{0}$)
- In pratica l'inversa **non si calcola mai**: si usa la fattorizzazione **QR** ($\mathbf{X} = \mathbf{QR} \Rightarrow \mathbf{R}\hat{\beta} = \mathbf{Q}^T\mathbf{y}$) o la **SVD** (pseudo-inversa), numericamente più stabili quando $\mathbf{X}^T\mathbf{X}$ è **mal condizionata**. Costo $O(nd^2)$

## Regressione vs fitting geometrico (slide 11)
- Figura: stessa nuvola di punti, a sinistra *Linear Regression (Least Square)* con i residui come segmenti **verticali**, a destra *PCA* con segmenti **perpendicolari** alla retta
- La regressione least square minimizza le **distanze verticali** dall'iperpiano, non le **distanze euclidee** (che si minimizzano con la **PCA**)
- Motivo: le due variabili **non hanno ruolo simmetrico** (indipendente esatta, dipendente con errore); **scambiando le variabili il risultato cambia**
- Per **nuvole di punti geometrici** le coordinate hanno lo stesso ruolo e il **PCA fitting** è preferibile

## Accuratezza di predizione (slide 12-13)
Con $y_i$ valore osservato e $\hat{y}_i$ valore predetto ($\hat{y}_i - y_i$ è l'errore punto per punto):

| Misura | Formula | Note |
|---|---|---|
| **MSE** (Mean Square Error) | $\frac{1}{N}\sum_{i=1}^{N}(\hat{y}_i - y_i)^2$ | criterio **implicito** nell'ottimizzazione least square |
| **RMSE** (Root MSE) | $\sqrt{MSE}$ | indicatore di accuratezza, stessa unità di $y$ |
| **MAE** (Mean Absolute Error) | $\frac{1}{N}\sum_{i=1}^{N}\lvert\hat{y}_i - y_i\rvert$ | più **robusto agli outlier** di MSE; mantiene l'unità di misura (es. metri) |
| **MAPE** (Mean Absolute Percentage Error) | $\frac{1}{N}\sum_{i=1}^{N}\left\lvert\frac{\hat{y}_i - y_i}{y_i}\right\rvert$ | variante del MAE con penalità sullo scostamento **percentuale** rispetto alla grandezza dei dati |
| **$R^2$** (coefficiente di determinazione) | $1 - \frac{\sum_{i}(y_i - \hat{y}_i)^2}{\sum_{i}(y_i - \bar{y})^2}$ | fra 0 e 1, quanto il modello lineare **spiega la varianza** di $y$; **non valido per modelli non lineari** |

- MAE, MAPE e $R^2$ **non** sono direttamente utilizzabili come loss del modello lineare (risolto ai minimi quadrati)
- (Aggiunta, non nelle slide: il MAPE non è definito se qualche $y_i = 0$ ed esplode per $y_i$ vicini a zero)

## Regressione polinomiale (slide 14-15)
- Con un semplice accorgimento si usa ancora la regressione lineare per approssimare **curve e superfici**: basta che $f$ sia **lineare rispetto ai parametri**, non rispetto alla variabile indipendente, i cui elementi possono comparire **elevati a potenza**, **combinati** fra loro, come argomento di **funzioni trascendenti**, ecc.
- Esempio $d = 1$, modello **quadratico** $y = \beta_1 x^2 + \beta_2 x + \beta_3$:
$$\mathbf{X} = \begin{bmatrix} x_1^2 & x_1 & 1 \\ x_2^2 & x_2 & 1 \\ \vdots & \vdots & \vdots \\ x_n^2 & x_n & 1 \end{bmatrix}$$
- Figure: parabola blu che fitta punti rossi ($d = 1$) e superficie curva in 3D ($d = 2$)

## Inferenza statistica e selezione del modello (slide 16-17)
- Domande: il modello stimato è **affidabile**? Quali variabili **servono davvero**? Quale modello scegliere fra più **candidati**?
- Finora $\hat{\beta}$ è una **stima puntuale**, ma il training set è un **campione**: ripetendo l'esperimento (nuovi $\varepsilon_i$) si otterrebbe un $\hat{\beta}$ diverso, quindi $\hat{\beta}$ è una **variabile aleatoria**

| Domanda | Strumento |
|---|---|
| il coefficiente $\beta_j$ è davvero $\ne 0$? (la variabile $x_j$ serve?) | **test t** |
| il modello nel complesso spiega qualcosa? | **test F / ANOVA** |
| fra due modelli **annidati**, il più complesso è significativamente migliore? | **F parziale**, **likelihood ratio test** ($\chi^2$) |
| fra modelli **qualsiasi**, quale scegliere? | **AIC, BIC**, cross-validation |
| i dati rispettano le ipotesi del modello? | **diagnostica dei residui**, test $\chi^2$ di adattamento |

### Ipotesi del modello lineare classico (slide 18)
$$\mathbf{y} = \mathbf{X}\beta + \varepsilon, \qquad \mathbf{X} \in \mathbb{R}^{n \times p}, \quad p = d + 1$$
1. **linearità** nei parametri
2. errori a **media nulla**: $E[\varepsilon_i] = 0$
3. **omoschedasticità**: $Var(\varepsilon_i) = \sigma^2$ costante
4. errori **incorrelati**: $Cov(\varepsilon_i, \varepsilon_j) = 0$ per $i \ne j$
5. $\mathbf{X}$ a **rango pieno** ($p$ colonne linearmente indipendenti)
6. (per l'inferenza) **normalità**: $\varepsilon \sim N(\mathbf{0}, \sigma^2\mathbf{I})$

- **Teorema di Gauss-Markov**: sotto le ipotesi 1-5 lo stimatore least square è **BLUE** (Best Linear Unbiased Estimator): fra gli stimatori **lineari e non distorti** è quello a **varianza minima**
- Aggiungendo la 6: $\hat{\beta} \sim N(\beta, \sigma^2(\mathbf{X}^T\mathbf{X})^{-1})$ e least square **coincide con la stima di massima verosimiglianza**

### Richiami: test d'ipotesi (slide 19)
- **Ipotesi nulla** $H_0$ (es. $\beta_j = 0$) e **alternativa** $H_1$ (es. $\beta_j \ne 0$)
- **Statistica test** $T$: funzione dei dati con distribuzione **nota sotto $H_0$**
- **p-value**: probabilità, **assumendo $H_0$ vera**, di osservare un valore di $T$ **estremo almeno quanto** quello osservato
- **Livello di significatività** $\alpha$ (tipicamente 0.05): si rifiuta $H_0$ se p-value $< \alpha$
- **Errore di I tipo**: rifiutare $H_0$ vera (probabilità $\alpha$); **errore di II tipo**: non rifiutare $H_0$ falsa; **potenza** $= 1 - P(\text{errore II tipo})$
- **Attenzione**:
  - non rifiutare $H_0$ **non** significa dimostrarla
  - il p-value **non** è la probabilità che $H_0$ sia vera
  - con $m$ test la probabilità di almeno un falso positivo cresce: **correzione di Bonferroni** (si usa $\alpha/m$)

### Tre distribuzioni fondamentali (slide 20)
Con $Z, Z_1, \dots, Z_k$ indipendenti $\sim N(0, 1)$:
- **chi quadro** con $k$ gradi di libertà: $\chi^2_k = \sum_{i=1}^{k} Z_i^2$, $E[\chi^2_k] = k$, $Var[\chi^2_k] = 2k$
- **t di Student**: $t_k = \dfrac{Z}{\sqrt{\chi^2_k / k}}$
- **F di Fisher-Snedecor**: $F_{k_1, k_2} = \dfrac{\chi^2_{k_1}/k_1}{\chi^2_{k_2}/k_2}$, con numeratore e denominatore indipendenti
- Nota: $t_k^2 = F_{1,k}$
- Figura: densità di $\chi^2_k$ per $k = 2, 3, 5, 8$; per $k = 2$ parte da 0.5 in 0 ed è decrescente, al crescere di $k$ il picco si sposta a destra e si abbassa

### Stima della varianza dell'errore (slide 21)
- $\sigma^2$ è incognita; stimatore **non distorto**:
$$s^2 = \frac{RSS}{n - p}, \qquad RSS = \sum_{i=1}^{n} e_i^2 = \sum_{i=1}^{n}(y_i - \hat{y}_i)^2$$
- $n - p$ = **gradi di libertà residui**: $p$ gradi di libertà sono "consumati" per stimare $\beta$
- $s$ = **errore standard dei residui** (stessa unità di $y$); differisce dal RMSE ($\sqrt{RSS/n}$) **solo per il denominatore**
- Sotto normalità $\frac{(n-p)s^2}{\sigma^2} \sim \chi^2_{n-p}$, **indipendente da $\hat{\beta}$**: è ciò che permette i test t ed F

### Test t sui singoli coefficienti (slide 22)
- Errore standard del coefficiente $j$-esimo: $SE(\hat{\beta}_j) = s\sqrt{[(\mathbf{X}^T\mathbf{X})^{-1}]_{jj}}$
- $H_0: \beta_j = 0$ vs $H_1: \beta_j \ne 0$
$$t_j = \frac{\hat{\beta}_j}{SE(\hat{\beta}_j)} \sim t_{n-p} \text{ sotto } H_0, \qquad \text{p-value} = 2P(t_{n-p} > |t_j|)$$
- **Intervallo di confidenza** di livello $1 - \alpha$: $\hat{\beta}_j \pm t_{1-\alpha/2,\,n-p} \cdot SE(\hat{\beta}_j)$. $H_0$ è rifiutata al livello $\alpha$ $\Leftrightarrow$ lo **0 non appartiene** all'intervallo
- Nella regressione semplice:
$$SE(\hat{\beta}) = \frac{s}{\sqrt{\sum_i(x_i - \bar{x})^2}} \qquad SE(\hat{\alpha}) = s\sqrt{\frac{1}{n} + \frac{\bar{x}^2}{\sum_i(x_i - \bar{x})^2}}$$
- Il test valuta il contributo di $x_j$ **a parità delle altre variabili** presenti nel modello

### Esempio: regressione semplice e test t (slide 23-24)

| $x$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|
| $y$ | 2.3 | 2.9 | 4.8 | 4.1 | 6.5 | 6.0 | 8.2 | 7.4 |

- $n = 8$, $\bar{x} = 4.5$, $\bar{y} = 5.275$, $\sum(x_i - \bar{x})^2 = 42$, $\sum(x_i - \bar{x})(y_i - \bar{y}) = 34.1$
- $\hat{\beta} = 34.1/42 = 0.812$, $\hat{\alpha} = 5.275 - 0.812 \cdot 4.5 = 1.621$
- $RSS = 3.509$, $s^2 = 3.509/6 = 0.585$, $s = 0.765$
- $SE(\hat{\beta}) = 0.765/\sqrt{42} = 0.118$, $t = 0.812/0.118 = 6.88$; con 6 gradi di libertà $t_{0.975,6} = 2.447$, p-value $\approx 0.0005$ → **pendenza significativa**
- $SE(\hat{\alpha}) = 0.596$, $t = 2.72$, p-value $\approx 0.035$ → intercetta significativa al **5%** ma **non all'1%**
- Tipico output di libreria (statsmodels, `summary()` in R):

| | coef | std err | t | $P > \lvert t\rvert$ | [0.025 | 0.975] |
|---|---|---|---|---|---|---|
| intercetta | 1.621 | 0.596 | 2.72 | 0.035 | 0.163 | 3.080 |
| $x$ | 0.812 | 0.118 | 6.88 | 0.000 | 0.523 | 1.101 |

- Tutti i numeri ricalcolati e corretti (p-value pendenza 0.00046; il "0.000" della tabella è l'arrotondamento)
- (Aggiunta, non nelle slide: qui $RMSE = \sqrt{3.509/8} = 0.662$, contro $s = 0.765$: stessa RSS, denominatore $n$ invece di $n - p$)

### Intervalli di confidenza e di predizione (slide 25)
Nuovo punto $\mathbf{x}_0$, predizione $\hat{y}_0 = \mathbf{x}_0^T\hat{\beta}$. Due domande diverse:
- dove sta la **media** $E[y \mid \mathbf{x}_0]$? → **intervallo di confidenza**
$$\hat{y}_0 \pm t_{1-\alpha/2,\,n-p}\; s\sqrt{\mathbf{x}_0^T(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{x}_0}$$
- dove cadrà una **nuova osservazione** $y_0$? → **intervallo di predizione**
$$\hat{y}_0 \pm t_{1-\alpha/2,\,n-p}\; s\sqrt{1 + \mathbf{x}_0^T(\mathbf{X}^T\mathbf{X})^{-1}\mathbf{x}_0}$$
- L'intervallo di predizione è **sempre più ampio**: include anche il rumore $\varepsilon_0$ della nuova osservazione, che **non si riduce aumentando $n$**
- Entrambi si **allargano allontanandosi da $\bar{\mathbf{x}}$**: **estrapolare è rischioso**
- (Aggiunta, non nelle slide, sull'esempio delle slide 23-24 al 95%: in $x_0 = 4.5$ si ha $\hat{y}_0 = 5.28$, confidenza $\pm 0.66$, predizione $\pm 1.98$; in $x_0 = 10$ (fuori dai dati) $\hat{y}_0 = 9.74$, confidenza $\pm 1.72$, predizione $\pm 2.54$)

### Decomposizione della varianza e $R^2$ (slide 26-27)
- $TSS = \sum_i(y_i - \bar{y})^2$ variabilità **totale**; $ESS = \sum_i(\hat{y}_i - \bar{y})^2$ variabilità **spiegata**; $RSS = \sum_i(y_i - \hat{y}_i)^2$ variabilità **residua**
- Se il modello contiene l'**intercetta**, $\hat{\mathbf{y}} - \bar{y}\mathbf{1}$ ed $\mathbf{e}$ sono **ortogonali**, quindi (Pitagora)
$$TSS = ESS + RSS \quad \Rightarrow \quad R^2 = \frac{ESS}{TSS} = 1 - \frac{RSS}{TSS}$$
- Ecco perché $R^2$ **non vale** per modelli **non lineari** (o **senza intercetta**): la decomposizione non regge più
- Nell'esempio: $31.195 = 27.686 + 3.509$, $R^2 = 0.888$
- **$R^2$ non diminuisce mai** aggiungendo variabili (anche puro rumore): non si può usare per confrontare modelli con **numero diverso di parametri**
- **$R^2$ aggiustato**: confronta le **varianze stimate** invece delle somme dei quadrati
$$R^2_{adj} = 1 - \frac{RSS/(n-p)}{TSS/(n-1)} = 1 - (1 - R^2)\frac{n-1}{n-p}$$
  - **penalizza** il numero di parametri $p$
  - aumenta **solo** se la nuova variabile riduce RSS più di quanto ci si aspetterebbe per caso
  - **può essere negativo**
  - nell'esempio: $R^2_{adj} = 1 - 0.112 \cdot 7/6 = 0.869$

### ANOVA per la regressione: test F globale (slide 28-30)
- $H_0: \beta_1 = \dots = \beta_d = 0$ (nessuna variabile spiega $y$, basta la media); $H_1$: almeno un $\beta_j \ne 0$
- **Tabella ANOVA** (ANalysis Of VAriance; SS = somma dei quadrati, gdl = gradi di libertà, MS = media dei quadrati):

| Sorgente | SS | gdl | MS | F |
|---|---|---|---|---|
| Regressione | ESS | $p - 1$ | $MSR = ESS/(p-1)$ | $MSR/MSE$ |
| Residuo | RSS | $n - p$ | $MSE = RSS/(n-p)$ | |
| Totale | TSS | $n - 1$ | | |

- Sotto $H_0$: $F = \frac{MSR}{MSE} \sim F_{p-1,\,n-p}$; si rifiuta per $F$ **grande**
- **Intuizione**: se $H_0$ è vera sia MSR sia MSE stimano $\sigma^2$ e $F \approx 1$; se il modello spiega davvero parte della variabilità, MSR è molto più grande di MSE
- Figura (slide 29): densità di $F_{2,20}$ (es. $d = 2$ variabili, $n = 23$ punti), soglia $F_{0.95}(2, 20) = 3.49$ con l'area $\alpha = 0.05$ ombreggiata a destra: il test è **a una coda**
- **Esempio** (dati delle slide 23-24, $n = 8$, $p = 2$):

| Sorgente | SS | gdl | MS | F |
|---|---|---|---|---|
| Regressione | 27.686 | 1 | 27.686 | 47.34 |
| Residuo | 3.509 | 6 | 0.585 | |
| Totale | 31.195 | 7 | | |

  - $F_{0.95}(1, 6) = 5.99$, p-value $\approx 0.0005$ → si rifiuta $H_0$
  - con **una sola variabile** il test F globale **coincide** con il test t sulla pendenza: $F = t^2 = 6.88^2 = 47.34$, stesso p-value. (Arrotondamento: $6.88^2 = 47.33$; 47.34 viene dal $t$ non arrotondato, 6.8804.)
  - con **più variabili** i due test rispondono a domande diverse: può accadere che $F$ sia significativo ma **nessun $t_j$** lo sia (sintomo tipico di **multicollinearità**)

### Test F parziale fra modelli annidati (slide 31)
- Modello **ridotto** $M_0$ con $p_0$ parametri contenuto nel modello **completo** $M_1$ con $p_1 > p_0$ (es. polinomio di grado 3 vs grado 4)
- $H_0$: i $p_1 - p_0$ parametri aggiuntivi sono tutti nulli
$$F = \frac{(RSS_0 - RSS_1)/(p_1 - p_0)}{RSS_1/(n - p_1)} \sim F_{p_1 - p_0,\,n - p_1}$$
- Misura se la riduzione dei residui dovuta ai parametri aggiuntivi supera quella **attesa per caso**
- Il test F **globale** è il caso $M_0$ = **sola intercetta**; il test **t** su un coefficiente è il caso $p_1 - p_0 = 1$ (e $F = t^2$)
- Usi tipici: scegliere il **grado di un polinomio**, verificare se un **gruppo di variabili** (es. le dummy di una variabile categorica) è utile
- Vale **solo per modelli annidati**

### ANOVA a una via (slide 32-34)
- Nata con **Fisher** (anni '20) per confrontare le **medie di $k$ gruppi**. $y_{ij}$ = $j$-esima osservazione del gruppo $i$, $n_i$ osservazioni nel gruppo $i$, $N = \sum_i n_i$, $\bar{y}_i$ media del gruppo, $\bar{y}$ media globale
- $H_0: \mu_1 = \mu_2 = \dots = \mu_k$ vs $H_1$: almeno una media è diversa
$$\underbrace{\sum_{i,j}(y_{ij} - \bar{y})^2}_{SS_T} = \underbrace{\sum_i n_i(\bar{y}_i - \bar{y})^2}_{SS_B\ \text{(tra gruppi)}} + \underbrace{\sum_{i,j}(y_{ij} - \bar{y}_i)^2}_{SS_W\ \text{(entro i gruppi)}}$$
$$F = \frac{SS_B/(k-1)}{SS_W/(N-k)} \sim F_{k-1,\,N-k}$$
- Ipotesi: osservazioni **indipendenti**, **normalità** entro i gruppi, **varianze uguali** fra i gruppi (verificabile con i test di **Levene** o **Bartlett**)

**ANOVA come caso particolare della regressione** (slide 33):
- Variabile categorica con $k$ livelli → $k - 1$ **variabili dummy** (one-hot eliminando una **categoria di riferimento**). Con $k$ dummy più l'intercetta le colonne di $\mathbf{X}$ sarebbero linearmente dipendenti: **dummy variable trap**
$$y = \beta_0 + \beta_1 D_1 + \dots + \beta_{k-1}D_{k-1} + \varepsilon$$
- $\beta_0$ = media del gruppo di riferimento, $\beta_i = \mu_{i+1} - \mu_1$
- $H_0$ dell'ANOVA $\Leftrightarrow \beta_1 = \dots = \beta_{k-1} = 0 \Leftrightarrow$ test F globale della regressione; $SS_B = ESS$, $SS_W = RSS$
- **Modello lineare generale**: test t, ANOVA e regressione sono casi particolari di $\mathbf{y} = \mathbf{X}\beta + \varepsilon$. Estensioni: **ANOVA a due vie** (con interazioni), **ANCOVA** (variabili numeriche e categoriche), **MANOVA** ($y$ multivariata)

**Esempio: tre configurazioni di un algoritmo genetico** (slide 34), 5 esecuzioni indipendenti (seed diversi) ciascuna, fitness finale:

| Config. | Esecuzioni | $\bar{y}_i$ |
|---|---|---|
| A | 12, 14, 11, 15, 13 | 13 |
| B | 16, 18, 15, 17, 19 | 17 |
| C | 13, 15, 14, 12, 16 | 14 |

| | SS | gdl | MS | F |
|---|---|---|---|---|
| Tra | 43.33 | 2 | 21.67 | 8.67 |
| Entro | 30.00 | 12 | 2.50 | |
| Totale | 73.33 | 14 | | |

- $\bar{y} = 14.67$, $F_{0.95}(2, 12) = 3.89$, p-value $\approx 0.005$ → le configurazioni **non sono equivalenti** (numeri ricalcolati, tutti corretti)
- **Quali** differiscono? Servono test **post-hoc** (Tukey HSD, test t a coppie con correzione di Bonferroni)
- Se le configurazioni sono valutate sulle **stesse istanze** i dati non sono indipendenti: **ANOVA a misure ripetute** o test non parametrico di **Friedman**

### Test del chi quadro (slide 35-37)
- Per variabili **categoriche**: confronta le frequenze **osservate** $O_i$ con quelle **attese** $E_i$ sotto $H_0$ (Pearson)
$$\chi^2 = \sum_i\frac{(O_i - E_i)^2}{E_i} \overset{approx}{\sim} \chi^2_{gdl}$$
1. **Bontà di adattamento** (goodness of fit): i dati seguono una distribuzione teorica? $k$ categorie, $gdl = k - 1 - m$, con $m$ = parametri della distribuzione stimati dai dati
2. **Indipendenza** fra due variabili categoriche (tabella di contingenza $r \times c$):
$$E_{ij} = \frac{(\text{totale riga } i)\cdot(\text{totale colonna } j)}{N}, \qquad gdl = (r-1)(c-1)$$
- Si rifiuta $H_0$ per $\chi^2$ **grande**. Approssimazione affidabile se $E_i \ge 5$ in tutte le celle (altrimenti si accorpano categorie o si usa il **test esatto di Fisher**)

**Esempio: test di indipendenza** (slide 36): 150 utenti, il piano dipende dal dispositivo? (attese fra parentesi)

| | Base | Standard | Premium | Tot |
|---|---|---|---|---|
| Desktop | 30 (33.3) | 45 (40.0) | 25 (26.7) | 100 |
| Mobile | 20 (16.7) | 15 (20.0) | 15 (13.3) | 50 |
| Tot | 50 | 60 | 40 | 150 |

- Es. $E_{11} = 100 \cdot 50/150 = 33.3$
- $\chi^2 = \frac{(30-33.3)^2}{33.3} + \frac{(45-40)^2}{40} + \dots + \frac{(15-13.3)^2}{13.3} = 3.19$; $gdl = (2-1)(3-1) = 2$, $\chi^2_{0.95,2} = 5.99$, p-value $\approx 0.20$ → **non si rifiuta** l'indipendenza (ricalcolato: 3.1875, p = 0.203)

**Il chi quadro in regressione e nel ML** (slide 37):
- **Normalità dei residui**: si dividono i residui standardizzati in classi e si confrontano con le frequenze attese per una $N(0,1)$ ($gdl = k - 3$ se media e varianza sono stimate). Alternative: **Shapiro-Wilk**, **Q-Q plot**
- **Varianza dell'errore**: da $(n-p)s^2/\sigma^2 \sim \chi^2_{n-p}$ si ottiene un intervallo di confidenza per $\sigma^2$
- **Likelihood ratio test** (teorema di **Wilks**), per modelli annidati stimati a massima verosimiglianza:
$$LR = -2(\ell_0 - \ell_1) \overset{approx}{\sim} \chi^2_{p_1 - p_0}$$
  generalizza il test F parziale a modelli **non gaussiani** (regressione logistica, GLM, dove $-2\ell$ è detta **devianza**)
- **Feature selection**: in scikit-learn `SelectKBest(chi2)` ordina le feature (non negative, es. conteggi) per la statistica $\chi^2$ di dipendenza dalla classe

### Verosimiglianza del modello lineare (slide 38)
Con $\varepsilon_i \sim N(0, \sigma^2)$ indipendenti:
$$L(\beta, \sigma^2) = \prod_{i=1}^{n}\frac{1}{\sqrt{2\pi\sigma^2}}\exp\left(-\frac{(y_i - \mathbf{x}_i^T\beta)^2}{2\sigma^2}\right)$$
$$\ell(\beta, \sigma^2) = \log L = -\frac{n}{2}\log(2\pi\sigma^2) - \frac{RSS(\beta)}{2\sigma^2}$$
- Massimizzare $\ell$ rispetto a $\beta$ $\Leftrightarrow$ minimizzare RSS: **MLE = least square**
- $\hat{\sigma}^2_{ML} = RSS/n$ (**distorto**, a differenza di $s^2$)
- Sostituendo le stime:
$$\ell_{max} = -\frac{n}{2}\left[\log\left(2\pi\frac{RSS}{n}\right) + 1\right]$$
  la log-verosimiglianza massima dipende **solo da RSS**: è la base di **AIC e BIC**

### Selezione del modello (slide 39)
- Aggiungere parametri riduce **sempre** RSS sul training set (e aumenta $\ell_{max}$) → **overfitting**
- Bilanciare **bontà di adattamento** e **complessità** (principio di **parsimonia**, **rasoio di Occam**, trade-off **bias-varianza**)
- Approcci:
  - **test d'ipotesi** (F parziale, likelihood ratio): **solo modelli annidati**
  - **criteri informativi** (AIC, BIC): penalizzano $\ell_{max}$ con il numero di parametri; vanno bene anche per modelli **non annidati** (purché stimati sugli **stessi dati** e con la **stessa $y$**)
  - **validazione** (hold-out, k-fold cross-validation): stima **diretta** dell'errore di generalizzazione, computazionalmente più **costosa**
  - **regolarizzazione** (Ridge, Lasso): complessità controllata **in modo continuo**

### AIC e BIC (slide 40-41)
- $k$ = numero di parametri stimati (in regressione: $p$ coefficienti + $\sigma^2$, quindi $k = p + 1$)
$$AIC = 2k - 2\ell_{max} \ \text{(Akaike, 1974)} \qquad BIC = k\ln n - 2\ell_{max} \ \text{(Schwarz, 1978)}$$
- Per il modello lineare gaussiano, a meno di costanti comuni a tutti i modelli:
$$AIC = n\ln\frac{RSS}{n} + 2k \qquad BIC = n\ln\frac{RSS}{n} + k\ln n$$
- Si sceglie il modello con valore **minimo**; contano solo le **differenze** fra modelli
- La penalità del BIC supera quella dell'AIC quando $\ln n > 2$ ($n \ge 8$): **BIC è più parsimonioso**
- **AIC** stima la **distanza di Kullback-Leibler** dal modello vero: orientato alla **predizione** (asintoticamente equivalente alla **leave-one-out cross-validation**)
- **BIC** è **consistente**: se il modello vero è fra i candidati, viene scelto con probabilità $\to 1$ per $n \to \infty$
- **Interpretazione bayesiana del BIC**:
$$P(M \mid D) \propto P(D \mid M)P(M), \qquad P(D \mid M) = \int P(D \mid \theta, M)P(\theta \mid M)\,d\theta$$
  approssimando l'integrale (metodo di **Laplace**) per $n$ grande:
$$\ln P(D \mid M) \approx \ell_{max} - \frac{k}{2}\ln n \quad \Rightarrow \quad BIC \approx -2\ln P(D \mid M)$$
  - minimizzare il BIC $\approx$ scegliere il modello con **massima evidenza** (con prior uniforme sui modelli)
  - **fattore di Bayes**: $B_{10} = \frac{P(D \mid M_1)}{P(D \mid M_0)} \approx \exp(-\Delta BIC/2)$, con $\Delta BIC = BIC_1 - BIC_0$
  - scala di **Kass & Raftery** per $\Delta BIC$: 0-2 evidenza debole, 2-6 positiva, 6-10 forte, > 10 molto forte

### Esempio: scelta del grado del polinomio (slide 42)
Polinomi di grado 1-6 su $n = 50$ punti ($k$ = grado + 2); $F$ = test parziale rispetto al grado precedente, $F_{0.95}(1, \approx 45) \approx 4.05$:

| grado | $k$ | RSS | F | AIC | BIC |
|---|---|---|---|---|---|
| 1 | 3 | 412.0 | - | 111.45 | 117.19 |
| 2 | 4 | 198.5 | 50.55 | 76.94 | 84.59 |
| 3 | 5 | 101.3 | 44.14 | 45.30 | **54.86** |
| 4 | 6 | 95.8 | 2.58 | **44.51** | 55.98 |
| 5 | 7 | 94.1 | 0.79 | 45.62 | 59.00 |
| 6 | 8 | 93.6 | 0.23 | 47.35 | 62.65 |

- Figura: AIC e BIC per grado, entrambi crollano fino al grado 3 e poi risalgono piano (il BIC più rapidamente)
- **Test F e BIC scelgono il grado 3**, l'**AIC** (meno severo) il **grado 4**. Ma $\Delta AIC = 0.79$ e $\Delta BIC = 1.12$ sono piccole: i due modelli sono di fatto **equivalenti** e per parsimonia si preferisce il **grado 3**
- Ricalcolati AIC, BIC e F dalla colonna RSS: tutti corretti. Nel test F il denominatore usa $n - p_1$ con $p_1 = k - 1$ (coefficienti senza $\sigma^2$), coerente con la slide 31; il valore esatto della soglia è $F_{0.95}(1, 45) = 4.057$

### Regolarizzazione: Ridge e Lasso (slide 43)
Invece di scegliere un sottoinsieme discreto di variabili si **penalizza la norma** dei coefficienti:
- **Ridge** (Tikhonov):
$$\min_\beta\|\mathbf{y} - \mathbf{X}\beta\|^2 + \lambda\|\beta\|_2^2 \quad \Rightarrow \quad \hat{\beta} = (\mathbf{X}^T\mathbf{X} + \lambda\mathbf{I})^{-1}\mathbf{X}^T\mathbf{y}$$
  matrice **sempre invertibile**: utile con variabili molto **correlate**; coefficienti **ridotti ma non annullati**
- **Lasso**:
$$\min_\beta\|\mathbf{y} - \mathbf{X}\beta\|^2 + \lambda\|\beta\|_1$$
  molti coefficienti diventano **esattamente zero**: **selezione automatica** delle variabili; **niente forma chiusa** (si risolve con **coordinate descent**)
- **Elastic Net**: combinazione delle due penalità
- L'**intercetta non si penalizza** e le variabili vanno **standardizzate**; $\lambda$ si sceglie con **cross-validation**

### Selezione stepwise forward (slide 44-45)
Il **best subset selection** valuta $2^d$ modelli; alternativa **greedy**:

```
Input: dataset (X, y), variabili candidate V = {x1, ..., xd}, criterio C (es. BIC)
Output: insieme S di variabili selezionate
 1: S ← ∅
 2: best ← C(modello con sola intercetta)
 3: ripeti
 4:   per ogni v ∈ V \ S:
 5:     stima il modello con variabili S ∪ {v} e calcola C_v
 6:   v* ← argmin_v C_v
 7:   se C_v* < best:
 8:     S ← S ∪ {v*}; best ← C_v*
 9:   altrimenti:
10:     restituisci S
11: finché S = V
12: restituisci S
```

- È un **hill climbing** nello spazio dei sottoinsiemi di variabili con funzione obiettivo $C$: al più $O(d^2)$ modelli stimati invece di $2^d$
- Come ogni ricerca locale può fermarsi in un **ottimo locale**
- Varianti:
  - **backward elimination**: parte dal modello completo e toglie una variabile alla volta (richiede $n > p$)
  - **bidirezionale**: a ogni passo valuta sia inserimenti sia rimozioni
  - criterio sul **p-value del test F parziale** (soglie $\alpha_{in}, \alpha_{out}$) invece che AIC/BIC
- **Attenzione**: i p-value del modello finale sono **ottimistici**, perché le variabili sono state scelte guardando gli stessi dati: va validato su un **test set indipendente**
- Con variabili molto **correlate** la selezione è **instabile** (piccole variazioni dei dati cambiano le variabili scelte): spesso è preferibile il **Lasso**

### Diagnostica dei residui (slide 46)
L'inferenza vale solo se le ipotesi sono (circa) rispettate:
- **residui vs valori predetti**: andamento **curvo** → **non linearità**; dispersione "**a ventaglio**" → **eteroschedasticità** (test di **Breusch-Pagan**)
- **Q-Q plot** dei residui standardizzati → **normalità** (Shapiro-Wilk, $\chi^2$ di adattamento)
- **residui vs ordine/tempo** → **autocorrelazione** (test di **Durbin-Watson**)
- **punti influenti**:
  - **leverage** $h_{ii}$ (diagonale della hat matrix): sospetto se $h_{ii} > 2p/n$
  - **distanza di Cook**: $D_i = \frac{e_i^2}{p\,s^2}\cdot\frac{h_{ii}}{(1 - h_{ii})^2}$, sospetto se $D_i > 4/n$
- **Rimedi**: trasformazioni di $y$ (logaritmo, **Box-Cox**), termini polinomiali, **minimi quadrati pesati**, **regressione robusta**

### Multicollinearità (slide 47)
Variabili indipendenti fortemente correlate → $\mathbf{X}^T\mathbf{X}$ **quasi singolare**:
- $SE(\hat{\beta}_j)$ molto grandi e coefficienti **instabili** (anche con **segno controintuitivo**)
- test F globale significativo ma **nessun test t** significativo
- le **predizioni possono restare buone**: il problema riguarda soprattutto l'**interpretazione** dei coefficienti
- **Variance Inflation Factor**:
$$VIF_j = \frac{1}{1 - R_j^2}$$
  con $R_j^2$ = $R^2$ della regressione di $x_j$ su tutte le altre variabili indipendenti; $SE(\hat{\beta}_j)$ cresce di un fattore $\sqrt{VIF_j}$; valori **oltre 5-10** indicano un problema
- **Rimedi**: rimuovere o aggregare variabili, regressione sulle **componenti principali** (PCA), **Ridge**

### Riepilogo inferenza e selezione (slide 48)
- Con errori gaussiani omoschedastici: least square = **massima verosimiglianza**, e $\hat{\beta}$, $s^2$ hanno distribuzioni note ($N$, $\chi^2$)
- **test t**: il singolo coefficiente è significativo? → intervalli di confidenza
- **ANOVA / test F**: il modello (o un gruppo di variabili) spiega una parte significativa della varianza? ANOVA sui gruppi = regressione su variabili dummy
- **test $\chi^2$**: variabili categoriche (adattamento, indipendenza), likelihood ratio test per modelli annidati
- **$R^2_{adj}$, AIC, BIC, cross-validation**: confronto fra modelli di diversa complessità; **BIC penalizza di più** e sceglie modelli più semplici
- **stepwise** (ricerca greedy) o **regolarizzazione** (Lasso) quando le variabili candidate sono molte
- verificare **sempre** le ipotesi con la **diagnostica dei residui**

## Regressione non lineare - dipendenza nota (slide 49-53)
- Se il modello dipende in modo **non lineare dai parametri** non c'è soluzione least square in **forma chiusa**
- Esempio dalla biologia (reazione mediata da enzimi, **Michaelis-Menten**):
$$y = \frac{\beta_1 \cdot x}{\beta_2 + x}$$
- Con dipendenza **nota** si usano tecniche iterative di **ottimizzazione numerica**:
  - **Gradient Descent**: metodo del **primo ordine**, passi in direzione **contraria al gradiente**
  - **Gauss-Newton**: il più noto e usato; la slide 49 lo chiama metodo "del secondo ordine che richiede stima Hessiana". (Precisazione dalla slide 50: l'Hessiana non si calcola, si **approssima con $2\mathbf{J}^T\mathbf{J}$** usando **solo derivate prime**.)

### Gauss-Newton (slide 50-51)
- Modello $y_i = f(\mathbf{x}_i; \beta) + \varepsilon_i$, residui $r_i(\beta) = y_i - f(\mathbf{x}_i; \beta)$, obiettivo
$$S(\beta) = \sum_{i=1}^{n} r_i(\beta)^2 = \|\mathbf{r}(\beta)\|^2$$
- **Idea**: **linearizzare** $f$ attorno alla stima corrente
$$f(\mathbf{x}_i; \beta + \delta) \approx f(\mathbf{x}_i; \beta) + \mathbf{J}_i\delta, \qquad J_{ij} = \frac{\partial f(\mathbf{x}_i; \beta)}{\partial\beta_j}$$
  con $\mathbf{J}$ ($n \times p$) **Jacobiano**. Il passo $\delta$ risolve un problema di **regressione lineare**:
$$\min_\delta\|\mathbf{r} - \mathbf{J}\delta\|^2 \quad \Rightarrow \quad (\mathbf{J}^T\mathbf{J})\delta = \mathbf{J}^T\mathbf{r}$$
  cioè le **equazioni normali** con $\mathbf{J}$ al posto di $\mathbf{X}$ e $\mathbf{r}$ al posto di $\mathbf{y}$
- L'Hessiana di $S$ è $2(\mathbf{J}^T\mathbf{J} - \sum_i r_i\nabla^2 f_i)$: Gauss-Newton la approssima con $2\mathbf{J}^T\mathbf{J}$; l'approssimazione è buona se i **residui sono piccoli** o $f$ è **quasi lineare**

```
Input: dati (x_i, y_i), modello f, stima iniziale β(0), tolleranza τ
Output: stima β̂
1: β ← β(0)
2: ripeti
3:   r_i ← y_i − f(x_i; β)   per i = 1 ... n
4:   J ← Jacobiano di f in β
5:   risolvi (JᵀJ) δ = Jᵀr   (tramite QR di J)
6:   β ← β + δ
7: finché ||δ|| < τ (||β|| + τ)
8: restituisci β
```

- Ogni iterazione costa quanto una regressione lineare: $O(np^2)$
- Vicino alla soluzione converge **rapidamente**: **quadratica** se i residui all'ottimo sono nulli, **lineare** (ma veloce) se sono piccoli
- Può **divergere** se $\beta^{(0)}$ è lontano dalla soluzione o se $\mathbf{J}^T\mathbf{J}$ è mal condizionata

### Levenberg-Marquardt (slide 52)
- Rende Gauss-Newton **robusto** con uno **smorzamento** $\lambda > 0$:
$$(\mathbf{J}^T\mathbf{J} + \lambda\mathbf{I})\delta = \mathbf{J}^T\mathbf{r}$$
- $\lambda$ **grande**: passo corto nella direzione del gradiente (**gradient descent**); $\lambda$ **piccolo**: **Gauss-Newton**
- Se $S$ diminuisce il passo è **accettato** e $\lambda \leftarrow \lambda/10$, altrimenti è **rifiutato** e $\lambda \leftarrow 10\lambda$
- **Variante di Marquardt**: $\lambda\,\text{diag}(\mathbf{J}^T\mathbf{J})$ al posto di $\lambda\mathbf{I}$, per un passo **invariante rispetto alla scala** dei parametri
- $\mathbf{J}^T\mathbf{J} + \lambda\mathbf{I}$ è **sempre invertibile** (stessa idea della **Ridge**)
- È l'algoritmo di default di `scipy.optimize.curve_fit` (senza vincoli)

### Esempio: Michaelis-Menten (slide 53)
$$f(x; \beta_1, \beta_2) = \frac{\beta_1 x}{\beta_2 + x}, \qquad \frac{\partial f}{\partial\beta_1} = \frac{x}{\beta_2 + x}, \qquad \frac{\partial f}{\partial\beta_2} = -\frac{\beta_1 x}{(\beta_2 + x)^2}$$
- **Stima iniziale**: $\beta_1$ è l'**asintoto** (velocità massima) → $\beta_1^{(0)} \approx \max_i y_i$; $\beta_2$ è il valore di $x$ per cui $y = \beta_1/2$
- In alternativa si **linearizza** il modello (**Lineweaver-Burk**):
$$\frac{1}{y} = \frac{1}{\beta_1} + \frac{\beta_2}{\beta_1}\cdot\frac{1}{x}$$
  e si fa la regressione lineare di $1/y$ su $1/x$. Ma la trasformazione **distorce gli errori** (quelli sui $y$ piccoli vengono amplificati): va bene **solo come punto di partenza** per Gauss-Newton
- A convergenza $s^2(\mathbf{J}^T\mathbf{J})^{-1}$ dà (asintoticamente) gli **errori standard** dei parametri, e si applicano gli stessi **test t** del caso lineare

## Regressione non lineare - dipendenza sconosciuta (slide 54-55)
- Se la dipendenza non è nota (lineare o no), si provano e validano il **modello lineare** (**baseline**) e modelli non lineari via via più complessi
- Varianti per la regressione di tecniche di classificazione (disponibili in scikit-learn):
  - **Random Forest Regressor**
  - **Support Vector Regressor** (SVR): si **inverte** la funzione obiettivo, invece di volere che **nessun** sample cada nella fascia del margine si vuole che ci cada il **maggior numero** di sample del training set. (Aggiunta, non nelle slide: è la loss **$\varepsilon$-insensitive**, nulla per gli errori $|y_i - f(x_i)| \le \varepsilon$ e lineare oltre.)
  - **Gradient Boosting Regressor**
  - anche le **Reti Neurali** addestrate con **error backpropagation**
- **Vantaggi** di un modello non lineare:
  - maggiore **flessibilità** (più gradi di libertà)
  - **controllo della complessità** della soluzione (gradi di libertà, regolarizzazione, ecc.)
  - si possono usare **loss alternative** a MSE (che è implicita nel least square), come **MAE, MAPE**, ecc.

## Regressione ai quantili (slide 56)
- Il modello lineare ai minimi quadrati stima la **media condizionata**: la retta approssima la media dei dati, e gli **errori positivi e negativi pesano allo stesso modo**
- Per dare **peso diverso** a positivi e negativi (es. una **sottostima** è più grave di una **sovrastima**) si usa la **regressione ai quantili** (o percentili):
  - percentile **50%**: si passa dalla **media alla mediana** (metà dei punti del training set sopra la retta, metà sotto)
  - percentile $p$: la retta lascia il $p\%$ dei punti **sotto** e il resto **sopra**. (Errore di notazione nella slide 56: scrive "$1 - (p)\%$ sopra", mescolando frazione e percentuale; è $(100 - p)\%$, oppure $1 - p$ con $p$ in frazione.)
- Si usa una **loss MAE con penalità diversa** per predizioni in eccesso e in difetto. (Aggiunta, non nelle slide: è la **pinball loss** $\rho_\tau(u) = u\,(\tau - \mathbb{1}[u < 0])$ con $u = y_i - \hat{y}_i$ e $\tau \in (0,1)$ il quantile; per $\tau = 0.5$ è metà del valore assoluto, cioè il MAE.)

## Riepilogando (slide 57-58)
Problemi di regressione **piccoli-medi**:
- **modello lineare** (nei parametri) risolto con **least square** (fattorizzazione **SVD**): l'approccio più semplice, una sorta di **baseline**
- modello **non lineare nella variabile indipendente** ma **lineare nei parametri** (es. polinomiale): ottima **seconda scelta**, unisce semplicità e flessibilità
- servono modelli più potenti: **Random Forest Regressor**
- dipendenza **nota** ma **non lineare nei parametri**: ottimizzazione numerica con **Gauss-Newton**, prima scelta

Problemi **grandi** (lineari e non):
- **Gradient Descent** con **Reti Neurali**, preferibile per **trattabilità numerica** e **complessità computazionale**
- Nel **deep learning** reti addestrate con gradient descent risolvono regressioni enormi, es. stima della **posizione di un oggetto** in un'immagine da milioni di esempi (**Faster R-CNN**): variabile indipendente = l'immagine (pixel), variabile dipendente = la **bounding box** (un vettore, quindi **multivariate multiple regression**)

## Da ricordare per lo scritto
- Regressione = $y$ continua; **lineare** significa lineare **nei parametri** (la polinomiale è lineare); $x$ esatta, $y$ con errore
- Retta: $\beta^* = \frac{\sum(x_i - \bar{x})(y_i - \bar{y})}{\sum(x_i - \bar{x})^2}$, $\alpha^* = \bar{y} - \beta^*\bar{x}$; multipla: equazioni normali $\mathbf{X}^T\mathbf{X}\beta = \mathbf{X}^T\mathbf{y}$, $\hat{\beta} = (\mathbf{X}^T\mathbf{X})^{-1}\mathbf{X}^T\mathbf{y}$, in pratica QR o SVD, costo $O(nd^2)$; hat matrix = proiezione ortogonale, residui ortogonali alle colonne di $\mathbf{X}$
- Least square minimizza distanze **verticali** (non simmetrico), PCA quelle **euclidee**
- Metriche: MSE/RMSE (loss implicita), MAE (robusto agli outlier), MAPE (percentuale), $R^2 = 1 - RSS/TSS$ (solo lineare con intercetta, non cala mai aggiungendo variabili → $R^2_{adj}$, che può essere negativo)
- Ipotesi 1-5 → **Gauss-Markov**, least square è **BLUE**; con la normalità (6) least square = **MLE**, $\hat{\beta} \sim N(\beta, \sigma^2(\mathbf{X}^T\mathbf{X})^{-1})$
- $s^2 = RSS/(n-p)$ non distorto, $\hat{\sigma}^2_{ML} = RSS/n$ distorto; RMSE ha $n$ al denominatore
- Test t: $t_j = \hat{\beta}_j/SE(\hat{\beta}_j) \sim t_{n-p}$; rifiuto $\Leftrightarrow$ 0 fuori dall'intervallo di confidenza. Esempio: $\hat{\beta} = 0.812$, $t = 6.88$, $R^2 = 0.888$, $F = 47.34 = t^2$
- p-value **non** è $P(H_0 \text{ vera})$; Bonferroni $\alpha/m$; $t_k^2 = F_{1,k}$; $E[\chi^2_k] = k$, $Var = 2k$
- Intervallo di **predizione** sempre più largo di quello di **confidenza** (c'è il "$1 +$" sotto radice); entrambi si allargano lontano da $\bar{\mathbf{x}}$
- Test F globale $F = \frac{ESS/(p-1)}{RSS/(n-p)}$, a una coda; F parziale solo per modelli **annidati**; F significativo ma nessun t → **multicollinearità** ($VIF_j = 1/(1 - R_j^2)$, problema oltre 5-10)
- ANOVA a una via = regressione con $k - 1$ dummy (dummy variable trap con $k$); $SS_B = ESS$, $SS_W = RSS$; esempio GA: $F = 8.67$, p $\approx 0.005$; post-hoc Tukey/Bonferroni, Friedman se misure ripetute
- $\chi^2$ di Pearson: adattamento ($gdl = k - 1 - m$) e indipendenza ($E_{ij}$ = riga·colonna/N, $gdl = (r-1)(c-1)$), serve $E_i \ge 5$; esempio piano/dispositivo $\chi^2 = 3.19$, non si rifiuta. LR test $-2(\ell_0 - \ell_1) \sim \chi^2$ (Wilks)
- $AIC = 2k - 2\ell_{max}$, $BIC = k\ln n - 2\ell_{max}$, si minimizzano; BIC più severo per $n \ge 8$ e consistente, AIC orientato alla predizione (~ LOO-CV); $B_{10} \approx \exp(-\Delta BIC/2)$, Kass & Raftery 2/6/10. Esempio polinomio: F e BIC → grado 3, AIC → grado 4
- Ridge ($\ell_2$, forma chiusa, sempre invertibile, riduce) vs Lasso ($\ell_1$, azzera, coordinate descent); intercetta non penalizzata, variabili standardizzate, $\lambda$ con CV
- Stepwise forward = hill climbing, $O(d^2)$ modelli invece di $2^d$, ottimi locali, p-value finali ottimistici
- Diagnostica: ventaglio = eteroschedasticità (Breusch-Pagan), Q-Q plot (Shapiro-Wilk), Durbin-Watson, leverage $> 2p/n$, Cook $> 4/n$
- Non lineare nei parametri: Gauss-Newton ($\mathbf{J}^T\mathbf{J}\delta = \mathbf{J}^T\mathbf{r}$, Hessiana $\approx 2\mathbf{J}^T\mathbf{J}$, $O(np^2)$ a iterazione, può divergere); Levenberg-Marquardt ($+\lambda\mathbf{I}$, $\lambda/10$ se accetta, $10\lambda$ se rifiuta, default di `curve_fit`); Michaelis-Menten con start da Lineweaver-Burk
- Quantili: media → mediana a 50%, loss MAE asimmetrica; SVR = più punti possibili **dentro** la fascia
- Scelta: lineare (baseline) → polinomiale → Random Forest Regressor; Gauss-Newton se la forma è nota; reti neurali + gradient descent per problemi grandi
