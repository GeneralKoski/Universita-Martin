# Preprocessamento dei dati: normalizzazione, feature selection e riduzione della dimensionalità

Fonte: `Riduzione della dimensionalità.pdf` (titolo interno delle slide: *Preprocessamento dei dati*), con il notebook `Notebook - riduzione della dimensionalità.ipynb` integrato argomento per argomento nei riquadri **Dal notebook**.

## Workflow
- Figura 1: ciclo in 5 passi **Get Data → Clean, Prepare & Manipulate Data → Train Model → Test Data → Improve**
- Figura 2 (imbuto, da learnbyinsight.com), con le attività di ogni fase:
  - **Define Problem Statement**: descrizione del problema, scope, fattibilità
  - **Gather Data**: assunzioni, vincoli, dati forniti
  - **Pre-process Data**: data cleanup, **data imputation** (valori mancanti), drop
  - **Analyze Data**: correlazioni, feature importanti, tipo di problema
  - **Prepare Data**: trasformare, **normalizzare**, drop
  - **Evaluate Models**: train/test, classificare/regredire, **feature reduction**
  - **Tune Model**: cross validation, fine tuning dei parametri, analisi dei risultati
  - **Publish**: risolvere, applicare, approfondire

## Data preparation
- **Data cleaning**: preprocessing per ridurre il **rumore** e trattare i **valori mancanti**
- **Feature selection**: rimuovere i dati non rilevanti
- **Data transformation**: generalizzare e **normalizzare** i dati

## Tipi di dato
- **Binarie** ([0,1], presente/assente)
- **Nominali** (rosso, giallo, blu, verde): categorie senza ordine
- **Ordinali** (cattivo, buono, eccellente): categorie con ordine
- **A scala di intervallo** (interval-scaled): misure continue su scala approssimativamente lineare (peso, altezza, temperatura)
- **Di rapporto** (ratio)
- **Tipi misti**
- L'**unità di misura** influenza l'analisi (es. il clustering): passare da kg a libbre può cambiare la struttura dei gruppi
- Per non dipendere dall'unità di misura i dati vanno **normalizzati** o **standardizzati**, così ogni feature ha lo stesso peso/contributo

## Normalizzazione
Figura: case con "anni" (0-100) e "numero di stanze" (0-10). Senza normalizzazione le stanze sono schiacciate sullo zero perché la scala degli anni domina; dopo la **min-max** entrambe le feature stanno in $[0,1]$. Una casa di 100 anni (outlier) comprime tutte le altre in $[0, 0.4]$: la min-max è sensibile agli estremi.

Dato $X = \{x_1, \dots, x_n\}$, $\hat x_i$ è il valore normalizzato di $x_i$.

- **Normalizzazione 0-max**: proietta in $[0,1]$ con 0 = zero assoluto
  $$\hat x_i = \frac{x_i}{\max(X)}$$
  - Problema: valori negativi in $X$. Soluzione: riscalare in $[-1,1]$
  $$\hat x_i = \frac{x_i}{\max(\{|x_i| : x_i \in X\})}$$
- **Normalizzazione min-max**: proietta in $[0,1]$ con 0 = minimo dei dati
  $$\hat x_i = \frac{x_i - \min(X)}{\max(X) - \min(X)}$$
  - Niente più problema dei negativi: $\min(X)$ va sempre su 0
  - Problema: **dipende da $X$**. Se $\min(X) \neq \min(X')$ o $\max(X) \neq \max(X')$, lo stesso valore $x$ presente in entrambi viene mappato su valori diversi
- **Min-max sulla media**: media mappata su 0, valori in $[-1,1]$
  $$\hat x_i = \frac{x_i - \mathrm{media}(X)}{\max(X) - \min(X)}$$
  (Precisazione: i valori cadono in un intervallo di ampiezza 1 che contiene lo 0, quindi sempre dentro $[-1,1]$ ma senza riempirlo.)

## Standardizzazione
- **Deviazione media assoluta** di una variabile $f$ con $n$ valori:
  $$s_f = \frac{1}{n}\left(|x_{1f} - m_f| + |x_{2f} - m_f| + \dots + |x_{nf} - m_f|\right), \qquad m_f = \frac{1}{n}(x_{1f} + \dots + x_{nf})$$
- **z-score**: misura standardizzata, mappa i dati in $(-\infty, +\infty)$
  $$z_{if} = \frac{x_{if} - m_f}{s_f} \qquad \text{o, più comunemente,} \qquad z_i = \frac{x_i - \mu}{\sigma}$$
  con $\mu$ media e $\sigma$ deviazione standard

### Normalizzare e standardizzare (figure)
- **Boxplot** di 4 feature (Item_Weight, Item_Visibility, Item_MRP, Establishment_Year): originali su scale diversissime (Item_MRP fino a ~270, Item_Visibility vicino a 0); **normalizzati** tutti in $[0,1]$; **standardizzati** tutti centrati su 0 con ampiezza simile (circa da -3 a 2)
- Schema: dati originali → dopo la normalizzazione stanno nel quadrato $[0,1]^2$ → dopo la standardizzazione sono centrati sull'origine
- **Curva normale** con le percentuali per fasce di $\sigma$: 34,13% fra 0 e $\pm 1\sigma$, 13,59% fra $1\sigma$ e $2\sigma$, 2,14% fra $2\sigma$ e $3\sigma$, 0,13% oltre $3\sigma$; percentuali cumulative (0,1%, 2,3%, 15,9%, 50%, 84,1%, 97,7%, 99,9%), percentili, **z-score** (da -4 a +4), **T-score** (media 50, 10 punti per $\sigma$: 20...80), **stanine** (9 fasce: 4%, 7%, 12%, 17%, 20%, 17%, 12%, 7%, 4%)

