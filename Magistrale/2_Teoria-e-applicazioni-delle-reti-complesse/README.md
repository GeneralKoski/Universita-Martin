# Teoria e applicazioni delle reti complesse

**cod. 1014075** - 6 CFU, 48 ore - affine/integrativo, **esame a scelta** del 2° anno, primo semestre (a.a. 2026/27) - insegnamento in italiano.
**Docente:** Michele Bellingeri (michele.bellingeri@unipr.it), fisico, network science.
**Esame:** **progetto (50%)**, cioè l'analisi di un dataset di rete reale scelto dallo studente (anche in coppia) con un breve report, **+ orale (50%)** sul progetto e sui concetti. Conta più l'interpretazione dei risultati che lo strumento (Python/NetworkX o R/igraph). Le slide finora non parlano dell'esame.

Scelto al posto di Sicurezza e Informatica Forense (piano di studi compilato su Esse3 il 13/10/2026).

| Edizione | Elly | Corso | Stato |
|---|---|---|---|
| 2026/27 | elly2026 | [id 4989](https://elly2026.didattica.unipr.it/course/view.php?id=4989) | in corso, moduli 1-5 |

Iscrizione al corso Elly fatta il 18/10/2026, a corso già avviato (la prima slide è del 25/09). Nessuna edizione precedente scaricata.

## Struttura della cartella

- `2026-27/` - materiale Elly, una sottocartella per sezione

## Contenuti

Centralità, community detection, modelli di rete e robustezza. Niente laboratorio strutturato.

**Bibliografia** (dalla slide *Giorno 1*): Barabási - *Network Science*, Cambridge University Press 2016, gratis su networksciencebook.com (intuitivo, orientato alle applicazioni); Newman - *Networks: An Introduction*, Oxford University Press 2010 (più formale e rigoroso).

## Appelli 2026/27

Da Esse3 (via unidesk), letti il 19/10/2026. Tutti in stato "Inserito", iscrizioni non ancora aperte.

- gio 14/01/2027 ore 10:00 - orale - iscrizioni dal 15/12/2026 al 09/01/2027 **(sessione invernale)**
- gio 11/02/2027 ore 10:00 - orale - iscrizioni dal 12/01/2027 al 06/02/2027 **(sessione invernale)**
- lun 19/04/2027 ore 10:00 - orale - iscrizioni dal 20/03/2027 al 14/04/2027
- mar 08/06/2027 ore 10:00 - orale - iscrizioni dal 09/05/2027 al 03/06/2027
- mer 23/06/2027 ore 10:00 - orale - iscrizioni dal 24/05/2027 al 18/06/2027
- mer 14/07/2027 ore 10:00 - orale - iscrizioni dal 14/06/2027 al 09/07/2027
- ven 10/09/2027 ore 10:00 - orale - iscrizioni dal 11/08/2027 al 05/09/2027

---

## Edizione 2026/27 - Elly 4989

Scaricato il 18/10/2026 in `2026-27/`. Il docente tiene tutto in un'unica
sezione, che su Elly si chiama ancora "Nuova sezione": in locale è
`1_Materiale`. Niente registrazioni. Ricontrollato il 29/10/2026: il Modulo 5
è stato ricaricato dal docente il 22/10 (vedi sotto), il resto è identico (md5).

### 0 - Introduzione

- [forum] Annunci - https://elly2026.didattica.unipr.it/mod/forum/view.php?id=6341

Il docente usa gli annunci per assegnare le analisi da fare fra una lezione e
l'altra, sui dataset di https://networks.skewed.de (Python/NetworkX o R/igraph):

- 16/09/2026 - inizio del corso giovedì 24/09 alle 13:30, Aula B, Plesso di Matematica
- 28/09/2026 - rete [Karate](https://networks.skewed.de/net/karate): caricare l'edgelist, contare nodi e link, matrice di adiacenza, numero di link per nodo
- 01/10/2026 - sempre Karate: matrice di adiacenza, matrice di incidenza, distribuzione del grado; generare grafi casuali Erdős-Rényi con diversi N e probabilità di collegamento
- 05/10/2026 - Karate e grafo casuale: grado, betweenness e closeness di ogni nodo in una tabella; distanze (shortest path length) fra nodi
- 13/10/2026 - Karate e grafo casuale: PageRank e centralità degli autovettori
- 16/10/2026 - rete dei neuroni di C. elegans (https://networks.skewed.de/net/celegans_2019, sceglierne una): distanze binarie e pesate, diametro binario e pesato
- 22/10/2026 - niente prove intermedie nella LM Scienze Informatiche, quindi le lezioni del 3-6/11 non si fermano

### 1 - Materiale (su Elly "Nuova sezione")

Slide, nell'ordine del corso:

- `2026-27/1_Materiale/Giorno 1.pdf` (Giorno 1.pdf) - 12 pagine: i due libri di testo e i repository di dataset di reti (networkrepository.com, re3data), per lo più immagini
- `2026-27/1_Materiale/Modulo 1 - Introduzione.pdf` (Introduzione -Modulo 1.pdf) - 29 pagine
- `2026-27/1_Materiale/Breve Storia -Modulo 2.pdf` (Breve Storia -Modulo 2.pdf) - 36 pagine
- `2026-27/1_Materiale/Fondamenti Matematici - Modulo 3.pdf` (Fondamenti Matematici - Modulo 3.pdf) - 52 pagine
- `2026-27/1_Materiale/Centralità dei nodi - Modulo 4.pdf` (Centralità dei Nodi - Modulo 4.pdf) - 103 pagine
- `2026-27/1_Materiale/Proprietà Globali della Rete - Modulo 5.pdf` (Proprietà Globali della Rete - Modulo 5.pdf) - 131 pagine. Ricaricato dal docente il 22/10/2026 (prima erano 117): aggiunti il lemma della stretta di mano (somma dei gradi = 2m) e il grado medio, l'assortatività del grado spiegata come covarianza/Pearson con esempio numerico, e il coefficiente di clustering sviluppato (triangoli, transitività, clustering locale). Il riassunto `.md` è aggiornato alla nuova versione (29/10/2026)

Articoli scientifici:

- `2026-27/1_Materiale/Review Weighted Social Networks.pdf` (Bellingeri et al. 2023, Weighted Social Network.pdf) - review del docente sulle reti sociali pesate
- `2026-27/1_Materiale/Network Attack Manuscript.pdf` (Iyer et al. 2013, Attack Robustness and Centrality of Complex Networks.pdf) - robustezza agli attacchi e centralità
- `2026-27/1_Materiale/Recipe Similarity Network Manuscript.pdf` (The recipe similarity network a new algorithm to extract relevant information from cookbooks.pdf)
