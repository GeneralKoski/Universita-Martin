# Librerie Python, EDA e preprocessamento

Fonte: `Librerie python.zip`, notebook `python-libs/2-python-libs.ipynb` (moduli, standard library, regex, pandas, grafici con matplotlib/seaborn) e `python-libs/2-1-datasets-EDA.ipynb` (dataset di scikit-learn, analisi esplorativa, standardizzazione). Dati allegati: `Salaries.csv` (78 docenti), `flights.csv` (160.754 voli del 2013 da New York), `modulo.py`, immagini in `2-imgs/`. Copre le lezioni "Librerie python", "Librerie python (parte 2) + Exploratory data analysis (EDA)" e "Preprocessamento dei dati".

Gli output citati sono quelli salvati nei notebook, eseguiti con pandas 1.x: dove le API sono cambiate in pandas 2.x è segnalato.

## Moduli e pacchetti
- Un **modulo** è qualsiasi file `.py` raggiungibile dall'ambiente in esecuzione (analogia con i package Java e le librerie C++, ma organizzazione diversa).
- Un **package** è una gerarchia di cartelle con dentro un file `__init__.py` (il notebook scrive `__init.py__`, refuso). Figura: package `sound/` con i sottopackage `formats/`, `effects/`, `filters/`, ognuno con il suo `__init__.py`.
- Nel corso servono solo i moduli: un file `nomemodulo.py` nella cartella corrente si importa con `import` o `from ... import`.

```python
# modulo.py
def somma(a, b):
    return a + b
def sottrazione(a, b):
    return a - b
```

```python
import modulo
modulo.somma(1, 2)       # 3, con il prefisso del modulo
from modulo import *     # importa tutto nel namespace corrente
somma(1, 2)
from modulo import somma # importa solo la funzione indicata
```

## Python Standard Library
- Librerie non built-in ma incluse in Python, da importare (come `itertools`). Elenco: docs.python.org/3/library/.
- **`sys`**: parametri dell'ambiente. `sys.argv` = argomenti da linea di comando: `sys.argv[0]` è il nome dello script, `sys.argv[1]` il primo parametro, `len(sys.argv)` il numero di parametri (nome dello script compreso).
- **`getopt`**: gestione più sofisticata dei parametri (aggiunta: oggi si usa di solito `argparse`).
- **`os`**: file, percorsi, processi, interfaccia col sistema.
- **`math`**: `floor, ceil, factorial, log, sqrt, cos`, ...
- **`statistics`**: `mean`, ... (il notebook cita `stder`, che non esiste: le deviazioni standard sono `stdev` campionaria e `pstdev` della popolazione).

## Espressioni regolari: modulo `re`
- Uso diretto: `re.search(pattern, stringa)` restituisce un **match object** (con `span` e `match`) oppure `None`.

```python
import re
res = re.search('(?<=abc)def', 'abcdef')   # lookbehind: 'def' preceduto da 'abc'
# <re.Match object; span=(3, 6), match='def'>
re.search('den', 'abcdef')                 # None
```

- Conviene **compilare** il pattern se lo si riusa: `pattern = re.compile('(?<=abc)def')`.
- `re.match(regex, target)` per verificare se una stringa rispetta un pattern:

```python
name = 'ENSG_0000923.13'
if re.match(r'^ENS[GTP][0-9]+(\.[0-9]+)*$', name):
    print('The name is an Ensembl ID')
else:
    print('The name is not an Ensembl ID')
```

- (Precisazioni: `match` ancora il pattern solo all'**inizio** della stringa, `search` cerca ovunque, `fullmatch` richiede tutta la stringa. Nel notebook il pattern è una stringa normale con `\.`: va scritto raw, `r'...'`, altrimenti Python 3.12 dà `SyntaxWarning`. Con l'underscore, `'ENSG_0000923.13'` **non** rispetta il pattern e stampa "not an Ensembl ID", verificato.)
- Metodi di un pattern compilato (o funzioni omonime del modulo):
  - `.search(target[, start, end])`: prima occorrenza
  - `.findall(target[, start, end])`: lista di tutte le occorrenze (come stringhe)
  - `.split(target)`: tokenizza usando il pattern come separatore
  - `.sub(replacement, target)`: sostituisce il pattern
  - `re.finditer(...)`: iteratore di match object, per navigare le occorrenze con `.group()` e `.span()`
