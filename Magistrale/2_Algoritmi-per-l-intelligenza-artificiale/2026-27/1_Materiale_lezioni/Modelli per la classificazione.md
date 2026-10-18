# Algoritmi di classificazione

Fonte: `Modelli per la classificazione.pdf`

Il pacco è di 105 pagine (il piè di pagina dice "/ 1": i numeri di slide qui sotto sono quelli di pagina).

## Classificazione eager e lazy (slide 2-4)
- Due tipologie di modelli:
  - **eager** (volenterosi): costruiscono dai dati di addestramento un **modello generale**, indipendente dall'input, poi usato per classificare i nuovi dati
  - **lazy** (pigri): **memorizzano** i dati di addestramento in forma grezza (o con piccole elaborazioni) e rimandano tutta la classificazione **all'arrivo della nuova istanza**
- **Tempo**: i lazy richiedono **meno tempo in addestramento** ma **molto più tempo in classificazione** (figure: topo che dorme su un panino / Topolino che va a scuola)
- **Accuratezza**: i lazy usano uno **spazio delle ipotesi più ricco**, perché usano direttamente **funzioni locali** di classificazione che danno poi approssimazioni a livello globale; gli eager usano **una sola ipotesi** per tutto l'universo delle osservazioni
- Approcci tipicamente lazy:
  - **k-nearest neighbors (kNN)**: data point in uno spazio euclideo (ma sono possibili altre rappresentazioni)
  - **locally weighted regression**: costruisce approssimazioni locali
  - **case-based reasoning**: rappresentazione simbolica e inferenza basata sulla conoscenza (**knowledge-based inference**)
- Nel corso si vede **solo il kNN**

## k-nearest neighbors (slide 5-9)
- Osservazioni = **data point** in uno spazio **$n$-dimensionale**; ogni dimensione ha valori reali o discreti
- Spazio **euclideo** con **distanze euclidee**; con feature **categoriali** serve un'altra metrica: **Jaccard, Tanimoto, Dice, Hamming** o **distanza del coseno**
- Figura: due nuvole (punti blu, quadrati verdi) e un punto rosso da classificare con K = 3
- **Regola**: dato un TS e un'istanza da classificare, le si assegna la classe **più rappresentata fra i suoi $k$ vicini più prossimi**; $k$ è il **parametro chiave**
- Figura: nuovo esempio "?" fra stelle rosse (Class A) e triangoli verdi (Class B), con i cerchi dei vicini per $k = 3$ e $k = 7$: cambiando $k$ può cambiare la classe assegnata
- kNN è **non parametrico**: non fa **alcuna ipotesi sulla distribuzione** dei dati; la struttura del modello è determinata dai dati. Utile perché nel "mondo reale" la maggior parte dei dati non rispetta gli assunti teorici tipici (es. regressione lineare)
- Quindi kNN dovrebbe essere fra le **prime scelte** quando c'è poca o nessuna conoscenza a priori sulla distribuzione dei dati

### Potere predittivo e scelta di k (slide 8)
- **$k$ piccolo**: si limita la regione della previsione e il classificatore diventa "**più cieco**" rispetto alla distribuzione generale (sensibile al rumore)
- **$k$ grande**: riduce l'impatto della **varianza** dovuta all'errore casuale, ma rischia di **ignorare piccoli dettagli** rilevanti
- Euristiche: $k = \sqrt{n}$ (radice del numero di osservazioni del training set), oppure scegliere $k$ con la **cross-validazione**

### Weighted kNN (slide 9)
- I voti dei vicini sono **pesati in base alla distanza** (tipicamente con peso $1/d$)
- Figura: stella da classificare con 3 vicini "o" a distanze $d_1, d_2, d_3$ e 2 vicini "x" a distanze $d_4, d_5$; si confrontano $o: \frac{1}{d_1} + \frac{1}{d_2} + \frac{1}{d_3}$ e $x: \frac{1}{d_4} + \frac{1}{d_5}$ → predict **o**
- Per dataset **sbilanciati**: pesare il contributo di ogni vicino con l'**inverso del numero totale di punti** del dataset che hanno la **sua stessa classe**

## Alberi di decisione (slide 10-15)
- Un albero di decisione è un albero di ricerca (**$n$-ario**): le **foglie** sono le classificazioni, i **rami** l'insieme delle proprietà che portano a esse
- Ogni **nodo interno** contiene un **test** che stabilisce quale sotto-albero visitare; il test valuta una feature (booleana, numerica, categoriale, ...) o combinazioni di feature
- Figura: piano diviso da tagli paralleli agli assi (punti rossi e blu in quadranti) e albero corrispondente (Outlook → Wind / Humidity con soglia 77.500 → foglie yes/no)

### Costruzione (slide 11-12)
Si parte da un **nodo radice** con tutti i dati di addestramento:
1. se tutti i dati del nodo $t$ hanno lo **stesso valore dell'attributo classe**, si crea un **nodo foglia** con tutti i dati
2. altrimenti, con una **misura di goodness**, si effettua una **partizione** $S$ degli elementi del nodo
3. si sceglie la partizione $S^*$ che (ad esempio) **massimizza** la goodness
4. si creano tanti **figli** di $t$ quanti sono i sottoinsiemi della partizione $S^*$. (La slide dice "quante sono le **classi** presenti in $S^*$"; i figli corrispondono alle parti della partizione, cioè agli esiti del test, non alle classi.)
5. un figlio è **puro** se tutti i suoi elementi hanno lo stesso valore dell'attributo classe
6. si applicano **ricorsivamente** i passi sui nodi **impuri** o che non rappresentano una singola classe secondo una **soglia di maggioranza**

- **Obiettivi**: fra tutti gli alberi scegliere il **più semplice a parità di performance**; albero il più **compatto** possibile
- **Ostacolo**: trovare l'ipotesi consistente **minimale** è **NP-hard**
- **Soluzione**: strategia ricorsiva **divide-et-impera**, ma **greedy**, senza garanzia di ottimalità. **Decisione principale**: scegliere l'attributo su cui biforcare in modo che
  - divida in insiemi il più possibile **puri**
  - porti **più rapidamente** a nodi foglia

