# INGSW-2425-T4-A
Progetto 4 – Gioco cooperativo per la gestione di una città
## Descrizione generale:
Lo scopo è sviluppare un gioco simile a quelli già esistenti che permettono di costruire e gestire città.
La componente cooperativa del gioco si esprime nel fatto che ogni giocatore può controllare solo un determinato aspetto della amministrazione cittadina.
Ogni giocatore ha quindi assegnato un determinato assessorato. Esempi di assessorato sono: assessorato per la riscossione delle tasse e la ripartizione degli introiti agli altri assessorati. Assessorato per la creazione e gestione delle strade. Assessorato all’urbanistica che decide la destinazione d’uso di ogni area. L’assessorato alle attività commerciali che decide quali attività commerciali aprire. L’assessorato allo spettacolo che decide quali struttura creare per lo spettacoli e indice spettacoli. L’assessorato allo sport, simile a quello per lo spettacolo. Etc…
Lo scopo finale è costruire ed evolvere una città con la massima felicità dei suoi cittadini. La misura della felicità è lasciata 
## Requisiti minimi:
- Una Docker per il lato server
- Gestione degli utenti: login e loro informazioni (non sensibili)
- Invito ad amici per partecipare ad una partita
- I giocatori possono giocare in modo asincrono. La partita quindi rimane attiva anche se non ci sono giocatori che stanno giocando. Viene distrutta solo con il consenso di tutti i giocatori o dopo un determinato periodo di inattività.
- Interfaccia per la creazione manuale di nuove mappe da caricare sul server e mettere a disposizione degli altri giocatori