## Curse of dimensionality
- **Maledizione della dimensionalità** (Richard Bellman): il numero di campioni necessari per stimare una funzione arbitraria con una data accuratezza **cresce esponenzialmente** con il numero di variabili di input (dimensionalità)
- Slogan della slide: **#funzioni >> #campioni** (nelle slide "funzioni"/"funzionalità" è la traduzione di *features*: si legge "#feature >> #campioni")
- Troppe feature: l'algoritmo non impara la funzione obiettivo ma "finisce nel vortice delle dimensioni"; le feature in più agiscono come **rumore** e riducono la precisione (come chi spiega qualcosa divagando su cose non pertinenti)
- Figure:
  - Stessa densità di campionamento in **1-D, 2-D, 3-D**: 10 punti su una retta, una griglia 10×10, una nube 3D. Coprire lo spazio con la stessa densità richiede un numero di punti che cresce esponenzialmente
  - **10000 punti da una normale**: distanza dal vicino più prossimo, dal 10° vicino e dal più lontano al crescere delle dimensioni (scala log). Verso $10^3$ dimensioni le tre curve coincidono: *"every point's neighborhood is the same!"*
  - **Cubo unitario** $[0,1]^d$ con dati uniformi: il lato atteso di un sotto-cubo che contiene una frazione $f$ dei dati è $f^{1/d}$ (il volume è $f$, quindi il lato è $f^{1/d}$). Il lato necessario per catturare una data frazione esplode con $d$: con $d=10$ per il 10% del volume serve un lato di circa 0,8

### Curse of dimensionality e overfitting
- L'overfitting si verifica sia stimando relativamente pochi parametri in uno spazio ad alta dimensione, sia stimando molti parametri in uno spazio a bassa dimensione
- La **varianza** della stima di un parametro cresce con il numero di parametri da stimare; a parità di distorsione (bias) e dimensione del training set, la qualità delle stime **diminuisce** all'aumentare della dimensionalità
- Più feature che osservazioni: rischio di overfitting massiccio, prestazioni pessime **fuori campione**
- La crescita esponenziale dello spazio causa **sparsità**: il volume cresce così tanto che i dati non mantengono la loro struttura

### Distanze e ipersfera
- Con troppe dimensioni ogni osservazione appare **equidistante** da tutte le altre: un problema grosso per il clustering e per tutto ciò che usa una distanza (es. euclidea)
- **Frazione di ipercubo occupata dall'ipersfera inscritta**, in $n$ dimensioni:
  $$\frac{\pi^{n/2}}{2^n\,\Gamma\!\left(\frac{n}{2} + 1\right)}$$
  con $\Gamma$ funzione Gamma ($\Gamma(n) = (n-1)!$; precisazione: questa identità vale per $n$ intero, e per $n$ dispari $\frac{n}{2}+1$ non è intero, quindi serve la Gamma generale)
- Tende a **0** per $n$ grande: i dati si concentrano negli **angoli** dell'ipercubo, la sparsità aumenta e la funzione distanza perde significato. (Aggiunta, valori calcolati: $n=2$: 0,785; $n=3$: 0,524; $n=10$: 0,0025.)

### Potenza computazionale
- Con dati ad alta dimensione non si possono campionare tutte le combinazioni: vaste regioni dello spazio delle feature restano **inesplorate**
- Molte dimensioni non garantiscono utilità: spesso si misura lo **stesso pattern** sottostante in modi diversi, quindi molte dimensioni sono **ridondanti**
- **Quante feature usare?** Nessuna regola fissa: dipende da
  - quantità di **dati di training** disponibili
  - **complessità dei confini decisionali**
  - **tipo di classificatore**
- Con infiniti esempi di training la maledizione sparirebbe e si potrebbero usare infinite feature, ma infinite feature richiedono infiniti esempi

### Fenomeno di Hughes
- All'aumentare del numero di feature le prestazioni del classificatore **crescono fino a un numero ottimale**; oltre, a parità di dimensione del training set, **calano**
- Figura: curva "classifier performance" vs "dimensionality" con un picco iniziale e poi un lento decadimento verso 0
- Il numero di dati di training necessari cresce **esponenzialmente** con ogni feature aggiunta

## Soluzione 1: feature selection
- Figura: vantaggi della feature selection: rimuove feature irrilevanti, migliora le prestazioni dei modelli, velocizza il training, modelli più facili da debuggare, da capire e da costruire
- Gli algoritmi si dividono in **supervisionati** (dati etichettati) e **non supervisionati** (dati non etichettati)
- Si classificano in **filter**, **wrapper**, **embedded** (incorporati) e **ibridi**. (Correzione: la slide attribuisce questa classificazione alle sole tecniche non supervisionate e scrive "metodi ibridi (embedded)"; la classificazione vale in generale, soprattutto per i metodi supervisionati, e "embedded" sono i metodi incorporati, non gli ibridi.)
- **Metodi filter**: selezionano le feature in base a **statistiche** anziché alle prestazioni in cross-validation; una metrica identifica gli attributi irrilevanti
  - **univariati**: classifica ordinata delle feature, da cui si sceglie il sottoinsieme finale
  - **multivariati**: valutano la rilevanza delle feature nel loro insieme, individuando quelle **ridondanti** e irrilevanti
- **Metodi wrapper**: la selezione è un **problema di ricerca**; si preparano, valutano e confrontano combinazioni di feature con il modello. Colgono le **interazioni** fra variabili e puntano ai sottoinsiemi che migliorano il risultato dell'algoritmo
- **Metodi embedded**: la selezione fa parte dell'algoritmo di apprendimento, classificazione e selezione avvengono **insieme**. Esempi: importanza delle feature nelle **random forest**, negli **alberi di decisione**, **LASSO**

### Correlazione come criterio dei filter
Si usano misure statistiche di **correlazione** fra input e output. Scelta in base al tipo di variabili (figura ad albero):

| Input | Output | Misura |
|---|---|---|
| Numerico | Numerico | **Pearson**, **Spearman** |
| Numerico | Categoriale | **ANOVA**, **Kendall** |
| Categoriale | Numerico | **ANOVA**, **Kendall** |
| Categoriale | Categoriale | **Chi-quadro**, **Mutual Information** |

(Aggiunta, non nelle slide: in scikit-learn si usano `sklearn.feature_selection.VarianceThreshold`, `SelectKBest` con `f_regression` (Pearson), `f_classif` (ANOVA), `chi2`, `mutual_info_classif`/`mutual_info_regression`; wrapper: `RFE`, `SequentialFeatureSelector`; embedded: `SelectFromModel` su random forest o `Lasso`.)

