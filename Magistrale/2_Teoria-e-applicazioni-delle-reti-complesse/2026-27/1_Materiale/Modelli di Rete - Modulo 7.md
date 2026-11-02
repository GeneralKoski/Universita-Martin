# Modelli di rete (Modulo 7)

Fonte: `Modelli di Rete - Modulo 7.pdf` (67 pagine). Su Elly non esiste un Modulo 6: dopo le Proprietà globali (Modulo 5) si passa direttamente a questo

## Perché i modelli di rete
- Le reti reali hanno strutture molto complesse. Per capirne le proprietà si costruiscono **modelli matematici** che generano reti secondo **regole semplici**
- Un modello di rete permette di:
  - capire come semplici regole di formazione dei link producano **proprietà globali**
  - studiare la relazione tra **struttura** e **comportamento** della rete
  - **confrontare** le proprietà delle reti reali con quelle attese da un modello teorico
- Figura: lo stesso insieme di nodi con $p = 0{,}1$, $0{,}25$, $0{,}5$, sempre più fitto
- Le domande che un modello deve saper prevedere sono quelle dei moduli precedenti: qual è la **componente gigante**? qual è il **grado medio**? quanto distano i nodi? qual è l'**efficienza**? ci sono **comunità**? ci sono **hub**? la rete è robusta all'**errore** e all'**attacco**?

## Il grafo casuale di Erdős-Rényi

