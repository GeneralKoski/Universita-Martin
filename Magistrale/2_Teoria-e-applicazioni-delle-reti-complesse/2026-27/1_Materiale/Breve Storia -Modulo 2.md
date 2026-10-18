# Modulo 2 - Breve storia della scienza delle reti

Fonte: `Breve Storia -Modulo 2.pdf`

Percorso storico: Eulero (1736) → Erdős e Rényi (1959) → Milgram (anni '60) → Granovetter (1973) → Watts e Strogatz (1998) → Dodds, Muhamad e Watts (2003, ma qui presentato prima del modello small-world) → Barabási e Albert (1999).

## I ponti di Königsberg (1736)

### Il problema
- **Königsberg** (Prussia), XVIII secolo: la città è attraversata dal fiume Pregel, con due isole e **sette ponti**
- Domanda: **«È possibile fare una passeggiata che attraversi tutti e sette i ponti esattamente una volta, e tornare al punto di partenza?»**
- Figura: incisione della città con i sette ponti evidenziati

### La soluzione di Eulero
- **Leonhard Euler** (Eulero; Basilea, 1707 - San Pietroburgo, 1783) risolve il problema nel **1736** e **dimostra che è impossibile**
- **Astrae la mappa in un grafo**: le **terre** (due rive e due isole) diventano **nodi**, i **ponti** diventano **archi**
- Figura: schema con le quattro terre A, B, C, D e il **multigrafo** corrispondente. Nella versione delle slide 5-7: C è l'isola centrale, collegata ad A con **2** archi, a B con **2**, a D con **1**; A e B sono collegati a D con un arco ciascuno. Gradi: $k_C = 5$, $k_A = k_B = k_D = 3$. (La figura della slide 4 usa lettere diverse per le stesse terre, con A sull'isola centrale.)
- La **forma fisica** della città è **irrilevante**: conta solo quanti ponti (le slide dicono "strade") toccano ogni terra ("incrocio")
- **Nasce la teoria dei grafi**: la **struttura delle connessioni** è più importante della geometria o della fisica del sistema
- **Grado** di un nodo = numero di link che lo toccano

### La regola di Eulero
- In un **cammino chiuso** tutti i nodi devono avere **grado pari**: ogni volta che si entra in una terra se ne deve anche uscire
- **Cammino euleriano** (percorre ogni arco **una sola volta**): esiste se e solo se ogni nodo ha grado pari (cammino chiuso), oppure, per i cammini **non chiusi**, se al massimo due nodi hanno grado dispari. (Precisazione: la condizione vale per grafi **connessi**, e i nodi di grado dispari sono **zero o esattamente due**, mai uno solo, perché la somma dei gradi è sempre pari; i due nodi dispari sono gli estremi del cammino.)
- A Königsberg **tutti e quattro i nodi hanno grado dispari** → **impossibile**
- Lezione metodologica: **ignoro i dettagli fisici, estraggo solo la struttura delle relazioni, e ragiono su quella**

## Il grafo casuale di Erdős e Rényi (1959)

### Gli autori
- **Paul Erdős** (Budapest, 1913 - Varsavia, 1996): matematico ungherese, **apolide**, viveva con una valigia, girava il mondo e bussava alle porte dei colleghi dicendo **"la mia mente è aperta"**
- **Numero di Erdős** (le slide lo nominano soltanto; aggiunta: è la distanza di un autore da Erdős nella **rete delle co-autorialità**, 1 per chi ha scritto un articolo con lui, 2 per i co-autori dei suoi co-autori, ecc.)
- **Alfréd Rényi** (Budapest, 1921 - Budapest, 1970)

### Il modello $G(n, p)$
- **«Cosa succede se costruiamo un grafo in modo completamente casuale?»**: costruire un grafo **lanciando una moneta**
- Modello semplicissimo:
  - $N$ nodi
  - per **ogni coppia** di nodi si lancia una moneta: con probabilità $p$ si aggiunge un legame, con probabilità $1 - p$ no