### Esercizi
Su un dataset di scikit-learn:
- quali feature hanno la **varianza più alta**?
- considerando la varianza conviene **normalizzare**? (Aggiunta: la varianza dipende dalla scala, quindi senza normalizzare vince la feature con l'unità più grande; dopo una standardizzazione invece le varianze valgono tutte 1 e non dicono più nulla, quindi va usata una normalizzazione come la min-max)
- che **dipendenza** c'è fra le feature?
- si può calcolare una dipendenza fra una feature **categoriale** e una **numerica**? (dalla tabella: sì, con ANOVA o Kendall)

## Soluzione 2: riduzione della dimensionalità
- Il modo migliore di addestrare con dati limitati è **ridurre il numero di feature**: lo fa la **dimensionality reduction**
- L'algoritmo individua le **tendenze sottostanti** (**feature latenti**) estraendole dai dati, poi **riscrive (proietta)** ogni dato in un altro sistema in termini di queste feature latenti
- Nel nuovo spazio si possono classificare i punti con misure di distanza

### Panoramica delle tecniche
- **PCA** (Principal Component Analysis, o **trasformata KL**, Karhunen-Loève): **non supervisionata**, mapping **lineare** che preserva al massimo l'informazione dei pattern
- **LDA** (Linear Discriminant Analysis): mapping **lineare** ma **supervisionato**, privilegia le dimensioni che **discriminano** meglio le classi del training set
- **t-SNE** (t-distributed Stochastic Neighbor Embedding): **non lineare** e non supervisionata, pensata per ridurre a **2 o 3 dimensioni** per visualizzare
- **UMAP** (Uniform Manifold Approximation and Projection): simile a t-SNE; da ipotesi sulla distribuzione dei dati modella la varietà (manifold) con una **struttura topologica fuzzy**. (La slide dice che "generalizza nel caso non lineare", ma anche t-SNE è già non lineare: la differenza sta nel fondamento topologico, non nella non linearità.)
- **ICA** (Independent Component Analysis): **lineare**, proietta su componenti **statisticamente indipendenti**
- **LLE** (Locally Linear Embedding; la slide scrive "Local Linear Embedding"): **non lineare**; invece di un mapping globale considera le relazioni fra **gruppi di punti vicini**
- **Kernel PCA**: come PCA ma con mapping **non lineare**, grazie a un "trucco" (il **kernel trick**) simile a quello che porta da SVM lineare a SVM non lineare

### Classificazione di Anowar, Sadaoui, Selim (2021)
*Conceptual and empirical comparison of dimensionality reduction algorithms (PCA, KPCA, LDA, MDS, SVD, LLE, ISOMAP, LE, ICA, t-SNE)*, Computer Science Review 40, 100378. Due classi:
- **Random projection**: proietta su un nuovo spazio con una matrice "random" le cui colonne hanno norma 1 (la radice della somma dei quadrati di ogni colonna è 1). Preserva la **proporzionalità delle distanze**
- **Manifold** (la slide scrive "manyfold"): metodi in genere non lineari, non supervisionati, **basati su grafi**; assumono campionamento denso e dati che giacciono su un **manifold** da "srotolare"

Tabella di confronto (dalle slide):

| Metodo | Obiettivo | Supervisione | Linearità | Dati adatti | Iterativo | Topologia | Parametri | Complessità | Debolezza | Trasformazione |
|---|---|---|---|---|---|---|---|---|---|---|
| PCA | massimizzare la varianza | no | lineare | dati asimmetrici (skewed) | no | random projection | n. componenti | $O(d^2n + n^3)$ | solo proiezione lineare | autodecomposizione |
| LDA | massimizzare la separazione fra classi | sì | lineare | dati distribuiti uniformemente | no | random projection | nessuno | $O(d^2n)$ se $n>d$; $O(d^3)$ se $d>n$ | singolarità delle classi | separabilità con matrici di scatter |
| MDS | preservare le distanze euclidee a coppie | no | non lineare | dati relazionali | sì | manifold | n. componenti, iterazioni | $O(n^3)$ | molto calcolo e memoria per la matrice di dissimilarità | matrice di dissimilarità (euclidea) |
| KPCA | dati linearmente separabili | no | non lineare | dati non lineari | no | manifold | n. componenti, kernel | $O(n^3)$ | training lungo | mapping con kernel |
| SVD | minimizzare l'errore di ricostruzione | no | lineare | dati sparsi | sì | random projection | n. componenti, iterazioni | $O(d^2n + n^3)$ | non adatto a dati non lineari | teorema SVD |
| LLE | preservare proprietà locali | no | non lineare | sparsi e non lineari | sì | manifold | n. componenti, iterazioni, vicini | $O(d\log(c)\,n\log n) + O(dnc^3) + O(kn^2)$ | consuma memoria | grafo di vicinato, pesi di ricostruzione |
| ISOMAP | preservare le distanze geodetiche | no | non lineare | sparsi e rumorosi | no | manifold | n. componenti, vicini | $O(d\log(c)\,n\log n) + O(n^2(c + \log n)) + O(kn^2)$ | instabilità topologica | grafo di vicinato, distanza geodetica |
| LE | preservare le distanze locali | no | non lineare | dati rumorosi | no | manifold | n. componenti, vicini | $O(d\log(c)\,n\log n) + O(dnc^3) + O(kn^2)$ | può produrre grafi di vicinato sconnessi | grafo di vicinato, aggiornamento dei pesi degli archi |
| ICA | massimizzare l'indipendenza statistica | sì (sic) | lineare | statistiche di ordine superiore | sì | random projection | n. componenti, iterazioni, tolleranza | $O(2di(d+1)n)$ | training lungo | distribuzione non gaussiana |
| t-SNE | preservare la struttura locale | no | non lineare | dati numerici | sì | manifold | n. componenti, iterazioni | $O(n^2)$ | produce solo 2 o 3 feature | probabilità condizionate |

(Correzione: la tabella dà ICA come supervisionata; ICA è un metodo **non supervisionato**, non usa etichette.)

## PCA: analisi delle componenti principali
- Spiega la **struttura di correlazione** di un insieme di variabili con un insieme più piccolo di **combinazioni lineari** di esse, le **componenti**
- La variabilità totale delle $m$ variabili è spiegata quasi interamente da $k < m$ combinazioni lineari: le $k$ componenti contengono quasi tanta informazione quanta le $m$ variabili originali

### Definizione
Dato il training set $TS = \{x_i \in \mathbb{R}^d,\ i = 1 \dots n\}$:
$$\bar x = \frac{1}{n}\sum_{i=1}^{n} x_i \qquad \Sigma = \frac{1}{n-1}\sum_{i=1}^{n}(x_i - \bar x)(x_i - \bar x)^t$$
(Correzione: nella slide la covarianza è scritta con $\hat x$ invece di $\bar x$; è il vettore medio.)

- **Vettore medio** $\bar x \in \mathbb{R}^d$, **matrice di covarianza** $\Sigma \in \mathbb{R}^{d \times d}$
- Per un dato $k$ ($0 < k < d$, $k < n$) lo spazio $k$-dimensionale $(S_{\bar x, \Phi_k})$ è definito univocamente dal vettore medio e dalla **matrice di proiezione** $\Phi_k \in \mathbb{R}^{d \times k}$, le cui colonne sono gli **autovettori** di $\Sigma$ dei $k$ **autovalori più grandi**:
  $$\Phi_k = [\phi_{i_1}, \phi_{i_2}, \dots, \phi_{i_k}] \quad \text{con } \lambda_{i_1} \geq \lambda_{i_2} \geq \dots \geq \lambda_{i_k} \geq \dots \geq \lambda_{i_d}$$
  dove $\phi_{i_r}$ è l'autovettore di $\Sigma$ con autovalore $\lambda_{i_r}$
- $\phi_{i_1}$ è la **direzione di massima varianza** del training set; i primi $k$ autovettori sono le **componenti principali**
- Figura: nube di punti ellittica con $\phi_{i_1}$ lungo l'asse maggiore e $\phi_{i_2}$ perpendicolare

### Proiezione e retroproiezione
- **Proiezione**: proiezione geometrica del pattern sull'iperpiano dello spazio PCA. La vera proiezione geometrica avrebbe la stessa dimensione del vettore originale: qui "proiezione" indica il **vettore ridotto** nello spazio PCA. Si calcola come matrice di proiezione trasposta per il pattern meno la media:
  $$y = \Phi_k^t\,(x - \bar x) \in \mathbb{R}^k$$
- **Retroproiezione**: si moltiplica il vettore per la matrice di proiezione e si somma il vettore medio:
  $$x' = \Phi_k\,y + \bar x \in \mathbb{R}^d$$
  Non sposta il vettore, che resta sullo spazio PCA: cambia solo le coordinate, esprimendolo con le $d$ componenti dello spazio originale

### Esempio $2 \mapsto 1$
- Figura: spazio iniziale ($d=2$) con un'ellisse di punti centrata in $\bar x = [\bar x_1, \bar x_2]^t$, assi $\phi_1, \phi_2$ con semiassi $\sqrt{\lambda_1}$ e $\sqrt{\lambda_2}$; un punto $x = [x_1, x_2]^t$ ha proiezioni $y_1, y_2$. Nello "spazio KL" ($k=1$) $\Phi_1 = [\phi_1] \in \mathbb{R}^{2\times 1}$, $y = [y_1] \in \mathbb{R}^1$; la retroproiezione $x'$ giace sull'asse $\phi_1$
- L'ellisse rappresenta la distribuzione del training set; $\phi_1, \phi_2$ sono gli autovettori della covarianza; $\lambda_1, \lambda_2$ sono le **varianze** lungo quegli assi
- Se $\lambda_2$ è piccolo, $x$ si approssima con $x'$ senza perdite significative
- Fra tutte le riduzioni **lineari**, PCA è quella che **preserva al massimo l'informazione** dei vettori originali

### Scelta di $k$
- A volte è obbligata (visualizzazione 2D o 3D)
- Altrimenti si fissa la percentuale $t$ di informazione da preservare (es. $t = 95\%$) e si sceglie il **minimo** $k$ per cui la somma dei $k$ autovalori più grandi sul totale è almeno $t$ (autovalori in ordine decrescente):
  $$k = \arg\min_z \left\{ \frac{\sum_{i=1}^{z}\lambda_i}{\sum_{i=1}^{d}\lambda_i} \geq t \right\}$$
- Gli autovalori sono le varianze lungo gli assi: il rapporto è la **varianza conservata** sulla varianza totale

### Variable factor map
- Figura (**scree plot**): proporzione di varianza per autovalore (rango 1...20) a gomito; la prima componente spiega il 36,9%, le etichette vicino ai punti sono le percentuali **cumulative** (51,7, 60, 65,1, 74,8, ..., 85,5 alla ventesima)
- Con 2 componenti si possono disegnare in 2D i contributi delle feature originali a ogni componente
- Esempio iris: 4 feature (lunghezza e larghezza di sepalo e petalo) compresse in 2 componenti, che mantengono il **97,77%** dell'informazione (92,46% + 5,31%). I quattro vettori mostrano come le 2 componenti spiegano le feature originali. (Correzione: la slide dice componente 1 sull'asse y e componente 2 sull'asse x, ma nella figura la componente 1 è sull'asse x.)
- Coordinate dei vettori nella figura (componente 1, componente 2): sepal length (0,36, 0,66), sepal width (-0,08, 0,73), petal length (0,86, -0,17), petal width (0,36, -0,08). Sono i pesi delle componenti, gli stessi che il notebook stampa con `pca.components_`. Due cerchi di riferimento di raggio 1 e 0,5
- Lettura: la **componente 1** è dominata da **petal length**, la **componente 2** dalle misure del **sepalo**
- Figura (**biplot**, iris in R): punti su PC1/PC2 colorati per specie (setosa separata a sinistra, versicolor e virginica in parte sovrapposte a destra) con le frecce delle 4 feature; Petal.Length e Petal.Width allineate con PC1

