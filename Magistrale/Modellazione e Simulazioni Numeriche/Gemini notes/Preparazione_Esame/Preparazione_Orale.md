## Domanda 1: Perché l'algoritmo Hoshen-Kopelman non controlla mai i nodi a destra e in basso?

L'algoritmo legge la griglia come un libro, da sinistra a destra e dall'alto verso il basso. Controlla solo le celle sopra e a sinistra perché sono quelle dove è già passato e di cui conosce il risultato. Non serve guardare "nel futuro" (a destra o in basso) perché quelle celle verranno analizzate nei passaggi successivi. Se due pezzi di un cluster si devono unire, la funzione Union-Find li collega cambiando semplicemente il loro "nome", senza dover tornare indietro a ricalcolare tutto.

> **📂 Riferimento Relazione:** Sezione 2 (Ottimizzazione Architetturale). Spiega come la scansione "Raster" e la Parent List rendano il calcolo lineare O(N).

---

## Domanda 2: RACS: Perché togliamo il cluster gigante (s_max) dal calcolo? Cos'è quel picco nel grafico?

Togliamo il cluster più grande (s_max) perché, vicino alla soglia di percolazione, diventa così enorme che coprirebbe tutti gli altri cluster piccoli, rendendo il calcolo del RACS inutile. Il "picco" che vediamo nel grafico (chiamato a volte vulcano) rappresenta il momento in cui i cluster diventano molto grandi e iniziano a toccarsi, proprio prima di unirsi tutti insieme nel cluster gigante finale.

> **📂 Riferimento Relazione:** Sezione 3 (Suscettibilità di Transizione RACS) e Figura 2 (Pannello 3). Il "Vulcano Termodinamico" è la prova visiva della soglia critica.

---

## Domanda 3: Differenza tra reticoli piccoli e il Teorema Infinito (Heaviside). Cosa sono gli effetti di bordo?

In teoria, su una griglia infinita, la percolazione avviene all'improvviso come un interruttore (Funzione di Heaviside). Nei nostri computer, però, usiamo griglie piccole e finite. Questo crea degli "effetti di bordo": la curva non è un gradino netto ma una "S" più morbida. Questo effetto si chiama Finite-size Scaling e succede perché i confini della griglia influenzano il cammino dei cluster.

> **📂 Riferimento Relazione:** Sezione 4.1 (Finite-Size Scaling) e Figura 2 (Pannello 1). Nota come la curva non sia un angolo retto ma una sigmoide smussata.

---

## Domanda 4: Hai usato Autocorrelazioni temporali nei tuoi campionamenti?

No, non è stato necessario. Invece di seguire un processo che cambia nel tempo (dove ogni passaggio dipende dal precedente), ho creato ogni simulazione da zero in modo indipendente usando il metodo Monte Carlo. Avendo fatto 1000 simulazioni tutte diverse tra loro, la statistica è pulita e possiamo calcolare l'errore semplicemente dividendo per la radice del numero di prove ( s / radice(N) ).

> **📂 Riferimento Relazione:** Sezione 4.2 (Indipendenza Aleatoria). Spiega perché hai potuto usare il Teorema del Limite Centrale (CLT) senza preoccuparti dei tempi di correlazione.

---

## Domanda 5: Cosa succede se usiamo un cubo (3D) invece di una griglia piatta (2D)?

In 3D la percolazione avviene molto prima. In una griglia piatta (2D) la soglia è circa al 59%, mentre in un cubo (3D) scende al 31%. Questo succede perché in tre dimensioni ci sono molte più strade possibili (6 direzioni invece di 4) per collegare i nodi e creare un cammino continuo.

---

## Domanda 6: Se cambiassimo la forma della griglia (triangoli o esagoni), cambierebbe tutto?"

