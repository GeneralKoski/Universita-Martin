# Programmazione dinamica e allineamento di sequenze

Fonte: `Programmazione dinamica.pdf` (72 slide; lezione 13, "Serie temporali (parte 2) + Programmazione dinamica")

Il deck ha quattro blocchi: **DTW** (slide 2-11), la **programmazione dinamica** in generale con Fibonacci e le catene di montaggio (12-26), **SAX/PAA** (27-31), l'**allineamento di sequenze** biologiche: Needleman-Wunsch, Hirschberg, Smith-Waterman, BLAST, allineamento multiplo (32-72).

## Dynamic Time Warping (DTW)
- Algoritmo per misurare la **similarità tra due o più serie temporali**: produce un **allineamento** fra le due sequenze e, da questo, una **misura di distanza**
- Utile quando le componenti hanno caratteristiche che **variano nel tempo** e la semplice **espansione o compressione lineare** delle due sequenze non basta
- Esempio della slide 2:
  ```python
  x = numpy.arange(0, 20, .5)
  s1 = np.sin(x)
  s2 = np.sin(x - 1)
  ```
  Figura: le due sinusoidi (40 punti) una sopra l'altra, con linee gialle che collegano i punti abbinati dal DTW: ogni picco è collegato al picco corrispondente, non al punto con lo stesso indice. (Il codice mescola `numpy.` e `np.`: serve `import numpy` **e** `import numpy as np`. Eseguito: la distanza euclidea punto a punto è 4,383, il DTW con costo $|a-b|$ vale 2,761, il warping path ha 42 passi. Non è 0 perché ai bordi le due serie non hanno un corrispettivo.)
- **Riconoscimento vocale**: chi parla più veloce o più lento della voce campione non disturba il DTW, mentre disturba una distanza "punto per punto"
- Figura (slide 3) "Time Series Aligned by DTW": Signal 1 (blu) e Signal 2 (rosso tratteggiato), circa 70 campioni, con le linee di abbinamento che si **addensano** dove una serie è più lenta dell'altra
- Molto usato in ambito **IoT** (stream da video, audio, sensori trasformati in sequenze lineari), efficace con serie ad **alta frequenza di campionamento** (utilities, automotive)

### Regole dell'allineamento
L'idea è calcolare la distanza fra due serie **indipendentemente dalla loro lunghezza**, rispettando:
- ogni indice della prima sequenza deve poter essere confrontato con gli indici dell'altra e viceversa. (Precisazione: la slide dice "con tutti gli indici delle altre"; la regola standard è che ogni indice va abbinato ad **almeno uno** dell'altra sequenza.)
- il **primo** indice della prima è associato al **primo** dell'altra (ma non deve essere la sua unica corrispondenza)
- l'**ultimo** indice della prima corrisponde all'**ultimo** dell'altra (idem)
- la mappatura degli indici è **monotona crescente**: niente incroci all'indietro

### Calcolo della matrice
- Matrice $DTW$ di dimensione $(n+1) \times (m+1)$, con $n$ e $m$ lunghezze delle serie (la slide lo dice come "$n \times m$ dove $m$ ed $n$ sono la lunghezza delle serie più 1")
- $DTW[0, 0] = 0$, il resto di prima riga e prima colonna $= \infty$
- Da $DTW[1, 1]$ in poi, a ogni cella si somma alla distanza locale fra i due punti il **minimo** fra tre predecessori:
  $$DTW[i, j] = d(s_i, t_j) + \min(DTW[i-1, j],\ DTW[i, j-1],\ DTW[i-1, j-1])$$
  - slide 5: precedente **sulle righe** = **cancellazione**, precedente **sulle colonne** = **inserimento**, **diagonale** = **corrispondenza** (match)