### Esercizio
Lanciare PCA sui dataset di scikit-learn ed estrarre l'**importanza** e la **composizione** delle feature: data una componente principale, i pesi delle feature originali in quella componente.

### Dal notebook: PCA su iris
```python
import sklearn
from sklearn import *
from sklearn.decomposition import PCA

iris = sklearn.datasets.load_iris()

pca = PCA(n_components = 2)
pca.fit(iris.data)
irispca = pca.transform(iris.data)      # oppure PCA(...).fit_transform(iris.data)

import matplotlib.pyplot as plt
plt.scatter(irispca[:,0], irispca[:,1], c=iris.target)
```
- `iris.data` è un `ndarray` 150×4; `irispca` è 150×2 (prima riga: $(-2{,}684, 0{,}319)$)
- Scatter 2D: setosa nettamente separata (PC1 circa -3), versicolor e virginica adiacenti con leggera sovrapposizione
- **3 componenti** e grafico 3D con matplotlib e con plotly (`px.scatter_3d(x=..., y=..., z=..., color=iris.target)`, interattivo). (Errore nel notebook: con `ax = fig.add_subplot(111, projection="3d")` chiama poi `plt.scatter(x, y, z, c=...)`; `plt.scatter` è la versione 2D e prende il terzo argomento come **dimensione** dei marker, da cui il `RuntimeWarning: invalid value encountered in sqrt` sulle dimensioni negative. Va usato `ax.scatter(x, y, z, c=...)`.)
- **Varianza spiegata**:
  ```python
  pca.explained_variance_ratio_      # array([0.92461872, 0.05306648, 0.01710261])
  plt.bar([1,2,3], pca.explained_variance_ratio_)
  ```
  Cumulata: 92,46% con 1 componente, 97,77% con 2, 99,48% con 3: con $t = 95\%$ basta $k = 2$
