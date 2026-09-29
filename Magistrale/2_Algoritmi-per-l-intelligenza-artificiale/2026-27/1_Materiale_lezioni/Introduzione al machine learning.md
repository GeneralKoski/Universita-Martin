# Introduzione all'apprendimento automatico

Fonte: `Introduzione al machine learning.pdf`

## Tipi di apprendimento
Quattro tipi di attività:
- **Supervisionato** (supervised)
- **Semi-supervisionato** (semi-supervised)
- **Non supervisionato** (unsupervised)
- **Per rinforzo** (reinforcement learning), affermatosi più di "recente"

La differenza principale è la disponibilità di **ground truth** ("dati di verità di base"): informazione ottenuta per **osservazione diretta** (prova empirica), contrapposta a quella ottenuta per **inferenza**. È la conoscenza preliminare di quale dovrebbe essere l'**output** del modello per un dato input.

| Tipo | Obiettivo |
|---|---|
| Supervisionato | apprendere una funzione che, dati campioni e output desiderati, approssima la mappa input → output |
| Semi-supervisionato | etichettare i dati senza etichetta usando ciò che si apprende da **pochi dati etichettati** |
| Non supervisionato | nessun output etichettato: dedurre la **struttura naturale** dei dati |
| Per rinforzo | agenti autonomi che scelgono azioni interagendo con l'ambiente per **massimizzare il premio cumulativo** |

## Apprendimento supervisionato
Due contesti:
- **Classificazione**: input → **etichette** di output (discrete). Figura: due classi (cerchi e croci) nel piano $(x_1, x_2)$ separate da una retta
- **Regressione**: input → **output continuo**. Figura: punti $(x, y)$ con retta interpolante