- Il notebook dice che "gli oggetti ritornati da questi metodi sono match objects". (Precisazione: lo sono solo quelli di `search`/`match`/`fullmatch` (o `None`) e gli elementi di `finditer`; `findall` e `split` restituiscono liste di stringhe, `sub` una stringa.)

```python
re.findall(r"\d+", target_string)        # ['17', '1993', '112', '26', '12', '51']
for m in re.finditer(r"\d{2}", target_string):
    print(m, m.group())                  # '1993' dà '19' e '93' (match non sovrapposti)
```

## Librerie per la data science
- **NumPy**: array multidimensionali e funzioni matematiche su di essi.
- **SciPy**: calcolo scientifico (ottimizzazione, algebra, integrazione, interpolazione, FFT, segnali, ODE).
- **Pandas**: manipolazione e analisi di **dati strutturati**.
- **scikit-learn**: framework di **machine learning** (il notebook dice "a scopo educativo"; in realtà è usato anche in produzione).
- Visualizzazione:
  - **matplotlib**, basata su NumPy; il modulo **`pyplot`** dà grafici in stile MATLAB.
  - **seaborn**, basata su matplotlib, con grafici più curati e un'interfaccia ad alto livello sui DataFrame, simile a **ggplot2** di R (il notebook la dice "interattiva": i grafici seaborn sono statici come quelli di matplotlib).
- NumPy nei notebook non ha una sezione propria: compare negli esempi con `np.sqrt`, `np.arange`, `np.c_` (concatenazione per colonne), `np.vstack`, `np.random.seed`/`randn`, `reshape(-1, 1)` e `to_numpy()`.

## Pandas
- Non fa parte della standard library: `pip install pandas`. Ispirata ai data frame di R, pensata per uno stile **funzionale** più che imperativo, con operazioni simili a **SQL**.
- Strutture principali: **`DataFrame`** (tabella con metadati: indici di riga e di colonna) e **`Series`** (una colonna). Figura: righe con **row index** (0-4) e **index label** (S1-S5), colonne con **column index** e **header**, ogni cella è un **element/value**.
- Vincolo: i valori di **una colonna** devono essere di tipo **omogeneo**.

### Creazione e caricamento
```python
import pandas as pd
df = pd.DataFrame()                         # vuoto, len(df) = 0
df['nomi'] = ['Vincenzo', 'Flavio', 'Alessandro']
df['eta'] = [38, 41, 45]                    # una colonna alla volta, attenzione all'ordine
len(df)                                     # numero di righe: 3
df.eta                                      # accesso con '.' solo se la colonna esiste già
df = pd.read_csv("Salaries.csv")            # anche json, excel, stata, hdf5, sas, ...
```

- `display(df)` in Jupyter mostra la tabella formattata.

### Tipi di dato
- Pandas usa tipi propri (per dialogare con formati e piattaforme diverse): **`object`** ≈ stringa, **`int64`**, **`float64`**, **`datetime64`**.
- Al caricamento il tipo di ogni colonna è **inferito** dal contenuto. Si legge con `df['col'].dtype` o `df.dtypes`.
- Conversione con **`astype`**, se il contenuto è compatibile; molte operazioni restituiscono **copie**:

```python
df['salary_str'] = df['salary'].astype(str)   # int64 -> object
```

### Attributi
- `df.dtypes` (tipo per colonna), `df.columns` (nomi da sinistra a destra), `df.axes` (indice di riga e di colonna, es. `RangeIndex(0, 78)`), `df.ndim` (2), `df.shape` (righe, colonne), `df.size` (= righe × colonne), `df.values` (array NumPy; aggiunta: oggi si preferisce `df.to_numpy()`).