- Docstring di `PCA`: riduzione **lineare** tramite **SVD**; i dati vengono **centrati ma non scalati**; solver LAPACK (SVD completa) o SVD troncata randomizzata (Halko et al. 2009) o ARPACK; non supporta input sparso (per quello c'è `TruncatedSVD`). `n_components`: int, float o `'mle'`; se non impostato si tengono $\min(n\_samples, n\_features)$ componenti; con $0 <$ `n_components` $< 1$ (e `svd_solver='full'`) si sceglie il numero di componenti che spiega quella frazione di varianza, cioè la regola di scelta di $k$ vista sopra
- **Composizione delle componenti** (risposta all'esercizio):
  ```python
  print(pca.components_)
  # [[ 0.36138659 -0.08452251  0.85667061  0.3582892 ]
  #  [ 0.65658877  0.73016143 -0.17337266 -0.07548102]
  #  [-0.58202985  0.59791083  0.07623608  0.54583143]]
  print(iris.feature_names)        # sepal length, sepal width, petal length, petal width (cm)
  print(pca.get_feature_names_out())   # ['pca0' 'pca1' 'pca2']
  ```
  Ogni riga è una componente, ogni colonna il peso di una feature originale. `pca.feature_names_in_` dà `AttributeError`: l'attributo esiste solo se il fit è fatto su un DataFrame con nomi di colonna, non su un array numpy
- **Libreria `pca`** (`pip install pca`), con biplot pronti:
  ```python
  from pca import pca
  model = pca(n_components=0.95)   # componenti che spiegano il 95% della varianza
  model = pca(n_components=2)      # oppure 2 componenti
  results = model.fit_transform(iris.data)
  fig, ax = model.plot()           # varianza spiegata cumulata
  fig, ax = model.scatter()        # PC1 vs PC2
  fig, ax = model.biplot(n_feat=4) # biplot con le 4 feature
  ```
  Il log mostra che calcola anche loadings e **outlier detection** (test di **Hotelling T²** con $\alpha = 0{,}05$ e SPE/DmodX). Grafici: "2 Principal Components explain [97.76%] of the variance" e un biplot con le frecce dei loadings (1: 0,657, 2: 0,730, 3: 0,857, 4: 0,358)
- **Biplot fatto a mano** dopo una standardizzazione (*"in general, it's a good idea to scale the data prior to PCA"*):
  ```python
  from sklearn.preprocessing import StandardScaler
  X = StandardScaler().fit_transform(iris.data)
  pca = PCA()
  x_new = pca.fit_transform(X)

  def myplot(score, coeff, labels=None):
      xs, ys = score[:,0], score[:,1]
      scalex = 1.0/(xs.max() - xs.min())
      scaley = 1.0/(ys.max() - ys.min())
      plt.scatter(xs * scalex, ys * scaley, c = y)
      for i in range(coeff.shape[0]):
          plt.arrow(0, 0, coeff[i,0], coeff[i,1], color = 'r', alpha = 0.5)
          plt.text(coeff[i,0], coeff[i,1], labels[i] if labels else "Var"+str(i+1))

  myplot(x_new[:,0:2], np.transpose(pca.components_[0:2, :]))
  ```
  I punti vengono riscalati in $[-1,1]$ per stare sullo stesso grafico delle frecce (i pesi delle componenti)
- **Frecce dei pesi** senza scalatura: `plt.arrow(0, 0, pca.components_[0][i], pca.components_[1][i])` per ogni feature, cioè la variable factor map delle slide
- **Retroproiezione** con `inverse_transform`:
  ```python
  pca = PCA(n_components = 2).fit(iris.data)
  irispca = pca.transform(iris.data)
  inviris = pca.inverse_transform(irispca)
  print(sum(iris.data - inviris))   # [ 6.39e-14 -5.82e-14 -4.42e-14  4.51e-14]
  ```
  Con `n_components = 4` la ricostruzione è esatta a meno dell'errore di macchina (differenze dell'ordine di $10^{-15}$). (Errore nel notebook: la somma delle differenze vale circa 0 anche con $k=2$ e sembra indicare una ricostruzione senza perdite, ma i residui di PCA hanno **media zero per costruzione**, quindi si annullano sommandoli. Per misurare la perdita serve l'errore quadratico: con $k = 2$ l'errore quadratico medio per campione è circa 0,10, con scarti fino a 0,59 cm, e coincide con la somma degli autovalori scartati ($0{,}078 + 0{,}024$, valori ricalcolati); con $k=4$ è 0.)

## LDA: Linear Discriminant Analysis
- Come PCA si basa su **trasformazioni lineari**, ma invece di massimizzare la varianza complessiva trova i **discriminanti lineari** che **massimizzano la varianza fra le classi** e **minimizzano la varianza dentro la classe**
- Approfondita nel corso di teoria (Algoritmi per l'IA), perché la stessa tecnica serve anche come **classificatore**. (La slide scrive "LAD": è LDA.)

### Dal notebook: LDA su iris
```python
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis

lda = LinearDiscriminantAnalysis()
lda.fit(iris.data, iris.target)          # supervisionata: serve anche y
irislda = lda.transform(iris.data)
plt.scatter(irislda[:,0], irislda[:,1], c=iris.target)
```
- Il risultato ha 2 colonne: le tre specie sono ben separate lungo il primo asse (setosa fra 6 e 10, le altre due a valori negativi)
- `LinearDiscriminantAnalysis(n_components = 3)` dà `ValueError: n_components cannot be larger than min(n_features, n_classes - 1)`: con 3 classi al massimo **2 componenti**
- Varianza spiegata a confronto:
  ```python
  print(lda.explained_variance_ratio_)   # [0.9912126 0.0087874]
  print(pca.explained_variance_ratio_)   # [0.92461872 0.05306648]
  ```
  LDA concentra il 99,1% della separazione fra classi nel primo discriminante
- `lda.coef_` ha forma (n_classi, n_feature) = 3×4. (Precisazione: sono i coefficienti di LDA usata come **classificatore**, una riga per classe, non le direzioni di proiezione; le direzioni usate da `transform` stanno in `lda.scalings_`.)

## Distribuzioni di supporto per t-SNE
- **Gaussiana (normale)**:
  $$f(x) = \frac{1}{\sigma\sqrt{2\pi}}\,e^{-\frac{1}{2}\left(\frac{x-\mu}{\sigma}\right)^2}$$
  con $\mu$ media e $\sigma$ deviazione standard. Figure: densità e funzione cumulativa per $(\mu, \sigma^2) = (0, 0{,}2), (0, 1), (0, 5), (-2, 0{,}5)$
- **t di Student**: serve a stimare la media di una gaussiana quando il **campione è piccolo** e la deviazione standard della popolazione è **ignota**. Figure: densità e cumulativa per $\nu = 1, 2, 5, +\infty$; con $\nu$ piccolo le **code sono più pesanti**, con $\nu \to \infty$ diventa la normale
- Dato un campione di dimensione $n$ di una variabile $X$, media e varianza campionaria con la **correzione di Bessel** (si divide per $n-1$ invece che per $n$; la slide scrive "Blessel" e "usando $n-1$ campioni"):
  $$\bar X = \frac{1}{n}\sum_{i=1}^{n} X_i \qquad S^2 = \frac{1}{n-1}\sum_{i=1}^{n}(X_i - \bar X)^2$$
- $\dfrac{\bar X - \mu}{\sigma/\sqrt n}$ è una **normale standard** (media 0, varianza 1), mentre $\dfrac{\bar X - \mu}{S/\sqrt n}$ è una **t di Student con $n-1$ gradi di libertà**
- Densità:
  $$f(t) = \frac{\Gamma\left(\frac{\nu+1}{2}\right)}{\sqrt{\nu\pi}\,\Gamma\left(\frac{\nu}{2}\right)}\left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}} = \frac{1}{\sqrt{\nu}\,B\left(\frac12, \frac{\nu}{2}\right)}\left(1 + \frac{t^2}{\nu}\right)^{-\frac{\nu+1}{2}}$$
  con $\Gamma$ funzione gamma e $B$ funzione beta. (Correzione: la slide scrive la formula con $n$ al posto di $\nu$, ma il parametro è il numero di gradi di libertà, che qui vale $n-1$.)