### Esempio: giocare o no in base al meteo (slide 13-15)
Dataset di 14 record (9 P = play, 5 N = don't play):

| Outlook | Temperature | Humidity | Windy | Class |
|---|---|---|---|---|
| sunny | hot | high | false | N |
| sunny | hot | high | true | N |
| overcast | hot | high | false | P |
| rain | mild | high | false | P |
| rain | cool | normal | false | P |
| rain | cool | normal | true | N |
| overcast | cool | normal | true | P |
| sunny | mild | high | false | N |
| sunny | cool | normal | false | P |
| rain | mild | normal | false | P |
| sunny | mild | normal | true | P |
| overcast | mild | high | true | P |
| overcast | hot | normal | false | P |
| rain | mild | high | true | N |

- **Albero poco minimale** (radice *temperature*): cool / mild / hot, poi outlook, windy, humidity ripetuti in più rami; evidenziata la regola **IF (temperature = cool AND outlook = rain AND windy = false) THEN play**
- **Albero decisamente migliore** (radice *outlook*):

```
outlook =?
├─ sunny    → humidity =?
│             ├─ high   → N
│             └─ normal → P
├─ overcast → P
└─ rain     → windy =?
              ├─ true  → N
              └─ false → P
```

## Goodness function (slide 16)
- **Information gain** (**ID3, C4.5**):
  - tutti gli attributi sono **categorici**
  - modificabile per attributi a valori continui
- **Indice di Gini** (**CART**):
  - tutti gli attributi a valori **continui**
  - assume che esistano **diversi valori di splitting** per ogni attributo
  - può richiedere altri metodi, ad esempio **clustering**
  - modificabile per attributi categorici

## Information gain (slide 17-29)
- Mira alla **riduzione progressiva dell'entropia**; la **purezza** misura quanto un insieme è vicino alla situazione ideale di **una sola etichetta**
- **Ripasso**: $X$ assume $k$ valori $x_i$ con probabilità $p_i$; $H(p_1, \dots, p_k)$ è l'**incertezza media** rimossa all'accadere di un $x_i$, misura il **disordine**; è massima con eventi **equiprobabili** (nessuna struttura, massimo disordine):
$$H = -\sum_i p_i \log_b p_i$$
- **Due classi** P e N, $S$ con $p$ elementi di P e $n$ di N. Informazione necessaria per decidere se un esempio di $S$ sta in P o N:
$$Info(p, n) = -\frac{p}{p+n}\log_2\frac{p}{p+n} - \frac{n}{p+n}\log_2\frac{n}{p+n}$$
- Attributo $A$ con valori $\{a_1, \dots, a_v\}$ come radice: $S$ si partiziona in $\{S_1, \dots, S_v\}$, P e N in $\{P_1, \dots, P_v\}$ e $\{N_1, \dots, N_v\}$; se $S_i$ ha $p_i$ elementi di P e $n_i$ di N serve $Info(p_i, n_i)$. Informazione per l'albero con radice $A$ (**media pesata**):
$$Info_A(S) = \sum_{i=1}^{v}\frac{p_i + n_i}{p + n}\,Info(p_i, n_i)$$
- **Caso generale** con $k$ classi $C_1, \dots, C_k$ (**entropia dell'insieme** $S$, informazione media necessaria per identificare la classe di un record di $S$):
$$Info(S) = -\sum_{i=1}^{k}\frac{freq(C_i, S)}{|S|}\log_2\frac{freq(C_i, S)}{|S|}$$
- Partizionando $S$ con il test su $A$ (valori $a_1, \dots, a_n$), l'entropia è la **media ponderata** delle entropie dei sottoinsiemi:
$$Info_A(S) = \sum_{i=1}^{n}\frac{|S_i|}{|S|}\,Info(S_i)$$
- **Information gain**:
$$Gain(A) = Info(S) - Info_A(S)$$
- Si sceglie l'attributo con **gain massimo**, cioè con $Info_A(S)$ **minimo**, perché $Info(S)$ è lo stesso per tutti gli attributi del nodo

### Esempio meteo (slide 22)
- $gain(outlook) = 0.246$, $gain(humidity) = 0.151$, $gain(windy) = 0.048$, $gain(temperature) = 0.029$ → **outlook** è la radice. (Nella slide è scritto "0.0.48": refuso per 0.048.)
- Figura: tabella riordinata per outlook (overcast 4 P; rain 3 P e 2 N; sunny 2 P e 3 N) accanto all'albero migliore
- Verifica (calcolo aggiunto): $Info(S) = Info(9, 5) = 0.940$; $Info_{outlook}(S) = \frac{5}{14}Info(2,3) + \frac{4}{14}Info(4,0) + \frac{5}{14}Info(3,2) = \frac{5}{14}0.971 + 0 + \frac{5}{14}0.971 = 0.694$; $Gain = 0.940 - 0.694 = 0.246$

### Gain ratio (slide 23-26)
- **Problema**: l'information gain è **sbilanciato a favore dei test con molti esiti**. Un test molto discriminante ma su un attributo con **pochi valori** può essere scartato a favore di un test con **molti esiti** poco significativi
- **Soluzione**: **normalizzare** il gain con l'informazione della divisione stessa
- Informazione di un messaggio sulla divisione di $S$ negli $S_i$: $-\log_2\frac{|S_i|}{|S|}$; per analogia con $Info(S)$:
$$SplitInfo(A) = -\sum_{i=1}^{n}\frac{|S_i|}{|S|}\log_2\frac{|S_i|}{|S|}$$
  (potenziale informazione generata dalla divisione di $S$)
$$GainRatio(A) = \frac{Gain(A)}{SplitInfo(A)}$$
- Figura "Go out to play?": radice 30 P / 70 N ($Info(S)$); Weather = Sunny → 25 P / 10 N, Weather = Rainy → 5 P / 60 N ($Info_A(S)$); la divisione 35/65 dà $SplitInfo$
  - Calcolo aggiunto: $Info(S) = 0.881$; $Info(25,10) = 0.863$, $Info(5,60) = 0.391$; $Info_A(S) = 0.35 \cdot 0.863 + 0.65 \cdot 0.391 = 0.556$; $Gain = 0.325$; $SplitInfo = H(0.35, 0.65) = 0.934$; $GainRatio = 0.348$
- **GainRatio non risolve tutto**: può sfavorire attributi significativi che hanno solo qualche valore in più. Strategia usuale:
  1. calcolare il **gain** per ogni attributo
  2. calcolare la **media** dei gain
  3. tenere **SOLO** gli attributi con gain **sopra la media**
  4. fra questi scegliere quello con **GainRatio maggiore**

### Attributi continui (slide 27)
- Il test è un confronto con un **valore soglia** $Z$: due esiti, $A > Z$ oppure $A \le Z$
- Restrizione: in ogni divisione i due insiemi risultanti devono avere un **numero minimo** di elementi
- La soglia si cerca valutando **tutti i valori** assunti dall'attributo nel training set, ordinati $\{v_1, \dots, v_m\}$: scelta $v_i$ come soglia, si partiziona in $\{v_1, \dots, v_i\}$ e $\{v_{i+1}, \dots, v_m\}$ (nella slide "$vi + 2$" è un refuso per $v_{i+2}$)

### Attributi con valori mancanti (slide 28-29)
- Possibilità: assegnare il **valore più comune**, oppure assegnare una **probabilità** a ciascun valore possibile
- Il gain si riscrive:
$$Gain(A) = F \cdot (Info(S) - Info_A(S))$$
  con $F$ = **frazione** di casi del training set in cui $A$ è **noto**
- Vanno ricalcolati $SplitInfo$ e quindi $GainRatio$, con effetto sul partizionamento (la slide scrive $SplitInfo(S)$; è $SplitInfo(A)$)
- Si possono anche **pesare i record**: un record con valore sconosciuto ha come peso la **probabilità che il valore sia $v_i$**. Gli $S_i$ diventano collezioni di casi con **pesi frazionari** e $|S_i|$ si reinterpreta come **somma dei pesi**
- In generale un caso con peso $w$ ed esito sconosciuto va in ogni $S_i$ con peso $w \cdot P(\text{esito} = v_i)$

## Indice di Gini (slide 30-35)
- Insieme $S$ con $n$ classi, $p_j$ = frequenza della classe $j$:
$$gini(S) = 1 - \sum_{j=1}^{n} p_j^2$$
- Esempio due classi P e N con $p$ e $n$ elementi: $p_P = \frac{p}{p+n}$, $p_N = \frac{n}{n+p}$, $gini(S) = 1 - p_P^2 - p_N^2$
- **Gini dello split** se l'attributo $a$ divide $S$ in $S_1, S_2$ di dimensioni $N_1, N_2$:
$$gini_{split}(S, a) = \frac{N_1}{N}gini(S_1) + \frac{N_2}{N}gini(S_2)$$
  (la slide dice "dove $c$ è l'attributo": refuso per $a$). In generale, con $m$ sottoinsiemi:
$$gini_{split}(S, a) = \sum_{i=1}^{m}\frac{N_i}{N}gini(S_i)$$
- Si sceglie l'attributo con il **minore** $gini_{split}$ (al contrario del gain, che si massimizza)

### Esempio CART su attributo numerico (slide 32-35)
Per attributi numerici (interi) si valutano **tutti i possibili split binari** definiti dai valori.

| RID | Age | Car Type | Risk |
|---|---|---|---|
| 0 | 23 | family | high |
| 1 | 17 | sport | high |
| 2 | 43 | sport | high |
| 3 | 68 | family | low |
| 4 | 32 | truck | low |
| 5 | 20 | family | high |

- Figura anche con le **attribute list** ordinate: Age (17 h, 20 h, 23 h, 32 l, 43 h, 68 l) e Car Type
- Split candidati: $Age \le 17, 20, 23, 32, 43, 68$
- $Age \le 17$ (1 high / 0 low vs 3 high / 2 low):
  - $G(\le 17) = 1 - (1^2 + 0^2) = 0$
  - $G(> 17) = 1 - ((3/5)^2 + (2/5)^2) = 1 - 13/25 = 12/25$ (la slide scrive $1 - (13/25)^2$; il quadrato è di troppo, il risultato 12/25 è giusto)
  - $G_{SPLIT} = \frac{1}{6} \cdot 0 + \frac{5}{6} \cdot \frac{12}{25} = \frac{2}{5}$
- $Age \le 20$ (2/0 vs 2/2):
  - $G(\le 20) = 0$, $G(> 20) = 1 - ((1/2)^2 + (1/2)^2) = 1/2$
  - $G_{SPLIT} = \frac{2}{6} \cdot 0 + \frac{4}{6} \cdot \frac{1}{2} = \frac{1}{3}$ (la slide scrive $\frac{4}{6} \cdot \frac{1}{8}$; dovrebbe essere $\frac{1}{2}$, il risultato 1/3 è giusto)
- $Age \le 23$ (3/0 vs 1/2):
  - $G(\le 23) = 0$, $G(> 23) = 1 - ((1/3)^2 + (2/3)^2) = 1 - 1/9 - 4/9 = 4/9$
  - $G_{SPLIT} = \frac{3}{6} \cdot 0 + \frac{3}{6} \cdot \frac{4}{9} = \frac{2}{9} \approx 0.222$
- $Age \le 32$ (3/1 vs 1/1):
  - $G(\le 32) = 1 - ((3/4)^2 + (1/4)^2) = 1 - 10/16 = 3/8$, $G(> 32) = 1/2$
  - $G_{SPLIT} = \frac{4}{6} \cdot \frac{3}{8} + \frac{2}{6} \cdot \frac{1}{2} = \frac{1}{4} + \frac{1}{6} = \frac{5}{12} \approx 0.417$ (la slide scrive $\frac{1}{8} + \frac{1}{6} = \frac{14}{48} = \frac{7}{24}$: $\frac{4}{6} \cdot \frac{3}{8}$ fa $\frac{1}{4}$, non $\frac{1}{8}$; la conclusione non cambia)
- Le slide non calcolano gli ultimi due (calcolo aggiunto): $Age \le 43$ (4/1 vs 0/1) → $\frac{5}{6} \cdot \frac{8}{25} = \frac{4}{15} \approx 0.267$; $Age \le 68$ non divide nulla → $gini(S) = 4/9$
- Il **minimo** $G_{SPLIT}$ è per **$Age \le 23$**

## Pruning (slide 36-40)
- **Problema**: molti attributi o una particolare distribuzione dei valori fanno **crescere molto l'albero**: è **overfitting**, che rende più difficile la classificazione (anche a causa di **outlier**) ed è associato a un aumento ingiustificato di errori
- **Soluzione**: **pruning** (potatura), rimuovere i rami che non contribuiscono a una corretta classificazione → albero meno complesso e più comprensibile
- Due strategie:
  - **pre-pruning**: durante la costruzione si decide se dividere ancora un sottoinsieme; es. soglia $t$ sul gain (si troncano i rami con gain $< t$) oppure **metodi statistici**
  - **post-pruning**: si recidono rami ad albero **già costruito**
- Il post-pruning è più **dispendioso** ma permette un'analisi più approfondita e produce un albero più realistico; **C4.5** fa post-pruning
- Figura: albero $A_1? \to A_2?, A_3? \to A_4?, A_5?$ con foglie class A/B; nella versione potata il sottoalbero di $A_3?$ è sostituito dalla foglia **class B**
- **Problema**: potando si classificano male alcuni casi, quindi le foglie non contengono più una sola classe. **Soluzione**: ogni foglia riporta una **distribuzione di classe**, cioè per ogni classe la **probabilità** che un caso vi appartenga; può migliorare la determinazione della classe più probabile per un caso non visto
- **C4.5**: oltre a sostituire un sottoalbero con **una foglia**, può sostituire un sottoalbero con **un suo ramo**
  - Se si sa predire il tasso d'errore di un albero e dei sottoalberi, si pota in funzione della **variazione di errore predetto** sull'intero albero
  - Usa il training set e la **potatura "pessimistica"**: scopo ridurre l'errore totale; se l'**errore medio** del sottoalbero dopo aver annullato un test (nodo interno) è minore di quello con il test, il nodo viene potato con tutto il suo sottoalbero

## Minimal cost-complexity pruning (slide 41-45)
- Potatura parametrizzata da $\alpha \ge 0$, **parametro di complessità**; misura di costo-complessità di un albero $T$:
$$R_\alpha(T) = R(T) + \alpha|\widetilde{T}|$$
  con $|\widetilde{T}|$ = numero di **nodi terminali** (foglie) e $R(T)$ = tasso d'errore (impurità) dei nodi terminali
- Si cerca il **sottoalbero di $T$ che minimizza $R_\alpha(T)$**
- Costo di un **singolo nodo**: $R_\alpha(t) = R(t)$ (più precisamente $R(t) + \alpha$, visto che il nodo diventa una foglia: aggiunta esplicativa). Il **ramo** $T_t$ è l'albero con radice $t$
- In generale $R(T_t) < R(t)$ (l'impurità del nodo è maggiore della somma di quelle delle foglie del suo ramo), ma i costi di $t$ e $T_t$ possono diventare **uguali** per un certo $\alpha$
- **$\alpha$ effettivo** di $t$: l'$\alpha$ per cui $R_\alpha(T_t) = R_\alpha(t)$:
$$\alpha_{eff} = \frac{R(t) - R(T_t)}{|\widetilde{T}_t| - 1}$$
  (La slide scrive al denominatore $|T| - 1$; è il numero di foglie **del ramo** $T_t$ meno uno.)
- Si pota il nodo non terminale con **$\alpha_{eff}$ minimo**; ci si ferma quando l'$\alpha_{eff}$ minimo supera una **soglia**
- Figure (esempio con alberi di scikit-learn):
  - *Total impurity vs effective alpha*: all'aumentare di $\alpha$ si pota di più e l'**impurità totale delle foglie cresce** (da 0 a circa 0.14 per $\alpha \approx 0.034$)
  - *Number of nodes / Depth vs alpha*: **nodi** (da circa 31 a 1) e **profondità** (da 8 a 1) **diminuiscono** all'aumentare di $\alpha$
  - *Accuracy vs alpha*: con soglia **0** l'albero è in **overfitting**, accuratezza di training **100%** e di test **88%**; aumentando $\alpha$ l'accuratezza di test sale (picco circa 0.94 per $\alpha \approx 0.01$-$0.02$) e l'albero **generalizza meglio**, mentre per $\alpha$ troppo grande calano entrambe

## Metodi consenso (slide 46-49)
- Alberi: **semplici**, **interpretabili**, **efficienti**, ma in genere **non competitivi** in qualità di predizione; inoltre **instabili**: piccoli cambi nei dati cambiano molto l'albero, quindi **alta varianza**
- Rimedi: **bagging**, **random forests**, **boosting**: costruiscono **molti alberi** combinati in una **predizione consenso**; molta più **accuratezza** al prezzo di una **perdita parziale di interpretabilità**
- In generale si usa un modello combinato $M^*$ da $k$ modelli addestrati separatamente (figura: Data → $C_1, C_2, \dots, C_T$ → Combine votes, con New data sample → Class prediction)
  - **bagging**: si **media** la predizione su una collezione di classificatori
  - **boosting**: collezione di classificatori con **voto pesato**
  - **ensemble**: combinazione di un insieme **eterogeneo** di classificatori

### Bagging (slide 48-49)
- **Bootstrap aggregation**: tecnica generale per **ridurre la varianza** di un metodo di apprendimento o per **stimare l'accuratezza** di uno stimatore; particolarmente utile con gli alberi
- Idealmente con più insiemi di osservazioni si addestrerebbe un albero per insieme e si combinerebbe (media o voto di maggioranza); ma di solito c'è **un solo insieme**
- **Bootstrap**: si estraggono **casualmente $B$ sottoinsiemi** dall'unico training set per simulare la variabilità dei dati; si addestra un classificatore $f_i$ per ciascuno; si aggregano le predizioni:
$$f_{bag}(x) = \frac{1}{B}\sum_{i=1}^{B} f_i(x)$$
- Figura: Original Data → Bootstrapping (campioni colorati con ripetizioni) → un Classifier per campione → Aggregating → Ensemble classifier

## Random forest (slide 50-64)
- Consenso costituito da un **bagging di alberi di decisione non potati** (non-pruned) e complessi, con **scelta casuale di un sottoinsieme delle feature** (predittori) **a ogni split**
- Figura: Instance → Tree-1 (Class-A), Tree-2 (Class-A), ..., Tree-n (Class-B) → **Majority-Voting** → Final-Class (A)
- Metodo **non lineare** e **robusto**, **bassa varianza**, predizioni **stabili** al variare dei dati; migliora il singolo albero appreso su tutti i dati; **perde la facile interpretabilità** e scala meno bene

### Addestramento e predizione (slide 52-53)
Fissati $n_{tree}$ e il numero $m_{try}$ di predittori da scegliere a caso, per $n_{tree}$ volte:
1. scegli un **sottoinsieme bootstrap** $S$ dai dati di training
2. apprendi su $S$ un albero **accurato** ($minsplit = 1$) in cui a ogni split solo $m_{try}$ predittori, scelti **a caso** fra quelli disponibili, sono candidati
3. **non** fare pruning
4. salva l'albero

- **Predizione**: come nel bagging, **voto di maggioranza** degli $n_{tree}$ alberi (classificazione) o **media** (regressione)
- Di solito $m_{try} = m/3$ per la **regressione** e $m_{try} = \sqrt{m}$ per la **classificazione**, con $m$ = numero totale di predittori

### Proprietà (slide 54)
- **Scalabilità**: aumento contenuto della complessità temporale rispetto agli alberi (ogni albero vede un sottoinsieme dei dati e, a ogni split, dei predittori); gestisce dati grandi prima di rallentare in modo evidente
- **Nessun overfitting all'aumentare del numero di alberi**, perché a ogni split si usa solo una piccola parte dei predittori e si predice per aggregazione
- Più **stabile** alle variazioni dei dati grazie al bagging
- Alberi **indipendenti** (a differenza del boosting) → facilmente **parallelizzabile** (più core o processori)

### Una costruzione più raffinata: perché funziona (slide 55-60)
- Il bagging fa la **media di molti modelli rumorosi ma approssimativamente non distorti** per **ridurre la varianza**. Gli alberi sono candidati ideali: catturano interazioni complesse e, se profondi, hanno **bassa distorsione** (bias); essendo molto soggetti a errore beneficiano molto della media
- Gli alberi del bagging sono **identicamente distribuiti** (i.d.): il valore atteso della media di $B$ alberi è quello di uno qualunque di essi, quindi il **bias** degli alberi "bagged" è quello del singolo albero e si migliora **solo riducendo la varianza**
- Media di $B$ variabili **i.i.d.** con varianza $\sigma^2$: varianza $\frac{1}{B}\sigma^2$
- Se sono solo **i.d.** con correlazione a coppie $\rho > 0$:
$$\rho\sigma^2 + \frac{1-\rho}{B}\sigma^2$$
  Al crescere di $B$ il secondo termine si annulla ma il primo resta: la **correlazione fra alberi limita il beneficio** della media. Le random forest **riducono la correlazione** fra gli alberi senza aumentare troppo la varianza, tramite la **selezione casuale delle variabili** di input
- Prima di ogni split si scelgono a caso $m \le p$ variabili candidate; $m$ va da $p$ a valori molto piccoli (anche 1), valore usuale $p/3$. (Qui la slide dà $p/3$ senza distinguere; secondo la slide 53, e secondo la letteratura, $p/3$ è il default per la regressione, mentre per la classificazione si usa $\sqrt{p}$.)
- Dopo aver costruito $B$ alberi $\{T_b(x; \theta_b)\}_1^B$, il predittore è
$$\hat{f}_{rf}^B(x) = \frac{1}{B}\sum_{b=1}^{B} T_b(x; \theta_b)$$
  dove $\theta_b$ caratterizza il $b$-esimo albero (variabili di split, punti di split, valori delle foglie) e $T_b(x; \theta_b)$ è la sua previsione
- **Ridurre $m$ riduce la correlazione** fra coppie di alberi, quindi la varianza della media

```
Per b = 1 ... B:
  a. estrai un campione bootstrap Z* di dimensione N dai dati di training
  b. fai crescere un albero T_b sui dati bootstrapped, ripetendo ricorsivamente
     per ogni nodo terminale, finché si raggiunge la dimensione minima n_min:
       i.   seleziona m variabili a caso fra le p
       ii.  scegli la migliore variabile e il miglior punto di split fra le m
       iii. dividi il nodo in due nodi figli
Ritorna l'insieme degli alberi {T_b}, b = 1 ... B
```

### Numero di alberi, OOB e importanza delle variabili (slide 61-62)
- **100 alberi o più** sono di solito un buon compromesso fra tempo di training e potere predittivo, ma dipende da numero di attributi, rumore e dipendenza fra feature. Figura: errore vs numero di alberi (0-500), crolla da circa 50 a circa 10 nei primi alberi e poi si stabilizza
- **Out Of Bag (OOB) error**: stima dell'errore di test, media degli errori di predizione su ogni istanza di training $x_i$ usando **solo gli alberi che non avevano $x_i$** nel proprio campione bootstrap
- **Importanza delle variabili**, due strategie:
  - **Mean decrease in accuracy**: si calcola l'accuratezza sui dati OOB; poi, per ogni albero e ogni variabile $i$, si **permuta la colonna $i$** dei dati OOB (si rompe la correlazione con l'outcome), si ripredice e si misura il **calo di accuratezza**; si media sugli alberi
  - **Mean decrease in the Gini index**: per ogni albero e variabile $i$, per ogni nodo il cui split usa $i$ si calcola la **diminuzione dell'indice di Gini** prima/dopo lo split, pesata per il numero di istanze nel nodo; si media sugli alberi

### Quando evitarle, vantaggi e svantaggi (slide 63-64)
- **Estrapolazione**: la regressione con random forest non estrapola oltre l'intervallo osservato (la regressione lineare sì): per questo le RF si usano soprattutto in classificazione
- **Dati scarsi**: con pochi dati, sottoinsieme di feature e campione bootstrap producono uno **spazio invariante** → split improduttivi
- **Vantaggi**: regressione e classificazione; buone predizioni "comprese facilmente" (così la slide 64, in contrasto con la slide 51 che dice che le RF perdono la facile interpretabilità degli alberi); gestiscono dataset grandi; più precise di un singolo albero
- **Svantaggi**: più risorse di calcolo; più tempo di un singolo albero al crescere della foresta

## Boosting e AdaBoost (slide 65-67)
- **Analogia**: consultare più medici e combinare le diagnosi **pesate** in base all'**accuratezza delle diagnosi precedenti**
- Procedura:
  1. si assegna un **peso a ogni tupla** di training
  2. si addestrano in serie $k$ classificatori: dopo $M_i$ i pesi vengono aggiornati perché $M_{i+1}$ presti **più attenzione alle tuple sbagliate** da $M_i$
  3. il classificatore finale $M^*$ combina i voti, ciascuno con peso **proporzionale all'accuratezza** del classificatore
- **AdaBoost**: $D$ = $d$ tuple etichettate $(X_1, y_1), \dots, (X_d, y_d)$; pesi iniziali tutti **$1/d$**. Per ogni passo $i = 1 \dots k$:
  1. si campiona $D$ **con replacement** (con reinserimento) per formare $D_i$ della **stessa dimensione** di $D$
  2. la probabilità di estrarre una tupla è **proporzionale al suo peso**
  3. si addestra $M_i$ su $D_i$
  4. si calcola il tasso d'errore di $M_i$ usando $D_i$ come test set
  5. le tuple **sbagliate** aumentano di peso, quelle corrette diminuiscono
- $err(X_j) \in \{0, 1\}$ per i classificatori; errore di $M_i$:
$$error(M_i) = \sum_{j=1}^{d} w_j \times err(X_j)$$
- **Peso del voto** di $M_i$:
$$\log\frac{1 - error(M_i)}{error(M_i)}$$
  (osservazione aggiunta: è positivo solo se $error(M_i) < 0.5$, e cresce quando l'errore diminuisce)

## SVM: Support Vector Machines (slide 68-84)
- Teoria di **Vapnik** (statistical learning theory dal **1965**, perfezionata nel **1995** da Vapnik e altri); fra gli strumenti più usati per classificare pattern
- Invece di stimare le **densità di probabilità** delle classi (classificatore bayesiano), si risolve direttamente il problema, ritenuto più semplice: trovare le **superfici decisionali** (**classification boundaries**)
- Nasce **binario**, estendibile a più classi. Casi:
  - **SVM lineare** con pattern **linearmente separabili** (esiste per ipotesi un iperpiano che li separa)
  - **SVM lineare** con pattern **non linearmente separabili**: errori inevitabili sul training set
  - **SVM non lineare**: superficie complessa, senza ipotesi di separabilità
  - **estensione multiclasse**
- Fra tutti gli iperpiani separatori si sceglie quello con **margine massimo**; **margine** = distanza minima dei punti del training set dall'iperpiano (figura: *optimal hyperplane* fra regioni $\mathcal{R}_1$ e $\mathcal{R}_2$, con i punti più vicini sulle rette del margine)
- Massimizzare il margine è legato alla **generalizzazione**: con ampio margine anche i record di test vicini al confine verranno probabilmente gestiti bene
- È un problema di **ottimizzazione convessa**: **un solo minimo globale**, nessun rischio di minimi locali

### SVM lineari, caso separabile (slide 72-77)
- TS di $n$ campioni $(x_1, y_1), \dots, (x_n, y_n)$, $x_i \in \mathbb{R}^d$, $y_i \in \{+1, -1\}$; esistono più iperpiani separatori
- Iperpiano generico di parametri $(w, b)$ (trasposto omesso):
$$D(x) = w \cdot x + b$$
  - $w$ = vettore **normale** all'iperpiano; $b/\|w\|$ = distanza dall'origine; $D(x) = 0$ = punti sul piano
  - se $x = x_p + r\frac{w}{\|w\|}$ con $D(x_p) = 0$, allora $D(x) = r\|w\|$, quindi la **distanza** di $x$ dall'iperpiano è
$$r = \frac{D(x)}{\|w\|}$$
  - Figura: piano $g(x) = 0$ in 3D, punto $x$ e sua proiezione $x_p$ a distanza $r$, regioni $\mathcal{R}_1$, $\mathcal{R}_2$
- Iperpiani che separano il TS con distanza minima $1/\|w\|$ da ogni lato:
$$w \cdot x_i + b \ge +1 \text{ se } y_i = +1, \qquad w \cdot x_i + b \le -1 \text{ se } y_i = -1$$
  in forma compatta $y_i[w \cdot x_i + b] \ge 1$ per $i = 1, \dots, n$
- **Margine** $\tau$: distanza minima fra iperpiano e dati. I punti su $D(x) = +1$ e su $D(x) = -1$ distano $1/\|w\|$ da $D(x) = 0$, quindi
$$\tau = \frac{2}{\|w\|}$$
  (figura: rette $D(x) = +1$, $0$, $-1$; sopra $D(x) > +1$, sotto $D(x) < -1$; punti pieni sul margine)
- **Problema di ottimizzazione** (massimizzare $\tau$ = minimizzare il suo inverso):
$$\min \frac{\|w\|^2}{2} \quad \text{vincoli: } y_i[w \cdot x_i + b] - 1 \ge 0, \quad i = 1, \dots, n$$
- **Support vector**: i dati che giacciono **sul margine** (cerchi pieni). Sono i casi più difficili e **definiscono completamente la soluzione**, esprimibile solo in funzione di essi, **indipendentemente** da $d$ e da $n$
- Si risolve con la **formulazione lagrangiana** e poi quella **duale**
- **Vantaggi**:
  - soluzione definita da **pochi support vector**
  - il numero $n_{sv}$ indica la **complessità** del problema; si dimostra che l'**errore medio** (sui possibili training set) è limitato da $n_{sv}/n$
  - scala molto bene con la **dimensionalità** $d$ (grazie ai **prodotti scalari**); il training è **quadratico** nel numero $n$ di dati; in pratica risolvibile per $d = 10^7$ e $n$ fino a $10^4$

### SVM per dati non separabili (slide 78-80)
- Si **rilassano i vincoli** per permettere ad alcuni pattern (il minor numero possibile) di superare il confine
- Si introducono $n$ **variabili di slack** $\xi_i \ge 0$:
$$y_i[w \cdot x_i + b] \ge 1 - \xi_i, \quad i = 1, \dots, n$$
  $\xi_i$ codifica la **deviazione dal margine**; per i dati separabili $\xi_i = 0$ (figura: due pattern erroneamente classificati, con $\xi > 0$)
- Si massimizza il margine e insieme si minimizzano gli errori:
$$\min \frac{\|w\|^2}{2} + C\sum_{i=1}^{n}\xi_i \quad \text{vincoli: } y_i[w \cdot x_i + b] \ge 1 - \xi_i$$
- $C$ = **importanza relativa degli errori** rispetto all'ampiezza del margine. Figura: $C = 10$ → 2 errori, **margine maggiore**; $C = 200$ → 1 solo errore, **margine minore**

### SVM non lineari (slide 81-82)
- Mapping **non lineare** $\Phi$ verso uno spazio a **più alta dimensionalità** ($m > d$):
$$\Phi : \mathbb{R}^d \mapsto \mathbb{R}^m, \qquad \Phi(x) = [g_1(x), g_2(x), \dots, g_m(x)]$$
  (la slide scrive $\mathbb{R}^n \mapsto \mathbb{R}^m$; lo spazio di partenza è $\mathbb{R}^d$)
- In $\mathbb{R}^m$ ci sono **più gradi di libertà** e i $\Phi(x_i)$ si separano più facilmente con un iperpiano (teoria già vista); equivale a separare gli $x_i$ in $\mathbb{R}^d$ con **superfici arbitrariamente complesse**
- Figura (senza testo): frontiere ottenute con kernel **polinomiale** $q = 2$ e $q = 10$ e **RBF** $\sigma = 1$ e $\sigma = 0.2$; grado alto o $\sigma$ piccolo danno frontiere più frastagliate

### Estensione multiclasse (slide 83-84)
- Problema **ancora aperto**, soluzioni più usate:
  - **One-Against-One**: iperpiani di separazione **per ogni coppia** di classi, poi un metodo **ensemble**
  - **One-Against-All**: con $s$ classi $w_1, \dots, w_s$, per ogni classe $w_k$ si addestra una SVM fra $w_k$ (etichetta $+1$) e **tutte le altre** $w_{h \ne k}$ (etichetta $-1$), ottenendo $D_k(x)$, distanza di $x$ dalla superficie in direzione di $w_k$ (più è grande, più si è confidenti); si assegna $x$ alla classe $k^*$ con **$D_k(x)$ massima**
- (La slide chiude con "Nota bene: **non** è necessario eseguire $s$ training SVM diversi"; nel One-Against-All descritto sopra si addestrano invece **$s$ SVM**, una per classe, quindi la nota va letta come "**è** necessario".)

## Analisi discriminante (slide 85-105)
### Esempio Default (slide 85-86)
- Una società di credito vuole stimare la **probabilità di default** (incapacità di pagare) da caratteristiche del debitore:
  - $Y$ **default**: binaria (sì/no)
  - $X_1$ **student**: binaria
  - $X_2$ **balance**: debito medio residuo sulla carta dopo i versamenti mensili
  - $X_3$ **income**: reddito
- Figure: prime righe del dataset; scatter Income vs Balance (chi va in default, arancione, ha balance alto); boxplot di Balance per default (molto più alto per i Yes) e di Income per default (simile)
- Usando solo *student* per stimare $P(default = Yes | student = Yes)$, tabella incrociata:

| default \ student | No | Yes | Sum |
|---|---|---|---|
| No | 6850 | 2817 | 9667 |
| Yes | 206 | 127 | 333 |
| Sum | 7056 | 2944 | 10000 |

- Stima diretta: $\hat{P}(default = Yes | student = Yes) = \frac{127}{2944} = 0.043$
- In pratica, con predittori **qualitativi e quantitativi**, è più semplice passare dal **teorema di Bayes**

### Calcolo delle probabilità (slide 87-90)
- **Probabilità condizionata**: probabilità che A accada dato che B è già accaduto
$$P(A|B) = \frac{P(A \wedge B)}{P(B)}$$
- **Indipendenti**: $P(A|B) = P(A)$, notazione $A || B$. **Disgiunti**: $P(A \wedge B) = 0$
- **Negazione** come complemento: se $A = (X \in S)$ allora $\neg A = (X \in range(X) - S)$
- **Regole**:
  1. $P(A) \ge 0$
  2. $P(A \vee \neg A) = 1$
  3. $P(A \wedge \neg A) = 0$
  4. $P(\neg A) = 1 - P(A)$
  5. $P(A \vee B) = P(A) + P(B) - P(A \wedge B)$ (**inclusione-esclusione**)
  6. $P(A|B) = \frac{P(A \wedge B)}{P(B)}$
  7. $A || B \Leftrightarrow P(A \wedge B) = P(A) \cdot P(B)$
- **Esempio del pilota**: probabilità di morire in un volo $p = 2\%$; in 50 voli?
  - Sommare darebbe $2\% \times 50 = 100\%$: sbagliato, perché gli eventi **non sono disgiunti** (per morire al volo $k$ bisogna essere sopravvissuti ai precedenti)
  - $P(\text{morte}) = p + (1-p)p + (1-p)^2 p + \dots + (1-p)^{49}p = 1 - (1-p)^{50}$
  - Sopravvivenza dopo 2 voli: $1 - (p + (1-p)p) = 1 - 2p + p^2 = (1-p)^2$, e così via. (La slide scrive $(1 - ((1-p)p)) = 1 - (p - p^2) = a - p + p^2 = (1-p)^2$: manca il termine $p$ della morte al primo volo e "$a$" è un refuso per 1; così com'è scritta l'uguaglianza è falsa.)
  - Sopravvivenza $0.98^{50} \approx 0.36$, morte $\approx 0.64$
- **Teorema di Bayes**:
$$P(A|B) = \frac{P(A)P(B|A)}{P(B)}$$
  Dim.: $P(A \wedge B) = P(A|B)P(B)$ e $P(A \wedge B) = P(B \wedge A) = P(B|A)P(A)$, quindi $P(A|B)P(B) = P(B|A)P(A)$ $\square$

### Approccio bayesiano (slide 91-95)
- $\pi = P(default = Yes)$, $1 - \pi = P(default = No)$, $P(S|D) = P(student = Yes | default = Yes)$, $P(S|\bar{D}) = P(student = Yes | default = No)$
$$P(default = Yes | student = Yes) = \frac{\pi \cdot P(S|D)}{\pi \cdot P(S|D) + (1-\pi) \cdot P(S|\bar{D})}$$
- Stime dalla tabella:
  - $\hat{\pi} = \frac{333}{10000} = 0.0333$ (la slide scrive $\frac{333}{1000} = 0.333$; i record sono 10000 e nella formula sotto la slide usa infatti 0.0333)
  - $\hat{P}(S|D) = \frac{127}{333} = 0.38$, $\hat{P}(S|\bar{D}) = \frac{2817}{9667} = 0.29$
$$\hat{P}(default = Yes | student = Yes) = \frac{0.0333 \cdot 0.38}{0.0333 \cdot 0.38 + 0.9667 \cdot 0.29} = 0.043$$
  stesso risultato della stima diretta
- L'**analisi discriminante** usa Bayes per stimare la probabilità che una risposta qualitativa $Y$ cada nella categoria $k = 1, \dots, K$ dati predittori qualitativi e quantitativi
- **Perché un altro metodo?**
  - con classi **ben separate**, le stime della **regressione logistica** sono sorprendentemente **instabili**; la LDA no
  - con $n$ **piccolo** e $X$ circa **normale** in ogni classe, la LDA è più stabile della logistica
  - la LDA è più semplice con **più di due classi**
- Setting: $Y$ con $K \ge 2$ valori non ordinati; $\pi_k$ = probabilità **a priori** della classe $k$; $f_k(x) = Pr(X = x | Y = k)$ = **densità** di $X$ condizionata a $Y = k$ (servono le densità perché $X$ può essere continua)
$$P(Y = k | X = x) = \frac{\pi_k f_k(x)}{\sum_{j=1}^{K}\pi_j f_j(x)}$$
  (nella slide il denominatore è scritto $\sum_{j=1} K\pi_j f_j(x)$: la $K$ è l'estremo superiore della somma)
- $p_k(x) = P(Y = k | X = x)$ = probabilità **a posteriori**. I $\pi_k$ si stimano con le **frequenze relative** delle classi: il problema si riduce a **stimare bene $f_k(x)$**

### LDA con un predittore, p = 1 (slide 96-100)
- Figura: due classi proiettate su due direzioni diverse, con gli istogrammi delle proiezioni; a seconda della direzione le classi proiettate si sovrappongono di più o di meno
- Assunzione: $f_k$ **gaussiana**
$$f_k(x) = \frac{1}{\sigma_k\sqrt{2\pi}}\exp\left(-\frac{1}{2\sigma_k^2}(x - \mu_k)^2\right)$$
  con $\mu_k$, $\sigma_k^2$ media e varianza della classe $k$; nella LDA **varianza comune** $\sigma_1^2 = \dots = \sigma_K^2 = \sigma^2$
- Posteriori:
$$p_k(x) = \frac{\pi_k \frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{1}{2\sigma^2}(x - \mu_k)^2\right)}{\sum_{j=1}^{K}\pi_j \frac{1}{\sigma\sqrt{2\pi}}\exp\left(-\frac{1}{2\sigma^2}(x - \mu_j)^2\right)}$$
  (Nella slide il denominatore usa $\sigma_k$ e $\mu_k$ dentro la somma su $j$; vanno $\mu_j$, e con varianza comune $\sigma$.)
- Il **classificatore di Bayes** assegna alla classe con $p_k(x)$ **massima**, cioè con massima **funzione discriminante**
$$\delta_k(x) = x\frac{\mu_k}{\sigma^2} - \frac{\mu_k^2}{2\sigma^2} + \log(\pi_k)$$
  (La slide scrive $\log(\mu_k)$; il termine corretto è il logaritmo della probabilità a priori, $\log(\pi_k)$.) $\delta_k$ è **lineare in $x$**, da cui il nome LDA
- **Esempio**: $K = 2$, $\pi_1 = \pi_2 = 0.5$ → classe 1 se
$$2x(\mu_1 - \mu_2) > \mu_1^2 - \mu_2^2$$
  altrimenti classe 2; **frontiera di decisione**:
$$x = \frac{\mu_1^2 - \mu_2^2}{2(\mu_1 - \mu_2)} = \frac{\mu_1 + \mu_2}{2}$$
- **Stima dei parametri** ($n_k$ = osservazioni di training nella classe $k$):
$$\hat{\mu}_k = \frac{1}{n_k}\sum_{i: y_i = k} x_i \qquad \hat{\sigma}^2 = \frac{1}{n - K}\sum_{k=1}^{K}\sum_{i: y_i = k}(x_i - \hat{\mu}_k)^2 \qquad \hat{\pi}_k = \frac{n_k}{n}$$
  (nella slide la varianza usa $\mu_k$ invece della stima $\hat{\mu}_k$) e si sostituiscono nelle formule per classificare
- **Esempio grafico**: a sinistra la popolazione (due gaussiane, verde e rosa, simmetriche intorno a 0), a destra un campione (istogrammi); **tratteggiato** = frontiera di Bayes (in 0), **continuo** = frontiera LDA stimata dal campione (poco spostata)

### LDA con più predittori, p > 1 (slide 101-102)
- $X = (X_1, \dots, X_p)$; le osservazioni della classe $k$ seguono una **normale multivariata** $X \sim N(\mu_k, \Sigma)$
- **Nota**: $\mu_k$ è **specifico per classe**, $\Sigma$ è **comune** a tutte le $K$ classi
- Stimati $(\mu_k, \Sigma)$, le $P(Y = k | X = x)$ si ottengono con Bayes e si classifica
- Esempio con $K = 3$ classi e tre frontiere: il classificatore di Bayes assegna in base alla **regione**. Sinistra: popolazione (ellissi delle tre gaussiane); destra: campione; **tratteggiato** = frontiere di Bayes, **continuo** = frontiere LDA

### QDA e confronto con LDA (slide 103-104)
- **LDA**: per ogni classe $X \sim N(\mu_k, \Sigma)$ (covarianza **comune**) → frontiere **lineari**. (La slide 103 scrive per la LDA $N(\mu_k, \Sigma_k)$, identica alla QDA; per la LDA la covarianza è $\Sigma$ senza indice, come nella slide 101.)
- **QDA** (analisi discriminante quadratica): $X \sim N(\mu_k, \Sigma_k)$, ogni gruppo ha **variabilità diversa** → frontiere **non lineari** (quadratiche)
- Figura: viola tratteggiato = Bayes, nero punteggiato = LDA, verde continuo = QDA; a sinistra Bayes e LDA sono rette quasi coincidenti, a destra la frontiera di Bayes è curva e la QDA la segue meglio
- **Confronto**:
  - LDA è **meno flessibile** → **minore varianza**
  - tradeoff: se l'assunto di **covarianza comune** è molto sbagliato, LDA può avere **bias elevato**
  - LDA è preferibile con **poche osservazioni** di training, quando ridurre la variabilità è cruciale
  - QDA è consigliata con training set **molto grande** o quando la covarianza comune è **chiaramente insostenibile**

### Mixture discriminant analysis, MDA (slide 105)
- Ogni classe è una **miscela gaussiana di sottoclassi**, e ogni punto ha una probabilità di appartenere a ciascuna **sottoclasse** (la slide dice "a ciascuna classe"; nella MDA la probabilità è sulle sottoclassi della miscela)
- Si assume ancora **covarianza uguale** fra le classi
- Figura: dati a griglia 3×3 di cluster di tre classi alternate; la LDA (rette) e la QDA (curve quasi piatte) falliscono, la **MDA** traccia frontiere a griglia che separano bene i cluster

## Da ricordare per lo scritto
- **Eager** vs **lazy**: lazy = training veloce, classificazione lenta, ipotesi locali più ricche; kNN è lazy e **non parametrico**
- kNN: classe di maggioranza fra i $k$ vicini; $k$ piccolo = sensibile al rumore, $k$ grande = perde i dettagli; $k = \sqrt{n}$ o cross-validazione; metriche per feature categoriali (Jaccard, Tanimoto, Dice, Hamming, coseno); weighted kNN con $1/d$ e, per classi sbilanciate, con $1/|\text{classe}|$
- Alberi: costruzione greedy divide-et-impera (albero minimo consistente NP-hard); goodness = **information gain** (ID3, C4.5, si massimizza) o **Gini** (CART, $gini_{split}$ si minimizza)
- $Info(S) = -\sum \frac{freq}{|S|}\log_2\frac{freq}{|S|}$, $Info_A(S) = \sum\frac{|S_i|}{|S|}Info(S_i)$, $Gain = Info(S) - Info_A(S)$; meteo: outlook 0.246 > humidity 0.151 > windy 0.048 > temperature 0.029
- Gain favorisce attributi con molti valori → $GainRatio = Gain/SplitInfo$; strategia: solo attributi con gain sopra la media, poi GainRatio massimo
- Continui: soglia scelta fra i valori ordinati; mancanti: $Gain = F \cdot (Info(S) - Info_A(S))$ o pesi frazionari
- Gini: $1 - \sum p_j^2$; esempio Age: minimo per $Age \le 23$ con $2/9$
- Pruning: pre (soglia sul gain) vs post (C4.5, pessimistico, sostituisce sottoalberi con foglie o rami); cost-complexity $R_\alpha(T) = R(T) + \alpha|\widetilde{T}|$, si pota il nodo con $\alpha_{eff}$ minimo; $\alpha = 0$ → overfitting (train 100%, test 88%)
- Consenso: bagging (media su campioni bootstrap, riduce la varianza), boosting (pesi sulle tuple e voto pesato $\log\frac{1-err}{err}$), ensemble (classificatori eterogenei)
- Random forest: bagging di alberi non potati + $m_{try}$ feature casuali a ogni split ($\sqrt{m}$ classificazione, $m/3$ regressione); varianza della media $\rho\sigma^2 + \frac{1-\rho}{B}\sigma^2$, ridurre $m$ riduce $\rho$; niente overfitting all'aumentare degli alberi; OOB error; importanza con mean decrease in accuracy / Gini
- SVM: margine massimo $\tau = 2/\|w\|$, $\min\frac{\|w\|^2}{2}$ con $y_i[w \cdot x_i + b] \ge 1$; problema convesso; support vector; soft margin con $\xi_i$ e $C$ (C grande = meno errori, margine minore); kernel per il non lineare; multiclasse One-Against-One e One-Against-All
- Bayes: $P(A|B) = \frac{P(A)P(B|A)}{P(B)}$; esempio pilota $1 - 0.98^{50} \approx 0.64$; esempio Default 0.043 in due modi
- LDA: gaussiane con covarianza comune, $\delta_k(x) = x\frac{\mu_k}{\sigma^2} - \frac{\mu_k^2}{2\sigma^2} + \log\pi_k$, con $K = 2$ e priori uguali frontiera $\frac{\mu_1 + \mu_2}{2}$; QDA con $\Sigma_k$ diverse (frontiere quadratiche, più flessibile, più varianza); MDA con miscele di sottoclassi