### Statistiche rapide per l'EDA
- **`df.describe()`**: per le colonne numeriche `count, mean, std, min, 25%, 50%, 75%, max`. Su `Salaries.csv`: salary media 108.024, mediana 104.671, std 28.294.
- `df.min()`, `df.max()` per colonna: sulle colonne `object` il confronto è **lessicografico** (nel notebook `salary_str` ha min `'102000'` e max `'99418'`: ecco perché i numeri vanno tenuti numerici).
- `df.mean()`, `df.std()`, `df['salary'].median()`: solo per colonne numeriche. (API cambiata: nel notebook `df.mean()` su un DataFrame con colonne di testo dà un `FutureWarning`; da pandas 2.0 dà `TypeError`, verificato. Si usa `df.mean(numeric_only=True)` o si selezionano prima le colonne numeriche.)

### Groupby
- Come il `GROUP BY` di SQL: divide le righe in gruppi secondo un criterio e calcola statistiche per gruppo. Con più colonne il gruppo è la combinazione dei valori (prodotto cartesiano), con indice gerarchico.

```python
df.groupby(['rank']).mean()
df.groupby(['rank', 'discipline', 'sex']).mean()
df.groupby(['rank'], sort=False)[['salary']].mean()   # sort=False: niente ordinamento, più veloce
```