## t-SNE
- PCA cattura soprattutto proprietà **globali** del dataset, quindi può dare **inconsistenze locali**: punti lontani in origine finiscono vicini
- **t-SNE** (t-Distributed Stochastic Neighbor Embedding) privilegia l'informazione **locale**: le **relazioni di vicinanza** si conservano nella riduzione
- **Svantaggi**:
  - distorsione **non lineare**, difficile da interpretare
  - mappare un **nuovo dato** dopo il calcolo non è facile (anche se possibile): per questo si usa spesso **solo per la visualizzazione**
  - le prestazioni dipendono dal dataset e da dettagli algoritmici

### SNE: idea
- Codificare l'informazione di vicinato come una **distribuzione di probabilità**: dato un punto, alta probabilità ai vicini, bassa ai lontani
- Si ottiene una distribuzione per ogni punto; le distribuzioni si confrontano con la **divergenza di Kullback-Leibler** (la slide la chiama "divergenza entropica")

### Distribuzioni di vicinato
- Gaussiana centrata in $x_i \in \mathbb{R}^d$: la probabilità che $x_i$ scelga $x_j$ come vicino è proporzionale alla densità della gaussiana in $x_j$
- Con $d$ funzione distanza (tipicamente euclidea):
  $$P_{j|i} = \frac{e^{-\frac{d(x_i, x_j)^2}{2\sigma_i^2}}}{\sum_{k \neq i} e^{-\frac{d(x_i, x_k)^2}{2\sigma_i^2}}}, \qquad P_{i|i} = 0$$
- $\sigma_i$ regola la **dimensione del vicinato**: piccolo, solo i vicini più prossimi hanno probabilità alta; grande, probabilità quasi uniformi. Si sceglie un $\sigma_i$ **diverso per ogni punto** in base alla **perplessità**
- Problema: $P_{i|j} \neq P_{j|i}$. Soluzione: distribuzione **simmetrica**
  $$P_{ij} = \frac{1}{2N}\left(P_{i|j} + P_{j|i}\right)$$

### Perplessità
- Sia $P_i$ la distribuzione condizionata di $x_i$ su tutti gli altri punti:
  $$\mathrm{perplexity}(P_i) = 2^{H(P_i)}, \qquad H(P_i) = -\sum_j P_{j|i}\log_2 P_{j|i}$$
