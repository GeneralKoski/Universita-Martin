# Giorno 1: testi, strumenti e dataset di reti

Fonte: `Giorno 1.pdf`

Contatto del docente: **Michele Bellingeri**, michele.bellingeri@unipr.it

## Libri di testo
- **Barabási, A.-L. (2016). *Network Science*. Cambridge University Press**. Gratuito su **networksciencebook.com**: trattazione **intuitiva e visuale**, orientata alle applicazioni. Screenshot del sito con l'indice: Personal Introduction, 1. Introduction, 2. Graph Theory, 3. Random Networks, 4. The Scale-Free Property, 5. The Barabási-Albert Model, 6. Evolving Networks, 7. Degree Correlations, 8. Network Robustness, 9. Communities, 10. Spreading Phenomena, Preface; disponibile in inglese, russo, ungherese, persiano, giapponese
- **Newman, M. (2010). *Networks: An Introduction*. Oxford University Press**, DOI 10.1093/acprof:oso/9780199206650.001.0001: trattazione **più formale e matematicamente rigorosa**. (Lo screenshot IBS mostra però la **seconda edizione**, *Networks*, OUP 2018, a 91,44 euro; il DOI citato è quello della prima edizione del 2010.)
- **Barabási, *LINK. La nuova scienza delle reti***, Einaudi / Le Scienze, 2008: libro divulgativo in italiano (screenshot di un annuncio usato a 10 euro)

## Software
- **R** (The R Project for Statistical Computing, download da CRAN; screenshot con R 4.6.1 "Happy Hop" del 24/06/2026) e **Python** (python.org, Python 3.14.7): i due ambienti per il progetto (NetworkX in Python, igraph in R)

## Repository di dataset di reti

### Network Repository (networkrepository.com)
- Primo repository **interattivo** di grafi: oltre a scaricare i dati (**Get network data**) permette di **confrontare** (**Compare graph data**) e **visualizzare** (**Visualize networks**) le reti nel browser
- Scheda su **re3data.org** (r3d100011340): "Network Data Repository, Graph Data, Social Networks"; centinaia di reti reali e dataset di benchmark; discipline: scienze della vita, sociali, biologia, informatica, fisica, matematica, scienze umane, ingegneria, scienze naturali
- Collezioni con il numero di reti (dallo screenshot):

| Collezione | N. | Collezione | N. | Collezione | N. |
|---|---|---|---|---|---|
| Animal social | 816 | Interaction | 29 | Scientific computing | 11 |
| Biological | 37 | Infrastructure | 8 | Social | 77 |
| Brain | 116 | Labeled | 105 | Facebook | 114 |
| Collaboration | 20 | Massive network data | 21 | Technological | 12 |
| Cheminformatics | 646 | Miscellaneous | 2669 | Web graphs | 36 |
| Citation | 4 | Power | 8 | Dynamic | 115 |
| Ecology | 6 | Proximity | 13 | Temporal reachability | 38 |
| Economic | 16 | Generated graphs | 221 | BHOSLIB | 36 |
| Email | 6 | Recommendation | 36 | DIMACS | 78 |
| Graph 500 | 8 | Road | 15 | DIMACS10 | 84 |
| Heterogeneous | 15 | Retweet | 34 | Non-relational ML data | 211 |

### SNAP - Stanford Large Network Dataset Collection (Jure Leskovec)
- Categorie: **social** (interazioni fra persone), **ground-truth communities**, **communication** (email), **citation** (articoli → citazioni), **collaboration** (co-autori), **web graphs** (pagine e hyperlink), **Amazon** (co-acquisti), **Internet** (computer), **road** (incroci e strade), **autonomous systems**, **signed** (archi positivi/negativi, amico/nemico, fiducia/sfiducia), **location-based** (check-in geografici), **Wikipedia** (talk, editing, voti), **temporal** (archi con timestamp), **Twitter e Memetracker** (467 milioni di tweet), **online communities** (Reddit, Flickr), **online reviews** (BeerAdvocate, Amazon), **user actions**, **face-to-face**, **graph classification**, **computer communication**, **cryptocurrency transactions**, **telecom**
- Le reti SNAP sono anche nella SuiteSparse Matrix Collection (Tim Davis)
- Tabella **Social networks** (tipo, nodi, archi):

| Nome | Tipo | Nodi | Archi | Descrizione |
|---|---|---|---|---|
| ego-Facebook | Undirected | 4.039 | 88.234 | cerchie sociali Facebook (anonimizzate) |
| ego-Gplus | Directed | 107.614 | 13.673.453 | cerchie Google+ |
| ego-Twitter | Directed | 81.306 | 1.768.149 | cerchie Twitter |
| soc-Epinions1 | Directed | 75.879 | 508.837 | chi si fida di chi su Epinions.com |
| soc-LiveJournal1 | Directed | 4.847.571 | 68.993.773 | social LiveJournal |
| soc-Pokec | Directed | 1.632.803 | 30.622.564 | social Pokec |
| soc-Slashdot0811 / 0922 | Directed | 77.360 / 82.168 | 905.468 / 948.464 | Slashdot, nov 2008 / feb 2009 |
| wiki-Vote | Directed | 7.115 | 103.689 | chi vota chi su Wikipedia |
| wiki-RfA | Directed, signed | 10.835 | 159.388 | richieste di adminship Wikipedia (con testo) |
| gemsec-Deezer / -Facebook | Undirected | 143.884 / 134.833 | 846.915 / 1.380.293 | dataset Gemsec |
| soc-RedditHyperlinks | Directed, signed, temporal, attributed | 55.863 | 858.490 | hyperlink fra subreddit |
| soc-sign-bitcoin-otc / -alpha | Weighted, signed, directed, temporal | 5.881 / 3.783 | 35.592 / 24.186 | rete di fiducia Bitcoin |
| comm-f2f-Resistance | Weighted, directed, temporal | 451 | 3.126.993 | interazioni faccia a faccia dinamiche |
| musae-twitch | Undirected | 34.118 | 429.113 | utenti Twitch |
| musae-facebook | Undirected | 22.470 | 171.002 | rete pagina-pagina Facebook |

