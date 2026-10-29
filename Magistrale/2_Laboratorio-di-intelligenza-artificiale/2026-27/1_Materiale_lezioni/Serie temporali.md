# Regressione e analisi di serie temporali

Fonte: `Serie temporali.pdf`

## Che cos'è una serie temporale
- In statistica descrittiva una **serie storica** (o **temporale**) è un **insieme di variabili casuali (stocastiche) ordinate rispetto al tempo**: esprime la dinamica di un fenomeno nel tempo
- Si studia per due scopi:
  - **interpretare** il fenomeno, individuando le componenti di **trend**, **ciclicità**, **stagionalità** e/o **accidentalità**
  - **prevedere** il suo andamento futuro
- Figura: PIL trimestrale a valori concatenati (anno di riferimento 2000, dati grezzi), dal 1980 a oltre il 2005: **trend crescente** con un'oscillazione **stagionale** regolare sovrapposta

### Deterministiche e stocastiche
- **deterministica**: i valori si possono determinare **esattamente** dai valori precedenti
- **stocastica**: i valori si possono determinare dai precedenti **solo in parte**
- La maggior parte delle serie reali è stocastica: è **impossibile** fare previsioni **prive di errore**

### Approccio classico e approccio moderno
- **Classico**: si assume il modello
  $$Y_t = f(t) + u_t$$
  - $f(t)$ è una sequenza **deterministica**, la **parte sistematica**; $u_t$ è una successione di variabili aleatorie, la **parte stocastica**
  - la parte deterministica si scompone in componenti **tendenziali, cicliche e/o stagionali**; la differenza fra il modello deterministico e i dati osservati è una **componente casuale residua**
- **Moderno**: si suppone che la parte sistematica **manchi** (o sia stata **eliminata** dai dati) e ci si concentra sulla **parte stocastica**, assumendo che i dati siano generati da un processo stocastico descritto da un **modello probabilistico parametrico** (regressione lineare multipla, cioè i modelli AR, MA, ARMA visti più avanti)