Algoritmi comuni:
- **regressione logistica**
- **classificatore bayesiano naif** (tipicamente per categorizzazione di testi)
- **macchine a vettori di supporto** (SVM, sia regressione sia classificazione)
- **reti neurali artificiali**
- **foreste casuali** (random forest: classificatori d'insieme composti da molti alberi di decisione)

In entrambi i casi si cercano **relazioni o strutture specifiche** nei dati di input che permettano di produrre output corretti.

- L'output "corretto" è determinato **interamente dai dati di addestramento**: la ground truth è ciò che il modello riterrà vero
- Nel mondo reale le etichette non sono sempre corrette: etichette **rumorose** o **errate** riducono l'efficacia del modello

## Overfitting
- **Complessità del modello**: complessità della funzione da apprendere, analoga al **grado di un polinomio**. Il livello giusto dipende dalla natura dei dati di training
- Con **pochi dati** o dati **non distribuiti uniformemente** sui possibili scenari → preferire un modello a **bassa complessità**
- Un modello ad alta complessità su pochi punti va in **overfitting** (sovradattamento): ha troppi parametri rispetto al numero di osservazioni e si adatta al campione
- Definizione: apprendere una funzione che si adatta molto bene ai dati di training ma **non generalizza** ad altri punti; si impara a riprodurre il training senza cogliere la tendenza o struttura reale che genera l'output

Esempio: per far passare una curva per 2 punti si può usare una funzione di qualsiasi grado, ma per **parsimonia** si sceglie quella lineare.

Figure della slide 7:
- punti 1D approssimati da una **retta** vs una curva polinomiale che passa per tutti i punti oscillando molto
- classificazione 2D (punti rossi e blu): frontiera liscia vs frontiera frastagliata che segue i singoli punti

## Compromesso bias-varianza
Riguarda la **generalizzazione**. In ogni modello c'è equilibrio tra:
- **distorsione (bias)**: termine di errore **costante**
- **varianza**: quanto l'errore può **variare tra diversi dataset**

Problema: un modello che catturi bene le regolarità del training ma generalizzi bene su dati non di training.

Grafico della slide 9 (errore in funzione della complessità del modello):
- **Bias²** decresce al crescere della complessità
- **Varianza** cresce al crescere della complessità
- **Errore totale** a forma di U, minimo alla **complessità ottima** (linea tratteggiata)

Proprietà:
- **Più bias, meno varianza** → prestazioni relativamente **garantite** (importante in certe attività)
- La varianza del modello va dimensionata su **dimensione e complessità** dei dati di training:
  - dataset **piccoli e semplici** → modelli a **bassa varianza**
  - dataset **grandi e complessi** → spesso modelli a **varianza più alta** per coglierne tutta la struttura

## Apprendimento semi-supervisionato
Esempio: rilevare messaggi inappropriati in un social network. Etichettarli tutti a mano è troppo costoso; si etichetta a mano un **sottoinsieme** e lo si usa per interpretare i messaggi nuovi.

Metodi comuni:
- **SVM trasversali** (così nella slide; nella letteratura sono le *transductive SVM*)
- **metodi basati su grafi**, es. **propagazione delle etichette** (label propagation)

### Presupposti
Servono ipotesi sui dati per giustificare l'uso di pochi dati etichettati per concludere sui non etichettati:
- **Continuità**: punti **vicini** hanno più probabilità di avere la stessa etichetta
- **Ipotesi del cluster**: i dati formano naturalmente **cluster discreti**; punti nello stesso cluster tendono a condividere l'etichetta
- **Presupposto molteplice** (manifold): i dati stanno approssimativamente in uno spazio di **dimensione inferiore** (collettore/varietà) rispetto allo spazio di input. Rilevante quando un sistema difficile da osservare, con **pochi parametri**, produce output osservabile **ad alta dimensione**

## Apprendimento non supervisionato
- Trova **pattern intrinseci** nei dati, senza etichette esplicite
- Attività più comuni: **clustering**, **apprendimento della rappresentazione**, **stima della densità**
- Algoritmi comuni: clustering, **analisi delle componenti principali** (PCA), **autoencoder**
- Senza etichette **non esiste un modo specifico per confrontare le prestazioni** del modello nella maggior parte dei metodi

Due tecniche principali: **clustering** e **riduzione della dimensionalità**.

### Clustering
- Tecnica **esplorativa**: aggrega in gruppi (**cluster**) dati di cui non si conosce a priori l'appartenenza
- Ogni cluster contiene dati con molte caratteristiche simili tra loro
- Serve a **scoprire relazioni** tra i dati
- Figura: tre gruppi di punti nel piano $(x_1, x_2)$ racchiusi da ellissi

### Riduzione della dimensionalità
- Molto usata nella **pre-elaborazione delle feature**, per eliminare il **rumore**
- Può ridurre la prestazione predittiva, ma rende lo spazio più **compatto** mantenendo l'informazione più rilevante
- Figure: **PCA biplot** sul dataset Iris (Dim1 73%, Dim2 22,9%; frecce delle variabili Sepal.Width, Sepal.Length, Petal.Width, Petal.Length) e **scree plot** della percentuale di varianza spiegata per dimensione (41,2%, 18,4%, 12,4%, 8,2%, 7%, 4,2%, 3%, 2,7%, 1,6%, 1,2%). Nota: i due grafici non si riferiscono allo stesso dataset (il biplot ha 4 variabili, lo scree plot 10 dimensioni)
- Utile anche per la **visualizzazione**: proiettare un feature space ad alta dimensione in 1D, 2D o 3D. Figura: "swiss roll" proiettato in 2D, "unrolled manifold", recupero con **LLE** e **HLLE** (i nomi compaiono solo nei titoli dei grafici, non spiegati)

### Analisi esplorativa
- Il non supervisionato è molto utile nell'**exploratory data analysis**: identifica automaticamente la struttura
- Esempio: **segmentazione dei consumatori** → il clustering è un ottimo punto di partenza
- Quando per un umano è impossibile o impraticabile proporre tendenze, fornisce **informazioni iniziali** da usare per formulare e verificare ipotesi

## Da ricordare per lo scritto
- I tipi di apprendimento si distinguono per **disponibilità di ground truth** (output noto per un input); ground truth = osservazione diretta, non inferenza
- Supervisionato: **classificazione** (output discreto, etichette) vs **regressione** (output continuo)
- Il semi-supervisionato **etichetta i dati non etichettati** partendo da pochi etichettati; il non supervisionato cerca **struttura** senza etichette; il rinforzo massimizza il **premio cumulativo** tramite interazione con l'ambiente
- **Overfitting**: ottimo sul training, non generalizza; tipico di modelli complessi (troppi parametri) su pochi dati. Rimedio indicato: modello a bassa complessità, **parsimonia**
- **Bias** = errore costante; **varianza** = variabilità dell'errore tra dataset. Al crescere della complessità bias² scende, varianza sale, errore totale a U con minimo alla complessità ottima
- Dati piccoli/semplici → bassa varianza; dati grandi/complessi → varianza più alta
- Presupposti del semi-supervisionato: **continuità**, **cluster**, **manifold**
- Il non supervisionato non ha un criterio specifico per **valutare le prestazioni**
- Tecniche non supervisionate: **clustering** e **riduzione della dimensionalità** (PCA, autoencoder); usi: preprocessing, rimozione del rumore, visualizzazione, analisi esplorativa
- Etichette rumorose/errate nel training peggiorano il modello: il "corretto" è definito solo dai dati di addestramento
