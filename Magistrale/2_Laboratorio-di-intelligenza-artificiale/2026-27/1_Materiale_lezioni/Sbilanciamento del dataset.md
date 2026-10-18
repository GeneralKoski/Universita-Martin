# Gestione dello sbilanciamento tra le classi

Fonte: `Sbilanciamento del dataset.pdf`

## Il problema
- Lo **sbilanciamento** compare in molte applicazioni pratiche dell'apprendimento supervisionato (e non)
- Nasce quando si deve riconoscere una classe con **pochi campioni** nel dataset: la classe è **rara**
- Per la disparità di numerosità l'algoritmo riconosce meglio la classe (o le classi) con più campioni e ha **prestazioni molto ridotte** sulla classe rara
- Il problema è più subdolo: si rischia di **non accorgersene** se la misura di qualità usata (es. **accuratezza**) non è adeguata a un dataset sbilanciato
- Figura: dataset bilanciato (genere: 50,4% maschi, 49,6% femmine) contro dataset sbilanciato (transazioni: 99% normali, 1% fraudolente)
- È più comune di quanto si pensi. In molte applicazioni lo sbilanciamento non è un difetto di campionamento ma è **intrinseco** al problema: **rilevamento di frodi**, **rilevamento di anomalie**, **diagnosi di malattie rare**, fuoriuscite di petrolio, rilevamento facciale, ...

### Perché il modello sbaglia
- Riceve molti più esempi di una classe e ne viene **sbilanciato**: non impara cosa rende l'altra classe "diversa" né i **pattern sottostanti** che distinguono le classi
- Impara che una classe è più comune, quindi tende "naturalmente" verso di essa: è incline a **sovra-adattarsi alla classe maggioritaria**. Predicendo solo la maggioritaria otterrebbe già un buon punteggio nella funzione di costo
- **Paradosso dell'accuratezza**: se la classe A è il 99% dei campioni, un classificatore che risponde sempre A ha comunque circa il **99% di accuratezza**
- Una soluzione è usare **precisione** e **richiamo (recall)**, ma cambiare misura non aiuta il classificatore sulle **istanze problematiche**: serve solo ad accorgersi del problema

(Aggiunta, non nelle slide, con $TP, FP, FN, TN$ della matrice di confusione e la classe rara come positiva: $\text{precision} = \frac{TP}{TP + FP}$, $\text{recall} = \frac{TP}{TP + FN}$, $F_1 = 2\,\frac{\text{precision}\cdot\text{recall}}{\text{precision} + \text{recall}}$. Nel caso "sempre A" la recall della classe rara è 0 nonostante il 99% di accuratezza. In scikit-learn: `precision_score`, `recall_score`, `f1_score`, `balanced_accuracy_score`, `classification_report`.)

## Ri-campionare non è sempre la scelta migliore
Prima di ri-campionare:
- si possono **raccogliere più dati**? Se sì conviene sempre, perché i dati artificiali non sostituiscono mai quelli reali
- usare un **algoritmo adeguato**: alcuni sono più robusti di altri allo sbilanciamento, ma la scelta dipende anche dagli obiettivi della classificazione
- alcuni modelli possono **penalizzare di più gli errori sulle classi minoritarie**, eliminando il bisogno di ri-campionare (vedi cost-sensitive learning)
- a volte conviene **cambiare approccio**: per le frodi, ad esempio, un algoritmo di **riconoscimento degli outlier** (la slide scrive "rinascimento")

## Ri-campionamento
La soluzione più adottata, in due tipologie principali (ma non le uniche):
- **Sotto-campionamento (undersampling)**: si riducono i campioni della classe più frequente
- **Sovra-campionamento (oversampling)**: si aumentano artificialmente i campioni della classe meno frequente
- Figura: nell'undersampling la barra della maggioritaria viene ridotta a un sottoinsieme dei suoi campioni; nell'oversampling la barra della minoritaria viene allungata con copie dei suoi campioni fino a pareggiare l'altra