- Risultato su `Salaries`: Prof 123.625, AssocProf 91.786, AsstProf 81.363 di salario medio.
- (Stessa modifica di API: in pandas 2.x `groupby(...).mean()` con colonne non numeriche dà `TypeError`, verificato; usare `numeric_only=True` o selezionare le colonne, come nell'ultima riga.)

### Filtro e selezione
- **Maschere booleane**: il risultato è una **copia** che conserva le **etichette di riga originali** (nel filtro sul salario mancano per esempio le righe 8 e 9).

```python
df[df['salary'] > 120000]
df[df['sex'] == 'Female']
```

- **Slicing** con `[]`:
  - stringa o lista di stringhe → **colonne**: `df[['rank', 'salary']]`
  - intervallo di interi → **righe per posizione** (non per etichetta): `df[10:20]`; dopo un filtro, `df[df['salary'] > 120000][1:10]` prende le posizioni 1-9 del risultato
  - righe e colonne si combinano in sequenza: `df[0:2]['rank']` è una `Series`, `df[0:2][['rank']]` (lista) un `DataFrame`
- Operatori di slicing in cascata sono poco efficienti (ognuno crea una copia): meglio una sola operazione con
  - **`loc`** per **etichette**: `df.loc[10:20, ['rank', 'sex', 'salary']]` (aggiunta: con `loc` l'estremo finale è **incluso**, infatti restituisce 11 righe, 10-20)
  - **`iloc`** per **posizione**: `df.iloc[10:20, [0, 1]]` o `df.iloc[10:20, 0:2]` (estremo finale escluso, come in Python)
- `iloc` permette anche di **modificare** celle: `df.iloc[0, 0] = 'AsstProf'` cambia il DataFrame originale. (Il notebook dice che `iloc` "non crea copie ma è una vista": vale per l'**assegnamento** con `df.iloc[...] = ...`; il risultato di una lettura con `iloc`, se lo si salva e modifica, può essere una copia, e da pandas 3.0, col Copy-on-Write, lo è sempre.)

### Ordinamento
```python
df.sort_values(by='service')
df.sort_values(by=['service', 'salary'], ascending=[True, False])   # più colonne con priorità
```

### Valori mancanti
- Dataset `flights.csv`: ritardi, orari, `tailnum`, `air_time` con molti `NaN` (voli cancellati).
- Il null di pandas (`NaN`) non è `None`: servono **`isnull()`** / **`notnull()`** (aggiunta: alias `isna()`/`notna()`).

```python
flights[flights['dep_time'].isnull()]          # righe con dep_time nullo
flights.isnull()                               # DataFrame di booleani
flights[flights.isnull().any(axis=1)]          # righe con almeno un valore nullo
```

- `any` restituisce `True` se almeno un elemento lungo l'asse è vero. **Asse 0** = lungo le righe (risultato per colonna), **asse 1** = lungo le colonne (risultato per riga).
- (Errore: la cella `flights[flights.isnull()]` è commentata come "righe dove tutte le colonne sono null", ma indicizzare con un DataFrame booleano **maschera** le celle e restituisce tutto il DataFrame pieno di `NaN`, come si vede nell'output. Per le righe tutte nulle si scrive `flights[flights.isnull().all(axis=1)]`.)
- Eliminazione e sostituzione:
  - `dropna()`: elimina le righe con almeno un nullo
  - `dropna(how='all')`: righe con tutti i valori nulli
  - `dropna(axis=1, how='all')`: colonne tutte nulle
  - `dropna(thresh=5)`: il notebook dice "elimina le righe che contengono più di 4 valori nulli" (errore: `thresh` è il numero **minimo di valori non nulli** per tenere la riga, quindi elimina le righe con **meno di 5 valori validi**; verificato)
  - `fillna(0)`: sostituisce i nulli con un valore. Colonne di tipo diverso richiedono valori diversi, quindi conviene un `fillna` **per colonna**:

```python
flights['tailnum'] = flights['tailnum'].fillna('NESSUNO')
```

### Modifica di più celle e colonne derivate
- Lo slicing a sinistra di un assegnamento **modifica** il DataFrame:

```python
flights[flights['month'] == 1] = 0     # tutte le colonne delle righe di gennaio diventano 0
```

- (Attenzione: questa riga azzera **tutte** le colonne delle righe selezionate, non solo `month`, infatti dopo `n2` vale 0 su quelle righe. Per una sola colonna: `flights.loc[flights['month'] == 1, 'month'] = 0`.)
- Colonne derivate con operazioni vettoriali fra colonne: `flights['n2'] = flights['distance'] + 2 * flights['month']`.
- **`apply`** applica una funzione lungo un asse: `df.apply(np.sqrt)` (con `[[4, 9]] * 3` dà 2.0 e 3.0).

### Unire DataFrame
- **`pd.concat([df1, df2])`** accoda DataFrame con le stesse colonne; attenzione alle etichette di riga, che possono ripetersi (`x, y, x, y`). Rimedi: `ignore_index=True` (rinumera 0..n-1) oppure `reset_index(inplace=True)`, che sposta il vecchio indice in una colonna `index` (aggiunta: `drop=True` per scartarlo).
- **`merge`**: join in stile SQL. Figura: **left**, **right**, **inner**, **outer** join con diagrammi di Venn.

```python
df1.merge(df2, left_on='lkey', right_on='rkey')   # chiavi con nomi diversi; colonne omonime -> suffissi _x, _y
df1.merge(df2, on='a')                            # default: how='inner'
df1.merge(df2, how='outer', on='a')               # chiavi di entrambi, NaN dove manca il valore
```

- Con chiavi duplicate (`foo` due volte a sinistra e due a destra) si ottengono tutte le combinazioni (4 righe `foo`). L'ordine dei DataFrame conta; il default è **inner**.

## Grafici
- Pandas offre grafici per l'EDA tramite matplotlib e seaborn (documentazione: `pandas.DataFrame.plot`). Nei notebook vecchi può servire `%matplotlib inline`.

### Anatomia di un grafico matplotlib
- Figure: una **figure** (`plt.figure()`) contiene uno o più **axes** (`fig.add_subplot()`, `fig.subplots()`, `fig.add_axes([left, bottom, width, height])`). Ogni axes ha titolo, assi x/y con **major/minor tick** e relative label, **xlabel/ylabel**, **legend**, **grid**, **spine**, linee (`ax.plot`) e marker (`ax.scatter`). Cheatsheet: matplotlib.org/cheatsheets.

```python
import matplotlib.pyplot as plt
fig1, fig1_axes = plt.subplots(ncols=2, nrows=2)   # fig1_axes è un ndarray 2x2 di axes
fig1_axes[0, 0].set_title("axis 0,0")
fig1.tight_layout()                                # "asso piglia tutto": evita sovrapposizioni
```

- Con `subplots` ogni riga ha lo stesso numero di colonne e le colonne la stessa larghezza; **gridspec** toglie questi vincoli e permette elementi con **span** diverso:

```python
fig3 = plt.figure(constrained_layout=True)
gs = fig3.add_gridspec(3, 3)
ax1 = fig3.add_subplot(gs[0, :])     # tutta la prima riga
ax2 = fig3.add_subplot(gs[1, :-1])   # riga 1, tutte tranne l'ultima colonna
ax3 = fig3.add_subplot(gs[1:, -1])   # ultima colonna, righe 1-2
```

### Istogrammi e density plot
```python
flights.hist()                               # un istogramma per ogni colonna numerica
flights.hist(column='distance', bins=100)
import seaborn as sns
sns.displot(flights.distance, bins=10, kde=True)   # istogramma + stima di densità (KDE)
```

- **Attenzione al numero di bin**: con i 10 bin di default la distribuzione di `distance` ha una forma grossolana; con 100 bin emergono picchi isolati (le distanze sono poche e discrete, una per tratta).
- **Attenzione ai density plot, spesso ingannano**: la KDE liscia e interpola dove non ci sono dati e cambia molto con i bin e la banda.

### Grafici a barre
```python
df.plot.bar(x='lab', y='val', rot=0)      # rot ruota le etichette sull'asse x
df.plot.bar()                             # una barra per colonna, raggruppate per indice
df.plot.bar(stacked=True)                 # barre impilate
```

- Barre affiancate con matplotlib puro: `ax.bar(x - width/2, ...)` e `ax.bar(x + width/2, ...)` con `x = np.arange(n)`, poi `ax.set_xticks(x, labels)` (da matplotlib 3.5), `ax.legend()`, `ax.bar_label(rects, padding=3)` per scrivere i valori sopra le barre. Spostare l'indice in una colonna: `df['animal'] = df.index; df.index = range(len(df))`.

### Scatter plot e densità 2D
- Richiedono due misure **numeriche**.

```python
df.plot.scatter(x='speed', y='lifespan', c=df['animal'].map(color_map))   # colori da un dict categoria->colore
sns.scatterplot(x='speed', y='lifespan', data=df, hue='animal')           # hue colora per categoria
sns.jointplot(x='distance', y='hour', data=flights)                       # scatter + istogrammi marginali
plt.hist2d(x, y, bins=100, cmap="RdYlGn_r", norm=colors.LogNorm())        # densità 2D, scala log
```

- `sorted(set(flights.hour))` mostra molti `nan` ripetuti: `NaN != NaN`, quindi un set non li deduplica (aggiunta).
- (API deprecata: `flights['hour'].fillna(0, inplace=True)` su una colonna estratta è chained assignment; da pandas 2.x dà `FutureWarning` e col Copy-on-Write non modifica il DataFrame. Si scrive `flights['hour'] = flights['hour'].fillna(0)`.)
- (Errore nell'esempio `hist2d` con dati sintetici: la covarianza `[[2, 3], [1, 3]]` non è simmetrica né semidefinita positiva, infatti NumPy dà `RuntimeWarning`; una matrice di covarianza valida è simmetrica, es. `[[2, 1], [1, 3]]`. Aggiunta: oggi si usa `np.random.default_rng(seed).multivariate_normal(...)`.)

### Pair plot
```python
from sklearn.datasets import load_iris
iris = load_iris()                           # oggetto Bunch: dict con accesso anche per attributo
data1 = pd.DataFrame(data=np.c_[iris['data'], iris['target']],
                     columns=iris['feature_names'] + ['target'])
sns.pairplot(data1, hue="target", diag_kind="hist")              # scatter a coppie + istogrammi in diagonale
sns.pairplot(data1, hue="target", diag_kind="hist", corner=True) # solo il triangolo inferiore
sns.pairplot(data1, hue="target", markers=["o", "s", "D"])
```

- Il pair plot mostra per ogni coppia di feature come si separano le classi: è il primo strumento per capire quali feature servono alla classificazione.

### Box plot
```python
df.boxplot()
dft.boxplot(by='X')                       # un box per gruppo
flights.boxplot(column='distance', by='carrier')
```

- Figura: box da **Q1** a **Q3** con la **mediana**; baffi fino a $Q1 - 1.5 \cdot IQR$ e $Q3 + 1.5 \cdot IQR$; i punti oltre sono **outlier**. Su una normale corrispondono a $\pm 0.6745\sigma$ (box, 50% dei dati) e $\pm 2.698\sigma$ (baffi, 99,3%).

$$IQR = Q3 - Q1$$

- **IQR** è un indice di **dispersione**: il notebook lo chiama "interquantile range" e dice che riguarda "il 50% dei dati più vicini alla media". (Precisazione: è l'**interquartile** range e copre il 50% centrale dei dati, fra il primo e il terzo quartile, attorno alla **mediana**, non alla media.)

### Violin e swarm plot
```python
sns.violinplot(x='X', y='Col1', data=dft, ax=axes)   # distribuzione (KDE) per categoria
sns.swarmplot(x='X', y='Col1', data=dft)             # tutti i punti, senza sovrapposizioni
sns.violinplot(x='rank', y='service', data=salaries)
sns.swarmplot(x='rank', y='service', data=salaries, color='k', alpha=0.3)  # sovrapposto al violino
```

- **Attenzione**: ogni violino è **indipendente**, le larghezze sono relative al singolo violino e non confrontabili fra violini. Inoltre la KDE si estende oltre i dati: nel grafico di `service` il violino dei Prof scende sotto zero, valori impossibili.
- Formato **long/tidy** con **`pd.melt`**, per mettere tutte le misure in una colonna e plottarle insieme:

```python
iris = sns.load_dataset("iris")
iris = pd.melt(iris, "species", var_name="measurement")   # colonne: species, measurement, value
sns.swarmplot(x="measurement", y="value", hue="species", data=iris, ax=ax)
```

- (Nel notebook l'ultima chiamata usa `axes=ax`; il parametro di seaborn è `ax=ax`. `sns.set(...)` è un alias del più recente `sns.set_theme(...)`.)

## Dataset di esempio di scikit-learn
- Tre categorie:
  - **toy**: piccoli, inclusi nella libreria (scikit-learn.org/stable/datasets/toy_dataset.html)
  - **real world**: scaricati al bisogno, spesso multiclasse e con molto preprocessing, specie per l'NLP (scikit-learn.org/stable/datasets/real_world.html)
  - **generati** sinteticamente (rimandati a una lezione successiva)
- Toy usati:
  - **Iris** di Fisher
  - **Diabetes**: dati biometrici e anagrafici di pazienti diabetici, per la **regressione** (target = misura quantitativa della progressione della malattia)
  - **Wine recognition**: misure chimiche di vini da tre **cultivar** di una regione italiana (classificazione a 3 classi)
  - **Breast cancer Wisconsin (diagnostic)**: feature estratte da immagini per distinguere tumori **benigni** e **maligni**
- Real world:
  - **Forest covertypes**: tipo di copertura forestale (7 classi) su quadrati di 30×30 m da dati cartografici
  - **RCV1**: articoli di agenzia Reuters, ognuno con la sua appartenenza a **103 categorie**, feature bag of words (il notebook scrive "RCV!")
- Altra fonte: **UCI Machine Learning Repository** (archive.ics.uci.edu).
- Caricamento: `load_*` restituisce un **Bunch**; con `return_X_y=True, as_frame=True` restituisce direttamente `(X, y)` come DataFrame e Series:

```python
from sklearn import datasets, preprocessing
X, y = datasets.load_wine(return_X_y=True, as_frame=True)
X['target'] = y        # comodo per i grafici con hue='target'
```

- (Il notebook usa `from sklearn import *`; è più chiaro importare i sottomoduli che servono. La prima cella sul diabetes fallisce per un problema d'ambiente, NumPy 2 con una SciPy compilata per NumPy 1.x, non per il codice.)

## Exploratory Data Analysis (EDA)
Schema seguito sui tre dataset: caricamento → `describe()` → box plot → (pair plot, correlazioni, heatmap) → standardizzazione → di nuovo box plot e pair plot.

### Diabetes (regressione)
```python
dfi, dfo = datasets.load_diabetes(return_X_y=True, as_frame=True, scaled=False)
dfi['target'] = dfo                         # 442 righe, 10 feature + target (25-346)
dfit = dfi.describe().transpose()           # una riga per feature
dfit['varcoeff'] = dfit['mean'] / dfit['std']
```

- `scaled=False` dà i valori originali (di default le feature sono già centrate e scalate); `sex` è codificato 1/2.
- (Errore: il **coefficiente di variazione** è $CV = \sigma / \mu$, deviazione standard su media; il notebook calcola l'inverso, media su deviazione. Con la formula corretta il target, molto disperso, ha $CV \approx 0.51$.)
- `dfi.boxplot()`: le feature hanno **scale molto diverse** (s1 attorno a 190, s4 e s5 attorno a 4), quindi il box plot di più feature insieme non si legge: primo motivo per standardizzare.
- `sns.swarmplot(x="target", y="age", data=dfi)`: con un target **continuo** usato come categoria i punti non entrano (warning "% of the points cannot be placed").
- `sns.pairplot(dfi, hue="target", corner=True)`: con hue continuo i colori sono una scala.
- **`dfi.corr()`**: matrice di correlazione di **Pearson**. Il target correla di più con **bmi** (0.59), **s5** (0.57), bp (0.44), s4 (0.43); fra le feature, **s1-s2** (0.90) e **s3-s4** (-0.74) sono fortemente correlate (aggiunta: feature quasi ridondanti, candidate alla selezione o alla riduzione della dimensionalità).

### Wine (classificazione a 3 classi)
- 178 campioni, 13 feature chimiche, target {0, 1, 2}.
- `winedf.describe()` e `seaborn.boxplot(data=winedf)`: **proline** (fino a 1680) schiaccia tutte le altre feature vicino a zero.

### Preprocessamento: standardizzazione con `StandardScaler`
- Trasforma ogni feature in media 0 e deviazione standard 1 (z-score):

$$z = \frac{x - \mu}{\sigma}$$

- Codice del notebook: uno scaler per colonna, conservato in un dict per poter tornare ai valori originali con `inverse_transform`:

```python
scalers = dict()
for c in set(winedf.columns):
    x = winedf[c].to_numpy().reshape(-1, 1)        # lo scaler vuole una matrice 2D (n, 1)
    scaler = preprocessing.StandardScaler().fit(x) # fit: stima media e std
    winedf[c] = scaler.transform(x)                # transform: applica z-score
    scalers[c] = scaler
seaborn.boxplot(data=winedf)                       # ora tutte le feature sono confrontabili
```

- Dopo la standardizzazione il box plot è leggibile: si vedono asimmetrie e **outlier** (punti oltre ±3) di ogni feature, e il pair plot con `hue="target"` mostra quali coppie separano le tre cultivar.
- (Errore di metodo: il ciclo standardizza anche la colonna **`target`**, cioè le etichette di classe, che invece non vanno toccate: nel box plot scalato compare anche il target e nel pair plot l'hue diventa -1.2, 0.08, 1.37. Va escluso, es. `for c in winedf.columns.drop('target')`. Aggiunta: lo scaler va stimato solo sul **training set** e poi applicato al test set, altrimenti c'è **data leakage**; lo stesso si può fare su tutte le colonne insieme con `StandardScaler().fit_transform(X)`.)
- Variante finale del notebook: scaling in un nuovo DataFrame `wdf_X_scaled = pd.DataFrame(wdf_X)` lasciando i dati originali, con `plt.setp(ax.get_xticklabels(), rotation=90)` per leggere i nomi delle feature. (Errori: la cella `sns.pairplot(wdf, ...)` usa la variabile `wdf`, mai definita, che in un kernel pulito dà `NameError`, va `wdf_X`; il dict degli scaler si chiama `bcscalers` come quello del breast cancer, nome riciclato.)

### Breast cancer (classificazione binaria)
- 569 campioni, 30 feature (`mean`, `error` e `worst` di raggio, texture, perimetro, area, smoothness, ...), target {0, 1} (aggiunta: in scikit-learn 0 = maligno, 1 = benigno).
- Box plot grezzo → standardizzazione come sopra (anche qui il ciclo scala il target).
- **`bcdf.corr()`**: raggio, perimetro e area sono quasi perfettamente correlati (mean radius - mean perimeter 0.998, - mean area 0.987), com'è ovvio geometricamente: feature ridondanti.
- **Heatmap dei dati**: `sns.heatmap(bcdf, cmap='RdYlGn')`; ordinando le righe per target (`bcdf.sort_values(by='target')`) si vedono due blocchi di colore diversi, cioè le feature distinguono le classi.
- **Heatmap della correlazione**:

```python
hmap = sns.heatmap(bcdf.corr(), cmap='RdYlGn', xticklabels=True, yticklabels=True)
hmap.set_xticklabels(hmap.get_xmajorticklabels(), fontsize=6)
```

  (Il notebook passa anche `fmt='d'`, che senza `annot=True` è ignorato e con `annot=True` darebbe errore su valori float: per le correlazioni si usa `fmt='.2f'`.)
- **`sns.clustermap(bcdf.corr(), ...)`**: heatmap con **clustering gerarchico** di righe e colonne e dendrogrammi; raggruppa le feature correlate in blocchi (immagine `save_as_a_png.png`: il target correla negativamente con concavità, concave points, perimetro, raggio e area). `sns.clustermap(bcdf, figsize=(5, 5))` fa lo stesso sui dati.
- `sns.violinplot(data=bcdf)`; `sns.violinplot(data=bcdf[bcdf.columns[0]], bw=.05)` con banda stretta mostra una densità frastagliata. (API deprecata: da seaborn 0.13 `bw` è sostituito da `bw_adjust` / `bw_method`.)

### RCV1 (dati sparsi)
- La sezione è intitolata "Forest covertypes", ma il codice scarica **RCV1** con `fetch_rcv1()` (errore di intestazione: covertype si carica con `fetch_covtype()`).
- `rcv1.data`: matrice **sparsa CSR** (SciPy) 804.414 × 47.236, vettori **TF-IDF** log normalizzati (coseno), solo lo 0,16% di valori non nulli; `rcv1.target`: matrice sparsa 804.414 × 103, **multilabel** (ogni articolo ha da 1 a 17 categorie). Download di circa 656 MB.
- Conversione in DataFrame sparso: `pandas.DataFrame.sparse.from_spmatrix(rcv1.data)`. (Aggiunta: per dati di queste dimensioni conviene restare sulla matrice sparsa, che gli stimatori di scikit-learn accettano direttamente.)

## Da ricordare per il progetto
- Prima esplorazione: `df.shape`, `df.dtypes`, `df.describe()`, `df.isnull().sum()`, conteggio delle classi.
- Selezione: maschere booleane, `loc` (etichette, estremo incluso), `iloc` (posizioni, estremo escluso); modificare con `df.loc[mask, 'col'] = v`, non con slicing a catena.
- Valori mancanti: individuarli con `isnull().any(axis=...)`, poi `dropna` (`how`, `axis`, `thresh` = minimo di valori validi) o `fillna` **per colonna**.
- `groupby` per statistiche per classe/gruppo; `merge`/`concat` per unire tabelle (attenzione agli indici duplicati).
- Grafici EDA: istogrammi (scegliere i bin), box plot (IQR, outlier), violin/swarm, scatter e pair plot con `hue` sulla classe, heatmap e clustermap della correlazione.
- Diffidare di KDE e violini: inventano densità dove non ci sono dati.
- Feature con scale diverse → **standardizzazione** (`StandardScaler`, z-score), senza toccare il target e stimata solo sul training set.
- Feature molto correlate (s1-s2, raggio-perimetro-area) sono ridondanti: candidate alla selezione delle feature.
- Con pandas 2.x usare `numeric_only=True` nelle aggregazioni e niente `inplace` su colonne estratte.