### Domanda fondamentale e due modelli
- **Quali proprietà emergono se i collegamenti tra i nodi vengono generati completamente a caso?**
- Paul Erdős e Alfréd Rényi pubblicarono due modelli diversi:
  - $G(n, m)$: fissa il **numero esatto di archi** $m$, scelti a caso tra tutti quelli possibili
  - $G(n, p)$, il più usato oggi: ogni arco esiste **con probabilità $p$, indipendentemente** dagli altri
  - (Precisazione storica, non nelle slide: l'articolo di Erdős e Rényi del 1959 usa $G(n, m)$; il modello $G(n, p)$ fu introdotto nello stesso anno da Edgar Gilbert, e oggi porta il nome di Erdős-Rényi perché ne hanno sviluppato la teoria. Per $n$ grande i due modelli si comportano allo stesso modo con $m = p\,n(n-1)/2$)
- Tre fatti che le slide mettono in evidenza:
  1. la **transizione di fase** (la comparsa della componente gigante) fu una scoperta accidentale
  2. il **clustering è bassissimo**
  3. è ancora il **modello nullo di riferimento**: si confronta una rete reale con un ER con lo stesso $n$ e lo stesso grado medio

### Numero di Erdős
- Erdős co-firmò oltre 1500 articoli con circa 500 collaboratori diversi
- **Rete di co-autori matematici**: nodi = ricercatori, archi = almeno un articolo pubblicato insieme
- Il **numero di Erdős** di un ricercatore è la **distanza binaria** dal suo nodo al nodo "Paul Erdős":

$$E(v) = d(v, \text{Erdős})$$

  - Erdős ha numero 0; chi ha pubblicato con lui ha numero 1; chi ha pubblicato con qualcuno di numero 1, ma non con Erdős, ha numero 2, e così via
- La rete di co-autori è un tipico esempio di **small-world**:
  - **distanza media** $\langle d \rangle \approx 4-5$
  - **clustering alto**: i collaboratori di un matematico tendono a conoscersi
  - **distribuzione dei gradi con coda pesante**: pochi ricercatori molto prolifici, molti con pochi collaboratori
  - (Precisazione, non nelle slide: 4-5 è il **numero di Erdős medio** dei matematici collegati a lui, circa 4,65 con mediana 5 secondo l'Erdős Number Project. La distanza media fra **tutte** le coppie della rete di co-autori matematici è più alta: Newman, *The structure and function of complex networks* (SIAM Review 2003), riporta circa 7,6 su 253.339 nodi, la stessa rete con $r = 0{,}120$ della tabella sull'assortatività del Modulo 5)
- Figura (Easley e Kleinberg, 2010): **rete ego-centrata** (*ego network*) di Erdős, con i co-autori attorno a lui; Gauss compare in alto a sinistra
- Demo interattiva: Wolfram Demonstrations, *Collaboration Graph for Paul Erdos Coauthors* (layout a molla, i co-autori di Erdős formano grandi stelle)

### Il modello $G(n, p)$
- Si considerano $n$ nodi; **ogni coppia di nodi viene collegata con probabilità $p$, indipendentemente dalle altre coppie**
- Due parametri: $n$ = numero di nodi, $p$ = probabilità che esista un arco tra due nodi distinti; per grafi semplici e non orientati $0 \leq p \leq 1$
- Casi limite:
  - $p = 0$: nessun arco, tutti i nodi isolati
  - $p = 1$: grafo completo, tutte le coppie collegate
  - $0 < p < 1$: rete casuale, con un numero di archi **variabile** da una realizzazione all'altra
- Figura con $n = 8$:

| | $p = 0$ | $p = 0{,}3$ | $p = 1$ |
|---|---|---|---|
| archi $m$ | 0 | circa 8-9 | 28 |
| $\langle k \rangle$ | 0 | circa 2,1 | 7 |
| $C$ | 0 | circa 0,3 | 1 |

  (I valori per $p = 0{,}3$ sono quelli attesi: $0{,}3 \cdot 28 = 8{,}4$ archi, $7 \cdot 0{,}3 = 2{,}1$, $C \approx p$, come si vedrà sotto)

### Numero di archi
- Numero **massimo** di archi in un grafo semplice non orientato:

$$M = \frac{n(n-1)}{2}$$

  ogni nodo può collegarsi agli altri $n - 1$; il prodotto $n(n-1)$ conta ogni arco due volte, quindi si divide per 2
- Poiché ogni arco esiste con probabilità $p$, il numero **medio** di archi è:

$$\langle m \rangle = p\,\frac{n(n-1)}{2}$$

- Esempio, $n = 100$ e $p = 0{,}1$: $\langle m \rangle = 0{,}1 \cdot \frac{100 \cdot 99}{2} = 495$
- È il numero **atteso**, non necessariamente quello effettivo di una singola realizzazione (aggiunta: il numero di archi è una binomiale con media 495 e deviazione standard $\sqrt{4950 \cdot 0{,}1 \cdot 0{,}9} \approx 21$; su 1000 realizzazioni in NetworkX la media è 493,8)

### Grado medio
- Ogni nodo può collegarsi agli altri $n - 1$, ciascuno con probabilità $p$:

$$\langle k \rangle = (n-1)\,p \approx np \quad \text{per reti grandi}$$

- Esempio, $n = 100$ e $p = 0{,}1$: $\langle k \rangle = 99 \cdot 0{,}1 = 9{,}9$, il **grado medio teorico atteso**
- Figura: istogramma del grado medio su 1000 realizzazioni di ER ($n = 100$, $p = 0{,}1$), a campana fra circa 8,6 e 11,5; media simulata 9,89, valore atteso 9,9

### Distribuzione dei gradi: binomiale
- Il grado $k$ di un nodo è una **variabile casuale binomiale**: $n - 1$ possibili vicini, ciascuno presente con probabilità $p$, indipendentemente

$$P(k) = \binom{n-1}{k} p^k (1-p)^{n-1-k}$$

  - $P(k)$: probabilità che un nodo abbia **esattamente** grado $k$
  - $\binom{n-1}{k}$: numero di modi di scegliere i $k$ vicini tra gli $n - 1$ possibili
  - $p^k$: probabilità che quei $k$ collegamenti siano presenti
  - $(1-p)^{n-1-k}$: probabilità che gli altri $n - 1 - k$ siano assenti
- **Coefficiente binomiale**:

$$\binom{n-1}{k} = \frac{(n-1)!}{k!\,(n-1-k)!}, \qquad \text{es. } 4! = 4 \cdot 3 \cdot 2 \cdot 1 = 24$$

### Dalla binomiale alla Poisson
- Per reti **grandi e sparse** ($n \to \infty$, $p \to 0$, con $\langle k \rangle$ costante) la binomiale converge alla **distribuzione di Poisson**:

$$P(k) = \frac{e^{-\lambda} \lambda^k}{k!}, \qquad \lambda = \langle k \rangle = (n-1)\,p$$

- Nel limite di Poisson **media e varianza coincidono**: $\langle k \rangle = \sigma_k^2 = \lambda$; se il grado medio è 4 anche la varianza è 4. (Nella slide è scritto $\sigma_2^k$, con indice ed esponente scambiati: è $\sigma_k^2$. Aggiunta: per la binomiale esatta la varianza è $(n-1)p(1-p)$, appena sotto la media; con $n = 1000$, $p = 0{,}004$ vale 3,98)
- **Siméon Denis Poisson** (1781-1840): nel 1837 pubblicò *Recherches sur la probabilité des jugements en matière criminelle et en matière civile*, sulla probabilità applicata alle decisioni giudiziarie, dove compare la distribuzione. Emerge come limite della binomiale quando il numero di prove è molto grande e la probabilità di successo molto piccola, a numero medio di successi costante
- **I soldati prussiani** (Ladislaus Bortkiewicz, 1898): numero di soldati uccisi ogni anno da calci di cavallo; 200 osservazioni (10 corpi d'armata per 20 anni), 122 decessi, media 0,61 per osservazione. I dati seguono bene una Poisson con $\lambda = 0{,}61$
- Figura: Poisson teoriche per $\lambda = 1, 4, 10$: con $\lambda = 1$ il massimo è in 0-1 (circa 0,37), con $\lambda = 4$ in 3-4 (circa 0,2), con $\lambda = 10$ la curva è più bassa e larga (circa 0,125 attorno a 10)

### Verifiche numeriche (figure)
- ER $n = 1000$, $p = 0{,}004$ ($\langle k \rangle$ simulato 3,90): la distribuzione simulata coincide quasi punto per punto con la Poisson con $\lambda = 4{,}00$, massimo circa 0,2 in $k = 3$ e $k = 4$
- Confronto con la Poisson al crescere dei nodi, unendo più reti (la distanza $L_1$ è la somma degli scarti assoluti fra le due distribuzioni):

| Reti unite | Nodi totali | $\lambda$ | Distanza $L_1$ |
|---|---|---|---|
| 1 | 50 | 3,92 | 0,2299 |
| 5 | 250 | 3,92 | 0,2153 |
| 20 | 1.000 | 3,92 | 0,0757 |
| 100 | 5.000 | 3,92 | 0,0404 |
| 1 | 1.000 | 4,0 | 0,0676 |
| 5 | 5.000 | 4,0 | 0,0311 |
| 20 | 20.000 | 4,0 | 0,0095 |
| 100 | 100.000 | 4,0 | 0,0106 |

- Più nodi si raccolgono, più l'istogramma si avvicina alla Poisson: con 50 nodi lo scarto è grande (barra a $k = 3$ circa 0,26 contro 0,2 attesi), da qualche migliaia di nodi l'accordo è quasi perfetto. L'ultima riga (0,0106 contro 0,0095) mostra che a quel livello resta solo rumore statistico. Le slide 26 e 27 sono identiche

## Componente gigante

### LCC e componente gigante
- Componente connessa (grafo non orientato): insieme **massimale** di nodi in cui ogni coppia è collegata da almeno un cammino. **LCC** (*Largest Connected Component*): la componente con il maggior numero di nodi

$$S = \frac{N_{LCC}}{n}$$

  frazione di nodi nella componente più grande
- **Nota**: in una rete finita esiste **sempre** una componente più grande, ma non necessariamente una componente **gigante** in senso matematico. Una componente è **gigante** quando contiene una **frazione non nulla** dei nodi nel limite $n \to \infty$

### La transizione di fase
- Si tiene fisso $n$ e si aumenta progressivamente $p$: un **cambiamento quantitativo** produce un **cambiamento qualitativo**
- Figura: tre reti con grado medio 0,99, 1,18 e 3,96 (prima solo pezzetti, poi un ammasso che cresce, poi quasi tutti i nodi collegati) e la curva della taglia della componente gigante in funzione del grado medio, piatta a zero e poi in rapida salita
- **Risultato fondamentale** (proprietà fondamentale del modello ER):

$$\langle k \rangle_c = 1 \quad \Longrightarrow \quad p_c \approx \frac{1}{n} \quad (\text{da } \langle k \rangle = (n-1)p)$$

- **Perché proprio a grado medio 1? Processo di ramificazione**: si esplora la rete partendo da un nodo e si contano i nuovi nodi raggiunti
  - $\langle k \rangle < 1$, **regime sottocritico**: ogni nodo raggiunto genera mediamente meno di un nuovo nodo; l'esplorazione tende a estinguersi e le componenti restano piccole
  - $\langle k \rangle = 1$, **regime critico**: ogni nodo genera mediamente un nuovo nodo; confine tra estinzione e crescita sostenuta
  - $\langle k \rangle > 1$, **regime supercritico**: ogni nodo genera mediamente più di un nuovo nodo; l'esplorazione può continuare e raggiungere una frazione macroscopica della rete
- (Aggiunta, non nelle slide: nel limite $n \to \infty$ la taglia della componente gigante soddisfa $S = 1 - e^{-\langle k \rangle S}$, che ha soluzione positiva solo per $\langle k \rangle > 1$. Verificato con NetworkX su ER con $n = 10.000$:

| $\langle k \rangle$ | 0,5 | 1,5 | 2 | 2,5 | 4 |
|---|---|---|---|---|---|
| $S$ teorica | 0 | 0,583 | 0,797 | 0,893 | 0,980 |
| $S$ simulata | 0,002 | 0,577 | 0,796 | 0,893 | 0,980 |

  )
- Simulazione delle slide, ER con $N = 10.000$ ($p_c \approx 1/10.000 = 0{,}0001$):
  - su $p \in [0; 0{,}01]$: LCC/N sale quasi verticalmente subito dopo $p = 1/N$ e arriva a 1 già intorno a $p \approx 0{,}001$
  - zoom su $p \in [0{,}00005; 0{,}00025]$ ("Transizione di fase"): LCC/N è circa 0 fino a $p = 0{,}0001$, poi cresce (valori letti dal grafico, approssimati: circa 0,2 a $p \approx 0{,}00012$, circa 0,6 a $0{,}00016$, circa 0,9 a $0{,}00025$)
  - per $N \to \infty$, **sotto la soglia la frazione di nodi nella componente maggiore tende a zero**
- Animazione EPFL (corso NooC, canale YouTube @EPFLNooC): fotogramma di un $G(n;\, 0{,}002)$ con molti nodi quasi tutti isolati (il valore di $n$ nell'etichetta non è leggibile)

## Connettività completa
- **Quando diventa connessa tutta la rete?** Per **connettività completa** (*full connectivity*) si intende che tutti i nodi appartengono a un'**unica componente connessa** (figura: una rete con 5 nodi su 6 nella componente maggiore e uno isolato, contro una rete connessa di 6 nodi)

$$\langle k \rangle_c \sim \ln N \quad \Longrightarrow \quad p_c = \frac{\ln N}{N}$$

  (La slide scrive $\log(N)$, ma intende il logaritmo naturale, come mostra l'esempio. Inoltre usa ancora il simbolo $p_c$, già usato per la soglia della componente gigante: sono due soglie diverse, $1/N$ e $\ln N / N$)
- Esempio, $N = 1000$: $\ln 1000 \approx 6{,}91$, quindi $p_c = \ln 1000 / 1000 \approx 0{,}00691$
- **Attenzione: non significa che a $p = p_c$ la rete diventi certamente connessa.** La rete diventa connessa con **probabilità crescente** quando $p$ attraversa la regione critica $\ln N / N$, **molto dopo** la comparsa della componente gigante, che avviene attorno a $p = 1/N$
- Figura "Connettività completa vs $p$" (ER, $N = 1000$, 50 repliche): $P(\text{rete connessa})$ è 0 fino a $p \approx 0{,}0055$, vale circa 0,4 sulla linea $p = 0{,}00691$, supera 0,9 verso $p \approx 0{,}009$ e arriva a 1 oltre circa $0{,}0115$ (valori approssimati)
- (Aggiunta: con $p = (\ln N + c)/N$ la probabilità di essere connessa tende a $e^{-e^{-c}}$, quindi esattamente sulla soglia ($c = 0$) vale $e^{-1} \approx 0{,}37$, in linea con il grafico; su 200 realizzazioni con NetworkX esce 0,36. L'ultimo ostacolo alla connessione sono i nodi isolati)

## Distanza media
- In una rete connessa la distanza media è la media dei cammini minimi fra tutte le coppie di nodi distinti (Modulo 5):

$$\bar d = \frac{1}{n(n-1)} \sum_{i \neq j} d_{ij}$$

  per reti disconnesse si calcola sulla LCC
- **Come cambia quando aumentano i nodi o la probabilità di collegamento?**

$$\bar d \sim \frac{\ln n}{\ln \langle k \rangle}$$

- **Conseguenza**: a grado medio costante la distanza media cresce come $\ln n$, **non proporzionalmente a $n$**. È il comportamento alla base della proprietà **small-world**. (Nelle slide 39 e 40 la stima è scritta con "=", ma resta un'approssimazione: le simulazioni stanno leggermente sopra)
- (Aggiunta, l'intuizione: un nodo ha circa $\langle k \rangle$ vicini, $\langle k \rangle^2$ nodi a distanza 2, $\langle k \rangle^d$ a distanza $d$; si raggiungono tutti gli $n$ nodi quando $\langle k \rangle^d \approx n$, cioè $d \approx \ln n / \ln \langle k \rangle$)
- Esempio, $\langle k \rangle = 4$, $\bar d = \ln n / \ln 4$:

| $n$ | 100 | 1.000 | 10.000 | 100.000 | 1.000.000 |
|---|---|---|---|---|---|
| $\bar d$ stimata | 3,32 | 4,98 | 6,64 | 8,30 | 9,97 |

  ogni fattore 10 sui nodi aggiunge solo circa 1,66 alla distanza (figura: retta su asse $n$ logaritmico, da circa 3 a circa 10)
- Figure delle simulazioni (valori letti dai grafici, approssimati):
  - **$N = 1000$, grado medio atteso da 1,5 a 15**: la distanza media sulla LCC scende da circa 12,7 a circa 2,8; **diminuisce all'aumentare del grado medio**
  - **$n$ da 100 a 5000, $\langle k \rangle = 4$**: la simulazione (LCC) passa da circa 3,4 a circa 6,2, appena sopra la curva teorica $\ln n / \ln \langle k \rangle$; **aumentando i nodi la distanza media cresce solo logaritmicamente**. Su asse $n$ logaritmico i punti stanno su una retta
  - Stessa figura con una **crescita lineare di riferimento** (verde), "analoga a quella osservata in una rete a catena", che a $n = 5000$ arriva a circa 170, mentre ER e teoria restano schiacciati verso 6. (Precisazione: la retta verde indica solo l'andamento lineare, non il valore di una catena: in una catena di $n$ nodi $\bar d = (n+1)/3$, cioè circa 1667 per $n = 5000$, dieci volte più in alto)
- (Verifica con NetworkX, $\langle k \rangle = 4$, distanza sulla LCC: $n = 100$ → 3,51 (stima 3,32); $n = 1000$ → 5,06 (4,98); $n = 5000$ → 6,25 (6,14))

## Clustering
- In ER ogni coppia è collegata indipendentemente con probabilità $p$. Dato un nodo $i$ e due suoi vicini $j$ e $h$, la probabilità che esista anche l'arco $j - h$ è semplicemente $p$
- **Il clustering locale atteso di un nodo con almeno due vicini è uguale alla probabilità di collegamento $p$**:

$$\mathbb{E}[C_i \mid k_i \geq 2] = p$$

- Esempio, $p = 0{,}2$ e nodo con 4 vicini: le coppie di vicini sono $\frac{4 \cdot 3}{2} = 6$, quindi

$$\mathbb{E}[T_i \mid k_i = 4] = 6 \cdot 0{,}2 = 1{,}2, \qquad \mathbb{E}[C_i \mid k_i = 4] = \frac{1{,}2}{6} = 0{,}2 = p$$

### Clustering e dimensione della rete
- Da $\langle k \rangle = (n-1)p$ si ha $p = \frac{\langle k \rangle}{n-1}$ e, per reti grandi ($n - 1 \approx n$):

$$C \approx \frac{\langle k \rangle}{n}$$

  (clustering medio calcolato **sui nodi con grado almeno 2**)
- **A grado medio fisso il clustering diminuisce all'aumentare della dimensione della rete**. Esempio con $\langle k \rangle = 4$:

| $n$ | 100 | 1.000 | 10.000 | 100.000 |
|---|---|---|---|---|
| $C$ atteso $= p$ | 0,0404 | 0,0040 | 0,0004 | 0,00004 |

- Figure (20 repliche):
  - **ER $N = 1000$, $\langle k \rangle$ da 0 a 100**: il clustering medio simulato sta esattamente sulla retta teorica $C = p$, fino a circa 0,1 per $\langle k \rangle = 100$
  - **ER $\langle k \rangle = 6$, $N$ da 50 a circa 10.000** (scala log-log): il clustering scende da circa 0,12 a meno di $10^{-3}$, sulla curva teorica $C = \langle k \rangle / (N-1)$
- (Aggiunta: le reti reali di qualche migliaio di nodi hanno clustering dell'ordine di 0,1-0,5, centinaia di volte sopra il valore ER; è il motivo per cui ER non basta e nasce Watts-Strogatz)

## Assortatività
- In ER **non c'è preferenza** per collegare nodi di grado simile o diverso: la probabilità di creare un arco **non dipende dal grado** dei nodi
- Per reti grandi e sparse:

$$n \to \infty \quad \Longrightarrow \quad r \to 0$$

  con $r$ il coefficiente di assortatività di grado di Newman (Modulo 5). Il modello ER è **asintoticamente non assortativo**
- Figure (20 repliche, valori approssimati):
  - **ER $\langle k \rangle = 6$, $N$ da 50 a circa 10.000**: $r$ medio circa $-0{,}03$ per $N = 50$ e circa $-0{,}04$ per $N = 100$, poi praticamente 0; la banda di variabilità, circa $\pm 0{,}1$ a $N = 50$, si stringe fino quasi a zero
  - **ER $N = 1000$, $\langle k \rangle$ da 1 a 100**: aumentando molto il grado medio l'assortatività **resta molto vicina a zero** (oscillazioni entro circa $\pm 0{,}01$, banda più larga, circa $\pm 0{,}04$, per $\langle k \rangle$ piccoli)
- (Aggiunta: il valore leggermente negativo per $N$ piccolo è un effetto di taglia finita che sparisce al crescere di $N$; con NetworkX, su 200 ER con $N = 50$ e $\langle k \rangle = 6$, $r$ medio esce $-0{,}05$)

## Robustezza
- La **robustezza** misura la capacità di una rete di mantenere la propria connettività quando vengono rimossi nodi o archi. Due strategie di rimozione:
  - **errore casuale**: nodi rimossi a caso, indipendentemente dal grado
  - **attacco mirato**: rimossi per primi i nodi con **grado più elevato**
- Figura (fonte non indicata): taglia della componente maggiore contro frazione di nodi rimossi, con tre curve che partono da circa 0,6: *classical attacks* la azzerano entro circa il 3%, *almost-random node attacks* verso il 25%, *node failures* calano lentamente fino a circa il 100% (le tre strategie non sono spiegate nelle slide)
- **Misura più usata**: la dimensione relativa della LCC

$$S(f) = \frac{N_{LCC}(f)}{N_0}$$

  con $f$ frazione di nodi rimossi e $N_0$ numero **iniziale** di nodi. (Aggiunta: dividendo per $N_0$ vale sempre $S(f) \leq 1 - f$, quindi una rete molto robusta segue la diagonale $1 - f$)

### Errore vs attacco al variare del grado medio
- **LCC/N, $\langle k \rangle = 2, 4, 8, 16$** (valori letti dal grafico, approssimati):

| $\langle k \rangle$ | LCC/N iniziale | errore casuale: LCC quasi nulla a | attacco per grado: crollo a |
|---|---|---|---|
| 2 | circa 0,75 | circa 0,55 (calo graduale) | circa 0,07-0,1 |
| 4 | circa 0,98 | circa 0,7-0,8 | circa 0,27-0,3 |
| 8 | 1 | oltre 0,9 | circa 0,47-0,5 |
| 16 | 1 | oltre 0,9 (a 0,9 resta circa 0,07) | circa 0,64 |

  - sotto errore, per $\langle k \rangle \geq 8$ la LCC segue quasi la diagonale $1 - f$: si perdono solo i nodi tolti
  - sotto attacco la curva segue la diagonale e poi **crolla di colpo**; più alto il grado medio, più tardi avviene il crollo
- **Efficienza normalizzata** (efficienza / efficienza iniziale, $N = 500$): sotto errore cala in modo **graduale e convesso** fino a circa 0 verso 0,85-0,9 di nodi rimossi, con $\langle k \rangle = 2$ un po' più rapida; sotto attacco per grado si annulla a circa 0,1 ($\langle k \rangle = 2$), 0,27 (4), 0,47 (8), 0,65 (16), più o meno dove crolla la LCC
- **Attacchi per grado, betweenness, closeness ed errore casuale** ($N = 500$, valori approssimati):
  - efficienza: i tre attacchi sono simili; betweenness è un po' più lenta (azzeramento verso circa 0,12, 0,3, 0,5, 0,7 per i quattro gradi medi); l'errore casuale è nettamente il meno dannoso
  - LCC/N: grado e closeness quasi identici (crollo a circa 0,1, 0,28-0,3, 0,47, 0,65-0,67); con la betweenness il crollo arriva a circa 0,12, 0,25-0,27, 0,5, 0,72-0,75. Sotto errore la LCC scende quasi lineare fino a circa 0,85-0,9
  - (Nella figura dell'efficienza la legenda è tagliata, "<k> =" senza valore; i colori sono gli stessi della figura LCC. Le slide non dicono se le centralità vengono ricalcolate dopo ogni rimozione)
- (Aggiunta, non nelle slide: per ER la soglia teorica dell'errore casuale è $f_c = 1 - 1/\langle k \rangle$, cioè 0,5, 0,75, 0,875 e 0,94 per i quattro gradi medi, coerente con le curve. Il motivo: togliendo a caso una frazione $f$ di nodi, la rete residua è ancora un ER con grado medio $\langle k \rangle (1-f)$, e la componente gigante sparisce quando questo scende a 1, come nel processo di ramificazione. Sotto attacco la soglia è molto più bassa perché si tolgono per primi i nodi che portano più archi)

### Robustezza e dimensione della rete
- **$\langle k \rangle = 6$, $N = 100$, 500, 1000, 5000, poi anche 50.000**: le curve si sovrappongono. Sotto errore la LCC scende quasi lineare fino a circa 0,8-0,83; sotto attacco per grado crolla attorno a 0,38-0,4 (valori approssimati)
- **Nel ER, a grado medio costante, la robustezza alla rimozione dei nodi tende a essere indipendente dalla dimensione della rete**
- (Verifica con NetworkX, ER $N = 2000$, $\langle k \rangle = 6$, attacco con grado ricalcolato a ogni passo: la LCC scende sotto il 5% a $f = 0{,}81$ sotto errore, contro la teoria $1 - 1/6 \approx 0{,}83$, e a $f = 0{,}39$ sotto attacco)

## Modello Watts-Strogatz

### Perché nasce
- Il modello ER per reti grandi e sparse a grado medio costante ha:

$$\bar d_{ER} \sim \frac{\ln n}{\ln \langle k \rangle} \quad \text{distanze relativamente piccole}, \qquad C_{ER} \approx \frac{\langle k \rangle}{n} \quad \text{clustering molto basso}$$

- Molte reti reali, soprattutto **sociali**, hanno invece **distanze medie piccole** e **clustering locale elevato**: è la proprietà **small-world**, che ER non riproduce

### Il reticolo regolare ad anello
- Il modello parte da un **reticolo regolare ad anello**: ogni nodo è collegato ai suoi **$K$ vicini più prossimi**, con $K$ pari, cioè $K/2$ per lato (figura con $K = 4$)
- Confronto delle slide:

| | Reticolo ad anello | Grafo casuale ER |
|---|---|---|
| Clustering $C$ | alto ($\approx 3/4$ per $K$ grande) | basso ($\approx p$) |
| Distanza media $\langle d \rangle$ | alta ($\sim n / 2K$, lineare in $n$) | bassa ($\sim \ln n / \ln \langle k \rangle$) |

- Figura con $N = 12$: $K = 2$ → $C(0) = 0$; $K = 4$ → $C(0) = 0{,}50$; $K = 6$ → $C(0) = 0{,}60$
- (Aggiunta: il clustering del reticolo vale esattamente $C(0) = \frac{3(K-2)}{4(K-1)}$, che dà 0, 0,5 e 0,6 per $K = 2, 4, 6$ e tende a $3/4$; verificato con NetworkX. Per $n = 1000$, $K = 10$ la distanza media è 50,45, contro $n/2K = 50$)

### Rewiring
- Poi **ogni arco viene ricablato** (*rewiring*) **con probabilità $\beta$**: uno dei suoi estremi viene spostato su un nodo scelto a caso. (Nella slide 65 il testo è coperto dall'immagine; si legge per intero nella 66)
- Figura (D. J. Watts e S. H. Strogatz, *Collective dynamics of "small-world" networks*, Nature 393 (6684): 440-442, giugno 1998): da $\beta = 0$ (reticolo regolare) a $\beta = 1$ (rete casuale), con **casualità crescente**; nel mezzo il reticolo con poche scorciatoie
- Il modulo finisce qui (slide "Fine"): le proprietà del regime small-world non sono ancora trattate. (Aggiunta, con NetworkX, $n = 1000$, $K = 10$:

| $\beta$ | 0 | 0,01 | 0,1 | 1 |
|---|---|---|---|---|
| $C$ | 0,667 | 0,650 | 0,482 | 0,009 |
| $\bar d$ | 50,45 | 9,66 | 4,40 | 3,27 |

  bastano pochissimi archi ricablati per far crollare la distanza media mentre il clustering resta quasi quello del reticolo: è il regime small-world. Nel Modulo 5 il WS con `nei = 3`, $p = 0{,}05$ aveva infatti clustering circa 0,45)

## Funzioni utili per il progetto (aggiunta, non nelle slide)
Le slide di questo modulo non riportano codice. Questi snippet sono stati eseguiti (NetworkX 3.7, python-igraph 1.0); i commenti riportano l'output.

```python
import math
import networkx as nx

n, p = 1000, 0.004
G = nx.gnp_random_graph(n, p, seed=42)            # G(n, p), alias nx.erdos_renyi_graph
H = nx.gnm_random_graph(100, 495, seed=42)        # G(n, m): esattamente m archi
F = nx.fast_gnp_random_graph(100000, 4 / 99999, seed=42)  # stesso modello, veloce su reti sparse

m = G.number_of_edges()
k_medio = 2 * m / n
P_k = [c / n for c in nx.degree_histogram(G)]     # P(k) empirica, da confrontare con Poisson
lcc = G.subgraph(max(nx.connected_components(G), key=len))
S = lcc.number_of_nodes() / n
d = nx.average_shortest_path_length(lcc)
C_k2 = sum(c for v, c in nx.clustering(G).items() if G.degree(v) >= 2) / sum(1 for v in G if G.degree(v) >= 2)
C_nx = nx.average_clustering(G)                   # conta come 0 i nodi con k < 2
r = nx.degree_assortativity_coefficient(G)

print(H.number_of_edges(), F.number_of_nodes())                 # 495 100000
print(m, round(k_medio, 2), round(P_k[4], 3), round(S, 3), nx.is_connected(G))  # 1986 3.97 0.218 0.978 False
print(round(d, 2), round(math.log(n) / math.log(k_medio), 2))   # 5.1 5.01
print(round(C_k2, 4), round(C_nx, 4), round(k_medio / n, 4), round(r, 3))  # 0.0065 0.0059 0.004 -0.032

W = nx.watts_strogatz_graph(1000, 10, 0.1, seed=42)  # n, K vicini (pari), beta
W = nx.connected_watts_strogatz_graph(1000, 10, 0.1, seed=42)  # ripete finché è connesso
print(round(nx.average_clustering(W), 3), round(nx.average_shortest_path_length(W), 2))  # 0.499 4.49
```

- Il clustering su una sola realizzazione oscilla molto (0,0065 contro $p = 0{,}004$): con $n = 1000$ e $p = 0{,}004$ i triangoli attesi sono solo una decina. Per confrontarlo con $p$ si fa la media su più repliche, come nelle figure delle slide
- `nx.average_clustering` conta come 0 i nodi con grado minore di 2, mentre la formula $C \approx \langle k \rangle / n$ delle slide è calcolata solo sui nodi con $k \geq 2$; con $\langle k \rangle = 4$ circa il 9% dei nodi ha grado 0 o 1, quindi le due medie differiscono (stesso problema del Modulo 5)

Robustezza, errore casuale contro attacco per grado ricalcolato:

```python
import random
import networkx as nx

def robustezza(G, attacco, seed=0):
    G = G.copy()
    n0 = G.number_of_nodes()
    ordine = list(G.nodes())
    random.Random(seed).shuffle(ordine)
    S = []
    for i in range(n0):
        S.append(max(len(c) for c in nx.connected_components(G)) / n0)
        v = max(G.degree, key=lambda x: x[1])[0] if attacco else ordine[i]
        G.remove_node(v)                          # attacco: grado ricalcolato a ogni passo
    return S

G = nx.fast_gnp_random_graph(2000, 6 / 1999, seed=4)
for attacco in (False, True):
    S = robustezza(G, attacco)
    print(attacco, next(i for i, s in enumerate(S) if s < 0.05) / 2000)
# False 0.807
# True 0.394
```

Gli stessi modelli con python-igraph:

```python
import igraph as ig

ig.set_random_number_generator(__import__("random").Random(42))
g = ig.Graph.Erdos_Renyi(n=1000, p=0.004)
h = ig.Graph.Erdos_Renyi(n=100, m=495)
w = ig.Graph.Watts_Strogatz(dim=1, size=1000, nei=5, p=0.1)   # nei = K/2 per lato

lcc = g.connected_components().giant()
print(g.ecount(), h.ecount(), lcc.vcount(), g.is_connected())  # 1957 495 978 False
print(round(lcc.average_path_length(), 2), round(g.transitivity_avglocal_undirected(mode="nan"), 4), round(g.transitivity_avglocal_undirected(mode="zero"), 4))  # 5.14 0.0022 0.002
print(round(g.assortativity_degree(), 3), round(w.transitivity_avglocal_undirected(), 3), round(w.average_path_length(), 2))  # -0.026 0.367 3.91
```

- In igraph `nei` è il numero di vicini **per lato** ($K/2$), in NetworkX `k` è il numero **totale** di vicini ($K$)
- **Attenzione**: a parità di probabilità igraph e NetworkX non danno lo stesso WS (clustering 0,367 contro 0,499 con $p = 0{,}1$). La documentazione di igraph dice che `Watts_Strogatz` ricabla **entrambi gli estremi** di ogni arco con probabilità $p$, mentre il modello originale (e NetworkX) ne sposta uno solo: l'effetto è circa quello di un $\beta$ doppio (NetworkX con $\beta = 0{,}2$ dà clustering circa 0,35). Vale anche per `sample_smallworld` di R, che usa lo stesso motore; nel report va detto quale implementazione si è usata
- `transitivity_avglocal_undirected(mode="nan")` esclude i nodi con grado minore di 2 (come la formula delle slide), `mode="zero"` li conta come 0 (come NetworkX)
- In R/igraph le funzioni corrispondenti sono `sample_gnp(n, p)`, `sample_gnm(n, m)` e `sample_smallworld(dim, size, nei, p)` (non eseguite qui: R non è installato su questa macchina; il Modulo 5 usava `erdos.renyi.game` e `sample_smallworld`)

## Da ricordare per l'orale e il progetto
- Un **modello di rete** genera reti con regole semplici; serve a capire come nascono le proprietà globali e come **modello nullo** per le reti reali (si confronta la rete reale con un ER con stessi $n$ e $\langle k \rangle$)
- **ER**: $G(n, m)$ fissa gli archi, $G(n, p)$ mette ogni arco con probabilità $p$ indipendente. $\langle m \rangle = p\,n(n-1)/2$ (es. 495 con $n = 100$, $p = 0{,}1$), $\langle k \rangle = (n-1)p \approx np$ (es. 9,9)
- Distribuzione dei gradi **binomiale** $\binom{n-1}{k} p^k (1-p)^{n-1-k}$, che per reti grandi e sparse diventa **Poisson** $e^{-\lambda}\lambda^k/k!$ con $\lambda = \langle k \rangle = \sigma_k^2$: rete **omogenea**, niente hub
- **Componente gigante**: compare a $\langle k \rangle_c = 1$, cioè $p_c \approx 1/n$ (transizione di fase, spiegata dal processo di ramificazione sotto/critico/sopra). Sotto soglia, per $n \to \infty$, la LCC è una frazione nulla dei nodi
- **Connettività completa**: serve $\langle k \rangle \sim \ln N$, cioè $p \approx \ln N / N$ (0,00691 per $N = 1000$), molto dopo la componente gigante; sulla soglia la rete è connessa solo con probabilità circa 0,37
- **Distanza media** $\bar d \sim \ln n / \ln \langle k \rangle$: cresce come $\ln n$, non come $n$ (small-world); diminuisce all'aumentare del grado medio
- **Clustering** $C = p \approx \langle k \rangle / n$: bassissimo e decrescente con $n$ a grado medio fisso; il calcolo è sui nodi con $k \geq 2$
- **Assortatività** $r \to 0$: in ER l'arco non dipende dal grado (leggermente negativa solo per reti piccole)
- **Robustezza** misurata con $S(f) = N_{LCC}(f) / N_0$: ER regge bene l'**errore** casuale (soglia $1 - 1/\langle k \rangle$) e cede prima all'**attacco** per grado; più alto il grado medio, più robusta la rete; a $\langle k \rangle$ costante la robustezza **non dipende da $N$**
- **Watts-Strogatz**: nasce perché ER ha distanze piccole ma clustering bassissimo, mentre le reti sociali hanno entrambi. Parte da un **anello** con $K$ vicini (clustering alto, $C(0) = 0{,}5$ con $K = 4$, distanza $\sim n/2K$) e **ricabla ogni arco con probabilità $\beta$**: $\beta = 0$ reticolo, $\beta = 1$ casuale
- Nel progetto: in igraph `Watts_Strogatz`/`sample_smallworld` ricabla entrambi gli estremi, in NetworkX uno solo; e `nx.average_clustering` conta 0 i nodi con $k < 2$
