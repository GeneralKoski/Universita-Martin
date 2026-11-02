# Algoritmi di clustering

Fonte: `Algoritmi di clustering.pdf`

Il pacco è di 131 pagine (il piè di pagina dice "x / 131": i numeri di slide qui sotto sono quelli di pagina). Blocchi: definizione, requisiti e criteri (slide 2-14), metodi a partizionamento: K-means, K-medoids, BFR, fuzzy K-means, Gaussian mixture con EM (slide 15-54), clustering gerarchico, BIRCH, BIRCH*, dynamic tree cut, ROCK, CURE, Chameleon (slide 55-109), algoritmi randomizzati, antipole clustering e range search (slide 110-121), clustering basato sulla densità con DBSCAN (slide 122-128), constraint-based clustering (slide 129-131).

## Definizione (slide 2-4)
- **Clustering** (raggruppamento): famiglia di metodi **non supervisionati** che individuano **raggruppamenti intrinseci** (cluster) di punti nello spazio multidimensionale e definiscono in corrispondenza di essi le classi (**incognite**)
- Figura (slide 2): nuvola di punti blu con tre gruppi cerchiati da ellissi tratteggiate (verde, blu, rossa) e alcuni punti isolati fuori da tutti i gruppi
- Un **cluster** è una raccolta di oggetti:
  - **simili** fra loro all'interno dello stesso cluster
  - **dissimili** dagli oggetti degli altri cluster
- Si chiama apprendimento **non supervisionato** perché non ci sono **classi predefinite**
- **Applicazioni** tipiche:
  - strumento **autonomo** per capire la **distribuzione** dei dati
  - fase di **pre-elaborazione** per altri algoritmi