## Sotto-campionamento
- La classe (o le classi) maggioritaria viene ridotta fino a una numerosità **compatibile** con quella delle classi sotto-rappresentate
- Si ri-campiona **in modo casuale**, facendo attenzione a campionare **uniformemente su tutte le dimensioni** (figura: nube blu prima e dopo, con la stessa copertura dello spazio ma meno punti)
- Non serve la stessa numerosità esatta: lasciare una certa **tolleranza** nella differenza può rendere il classificatore più generalizzabile
- **Rischio**: rimuovere punti importanti della classe ridotta, cambiando molto le prestazioni perché si interferisce con la stima della **frontiera** e quindi con i pattern appresi (la slide scrive "va ad inferire la stima"). Figura: con tutti i punti la frontiera stimata ("actual") è quasi parallela a quella ideale; tolti alcuni "−" vicino al confine, la frontiera stimata si inclina e si allontana dall'ideale
- Attenzione a **cosa** si elimina. Figura con i tipi di esempi della classe minoritaria: **safe** (in mezzo alla propria classe), **borderline** (sul confine), **rare** (piccoli gruppi isolati dentro l'altra classe), **outlier** (singoli punti immersi nell'altra classe). Domande:
  - rispetto al confine fra le classi, dove si trovano i punti eliminati?
  - ha senso eliminare le istanze rare o gli outlier?

### Collegamenti di Tomek (Tomek links)
- Siano $x_i$ e $x_j$ due punti di **classi diverse** e $d(x_i, x_j)$ la loro distanza
- $(x_i, x_j)$ è un **Tomek link** se non esiste alcun punto $x_l$ tale che
  $$d(x_i, x_l) < d(x_i, x_j) \quad \text{oppure} \quad d(x_j, x_l) < d(x_i, x_j)$$
  cioè $x_i$ è il punto più vicino a $x_j$ e viceversa (**vicini più prossimi reciproci** di classi diverse)
- Rimuovendo i punti della **classe maggioritaria** che fanno parte di un Tomek link si eliminano sia **rumore** sia **esempi borderline**: il confine fra le classi si pulisce (figura: prima e dopo, con i "−" a contatto con i "+" rimossi)

### CNN (Condensed Nearest Neighbor)
- Cerca un sottoinsieme dei campioni che non comporti **alcuna perdita di prestazioni**, detto **insieme minimo coerente**
- Si scorrono i punti del dataset e si aggiungono all'output **solo se non vengono classificati correttamente** dal contenuto corrente: si tengono i punti "difficili", si scartano quelli ridondanti
- Figura: la maggioritaria (blu, densissima) si riduce a pochi punti vicini alla minoritaria (arancione), che resta intatta
- Passi:
  1. $S$ = training set di partenza
  2. $S'$ = tutti i punti della classe **positiva** (minoritaria) più **un elemento a caso** della classe negativa
  3. si classifica tutto $S$ con un classificatore **1-NN** che usa $S'$
  4. si spostano da $S$ a $S'$ tutti i punti **classificati erroneamente**