- È il modello **$G(n, p)$** (1959). (Precisazione: nel lavoro del 1959 Erdős e Rényi definiscono la variante $G(N, L)$, con un numero fissato $L$ di link scelti a caso; la variante $G(N, p)$ è stata introdotta nello stesso anno da **E. N. Gilbert**. Le due varianti hanno proprietà equivalenti per $N$ grande e oggi si chiamano entrambe "grafo di Erdős-Rényi".)
- Figura: lo stesso insieme di nodi con $p = 0$ (nessun link), $p = 0{,}1$, $p = 0{,}2$ (sempre più link)

### Evoluzione e transizione di fase
- Il grafo casuale **non cambia gradualmente** all'aumentare di $p$: il cambiamento è **brusco** (le slide dicono "brusco e discontinuo"; precisazione sotto)
- Figura (da networksciencebook.com, cap. 3, "evolution of a random network"): frazione $N_G/N$ di nodi nella **componente gigante** in funzione del grado medio $\langle k \rangle$ (sull'asse c'è $\langle k \rangle$, le slide sovrappongono la scritta $p$; aggiunta: $\langle k \rangle = p(N-1)$, quindi le due scale sono proporzionali). La curva è nulla fino a $\langle k \rangle = 1$, poi sale rapidamente e tende a 1. Sotto, quattro reti di esempio: (b) solo piccoli frammenti, (c) al punto critico, (d) componente gigante (nodi viola) che ingloba quasi tutto, (e) rete tutta connessa. (Aggiunta, dal libro di Barabási: i quattro regimi colorati sono subcritico $\langle k \rangle < 1$, critico $\langle k \rangle = 1$, supercritico $\langle k \rangle > 1$, connesso $\langle k \rangle > \ln N$.)
- **Transizione di fase** con **soglia critica** $p_c \approx \dfrac{1}{N}$ (cioè $\langle k \rangle \approx 1$):
  - $p \ll \dfrac{1}{N}$: **no percolazione** (nessuna componente gigante)
  - $p \gg \dfrac{1}{N}$: **sì percolazione** (emerge una componente gigante che contiene una frazione finita dei nodi)
- (Precisazione su "discontinuo": la transizione di Erdős-Rényi è **brusca** nel senso che avviene a una soglia precisa, ma in senso fisico è **continua** (del secondo ordine): la frazione di nodi nella componente gigante parte da zero e cresce con continuità oltre $\langle k \rangle = 1$, come mostra la stessa curva della figura.)

### Distanze nel grafo casuale
- Figura (DOI 10.1103/PhysRevE.70.056110): **lunghezza media dei cammini** $l_{ER}$ in funzione della dimensione $N$ (da $10^2$ a $10^5$, asse logaritmico) per $\langle k \rangle = 4, 10, 20$: punti allineati su **rette**, quindi la distanza cresce come $\ln N$
- Figura in scala lineare: **crescita logaritmica della distanza media** nel grafo di Erdős e Rényi, con

$$\langle \ell \rangle \approx \frac{\ln N}{\ln \langle k \rangle}$$

- **A grado medio fissato**, la distanza media cresce **solo lentamente (logaritmicamente)** con $N$: con 100.000 nodi e $\langle k \rangle = 4$ si resta sotto 9 passi
- **A parità di $N$**, un **grado medio più grande** dà **distanze medie più piccole** (le curve per $\langle k \rangle = 10$ e $20$ stanno sotto quella per $4$)

## Sei gradi di separazione: Stanley Milgram
- **Stanley Milgram** (New York, 1933 - New York, 1984), psicologo sociale
- **Teoria del mondo piccolo** (le slide datano l'esperimento **1957**: l'esperimento di Milgram è del **1967**, pubblicato su *Psychology Today* nel 1967 e, con Travers, su *Sociometry* nel 1969)
- Figure: cartello "Small World Theory" e locandina del film *Six Degrees of Separation* (1993, Stockard Channing, Will Smith, Donald Sutherland)
- **L'esperimento**: lettere spedite da persone del Midwest (mappa con alcuni stati del centro evidenziati in rosso) a un **estraneo** in Massachusetts (Boston)
  - Ai partecipanti si danno **nome del destinatario**, **impiego**, **zona di residenza**, ma **non l'indirizzo**
  - Se il partecipante **conosce** il destinatario gli spedisce la lettera direttamente; altrimenti la spedisce a un proprio **conoscente** che ritiene più vicino al destinatario, che ripete il procedimento
  - Figura: piccola rete di conoscenze fra persone (Larry, Francis, Gary, Emily, Debbie, Doug, Richard, Rebecca, Rajat, Ryan, Arnold)