Cambierebbe solo il numero preciso della soglia (il punto in cui inizia la percolazione). Per tutto il resto, le leggi fisiche e la forma delle curve rimarrebbero identiche. Questo concetto si chiama 'Universalità': non importa la forma della singola cella, se siamo in 2D il comportamento generale del sistema segue le stesse identiche regole matematiche.

---

## Domanda 7: Questa è Percolazione di Siti o di Legami? Qual è la differenza?"

Noi abbiamo studiato la Percolazione di Siti (Site Percolation), dove decidiamo se "accendere" o "spegnere" i singoli quadratini. Nella Percolazione di Legami (Bond Percolation), invece, i quadratini sono fissi e decidiamo se collegarli tra loro con dei ponti. La differenza principale è matematica: nella percolazione di legami in 2D, la soglia critica è esattamente allo 0.5, un numero molto elegante e preciso.

---

## Domanda 8: Che forma ha il cluster gigante proprio sulla soglia critica Pc?

Sulla soglia critica, il cluster gigante non è una macchia piena e solida. È un "Frattale": un oggetto sfilacciato e pieno di buchi a ogni scala di ingrandimento. La sua dimensione non è un numero intero (come 2 per un’area), ma è circa 1.89. Significa che è più di una linea ma meno di una superficie piena.

---

## Domanda 9: Come si collega la percolazione al cammino casuale (Random Walk)?

Se immaginiamo una formica che si muove a caso sulla griglia, la percolazione decide dove può andare. Sotto la soglia, la formica resta bloccata in piccole isole e non va lontano. Sopra la soglia, trova un cammino infinito e può attraversare tutto lo spazio. Proprio sulla soglia, invece, la formica finisce spesso in "vicoli ciechi" (Dead Ends) e ci mette tantissimo tempo a muoversi. Questo fenomeno si chiama "Diffusione Anomala".

---

## Domanda 10: Senza supercomputer, come si calcola la soglia esatta per una griglia infinita?

Si usa una tecnica chiamata 'Gruppo di Rinormalizzazione'. In pratica, si rimpicciolisce la griglia unendo i quadratini in blocchi più grandi (Macro-Pixel) e si guarda come cambia la probabilità. Se rimpicciolendo la griglia la probabilità non cambia (Punto Fisso), allora abbiamo trovato l'esatta soglia di percolazione teorica per una griglia infinita.

---

## Domanda 11: Qual è la differenza tra Probabilità di Percolazione e Parametro d'Ordine P1?

La Probabilità di Percolazione ci dice solo SE esiste un cammino che attraversa la griglia (un "Sì" o "No"). Il Parametro d'Ordine P1 (p_1), invece, ci dice QUANTO è grande quel cammino rispetto a tutta la griglia. Uno ci dice se abbiamo vinto, l'altro ci dice quanto è grande il premio (quanta massa è nel cluster gigante).

> **📂 Riferimento Relazione:** Figura 2. Il Pannello 1 mostra la probabilità (0 o 1), il Pannello 2 mostra la crescita della massa P1.

---

## Domanda 12: In MATLAB hai usato dei cicli 'For' per creare la griglia?

No, sarebbe stato troppo lento. Ho usato la "vettorializzazione": ho creato tutta la matrice di numeri casuali in un colpo solo e l'ho confrontata direttamente con la probabilità scelta. In codice si scrive `reticolo = rand(N) < p`. Questo rende il codice molto più veloce perché evita di controllare le celle una per una con un ciclo lento.

> **📂 Riferimento Relazione:** Sezione 2. Cita la comparazione dei tempi tra l'approccio a pila e lo schema Union-Find (Figura 1).

---

## Domanda 13: Come controlli se un cluster attraversa davvero la griglia da parte a parte?

Dopo aver trovato tutti i cluster, chiedo al computer di fare un confronto: prendo l'elenco dei nomi (etichette) dei cluster sulla prima riga e quello dell'ultima riga. Se c'è almeno un "nome" presente in entrambi gli elenchi, significa che quel cluster tocca sia l'inizio che la fine, quindi ha percolato.
