# Simulatore Domande d'Esame (Semplificato)

Queste domande servono per prepararti alla discussione del progetto e alla teoria. Sono scritte in modo diretto per aiutarti a capire subito cosa chiede il professore.

---

### Statistica e Simulazione

1. **L'Autocorrelazione**: "Perché per le Code non usiamo l'errore standard normale ( std(X) / radice(N) )? In che modo l'autocorrelazione (fatto che un tempo dipende dal precedente) cambia il calcolo dell'errore?"
   - **Risposta:** Nelle code i dati non sono indipendenti: se la coda è piena ora, lo sarà probabilmente anche tra un secondo. Questo "legame" (autocorrelazione) rende il campione meno informativo. Usare la formula normale sottostimerebbe l'errore. Bisogna invece tener conto del "tempo di autocorrelazione" per capire quanti dati sono davvero indipendenti.

2. **Convergenza**: "Al crescere del numero di prove (N), perché l'errore nei grafici diventa più piccolo? Qual è il principio matematico che lo garantisce?"
   - **Risposta:** È merito del **Teorema del Limite Centrale**. L'errore sulla media diminuisce proporzionalmente a **1 / radice(N)**. Più simulazioni fai, più le fluttuazioni casuali si annullano a vicenda, facendo convergere il risultato verso il valore teorico vero.

---

### Percolazione (Teoria e Grafica)

3. **Griglia Infinita**: "Cosa succede alla forma della curva della probabilità (P_perc) se la griglia fosse infinita? Perché somiglierebbe a un 'gradino' (Funzione di Heaviside)?"
   - **Risposta:** In un sistema infinito, la transizione è istantanea: o non si passa (0) o si passa (1). Non ci sono vie di mezzo. Questo salto netto avviene esattamente alla soglia critica. Nei sistemi finiti (come il tuo 100x100) la curva è più morbida a causa degli "effetti di bordo" (Finite-size scaling).

4. **Il RACS**: "Che cos'è il RACS e perché è diverso dalla semplice media dei cluster? Cosa succede a questa formula proprio sulla soglia di percolazione (Pc)?"
   - **Risposta:** Il RACS è la media della taglia dei cluster **escludendo** quello gigante. Se non lo escludessimo, la media ci direbbe solo quanto è grande il cluster gigante. Escludendolo, possiamo vedere come gli altri cluster crescono e "esplodono" (il vulcano) proprio vicino alla soglia, prima di unirsi tutti insieme.

5. **Percolazione in 3D**: "Se usassimo un cubo invece di una griglia piatta, la soglia di percolazione sarebbe più alta o più bassa? Perché?"
   - **Risposta:** È molto **più bassa** (circa 31% invece di 59%). Questo succede perché in 3D ogni cella ha più vicini (6 invece di 4) e quindi ci sono molte più "strade" possibili per aggirare gli ostacoli e connettere il sistema.

---

### Code e Algoritmi

6. **Coda Infinita**: "Perché in una coda dove arrivano troppi clienti (sala d'attesa infinita) non è possibile trovare un equilibrio stabile?"
   - **Risposta:** Perché se il tasso di arrivo (lambda) è maggiore o uguale a quello di servizio, il sistema non riesce mai a smaltire i clienti. La coda cresce all'infinito e la media matematica del numero di persone non esiste (il sistema "esplode"). Il parametro di traffico **rho** deve essere < 1 per avere stabilità.

7. **Arrivi Costanti vs Poisson**: "Qual è la differenza nei tempi di attesa se i clienti arrivano a intervalli regolari (costanti) invece che a caso (Poisson)?"
   - **Risposta:** Con arrivi costanti i tempi di attesa sono **minori**. La casualità (Poisson) introduce varianza: a volte arrivano tanti clienti insieme creando picchi di coda, anche se la media degli arrivi è la stessa. Meno varianza c'è, più la coda è efficiente.

8. **Algoritmo Hoshen-Kopelman (HK)**: "Perché l'algoritmo HK è così veloce? Perché non ha bisogno di guardare avanti (destra e basso) per trovare tutti i cluster correttamente?"
   - **Risposta:** HK è veloce perché legge la griglia una sola volta (scansione lineare). Non guarda avanti perché usa la struttura **Union-Find**: assegna etichette provvisorie e, se scopre più avanti che due cluster sono in realtà lo stesso, li unisce virtualmente "cambiando nome" in una tabella separata, senza dover tornare indietro a ricolorare la griglia.