- Misura il **numero effettivo di vicini** del punto $i$: se $P_i$ è uniforme su $k$ elementi, la perplessità è $k$
- Perplessità alta ↔ $\sigma_i^2$ alto, e viceversa
- L'algoritmo originale trova $\sigma_i$ con una **ricerca binaria** per ottenere la perplessità voluta; la perplessità è un parametro **scelto dall'utente**, perché valori diversi catturano **scale** diverse

### Obiettivo e ottimizzazione
- Dati $x_1, \dots, x_N \in \mathbb{R}^D$ e le $P_{ij}$, si cerca un **embedding** $y_1, \dots, y_N \in \mathbb{R}^d$ con $d < D$ (tipicamente 2 o 3)
- Distribuzione sui punti dell'embedding (SNE, gaussiana):
  $$Q_{ij} = \frac{e^{-d(y_i, y_j)^2}}{\sum_k \sum_{l \neq k} e^{-d(y_l, y_k)^2}}$$
- Si rende $Q$ il più simile possibile a $P$ minimizzando la divergenza KL; i parametri ottimizzati sono le coordinate $y_1, \dots, y_N$:
  $$L(Q) = KL(P\,\|\,Q) = \sum_{ij} P_{ij}\log\frac{P_{ij}}{Q_{ij}} = -\sum_{ij} P_{ij}\log Q_{ij} + \text{cost.}$$
