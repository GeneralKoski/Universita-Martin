# Classificazione: tecniche per la validazione

Fonte: `Validazione dei modelli di classificazione.pdf`

Il pacco è di 33 pagine (il piè di pagina dice "/ 32", l'ultima slide è numerata 33/32).

## Classificazione vs regressione (slide 2)
- **Regressione**: si costruisce un modello che predice un **valore numerico** di output dati uno o più valori **numerici** di input
- **Classificazione**: si predice la **classe** di un oggetto dati uno o più dati di input **di qualsiasi natura**
- Figura: *Regression Schema* (training data Size + Price; test data Size → prediction Price) vs *Classification Schema* (training data Height, Weight, Species; test data Height, Weight → prediction Species)
- Quindi gli strumenti per valutare un classificatore sono **sostanzialmente diversi** dalle metriche della regressione (tipicamente basate sul **calcolo numerico dell'errore**)

## Modello di validazione base (slide 3-5)
- Si dividono i dati disponibili in **training set** e **test set** secondo una certa **percentuale** (figura: barra con Training set "train and tune your model" e Test set "evaluate the model's performance")
- Nel training set le label servono ad **addestrare**; nel test set servono a **valutare la bontà**: il classificatore ha assegnato correttamente le label ai dati del test set?
- Altre domande di interesse:
  - il classificatore performa in modo **bilanciato** su tutti i tipi di label?
  - o ha delle **preferenze**? e da cosa dipendono?
- Si vogliono **indici matematici** che diano stime **oggettive** e permettano di **automatizzare** altre fasi di progettazione/sviluppo del classificatore
- Indici dall'aspetto più computazionale:
  - **Accuratezza**: bontà nel predire le etichette delle classi
  - **Robustezza**: capacità di gestire dati con **rumore** e **mancanti**
  - **Velocità**: tempo per costruire il modello (**training time**) e per usarlo (**classification/prediction time**)
  - **Scalabilità**: efficienza su dati in **memoria secondaria**
  - **Interpretabilità** dei risultati

## Precision e recall (slide 6-10)
- Si dividono i record in quattro insiemi in base all'esito della validazione. (La slide 6 dice "i dati del **training set**"; si tratta invece del **control/test set CS**, come dice la stessa slide subito dopo: "l'immagine rappresenta tutti e soli i record appartenenti a CS".)
- Caso binario: insieme delle classi $\mathbb{C} = \{A, B\}$; le misure si definiscono **relativamente a una delle due classi**
- $c : CS \mapsto \mathbb{C}$ = classe **reale** di ogni record $x \in CS$; $\tilde{c} : CS \mapsto \mathbb{C}$ = classe **assegnata** dal classificatore
- Figura: rettangolo dei record di CS; metà sinistra = **relevant elements** (punti pieni, classe reale A), metà destra = non rilevanti (punti vuoti); cerchio centrale = **selected elements** (classificati A). Dentro il cerchio a sinistra **true positives**, a destra **false positives**; fuori dal cerchio a sinistra **false negatives**, a destra **true negatives**
- Data la classe A (positiva):
  - **True Positive (TP)**: classificati **correttamente**, classe reale A: $\tilde{c}(x) = c(x) = A$
  - **True Negative (TN)**: classificati **correttamente**, classe reale B: $\tilde{c}(x) = c(x) = B$
  - **False Positive (FP)**: classificati **erroneamente** come A, classe reale B: $\tilde{c}(x) = A \neq B = c(x)$
  - **False Negative (FN)**: classificati **erroneamente** come B, classe reale A: $\tilde{c}(x) = B \neq A = c(x)$
  - (Nella slide 8 le definizioni di FP e FN sono **scambiate**: FP è descritto come "classe reale A, $\tilde{c}(x) = B$" e FN come "classe reale B, $\tilde{c}(x) = A$", e FN è anche siglato "(FP)". Quelle sopra sono le definizioni corrette, coerenti con la figura e con le formule di precision e recall.)
- **Record rilevanti**: tutti e soli i record di CS con classe reale uguale a quella investigata: $\{x \in CS : c(x) = A\}$
- **Precision** (precisione): frazione di elementi rilevanti fra tutti quelli **classificati come A**
$$Precision = \frac{TP}{TP + FP}$$
- **Recall** (recupero o **sensitività**): frazione di elementi rilevanti che sono stati classificati come A, fra **tutti gli elementi rilevanti**
$$Recall = \frac{TP}{TP + FN}$$
- Figura: Precision = (mezzo cerchio verde) / (cerchio intero verde+rosso); Recall = (mezzo cerchio verde) / (tutto il rettangolo sinistro dei rilevanti)
- Più alti precision e recall, migliore il classificatore; ma a volte serve **un solo indice**
- **F1-score**: **media armonica** di precision e recall
$$F_1 = 2\,\frac{Precision \cdot Recall}{Precision + Recall} = \frac{2TP}{2TP + FP + FN}$$
- Come precision e recall, $F_1 \in [0, 1]$, più alto è meglio; tuttavia valori **prossimi a 1** possono indicare **overfitting**

## Accuratezza (slide 11-12)
- **Accuratezza** (accuracy): oggetti correttamente classificati rispetto al totale degli oggetti del CS, cioè quanto il classificatore identifica o esclude correttamente gli oggetti da una classe
$$Accuracy = \frac{TP + TN}{TP + TN + FP + FN}$$
- **Poco indicata per dataset sbilanciati**. Esempio: 95 negativi e 5 positivi; un classificatore che assegna **sempre la classe negativa** ha accuratezza **95% (0.95)**
- In questi casi si usa la **balanced accuracy**:
$$Balanced\ accuracy = \frac{TPR + TNR}{2}$$
  - **TPR** (True Positive Rate) $= \frac{TP}{TP + FN}$, detta **sensitività**: quanto il classificatore è **sensibile** nel riconoscere una classe
  - **TNR** (True Negative Rate) $= \frac{TN}{TN + FP}$, detta **specificità**: quanto è **specifico** nel distinguere la classe dalle altre
  - Esempio delle slide rifatto con la balanced accuracy (calcolo aggiunto): TPR = 0/5 = 0, TNR = 95/95 = 1, balanced accuracy = 0.5, cioè quanto un classificatore casuale

## False discovery rate (slide 13)
- Misura molto usata in statistica per analizzare il tasso di **errori di tipo I** (rigettare un'ipotesi nulla vera) nei test con **confronti multipli**
- In classificazione:
$$FDR = \frac{FP}{FP + TP} = 1 - \frac{TP}{TP + FP}$$
  cioè $FDR = 1 - Precision$

## Matrice di confusione e indici: resumé (slide 14)
Matrice per classificatori binari (righe = classe **predetta**, colonne = classe **reale**):

| | Actual Positive | Actual Negative | |
|---|---|---|---|
| **Predicted Positive** | TP | FP (**Type I Error**) | **Precision** $= \frac{TP}{TP+FP}$ |
| **Predicted Negative** | FN (**Type II Error**) | TN | **Negative Predictive Value** $= \frac{TN}{TN+FN}$ |
| | **Recall/Sensitivity** $= \frac{TP}{TP+FN}$ | **Specificity** $= \frac{TN}{TN+FP}$ | **Accuracy** $= \frac{TP+TN}{TP+TN+FP+FN}$ |

- **ATTENZIONE**: sensitività, precisione, specificità e NPV sono **specifiche della classe** considerata; l'**accuratezza** è invece **invariante per classe**. (La slide scrive "NPR" e "casse": si intende NPV, Negative Predictive Value, come in tabella, e "classi".)

## AUC e curva ROC (slide 15-17)
- **AUC** (Area Under the Curve): area sotto la curva **ROC** (Receiver Operating Characteristics), usate per la prima volta nella **seconda guerra mondiale** da ingegneri elettrotecnici per individuare i nemici con il **radar** nelle battaglie aeree
- Figura: asse x = **FPR = 1 - Specificity**, asse y = **TPR / Recall / Sensitivity**; curva verde concava sopra la diagonale (**random model**), area sottesa = "Area Under Curve"
- **Curva ROC**: grafico delle coppie (FP, TP) al variare di un **parametro** del classificatore. Es. classificatore **a soglia**: per ogni valore della soglia si calcolano la frazione di veri positivi e quella di falsi positivi; i punti nello spazio FP-TP formano la curva. (Le coordinate sono i **tassi** FPR e TPR, cioè le frazioni, come nella figura, non i conteggi FP e TP.)
- Serve a valutare la capacità di **discernere**, es. aereo amico vs nemico, popolazione sana vs malata
- **Interpretazione probabilistica**: AUC $\in [0, 1]$ è la **probabilità** che il punteggio del classificatore su un individuo estratto a caso dai **malati** sia **superiore** a quello su un individuo estratto a caso dai **sani**
- Le curve ROC passano per **(0,0)** e **(1,1)**; due curve limite:
  - **retta a 45 gradi** per l'origine: **classificatore casuale**, AUC = **0,5**
  - spezzata (0,0) → (0,1) → (1,1): **classificatore perfetto**, AUC = **1**

## Classificazione a più di due classi (slide 18-19)
- Le misure viste nascono per il caso binario e non sono di facile applicazione al **multi-classe**
- Con 10 o più classi, precision e recall per classe dicono quanto il classificatore è bravo su **ogni singola classe** ma si perde la **visione globale**
- Per l'$F_1$ si possono mediare i valori per classe in (almeno) due modi: **micro** e **macro**
- Per ogni classe $g_i \in G = \{1, \dots, K\}$ si costruisce una matrice di confusione **centrata su $g_i$** (**one-vs-rest**): $g_i$ è il caso positivo, tutte le altre classi unite formano il negativo → valori $TP_i$, $FP_i$, $FN_i$

### Micro average (slide 20)
- Riassume le prestazioni sull'**unità più piccola** possibile, cioè su **tutti i campioni** (si sommano i conteggi prima di dividere):
$$P_{micro} = \frac{\sum_{i=1}^{|G|} TP_i}{\sum_{i=1}^{|G|}(TP_i + FP_i)} \qquad R_{micro} = \frac{\sum_{i=1}^{|G|} TP_i}{\sum_{i=1}^{|G|}(TP_i + FN_i)}$$
$$F_{1,micro} = 2\,\frac{P_{micro} \cdot R_{micro}}{P_{micro} + R_{micro}}$$
- Più grande è meglio, ma **non è sensibile** alle prestazioni sulle **singole classi**: può essere **fuorviante con classi sbilanciate** (dominano le classi numerose)

### Macro average (slide 21)
- Fa la media su gruppi più grandi, cioè sulle **performance per classe** invece che sulle osservazioni:
$$P_{macro} = \frac{1}{|G|}\sum_{i=1}^{|G|}\frac{TP_i}{TP_i + FP_i} = \frac{\sum_{i=1}^{|G|} P_i}{|G|} \qquad R_{macro} = \frac{1}{|G|}\sum_{i=1}^{|G|}\frac{TP_i}{TP_i + FN_i} = \frac{\sum_{i=1}^{|G|} R_i}{|G|}$$
$$F_{1,macro} = 2\,\frac{P_{macro} \cdot R_{macro}}{P_{macro} + R_{macro}}$$
- Un valore grande indica che il classificatore funziona bene **(in media) su ogni singola classe**: la macro-media è **più adatta a classi sbilanciate**

## Generalizzazione di AUC al multi-classe: metodo Hand & Till (slide 22-27)
(Hand & Till, *Machine Learning*, 45, 171-186, 2001.)
- Figura: quattro curve ROC one-vs-rest di un classificatore multi-classe (Ideal area ≈ 0.789, Premium ≈ 0.824, Good ≈ 0.857, Fair ≈ 0.814)
- Classi etichettate $0, 1, 2, \dots, c-1$ con $c > 2$; si considerano le **coppie di classi** $(i, j)$
- Un buon classificatore assegna **alta probabilità** alla classe corretta e **bassa** a quella sbagliata
- $\hat{A}(i|j)$: probabilità che un elemento scelto a caso dalla classe $j$ abbia probabilità stimata di appartenere alla classe $i$ **inferiore** a quella di un elemento scelto a caso dalla classe $i$ stessa; $\hat{A}(j|i)$ analoga
- Definizioni:
  - $\hat{p}(x_l)$ = probabilità stimata che l'osservazione $x_l$ provenga dalla classe $i$
  - per le osservazioni della classe $i$: $f_l = \hat{p}(x_l)$
  - per le osservazioni della classe $j$: $g_l = \hat{p}(x_l)$ (sempre probabilità di appartenere alla classe $i$)
- Si ordinano in modo **crescente** $\{g_1, \dots, g_{n_j}, f_1, \dots, f_{n_i}\}$; $r_l$ = **rango** della $l$-esima osservazione della classe $i$ (ordinate per rango crescente)
- Numero totale di coppie (punto di $j$, punto di $i$) in cui il punto di $j$ ha probabilità stimata **minore** del punto di $i$:
$$\sum_{l=1}^{n_i}(r_l - l) = \sum_{l=1}^{n_i} r_l - \sum_{l=1}^{n_i} l = S_i - \frac{n_i(n_i+1)}{2}$$
  con $S_i$ = **somma dei ranghi** delle osservazioni della classe $i$ (spiegazione aggiunta: $r_l - l$ conta quante osservazioni di $j$ precedono la $l$-esima di $i$; è la statistica di Mann-Whitney)
- Le coppie possibili sono $n_i n_j$, quindi:
$$\hat{A}(i|j) = \frac{S_i - n_i(n_i+1)/2}{n_i n_j}$$
  (La slide scrive "coppie del tipo $n_0 n_1$"; nella notazione generale sono $n_i n_j$.)
- Non si può distinguere $\hat{A}(i|j)$ da $\hat{A}(j|i)$, quindi la **misura di separabilità** delle classi $i$ e $j$ è
$$\hat{A}(i, j) = \frac{\hat{A}(i|j) + \hat{A}(j|i)}{2}$$
  (Nella slide il membro sinistro è scritto di nuovo $\hat{A}(i|j)$, che renderebbe la formula circolare; in Hand & Till è $\hat{A}(i, j)$.)
- **AUC globale multi-classe** = media sulle coppie:
$$M = \frac{2}{c(c-1)}\sum_{i<j}\hat{A}(i, j)$$
  Il fattore $\frac{2}{c(c-1)}$: ci sono $c(c-1)$ coppie ordinate distinte, ma interessa solo **metà** di esse (coppie non ordinate $i < j$)

### Esempio numerico (slide 27)
- Classi $i$ e $j$ con $n_j = 6$, $n_i = 7$
- Probabilità stimate di appartenere a $i$:
  - classe $j$: $\{0.42, 0.15, 0.30, 0.01, 0.04, 0.23\}$
  - classe $i$: $\{0.89, 0.67, 0.39, 0.57, 1, 0.96, 0.92\}$
- Ordinamento (rango fra parentesi per i punti di $i$): 0.01, 0.04, 0.15, 0.23, 0.30, **0.39 (6)**, 0.42, **0.57 (8)**, **0.67 (9)**, **0.89 (10)**, **0.92 (11)**, **0.96 (12)**, **1 (13)**
- $S_i = 6 + 8 + 9 + 10 + 11 + 12 + 13 = 69$
$$\hat{A}(i|j) = \frac{69 - (7 \cdot 8)/2}{7 \cdot 6} = \frac{69 - 28}{42} = \frac{41}{42} = 0.976$$
- Lettura (aggiunta): delle 42 coppie solo una è "invertita" (0.42 di $j$ sopra 0.39 di $i$), quindi separazione quasi perfetta
- (Nella slide la somma è scritta $\sum_{l=1}^{n_1}$; va letto $n_i$.)

## Cross-validazione (slide 28-30)
- Tecnica per validare modelli statistici, cioè valutare come i risultati si **generalizzeranno** a un insieme di dati **indipendente**
- Obiettivo: testare la capacità di prevedere **dati nuovi**, non usati nell'addestramento
- Serve soprattutto a valutare problemi di **overfitting** o di **selection bias**
- Può servire anche a **scegliere** fra più modelli di classificazione: in tal caso tutti i metodi vanno verificati **sugli stessi TS+CS**
- **Selection bias**: la scelta del training set è **viziata da fattori esterni** invece di rispecchiare una selezione imparziale. TS e CS dovrebbero essere prodotti con **campionamento uniforme** dell'universo delle osservazioni (figura: griglia con celle campionate sparse uniformemente, "Uniform sampling")
- Due famiglie:
  - **esaustiva**: addestramento e verifica su **tutti i possibili modi** di dividere il dataset in TS e CS
  - **non esaustiva**: solo un **sottoinsieme** delle divisioni possibili, generalmente scelte **a caso**

### Cross-validazione esaustiva (slide 31)
- **Leave-p-out**: dataset di $N$ osservazioni, $p$ come CS e le restanti $N - p$ come TS, ripetuto per **tutti i tagli possibili**: il modello viene testato $\binom{N}{p}$ volte. (La slide scrive $\binom{n}{p}$ con $n$ minuscolo; il dataset ha $N$ osservazioni.)
- Figura: righe di celle rosse (Train) con poche celle gialle (Test) in posizioni diverse a ogni ripetizione
- Con $p = 2$ è usata come metodo **unbiased** per stimare l'**AUC** di classificatori binari
- **Leave-one-out** ($p = 1$, $N$ ripetizioni): adatta con **pochi dati** o quando una stima accurata delle prestazioni conta più del **costo computazionale**

### Cross-validazione non esaustiva: k-fold (slide 32)
- La più usata: il dataset è diviso in $k$ parti di **uguale dimensione**; a turno ogni parte è il CS e le restanti $k-1$ sono il TS
- Figura: Dataset → "Create stratified folds" (5 fold, ognuno con una porzione Test diversa) → "Repeat for each fold": Train → Learn model → Model → Apply model sul Test → Calculate metrics → **Stored metrics**
- Ogni fold deve essere **unbiased**: metodo comune è **mescolare a caso** il dataset e verificare che le osservazioni delle varie classi siano distribuite in modo più o meno **uniforme**

### Stratified k-fold (slide 33)
- Variante del KFold che restituisce **fold stratificati**: ogni fold preserva la **percentuale di campioni di ciascuna classe** in $y$, in classificazione binaria o multiclasse
- Figura *StratifiedKFold*: 100 campioni, 4 iterazioni di CV (testing set in rosso, training set in blu), 3 classi sbilanciate (circa 10, 30 e 60 campioni); a ogni iterazione il test set prende un pezzo **di ogni classe** in proporzione

## Da ricordare per lo scritto
- TP/TN/FP/FN rispetto a una classe positiva: **FP** = predetto positivo ma reale negativo (errore di **tipo I**), **FN** = predetto negativo ma reale positivo (errore di **tipo II**)
- $Precision = \frac{TP}{TP+FP}$, $Recall = Sensitività = TPR = \frac{TP}{TP+FN}$, $Specificità = TNR = \frac{TN}{TN+FP}$, $NPV = \frac{TN}{TN+FN}$, $FDR = \frac{FP}{FP+TP} = 1 - Precision$
- $F_1$ = media armonica $= \frac{2TP}{2TP+FP+FN}$; valori vicini a 1 possono segnalare overfitting
- $Accuracy = \frac{TP+TN}{tot}$, invariante per classe ma ingannevole su dati sbilanciati (95/5 → 95% con classificatore costante); usare $\frac{TPR+TNR}{2}$
- ROC: TPR vs FPR al variare della soglia, passa per (0,0) e (1,1); AUC = 0,5 casuale, 1 perfetto; AUC = P(punteggio di un positivo a caso > punteggio di un negativo a caso)
- Multi-classe: one-vs-rest; **micro** somma i conteggi (dominano le classi grandi, fuorviante se sbilanciato), **macro** media le metriche per classe (più adatta a classi sbilanciate)
- Hand & Till: $\hat{A}(i|j) = \frac{S_i - n_i(n_i+1)/2}{n_i n_j}$, $\hat{A}(i,j)$ = media dei due versi, $M = \frac{2}{c(c-1)}\sum_{i<j}\hat{A}(i,j)$; esempio $41/42 = 0.976$
- Cross-validazione contro overfitting e selection bias; per confrontare modelli usare gli stessi TS+CS; esaustiva (leave-p-out, $\binom{N}{p}$ test; leave-one-out) vs non esaustiva (k-fold, stratified k-fold)