- Pseudocodice (slide 6), `DTWDistance(s: array [1..n], t: array [1..m])`: inizializza tutto a infinito, `DTW[0,0] := 0`, poi i due cicli con `cost := d(s[i], t[j])` e il minimo dei tre vicini; restituisce `DTW[n, m]`
- (Osservazione: i nomi dei due spostamenti sono **scambiati** fra le due slide. Nella 5 il precedente sulle righe, $DTW[i-1, j]$, è la cancellazione; nei commenti del codice della 6 `DTW[i-1, j]` è `// insertion` e `DTW[i, j-1]` è `// deletion`. È solo una convenzione, ma conviene fissarne una all'orale.)

### Warping path
- Riempita la matrice si costruisce il **warping path**, muovendosi in orizzontale, verticale o obliquo verso il valore minimo
- spostamento **orizzontale**: la serie 2 è **accelerata** in quell'intervallo; **verticale**: è **decelerata**
- il **valore finale** del path, $DTW[n, m]$, è la **distanza** fra le serie
- (Precisazione: la slide dice di partire da $DTW[0, 0]$ e andare da sinistra verso destra. Il percorso ottimo si ricostruisce invece **all'indietro** da $DTW[n, m]$, scegliendo a ogni passo il predecessore con il valore minimo; andare in avanti scegliendo il vicino minimo è una strategia greedy che non garantisce il percorso ottimo.)

Esempio della slide 7, verificato: sequenza X $= 1, 2, 3, 4, 3, 2, 1, 1, 1, 2$ sulle colonne, sequenza Y $= 0, 1, 1, 2, 3, 4, 3, 2, 1, 1$ sulle righe. Ricalcolando la matrice con costo $(x - y)^2$ si ottengono **esattamente** i valori della slide:

| | 1 | 2 | 3 | 4 | 3 | 2 | 1 | 1 | 1 | 2 |
|---|---|---|---|---|---|---|---|---|---|---|
| **0** | **1** | 5 | 14 | 30 | 39 | 43 | 44 | 45 | 46 | 50 |
| **1** | **1** | 2 | 6 | 15 | 19 | 20 | 20 | 20 | 20 | 21 |
| **1** | **1** | 2 | 6 | 15 | 19 | 20 | 20 | 20 | 20 | 21 |
| **2** | 2 | **1** | 2 | 6 | 7 | 7 | 8 | 9 | 10 | 10 |
| **3** | 6 | 2 | **1** | 2 | 2 | 3 | 7 | 11 | 13 | 11 |
| **4** | 15 | 6 | 2 | **1** | 2 | 6 | 12 | 16 | 20 | 15 |
| **3** | 19 | 7 | 2 | 2 | **1** | 2 | 6 | 10 | 14 | 15 |
| **2** | 20 | 7 | 3 | 6 | 2 | **1** | 2 | 3 | 4 | 4 |
| **1** | 20 | 8 | 7 | 12 | 6 | 2 | **1** | **1** | **1** | 2 |
| **1** | 20 | 9 | 11 | 16 | 10 | 3 | 1 | 1 | **1** | **2** |

- Il path evidenziato (in grassetto) scende due volte in verticale, poi in diagonale, fa tre passi orizzontali sulla penultima riga, scende e chiude a destra: **distanza DTW = 2**. (Dall'ultima cella c'è un pareggio fra diagonale e verticale, entrambe valgono 1: un traceback automatico può scegliere la diagonale, con lo stesso valore finale.)
- (Osservazione: la slide 5 parla di "distanza euclidea", ma i valori della matrice sono **differenze al quadrato**: già la prima riga fa $1, 1+4, 5+9, 14+16, \dots$. Con $|x-y|$ la distanza finale qui è comunque 2, perché le differenze lungo il path sono 0 o 1. La matrice della figura non mostra la riga e la colonna di infiniti.)

### Complessità e finestra
- Costo $O(n \times m)$. Con sequenze molto lunghe confrontare posizioni lontanissime è costoso e anche **inutile**: si introduce un parametro $w$, una **finestra temporale** attorno alla diagonale
- La slide dice: la finestra è il **minimo** fra un intero scelto dall'utente e $|m - n|$. **Errore nella slide 8**: va presa il **massimo**, $w = \max(w_{utente}, |n - m|)$. Con una finestra più stretta di $|n - m|$ l'angolo $DTW[n, m]$ non è raggiungibile. Verificato: con serie di lunghezza 10 e 7 e $w = \min(1, 3) = 1$ la distanza viene $\infty$, con $w = \max(1, 3) = 3$ viene 0 come senza finestra; con due serie di uguale lunghezza la regola della slide dà sempre $w = 0$, cioè solo la diagonale, il confronto punto a punto (6 invece di 0 sull'esempio provato)
- (Aggiunta: è la **banda di Sakoe-Chiba**.)
- Figura: a sinistra "Dynamic Time Warping", il path a scalini sulla griglia fra Sequence A e Sequence B, con una freccia su un tratto verticale; a destra "Local Time Warping", dove il path è sostituito da una **curva liscia** $f(\theta)$. Sotto, il risultato: col DTW la soluzione ha **discontinuità indesiderate** ("Undesired discontinuities"), con la funzione liscia no
- Un'altra alternativa è **FastWTD**. (La sigla corretta è **FastDTW**, Salvador e Chan 2007: approssima il DTW in tempo lineare lavorando a risoluzioni crescenti.)

### DTW e Machine Learning
- **supervisionato**: come distanza per **KNN** su serie temporali
- **non supervisionato**: come misura di similarità nel **clustering** di serie temporali
- **semi-supervisionato**: si etichettano le serie con un clustering basato su DTW e poi si classifica secondo queste assegnazioni
- Figura (slide 10), sei pannelli: sequenze originali (tante random walk sovrapposte), **centroidi** (tre curve), Cluster A trend costante (rosso), Cluster B trend decrescente (verde), Cluster C trend crescente (blu), sequenze etichettate con i tre colori

### Altre misure basate sull'allineamento
- Il DTW è la più nota ma non l'unica; alcune si basano su **match locali** invece che sull'intera serie: **Longest Common Sub-Sequence (LCSS)** e **Longest Common Substring (LCS)**. (Attenzione alla sigla: in letteratura LCS indica spesso la *subsequence*; la sottosequenza può saltare elementi, la sottostringa deve essere contigua.)
- Serie **eterogenee** (elementi in spazi diversi, non confrontabili direttamente):
  - **Canonical Time Warping** (Zhou e De la Torre 2009): trova uno **spazio comune** con l'analisi di correlazione canonica e un percorso di allineamento ottimo alla DTW
  - lavori più recenti mappano le caratteristiche di una serie nello **spazio delle caratteristiche** dell'altra (Vayer et al. 2020) o abbinano **matrici di auto-somiglianza** (Cohen et al. 2020)

## Programmazione dinamica
- Approccio per risolvere in modo efficiente un **problema di ottimizzazione**: più soluzioni possibili, ognuna con un **costo**, si cerca quella di costo **minimo** (o massimo), la **soluzione ottimale**
- Come **divide-et-impera** combina le soluzioni di **sottoproblemi**, ma si applica anche quando i sottoproblemi **non sono indipendenti**
- Risolve i sottoproblemi in comune **una sola volta**, divide-et-impera **più volte**

### Fibonacci
Definizione della slide: $F(n) = 1$ se $n \le 1$, altrimenti $F(n-1) + F(n-2)$ (convenzione con $F(0) = F(1) = 1$, quindi $F(5) = 8$).

```python
def Fib(n):
    if n <= 1:
        return 1
    else:
        return Fib(n-1) + Fib(n-2)
```
- La slide ricava: essendo $T(n-1) > T(n-2)$, $T(n) = 2 \cdot T(n-2) + \Theta(1)$, albero di ricorsione binario completo di altezza $\lfloor n/2 \rfloor$ con $2^{\lfloor n/2 \rfloor + 1} - 1$ nodi, "complessità totale $2^n$"
- **Errore nella slide 13**: il ragionamento non porta a $2^n$. Da $T(n-1) > T(n-2)$ segue $T(n) > 2T(n-2) + \Theta(1)$, che è un **limite inferiore**, $\Omega(2^{n/2})$ (il disuguale è diventato uguale). Il limite superiore viene dall'altra parte, $T(n) < 2T(n-1) + \Theta(1)$, cioè $O(2^n)$. Il valore esatto sta in mezzo: $\Theta(\varphi^n)$ con $\varphi = \frac{1+\sqrt5}{2} \approx 1{,}618$. Verificato contando le chiamate: sono $2F(n) - 1$; per $n = 30$ sono 2.692.537, contro $2^{15} = 32.768$ e $2^{30} \approx 1{,}07 \cdot 10^9$
- Figura (slide 14): albero delle chiamate di $Fib(5)$. **$Fib(1)$ viene calcolato 5 volte, $Fib(0)$ e $Fib(2)$ 3 volte, $Fib(3)$ 2 volte**: è la ripetizione che la programmazione dinamica elimina

**Memoization** (slide 15): si memorizzano in una tabella i valori già calcolati; se $n$ è già visto si legge dalla tabella, altrimenti si calcola e si memorizza. Efficiente se lettura e scrittura sono in **tempo costante** (un `dict`).
```python
table = dict() # chiave n -> valore F(n)
def MemoFib(n):
    if n <= 1:
        return 1
    else:
        if n in table:
            return table[n]
        else:
            return MemoFib(n-1) + MemoFib(n-2)
```
- **Errore nella slide 15**: il codice **non scrive mai** nella tabella, quindi `n in table` è sempre falso e la funzione è identica a `Fib`. Eseguito: `MemoFib(25)` fa 242.785 chiamate, come `Fib(25)`, e alla fine `table` è vuota. Va memorizzato il risultato prima di restituirlo:
  ```python
  else:
      table[n] = MemoFib(n-1) + MemoFib(n-2)
      return table[n]
  ```
  Così `MemoFib(25)` fa 49 chiamate

**Bottom-up** (slide 16): per $F(n)$ servono sempre **tutti** gli $F(i)$ con $0 \le i < n$, già risolti; allora si parte da $F(0)$ e si risale fino a $F(n)$, in **$\Theta(n)$**.
```python
def IterFib(n):
    # un semplice array di dimensione n
    F = numpy.empty([10,1], dtype=int)
    F[0] = F[1] = 1
    for i in range(2,n+1):
        F[i] = F[i-1] = F[i-2]
    return F[n]
```
- **Errore nella slide 16**, due bug. (1) `F[i] = F[i-1] = F[i-2]` è un'**assegnazione a catena**, non una somma: copia 1 dappertutto. Eseguito: `IterFib(5)` restituisce `[1]` invece di 8. (2) L'array ha dimensione fissa 10, non $n$ come dice il commento: `IterFib(10)` dà `IndexError: index 10 is out of bounds`. Corretto: `F = numpy.empty(n+1, dtype=int)` e `F[i] = F[i-1] + F[i-2]`; restituisce 1, 2, 8, 89, 121393 per $n = 1, 2, 5, 10, 25$. (Con la forma `[10,1]` restituisce anche un array di un elemento invece di un intero.)

### I quattro passi
1. **caratterizzare** la struttura di una soluzione ottima
2. **definire ricorsivamente** il valore di una soluzione ottima
3. **calcolare** il valore in modo **bottom-up**, **memorizzando** in tabelle i valori delle sottosoluzioni ottime
4. **costruire** una soluzione ottima dalle informazioni calcolate (non serve se basta il valore ottimo)
- Nota storica: inventata da **Bellman** (la slide scrive "Bellmann") negli anni '50 per problemi di schedulazione. "Dinamica" per l'aspetto che **varia nel tempo** e perché "suonava impressionante"; "programmazione" nel senso di trovare un **programma** (piano) ottimale, non di scrivere codice

### Quando conviene
- quando un algoritmo ricorsivo invocherebbe **più volte lo stesso sottoproblema**; altrimenti basta divide-et-impera
- risolve ogni sottoproblema **una sola volta** e riusa il valore quando si ripresenta
- lo spazio dei sottoproblemi deve essere **piccolo**: il numero di sottoproblemi distinti deve essere **polinomiale** nella dimensione dell'input
- si memorizza la soluzione di ogni sottoproblema in una tabella (**memoization**). (Precisazione sui termini: in senso stretto *memoization* è la versione **top-down** ricorsiva con cache, come `MemoFib`; quella **bottom-up** si chiama *tabulation*. La slide 18 usa memoization per entrambe.)
- Le due condizioni (slide 26):
  - **sottostruttura ottima**: una soluzione ottima del problema contiene al suo interno soluzioni ottime di sottoproblemi. È un segno che la DP si può usare, ma si potrebbero usare anche **divide-et-impera** e **greedy**
  - **sottoproblemi sovrapposti**
- La sottostruttura ottima varia da problema a problema per il **numero di sottoproblemi** nella soluzione ottima e per il **numero di scelte** su quali sottoproblemi usare

### Catene di montaggio (assembly line scheduling)
- Uno chassis attraversa $n$ stazioni su una qualunque di **due linee**; $a_{i,j}$ è il **tempo di stazionamento** nella stazione $S_{i,j}$, $t_{i,j}$ il **tempo di trasferimento** dalla linea $i$ all'altra dopo la stazione $j$; $e_i$ e $x_i$ i tempi di entrata e uscita. Si cerca il percorso di **tempo minimo**
- Dato un percorso, il suo tempo si calcola in $\Theta(n)$, ma i percorsi sono **$2^n$**: la forza bruta non è fattibile
- **Sottostruttura ottima**: il percorso più veloce fino a $S_{1,j}$ ($j > 1$) passa o per il più veloce fino a $S_{1,j-1}$ e poi direttamente a $S_{1,j}$, o per il più veloce fino a $S_{2,j-1}$ e poi il trasferimento
- **Ricorrenza**, con $f_i[j]$ tempo minimo all'uscita di $S_{i,j}$ e $f^*$ tempo minimo totale:
  $$f^* = \min(f_1[n] + x_1,\ f_2[n] + x_2)$$
  $$f_1[1] = e_1 + a_{1,1} \qquad f_2[1] = e_2 + a_{2,1}$$
  $$f_1[j] = \min(f_1[j-1] + a_{1,j},\ f_2[j-1] + t_{2,j-1} + a_{1,j}) \quad j > 1$$
  $$f_2[j] = \min(f_2[j-1] + a_{2,j},\ f_1[j-1] + t_{1,j-1} + a_{2,j}) \quad j > 1$$
- Per ricostruire il percorso: $l_i[j]$ = linea della stazione $j-1$ che precede $S_{i,j}$ nel percorso più veloce, $l^*$ = linea della stazione $n$
- Pseudocodice (slide 24): `Fastest-Way(a, t, e, x, n)` riempie $f$ e $l$ con gli `if ... <= ...` della ricorrenza; `Print-Stations(l, n)` parte da $i = l^*$, stampa la stazione $n$ e risale con `i ← l_i[j]` per $j$ da $n$ a 2

Esempio (slide 20 e 23), $n = 6$: $e = (2, 4)$, $x = (3, 2)$, linea 1 $a = 7, 9, 3, 4, 8, 4$, linea 2 $a = 8, 5, 6, 4, 5, 7$, trasferimenti $t_1 = 2, 3, 1, 3, 4$ e $t_2 = 2, 1, 2, 2, 1$.

| $j$ | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|
| $f_1[j]$ | 9 | 18 | 20 | 24 | 32 | 35 |
| $f_2[j]$ | 12 | 16 | 22 | 25 | 30 | 37 |
| $l_1[j]$ | | 1 | 2 | 1 | 1 | 2 |
| $l_2[j]$ | | 1 | 2 | 1 | 2 | 2 |

$f^* = 38$, $l^* = 1$. Percorso: linea 1, 2, 1, 2, 2, 1 (tempo $2+7+2+5+1+3+1+4+5+1+4+3 = 38$). Verificato in Python traducendo `Fastest-Way` e `Print-Stations`: tabelle, $f^*$, $l^*$ e percorso coincidono con la slide.

**Versione ricorsiva** (slide 25): esponenziale. Con $r_i(j)$ numero di chiamate per $f_i[j]$: $r_1(n) = r_2(n) = 1$, $r_1(j) = r_2(j) = r_1(j+1) + r_2(j+1)$, quindi $r_i(j) = 2^{n-j}$: $f_1[1]$ viene chiamata $2^{n-1}$ volte e il totale è $\Theta(2^n)$. Calcolando $f_1[j]$ e $f_2[j]$ per $j$ crescente si scende a **$\Theta(n)$**. (Verificato: la ricorsione ingenua su entrambe le linee fa esattamente $2^{n+1} - 2$ chiamate, 126 per $n = 6$, 131.070 per $n = 16$.)

## SAX (Symbolic Aggregate approXimation)
- Metodo per **semplificare** le serie storiche trasformandole in una **sequenza di simboli**; ogni simbolo rappresenta un **intervallo** di valori
- È una **riduzione della dimensionalità**, quindi un metodo **non supervisionato**
- La slide dice che SAX è molto **robusta ai valori mancanti** "e quindi" utilizzabile con serie di **lunghezza diversa**. (Precisazione: le due cose non sono legate. Serie di lunghezza diversa diventano confrontabili perché la PAA le riduce allo **stesso numero di segmenti** $m$; i valori mancanti, al più, pesano poco perché ogni segmento è una media.)
- Le serie vanno **standardizzate** per avere la stessa scala: $Z = \frac{x - \mu}{\sigma}$

### PAA (Piecewise Aggregate Approximation)
- SAX riduce la dimensionalità con la **PAA**: si "riassume" la sequenza in **segmenti** che ne riducono la lunghezza ma ne conservano l'informazione
- Figura (slide 28): serie di 15 punti (valori fra circa 1,5 e 9, letti dal grafico) con sovrapposta la PAA a gradini rossi tratteggiati, ognuno la media del suo tratto
- Formula della slide: $\bar X_i = \frac{m}{n} \cdot \sum_{j = n/N(i-1)+1}^{(n/M)i} x_j$. **Errore nella slide 29** (di notazione): negli estremi compaiono $N$ e $M$ maiuscole mai definite, e la serie si chiama $Y$ ma nella somma diventa $x$. Con $Y$ di lunghezza $n$ ridotta a $m$ segmenti:
  $$\bar X_i = \frac{m}{n} \sum_{j = \frac{n}{m}(i-1)+1}^{\frac{n}{m} i} Y_j$$
  cioè la **media** di ogni finestra di $n/m$ punti. Casi particolari: $m = n$ restituisce la serie originale, $m = 1$ un solo valore, la media dell'intera serie (verificato: su 16 punti $0, \dots, 15$ con $m = 4$ dà $1{,}5;\ 5{,}5;\ 9{,}5;\ 13{,}5$)
- Si sceglie la **dimensione $w$ della finestra**, che decide quanti segmenti si usano: la serie ridotta ha $\text{lunghezza}/w$ periodi, ognuno con la media del periodo. Se il numero di periodi non è intero va **arrotondato per eccesso** per non perdere informazione (es. 15 punti con $w = 2$: $\lceil 7{,}5 \rceil = 8$ periodi, l'ultimo con un punto solo)

### SAX string
- Il valore numerico diventa una **stringa**: si sceglie il **numero di livelli** in cui dividere i valori, ogni livello ha un'**etichetta**, le etichette dei segmenti concatenate formano la **SAX string**
- La scelta dei livelli influisce sul risultato: meglio farsi affiancare da un **esperto di dominio** e **non creare troppi livelli**, altrimenti l'eterogeneità è troppo alta e non si trovano pattern
- I livelli possono essere **fissati** oppure **calcolati a ogni periodo**
- (Aggiunta, non nelle slide: nel SAX classico di Lin e Keogh i livelli si fissano con i **quantili della normale standard**, così ogni simbolo è equiprobabile su dati standardizzati. Per 3 simboli i confini sono $-0{,}43$ e $0{,}43$, per 4 sono $-0{,}67$, $0$, $0{,}67$, calcolati con `statistics.NormalDist().inv_cdf(k/a)`. Esempio: la serie della figura, standardizzata e ridotta a 5 segmenti con PAA $-0{,}88;\ 1{,}43;\ 0{,}74;\ -0{,}16;\ -1{,}13$, con 3 simboli diventa `accba`.)

## Allineamento di sequenze
- **Appaiamento delle regioni simili** condivise da due sequenze
- Figura (slide 32): **allineamento globale**, sequenze allineate per **tutta la lunghezza** (gap se le lunghezze sono diverse); **allineamento locale**, non richiede di confrontare le sequenze per intero, solo i tratti simili
- Nasce in **bioinformatica**: confrontare le sequenze di **due proteine** di specie diverse con un presunto **progenitore comune**, per capire come una sia stata **modificata** per ottenere l'altra
- Una proteina cambia per **mutazioni** della sequenza codificante, **puntiformi** (una base) o più estese. La slide elenca come puntiformi:
  - **sostituzione**: una base viene sostituita con un'altra
  - **inserzione**: una o più basi vengono inserite
  - **delezione**: una o più basi vengono tolte
  - **inversione**: un tratto di DNA si inverte
  - (Osservazione: "una o più basi" e l'inversione di un tratto non sono puntiformi per definizione; puntiformi in senso stretto sono sostituzione e inserzione/delezione di **una** base.)
- Obiettivo: convertire le sequenze con il **minor numero di cambiamenti**, con un punteggio per
  - **MATCH**: similarità positiva
  - **MISMATCH**: similarità negativa
  - **GAP**: similarità negativa, ma che può **migliorare l'allineamento** complessivo
- Figura (slide 34): con soli mismatch, `ATTCGTAAGCGTCCTCATAGCTGCAGT` su `ATTCATAAGGGTCGTCAGTGCTGCAGT` (22 match su 27, verificato); con gap da inserimenti e cancellazioni, `IPLMTRWDQEQESDFGHKLP-IYTREWCTRG` su `CHKIPLMTRWDQ-QESDFGHKLPVIYTREW`. (Nella slide 40 la stessa seconda sequenza ha una P al posto della D, `CHKIPLMTRWPQ...`: piccola incoerenza fra le due figure.)
- Per due sequenze biologiche: **massimizzare** le coppie allineate con punteggio positivo, **minimizzare** gap e coppie con punteggio negativo
- Il problema si **decompone**: prima si allineano in modo ottimo coppie di singoli elementi, poi **sottosequenze** sempre più grandi: è la struttura da programmazione dinamica
- Figura (slide 36), **dogma centrale della biologia**: DNA → (trascrizione) → RNA → (traduzione) → proteina

### Matrici di sostituzione
- Una proteina si identifica con la sequenza **nucleotidica** (DNA) o **aminoacidica**; gli aminoacidi sono un alfabeto di **20** (a volte 21) caratteri
- La similarità fra aminoacidi non deve basarsi solo sull'**identità** ma sulle caratteristiche **chimico-fisiche**:
  - una coppia **S/T** deve valere più di **S/W**
  - alcuni aminoacidi sono più **conservati**: **C/C** deve essere premiato più di **A/A**
  - gruppi: **aromatici** WYF, **idrofobici** VILMA, **polari carichi** KRDE, **polari non carichi** HCSTQNPG
- Una **matrice di sostituzione** è una griglia **20 × 20** con il punteggio di ogni coppia; nelle figure (PAM250 e BLOSUM45) è disegnata **triangolare** perché è **simmetrica**
- (Verificato con Biopython 1.88: PAM250 S/T $= 1$, S/W $= -2$, C/C $= 12$, A/A $= 2$; BLOSUM45 S/T $= 2$, S/W $= -4$, C/C $= 12$, A/A $= 5$. Gli esempi della slide tornano.)
- (Osservazione sulla figura della PAM250: la cella C/C riporta 4, nella PAM250 vale **12**, come si legge anche nella BLOSUM45 accanto.)

### Algoritmo esaustivo: scorrimento senza gap
- Si fa **scorrere** una sequenza sull'altra, con una matrice identità (1 per carattere uguale, 0 altrimenti)
- Figura (slide 39): `AAKKQV` contro `AAKWQ` in tutte le 10 posizioni; il migliore è l'allineamento dall'inizio, score 4 (A, A, K, Q), gli altri fanno 0, 1 o 2. "Combinazioni possibili: 6 × 5 = 30" è il numero di **confronti fra caratteri** su tutti gli scorrimenti, non il numero di posizioni (verificato: 10 scorrimenti, 30 confronti in totale)
- Complessità $O(n \cdot m)$, $O(n^2)$ se $n \approx m$; con $k$ sequenze $O(n^k)$
- **Problema**: non si considerano ancora i **gap**. Il numero di modi di inserirli è $\binom{n+m}{m} \approx 2^{m+n}$. (Precisazione: è un ordine di grandezza per eccesso; per $n = m$ vale $\binom{2n}{n} \approx \frac{4^n}{\sqrt{\pi n}}$. Il punto è che cresce in modo **esponenziale**.)

### Il problema dei gap
- Score **senza gap** per due sequenze $A = (a_1, \dots, a_L)$ e $B = (b_1, \dots, b_L)$: $\sum_{i=1}^{L} S(a_i, b_i)$, con $S$ dalla matrice di sostituzione
- Score **con gap**: si penalizzano l'**apertura** e l'**estensione** di ogni gap, così si inseriscono solo i gap davvero vantaggiosi:
  $$\sum_{i=1}^{L} S(a_i, b_i) - \sum_{j=1}^{G} \left(\gamma + \delta\,[len(j) - 1]\right)$$
  con $G$ numero di gap, $\gamma$ penalità di **apertura**, $\delta$ penalità di **allungamento** (è la **affine gap penalty**)
- Esempio (slide 40), con matrice identità: miglior allineamento **senza gap** score **14** (7 + 1 + 6 match); **con gap** score $24 - (2 \times 5) = 14$, due gap di lunghezza 1 con $\gamma = 5$. Verificato: 14 è il massimo su tutti gli scorrimenti, e l'allineamento con i due gap ha 24 match. (Osservazione: con queste penalità i due allineamenti **pareggiano**; con $\gamma < 5$ vincerebbe quello con i gap.)

## Allineamento globale
- Allineamento con il **massimo numero di elementi** allineati, esteso a **tutta la sequenza** (similarità globali); gap se le lunghezze sono diverse
- Algoritmo di **Needleman e Wunsch (1970)** (la slide scrive "Needelman")
- Figura (slide 42): due sequenze con blocchi A, B, C: se l'ordine dei blocchi è lo stesso l'allineamento globale funziona; con blocchi in ordine inverso (A B contro B A) ne allinea solo una parte

### Needleman-Wunsch
- **Obiettivo**: il miglior allineamento di $A$ e $B$ che comprenda **ogni elemento** di entrambe
- **Vincoli** dell'allineamento globale, secondo la slide:
  - simmetria: $S(A, B) = S(B, A)$
  - $S(A, B) \le S(A, C) + S(B, C)$, descritta come "migliore o uguale" alla somma
  - (Precisazione: la seconda è la **disuguaglianza triangolare**, che vale per le **distanze** (es. edit distance: $d(A, B) \le d(A, C) + d(C, B)$), non per gli score di similarità; e "migliore o uguale" contraddice il $\le$ se più alto vuol dire più simile.)

**Formulazione originale del 1970** (slide 44-50), senza penalità di gap:
1. matrice $n \times m$ con 1 dove i caratteri sono **identici**, 0 altrimenti (esempio: righe `AYCYNRCKCRBP`, colonne `ABCNYRQCLCRPM`)
2. **trasformazione** a partire dalla cella **in basso a destra**: a ogni cella si somma il **massimo** fra le celle della riga sotto (a destra della diagonale) e della colonna a destra (sotto la diagonale), cioè la "coppia riga-colonna con l'angolo in alto a sinistra in basso a destra della cella"
3. **traceback**: dal **valore massimo** (in alto a sinistra, 8) si scende verso il basso a destra seguendo il percorso che realizza il punteggio più alto

Matrice finale (slide 47), ricalcolata in Python con la regola del punto 2 e identica alla slide:

| | A | B | C | N | Y | R | Q | C | L | C | R | P | M |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **A** | 8 | 7 | 6 | 6 | 5 | 4 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **Y** | 7 | 7 | 6 | 6 | 6 | 4 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **C** | 6 | 6 | 7 | 6 | 5 | 4 | 4 | 4 | 3 | 3 | 1 | 0 | 0 |
| **Y** | 6 | 6 | 6 | 5 | 6 | 4 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **N** | 5 | 5 | 5 | 6 | 5 | 4 | 4 | 3 | 3 | 2 | 1 | 0 | 0 |
| **R** | 4 | 4 | 4 | 4 | 4 | 5 | 4 | 3 | 3 | 2 | 2 | 0 | 0 |
| **C** | 3 | 3 | 4 | 3 | 3 | 3 | 3 | 4 | 3 | 3 | 1 | 0 | 0 |
| **K** | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 3 | 2 | 1 | 0 | 0 |
| **C** | 2 | 2 | 3 | 2 | 2 | 2 | 2 | 3 | 2 | 3 | 1 | 0 | 0 |
| **R** | 2 | 1 | 1 | 1 | 1 | 2 | 1 | 1 | 1 | 1 | 2 | 0 | 0 |
| **B** | 1 | 2 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 1 | 0 | 0 |
| **P** | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 1 | 0 |

- Le slide 45 e 46 mostrano i passi intermedi: prima le ultime righe (B, P), poi il blocco da R in giù
- La soluzione **non è unica** (slide 49): due percorsi con lo stesso punteggio massimo,
  - `ABCNY-RQCLCR-PM` / `AYC-YNR-CKCRBP-`
  - `ABC-NYRQCLCR-PM` / `AYCYN-R-CKCRBP-`
  - (verificato: entrambi hanno 8 match e 5 gap; il punteggio 8 conta solo i match perché questa versione non penalizza i gap)
- **NB** (slide 50): non sono ammessi spostamenti diretti **verso destra o verso il basso**, solo passi in diagonale (eventualmente saltando righe o colonne, il che corrisponde ai gap). Figura: la matrice originale dell'articolo del 1970, con le frecce del percorso; vi compaiono J e O al posto di Y e Q
- (Aggiunta, non nelle slide: oggi Needleman-Wunsch si presenta con la ricorrenza della slide 51, riempiendo la matrice dall'alto a sinistra con una penalità di gap; è quella implementata nelle librerie.)

### Hirschberg
- Definisce l'allineamento globale in termini di programmazione dinamica, partendo da due osservazioni:
  - in Needleman-Wunsch, per calcolare la matrice basta tenere in memoria la **riga corrente** e quella **precedente**
  - se $NW(A, B)$ è un allineamento ottimo e $A = A^l + A^r$ una partizione **arbitraria** di $A$, esiste una partizione $B = B^l + B^r$ tale che $NW(A, B) = NW(A^l, B^l) + NW(A^r, B^r)$
- Matrice $F_{i,j}$:
  $$F_{0,j} = d \cdot j \qquad F_{i,0} = d \cdot i$$
  $$F_{i,j} = \max(F_{i-1,j-1} + S(a_i, b_j),\ F_{i,j-1} + d,\ F_{i-1,j} + d)$$
  con $d$ il costo di un gap. (La slide scrive $S(A, B)$ nella ricorrenza: va letto $S(a_i, b_j)$, il punteggio dei due caratteri. Poiché si prende il **massimo** e si **somma** $d$, il costo del gap è un numero **negativo**. Le dimensioni sono $(n+1) \times (m+1)$, non "al più $n \times m$".)
- (Aggiunta, non nelle slide: il punto di Hirschberg è lo **spazio lineare**. Con due sole righe si ottiene il punteggio ma non l'allineamento; Hirschberg divide $A$ a metà, trova il taglio ottimo di $B$ calcolando l'ultima riga in avanti per $A^l$ e all'indietro per $A^r$, e ricorre sulle due metà: tempo $O(nm)$, spazio $O(\min(n, m))$. Verificato sull'esempio classico `AGTACGCA` / `TATGC` con match $+2$, mismatch $-1$, gap $d = -2$: la ricorrenza dà 1, come `PairwiseAligner` di Biopython, e spezzando $A$ in `AGTA` + `CGCA` il miglior taglio di $B$ dà di nuovo 1.)
- Figure (slide 52-53): **struttura delle proteine** (primaria = sequenza di aminoacidi, secondaria = $\alpha$-eliche e foglietti $\beta$, terziaria = ripiegamento 3D, quaternaria = più catene) e **domini proteici** (sei strutture, es. PRYSPRY domain, RNA recognition motif, zinc finger): motivano l'allineamento locale, perché proteine diverse possono condividere solo **un dominio**

## Allineamento locale
- Considera anche l'**estensione della regione simile**: a parità di aminoacidi uguali, il punteggio è tanto più alto quanto più la regione è **concentrata**; si favoriscono le **similarità locali** in regioni circoscritte
- Algoritmo di **Smith e Waterman (1981)**
- Figura (slide 54): con blocchi A B C contro A C l'allineamento locale abbina i singoli blocchi; con A B contro B A abbina A con A e B con B separatamente, cosa che il globale non può fare

### Smith-Waterman
- **Obiettivo**: date $S_A = a_1, \dots, a_n$ e $S_B = b_1, \dots, b_m$, trovare la **sottosequenza** della prima con il maggior grado di similarità con una sottosequenza della seconda
- **Inizializzazione**: la slide dice "matrice $H_{i,j}$ con $n-1$ righe ed $m+1$ colonne", inizializzata con "$H_{i,0} = H_{0,j}$". **Errore nella slide 55**: le righe sono $n + 1$, e l'inizializzazione è $H_{i,0} = H_{0,j} = 0$ per $0 \le i \le n$, $0 \le j \le m$ (manca lo zero, che si vede nella figura: prima riga e prima colonna a 0)
- **Punteggi** per sequenze nucleotidiche: $s(a_i, b_j) = \alpha$ se $a_i = b_j$ (di solito $> 0$), $\beta$ se diversi (di solito $\le 0$); gap di lunghezza $k$: $W_k = \gamma + \delta(k-1)$, con $\gamma$ costo fisso di apertura e $\delta$ penalità per ogni estensione
- **Ricorrenza**:
  $$H_{i,j} = \max(H_{i-1,j-1} + s(a_i, b_j),\ H_{i-1,j} - W_k,\ H_{i,j-1} - W_k,\ 0)$$
  - diagonale: allungamento con **match o mismatch**
  - $H_{i-1,j} - W_k$: allungamento con un gap su $S_A$; $H_{i,j-1} - W_k$: con un gap su $S_B$ (così la slide; in $H_{i-1,j}$ è $a_i$ ad essere allineato a un gap, quindi il trattino compare nella riga di $S_B$, e viceversa: anche qui è una questione di convenzione)
  - **0**: non c'è più similarità, l'allineamento locale **ricomincia** da lì. È l'unica differenza di ricorrenza rispetto al globale, insieme all'inizializzazione a 0
- (Precisazione sulla formula: scritta così, con $H_{i-1,j}$ e $W_k$, $k$ non è definito. La figura accanto mostra la forma corretta, che prova tutte le lunghezze di gap: $\max_{k \ge 1}(H_{i-k,j} - W_k)$ e $\max_{l \ge 1}(H_{i,j-l} - W_l)$. Con penalità lineare basta $H_{i-1,j} - W_1$.)
- **Backtracking**: si parte dalla cella di **score massimo** e si risale fino a uno **0**, che segna l'inizio dell'allineamento locale. La slide dice di risalire "seguendo la cella di score massimo tra $H_{i-1,j-1}$, $H_{i-1,j}$, $H_{i,j-1}$". (Precisazione: va seguita la cella **da cui il valore è stato calcolato**, non il vicino più grande. L'esempio della slide stessa lo mostra, vedi sotto.)

Esempio (slide 58), verificato: Sequence A $=$ `CAGCCUCGCUUAG` sulle colonne, Sequence B $=$ `AAUGCCAUUGACGG` sulle righe, con match $+1$, mismatch $-1/3$, $W_k = 1 + k/3$ (cioè $\gamma = 4/3$, $\delta = 1/3$; i parametri non sono scritti nella slide, li ho ricavati facendo tornare la matrice). Massimo **3,3** nella cella (G di B, G di A), allineamento
```
GCCAUUG
||| | |
GCC-UCG
```
- Ricalcolando la matrice tornano tutti i valori della figura tranne uno: nella riga della prima U di B, colonna G di A, la slide ha 0,8, il valore corretto è $1 - 1/3 \approx 0{,}7$
- Il percorso giusto da 3,3 risale 2,3 → 2,7 (U, U) → **1,7** (A di B allineata al gap) → 3,0 → 2,0 → 1,0. Da 2,7 la regola "vicino massimo" sceglierebbe invece il 2,7 sopra (A, U) al posto di 1,7, e ne uscirebbe un allineamento che non dà 3,3. La figura sottolinea proprio 1,7, ma una freccia passa per il 2,7: conferma che il backtracking va fatto con i puntatori
- Stesso risultato con Biopython: `PairwiseAligner(mode="local", match_score=1, mismatch_score=-1/3, open_gap_score=-4/3, extend_gap_score=-1/3)` dà score 3,33 e lo stesso allineamento

Figura (slide 59): su due sequenze di DNA il percorso dell'allineamento **globale** attraversa tutta la matrice da un angolo all'altro; quello **locale** trova più segmenti diagonali separati (blocchi A, B, C, D di una sequenza abbinati a B, D, A, C dell'altra, cioè riarrangiati).

Figura (slide 60), tassonomia dell'**allineamento di sequenze**:
- **pairwise**: algoritmi **esatti** (programmazione dinamica, globale e locale; dot plot) ed **euristici** (k-tuple, cioè BLAST e simili)
- **multiplo**: algoritmi **esatti** (programmazione dinamica, globale e locale) ed **euristici** (metodi **progressivi** e **iterativi**)

## BLAST
- **Basic Local Alignment Search Tool**: algoritmo **euristico** per l'allineamento locale, o per trovare in una collezione di sequenze target quella **più simile** a una query
- Idea: limitare l'attenzione a coppie di segmenti in cui si allineano **parole di lunghezza $w$** con punteggio **almeno $T$**
- Figura (slide 61): un **seed** (parola che combacia) sulla sequenza del database, poi **extend** in avanti
- Fasi:
  - **0**: si estraggono dalle sequenze del database tutte le parole di lunghezza $w$ e se ne memorizza la **posizione**
  - **1**: lista di coppie di parole (di lunghezza $w = 3$) con punteggio oltre la soglia $T$
  - **2**: scansione del database per le voci che corrispondono alla lista
  - **3**: trovata una corrispondenza (un **seed**), si **estende** l'allineamento nelle due direzioni; poi lo si **raffina** con Smith-Waterman
- (Aggiunta, non nelle slide: $w = 3$ è il default per le proteine, per il DNA si usa $w = 11$. Precisazione sul raffinamento: il BLAST con gap non lancia uno Smith-Waterman completo, ma una programmazione dinamica **limitata attorno al seed** che si ferma quando lo score scende troppo sotto il massimo raggiunto (X-drop); per questo è veloce e non garantisce l'ottimo.)

### Significatività: E-value, bit score, p-value
- Gli score seguono una **distribuzione del valore estremo** (EVD, Gumbel), non una normale; parametro principale la **costante di decadimento** $\lambda$
- **Valore atteso $E$**: numero di allineamenti (HSP, *high scoring segment pairs*) con punteggio $\ge S$ che ci si aspetta **per caso** in quella ricerca; un indice di **incertezza**
  $$E = K M N e^{-\lambda S}$$
  con $M$ lunghezza della query, $N$ lunghezza della sequenza target, $S$ score, $\lambda$ dipendente dallo **scoring system**, $K$ "dipendente dal database usato"
- $E$ **decresce esponenzialmente** con $S$: allineamenti migliori hanno $E$ più bassi
- $E = 1$: ci si aspetta **un** allineamento con lo stesso score per puro caso
- La stessa ricerca su un database più piccolo o più grande deve dare un $E$ diverso anche per lo stesso allineamento, "e ciò dipende da $K$". **Errore nelle slide 63-64**: la dimensione del database entra in $E$ attraverso **$N$**, che in una ricerca è la lunghezza **totale** del database (somma delle sequenze), non di una sola sequenza target. $K$ e $\lambda$ sono costanti di Karlin-Altschul che dipendono dalla **matrice di punteggio** e dalla composizione delle sequenze, non dalla dimensione del database
- **Bit score**, normalizzato e quindi confrontabile fra ricerche con matrici o database diversi:
  $$S' = \frac{\lambda S - \ln K}{\ln 2}$$
  (Aggiunta, ricavata dalla formula: sostituendo, $E = M N \, 2^{-S'}$, cioè ogni bit in più dimezza $E$.)
- **p-value**, modo equivalente di esprimere la significatività:
  $$p = 1 - e^{-E}$$
  Per $E$ molto piccoli $E$ e $p$ quasi coincidono; fra 1 e 10 $E$ è più leggibile perché conta un **numero di hit**, mentre $p$ è già vicino a 1. (Calcolato: $E = 0{,}01 \to p = 0{,}00995$; $E = 0{,}1 \to 0{,}095$; $E = 1 \to 0{,}632$; $E = 3 \to 0{,}950$; $E = 10 \to 0{,}99995$.)

## Allineamento multiplo
- Scopo: dati dei **cluster** di stringhe, trovare una **stringa consenso**, allineando tutte le stringhe in un unico allineamento
- Figura (slide 66): un allineamento multiplo di una famiglia di proteine (RLA0 di molte specie: umano, topo, ratto, pollo...), colorato per tipo di aminoacido, con le colonne **conservate** che risaltano

### Ottimale (programmazione dinamica)
- Per tre sequenze la matrice diventa un **cubo**: sulle facce ci sono le matrici a coppie A-B, B-C, A-C, e l'allineamento ottimo richiede di riempire tutto il cubo valutando tutte le mosse interne
- Complessità $O(L^N)$, con $L$ lunghezza e $N$ numero di sequenze; la DP completa è usabile in pratica **solo fino a tre sequenze**. (Precisazione: $O(L^N)$ è lo **spazio**; il tempo è $O(2^N L^N)$, perché ogni cella ha $2^N - 1$ predecessori.)
- In generale, con $X = \{x_1, \dots, x_k\}$ e $\alpha(i_1, \dots, i_k)$ massimo punteggio di un allineamento dei prefissi $x_1[1 \dots i_1], \dots, x_k[1 \dots i_k]$:
  $$\alpha(i_1, \dots, i_k) = \max \begin{cases} \alpha(i_1 - 1, i_2 - 1, \dots, i_k - 1) + S(m_{1 i_1}, m_{2 i_2}, \dots, m_{k i_k}) \\ \alpha(i_1, i_2 - 1, \dots, i_k - 1) + S(-, m_{2 i_2}, \dots, m_{k i_k}) \\ \alpha(i_1 - 1, i_2, \dots, i_k - 1) + S(m_{1 i_1}, -, \dots, m_{k i_k}) \\ \vdots \\ \alpha(i_1, i_2 - 1, \dots, i_{k-1} - 1, i_k) + S(-, m_{2 i_2}, \dots, -) \\ \vdots \end{cases}$$
  dove ogni riga sceglie quali sequenze avanzano di un carattere e quali mettono un gap ($-$); $m_{j i_j}$ è il carattere $x_j[i_j]$ (la slide cambia nome alle sequenze da $x$ a $m$ senza dirlo)

### Progressivo (euristico)
- Figura (slide 69), tre sequenze per passi successivi:
  1. si allinea la coppia **A-B**: `DGEKFGPPQRSGQRSG` con `DGERFGP-QRSGNRSG`
  2. il **consenso** di A-B si allinea con **C**, `DHEKFGSSQRSGQRSG`
  3. si ottiene l'allineamento multiplo delle tre
- Procedura:
  1. $N$ sequenze non allineate
  2. si allineano **tutte le coppie**: $N(N-1)/2$ allineamenti
  3. si costruisce un **albero guida** dai punteggi di similarità delle coppie, con **Neighbor-joining** o **UPGMA** (*Unweighted Pair Group Method with Arithmetic mean*)
  4. dalla coppia **più simile** si fissano le **colonne conservate** e si allinea la coppia successiva mantenendole e ricalcolando lo score
  5. in output, $N$ sequenze allineate
- Figura (slide 71), **schema di Clustal**: (1) allineamento a coppie di A-F, $N(N-1)/2$; (2) **matrice delle distanze** $D_{AB}, D_{AC}, \dots$; (3) **albero guida**; (4-5) allineamento progressivo seguendo l'albero: A con B, C con D, poi le due coppie insieme, poi E con F, infine tutto
- (Aggiunta: il limite dei metodi progressivi è "once a gap, always a gap": un errore nei primi allineamenti non si corregge più. I metodi **iterativi** della tassonomia ri-allineano per migliorare.)

### Feng-Doolittle
- È la metodologia **alla base di Clustal**. Problema: gli algoritmi per costruire l'albero vogliono una **matrice delle distanze**, quelli di allineamento danno **score di similarità**: serve convertire
- Con $S(a, b)$ similarità, $S^{max}_{a,b}$ massima similarità possibile, $S_{rand}$ score atteso per due sequenze **casuali** della stessa lunghezza (e composizione):
  $$S^{eff}_{a,b} = \frac{S(a, b) - S_{rand}}{S^{max}_{a,b} - S_{rand}}$$
  - secondo la slide è **sempre fra 0 e 1** e **tende lentamente a zero** per sequenze evolutivamente sempre più lontane
  - (Precisazione su "sempre": se due sequenze allineano peggio di due casuali, $S(a, b) < S_{rand}$ e $S^{eff}$ è **negativo**, con il logaritmo non definito; nella pratica si tronca. Vale 1 quando $S(a, b) = S^{max}_{a,b}$, cioè sequenze identiche.)
- **Distanza**: $D(a, b) = -\log S^{eff}_{a,b}$, 0 per sequenze identiche e crescente al diminuire della similarità

## Aggiunta: codice di riferimento
Non nelle slide, solo come riferimento per il progetto e la parte pratica dell'orale. Verificato con numpy 2.5 e Biopython 1.88: le tre versioni di Fibonacci danno $F(40) = 165.580.141$, il DTW sull'esempio della slide 7 dà 2, quello con finestra sull'esempio di lunghezze 10 e 7 dà 0, il globale dà 1 e il locale 3,33 con l'allineamento `GCCAUUG` / `GCC-UCG`.

```python
import numpy as np
from functools import lru_cache
from Bio import Align

@lru_cache(maxsize=None)
def Fib(n):
    return 1 if n <= 1 else Fib(n-1) + Fib(n-2)

def dtw(s, t, w=None):
    n, m = len(s), len(t)
    if w is not None:
        w = max(w, abs(n - m))
    D = np.full((n + 1, m + 1), np.inf)
    D[0, 0] = 0
    for i in range(1, n + 1):
        lo, hi = (1, m) if w is None else (max(1, i - w), min(m, i + w))
        for j in range(lo, hi + 1):
            cost = (s[i-1] - t[j-1]) ** 2
            D[i, j] = cost + min(D[i-1, j], D[i, j-1], D[i-1, j-1])
    return D

glob = Align.PairwiseAligner(mode="global", match_score=2, mismatch_score=-1, gap_score=-2)
glob.score("AGTACGCA", "TATGC")

loc = Align.PairwiseAligner(mode="local", match_score=1, mismatch_score=-1/3,
                            open_gap_score=-4/3, extend_gap_score=-1/3)
print(loc.align("AAUGCCAUUGACGG", "CAGCCUCGCUUAG")[0])
```
- `lru_cache` fa la memoization di `MemoFib` senza gestire la tabella a mano; per $n$ grandi la ricorsione supera comunque il limite di Python (1000 di default), quindi meglio la versione bottom-up
- `dtw` restituisce l'intera matrice: la distanza è `D[-1, -1]`, il warping path si ricava risalendo da lì verso il predecessore minimo
- in `PairwiseAligner` un gap di lunghezza $k$ costa `open_gap_score + (k-1) * extend_gap_score`: con $-4/3$ e $-1/3$ è $W_k = 1 + k/3$ dell'esempio della slide 58
- le matrici di sostituzione si caricano con `Align.substitution_matrices.load("BLOSUM62")` (o `"PAM250"`, `"BLOSUM45"`) e si passano con `aligner.substitution_matrix = ...`