- Gradiente:
  $$\frac{\partial L}{\partial y_i} = 4\sum_j (P_{ij} - Q_{ij})(y_i - y_j)$$
  (La slide omette il fattore 4, che non cambia la direzione. Precisazione: la slide dice "possiamo ottimizzare facendo dei restart multipli"; l'ottimizzazione è una **discesa del gradiente**, e i restart multipli servono perché la funzione non è convessa e ha minimi locali.)
- **Crowding problem**: un punto con $k$ vicini nello spazio originale non riesce a sistemarli tutti in uno spazio di dimensione inferiore. Se in 2D ha $k$ vicini a distanza 1, in 1D a distanza 1 ne può avere al più 2

### Da SNE a t-SNE
- Contro il crowding problem si usa nello spazio ridotto una distribuzione a **code più lunghe**: la **t di Student**
  $$p(x) \propto \left(1 + \frac{x^2}{\nu}\right)^{-\frac{\nu+1}{2}}, \qquad \nu = 1:\ p(x) \propto \frac{1}{1 + x^2}$$
- Quindi:
  $$Q_{ij} = \frac{\left(1 + d(y_i, y_j)^2\right)^{-1}}{\sum_k \sum_{l \neq k}\left(1 + d(y_k, y_l)^2\right)^{-1}}$$
  (Correzione: al numeratore la slide scrive $(1 - d(y_i, y_j)^2)^{-1}$; il segno corretto è $+$, come nel denominatore.)
- Le code pesanti permettono a punti moderatamente lontani in origine di stare **più lontani** nell'embedding, liberando spazio per i vicini veri

### Algoritmo (versione semplice, van der Maaten e Hinton)
- **Dati**: $X = \{x_1, \dots, x_n\}$; parametro di costo: perplessità $Perp$; ottimizzazione: iterazioni $T$, learning rate $\eta$, momentum $\alpha(t)$
- **Risultato**: rappresentazione $\mathcal{Y}^{(T)} = \{y_1, \dots, y_n\}$
- Passi:
  1. calcola le affinità $p_{j|i}$ con perplessità $Perp$
  2. $p_{ij} = \frac{p_{j|i} + p_{i|j}}{2n}$
  3. soluzione iniziale $\mathcal{Y}^{(0)}$ campionata da $\mathcal{N}(0, 10^{-4}I)$
  4. per $t = 1 \dots T$: calcola le $q_{ij}$, calcola il gradiente $\frac{\delta C}{\delta \mathcal{Y}}$, aggiorna
     $$\mathcal{Y}^{(t)} = \mathcal{Y}^{(t-1)} - \eta\,\frac{\delta C}{\delta \mathcal{Y}} + \alpha(t)\left(\mathcal{Y}^{(t-1)} - \mathcal{Y}^{(t-2)}\right)$$
  (Correzione: nella figura, ripresa dall'articolo originale, il gradiente compare con il $+$; per minimizzare il costo serve il $-$.)

### Dal notebook: t-SNE su iris
```python
from sklearn.manifold import TSNE
tsne = TSNE(n_components=2)
iristsne = tsne.fit_transform(iris.data)
plt.scatter(iristsne[:,0], iristsne[:,1], c=iris.target)

tsne = TSNE(n_components=2, init='random')
iristsne = tsne.fit_transform(iris.data)
```
- Setosa è un gruppo compatto e lontanissimo; versicolor e virginica sono due gruppi vicini con pochi punti mescolati
- Le due esecuzioni danno layout diversi (coordinate e orientamento cambiano): t-SNE è **stocastico** e le coordinate assolute non hanno significato, contano solo i vicinati
- Il notebook chiama `tsne.fit(...)` e poi `tsne.fit_transform(...)`: il primo calcolo è inutile, perché `TSNE` non ha `transform` per dati nuovi (coerente con lo svantaggio visto sopra) e si usa solo `fit_transform`
- `FutureWarning` della versione usata: in scikit-learn 1.2 l'inizializzazione di default passa da `'random'` a `'pca'` e il learning rate da 200 ad `'auto'`
- Link nel notebook: *How to Use t-SNE Effectively* (distill.pub/2016/misread-tsne) sugli errori di lettura dei grafici t-SNE; esempi scikit-learn *plot_manifold_sphere* e *plot_compare_methods* (confronto dei metodi di manifold learning)

## UMAP
- **Uniform Manifold Approximation and Projection for Dimension Reduction**. Come t-SNE si basa sulla **costruzione di un grafo di similarità** fra i punti (la slide scrive "costrizione")
- Serve sia per la **visualizzazione** sia come **preprocessing per il clustering**: a differenza di t-SNE è facile ottenerne la **funzione inversa** (e proiettare dati nuovi)
- Articolo del 2018 (arXiv 1802.03426v1), rivisto nel 2020 (v3); documentazione: umap-learn.readthedocs.io
- **Input**: matrice di distanze $N \times N$, ad esempio da $N$ punti in $\mathbb{R}^m$
- **Due parametri**: numero di vicini $k$ per ogni punto, numero di dimensioni $d$ dell'output
- **Due passi**: semplificazione della topologia, riduzione della dimensionalità

### Semplificazione della topologia
- **Simplesso** $n$-dimensionale: la slide lo definisce "un poligono col minor numero di vertici". (Precisazione: è l'inviluppo convesso di $n+1$ punti affinemente indipendenti, cioè punto, segmento, triangolo, tetraedro...)
- **Complesso simpliciale** $K$: collezione finita di simplessi tale che (i) ogni faccia di un simplesso di $K$ sta in $K$; (ii) l'intersezione di due simplessi qualsiasi di $K$ è una faccia di entrambi
- Con la logica **fuzzy** gli insiemi di simplessi vengono mappati (normalizzati) in $[0,1]$
- Passi:
  - per ogni punto $i = 1 \dots N$ costruisce uno spazio **quasi metrico** $M_i$ locale, normalizzando le distanze rispetto ai $k$ punti più vicini a $i$
  - distilla il contenuto topologico e geometrico di ogni $M_i$ in un **insieme simpliciale fuzzy** $F_i$
  - l'**unione fuzzy** $\bigcup_i F_i$ è la rappresentazione topologica globale

### Riduzione della dimensionalità
- Inizializza una nuvola $Z$ di $N$ punti in $\mathbb{R}^d$
- Misura con la **fuzzy set cross-entropy** la distanza fra la rappresentazione simpliciale fuzzy di $Z$ e quella dei dati di input
- Sposta i punti di $Z$ fino a minimizzarla

### UMAP e altri
- Figura: tre dataset 3D da 3023 punti (**Swiss roll**, **S-shape**, **sfera**) ridotti con PCA, t-SNE (perplexity = 2000) e UMAP (n_neighbor = 2000). PCA schiaccia il manifold su un piano e sovrappone parti diverse; t-SNE e UMAP srotolano meglio la struttura, con UMAP che separa più nettamente i gruppi colorati
- Tecniche più recenti: **TriMAP** e **PaCMAP**. Figura sul dataset a forma di mammut, con tempi: t-SNE 69,27 s, UMAP 24,12 s, TriMAP 12,56 s, PaCMAP 8,42 s. t-SNE e UMAP frammentano la forma in pezzi, TriMAP e PaCMAP conservano meglio la struttura globale e sono più veloci

### Esercizio
Lanciare i metodi di riduzione della dimensionalità di scikit-learn, più UMAP, sui dataset di scikit-learn e analizzare le differenze. (Aggiunta, non nelle slide: `sklearn.decomposition.PCA`, `KernelPCA`, `FastICA`, `TruncatedSVD`; `sklearn.discriminant_analysis.LinearDiscriminantAnalysis`; `sklearn.manifold.TSNE`, `Isomap`, `LocallyLinearEmbedding`, `MDS`, `SpectralEmbedding` (Laplacian Eigenmaps, LE); `sklearn.random_projection.GaussianRandomProjection`; UMAP con `umap.UMAP(n_neighbors=..., n_components=...)` dal pacchetto `umap-learn`. Il materiale non tratta PLS.)

## Self-organizing maps (SOM)
- **Mappa auto-organizzante**: tecnica **non supervisionata** che produce una rappresentazione a bassa dimensione (di solito **2D**) di dati ad alta dimensione **preservandone la struttura topologica**
- È una **rete neurale** addestrata con **apprendimento competitivo** invece che con correzione dell'errore (backpropagation con discesa del gradiente)
- Introdotta da **Kohonen** negli anni '80 (**mappa/rete di Kohonen**); astrazione costruita su modelli biologici dei sistemi neurali degli anni '70 e sui modelli di morfogenesi di Turing degli anni '50
- **Due livelli**: input e output (la **feature map**, una griglia di neuroni)
- Niente **funzione di attivazione**: i pesi passano direttamente al livello di output
- Ogni neurone ha un **vettore peso** della stessa dimensione $d$ dell'input; i pesi si imparano con il competitive learning

### I tre processi del competitive learning
- **Competizione**: ogni neurone di output ha un vettore di dimensione $n$; si calcola la distanza (di solito **euclidea**) fra ogni neurone e il dato di input, e il neurone con la **distanza più bassa** vince (in letteratura **BMU**, best matching unit; il nome non è nelle slide). Figura: 3 input $x_1, x_2, x_3$ collegati a tutti i neuroni di una griglia 3×3, ognuno con pesi $w_{ij}$
- **Cooperazione**: non si aggiorna solo il vincitore ma anche i suoi **vicini**, scelti con la **funzione kernel di vicinato**, che dipende dal **tempo** (cresce a ogni nuovo input) e dalla **distanza** fra il neurone e il vincitore sulla griglia. Figura: griglia con il vincitore al centro e vicinati a rombo che si restringono da $t_0$ a $t_1$ a $t_N$
- **Adattamento**: vincitore e vicini vengono aggiornati con forza diversa:
  $$w_k \leftarrow w_k + \eta(t)\cdot h_{ik}(t)\cdot(x_n - w_k)$$
  con $h_{ik}(t)$ il kernel di vicinato (la slide lo indica con $\eta_{ik}(t)$) e $\eta$ learning rate a **decadimento esponenziale**, tipicamente $\eta(t) = \eta_0\,e^{-t/T_1}$. Figura: la griglia si deforma verso il dato, con il vincitore che si sposta di più. (Correzione: la slide dice che la forza cala al crescere della distanza fra il neurone e il **dato di input**; per il kernel conta la distanza fra il neurone e il **neurone vincitore**, come dice la slide successiva.)
- Per $t \to \infty$ il learning rate tende a **zero**: nessun aggiornamento, nemmeno per il vincitore
- Il kernel di vicinato **decresce** con la distanza dal vincitore e con il tempo (la dimensione del vicinato si restringe), quindi è **monotono decrescente**