### ENN (Edited Nearest Neighbors) e NCR (Neighborhood Cleaning Rule)
- **ENN**: usa un **3-NN**
  - un esempio della classe **maggioritaria** classificato erroneamente dai suoi 3 vicini più prossimi viene **rimosso**
  - un esempio della classe **minoritaria** classificato erroneamente dai suoi 3 vicini fa rimuovere i suoi **vicini della classe maggioritaria**
  - (Precisazione: la regola sui vicini maggioritari di un esempio minoritario è in letteratura quella della NCR di Laurikkala, 2001; l'ENN di Wilson rimuove ogni esempio la cui classe differisce da quella della maggioranza dei suoi 3 vicini, come dice la slide su SMOTE + ENN più avanti.)
  - Figura: classe 0 (verde) e classe 1 (blu), con evidenziati i campioni della classe 0 rimossi, tutti nella zona di sovrapposizione con la classe 1
- **NCR**: combina ENN con CNN. Con CNN rimuove i **duplicati** (esempi ridondanti), poi con ENN rimuove **rumore** ed elementi **ambigui**

## Sovra-campionamento
- Si aumenta la numerosità della classe sotto-rappresentata aggiungendo **campioni artificiali** costruiti dalle proprietà dei campioni originali, soprattutto dalla loro **disposizione nello spazio** $n$-dimensionale
- Figura: dataset sbilanciato (molti blu, pochi rossi) → con under-sampling diventano pochi blu e pochi rossi; con over-sampling molti blu e molti rossi

### SMOTE (Synthetic Minority Over-sampling Technique)
- Genera **nuove istanze** invece di replicare quelle esistenti, **interpolando** esempi della classe minoritaria vicini nello spazio delle feature
- Per ogni classe minoritaria introduce **esempi sintetici** sui **segmenti** che uniscono un esempio a tutti o ad alcuni dei suoi $k$ **vicini** della stessa classe minoritaria (la slide scrive "vinci")
- Figura: punti arancioni (minoritari) collegati da segmenti tratteggiati, con i campioni sintetici (verdi) generati lungo i segmenti
- Algoritmo, per ogni esempio $x_i$ della classe minoritaria:
  1. **trova** i suoi $k$ vicini minoritari
  2. **sceglie** a caso $j$ di questi vicini ($j$ dipende da quanti esempi si vogliono generare)
  3. **genera** esempi sintetici in modo casuale lungo i segmenti che uniscono $x_i$ ai $j$ vicini scelti:
     - calcola la differenza fra il vettore delle feature del vicino e quello di $x_i$
     - la moltiplica per un numero casuale fra 0 e 1
     - somma il risultato al vettore di $x_i$
  $$x_{new} = x_i + \text{gap}\cdot(x_{nn} - x_i), \qquad \text{gap} \sim U(0,1)$$
- Figura (esempio con $k = 4$): $x_1$ con i vicini $x_{11}, \dots, x_{14}$; il punto sintetico è $r_1 = x_1 + \text{gap}\cdot\text{diff}$ sul segmento $x_1 x_{11}$
- Riferimento: N.V. Chawla, K.W. Bowyer, L.O. Hall, W.P. Kegelmeyer, *SMOTE: synthetic minority over-sampling technique*, Journal of Artificial Intelligence Research 16 (2002), 321-357
- **Limite**: SMOTE è intrinsecamente pericolosa perché **generalizza ciecamente** l'area minoritaria **senza guardare la classe maggioritaria**. Figura: un campione sintetico generato fra due minoritari finisce vicino a un campione maggioritario ("but what if there is a majority sample nearby?")
- Il problema è grave con distribuzioni **molto asimmetriche**: la minoritaria è molto **sparsa** rispetto alla maggioritaria e aumenta la probabilità di **mescolanza fra le classi**

### SMOTE + Tomek links
- Soluzione al problema: combinare SMOTE con i **Tomek link**, che ripuliscono le sovrapposizioni create
- Figura in 4 passi: (a) dataset originale (stelle minoritarie fra cerchi maggioritari); (b) dopo SMOTE, molte più stelle; (c) Tomek link individuati (riquadri tratteggiati nelle zone di contatto); (d) dopo la rimozione, gruppi di classe ben definiti

### SMOTE + ENN
- SMOTE si può combinare anche con ENN. Figura: dataset originale → dopo SMOTE (minoritaria blu infoltita, ancora mescolata) → dopo SMOTE + ENN (confine più pulito)
- ENN rimuove qualsiasi esempio la cui classe è **diversa da quella di almeno due dei suoi 3 vicini**
- ENN rimuove **più esempi** dei Tomek link
- ENN rimuove esempi da **entrambe le classi**

### Borderline-SMOTE
- Variante di SMOTE che si concentra sui dati **al confine** fra le classi, per rafforzare il confine verso l'"interno" della classe
- **Ignora i punti rumorosi** (outlier), definiti come punti i cui vicini sono **tutti** della classe maggioritaria
- Figura (dataset "Circle"): (a) distribuzione originale, minoritaria dentro un cerchio; (b) esempi minoritari di confine; (c) esempi sintetici generati solo lungo il bordo del cerchio
- (Aggiunta, non nelle slide: nell'articolo originale si sovracampionano i punti "in pericolo", cioè con più della metà dei vicini maggioritari ma non tutti.)

### ADASYN (Adaptive Synthetic sampling)
- Per ogni osservazione minoritaria calcola l'**impurità del vicinato**: il rapporto fra le osservazioni **maggioritarie** fra i $k$ vicini e $k$
  $$r_i = \frac{\Delta_i}{k}$$
  con $\Delta_i$ il numero di vicini maggioritari di $x_i$
- I rapporti vengono normalizzati in una **distribuzione di probabilità** (somma 1)
  $$\hat r_i = \frac{r_i}{\sum_j r_j}$$
- Più alto è il rapporto, **più punti sintetici** si generano per quel punto: l'oversampling si concentra dove la minoritaria è più difficile da imparare
- Figura SMOTE vs ADASYN: con SMOTE i sintetici (gialli) sono distribuiti fra tutti i minoritari (rossi); con ADASYN se ne generano di più attorno ai minoritari circondati da maggioritari (blu)

### VAE (Variational Autoencoder)
- Permette di esplorare le variazioni nei dati non solo a caso ma **nella direzione desiderata** (la slide scrive "autoencorers")
- Un **autoencoder** è un **encoder** collegato a un **decoder**:
  - l'encoder trasforma l'input in una **rappresentazione più piccola e densa**
  - il decoder usa questa rappresentazione per **ricostruire l'input** originale
- Figura: input $x$ → strati dell'encoder → due vettori di "latent state distributions" (**media** e **varianza**) → campioni dalle distribuzioni → strati del decoder → ricostruzione $\hat x$
- Lo **spazio latente** di un autoencoder standard (dove finiscono i vettori codificati) può non essere continuo né permettere un'interpolazione facile; gli autoencoder standard imparano solo rappresentazioni compatte che ricostruiscono bene l'input
- Nei VAE lo spazio latente è **continuo per costruzione**, quindi campionamento e interpolazione casuali sono facili: l'encoder non produce un vettore ma **due vettori $\mu$ e $\sigma$**, parametri di una **gaussiana** da cui si campiona il codice da passare al decoder. Per l'oversampling si campionano nuovi punti nello spazio latente della classe minoritaria e li si decodifica
- (Le slide 23 e 24 sono identiche.)

## Ri-campionamento combinato con ensemble
### RUSBoost
- Combina **campionamento** dei dati e **boosting** (la slide dice "potenziamento")
- Deriva da **SMOTEBoost**, che crea esempi sintetici della minoritaria con SMOTE; RUSBoost sostituisce SMOTE con il **Random UnderSampling (RUS)**, che rimuove esempi della maggioritaria. (Precisazione: la slide è costruita in modo confuso, "è una variante di SMOTEBoost che crea nuovi esempi sintetici... mentre RUSBoost...": è SMOTEBoost a creare i sintetici, RUSBoost ne è la variante con RUS.)
- Molto simile ad **AdaBoost**: i pesi degli esempi originali partono da $1/m$ ($m$ = numero di esempi del training set); per $T$ iterazioni si crea un training set applicando il RUS sulla maggioritaria e si addestra un classificatore debole
- Rispetto a SMOTEBoost è **meno costoso** computazionalmente e in tempo

### HardEnsemble
- Figura: input data → **UnderSampling** con un algoritmo di editing, il **Reduced Reward-Punishment**; input data → **OverSampling** della minoritaria con **CSMOTE**; poi **Classification and Fusion**: combinazione degli $n$ classificatori RUSBoost con la **sum rule**
- **Osservazioni** di partenza:
  - sotto-campionare la maggioritaria può **buttare via dati utili**
  - sovra-campionare la minoritaria può **ridurre le prestazioni** se gli esempi usati per generare sono outlier
- **Componenti**:
  - **50 classificatori** su dati sovra-campionati e **100** su dati sotto-campionati, combinati con la **sum rule** (numeri scelti empiricamente)
  - quelli di sovra-campionamento si addestrano su dati generati con **CSMOTE** (5 volte i dati della classe minoritaria; correzione: la slide scrive "maggioritaria", ma il sovra-campionamento genera dati della minoritaria)
  - quelli di sotto-campionamento si addestrano su dati ottenuti con il **Reduced Reward-Punishment**, che rimuove i dati nelle **regioni di sovrapposizione** fra le classi

## Valutazione critica del sovra-campionamento
- Per capire se un metodo funziona: **sotto-campionare un dataset noto** e vedere quanto bene il metodo **ricostruisce** il dataset originale
- Figura (Cao, Tan, Pang, IEEE Transactions on Neural Networks and Learning Systems 25(12), 2014, 2226-2239): dataset bilanciato vero, versione sbilanciata, e le ricostruzioni con **SMOTE**, **B-SMOTE**, **ADASYN**, **DataBoost**, **2MoGT** e **SPO**. SMOTE, B-SMOTE e ADASYN generano punti solo attorno ai pochi minoritari rimasti; DataBoost e SPO spargono i sintetici su una regione molto più ampia della forma originale

## Cost-sensitive learning
- Ri-campionando si **alterano i dati di input**; nel sovra-campionamento si generano esempi che non sappiamo se esistano in natura
- Alternativa: il **cost-sensitive learning**, cioè addestrare assegnando **costi diversi ai diversi tipi di errore**
- Gli errori sulla **classe minoritaria** pesano **di più** di quelli sulla maggioritaria
- Così si corregge il pregiudizio verso la maggioritaria dei classificatori standard, il cui errore di training corrisponde all'**accuratezza** semplice non ponderata (la slide scrive "precisione semplice", ma intende l'accuratezza, non la precision)

### Dalla perdita al costo
- Tradizionalmente si addestra minimizzando gli errori: il fit è un **problema di ottimizzazione**, e la funzione che misura l'errore sul training set si chiama in generale **perdita** (loss)
- Nel cost-sensitive learning a una previsione errata si associa una **sanzione/peso**, detta **costo**; l'inverso della sanzione è il **beneficio**
- Obiettivo: **minimizzare il costo** del modello sul training set, assumendo che i diversi tipi di errore abbiano costi **diversi e noti**
- Classificazione sbilanciata e cost-sensitive learning sono strettamente legate (la prima si può affrontare con il secondo), ma il cost-sensitive learning è un campo a sé e il costo può essere più ampio dell'errore di previsione:
  - costo degli errori di classificazione (o di previsione in generale)
  - costo delle prove o della valutazione
  - costo di etichettatura
  - costo di calcolo, complessità computazionale
  - costo dell'instabilità o della varianza, noto come **deriva concettuale** (concept drift)
  - ...

### Matrice dei costi
- Si parte dalla **matrice di confusione** e si costruisce una **matrice dei costi**:
  - $C(+,+) = C(-,-) = 0$: la classificazione corretta non costa nulla
  - un errore costa più dell'altro: la slide scrive $C(+,-) > C(-,+)$, "il costo di un **falso positivo** è maggiore del costo di un **falso negativo**". (Correzione: con la classe minoritaria come positiva vale il contrario, il **falso negativo** deve costare di più, come dicono la slide precedente, dove gli errori sulla minoritaria pesano di più, e la successiva, dove il falso negativo costa 100 e il falso positivo 1.)
- La matrice si usa per **addestrare** o per **valutare** il modello
- In alcuni domini è ovvia, in altri difficile da definire; il costo può anche essere una funzione **multidimensionale** complessa

### Euristica: distribuzione inversa delle classi
- Buon punto di partenza: costi pari alla **distribuzione inversa delle classi**
- Esempio: rapporto 1:100 fra minoranza e maggioranza → costo di un **falso negativo = 100**, di un **falso positivo = 1**
- Euristica efficace, ma presuppone che la distribuzione osservata nel training set sia **rappresentativa** del problema reale e adatta al metodo cost-sensitive scelto

### Come usare la matrice dei costi
- per **guidare il ri-campionamento**
- per **addestrare** un modello di classificazione (figura: in training $F(X_{train}, params)$ produce $y_{pred}$, la loss $L(y_{true}, y_{pred}, costs)$ include i costi e aggiorna i parametri; in predizione $F(X_{test}, params)$ dà $y_{pred}$ come al solito)
- per **ripesare la decisione** di un modello probabilistico, calcolando il **rischio**
  $$L(x, i) = \sum_j P(j \mid x)\,C(i, j)$$
  dove $P(j \mid x)$ si ottiene con il **teorema di Bayes**. (Precisazione: $L(x,i)$ è il costo atteso di **assegnare** $x$ alla classe $i$, non il rischio che $x$ "sia" di classe $i$; si sceglie la classe con rischio minimo.)
- con un **ensemble** di modelli cost-insensitive, uno specifico per ogni classe

## Aggiunta: nomi nelle librerie
Non nelle slide, solo come riferimento per il progetto. Pacchetto **imbalanced-learn** (`imblearn`):
- sotto-campionamento: `under_sampling.RandomUnderSampler`, `TomekLinks`, `CondensedNearestNeighbour`, `EditedNearestNeighbours`, `NeighbourhoodCleaningRule`
- sovra-campionamento: `over_sampling.RandomOverSampler`, `SMOTE`, `BorderlineSMOTE`, `ADASYN`
- combinati: `combine.SMOTETomek`, `SMOTEENN`; ensemble: `ensemble.RUSBoostClassifier`
- cost-sensitive in scikit-learn: parametro `class_weight='balanced'` (pesi inversamente proporzionali alla frequenza delle classi, cioè l'euristica della distribuzione inversa) o `sample_weight` in `fit`
- il ri-campionamento va applicato **solo al training set** (con `imblearn.pipeline.Pipeline` dentro la cross-validation), mai al test set, altrimenti la valutazione è falsata

```python
from imblearn.over_sampling import SMOTE
from imblearn.pipeline import Pipeline
from sklearn.model_selection import cross_val_score

pipe = Pipeline([("smote", SMOTE(k_neighbors=5)), ("clf", clf)])
cross_val_score(pipe, X, y, scoring="f1")
```
