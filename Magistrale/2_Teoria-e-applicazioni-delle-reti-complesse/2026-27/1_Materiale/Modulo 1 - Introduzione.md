# Modulo 1 - Introduzione

Fonte: `Modulo 1 - Introduzione.pdf`

Corso *Teoria e applicazioni delle reti complesse* (Network Science), prof. Michele Bellingeri, Università di Parma, A.A. 2026/2027, LM Scienze Informatiche, 6 CFU.

## Che cos'è una rete
- La **scienza delle reti** (network science) studia le **reti complesse**
- Una **rete** è composta da:
  - **nodi**: persone, luoghi, specie biologiche, computer, ...
  - connessi da **legami (link)**: relazioni, contatti, flussi di energia, strade, connessioni, ...
- Figura: piccolo grafo con nodi di quattro colori, a indicare che i nodi possono essere di tipo diverso

## Dai dati reali alla rete
- La rete è un **potente strumento per modellare sistemi complessi reali**
- Schema: **database** di dati grezzi → **pre-processing** → **rete** (grafo di nodi colorati e archi). La rete non è data già pronta: va costruita dai dati decidendo che cosa sono nodi e link (passo centrale anche per il progetto d'esame)

## Esempi di reti reali
Per ogni rete le slide indicano che cosa sono **nodi** e **link**.

| Rete | Nodi | Link |
|---|---|---|
| Sociale | individui | amicizia, contatto, lavoro, contagio |
| Sociale online (Facebook) | pagine | collegamento ipertestuale, "mi piace" reciproco |
| Ecologica (rete trofica) | specie | relazioni trofiche ("chi mangia cosa") |
| Comunicazione (e-mail) | impiegati | scambio di e-mail |
| Computer | router, PC | cavi |
| Interazione proteica | proteine | interazioni (le slide scrivono "metaboliche") |
| Regolazione genica | geni, fattori di trascrizione | relazioni di regolazione |
| Cerebrale | neuroni, aree cerebrali | sinapsi, fasci di fibre, connessioni anatomiche, attività elettrica |
| Stradale | incroci, paesi, città | strade |
| Aeroporti | aeroporti | voli, rotte |
| Treni | stazioni | collegamenti |
| Gastronomica (ingredienti) | ingredienti | molecole comuni |
| Gastronomica (ricette) | ricette | ingredienti comuni |
| Fotosintetica | cromofori | trasferimenti energetici |
| Epidemica | individui, computer, città, animali, aeroporti | contagio: interazioni sociali, contatto fisico, viaggi aerei, connessioni biologiche |
| Elettrica | centrali, sottostazioni, trasformatori, città, impianti rinnovabili | linee ad alta tensione, cavi elettrici |
| Finanziaria | banche, Stati, aziende, fondi di investimento, mercati, investitori | prestiti, esposizioni finanziarie, transazioni, debiti, partecipazioni azionarie |
| Batteri | batteri | co-occorrenza (in campioni, ambienti, ...) |
| Linguistica e semantica | parole | co-occorrenza, relazioni grammaticali, vicinanza nei testi, similarità |

### Reti sociali
- Descrivono le **interazioni sociali**: nodi = **individui**, link = **amicizia**, **contatto**, **lavoro**, **contagio**
- Figura: folla di omini collegati da linee (fonte pmrpressrelease.com, location-based social networking)

### Reti sociali online
- I **social network online** descrivono le interazioni sociali online
- **Rete complessa di Facebook**: nodi = **pagine**, link = **collegamento ipertestuale** oppure **"mi piace" reciproco**
- Figura: rete ramificata ad albero con nodi rosa e blu (fonte cs.uoi.gr)

### Reti ecologiche
- Le **reti trofiche** (food web) descrivono **"chi mangia cosa"** negli ecosistemi: nodi = **specie**, link = **relazioni trofiche**
- Figure: schema illustrato di una rete trofica (piante, insetti, rana, serpente, uccelli, volpe, aquila con frecce preda → predatore) e la **Quintessence Network** (DOI 10.1016/j.tree.2015.12.003), grafo circolare con le specie raggruppate per tipo lungo la circonferenza (insetti impollinatori, uccelli, roditori, ...)

### Reti di comunicazione
- Modellano le **attività di comunicazione** fra individui o entità
- **Reti di e-mail**: nodi = **impiegati**, link = **scambio di e-mail**
- Esempio: **Enron email network** (DOI 10.1038/srep01223), con un nucleo denso centrale e molti "ventagli" di nodi periferici attorno a pochi nodi

### Reti di computer
- Nodi = **router** e **PC**, link = **cavi**
- Figure: rete a stella attorno a un server; "Network Structure of the Internet" con tre domini collegati da router (DOI 10.5120/17765-8882); mappa di Internet come enorme nuvola colorata (newmedialab.cuny.edu)

### Reti di interazione proteica (PPI)
- Nodi = **proteine**, link = **interazioni** (le slide scrivono "interazioni metaboliche": nelle reti PPI i link sono in realtà interazioni **fisiche** fra proteine, cioè il loro legarsi; le interazioni metaboliche sono l'oggetto delle **reti metaboliche**, un'altra famiglia di reti biologiche)
- Figure: struttura 3D di un complesso proteico, due grandi reti PPI, schema di una cellula eucariote (fonte creative-proteomics.com)

### Reti di regolazione genica
- Nodi = **geni** e **fattori di trascrizione**, link = **relazioni di regolazione**
- Un gene o una proteina regolatrice **controlla l'espressione di un altro gene** (link orientati)
- Figure: due reti con nodi etichettati con nomi di geni (CD44, BIRC1, MTRR, ...) e forme/colori per tipo di nodo (fonte ese.wustl.edu)

### Reti cerebrali
- Nodi = **neuroni** o **aree cerebrali**; link = **sinapsi**, **fasci di fibre**, **connessioni anatomiche**, **attività elettrica**
- Ordini di grandezza: circa **86 miliardi di neuroni**, circa **$10^{14}$-$10^{15}$ connessioni sinaptiche**
- **Human Connectome**: figure di un cervello, di una rete fra regioni anatomiche (superior frontal, putamen, hippocampus, thalamus, precuneus, superior parietal, sinistra/destra) con archi di spessore proporzionale alla connessione (DOI 10.1523/JNEUROSCI.3539-11.2011) e del connettoma con nodi colorati per modulo
- Collegamento con le **reti neurali artificiali**: **McCulloch e Pitts (1943)** modellano il **neurone** come unità che riceve **diversi input** e produce **un output**. Figura: rete feed-forward con input layer, due hidden layer e output layer completamente connessi (fonte geeksforgeeks.org)

### Reti stradali
- Nodi = **incroci**, **paesi**, **città**; link = **strade**
- Figure: navigatore satellitare, mappa luminosa delle strade degli Stati Uniti, e due mappe dello stesso quartiere: a sinistra incroci (nodi blu) collegati lungo le strade, a destra una rete più astratta di nodi rossi con frecce (DOI 10.1007/978-3-031-15740-0_7). La stessa città dà reti diverse a seconda di come si scelgono nodi e link

### Rete degli aeroporti
- Nodi = **aeroporti**, link = **voli**, **rotte**
- Figure: mappa mondiale delle rotte con i grandi hub (Nord America, Europa, Asia orientale) e la rete degli aeroporti disegnata con colori per comunità, che ricalcano i continenti (DOI 10.59521/5E2DDEC9FAD4593B)

### Rete ferroviaria
- Nodi = **stazioni**, link = **collegamenti**
- Figura: mappa ferroviaria dei Paesi Bassi (*Spoorkaart van Nederland*) e la sua astrazione come grafo (networkpages.nl)

### Reti gastronomiche
- **Ingredienti**: nodi = **ingredienti**, link = **molecole (composti aromatici) comuni** (DOI 10.1038/srep00196). Figura: rete con nodi colorati per categoria (frutta, latticini, spezie, bevande alcoliche, frutta secca, pesce, carne, erbe, derivati vegetali, verdure, fiori, prodotti animali, piante, cereali), dimensione del nodo = **prevalenza** dell'ingrediente nelle ricette (1-50%), spessore del link = numero di **composti condivisi** (10-150)
- **Ricette**: nodi = **ricette**, link = **ingredienti comuni**, con un peso $w$ di similarità (DOI 10.1038/s41598-025-17189-6, Bellingeri et al., *The recipe similarity network*, cucina catalana; è il `Recipe Similarity Network Manuscript.pdf` di questa cartella). Figura:
  - A: rete con tutti i link $w > 0$, quasi completa
  - B: solo link con $w > 0{,}60$, molti nodi restano isolati
  - C: **componente connessa più grande** (LCC) con $w > 0{,}60$
  - D: una **7-clique** con $w > 0{,}60$ (nodi 3, 25, 26, 36, 41, 49, 55)
  - E: le ricette della clique: Allioli Sauce, Bean and Potato Stew, Mixed meat paella, Fairy rings mushrooms omelette, Monkfish Stew, Grilled Langoustines, Dry Salted Codfish Soup
  - Mostra come **filtrare i link per peso** (soglia) faccia emergere struttura

### Rete fotosintetica
- Nodi = **cromofori**, link = **trasferimenti energetici** (DOI 10.1098/rsif.2020.0813)
- Figura: pianta di pisello → schema della fotosintesi nella membrana del tilacoide (PSII, citocromo b6f, PSI, ATP sintasi) → struttura del **fotosistema I (PSI)** con i complessi antenna Lhca1-4 → rete orientata dei cromofori (clorofille CLA/CLB, carotenoidi CAR, clorofille "red", centro di reazione **P700**)

### Rete epidemica
- Nodi = **individui**, **computer**, **città**, **animali**, **aeroporti**; link = **contagio** tramite interazioni sociali, contatto fisico, viaggi aerei, connessioni biologiche
- Figura (a, b, c): persone che si spostano fra case, scuola, uffici e fabbrica in una città (a); rete **bipartita** persone-luoghi (b); rete di contatto fra persone che ne deriva (c)

### Vaccinazione come rimozione di nodi
- Vale per reti di contatti sociali, di interazioni animali, di computer
- **Rimozione di nodo** = **vaccinazione di individuo**
- Catena: vaccinazione di nodo → **rompe i canali di infezione** → **rallenta la diffusione epidemica**
- Figura (a-d): in una rete si rimuovono via via i nodi rossi (centrali, di collegamento); in (d) la rete si è spezzata in **due componenti separate**, quindi l'infezione non passa più dall'una all'altra. Anticipa i temi di **centralità** e **robustezza**

### Rete elettrica
- Nodi = **centrali elettriche**, **sottostazioni**, **trasformatori**, **città**, **impianti rinnovabili**; link = **linee ad alta tensione**, **cavi elettrici**
- Figure: schema della rete (generating station, transmission system, distribution system, load; fonte electrical4u.com) e una rete elettrica reale disegnata come grafo sulla mappa geografica, migliaia di nodi (DOI 10.1038/srep04949)

### Rete finanziaria
- Nodi = **banche**, **Stati**, **aziende**, **fondi di investimento**, **mercati**, **investitori**; link = **prestiti**, **esposizioni finanziarie**, **transazioni**, **debiti**, **partecipazioni azionarie**
- Figura: **rete finanziaria globale delle partecipazioni azionarie**, link orientati fra grandi istituti (Goldman Sachs, JP Morgan Chase, Deutsche Bank, Barclays, UBS, HSBC, Citigroup, Merrill Lynch, Generali, Mitsubishi UFJ, ...)

### Rete di batteri
- Nodi = **batteri**, link = **co-occorrenza** (nello stesso campione, ambiente, ecc.)
- Figura: rete con nodi colorati per phylum (Proteobacteria, Firmicutes, Verrucomicrobia, Archaea, Acidobacteria, Bacteroidetes, Gemmatimonadetes, Chloroflexi, Actinobacteria, Planctomycetes, altri)

### Reti linguistiche e semantiche
- Nodi = **parole**; link = **co-occorrenza**, **relazioni grammaticali**, **vicinanza nei testi**, **similarità**
- Rete linguistica: gli archi collegano parole che **compaiono vicine nel testo**
- Figura: *Co-Occurrence Network of Words* (Wikipedia, "Co-occurrence network") con 52 nodi e 112 archi (densità 0,084), colorati per comunità (modularity): parole come say, make, tell, come, teacher, school, house, ...

## Da ricordare
- Rete = **nodi** + **link**; il primo passo di ogni analisi è decidere, dai dati, **che cosa sono i nodi e che cosa sono i link** (pre-processing)
- Lo stesso schema astratto descrive sistemi molto diversi: sociali, online, ecologici, di comunicazione, tecnologici (computer, strade, aeroporti, treni, rete elettrica), biologici (proteine, geni, cervello, batteri, fotosintesi), economici, linguistici, gastronomici
- I link possono essere **orientati** (chi mangia chi, regolazione genica, e-mail, partecipazioni azionarie) o no, **pesati** (composti condivisi, similarità fra ricette, spessore delle connessioni cerebrali) o no, e le reti possono essere **bipartite** (persone-luoghi)
- Applicazione chiave: **rimuovere nodi** (vaccinare) spezza la rete in componenti e rallenta le epidemie
- Riferimenti dati nelle slide: Quintessence 10.1016/j.tree.2015.12.003; Enron 10.1038/srep01223; Internet 10.5120/17765-8882; connettoma 10.1523/JNEUROSCI.3539-11.2011; McCulloch e Pitts 1943; strade 10.1007/978-3-031-15740-0_7; aeroporti 10.59521/5E2DDEC9FAD4593B; ingredienti 10.1038/srep00196; ricette 10.1038/s41598-025-17189-6; fotosintesi 10.1098/rsif.2020.0813; rete elettrica 10.1038/srep04949
