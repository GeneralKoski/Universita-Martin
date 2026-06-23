# Guida al Tema d'Esame: Punti c2.1 - c2.7

Questo documento riassume l'implementazione e la giustificazione teorica dei punti richiesti per il progetto sulla Percolazione (Modellazione e Simulazioni Numeriche).

---

## Punto c2.1: Tempo di esecuzione vs Taglia ($L$)

- **Cos'è:** Verificare come aumenta il tempo di calcolo all'aumentare delle dimensioni della griglia.
- **Cosa hai fatto:** Nello script `Test_Efficienza.m` (Subplot 1) hai fatto variare $L$ da 50 a 600.
- **Come spiegarlo:** _"Ho dimostrato che l'algoritmo HK ha una complessità lineare rispetto al numero di siti ($L^2$). Questo lo rende scalabile: posso analizzare sistemi molto grandi in pochi secondi, cosa impossibile col metodo ricorsivo."_

## Punto c2.2: Tempo di esecuzione vs Probabilità ($p$)

- **Cos'è:** Verificare se l'algoritmo rallenta quando il sistema diventa "difficale" (vicino alla soglia critica).
- **Cosa hai fatto:** Sempre in `Test_Efficienza.m` (Subplot 2) hai misurato il tempo fissando $L=400$ e variando $p$ da 0.1 a 0.9.
- **Come spiegarlo:** _"Questa è la forza di HK: il tempo di calcolo resta stabile anche vicino a $p \approx 0.59$. Il metodo classico invece rallenta perché lì i cluster diventano labirinti infiniti e la ricorsione fatica a gestirli."_

## Punto c2.3: Probabilità di Percolazione ($P_{perc}$)

- **Cos'è:** Tracciare la curva che mostra la probabilità di successo del sistema (Sigmoide).
- **Cosa hai fatto:** In `Analisi_Soglia_RACS.m` (Subplot 1 - verde) hai creato la curva "a S".
- **Come spiegarlo:** _"Ho individuato la transizione di fase. Grazie al campionamento infittito vicino a 0.59, ho mostrato che la curva cambia pendenza bruscamente, segnalando l'insorgenza della percolazione nel limite termodinamico."_

## Punto c2.4: Barre d'Errore (Errorbars)

- **Cos'è:** Dare un valore scientifico ai grafici aggiungendo l'incertezza statistica.
- **Cosa hai fatto:** In tutti i grafici hai usato la funzione `errorbar` calcolando $\frac{std(voti)}{\sqrt{N}}$.
- **Come spiegarlo:** _"Non ho plottato solo dei punti, ma delle stime statistiche. Usando il Teorema Limite Centrale, ho calcolato l'Errore Standard della Media. Più esperimenti ($N$) faccio, più queste barre diventano corte, rendendo la mia misura più precisa."_

## Punto c2.5: RACS (Reduced Average Cluster Size)

- **Cos'è:** Analizzare la taglia media dei cluster "piccoli" (quelli che non percolano).
- **Cosa hai fatto:** In `Analisi_Soglia_RACS.m` (Subplot 3 - magenta) hai calcolato la media scartando il cluster più grande.
- **Come spiegarlo:** _"Il RACS è l'indicatore più sensibile della soglia. Esattamente al valore critico, i cluster tendono a unirsi tutti insieme e la loro dimensione media 'esplode', creando un picco a forma di vulcano."_

## Punto c2.6: Massa del Cluster Gigante ($P_1$)

- **Cos'è:** Vedere quanto è grande fisicamente il raggruppamento principale.
- **Cosa hai fatto:** In `Analisi_Soglia_RACS.m` (Subplot 2 - blu) hai calcolato la frazione di siti occupati dal cluster massimo.
- **Come spiegarlo:** _"P1 è il mio parametro d'ordine. Prima della soglia è quasi zero; appena superata la soglia critica, cresce rapidamente perché il cluster gigante inizia a mangiare quasi tutti i siti attivi del reticolo."_

## Punto c2.7: Validazione tra algoritmi

- **Cos'è:** Dimostrare che il codice HK è corretto e dà gli stessi risultati del metodo standard.
- **Cosa hai fatto:** Hai creato lo script `Valida_HK.m` che confronta le matrici delle label di `HK.m` e `CercaCluster.m`.
- **Come spiegarlo:** _"Ho effettuato un test di validazione incrociata. Ho dato la stessa matrice casuale a entrambi gli algoritmi e ho verificato che identificassero esattamente gli stessi cluster. Questo garantisce che la velocità di HK non vada a scapito dell'accuratezza."_