- Esempio di scheda: **Social circles: Facebook** (ego-Facebook). Cerchie ("friends lists") raccolte con un'app Facebook da partecipanti a un sondaggio; contiene feature dei nodi (profili), cerchie ed ego-network. **Anonimizzato**: id sostituiti e feature oscurate (es. "political=anonymized feature 1"), si sa se due utenti hanno la stessa affiliazione ma non quale
  - Statistiche: **4039 nodi**, **88234 archi**, componente debolmente/fortemente connessa più grande = tutta la rete (1.000), **clustering medio 0,6055**, **1.612.010 triangoli**, frazione di triangoli chiusi 0,2647, **diametro 8**, diametro effettivo al 90° percentile 4,7 (statistiche calcolate unendo le ego-network, ego compresi)
  - Citazione: **J. McAuley, J. Leskovec, "Learning to Discover Social Circles in Ego Networks", NIPS 2012**
  - File: `facebook.tar.gz` (10 reti anonimizzate), `facebook_combined.txt.gz` (archi di tutte le egonet unite), `readme-Ego.txt`

### Netzschleuder (networks.skewed.de)
- "Network catalogue, repository and centrifuge": tabella ordinabile con, per ogni rete, nodi, archi e statistiche: $\langle k \rangle$, $\sigma_k$, $\lambda_h$, $\tau$, $r$, $c$, $\oslash$, $S$, tipo (**Directed/Undirected**), modo (**Unipartite/Bipartite**), $n$ (numero di reti nel dataset) e tag. (Aggiunta, dalla legenda del sito: $\langle k \rangle$ grado medio, $\sigma_k$ deviazione standard del grado, $\lambda_h$ autovalore massimo della matrice non-backtracking, $\tau$ tempo di mescolamento del random walk, $r$ assortatività di grado, $c$ clustering globale, $\oslash$ diametro, $S$ frazione di nodi nella componente più grande.)
- Righe mostrate: 7th_graders (29 nodi, 740 archi), academia_edu (200.169 / 1.398.063, directed), add_health (2.587 / 12.969, 84 reti, pesata), adjnoun (adiacenze di parole in *David Copperfield*, 112 / 425, undirected), advogato (rete di fiducia 2009, 6.541 / 51.127, pesata), amazon_copurchases (410.236 / 3.356.824), amazon_ratings (3.376.972 / 5.838.041, **bipartita**, pesata, con timestamp), ambassador (attentato all'ambasciatore filippino 2000, 16 / 19, temporale), anybeat (12.645 / 67.053), arxiv_authors (133.280 / 396.160, collaborazioni, proiezione)
- Esempio di scheda: **7th_graders - Vickers 7th Graders (1981)**: piccola rete **multiplex** di amicizie fra **29 studenti** di una classe di 7th grade a Victoria (Australia). Ogni studente nomina compagni per tre attività (con chi vai d'accordo, migliori amici, con chi preferisci lavorare); la direzione dell'arco indica che i ha nominato j, il peso la frequenza della nomina. Studenti 1-12 maschi, 13-29 femmine. Citazione: M. Vickers, S. Chan, "Representing Classroom Social Structure", Victoria Institute of Secondary Education, 1981. Statistiche: $\langle k \rangle$ = 25,52, $r$ = -0,01, $c$ = 0,76, diametro 2, directed, unipartita, proprietà dei nodi `name`, degli archi `weight` e `layer`. Si carica con graph-tool (`gt.collection.ns["7th_graders"]`) o si scarica in formato gt, GraphML, GML, csv

## Per la scelta del dataset del progetto
(Aggiunta, ricavata dai contenuti delle slide.)
- Partire dai tre repository: **Network Repository**, **SNAP**, **Netzschleuder**; le schede danno già nodi, archi, tipo e la citazione da riportare nel report
- Decidere subito le caratteristiche che condizionano l'analisi: **orientata o no**, **pesata o no**, **unipartita o bipartita**, **statica o temporale**, **signed**
- Taglia gestibile con NetworkX/igraph: da qualche centinaio a qualche decina di migliaia di nodi (es. ego-Facebook, 4039 nodi); le reti da milioni di nodi (LiveJournal, Pokec) sono pesanti per centralità e community detection
- Preferire reti con metadati sui nodi (es. sesso in 7th_graders, cerchie in ego-Facebook): permettono di interpretare i risultati, che all'esame conta più dello strumento