- **Risultato**: si poteva ipotizzare che servissero **centinaia di intermediari**, invece le lettere **giunsero con circa sei passaggi** → **sei gradi di separazione**. Figura: rete fitta e un cammino A → 1 → 2 → 3 → 4 → 5 → 6 → B
- **Omaha e Boston** sono a quasi **2000 km** di distanza

## La forza dei legami deboli: Mark Granovetter (1973)
- **Mark Granovetter** (Jersey City, 1943), sociologo
- **"The Strength of Weak Ties"**, *American Journal of Sociology*, **1973**
- **Intervista centinaia di professionisti** nel Massachusetts che avevano **cambiato lavoro di recente**: **come avevano trovato il nuovo impiego?**
- **Risultato inaspettato**: la maggior parte aveva trovato lavoro attraverso **conoscenti**: **non amici**, **non parenti**, **non agenzie**
- Granovetter chiede: **quanto spesso vedevano questa persona?** Risposta: **raramente**, **qualche volta l'anno** → sono **legami deboli**
- Figura "Weak hypothesis" (DOI 10.3389/fphy.2020.00228): gruppi densi di nodi (**legami forti** all'interno) collegati fra loro da pochi link singoli (**legami deboli**)
- **Conseguenze**: i legami deboli
  - sono **fondamentali alla diffusione delle informazioni** (portano notizie nuove, che nel proprio gruppo stretto già circolano)
  - sono **fondamentali alla coesione della rete**
  - conferiscono **robustezza** al sistema sociale
  - **connettono insiemi differenti** (fanno da ponte fra gruppi)
- Figura "The Strength of Weak Ties" (blog.orglens.com, "it is your friends' friends who will help you get your next job"): un cerchio di **strong ties** separato e una costellazione di cerchi collegati dai **weak ties**

## Weak ties su scala globale: Dodds, Muhamad e Watts (2003)
- **2003**: Watts, Dodds e Muhamad **replicano digitalmente l'esperimento di Milgram su scala globale**, con una **gigantesca catena di e-mail** via Internet: **oltre 60.000 persone**, **166 paesi**
- Articolo: P. S. Dodds, R. Muhamad, D. J. Watts, **"An Experimental Study of Search in Global Social Networks"** (*Science*; lo screenshot riporta l'abstract: oltre 60.000 utenti e-mail, 18 target in 13 paesi, la ricerca riuscita passa soprattutto per **legami di forza intermedia**, **non richiede hub** molto connessi, e le catene arrivano in una **mediana di 5-7 passi**)
- Domanda: **è possibile raggiungere uno sconosciuto qualsiasi tramite pochi passaggi sociali?**, cioè **"navigare"** una rete sociale globale usando **solo conoscenza locale**
- **Target**: **18 persone** in **13 paesi** diversi, fra cui un professore universitario, un poliziotto australiano, un veterinario norvegese, un archivista estone, un consulente tecnologico indiano
- **Reclutamento**: i partecipanti si **registravano online**
- **Informazioni minime** sul target: **nome**, **città**, **professione**, **istruzione**
- **Compito**: inoltrare il messaggio a **UNA** persona conosciuta che ritenevano **"più vicina" al target**, usando solo la **propria rete sociale reale**
- **Catene sociali**: ogni inoltro crea **un edge della catena**, es. A → B → C → D → target
- **Risultato finale**: circa **5-7 passaggi medi** (figura "Six degrees of separation": You → 1 → ... → 6 → a random person in the World)

## Come descrivere le reti small world
- **Small-world network** = **bassa distanza fra i nodi** + **alto clustering** (forte coesione locale)
- Figure (DOI 10.3389/fnins.2019.00585): **clustering coefficient** (un nodo i cui vicini sono collegati fra loro formano triangoli, evidenziati in rosso) e **modularity** (tre gruppi densi collegati da pochi link)
- Il **grafo casuale** descrive bene la **bassa distanza** fra i nodi delle reti reali, ma **non** il loro **alto clustering**: serve un altro modello

## Watts e Strogatz (1998): il modello small-world
- **Duncan Watts** (le slide: "Guelph (US), 1971"; Guelph è in **Canada**, Ontario, non negli Stati Uniti) e **Steven Strogatz** (Torrington, USA, 1959)
- Introducono un **modello matematico di grafo** per spiegare le reti sociali: la rete **"small-world"** (le slide scrivono "Watts and Strogatz (1999)" nel testo e "1998" nel titolo: l'anno corretto è il **1998**)
- Riferimento: **Watts, D., Strogatz, S. "Collective dynamics of 'small-world' networks". *Nature* 393, 440-442 (1998)**, https://doi.org/10.1038/30918
- Le **reti sociali reali** hanno:
  - **clustering alto**, come le **reti regolari**
  - **distanze brevi**, come le **reti casuali**
- Figura: un anello regolare in cui un solo link (rosso) collega due nodi lontani: una **scorciatoia** basta ad accorciare molto le distanze
- Figura classica **Regular → Small-world → Random**: anello regolare in cui ogni nodo è collegato ai vicini più prossimi ($p = 0$); aumentando la casualità (**increasing randomness**) alcuni link vengono ricollegati a caso (small-world); con $p = 1$ la rete è completamente casuale. (Aggiunta: $p$ è la **probabilità di ricablare** ogni link.)
- La rete small-world sta **in mezzo**: **distanze brevi** come le reti casuali e **clustering alto** come le reti regolari

## Barabási e Albert (1999): reti scale-free

### Gli autori
- **Albert-László Barabási** (le slide: "Cârța (Ungheria), 1967"; Cârța si trova in **Romania**, in Transilvania: Barabási è di etnia ungherese, ma nato in Romania)
- **Réka Albert** (Reghin, Romania, 1972)

### Il punto di partenza: mappare il Web
- Il gruppo di Barabási sviluppa un **crawler** e mappa una porzione significativa del Web: **circa 300.000 pagine e milioni di link** (aggiunta: il dominio nd.edu, circa 325.000 pagine e 1,5 milioni di link, Albert, Jeong e Barabási, *Nature* 1999)
- Grafo: **nodi = pagine web**, **archi = link da una pagina all'altra** (orientati)
- Figura: mappa del Web in rosso e giallo, con pochi centri luminosissimi da cui si irradiano moltissimi link

### La distribuzione dei gradi
- Misurano i **link per nodo** (**grado del nodo**)
- **Si aspettano una distribuzione di Poisson**, come nel modello casuale (random graph)
- Trovano invece una **legge di potenza** (power law):

$$P(k) \sim k^{-\gamma}$$

- Figura "Power Law Distribution": $p(k)$ (numero di nodi di grado $k$) crolla rapidamente con $k$ ma ha una **coda lunga**
- Conseguenza: esistono **huge hubs**, **iperconnettori**: pochi nodi con un numero enorme di link, impossibili in un grafo casuale

### Robustezza: attacco ed errore
- **Attacco**: si rimuovono i **nodi più connessi** (hub per primi)
- **Random** (errore, guasto casuale): si rimuovono nodi a caso
- Figura (networksciencebook.com, cap. 8): rete scale-free con hub; grafico di $P_\infty(f)/P_\infty(0)$ (dimensione relativa della componente gigante) in funzione della frazione $f$ di nodi rimossi
  - **Random failures** (verde): la componente gigante cala **lentamente** e si annulla solo per $f$ vicino a 1
  - **Attacks** (viola): crolla a **zero già per $f \approx 0{,}15$-$0{,}2$**
- Le **reti reali** sono quindi **vulnerabili all'attacco** ma **resistenti all'errore**
- (Precisazione: questo risultato è di Albert, Jeong e Barabási, "Error and attack tolerance of complex networks", *Nature*, **2000**, cioè successivo al modello del 1999 sotto il cui titolo compare nelle slide.)

### Il modello di Barabási-Albert
Due ingredienti:
1. **Crescita** (*growth*): la rete **non è statica**, ma **cresce nel tempo**; ogni **nuovo nodo** crea $m$ collegamenti con nodi già presenti
2. **Attaccamento preferenziale** (*preferential attachment*): il nuovo nodo **non sceglie a caso** a chi collegarsi; la probabilità di collegarsi al nodo $i$ è **proporzionale al suo grado**:

$$\pi_i = \frac{k_i}{\sum_j k_j}$$

- Più un nodo è connesso, maggiore è la probabilità che riceva nuovi link: **"rich get richer"**
- Figura: dieci istantanee della crescita; a ogni passo compare un nuovo nodo (bianco) che si collega a nodi esistenti, e i nodi già ricchi di link ne raccolgono sempre di più
- (Aggiunta: il modello produce una distribuzione $P(k) \sim k^{-3}$, cioè $\gamma = 3$.)

### Rete casuale contro rete scale-free
- **Random network** → **grado caratteristico** (quasi tutti i nodi hanno grado vicino a $\langle k \rangle$), **struttura omogenea**
- **Scale-free network** → **assenza di una scala caratteristica**, **forte eterogeneità**, presenza di **hub**
- Figura:
  - (a) scala lineare: la Poisson (verde) è una campana centrata intorno a $k \approx 10$; la legge di potenza $p_k \sim k^{-2,1}$ (viola) parte altissima per $k$ piccoli e scende con una coda lunga
  - (b) scala **log-log**: la legge di potenza è una **retta**, la Poisson crolla velocemente per $k$ grandi (nodi di grado alto praticamente impossibili)
  - (c) rete casuale: nodi tutti simili
  - (d) rete scale-free: pochi grandi hub e molti nodi con pochi link

## Da ricordare
- **1736, Eulero**, ponti di Königsberg: terre = nodi, ponti = archi; cammino euleriano chiuso solo se tutti i gradi sono pari (aperto se esattamente due dispari, grafo connesso); a Königsberg tutti e quattro dispari → impossibile; nasce la **teoria dei grafi**, conta la struttura e non la geometria
- **1959, Erdős e Rényi**: grafo casuale, ogni coppia collegata con probabilità $p$; **transizione di fase** a $p_c \approx 1/N$ ($\langle k \rangle \approx 1$) con comparsa della componente gigante (percolazione); distanza media $\langle \ell \rangle \approx \ln N / \ln \langle k \rangle$, cresce logaritmicamente; **clustering basso**; distribuzione dei gradi di **Poisson**
- **Milgram (1967)**: lettere verso un estraneo tramite conoscenti, circa **sei passaggi** → **sei gradi di separazione**, mondo piccolo
- **Granovetter (1973)**, *The Strength of Weak Ties*: il lavoro si trova tramite **conoscenti** visti raramente; i legami deboli fanno da **ponte** fra gruppi, diffondono informazione, danno coesione e robustezza
- **Dodds, Muhamad, Watts (2003)**: Milgram via e-mail, oltre 60.000 persone, 166 paesi, 18 target in 13 paesi, solo conoscenza locale, **5-7 passaggi**
- **Small world** = distanza media bassa + clustering alto; **Watts e Strogatz (1998, *Nature* 393)**: ricablando con probabilità $p$ un reticolo regolare si ottengono reti a metà fra regolare e casuale
- **Barabási e Albert (1999)**: il Web ha gradi a **legge di potenza** $P(k) \sim k^{-\gamma}$ con **hub**; modello = **crescita** + **attaccamento preferenziale** $\pi_i = k_i / \sum_j k_j$ ("rich get richer"); reti scale-free **robuste ai guasti casuali** e **fragili agli attacchi mirati** agli hub