- **Bontà**: un buon metodo produce cluster con **alta somiglianza intra-classe** e **bassa somiglianza inter-classe**
- La qualità del risultato dipende sia dalla **misura di similarità** sia dalla sua **attuazione** (l'algoritmo); la qualità del metodo si misura anche dalla capacità di **scoprire schemi nascosti** (pattern, regolarità)

## Requisiti (slide 5)
- **Scalabilità**
- gestire **diversi tipi di attributi**
- gestire **dati dinamici**
- scoprire cluster di **forma arbitraria** (con la misura euclidea si trovano cluster **sferici**)
- **requisiti minimi** di conoscenza del dominio per fissare i parametri di input
- gestire **rumore e valori anomali** (dati mancanti, sconosciuti, errati)
- **insensibilità all'ordine** dei record di input
- **alta dimensionalità** (l'occhio umano giudica bene un raggruppamento fino a tre dimensioni; in alta dimensione i dati sono **sparsi**)
- incorporare **vincoli** specificati dall'utente
- **interpretabilità** e **usabilità**

## Complessità (slide 6)
- Il problema è **NP-hard**: la ricerca esaustiva dell'ottimo è possibile solo con **pochi dati**
- Con $n$ oggetti e $s$ classi **note**, il numero di soluzioni distinte è il **numero di Stirling di seconda specie** $S(n, s)$, dell'ordine di
$$\frac{s^n}{s!}$$
  - esempio $n = 100$, $s = 5$: circa $10^{67}$. (Ricalcolato: $5^{100}/5! = 6.57 \cdot 10^{67}$, e anche il valore esatto $S(100, 5)$ è $6.57 \cdot 10^{67}$; l'ordine di grandezza è giusto.)
- Con $s$ **non noto** il numero di soluzioni è il **numero di Bell**:
$$B_0 = 1, \qquad B_{n+1} = \sum_{s=0}^{n}\binom{n}{s}B_s$$
- **Formula di Dobinski**: $B_n = \frac{1}{e}\sum_{k=0}^{\infty}\frac{k^n}{k!}$. (La slide la chiama "approssimazione", ma è una formula **esatta** sotto forma di serie; inoltre scrive l'indice della somma come $s$ e il termine con $k$: l'indice è $k$.)
- Esempio $\{A, B, C\}$, $n = 3$, $s = 2$: $(A)(B, C)$; $(A, B)(C)$; $(B)(A, C)$, cioè $S(3, 2) = 3$ (corretto). (Aggiunta, non nelle slide: contando anche la partizione in un solo cluster e quella in tre singoletti si ha $B_3 = 1 + 3 + 1 = 5$; la successione di Bell è 1, 1, 2, 5, 15, 52, 203, ...)

## Famiglie di algoritmi (slide 7-8)
- **Partizionamento**: metodi euristici iterativi che minimizzano la distanza dei punti dai **centroidi** del proprio cluster: **K-means**, **Fuzzy K-means**, **Expectation-Maximization** (Gaussian Mixture)
- **Gerarchico**: operazioni tipicamente **bottom-up** che aggregano punti in base a una distanza, organizzando i dati in una **struttura ad albero** (**dendrogramma**)
- **Basato sulla densità**: i cluster sono **regioni connesse ad alta densità**; il più noto è **DBSCAN**
- **Hard** vs **soft**:
  - **hard**: ogni punto è assegnato in modo **esclusivo** a un solo cluster
  - **soft** (fuzzy, "sfocato"): ogni punto ha un **grado di appartenenza** (es. fra 0 e 1) a ciascun cluster; gestisce meglio i pattern **vicini al bordo** fra cluster e gli **outlier**; si torna all'hard assegnando ogni punto al cluster con grado **massimo**

## Criteri e algoritmi (slide 9-10)
- **Criterio**: descrive **cosa** si vuole ottenere, cioè il grado di ottimalità di ogni soluzione ammissibile
- **Algoritmo**: dato un criterio, una **procedura** per trovare soluzioni che lo ottimizzano
- I criteri si basano di solito su due osservazioni:
  - i punti dello stesso cluster (**intra**) sono più simili fra loro che a punti di cluster diversi (**inter**)
  - i cluster sono **nuvole ad alta densità** separate da zone a **densità più bassa**
- **Partizionamento**: dato $k$, trovare la partizione del data set $D$ di $n$ oggetti in $k$ cluster che ottimizza il criterio
  - metodi **ottimali**: enumerano tutte le partizioni
  - metodi **euristici**: **k-means** (cluster rappresentato dal **baricentro**) e **k-medoids** (cluster rappresentato dall'oggetto **più centrale** del cluster)

### Minimizzazione delle distanze dai centroidi (slide 11-12)
$$J_e = \sum_{i=1}^{k}\sum_{x \in C_i}\|x - \hat{x}_i\|^2, \qquad \hat{x}_i = \frac{1}{n_i}\sum_{x \in C_i}x$$
- $C_i$ = $i$-esimo cluster, $n_i$ = numero dei suoi punti, $\hat{x}_i$ = **centroide** (baricentro). (Errore nella slide 11: il centroide è scritto con $\frac{1}{n}$; va diviso per $n_i$, la cardinalità del cluster, come dice il testo sotto la formula.)
- (Precisazione: il titolo delle slide 11-12 dice "distanze tra centroidi (inter-classe)", ma $J_e$ è la somma dei quadrati delle distanze di ogni punto **dal centroide del proprio cluster**, cioè una misura di **compattezza intra-cluster**, la SSE; non misura distanze fra centroidi.)
- Figura (slide 11): quattro gruppi colorati nel piano feature 1 / feature 2, ognuno con il centroide nero
- Buon criterio per cluster a **simmetria radiale** (circolari); **penalizza** forme **allungate** o cluster **innestati** (es. un anello con dentro un altro cluster)
- Figura (slide 12): sei dataset con l'algoritmo che li risolve e l'**ARI** (adjusted Rand index, accordo con le classi vere): PAM, $K = 3$, ARI 0.990 su gruppi compatti; mclust, $K = 4$, ARI 0.955 e 0.834 su gruppi ellittici (il secondo con molta sovrapposizione); complete linkage su due gruppi allungati, single linkage su due anelli concentrici, spectral clustering su due mezze lune, tutti con $K = 2$ e ARI 1.000. Le forme dell'ultima riga sono quelle che il criterio dei centroidi non riesce a separare

### Minimizzazione delle distanze intra-classe (slide 13-14)
$$J_e = \sum_{i=1}^{k}n_i \cdot \hat{s}_i, \qquad \hat{s}_i = \frac{1}{n_i}\sum_{x \in C_i}f_s(x, C_i)$$
con $f_s(x, C_i)$ distanza fra $x$ e il suo cluster. Due scelte:
1. $f_s(x, C_i) = \frac{1}{n_i}\sum_{x' \in C_i}\|x - x'\|^2$: criterio **simile** alla minimizzazione delle distanze dal centroide. (Aggiunta, non nelle slide: è esattamente il doppio, perché $\sum_{x, x' \in C_i}\|x - x'\|^2 = 2n_i\sum_{x \in C_i}\|x - \hat{x}_i\|^2$; verificato numericamente.)
2. $f_s(x, C_i) = \min_{x' \in C_i, x' \ne x}\|x - x'\|^2$: **non penalizza** i cluster **allungati**, perché per avere $f_s$ piccolo basta **un vicino**, non serve che tutto il cluster sia vicino a $x$
- Figura (slide 14), $k = 2$: due strisce orizzontali di punti, rossi sopra e blu sotto. Il criterio dei centroidi preferisce i due **cerchi tratteggiati** (metà sinistra e metà destra, ognuna con rossi e blu), il criterio 2 separa le due strisce **per colore**

## K-means (slide 15-20)
- K-means (o **C-means**): **computazionalmente semplice** e facile da implementare, spesso la **prima scelta**
- Minimizza **implicitamente** $J_e$ (distanze dai centroidi)
- Richiede in input il **numero di cluster $k$** e una **soluzione iniziale**; dà buoni risultati se entrambi sono ragionevoli
- Ottimizzazione **iterativa e locale**: può convergere a ottimi **locali**; di solito converge in **pochi passi** ($\le 10$). (La slide 15 dice "massimi locali"; poiché $J_e$ si minimizza sono **minimi** locali, come dice la slide 21.)
- Con distanza **euclidea** trova cluster **iper-sferici**, con la distanza di **Mahalanobis** cluster **iper-ellissoidali**:
$$d(\vec{x}, \vec{y}) = \sqrt{\sum_i\frac{(x_i - y_i)^2}{\sigma_{x_i}^2}}$$
  (Precisazione: questa è la Mahalanobis con covarianza **diagonale**, cioè la distanza euclidea standardizzata; la forma generale è $\sqrt{(\vec{x} - \vec{y})^T\Sigma^{-1}(\vec{x} - \vec{y})}$, che dà anche ellissoidi ruotati.)

### Algoritmo (slide 16)
```
1: inizializza n, k
2: scegli casualmente k punti come centroidi iniziali
3: do
     a. assegna ogni punto al cluster con centroide più vicino
     b. ricalcola ogni centroide come media dei punti del cluster
   while (i cluster sono cambiati AND iteration < max)
```
- Termina quando i centroidi sono **stabili** e le partizioni non cambiano
- (Aggiunta, non nelle slide: la convergenza è garantita perché entrambi i passi non aumentano $J_e$ e le partizioni possibili sono finite; si arriva però a un minimo **locale**)
- Figura (slide 17): sei pannelli (a)-(f): dati in tre gruppi, tre centroidi iniziali (cerchi vuoti), assegnamento con le frontiere tratteggiate (regioni di Voronoi), spostamento dei centroidi (frecce) e nuove frontiere, fino alla configurazione finale con i tre gruppi corretti

**Esempio** (aggiunta, non nelle slide; ricalcolato a mano e verificato con codice): punti 1D $\{2, 3, 4, 10, 11, 12, 20, 25, 30\}$, $k = 2$, centroidi iniziali $m_1 = 2$, $m_2 = 12$

| iter. | $m_1$ | $m_2$ | $C_1$ | $C_2$ |
|---|---|---|---|---|
| 1 | 2 | 12 | {2, 3, 4} | {10, 11, 12, 20, 25, 30} |
| 2 | 3 | 18 | {2, 3, 4, 10} | {11, 12, 20, 25, 30} |
| 3 | 4.75 | 19.6 | {2, 3, 4, 10, 11, 12} | {20, 25, 30} |
| 4 | 7 | 25 | {2, 3, 4, 10, 11, 12} | {20, 25, 30} |

- Alla quarta iterazione le partizioni non cambiano: stop. $J_e = 100 + 50 = 150$

### Limitazioni e pro/contro (slide 18-20)
- Figura (slide 18): **3 classi, 8 iterazioni**, dati a forma di croce/stella; K-means taglia i bracci in tre settori (rosso, blu, verde) invece di seguire le forme: **non** identifica cluster **non sferici**
- Figura (slide 19): **11 classi, 31 iterazioni** su un dataset di gruppi irregolari: alcuni cluster trovati spezzano o fondono i gruppi veri
- **Vantaggi**: relativamente efficiente, $O(t \cdot k \cdot n)$ con $t$ iterazioni, $k$ cluster, $n$ oggetti. (Aggiunta: con $d$ dimensioni il costo è $O(t \cdot k \cdot n \cdot d)$.)
- **Svantaggi**:
  - termina spesso in **ottimi locali** (dipende dalla soluzione iniziale)
  - serve **specificare $k$**
  - **poco robusto** a rumore e outlier
  - non trova cluster di forma **non convessa** (trova sfere o ellissi)
  - non applicabile direttamente a dati **categoriali**

### Soluzione iniziale (slide 21)
- Per ridurre il rischio di **minimi locali** si esegue **più volte** da soluzioni iniziali diverse: **random**, prodotte da **euristiche**, prodotte da un metodo **evoluzionistico** (algoritmo genetico)
- (Aggiunta, non nelle slide: l'euristica più usata è **k-means++**, che sceglie ogni nuovo centroide con probabilità proporzionale al quadrato della distanza dal centroide già scelto più vicino; è il default di scikit-learn)

### Quanti cluster? (slide 22-29)
- Le tecniche di **validazione** valutano a posteriori le soluzioni per diversi $k$ e scelgono con un criterio che tiene conto di **bontà** e **complessità**. (La slide 22 scrive "diversi valori di $s$": è il numero di cluster, qui chiamato $k$.)
- **Problema**: $J_e$ **cala sempre** al crescere di $k$; per $k = n$ (ogni cluster un solo punto) **$J_e = 0$** (risposta alla domanda della slide)
- **Possibile soluzione**: penalizzare i molti cluster, $J_e^* = J_e + penalty \cdot k$; ma il problema si sposta sulla scelta di $penalty$
- **Metodo del gomito** (discontinuità del grafico di $J_e$): si cerca il punto in cui il calo di $J_e$ **rallenta** bruscamente. Figura (slide 23): $J_e$ per $s = 2, \dots, 7$, il calo rallenta molto a $s = 4$, che è il **gomito** (elbow). (Precisazione: la slide lo chiama "punto di inflessione"; il gomito è il punto di **massima curvatura**, non un flesso in senso analitico.)

**Silhouette** (slide 24): si sceglie il $k$ che **massimizza** il silhouette score, media dei coefficienti dei singoli punti
$$s(x) = \frac{b - a}{\max(a, b)}$$
- $a$ = distanza **media** di $x$ dagli altri punti del suo cluster; $b$ = distanza **media** di $x$ dai punti del cluster **più vicino** (escluso il suo)
- (Errore nella slide 24: il numeratore è scritto $|b - a|$. Con il valore assoluto il coefficiente sarebbe sempre $\ge 0$ e un punto assegnato al cluster sbagliato ($a > b$) avrebbe lo stesso punteggio di uno ben assegnato; la formula corretta è $b - a$, con $s \in [-1, 1]$: vicino a 1 punto ben assegnato, vicino a 0 punto sul bordo, negativo punto probabilmente nel cluster sbagliato. La slide inoltre definisce $b$ come "la distanza fra il punto e i punti del cluster più vicino": è la distanza **media**.)
- Funziona per cluster sferici come quelli di K-means; **pesante** per grandi dataset ($O(n^2)$ distanze)
- (Aggiunta, non nelle slide: punti $(0,0), (0,1)$ nel cluster 1 e $(4,0), (4,1)$ nel cluster 2. Per $(0,0)$: $a = 1$, $b = (4 + \sqrt{17})/2 = 4.06$, $s = (4.06 - 1)/4.06 = 0.75$; per simmetria tutti e quattro valgono 0.75, verificato con scikit-learn)

**Figure (slide 25-29)**: esempio della documentazione di scikit-learn, 500 punti in 4 gruppi (uno isolato in alto a destra, tre vicini fra loro in basso a sinistra), K-means con $k = 2, \dots, 6$. A sinistra il silhouette plot (coefficienti dei punti per cluster, ordinati) con la linea rossa tratteggiata della media, a destra i cluster trovati. Medie lette dal grafico (approssimate):

| $k$ | silhouette medio (grafico) | ricalcolato | lettura |
|---|---|---|---|
| 2 | $\approx 0.70$ | 0.705 | il gruppo isolato contro gli altri tre fusi |
| 3 | $\approx 0.59$ | 0.588 | un cluster fonde due gruppi vicini |
| 4 | $\approx 0.65$ | 0.651 | i quattro gruppi veri, cluster di spessore simile |
| 5 | $\approx 0.56$ | 0.58 | un gruppo spezzato in due |
| 6 | $\approx 0.48$ | 0.50 | due gruppi spezzati |

- (Aggiunta, non nelle slide: valori ricalcolati con scikit-learn sullo stesso dataset; quelli per $k = 5, 6$ dipendono un po' dall'inizializzazione. Il massimo assoluto è a $k = 2$, non a $k = 4$: il silhouette premia la separazione netta del gruppo isolato. Per questo nell'esempio si guarda anche la **forma** dei profili: con $k = 4$ tutti i cluster superano la media e hanno spessore simile, con $k = 2$ il cluster grande ha molti punti sotto la media. Sullo stesso dataset $J_e$ vale circa 3735, 1904, 908, 819, 731 per $k = 2, \dots, 6$: il **gomito** è chiaramente a $k = 4$.)

## K-medoids (slide 30-34)

### PAM (slide 30-31)
- Affronta il problema degli **outlier** di K-means: un oggetto con valori molto più alti della media **distorce** la media del cluster
- **K-medoids**: invece del centroide si usa il **medoide**, l'oggetto **più centrale** del cluster (è sempre un punto dei dati)
- **PAM** (Partitioning Around Medoids, 1987): parte da un insieme di medoidi e **sostituisce** iterativamente un medoide con un non-medoide **se** migliora la distanza totale del clustering

```
1: scegli arbitrariamente k oggetti come medoidi iniziali
2: assegna ogni oggetto al medoide più vicino; calcola il costo totale
3: do
     scegli a caso un non-medoide O_random
     calcola il costo totale dello scambio fra un medoide O e O_random
     se la qualità migliora, effettua lo scambio
   until nessun cambiamento
```

- Figura (slide 31), $K = 2$: dieci punti su una griglia 10×10 (coordinate lette dalla figura, approssimate: (2,6), (3,8), (3,4), (4,7), (6,2), (6,4), (7,3), (7,4), (7,6), (8,5)); medoidi iniziali (3,8) e (6,4), costo totale **20**; si prova a scambiare (6,4) con $O_{random}$ = (6,2), costo totale **26**: peggiora, quindi lo scambio **non** si fa
- (Ricalcolo con distanza di Manhattan sulle coordinate lette: lo scambio con (6,2) dà davvero **26**. Il 20 invece torna solo assegnando (3,4) al medoide (3,8), come nel cerchio tratteggiato della figura; ma (3,4) dista 3 da (6,4) e 4 da (3,8), quindi con l'assegnamento al medoide più vicino il costo iniziale è **19**. La conclusione non cambia: 26 > 19, scambio rifiutato.)

### CLARA (slide 32-34)
- PAM è **più robusto** di k-means a rumore e outlier, perché un medoide è meno influenzato dai valori estremi di una media
- PAM funziona bene per **piccoli** dataset ma **non scala**: $O(k(n - k)^2)$ **per iterazione** (per ognuna delle $k(n - k)$ coppie medoide/non-medoide si ricalcola il costo su $n - k$ punti)
- **CLARA** (Clustering LARge Applications, Kaufman & Rousseeuw, 1990; la slide scrive "Kaufmann"): estrae **più campioni** del dataset, applica **PAM su ciascuno** e restituisce il **miglior** clustering
  - **vantaggio**: gestisce dataset più grandi di PAM
  - **svantaggi**: l'efficienza dipende dalla **dimensione del campione**; se il campione è **distorto**, un buon clustering del campione non è un buon clustering dell'intero dataset
- (Aggiunta, non nelle slide: nella proposta originale 5 campioni di $40 + 2k$ oggetti; il miglior clustering si sceglie valutando il costo dei medoidi trovati su **tutto** il dataset)
- Figura (slide 34): *Cluster plot* di 150 punti numerati (dati iris) proiettati sulle prime due componenti principali (Dim1 73%, Dim2 22.9%), 3 cluster con ellissi: il rosso (1) ben separato a sinistra, il verde (2) e il blu (3) parzialmente sovrapposti

## BFR (slide 35-42)
- **BFR** (Bradley-Fayyad-Reina): variante di k-means per renderlo **scalabile** a dati che non stanno in memoria
- Tre tipi di regioni:
  - **scartabili**: oggetti la cui appartenenza a un cluster è **certa**
  - **comprimibili**: non scartabili, ma appartengono a **sottocluster** stretti e densi
  - da tenere in **memoria principale**: non ancora associati a nessun cluster o sottocluster
- Funziona meglio se i punti sono distribuiti **normalmente** attorno a dei centri, anche con **deviazioni standard diverse** per dimensione. (Aggiunta, non nelle slide: BFR assume dimensioni **indipendenti**, quindi ellissi con assi **allineati** agli assi coordinati; un cluster obliquo non è rappresentabile.)
- Esempio (slide 36): $\sigma$ orizzontale doppia di quella verticale; figura con l'ellisse di "raggio" $\sigma$ e quella di $2\sigma$ attorno al centro. La slide dice che circa il 70% dei punti sta nell'ellisse di $\sigma$, il 95% in $2\sigma$, il 99.9% in $3\sigma$, il 99.9999% in $4\sigma$. (Errore nella slide 36: per una gaussiana **1D** le percentuali entro $\sigma, 2\sigma, 3\sigma, 4\sigma$ sono 68.3%, 95.4%, **99.7%**, **99.994%**; per un'ellisse in **2D** (raggio di Mahalanobis $r$, probabilità $1 - e^{-r^2/2}$) sono 39.3%, 86.5%, 98.9%, 99.97%. Il 99.9% e il 99.9999% non tornano in nessuno dei due casi; ricalcolati.)

### Rappresentazione di un cluster (slide 37-40)
Fayyad lavorò a **Skycat** e pensò i cluster come **galassie**:
- **Discard Set (DS)**: il **nucleo** di ogni cluster; i suoi punti sono **certi** di appartenere al cluster, che è rappresentato solo da statistiche (centroide e deviazione standard per componente)
- **Compression Set (CS)**: **sottocluster** di punti abbastanza vicini fra loro da essere riassunti con le statistiche come i DS, ma troppo lontani dai centroidi dei DS per sapere a quale associarli
- **Retained Set (RS)**: **singoli punti** né in DS né in CS, tenuti in memoria così come sono, insieme alle statistiche di DS e CS
- Figura (slide 38): un cluster DS a forma di fagiolo con il suo centroide (+), alcuni sottocluster CS (cerchi con +) e punti isolati RS (cerchietti)

**Statistiche** per ogni cluster DS e sottocluster CS, in $k$ dimensioni:
1. cardinalità $N$
2. vettore $SUM$: somma delle coordinate per dimensione, $SUM_i = \sum x_i$
3. vettore $SUMSQ$: somma dei quadrati delle coordinate per dimensione, $SUMSQ_i = \sum x_i^2$
- In tutto $2k + 1$ numeri, sufficienti per:
  - centroide: $\mu_i = SUM_i/N$
  - varianza: $\sigma_i^2 = \frac{SUMSQ_i}{N} - \left(\frac{SUM_i}{N}\right)^2$ (la slide scrive $SUMQ_i$: è $SUMSQ_i$), e la deviazione standard $\sigma_i$ come sua radice
- Le statistiche si **sommano** quando si fondono due insiemi: è ciò che permette di non tenere i punti

### Elaborazione di una RAM piena di punti (slide 41-42)
Con il **primo carico** di punti BFR sceglie i $k$ centroidi iniziali con un algoritmo in memoria (es. k-means esatto su un campione). Poi ogni carico (il primo e i successivi) è trattato così:
1. i punti **abbastanza vicini** a un centroide vanno nel **DS**, combinando le loro statistiche con quelle del cluster
2. si aggiornano $N$, $SUM$, $SUMSQ$ del cluster
3. il criterio di "abbastanza vicino" è il **raggio di Mahalanobis** sotto una soglia, es. **4 deviazioni standard**:
$$r_M(y) = \sqrt{\sum_{i=1}^{k}\left(\frac{y_i - \mu_i}{\sigma_i}\right)^2}$$
   cioè la distanza dal centroide **scalata** per $\sigma_i$ in ogni dimensione. (Precisazione: i passi 1 e 3 della slide descrivono la stessa decisione; il 3 dice con quale criterio si prende.)
4. i punti rimasti (più quelli di RS dei round precedenti) si clusterizzano in memoria; i gruppi con **varianza sotto soglia** vanno nel **CS** (sostituiti dalle statistiche), il resto in RS
5. si **fondono** sottocluster CS nuovi e vecchi se la varianza del risultato (calcolabile dalle sole statistiche) resta sotto soglia
6. all'**ultimo round** CS e RS si assegnano al cluster DS **più vicino**, anche se lontano

## Fuzzy K-means (slide 43-46)
- Figura (slide 43): *Hard Clustering* (ogni punto o esagono blu o cerchio verde) contro *Soft Clustering*, dove ogni punto ha una coppia di gradi di appartenenza, es. (0.97, 0.03), (0.03, 0.97) e, per un punto a metà, (0.47, 0.53); ogni coppia somma a 1
- Un pattern appartiene con un certo **grado** (la slide dice "probabilità") a più classi. Criterio:
$$J_{fuz} = \sum_{i=1}^{s}\sum_{j=1}^{n}\left[P(C_i \mid x_j, \Theta)\right]^m\|x_j - \theta_i\|^2$$
  con $\Theta = \{\theta_1, \dots, \theta_s\}$ centroidi della soluzione corrente. (Refusi nella slide 44: $\Theta = \{\theta_1, \dots, \theta_2\}$ va letto $\theta_s$ e nel testo $P(C_j \mid x_j, \Theta)$ va letto $P(C_i \mid x_j, \Theta)$.)
- **Centroidi** come media **pesata** dalle appartenenze:
$$\theta_i = \frac{\sum_{j=1}^{n}P(C_i \mid x_j, \Theta)^m \cdot x_j}{\sum_{j=1}^{n}P(C_i \mid x_j, \Theta)^m}$$
  (Errore nella slide 45: i pesi sono scritti senza l'esponente $m$. Minimizzando $J_{fuz}$, che contiene $P^m$, rispetto a $\theta_i$ i pesi risultano $P^m$; con $m = 2$ sono i quadrati delle appartenenze.)
- **Gradi di appartenenza**:
$$P(C_i \mid x_j, \Theta) = \frac{1}{\sum_{k=1}^{s}\left(\frac{\|x_j - \theta_i\|}{\|x_j - \theta_k\|}\right)^{\frac{2}{m-1}}}$$
- $m > 1$ regola quanto l'appartenenza è **sfumata**; valore tipico **$m = 2$**. (Aggiunta: per $m \to 1$ si torna all'hard k-means, per $m \to \infty$ tutte le appartenenze tendono a $1/s$.)
- (Aggiunta, non nelle slide: con $m = 2$ e un punto a distanza 1 da $\theta_1$ e 2 da $\theta_2$: $P(C_1) = 1/(1 + (1/2)^2) = 0.8$, $P(C_2) = 1/((2/1)^2 + 1) = 0.2$; verificato)

```
1: inizializza n, s
2: inizializza casualmente P(C_i | x_j, Θ), i = 1..s, j = 1..n
3: do
     a. calcola i centroidi Θ = {θ_1, ..., θ_s}
     b. calcola i gradi di appartenenza P(C_i | x_j, Θ)
   while (riduzione di J_fuz significativa AND iteration < max)
```
(Nella slide 46 gli indici sono scritti $i = 1, \dots, x$: è $i = 1, \dots, s$.)
- **Pro**: a volte **convergenza più robusta** del K-means
- **Contro**: l'appartenenza di un punto **dipende implicitamente dal numero di cluster** (le appartenenze sommano a 1), quindi con $s$ sbagliato si ottengono cattive soluzioni

## Gaussian Mixture ed EM (slide 47-54)
- Si ipotizza che i punti siano generati da un **mix di distribuzioni**: ogni classe genera dati secondo una sua distribuzione, ma alla fine i punti sembrano provenire da un'**unica distribuzione multimodale**
- Figura (slide 47): tre gaussiane 1D sovrapposte (cluster 1, 2, 3) e lo scatter *Clusters Determined by EM* su dati iris (Petal Width / Sepal Width) con tre ellissi, due delle quali sovrapposte
- **Obiettivo**: risalire ai **parametri** delle singole distribuzioni; si suppone nota la forma, tutte dello stesso tipo, di solito **gaussiane multivariate**: $s$ vettori medi, $s$ matrici di covarianza, $s$ coefficienti $\alpha$
$$p(x \mid \Theta) = \sum_{i=1}^{k}\alpha_i \cdot p_i(x \mid \theta_i), \qquad \Theta = \{\alpha_1, \dots, \alpha_k, \theta_1, \dots, \theta_k\}$$
  (Precisazioni: la slide 48 usa sia $s$ sia $k$ per il numero di componenti; scrive $\theta_i = \{\mu_i, \sigma_i\}$, ma per una multinormale il secondo parametro è la **matrice di covarianza** $\Sigma_i$, come dice il testo. Aggiunta: $\alpha_i \ge 0$ e $\sum_i\alpha_i = 1$.)
- Stima con **massima verosimiglianza**: $\mathcal{L}(\Theta \mid \mathcal{X}) = p(\mathcal{X} \mid \Theta)$; si massimizza il **logaritmo**; con punti indipendenti
$$\log p(\mathcal{X} \mid \Theta) = \sum_{j=1}^{n}\log\left(\sum_{i=1}^{k}\alpha_i \cdot p_i(x_j \mid \theta_i)\right)$$
  (Nella slide 49 l'indice della somma interna è scritto $j$: è $i$, l'indice delle componenti.)
- Massimizzarlo è difficile per la **somma dentro il logaritmo**: servirebbe sapere da quale componente è stato generato ogni $x_j$

### EM (slide 50-54)
- **EM** è un approccio **iterativo** per la massima verosimiglianza con dati **incompleti**: $\mathcal{X}$ noto, $\mathcal{Y} = \{y_1, \dots, y_n\}$ mancante, punto completo $z_j = [x_j, y_j]$
- Nella gaussian mixture i dati sono completi, ma si usano gli $y_j$ come **indicatori** (ignoti) della componente che ha generato $x_j$: così la massimizzazione diventa trattabile
- Si massimizza il **log-likelihood completo** $\log\mathcal{L}(\Theta \mid \mathcal{X}, \mathcal{Y}) = \log p(\mathcal{X}, \mathcal{Y} \mid \Theta)$. (Nella slide 51 a destra manca il $\log$: scrive $= p(\mathcal{X}, \mathcal{Y} \mid \Theta)$.)
- Figura (slide 52): diagramma di flusso START, initial values, **expectation step**, **maximization step**, "is converged?" (no: si torna all'E-step; sì: STOP)
- **Expectation**: valore atteso del log-likelihood completo, dati $\mathcal{X}$ e la stima corrente $\Theta^g$, rispetto a $\mathcal{Y}$ distribuita come $f(y \mid \mathcal{X}, \Theta^g)$:
$$Q(\Theta \mid \Theta^g) = E\left[\log p(\mathcal{X}, \mathcal{Y} \mid \Theta) \mid \mathcal{X}, \Theta^g\right] = \int_{y \in \Psi}\log p(\mathcal{X}, y \mid \Theta) \cdot f(y \mid \mathcal{X}, \Theta^g)\,dy$$
- **Maximization**: $\Theta^{g+1} = \arg\max_\Theta Q(\Theta \mid \Theta^g)$
- (Aggiunta, non nelle slide: per la gaussian mixture i due passi hanno forma chiusa. E-step, **responsabilità** $\gamma_{ij} = \frac{\alpha_i\,N(x_j \mid \mu_i, \Sigma_i)}{\sum_k\alpha_k\,N(x_j \mid \mu_k, \Sigma_k)}$; M-step, con $N_i = \sum_j\gamma_{ij}$: $\alpha_i = N_i/n$, $\mu_i = \frac{1}{N_i}\sum_j\gamma_{ij}x_j$, $\Sigma_i = \frac{1}{N_i}\sum_j\gamma_{ij}(x_j - \mu_i)(x_j - \mu_i)^T$. Il log-likelihood **non diminuisce mai** fra un'iterazione e l'altra, ma si arriva a un massimo **locale**.)
- Simile al **fuzzy K-means** ($\gamma_{ij}$ fa la parte delle appartenenze), ma con più gradi di libertà: i cluster possono essere **ellissoidali**
- Figura (slide 54): a sinistra gruppi allungati e obliqui con ellissi colorate; a destra *Original Data*, *k-Means Clustering*, *EM Clustering* su due gruppi piccoli e compatti in alto e uno grande e diffuso in basso: k-means attribuisce ai due gruppi piccoli la parte alta di quello grande (confini a metà strada fra i centroidi), EM recupera i gruppi originali
- **Attenzione**: le probabilità possono diventare **molto piccole** e dare problemi numerici; usare costanti moltiplicative e **normalizzare** alla fine. (Aggiunta: in pratica si lavora con i logaritmi e il trucco **log-sum-exp**.)

## Clustering gerarchico (slide 55-61)
- Come la **tassonomia biologica**: si specializza da famiglie ampie a famiglie ridotte. Figura (slide 55): albero dei vertebrati (squali, pesci, anfibi, primati, roditori, coccodrilli, dinosauri e uccelli) con i caratteri sui rami (vertebre, scheletro osseo, quattro arti, uovo amniotico, ...)
- Algoritmi di solito **bottom-up** (**agglomerativi**): si parte dai singoli elementi e a ogni livello si fondono (punto-punto, punto-cluster, cluster-cluster) gli elementi **meno distanti**, rispetto a una soglia che dipende dal livello. (Aggiunta: esistono anche i **divisivi** top-down, che partono da un unico cluster e lo spezzano; l'antipole clustering delle slide 114-117 è di questo tipo.)
- Figura (slide 56): dendrogramma di 8 punti $x_1, \dots, x_8$ con scala di **similarità** 0-100 e livelli $k = 1, \dots, 8$ (a $k = 1$ otto singoletti, a $k = 8$ un solo cluster). Valori letti dal grafico, approssimati: $\{x_6, x_7\}$ a circa 85, $\{x_2, x_3\}$ a circa 83, $\{x_4, x_5\}$ a circa 67, $\{x_4, \dots, x_7\}$ a circa 63, $\{x_1, x_2, x_3\}$ a circa 48, $\{x_4, \dots, x_8\}$ a circa 41, tutto a circa 33

### Distanze fra cluster (slide 57-59)
| Criterio | Distanza fra $C_i$ e $C_j$ |
|---|---|
| **single linkage** | distanza **minima** fra un punto di $C_i$ e uno di $C_j$ |
| **complete linkage** | distanza **massima** fra un punto di $C_i$ e uno di $C_j$ |
| **average linkage** | distanza **media** fra tutte le coppie di punti dei due cluster |
| **Ward** | si fonde la coppia che **minimizza** l'aumento della **varianza intra-cluster** |
| **centroidi** | distanza fra i **centroidi** (media, punto che può non stare nei dati) |
| **medoidi** | distanza fra i **medoidi** (punto centrale, obbligatoriamente fra i dati) |

- (Aggiunta, non nelle slide: l'aumento di SSE fondendo $C_i$ e $C_j$ nel metodo di Ward è $\frac{n_in_j}{n_i + n_j}\|\mu_i - \mu_j\|^2$)
- Figura (slide 57): due gruppi di punti con il segmento rosso che li collega: fra i due punti più vicini (*single-link*), fra i più lontani (*complete-link*), fra due punti centrali (*average-link*, a rappresentare la media)
- Figura (slide 58): confronto (scikit-learn) dei quattro linkage su anelli concentrici, mezze lune e tre gruppi gaussiani di dispersione diversa. Solo il **single linkage** separa anelli e lune (segue le catene di punti), ma sui gruppi gaussiani mette quasi tutto in un cluster (**effetto catena**); average e complete sbagliano anelli e lune; **Ward** separa correttamente i tre gruppi gaussiani. Tempi fra 0.02 e 0.06 s
- Figura (slide 59): punti con due cluster, il **centroide** (croce, non è un punto dei dati) e il **medoide** (punto cerchiato)

**Esempio** (aggiunta, non nelle slide; ricalcolato a mano e verificato con scipy): punti 1D $\{0, 4, 6, 14, 19\}$

| passo | single linkage | complete linkage |
|---|---|---|
| 1 | {4, 6} a distanza 2 | {4, 6} a distanza 2 |
| 2 | {0, 4, 6} a 4 (0-4) | {14, 19} a 5 (contro 6 = max(0-4, 0-6)) |
| 3 | {14, 19} a 5 | {0, 4, 6} a 6 |
| 4 | tutto a 8 (6-14) | tutto a 19 (0-19) |

- Stessi cluster, **altezze** e **ordine** delle fusioni diversi: il single linkage guarda la coppia più vicina, il complete la più lontana

### Arresto e taglio (slide 60-61)
- Ci si ferma quando restano **$k$ cluster**, oppure quando ogni possibile fusione violerebbe un **vincolo di compattezza** (es. distanza media dal centroide troppo alta)
- Il risultato è un **dendrogramma** (albero di partizioni a livelli); il clustering si ottiene **tagliando** il dendrogramma al livello desiderato (figura della slide 61: lo stesso dendrogramma della slide 56)

## BIRCH (slide 62-74)
**Problemi** del gerarchico classico (slide 62):
- **complessità** $O(n^2)$: ogni decisione di merge o split richiede di conoscere molti altri dati. (Precisazione: $O(n^2)$ è la **memoria** della matrice delle distanze e il tempo delle versioni migliori, es. SLINK per il single linkage; l'implementazione ingenua è $O(n^3)$, con una coda di priorità $O(n^2\log n)$.)
- una fusione **non si può disfare**

**Metodologie note**: **BIRCH** (migliora in modo incrementale i sottocluster), **BIRCH*** (estende BIRCH a dataset molto grandi), **ROCK** (dati categoriali), **CURE**, **Chameleon** (modellazione dinamica della similarità fra cluster). (Precisazione: la slide 62 riassume ROCK come "distanza minima tra cluster" e CURE come "minimizzare la distanza media dei punti dal proprio centroide"; nelle slide dedicate ROCK usa i **link** (vicini comuni, slide 91) e CURE nasce proprio per **evitare** il criterio della distanza media dal centroide (slide 95), usando più punti rappresentativi.)

**BIRCH**: Balanced Iterative Reducing and Clustering using Hierarchies (Zhang, Ramakrishnan & Livny, SIGMOD'96), basato su **Cluster Feature** (CF) e **CF-tree**

### Cluster feature (slide 64-66)
$$CF = (N, \vec{LS}, \vec{SS}), \qquad \vec{LS} = \sum_{i=1}^{N}\vec{X}_i, \qquad \vec{SS} = \sum_{i=1}^{N}\vec{X}_i^2$$
- $N$ = numero di punti; il CF riassume il cluster con statistiche e permette un immagazzinamento **efficiente** (è l'analogo di $N$, $SUM$, $SUMSQ$ di BFR)
- **Centroide**: $\vec{X}_0 = \vec{LS}/N$
- **Raggio** (distanza dei punti dal centroide):
$$R = \sqrt{\frac{\sum_{i=1}^{N}(\vec{X}_i - \vec{X}_0)^2}{N}} = \sqrt{\frac{SS}{N} - \left(\frac{LS}{N}\right)^2}$$
  (Errore nella slide 65: scrive $\sqrt{(\frac{SS}{N} - \frac{LS}{N})^2}$, con il quadrato su tutta la differenza; la forma giusta è quella della slide 64, con il quadrato solo su $LS/N$. Nell'esempio qui sotto la formula sbagliata darebbe un risultato privo di senso.)
- **Diametro** (distanza fra coppie di punti del cluster):
$$D = \sqrt{\frac{\sum_{i=1}^{N}\sum_{j \ne i}(\vec{X}_i - \vec{X}_j)^2}{N(N-1)}}$$
  (Precisazione: $R$ e $D$ sono medie **quadratiche**, non medie semplici delle distanze. Aggiunta: anche $D$ si calcola dal solo CF, $D^2 = \frac{2N \cdot SS - 2\|\vec{LS}\|^2}{N(N-1)}$ con $SS$ sommato sulle dimensioni.)
- **Esempio** (slide 64): punti (3,4), (2,6), (4,5), (4,7), (3,8), $CF = (5, (16, 30), (54, 190))$. Ricalcolato: $LS = (3+2+4+4+3,\ 4+6+5+7+8) = (16, 30)$, $SS = (9+4+16+16+9,\ 16+36+25+49+64) = (54, 190)$: **corretto**. (Aggiunta, non nelle slide: centroide $(3.2, 6)$, varianze per dimensione $54/5 - 3.2^2 = 0.56$ e $190/5 - 6^2 = 2$, quindi $R = \sqrt{2.56} = 1.6$; $D = \sqrt{(2 \cdot 5 \cdot 244 - 2 \cdot 1156)/20} = \sqrt{6.4} = 2.53$; verificati anche dai punti.)
- **Teorema di additività** (slide 66): fondendo $C_1$ e $C_2$
$$CF_{C_3} = \langle n_{C_1} + n_{C_2},\ LS_{C_1} + LS_{C_2},\ SS_{C_1} + SS_{C_2}\rangle$$
  quindi i CF si aggiornano **senza** rileggere i punti

### CF-tree (slide 63, 67-69)
- **Albero bilanciato** con due parametri:
  - **branching factor $B$**: numero massimo di elementi in un nodo **non foglia**
  - **threshold $T$**: **diametro massimo** dei sottocluster nelle **foglie**
- Nodo non foglia: elementi $[CF_i, child_i]$, con $child_i$ puntatore all'$i$-esimo figlio e $CF_i$ il CF del sottocluster di quel figlio (somma dei CF dei figli, per additività)
- Nodo foglia: $[CF_j, \dots, CF_{j+L}]$, più i puntatori **prev** e **next** alle foglie vicine (le foglie formano una lista)
- Figure (slide 63, 68, 69): radice con $CF_1, \dots, CF_6$ e puntatori ai figli ($B = 7$, $L = 6$ nella slide 63, $L = 5$ nella 68), es. $CF_1 = CF_7 + \dots + CF_{12}$ e $CF_7 = CF_{90} + \dots + CF_{94}$; foglie collegate da prev/next, e una foglia che punta a un piccolo gruppo di punti. ($L$ è il numero massimo di elementi di una foglia; la slide 67 non lo nomina.)

### Fasi (slide 70-72)
- Figura (slide 70), dal lavoro originale: **Phase 1** carica i dati costruendo un CF-tree; **Phase 2** (opzionale) lo **condensa** costruendo un CF-tree più piccolo; **Phase 3** **clustering globale** (good clusters); **Phase 4** (opzionale, off line) **raffinamento** (better clusters)
- La slide 71 le riassume in due:
  - **Fase 1**: scan del dataset per costruire un CF-tree **in memoria** (compressione a più livelli che conserva la struttura a cluster)
  - **Fase 2**: un algoritmo di clustering raggruppa le **foglie** del CF-tree
- Figura (slide 72), costruzione della fase 1: si inserisce nel CF-tree $t_1$ con soglia iniziale $T$; se la memoria finisce si **aumenta $T$**, si ricostruisce un albero $t_2$ più piccolo da $t_1$ (le foglie candidate outlier vanno su disco, se c'è spazio) e si continua; a fine scan (o con il disco pieno) si **riassorbono** gli outlier potenziali

### Inserimento e rifinitura (slide 73-74)
1. si scende dalla radice fino alla **foglia appropriata** con una misura di **vicinanza**
2. si modifica la foglia:
   - se $D < T$ la foglia **assorbe** il punto e si aggiornano i CF
   - altrimenti si crea una **nuova entry**; se la foglia è piena si fa lo **split**: si scelgono le due entry **più lontane** e le altre vanno con la più vicina delle due
3. si aggiornano i CF lungo il **cammino** fino alla radice, con possibili split dei nodi padre
- **Rifinitura**: le entry delle foglie con **pochi elementi** si possono considerare **outlier** ed eliminare; $T$ e $B$ possono **spezzare cluster reali**; in fase 2 un algoritmo **agglomerativo** tratta ogni sottocluster foglia come un **singolo punto** con il suo CF
- **Vantaggi**: **scala linearmente**, trova un buon clustering con **una sola lettura** dei dati e lo migliora con letture successive
- **Svantaggi**: solo dati **numerici**, **sensibile all'ordine** di lettura, trova **solo cluster sferici** (si basa sul raggio)

## BIRCH* / GRGPF (slide 75-84)
- **GRGPF** (Ganti, Ramakrishnan, Gehrke, Powell, French): metrica $D$ **non necessariamente euclidea**, dati che **non stanno in memoria**
- I cluster stanno in una struttura tipo **R-tree**, il **CF*-tree**: i nodi sono **blocchi del disco**, foglie e nodi interni contengono dati diversi. Figura (slide 75): regioni rettangolari annidate R1-R11 e l'albero corrispondente
- Senza coordinate non esiste il centroide: si usa il **clusteroide** $\hat{C}$, il punto del cluster che minimizza la **rowsum**
$$rowsum(\hat{C}) = \sum_{x \in C}D(\hat{C}, x)^2$$
  analoga di $SUMSQ$ di BFR; il raggio è $\sqrt{rowsum/N}$
- **Foglie**: per ogni cluster
  1. cardinalità $N$
  2. clusteroide $\hat{C}$ e la sua rowsum
  3. i $p$ punti **più vicini** a $\hat{C}$ con le loro rowsum
  4. i $p$ punti **più lontani** da $\hat{C}$ con le loro rowsum
- **Nodi interni**: i clusteroidi dei cluster discendenti, la loro rowsum e il numero di punti (per il raggio). Per inserire un punto si scende solo lungo i cammini con clusteroidi **ragionevolmente vicini**

### Mantenimento (slide 78-80)
- **Inizializzazione** su una memoria piena di dati: prima stima dei cluster, organizzati nel CF*-tree; poi si inseriscono i **punti rimanenti**; i cluster si riconsiderano se sono troppi per la RAM o se uno diventa troppo grosso (raggio troppo grande)
- Aggiungendo $X$ al cluster $C$ con $D(\hat{C}, X)$ minimo (trovato con i campioni di clusteroidi dei nodi interni):
  - a ciascuna delle $2p + 1$ rowsum memorizzate si aggiunge il **quadrato della distanza** da $X$
  - la rowsum di $X$ si **stima** come
$$rowsum(X) \approx N\left(r^2 + D(\hat{C}, X)^2\right)$$
    perché in **alta dimensionalità** i segmenti $X\hat{C}$ e $\hat{C}Y$ sono circa **perpendicolari** e per Pitagora $D(X, Y)^2 \approx D(X, \hat{C})^2 + D(\hat{C}, Y)^2$; sommando su tutti gli $Y$ del cluster si ottiene $N \cdot D(X, \hat{C})^2 + rowsum(\hat{C})$, e $rowsum(\hat{C}) = Nr^2$ (figura: cerchio con $X$, $Y$ e $\hat{C}$ al centro)
- Dopo l'aggiunta il clusteroide può cambiare: diventa $X$ o uno dei $p$ punti più vicini se ha rowsum **minore**. Alla lunga il clusteroide uscirebbe dai $p$ punti tenuti, quindi serve un **ricalcolo periodico** con I/O su disco

### Spezzare e fondere (slide 81-84)
- Se il **raggio** supera una soglia il cluster si **spezza** in due: si ricarica in memoria e si esegue un algoritmo di split; le foglie aumentano di uno e un blocco in **overflow** si spezza come in un **B-tree**, a cascata. Se l'albero non sta più in memoria si **aumenta la soglia** e si fondono cluster
- **Fusione** di $C_i$ e $C_j$ senza caricare tutto:
  1. si assume che il nuovo clusteroide sia uno dei punti **più lontani** da $\hat{C}_i$ o da $\hat{C}_j$
  2. per ogni candidato $X \in C_i$ si stima
$$rowsum(X) = rowsum_i(X) + N_j\left(D^2(X, \hat{C}_i) + D^2(\hat{C}_i, \hat{C}_j)\right) + rowsum_j(\hat{C}_j)$$
     il primo addendo conta le distanze da $X$ ai punti di $C_i$; per i punti $Y \in C_j$ si applica due volte Pitagora (triangoli $X\hat{C}_iY$ e $\hat{C}_i\hat{C}_jY$, rettangoli per l'alta dimensionalità), con i segmenti $\hat{C}_jY$ riassunti da $rowsum_j(\hat{C}_j)$ (figure delle slide 82-83 con i due triangoli)
  3. scelto il clusteroide, si ricalcolano con la stessa stima le rowsum di tutti i punti tenuti nelle caratteristiche del cluster
- (Verificato: sommando $D^2(X, Y) \approx D^2(X, \hat{C}_i) + D^2(\hat{C}_i, \hat{C}_j) + D^2(\hat{C}_j, Y)$ sugli $N_j$ punti $Y$ si ottiene esattamente il secondo e il terzo addendo.)

## Dynamic tree cut (slide 85-88)
- Il taglio ad **altezza costante** è poco flessibile e va male su dendrogrammi complicati
- **DynamicTreeCut** (DTC) taglia i rami in modo **dinamico** secondo la loro forma. Vantaggi:
  1. identifica cluster **annidati**
  2. **flessibile**: parametri di forma regolabili per l'applicazione
  3. adatto all'**automazione**
  4. può combinare gerarchico e **PAM** per un migliore rilevamento degli **outlier**
- Figura (slide 86): (A) average linkage su una rete proteina-proteina di Drosophila con la topological overlap matrix, moduli come barra di colori sotto il dendrogramma (grigio = proteine non assegnate), arricchiti in ontologie geniche note; un taglio fisso non troverebbe molti di questi cluster. (B) dati di espressione genica simulati: barre di colore per *Simulated*, *Dynamic hybrid*, *Dynamic tree*, taglio statico a 0.92 e 0.995, PAM con 11, 10 e 9 cluster
- **Algoritmo** (slide 87, con diagramma di flusso): parte da **pochi grandi cluster** dal taglio statico; analizza le **altezze di fusione** di ogni cluster (fluttuazioni delle altezze dei rami) per trovare sottostrutture; i cluster con questo andamento si **suddividono ricorsivamente**; i cluster **molto piccoli** si uniscono ai più vicini; si ferma quando il numero di cluster è **stabile**
- **Dynamic Hybrid** (slide 88), bottom-up, migliora l'assegnazione dei **membri periferici**:
  1. cluster preliminari = rami che contengono un **numero minimo** di oggetti, da cui si escludono gli oggetti **troppo lontani** anche se dello stesso ramo, **distinti** dall'intorno e con un **nucleo** (la punta del ramo) strettamente connesso
  2. gli oggetti non assegnati si assegnano al cluster preliminare più vicino **se abbastanza vicino**

## ROCK (slide 89-93)
- **ROCK**: RObust Clustering using linKs (Guha, Rastogi & Shim, ICDE'99), per dati **categoriali**, dove le misure tradizionali (es. coefficiente di **Jaccard** usato direttamente) possono funzionare male (figura: foto di "The Rock", gioco di parole)
- **Tre fasi**:
  1. **campione casuale**, per scalare a grandi dataset
  2. **clustering** agglomerativo gerarchico con la similarità basata sui **link**
  3. **etichettatura** dei dati su disco: da ogni cluster $C_i$ si estrae un campione $L_i$ e ogni punto va al cluster con cui ha il **link più forte** verso $L_i$
- **Vicini**: due punti con similarità (tipicamente Jaccard) **sopra una soglia $\theta$**. **Link** di una coppia = numero di **vicini comuni**: porta informazione **globale** sull'intorno; più link, più è probabile che i due punti stiano nello stesso cluster
- (Aggiunta, non nelle slide: le transazioni $\{1, 2, 3\}$ e $\{1, 2, 4\}$ hanno Jaccard $2/4 = 0.5$; con $\theta = 0.5$ sono vicine)
- **Criterio** da massimizzare:
$$E_l = \sum_{i=1}^{k}n_i \times \sum_{p_q, p_r \in C_i}\frac{link(p_q, p_r)}{n_i^{1 + 2f(\theta)}}, \qquad f(\theta) = \frac{1 - \theta}{1 + \theta}$$
  massimizza i link **dentro** i cluster e minimizza quelli **fra** cluster diversi. (Aggiunta: $n_i^{1 + 2f(\theta)}$ è il numero **atteso** di link in un cluster di $n_i$ punti; dividendo si evita che convenga mettere tutto in un unico cluster. Con $\theta = 0.5$, $f = 1/3$ e l'esponente è $5/3$.)
- **Goodness** per scegliere la coppia da fondere nella fase agglomerativa:
$$g(C_i, C_j) = \frac{link[C_i, C_j]}{(n_i + n_j)^{1 + 2f(\theta)} - n_i^{1 + 2f(\theta)} - n_j^{1 + 2f(\theta)}}$$
  cioè i link fra i due cluster divisi per quelli attesi

## CURE (slide 94-97)
- **CURE**: Clustering Using REpresentatives (Guha, Rastogi & Shim, '98; figura: foto della band The Cure). Per spazi **euclidei** con cluster **non gaussiani** attorno a un centroide (come assume BFR), dove k-means va male
- **Esempio 1** (slide 95): con la distanza fra centroidi i cluster veri sono 4 (linee continue), ma l'algoritmo trova i cerchi tratteggiati: un cluster grande viene spezzato e i pezzi assorbono cluster piccoli vicini
- **Esempio 2**: minimizzando la distanza media dal centroide, un cluster **allungato** viene spezzato in tanti cerchi; non succede con il **raggio di Mahalanobis** di BFR (lo vede come "circolare" nelle coordinate scalate). (Precisazione: vale per un'ellisse allineata agli assi, come in figura.)
- **Algoritmo**:
  1. si riempie la memoria con punti **casuali** e si clusterizzano con un approccio **gerarchico**
  2. per ogni cluster si scelgono **$c$ punti rappresentativi**, il più **lontani** possibile fra loro: il primo è il più lontano dal centroide, poi ripetutamente il punto che **massimizza la distanza minima** da quelli già scelti; infine si **spostano** tutti del **20%** verso il centroide (non saranno più punti dei dati, non è un problema)
  3. si **partiziona** l'insieme assegnando ogni punto al rappresentativo più vicino
- Figura (slide 97): (a) campione di dati, (b) tre cluster con i punti rappresentativi, (c) fusione dei cluster con i punti più vicini, (d) restringimento dei rappresentativi verso il centro

## Chameleon (slide 98-109)
- Gerarchico, con **modellazione dinamica** della similarità fra cluster; nasce per le debolezze di ROCK e CURE (figura: un camaleonte):
  - **ROCK** guarda l'**interconnettività** e ignora la **vicinanza**
  - **CURE** guarda la **vicinanza** e ignora l'**interconnettività**
- Due cluster si **fondono** se sono molto **interconnessi** e **vicini**; non dipende da un modello statico dato dall'utente, si **adatta** alle caratteristiche interne dei cluster; vale per **qualsiasi tipo di dato** con una funzione di somiglianza
- **kNN graph** (slide 100): vertici = oggetti, arco fra due vertici se uno è fra i $k$ più simili dell'altro, archi **pesati** con la somiglianza. Figura: Data set → sparse graph (kNN) → partizione del grafo → fusione delle partizioni → cluster finali
  1. un algoritmo di **partizionamento** divide il grafo in molti **piccoli sottogruppi**
  2. un **agglomerativo** li fonde ripetutamente in base a interconnettività e vicinanza
- Il grafo cattura il vicinato in modo **dinamico**: il raggio di vicinato dipende dalla **densità** della regione; cluster più naturali di DBSCAN, che usa un **vicinato globale**. La densità finisce nei **pesi** degli archi
- **Edge cut** $EC_{\{C_i, C_j\}}$: peso totale degli archi tagliati dividendo un cluster in $C_i$ e $C_j$ (scelto **minimo**) = **interconnettività assoluta**
- **Interconnettività relativa**:
$$RI(C_i, C_j) = \frac{|EC_{\{C_i, C_j\}}|}{\frac{1}{2}\left(|EC_{C_i}| + |EC_{C_j}|\right)}$$
  con $EC_{C_i}$ = somma minima degli archi tagliati bisezionando $C_i$ in due parti circa uguali (la slide 103 mette il valore assoluto sulla somma, $|EC_{C_i} + EC_{C_j}|$; è lo stesso, perché i pesi sono positivi)
- **Vicinanza relativa**:
$$RC(C_i, C_j) = \frac{\bar{S}_{EC_{\{C_i, C_j\}}}}{\frac{|C_i|}{|C_i| + |C_j|}\bar{S}_{EC_{C_i}} + \frac{|C_j|}{|C_i| + |C_j|}\bar{S}_{EC_{C_j}}}$$
  con $\bar{S}_{EC_{\{C_i, C_j\}}}$ peso **medio** degli archi fra $C_i$ e $C_j$ e $\bar{S}_{EC_{C_i}}$ peso medio degli archi della bisezione di taglio minimo di $C_i$
- (Aggiunta, non nelle slide: nel lavoro originale si fonde la coppia che massimizza $RI \cdot RC^\alpha$, con $\alpha$ scelto dall'utente per pesare la vicinanza)
- **Partizionamento iniziale** con **hMETIS** (slide 105-106). Figura: schema multilivello, (1) **coarsening** $G_0 \to G_1 \to G_2 \to G_3$, (2) partizione iniziale del grafo più piccolo, (3) **uncoarsening e refinement** riproiettando la partizione fino a $G_0$
  - si minimizza l'edge cut con sottocluster che contengono ciascuno **almeno** il 25% dei nodi del cluster di partenza (la slide dice "il 25%": è un vincolo di bilanciamento, non una quota esatta)
  - si biseziona ripetutamente il sottocluster **più grande**, finché il più grande ha meno nodi di una soglia (fra l'1% e il 5% dei nodi totali). (Precisazione: la slide dice "si inizia dai singoli punti", ma questa fase è top-down: parte dal grafo intero, i cui vertici sono i singoli punti, e lo biseziona; i singoli punti sono il punto di partenza solo nel senso che sono i vertici del grafo.)
- Trova cluster di **forma arbitraria** di alta qualità meglio di BIRCH e DBSCAN, ma in alta dimensionalità può costare **$O(n^2)$** nel caso peggiore
- Figure (slide 108-109): dataset sintetici DS1-DS5 (ellissi, rombi, lettere, anelli, forme irregolari con rumore) e i risultati di Chameleon su DS3 (17 e 11 cluster), DS4 (25 e 11), DS5 (25 e 8): con meno cluster le forme sono riconosciute intere

## Algoritmi randomizzati (slide 110-113)
**1-mediana** (slide 110-111): elemento $c \in S$ che minimizza $w(c) = \sum_{s \in S}d(s, c)$. (Precisazione: la slide la chiama "centroide", ma con $c \in S$ è un **medoide**; il centroide è la media e minimizza la somma dei **quadrati** delle distanze.) Approssimazione a **torneo**:
1. si divide $S$ in **triple** casuali
2. per ogni tripla si tiene la sua 1-mediana e si **scartano** gli altri due
3. si ripete ricorsivamente sulle 1-mediane
4. l'ultima 1-mediana è l'output
- Figura (slide 111): punti con le triple disegnate come triangoli e il vincitore di ciascuna evidenziato, round dopo round, fino al punto finale (rossi gli eliminati, verde il vincitore)

**Diametro** (slide 112): a ogni round gli elementi rimasti si partizionano a caso in sottoinsiemi, ognuno elabora localmente la 1-mediana, gli elementi promossi passano al round successivo; si termina quando restano **due** elementi, che approssimano il **diametro** di $S$. (Precisazione: così come è scritta, la procedura promuove le **1-mediane** e quindi converge verso il **centro**, non verso due punti lontani; per il diametro, come nella fase 1 dell'antipole della slide 115, la 1-mediana di ogni tripla va **scartata** e passano gli altri due.)

**Teorema** (slide 113): con $|S| = n = 3^r$ si eseguono esattamente $\frac{3}{2}(n - 1)$ distanze.
- Per induzione su $r$: per $r = 1$ una tripla costa 3 distanze, e $\frac{3}{2}(3 - 1) = 3$
- Passo: con $n' = 3n$ si hanno $n$ tornei da 3 al primo round ($3n$ distanze) e poi un torneo su $n$ elementi:
$$3n + \frac{3}{2}(n - 1) = \frac{6n + 3n - 3}{2} = \frac{3(3n - 1)}{2} = \frac{3}{2}(n' - 1)$$
- Ricalcolato (anche con codice per $n = 3, 9, 27, 81, 243$: 3, 12, 39, 120, 363 distanze): **corretto**. (Precisazione: il conteggio vale per il torneo in cui da ogni tripla passa **un** solo elemento, cioè quello della 1-mediana; i tornei sono $(n-1)/2$, ognuno da 3 distanze.)

## Antipole clustering (slide 114-117)
(Le slide scrivono "Antilope clustering", con la foto di un'antilope: il metodo è l'**Antipole** clustering di Cantone et al., come dice la definizione di $\sigma$-antipole.)
- $S$ in uno spazio metrico $(X, d)$, $\sigma > 0$. Un **$\sigma$-antipole** è una coppia $(a, b)$ di $S$ con $d(a, b) > \sigma$
- Due punti a distanza **massima** sono i **poli**, la loro distanza il **diametro**
- **Clustering a diametro limitato** con soglia $\sigma$: ogni cluster ha diametro $< \sigma$

**Fase 1** (ricerca di un antipole):
1. si divide $S$ in triple casuali
2. in ogni tripla si prendono i **poli** $a, b$: se $d(a, b) > \sigma$ **STOP** e si restituisce $(a, b)$; altrimenti $a$ e $b$ passano al round successivo e si scarta il terzo (la **1-mediana** della tripla)
3. si continua ricorsivamente (l'ultimo gruppo può avere 3, 4 o 5 elementi)
4. se non si trova nulla si restituisce **FAIL**
- **Teorema** (complessità **lineare**): al più **$9n$** distanze. (Verifica, aggiunta: ogni tripla costa 3 distanze e ne passano 2 su 3, quindi le triple sono circa $n/3 + 2n/9 + 4n/27 + \dots = n$ e le distanze circa $3n$, confermato con codice; $9n$ è un limite valido ma largo.)

**Fase 2**:
1. se l'antipole è FAIL il cluster **non si spezza**
2. altrimenti, con l'antipole $(a, b)$, si divide il cluster in due secondo la **vicinanza** ad $a$ o a $b$
3. si continua ricorsivamente sui due sottoinsiemi
- Figura (slide 117): divisioni successive dell'insieme in $S_A$, $S_B$ con antipole $A, B$ a distanza $> \sigma$, poi $A_1, A_2$, $B_1, B_2$, fino ai cluster $C_{A_1}, C_{A_2}, C_{B_1}, C_{B_2}$ con centro e raggio; sotto l'**albero** (Antipole tree): nodi interni con $A, B, R_A, R_B$ (poli e raggi), foglie con centro e raggio $Rad$ di ogni cluster

## Range search e nearest neighbor (slide 118-121)
- **Range query** $(q, t)$: tutti gli oggetti del database $D$ a distanza $< t$ da $q$
- **k-Nearest Neighbor query**: i $k$ oggetti di $D$ più vicini a $q$
- Con un cluster $C$ di centroide $\hat{C}$ e raggio $r = \max_{x \in C}d(x, \hat{C})$, per la **disuguaglianza triangolare**:

| Condizione | Conseguenza | Perché |
|---|---|---|
| $d(q, \hat{C}) > t + r$ | si **scarta** tutto $C$ | $d(q, o') \ge d(q, \hat{C}) - d(o', \hat{C}) \ge d(q, \hat{C}) - r > t$ |
| $d(q, \hat{C}) \le t - r$ | **tutto** $C$ è nella risposta | $d(o', q) \le d(o', \hat{C}) + d(\hat{C}, q) \le r + d(q, \hat{C}) \le t$ |
| $t - r < d(q, \hat{C}) \le t + r$ | ogni elemento va **controllato** | nessuna delle due garanzie vale |

- (La slide 118 scrive il secondo caso con $<$, la 119 con $\le$: per la disuguaglianza va bene $\le$.)
- Figura (slide 120): query $q$ (verde) con il cerchio di raggio $t$ che interseca il cluster $C_{A_1}$; i cluster $C_{A_2}$, $C_{B_1}$, $C_{B_2}$ sono lontani e si scartano
- Figura (slide 121): la stessa ricerca sull'Antipole tree, in quattro passi: la visita parte dalla radice (verde = visitato), scende nel ramo $A$; il ramo $B$ e la foglia $C_{A_2}$ diventano blu (scartati senza calcolare le distanze dai loro punti) e resta da esaminare solo $C_{A_1}$

## Clustering basato sulla densità (slide 122-128)
- Criterio di cluster **locale**: conta la **densità** con cui i punti sono connessi. Caratteristiche:
  - scopre cluster di **forma arbitraria**
  - gestisce il **rumore**
  - **un solo scan** dei dati
  - servono **parametri di densità** per la condizione di stop
- Figura (slide 122): un cluster circolare blu e uno a mezzaluna verde, con punti di rumore sparsi; **DBSCAN** (Ester et al., KDD'96)

### Definizioni (slide 123-125)
- **Eps**: raggio massimo del vicinato; **MinPts**: numero minimo di punti nell'Eps-intorno
$$N_{Eps}(q) = \{p \in D : dist(p, q) \le Eps\}$$
- **Core point**: $|N_{Eps}(q)| \ge MinPts$
- $p$ è **direttamente raggiungibile per densità** da $q$ se $p \in N_{Eps}(q)$ **e** $q$ è un core point (figura: MinPts = 5, Eps = 1 cm, $q$ core con $p$ nel suo intorno)
- $p$ è **raggiungibile per densità** da $q$ se c'è una catena $p_1 = q, \dots, p_n = p$ con $p_{i+1}$ direttamente raggiungibile da $p_i$ (la slide 124 scrive "$p_i + 1$": è $p_{i+1}$)
- $p$ è **connesso per densità** a $q$ se esiste $o$ da cui **entrambi** sono raggiungibili per densità
- (Aggiunta, non nelle slide: la raggiungibilità **non è simmetrica**, perché un punto di bordo è raggiungibile da un core ma non viceversa; la connessione per densità **è** simmetrica. Per questo il cluster si definisce con la connessione.)
- **Cluster** $C$ rispetto a Eps e MinPts: insieme **non vuoto** tale che
  1. **massimalità**: se $p \in C$ e $q$ è raggiungibile per densità da $p$, allora $q \in C$
  2. **connettività**: ogni coppia $p, q \in C$ è connessa per densità
- Figura (slide 125): Eps = 1 cm, MinPts = 5, con un punto **core**, uno di **border** (nell'intorno di un core ma non core lui stesso) e un **outlier** (rumore)

### Algoritmo (slide 126)
1. si sceglie un punto $p$ arbitrario
2. se $p$ è **core**, si raccolgono tutti i punti raggiungibili per densità da $p$: è un **cluster**. Il risultato non dipende da quale core point del cluster si parte, perché fra core point la raggiungibilità è **simmetrica**
3. altrimenti $p$ si marca come **rumore**; se è un punto di **bordo** verrà recuperato più avanti, partendo da un core vicino
4. si continua finché tutti i punti sono processati
- (Aggiunta, non nelle slide: costo $O(n^2)$ senza indice, circa $O(n\log n)$ con un indice spaziale; regole pratiche: MinPts $\ge d + 1$ e Eps scelto dal gomito del grafico delle distanze dal $k$-esimo vicino)

**Esempio** (aggiunta, non nelle slide; verificato con scikit-learn, dove l'intorno include il punto stesso): punti 1D $\{1, 2, 3, 4, 10, 11, 12, 20\}$, Eps = 1, MinPts = 3
- core: 2 ($\{1, 2, 3\}$), 3 ($\{2, 3, 4\}$), 11 ($\{10, 11, 12\}$)
- border: 1 e 4 (intorno di 2 punti, ma vicini a un core), 10 e 12
- rumore: 20
- cluster $\{1, 2, 3, 4\}$ e $\{10, 11, 12\}$

### Confronti (slide 127-128)
- Figura (slide 127): DBSCAN e k-means su cinque dataset. DBSCAN separa i due **anelli** concentrici e le due **mezze lune**, trova i gruppi e lascia un unico cluster sul quadrato **uniforme**; k-means taglia anelli e lune con una retta e divide il quadrato uniforme in settori
- Figura (slide 128), dal lavoro di Chameleon: DBSCAN su DS1 con MinPts = 4 ed Eps = 0.5 (a) e 0.4 (b). Con Eps = 0.5 le due ellissi in alto, unite da un sottile ponte di punti, diventano **un solo cluster**; con Eps = 0.4 il grande cerchio si **frammenta** in tanti piccoli cluster. Con densità diverse **nessun Eps globale** va bene (è il limite che Chameleon supera con il vicinato dinamico)

## Constraint-based clustering (slide 129-131)
- Clusterizzare oggetti in presenza di **ostacoli**. Esempio: dove piazzare i **bancomat** (ATM) perché siano accessibili ai clienti, tenendo conto di fiumi, montagne, condomini: la **distanza** deve rispettare questi **vincoli**
- Figura (slide 129): stessa mappa clusterizzata **senza** e **con** gli ostacoli: senza, i cluster scavalcano i fiumi
- Meglio un **k-medoids** di un k-means: il centro di un cluster k-means potrebbe cadere **dentro un ostacolo**
- **Visibilità**: $p$ è visibile da $q$ nella regione $R$ se il segmento $pq$ non interseca ostacoli
- **Grafo di visibilità** $VG = (V, E)$: i nodi sono i **vertici degli ostacoli** (più i punti da clusterizzare), arco fra $v_1$ e $v_2$ se sono visibili fra loro. Figura (slide 130): due ostacoli poligonali $o_1$, $o_2$ con gli archi di visibilità fra i loro vertici e i punti $p$, $q$
- La **distanza** da usare è lo **shortest path** in $VG$ fra i due punti
- Poi si clusterizza con queste distanze. (Errore di coerenza nella slide 131: dice "usiamo **k-means**", mentre la slide 129 ha appena motivato il k-medoids; con distanze da cammino minimo non c'è una media da calcolare e il centro potrebbe finire in un ostacolo, quindi serve un metodo a **medoidi**. Aggiunta: il metodo di riferimento, COD-CLARANS, è infatti un k-medoids.)
- **Ottimizzazione**: **triangolazione** dello spazio e **micro-cluster** dentro ogni triangolo; ogni micro-cluster è rappresentato da **un solo punto**, così il numero di punti da clusterizzare scala con il numero di micro-cluster invece che con i dati (figura: regione con due ostacoli scuri triangolata, ingrandimento di un triangolo con i micro-cluster)

## Da ricordare per lo scritto
- Clustering = **non supervisionato**, classi incognite; buono = alta similarità **intra**, bassa **inter**; **hard** vs **soft** (gradi di appartenenza)
- Criterio (cosa) vs algoritmo (come); NP-hard: $S(n, s) \approx s^n/s!$ ($10^{67}$ per $n = 100$, $s = 5$), numeri di **Bell** se $s$ non è noto ($B_3 = 5$)
- $J_e = \sum_i\sum_{x \in C_i}\|x - \hat{x}_i\|^2$ (SSE, centroide con $1/n_i$): buono per cluster sferici, male per allungati e annidati; con il vicino più vicino ($\min$) non penalizza i cluster allungati
- **K-means**: input $k$ e soluzione iniziale, assegna/ricalcola fino a stabilità, $O(tkn)$, minimi locali, sferici con euclidea, ellissoidali con Mahalanobis, sensibile agli outlier, niente dati categoriali; più avvii o k-means++
- Numero di cluster: $J_e = 0$ per $k = n$; **gomito**; **silhouette** $s = \frac{b - a}{\max(a, b)} \in [-1, 1]$ (non $|b - a|$), $a$ e $b$ distanze **medie**, si massimizza la media, costo $O(n^2)$; nell'esempio il massimo è a $k = 2$ (0.705) anche se i gruppi sono 4 (0.651)
- **PAM**: medoidi, scambio se il costo cala, $O(k(n - k)^2)$ per iterazione, robusto agli outlier; **CLARA**: PAM su più campioni, dipende dal campione
- **BFR**: k-means scalabile, gaussiane con assi allineati; **DS** (certi), **CS** (sottocluster compressi), **RS** (punti singoli); statistiche $N$, $SUM$, $SUMSQ$ ($2k + 1$ numeri), $\mu_i = SUM_i/N$, $\sigma_i^2 = SUMSQ_i/N - (SUM_i/N)^2$; raggio di Mahalanobis sotto soglia (es. 4); all'ultimo round CS e RS al DS più vicino
- **Fuzzy K-means**: $J = \sum\sum P^m\|x_j - \theta_i\|^2$, centroidi pesati con $P^m$, $P(C_i \mid x_j) = 1/\sum_k(d_{ij}/d_{kj})^{2/(m-1)}$, $m = 2$ tipico; dipende dal numero di cluster
- **GMM + EM**: $p(x) = \sum\alpha_ip_i(x \mid \mu_i, \Sigma_i)$, log-likelihood con la somma nel log; E-step = valore atteso $Q(\Theta \mid \Theta^g)$ (responsabilità), M-step = $\arg\max Q$; cluster ellissoidali; attenzione all'underflow
- **Gerarchico** agglomerativo, dendrogramma, taglio a un livello; linkage **single** (min, trova forme allungate, effetto catena), **complete** (max), **average**, **Ward** (minimo aumento della varianza), centroidi, medoidi; $O(n^2)$ e fusioni irrevocabili
- **BIRCH**: $CF = (N, LS, SS)$, additivo; $R = \sqrt{SS/N - (LS/N)^2}$; esempio $CF = (5, (16, 30), (54, 190))$, $R = 1.6$; CF-tree con $B$ (figli) e $T$ (diametro massimo delle foglie); inserimento con assorbimento se $D < T$, altrimenti nuova entry/split; lineare, una sola lettura, ma solo numerici, sensibile all'ordine, solo sferici
- **BIRCH*/GRGPF**: metrica qualsiasi, **clusteroide** = minima rowsum, raggio $\sqrt{rowsum/N}$, $2p + 1$ rowsum tenute, $rowsum(X) \approx N(r^2 + D(\hat{C}, X)^2)$ per Pitagora in alta dimensionalità
- **DTC**: taglio dinamico del dendrogramma, trova cluster annidati, Dynamic Hybrid per i membri periferici
- **ROCK**: dati categoriali, vicini se Jaccard $\ge \theta$, **link** = vicini comuni, $f(\theta) = \frac{1 - \theta}{1 + \theta}$, goodness = link osservati / link attesi
- **CURE**: $c$ rappresentativi lontani fra loro spostati del 20% verso il centroide; cluster non sferici
- **Chameleon**: kNN graph, partizionamento con hMETIS, fusione con interconnettività relativa $RI$ e vicinanza relativa $RC$; ROCK guarda solo l'interconnettività, CURE solo la vicinanza; forme arbitrarie, $O(n^2)$
- 1-mediana a tornei di triple: $\frac{3}{2}(n - 1)$ distanze per $n = 3^r$; **antipole**: coppia a distanza $> \sigma$, poli = diametro, si scarta la 1-mediana della tripla, lineare ($\le 9n$), poi split ricorsivo verso $a$ o $b$ fino a diametro $< \sigma$
- Range query con cluster di raggio $r$: $d(q, \hat{C}) > t + r$ scarto tutto, $\le t - r$ prendo tutto, altrimenti controllo i punti
- **DBSCAN**: Eps, MinPts, core ($|N_{Eps}| \ge MinPts$), border, rumore; direttamente raggiungibile, raggiungibile (catena, non simmetrica), connesso (simmetrica); cluster = massimale e connesso; forme arbitrarie e rumore, ma un solo Eps globale (male con densità diverse)
- **Constraint-based**: ostacoli, distanza = cammino minimo nel grafo di visibilità, k-medoids (il centro non deve cadere in un ostacolo), micro-cluster da triangolazione