### Momenti fondamentali
- **media**: $\mu_t = E[Y_t]$
- **varianza**: $\sigma_t^2 = E[(Y_t - \mu_t)^2]$
- **autocovarianza** (covarianza del processo con se stesso fra coppie di istanti): $\gamma_{t,s} = E[(Y_t - \mu_t)(Y_s - \mu_s)]$
- (Aggiunta, non nelle slide: l'**autocorrelazione** è l'autocovarianza normalizzata, $\rho_{t,s} = \frac{\gamma_{t,s}}{\sigma_t \sigma_s} \in [-1, 1]$; per una serie stazionaria dipende solo dal ritardo $k = |t - s|$ e si scrive $\rho_k = \gamma_k / \gamma_0$. È la quantità disegnata dall'ACF.)

## Componenti di una serie
- **Tendenziale (trend)**: andamento crescente, decrescente o costante, con fluttuazioni più o meno regolari. Per stimarlo si usano soprattutto il **metodo dei minimi quadrati** e il **metodo delle medie mobili**
- **Ciclica**: fluttuazioni periodiche o non periodiche **attorno alla curva del trend**, di durata **pluriennale** (componenti **congiunturali**), con le quattro fasi del ciclo economico:
  - **prosperità**: aumento maggiore dell'aumento dell'anno precedente
  - **recessione**: aumento minore dell'aumento dell'anno precedente
  - **crisi**: aumento negativo maggiore di quello dell'anno precedente
  - **ripresa**: aumento negativo minore di quello dell'anno precedente
- **Stagionale**: variazioni che si ripetono **negli stessi mesi** in anni successivi; si analizzano con il metodo della **serie ideale di 12 mesi** e con la **media mobile di 12 mesi**
- **Casuale o accidentale**: piccole oscillazioni dovute a eventi casuali (scioperi, elezioni, fatti importanti)
- **Occasionale**: rara, dovuta a guerre, grandi innovazioni tecnologiche, crisi politiche, ecc.
  - se l'effetto **si smorza rapidamente** e non cambia il trend, il dato si esclude e si sostituisce con un dato "fittizio" ottenuto per **interpolazione**
  - se il trend **resta cambiato**, si **spezza la serie in due** e si analizzano separatamente le due parti, dette **periodi osservazionali**

### Caratteristiche delle componenti
Slide 8, in testo:
- **Trend**: senza intervallo fisso, una linea continua nel tempo; tendenza **positiva, negativa o nulla**
- **Stagionalità**: intervallo **regolare e fisso**; forma a campana o a dente di sega
- **Ciclico**: **nessun intervallo fisso**, movimento incerto
- **Irregolarità**: eventi imprevisti e picchi in un breve lasso di tempo

Slide 9, tabella:

| | Trend | Stagionalità | Ciclico | Irregolarità |
|---|---|---|---|---|
| Intervallo | fisso | fisso | non fisso | non fisso |
| Durata | lunga e breve | breve | lunga e breve | regolare/irregolare |
| Natura I | graduale | oscillazioni su e giù | su e giù ripetuti | errori o forti fluttuazioni |
| Natura II | trend su/giù | schema che si ripete | nessun periodo fisso | breve e non ripetibile |
| Prevedibilità | prevedibile | prevedibile | difficile | difficile |
| Esempio di mercato | (foto di un mercato agricolo) | (foto di un negozio affollato) | (ciclo economico) | eventi molto casuali o imprevisti, con rumore bianco |

(Osservazione: per il trend la slide 8 dice "non esiste un intervallo fisso", la tabella della slide 9 "Fixed Time Interval". Ha più senso la slide 8: il trend non ha periodo.)

## Obiettivi e passi dell'analisi
Obiettivi:
- capire come funziona la serie e quali fattori influenzano una o più variabili in momenti diversi
- ricavare informazioni dettagliate su come le caratteristiche del dataset cambiano nel tempo
- supportare la **previsione** dei valori futuri
- **presupposto**: un'unica ipotesi di **stazionarietà**, cioè l'origine dei tempi non influisce sulle proprietà statistiche del processo

Passi principali:
1. raccolta e pulizia dei dati
2. visualizzazione rispetto al tempo e alla caratteristica chiave
3. osservazione e analisi della **stazionarietà**
4. grafici per capirne la natura (ACF, PACF)
5. costruzione dei modelli: **AR, MA, ARMA, ARIMA**
6. estrazione di conoscenza dalla previsione

Figura riassuntiva (slide 29, "Timeseries Analysis - Process flow"): (1) individuare le componenti (trend, stagionalità, irregolare, ciclica) → (2) verificare la stazionarietà con ADF e KPSS → (3) renderla stazionaria con detrending, differencing, transformation → (4) ACF e PACF come lavoro preliminare per AR/MA → (5) ARMA → (6) AR + I + MA, cioè ARIMA, con il grafico previsione contro valori reali.

## Stazionarietà
- Un **processo stazionario** è un processo stocastico la cui **distribuzione congiunta non cambia** se traslata nel tempo; quindi anche media e varianza, se esistono, non cambiano nel tempo
- Un dataset stazionario deve rispettare:
  - **media costante** nel tempo
  - **varianza costante** rispetto all'orizzonte temporale
  - la **covarianza** (la slide dice solo che "misura la relazione tra due variabili")
- (Precisazione: la definizione con la distribuzione congiunta è la stazionarietà **in senso forte**. Le tre regole sono quella **in senso debole**, e la terza va letta così: l'autocovarianza $\gamma_{t,s}$ dipende **solo dal ritardo** $|t - s|$, non dall'istante $t$.)
- La causa più comune di non stazionarietà sono le **tendenze nella media**
- Poiché la stazionarietà è un presupposto, i dati non stazionari si **trasformano** per renderli stazionari
- Figura (slide 13), stazionario contro non stazionario:

| | Media | Varianza | Covarianza |
|---|---|---|---|
| Stazionario | costante nel tempo | costante nel tempo | indipendente dal tempo |
| Non stazionario | cresce nel tempo | varia nel tempo | al crescere del tempo le oscillazioni si infittiscono |

### Test statistici
- **Augmented Dickey-Fuller (ADF)**: ipotesi nulla **serie non stazionaria** (radice unitaria), alternativa **serie stazionaria**
- **Kwiatkowski-Phillips-Schmidt-Shin (KPSS)**: ipotesi nulla **serie stazionaria attorno a un trend deterministico**, alternativa **radice unitaria**
- (Aggiunta, non nelle slide: le ipotesi nulle sono **opposte**, quindi si leggono così, con soglia 0,05.)

| ADF p-value | KPSS p-value | Conclusione |
|---|---|---|
| < 0,05 | > 0,05 | stazionaria |
| > 0,05 | < 0,05 | non stazionaria (radice unitaria): differenziare |
| > 0,05 | > 0,05 | trend-stazionaria: togliere il trend |
| < 0,05 | < 0,05 | stazionaria alle differenze: differenziare |

(Aggiunta, verificata con statsmodels 0.15 su 500 punti simulati: AR(1) con $\phi = 0{,}7$ dà ADF $p = 0{,}000$ e KPSS $p = 0{,}100$, stazionaria; una random walk dà ADF $p = 0{,}725$ e KPSS $p = 0{,}010$, non stazionaria; le sue differenze tornano ADF $p = 0{,}000$, KPSS $p = 0{,}100$. KPSS restituisce p-value interpolati da una tabella e **troncati** fra 0,01 e 0,1, con un warning. In `kpss` il default è `regression="c"`, stazionarietà attorno a una costante; per il test attorno a un trend descritto nella slide serve `regression="ct"`.)

## Da non stazionaria a stazionaria
Tre metodi: **detrending**, **differencing**, **transformation**.

### Detrending
- Si **rimuove il trend** e si guardano solo le **differenze** dei valori rispetto al trend. La slide dice che "permette sempre di identificare gli schemi ciclici"
- Figura: variabile $y_t$ con trend lineare crescente e oscillazione → variabile senza trend che oscilla attorno a zero, con la formula $\hat\varepsilon_t = y_t - \hat\mu + \beta t$
- **Errore nella slide 15**: il segno del trend è sbagliato. Con il trend lineare stimato $\hat\mu + \hat\beta t$ il residuo è
  $$\hat\varepsilon_t = y_t - \hat\mu - \hat\beta t$$
  (Verificato: su una serie simulata $y_t = 2 + 0{,}05\,t + \varepsilon_t$ i minimi quadrati danno $\hat\mu = 2{,}016$, $\hat\beta = 0{,}0498$ e il residuo $y_t - \hat\mu - \hat\beta t$ ha media 0.)
- (Precisazione su "sempre": togliere il trend rende stazionaria solo una serie **trend-stazionaria**; se c'è una radice unitaria, come nella random walk, il detrending non basta e serve il differencing.)

### Differencing
- Trasforma la serie in una **nuova serie** per **togliere la dipendenza dal tempo** e **stabilizzare la media**, riducendo trend e stagionalità. La slide scrive $Y_t = Y_t - Y_{t-1}$
- **Errore nella slide 16** (di notazione): la serie differenziata è una variabile nuova,
  $$Y'_t = \nabla Y_t = Y_t - Y_{t-1}$$
  e ha un elemento in meno. (Aggiunta, non nelle slide: la differenza **stagionale** con periodo $m$ è $Y_t - Y_{t-m}$, es. $m = 12$ per dati mensili; in pandas `y.diff()` e `y.diff(12)`, con il primo valore `NaN` da togliere con `dropna()`.)
- Figura, processi non stazionari:
  - $Y_t = \alpha + Y_{t-1} + \beta t + \varepsilon_t$ (random walk con deriva e trend)
  - $Y_t = \alpha + Y_{t-1} + \varepsilon_t$ (random walk con deriva)
  - $Y_t = \alpha + \beta t + \varepsilon_t$ (trend deterministico)
  - $Y_t = Y_{t-1} + \varepsilon_t$ (random walk)
  - $\varepsilon_t \sim N(0, \sigma^2)$ (rumore bianco, già stazionario, per confronto)
- Il **differencing** rende stazionaria la random walk con deriva: $Y_t - Y_{t-1} = \alpha + \varepsilon_t$ (**difference stationary**)
- Il **detrending** rende stazionario il trend deterministico: $Y_t - \beta t = \alpha + \varepsilon_t$ (**trend stationary**)

### Transformation
- Tre metodi: **power transform**, **radice quadrata**, **logaritmo**; il più usato è il logaritmo (la slide scrive "Log Transfer", è *log transform*)
- Figura: serie mensile 2004-2017 con oscillazioni stagionali la cui **ampiezza cresce** nel tempo; dopo `log` e dopo `sqrt` l'ampiezza diventa molto più uniforme
- (Aggiunta, non nelle slide: le trasformazioni servono a **stabilizzare la varianza**, non la media, quindi di solito si combinano con il differencing, es. `np.log(y).diff()`. Il logaritmo richiede valori **positivi**. La power transform generale è Box-Cox, `scipy.stats.boxcox`.)

## Medie mobili (Moving Average, rolling mean)
- Metodo molto usato, efficace con **variazioni casuali di breve periodo**: la media mobile è la media dei dati **entro $k$ periodi**
- Tre tipi: **SMA** (semplice), **CMA** (cumulativa), **EMA** (esponenziale)
- (Attenzione: queste medie mobili sono **smoothing**, non il modello **MA(q)** usato in ARMA/ARIMA, che è una combinazione lineare degli **errori** passati.)

### Simple Moving Average (SMA)
- Media **non ponderata** dei **precedenti $M$ punti**, su una finestra scorrevole
- Aumentando $M$ si **attenua** di più il rumore, a scapito dell'**accuratezza** (la media reagisce più lentamente)
- La slide scrive $SMA_t = \frac{x_t + x_{t-1} + \dots + x_{M-(t-1)}}{M}$. **Errore nella slide 19**: l'ultimo termine ha gli indici scambiati, la finestra di $M$ punti finisce in $x_{t-(M-1)}$:
  $$SMA_t = \frac{x_t + x_{t-1} + \dots + x_{t-M+1}}{M} = \frac{1}{M}\sum_{i=0}^{M-1} x_{t-i}$$
- Figura: temperatura media annua di una città (circa 1780-2020) con SMA a 10 e a 20 anni; quella a 20 anni è più liscia
- In pandas: `DataFrame.rolling(window=M).mean()`

### Cumulative Moving Average (CMA)
- Media **non ponderata** di **tutti** i valori passati fino all'istante corrente:
  $$CMA_t = \frac{x_1 + x_2 + \dots + x_t}{t}$$
- Figura: stessa serie di temperature; la CMA è quasi piatta e sale solo lentamente alla fine, perché ogni nuovo valore pesa $1/t$
- In pandas: `DataFrame.expanding().mean()`

### Exponential Moving Average (EMA)
- Serve soprattutto a individuare le **tendenze** e a **filtrare il rumore**
- Il peso degli elementi **diminuisce gradualmente** andando indietro nel tempo: rispetto alla SMA l'EMA **cambia più in fretta** ed è **più sensibile**
  $$EMA_t = \begin{cases} x_0 & t = 0 \\ \alpha x_t + (1 - \alpha)\,EMA_{t-1} & t > 0 \end{cases}$$
  con $\alpha \in (0, 1)$ **fattore di smoothing**, il peso del periodo più recente
- La slide dice che dà peso "ai punti recenti, non a quelli storici". (Precisazione: li pesa **tutti**, ma con peso decrescente. Svolgendo la ricorsione, $EMA_t = \alpha \sum_{k=0}^{t-1} (1-\alpha)^k x_{t-k} + (1-\alpha)^t x_0$.)
- Figura: temperature con EMA $\alpha = 0{,}1$ (più liscia, rossa) ed EMA $\alpha = 0{,}3$ (segue di più i dati, gialla): $\alpha$ piccolo = più smoothing
- In pandas: `DataFrame.ewm(alpha=...).mean()`
- (Aggiunta, verificata con pandas 3.1: **la formula ricorsiva della slide corrisponde a `ewm(alpha=a, adjust=False)`**. Il default `adjust=True` normalizza i pesi sui soli punti disponibili e all'inizio dà valori diversi.)

Esempio ricalcolato (aggiunta), $x = 1, 2, 3, 4, 5, 6$:

| $t$ | 0 | 1 | 2 | 3 | 4 | 5 |
|---|---|---|---|---|---|---|
| $x_t$ | 1 | 2 | 3 | 4 | 5 | 6 |
| SMA, $M = 3$ (`rolling(3)`) | NaN | NaN | 2 | 3 | 4 | 5 |
| CMA (`expanding()`) | 1 | 1,5 | 2 | 2,5 | 3 | 3,5 |
| EMA, $\alpha = 0{,}5$, formula della slide = `adjust=False` | 1 | 1,5 | 2,25 | 3,125 | 4,0625 | 5,03125 |
| `ewm(alpha=0.5)` default | 1 | 1,667 | 2,429 | 3,267 | 4,161 | 5,095 |

Ad esempio $EMA_2 = 0{,}5 \cdot 3 + 0{,}5 \cdot 1{,}5 = 2{,}25$. Si vede anche il **ritardo** delle medie su un trend: la SMA a 3 resta 1 sotto il dato.

## Autocorrelazione
### ACF (Auto-Correlation Function)
- Indica **quanto un valore della serie è simile ai precedenti**: misura la somiglianza fra la serie e la sua **versione ritardata** (lag) a diversi intervalli
- Serve a individuare le tendenze e l'**influenza dei valori passati** su quelli attuali
- In statsmodels: `statsmodels.tsa.stattools.acf` per calcolarla, `statsmodels.graphics.tsaplots.plot_acf` per disegnarla

### PACF (Partial Auto-Correlation Function)
- Simile all'ACF ma più difficile da capire: è la correlazione della serie con se stessa a un certo ritardo $k$ considerando **solo l'effetto diretto**, cioè **togliendo gli effetti dei ritardi intermedi** $1, \dots, k-1$
- Figura "Auto-correlation and Partial Auto-Correlation": due correlogrammi delle temperature, entrambi partono da circa 0,65 al lag 1 e **decrescono lentamente**, restando sopra la banda di confidenza per molti lag
- Commento della slide: la temperatura precedente influenza quella attuale, ma l'influenza **diminuisce** al crescere del ritardo, con leggeri **aumenti** a intervalli regolari
- (Osservazione sulla figura: il pannello di destra non si comporta da PACF. La PACF al lag 2 si ricava dall'ACF come $\frac{\rho_2 - \rho_1^2}{1 - \rho_1^2}$: con $\rho_1 \approx 0{,}65$ e $\rho_2 \approx 0{,}62$, letti dal grafico, vale circa 0,34, mentre il pannello mostra circa 0,6. Inoltre la serie delle temperature ha un trend, quindi non è stazionaria, e il decadimento lento dell'ACF è proprio il segnale di non stazionarietà; la slide 25 ricorda che ACF e PACF richiedono serie stazionarie.)
- In statsmodels: `statsmodels.tsa.stattools.pacf` e `statsmodels.graphics.tsaplots.plot_pacf` (aggiunta, la slide nomina solo quelle dell'ACF)

### Scelta del modello dai correlogrammi
Figure: **autocorrelazione positiva** (punti consecutivi vicini, andamento a onda lenta), **autocorrelazione negativa** (punti che saltano alternativamente sopra e sotto), un'ACF **forte** (barre vicine a 1 per 35 lag) e uno scatter $y(t+1)$ contro $y(t)$ etichettato "weak autocorrelation" (anche se la nube è chiaramente allineata).

| ACF | PACF | Modello |
|---|---|---|
| decresce gradualmente | si azzera subito | **AR** |
| si azzera subito | decresce gradualmente | **MA** |
| decresce gradualmente | decresce gradualmente | **ARMA** |
| si azzera subito | si azzera subito | nessun modello (rumore) |

- **ACF e PACF richiedono serie stazionarie**
- (Aggiunta, non nelle slide: il lag a cui la PACF si azzera dà l'ordine $p$ di AR($p$), quello a cui si azzera l'ACF l'ordine $q$ di MA($q$). Verificato su 500 punti simulati: AR(1) con $\phi = 0{,}7$ ha ACF $0{,}68, 0{,}46, 0{,}30, 0{,}22$, che decresce, e PACF $0{,}68, 0{,}00, -0{,}03, 0{,}06$, che si azzera dopo il lag 1; MA(1) con $\theta = 0{,}8$ ha ACF $0{,}48, -0{,}04, -0{,}06$, che si azzera dopo il lag 1 (teoria: $\theta/(1+\theta^2) = 0{,}488$), e PACF $0{,}48, -0{,}35, 0{,}20, -0{,}14$, che decresce oscillando.)

## Modelli
### AR (auto-regressivo)
- Modello semplice che **prevede il futuro dai valori passati**; si usa quando c'è correlazione fra i valori della serie e quelli che li precedono. (La slide aggiunge "e si succedono (avanti e indietro)", ma il modello usa solo i valori **passati**.)
- È una **regressione lineare** con le **variabili ritardate** come input:
  $$Y_t = C + b_1 Y_{t-1} + b_2 Y_{t-2} + \dots + b_p Y_{t-p} + \varepsilon_t$$
  con $p$ il numero di valori passati (ordine), $C$ l'intercetta, $\varepsilon_t$ l'errore al tempo corrente (la slide lo scrive $Er_t$)
- Si può costruire con **scikit-learn** preparando a mano gli input ritardati, oppure con **statsmodels**, che ha funzioni specifiche per l'autoregressione in cui basta indicare il ritardo e addestrare
- (Aggiunta, verificata: su un AR(1) simulato `AutoReg(y, lags=2).fit().params` e `LinearRegression` sulle colonne `shift(1)`, `shift(2)` danno gli **stessi coefficienti**, $C = -0{,}029$, $b_1 = 0{,}679$, $b_2 = 0{,}001$: AR è davvero una regressione lineare sui lag.)

```python
import pandas as pd
from sklearn.linear_model import LinearRegression
from statsmodels.tsa.ar_model import AutoReg

df = pd.DataFrame({"y": y})
for k in (1, 2):
    df[f"lag{k}"] = df["y"].shift(k)
df = df.dropna()
lr = LinearRegression().fit(df[["lag1", "lag2"]], df["y"])

ar = AutoReg(y, lags=2).fit()
```

### ARMA e ARIMA
- **ARMA** combina **auto-regressivo** e **media mobile**: descrive un processo stocastico **debolmente stazionario** con due polinomi, uno per la parte AR e uno per la parte MA. Formula della slide:
  $$Y_t = \mu + \underbrace{\sum_{i=1}^{q} \gamma_i Y_{t-i}}_{\text{AR}} + \varepsilon_t + \underbrace{\sum_{i=1}^{q} \theta_i \varepsilon_{t-i}}_{\text{MA}}$$
- (Precisazione: le due somme hanno ordini **indipendenti**, $p$ per la parte AR e $q$ per la parte MA; la slide le scrive entrambe fino a $q$. ARMA($p$, $q$): $Y_t = \mu + \sum_{i=1}^{p} \gamma_i Y_{t-i} + \varepsilon_t + \sum_{i=1}^{q} \theta_i \varepsilon_{t-i}$.)
- ARMA va bene per serie **stazionarie** ma non per quelle **non stazionarie**: per questo nasce **AR-I-MA**, che gestisce entrambe
  - **AR**: usa i **valori passati** per prevedere il futuro
  - **MA**: usa gli **errori passati**
  - **I** (integrated): **differenzia** le osservazioni per renderle stazionarie
- (Aggiunta, non nelle slide: ARIMA($p$, $d$, $q$) è un ARMA($p$, $q$) applicato alla serie differenziata $d$ volte. Con $d = 1$ si modella $Y_t - Y_{t-1}$.)
- La slide indica in Python `statsmodels.tsa.arima_model`. **Errore nella slide 27** (codice obsoleto): in statsmodels 0.15 il modulo esiste ancora ma istanziare `arima_model.ARIMA` o `arima_model.ARMA` solleva `NotImplementedError` ("have been removed in favor of statsmodels.tsa.arima.model.ARIMA"). La classe da usare è `statsmodels.tsa.arima.model.ARIMA`; per l'ARMA basta `order=(p, 0, q)`
- Figura (slide 28): previsione ARIMA (blu) contro temperatura media annua reale (verde), 1980-2020: la previsione segue il trend crescente ma è **molto più liscia** e non insegue i picchi

### RNN (Recurrent Neural Network)
- L'architettura più tradizionale e accettata per la **previsione** di serie temporali
- Organizzata in livelli successivi: **input**, **nascosto** (intermedio), **output**
- I **pesi sono gli stessi** per ogni passo temporale e ogni neurone corrisponde a un istante; il livello nascosto è connesso a input e output dello stesso passo e viene **inoltrato** al passo successivo, nella direzione del tempo
- Figura: la cella ricorrente compatta ($x \to s \to o$, con il ciclo $W$ su $s$) e la sua versione **srotolata** (unfold) su $t-1, t, t+1$: $U$ collega l'input $x_t$ allo stato $s_t$, $W$ collega $s_{t-1}$ a $s_t$, $V$ collega $s_t$ all'output $o_t$
- Componenti:
  - **input**: il vettore $x(t)$ al passo $t$
  - **nascosto**: il vettore $h(t)$, lo **stato nascosto** al passo $t$, una sorta di **memoria** della rete; si calcola dall'input corrente $x(t)$ e dallo stato precedente $h(t-1)$
  - **output**: il vettore $y(t)$ al passo $t$
  - **pesi**: $U$ da input a nascosto, $W$ fra stati nascosti consecutivi, $V$ da nascosto a output; **$U$, $W$, $V$ sono costanti per ogni passo temporale**. (La slide dice che $W$ "è formata dai neuroni dello strato nascosto del tempo $t-1$ e $t+1$"; precisazione: $W$ collega lo stato al tempo $t-1$ a quello al tempo $t$, e lo stesso $W$ si riusa fra $t$ e $t+1$, come nella figura.)
- (Aggiunta, non nelle slide: le equazioni sono $h_t = \tanh(U x_t + W h_{t-1} + b)$ e $y_t = V h_t + c$, con l'eventuale funzione di output, es. softmax per classificare. L'addestramento è la backpropagation through time.)

**Vantaggi** (slide 32):
- ricorda "ogni informazione", quindi è molto utile per le serie temporali
- adatta a costruire modelli complessi da serie temporali
- **veloce nella previsione**
- non influenzata dai valori mancanti, quindi la pulizia dei dati può essere limitata

**Svantaggi**:
- la grande difficoltà è l'**addestramento**
- **calcolo costoso**

(Precisazione sui vantaggi: una RNN semplice **non** ricorda tutto. Per il problema del **vanishing/exploding gradient** fatica con le dipendenze lunghe, ed è proprio la difficoltà di addestramento elencata fra gli svantaggi; LSTM e GRU nascono per questo. Anche sui valori mancanti la slide è ottimista: una RNN standard vuole un input a ogni passo, quindi i buchi vanno comunque imputati o mascherati.)

## Aggiunta: codice di riferimento
Non nelle slide, solo come riferimento per il progetto e la parte pratica dell'orale. Verificato con pandas 3.1, statsmodels 0.15, scikit-learn 1.9 su una random walk mensile simulata (ADF $p = 0{,}841$, KPSS $p = 0{,}010$; dopo il differencing ADF $p = 0{,}000$).

```python
import pandas as pd
from statsmodels.tsa.stattools import adfuller, kpss, acf, pacf
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf
from statsmodels.tsa.arima.model import ARIMA

p_adf = adfuller(y)[1]
p_kpss = kpss(y, regression="ct")[1]

dy = y.diff().dropna()
plot_acf(dy, lags=30)
plot_pacf(dy, lags=30)

train, test = y[:-12], y[-12:]
res = ARIMA(train, order=(1, 1, 1)).fit()
pred = res.forecast(steps=12)
rmse = ((pred - test) ** 2).mean() ** 0.5
```
- `y` è una `pd.Series` con indice di date (`pd.date_range(..., freq="MS")`): così `forecast` restituisce una serie già indicizzata sulle date future
- lo split train/test va fatto **in ordine temporale**, mai mescolando: niente `train_test_split` con shuffle; per la cross-validation `sklearn.model_selection.TimeSeriesSplit`
- in statsmodels 0.15 `adfuller` dà un `FutureWarning`: dalla 0.16 restituirà un oggetto risultato invece della tupla
- con `ARIMA(..., order=(p, d, q))` la differenziazione la fa il modello: non passare la serie già differenziata se si mette $d = 1$
