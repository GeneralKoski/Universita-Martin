# Testo da esporre: TVL (Simon, King, Howe)

Seminario di Analisi statica e verifica del software, durata massima 15 minuti. Il testo è lo stesso delle note del relatore in `presentazione-TVL.pptx`; i tempi sono indicativi (circa 130 parole al minuto).

## Slide 1 - Two Variables per Linear Inequality as an Abstract Domain (0:45)

Buongiorno. Presento il paper "Two Variables per Linear Inequality as an Abstract Domain", di Axel Simon, Andy King e Jacob Howe.

Si inserisce nel tema che abbiamo visto a lezione: i domini numerici per l'interpretazione astratta. Il problema di fondo è sempre lo stesso: quanta precisione posso avere e quanto costa.

Il paper propone un dominio di disuguaglianze con al massimo due variabili e coefficienti qualsiasi, e mostra che tutte le operazioni richieste da un'analisi diventano polinomiali.

In quindici minuti vi mostro l'idea chiave, la completion, e come da lì discendono le altre operazioni.

## Slide 2 - Precisione contro trattabilità (1:15)

Parto dal compromesso tra precisione e trattabilità.

A sinistra gli intervalli: un vincolo per variabile, operazioni velocissime, ma nessuna relazione tra variabili.

A destra i poliedri: esprimono qualsiasi relazione lineare, ma il join richiede un algoritmo come quello di Chernikova, con costo esponenziale nel caso peggiore.

In mezzo c'è il dominio degli Octagon di Miné: disuguaglianze con due variabili, ma coefficienti solo meno uno, zero o più uno. Si rappresentano con una matrice di differenze di dimensione 2d per 2d, e la chiusura costa O(d al cubo) con Floyd-Warshall.

Il paper si mette tra Octagon e poliedri: stesso numero di variabili per disuguaglianza, ma coefficienti reali qualsiasi, senza perdere trattabilità. È lo stesso filo conduttore dei domini numerici visti a lezione.

## Slide 3 - Il dominio (1:30)

Ecco il dominio. Un elemento è un insieme finito di disuguaglianze a x più b y minore o uguale a c, ognuna con al più due variabili. L'ordine è l'entailment.

Con questo ordine ottengo un reticolo, ma non completo. Il meet è l'unione dei sistemi. Il join è la chiusura topologica dell'inviluppo convesso dell'unione.

Perché serve la chiusura? Lo mostra l'Esempio 1 del paper, a destra. T1 è il solo punto (0,1). T2 è la semiretta y uguale x, con x maggiore o uguale a zero. L'inviluppo convesso contiene il punto (0,1) ma non la semiretta y uguale x più uno: l'insieme non è chiuso, e un sistema di disuguaglianze non strette descrive solo insiemi chiusi. Quindi prendo la chiusura.

Una nota importante: non esiste la funzione α. Un cerchio non ha una migliore approssimazione con un numero finito di disuguaglianze, mentre negli Octagon ogni oggetto planare ha al massimo otto disuguaglianze. Si lavora quindi solo con la concretizzazione γ.

## Slide 4 - Forma completa (1:30)

L'idea chiave è la forma completa. Definisco la restrizione di un sistema a un insieme di variabili Y: tengo solo le disuguaglianze che usano soltanto variabili di Y.

Un sistema è completo se ogni sua conseguenza t è già implicata dalle sue disuguaglianze sulle sole variabili di t, quindi su una o due variabili.

Esempio a sinistra: da y minore o uguale a x e x minore o uguale a z segue y minore o uguale a z. In un sistema non completo questa relazione è nascosta; in uno completo è scritta esplicitamente.

La Proposizione 1 dice che ogni sistema ha una forma completa equivalente: basta aggiungere le proiezioni su tutte le coppie di variabili.

Il messaggio è questo: dopo la completion ragionare sul sistema intero equivale a ragionare coppia per coppia. È l'analogo della chiusura negli Octagon, con la differenza che i coefficienti sono qualsiasi.

## Slide 5 - Come si calcola la completion (2:00)

Come si calcola la completion? Il paper osserva che l'algoritmo esiste già: è dentro l'algoritmo di Nelson del 1978 per la soddisfacibilità. Ha due ingredienti.

Il primo è result: date due disuguaglianze con una variabile in comune, con coefficiente positivo in una e negativo nell'altra, elimino quella variabile. Per esempio da 2x più y minore o uguale a 4 e meno x più 3z minore o uguale a 1: moltiplico la seconda per due e sommo, e ottengo y più 6z minore o uguale a 6.

Il secondo ingrediente è filter: ordina per angolo le disuguaglianze di una coppia di variabili e toglie le ridondanti, in tempo lineare, usando il controllo di entailment fra tre disuguaglianze.

Quante volte ripeto? Il Lemma 1 dice che una iterazione di result dimezza il numero di variabili necessarie per ottenere una conseguenza. Bastano quindi circa log in base due del numero di variabili iterazioni.

A destra l'Esempio 2: una catena x0 minore o uguale a x1, fino a x4. La prima iterazione crea le relazioni a distanza due, la seconda quelle a distanza tre e quattro, e poi ho un punto fisso.

Con due iterazioni in più la completion rende esplicite anche le disuguaglianze su una sola variabile e rileva l'insoddisfacibilità, come nell'Esempio 3 del paper, dove si arriva a 0 minore o uguale a meno 24.

La complessità è O(k² d³ log d (log k + log d)), con k numero di disuguaglianze per proiezione.

## Slide 6 - Proiezione ed entailment (1:00)

Una volta completo il sistema, le altre operazioni diventano semplici.

La proiezione: per eliminare x basta togliere tutte le disuguaglianze che contengono x, senza Fourier-Motzkin, perché la completion ha già reso esplicite le conseguenze. Nell'esempio, da y minore o uguale a x e x minore o uguale a z resta y minore o uguale a z.

L'entailment: T primo implica T se e solo se l'implicazione vale su ogni proiezione a due variabili, è la Proposizione 7. Sul piano, con le disuguaglianze ordinate per angolo, il controllo è lineare. Il caso base, tre disuguaglianze, si risolve in tempo costante con la regola di Cramer: cerco una combinazione delle prime due con la stessa pendenza della terza e confronto le costanti.

## Slide 7 - Join: inviluppo convesso planare (2:00)

Il pezzo originale del paper è il join. Il join è l'inviluppo convesso, che nei poliedri generici richiede l'algoritmo di Chernikova con rappresentazione per vertici e raggi, potenzialmente esponenziale.

Qui, grazie alla completion, lo calcolo proiezione per proiezione. Le Proposizioni 4 e 5 dicono che il risultato è completo e coincide con l'inviluppo convesso nello spazio intero.

Ogni proiezione è un poliedro planare, e per quello l'algoritmo ha tre passi.

Primo, extreme: dalle disuguaglianze ordinate per angolo ricavo vertici e raggi. I raggi sono al massimo quattro per poliedro.

Secondo, applico Graham scan. I raggi si trattano traslando i vertici lungo il raggio, fuori da un quadrato che contiene tutti i vertici, e si calcola l'inviluppo di tutti i punti.

Terzo, connect: ogni coppia di vertici adiacenti sul bordo dell'inviluppo diventa una disuguaglianza.

Il costo è dominato da Graham, O(n log n). Gli autori scrivono che, per quanto ne sanno, un algoritmo di inviluppo convesso per poliedri planari fatto così non è presente in letteratura.

## Slide 8 - Widening (1:30)

Il widening. Per la terminazione si può usare un qualsiasi widening dei poliedri, applicato alle proiezioni. Per perdere meno precisione conviene ritardarlo e applicarlo quando numero e dimensione delle proiezioni si sono stabilizzati.

C'è una sottigliezza: applicare la completion dopo il widening può reintrodurre le disuguaglianze appena tolte e compromettere la terminazione.

Poi c'è il widening per la trattabilità: limito a una costante il numero di disuguaglianze per proiezione, scartando quella che contribuisce al lato più corto del poliedro. Così la rappresentazione è O(d al quadrato) come le DBM, e la completion costa O(d al cubo per log d al quadrato), contro O(d al cubo) degli Octagon, ma con coefficienti qualsiasi.

## Slide 9 - Evidenza empirica (1:15)

Ma limitare k fa perdere molta precisione? Gli autori hanno implementato una completion ingenua e l'hanno provata su poliedri planari casuali, in tre scenari: varying, constant e sparse.

La completion aumenta il numero di proiezioni del 56, del 123 e del 9 per cento. Meno dello 0,3 per cento delle proiezioni ha più di trenta disuguaglianze.

La spiegazione è probabilistica: l'inviluppo convesso di n punti casuali in un quadrato ha in media O(log n) punti estremi, quindi il numero di disuguaglianze non cresce con n.

Dico onestamente il limite: i dati sono casuali, non vengono da programmi reali, e non c'è un confronto dei tempi con gli Octagon.

## Slide 10 - Confronto con gli Octagon e limiti (1:00)

Riassumo il confronto con gli Octagon. Il TVL toglie il vincolo sui coefficienti a un costo di poco superiore: O(d al cubo per log d al quadrato) contro O(d al cubo). La rappresentazione è densa: occupa spazio solo per le disuguaglianze presenti, invece di una matrice 2d per 2d.

I limiti: non c'è α; il dominio è definito sui reali; le prove sono su dati casuali e non c'è un tool di analisi.

Nell'introduzione gli autori citano applicazioni dei domini a due variabili: verifica di programmi, automi temporizzati, parallelizzazione, vulnerabilità di sicurezza, memory leak, terminazione di programmi logici.

## Slide 11 - Conclusioni (0:30)

Concludo. Un'unica operazione, la completion, rende meet, join, proiezione ed entailment polinomiali e semplici da implementare, quindi meno soggette a errori.

Rispetto agli Octagon si tolgono i coefficienti unitari senza perdere la trattabilità.

Grazie, sono a disposizione per le domande.

## Note

- **Durata**: il testo conta circa 1400 parole, cioè circa 11 minuti a 130 parole al minuto e circa 14 a 100. Se vai lento, taglia dalla slide 9 e dalla 10, non dalla 5 e dalla 7. Prova a leggerlo ad alta voce con un cronometro almeno una volta.
- **Figure**: i disegni delle slide 3, 4 e 7 sono schemi fatti da me a partire dal testo del paper (Esempio 1 e descrizione del join). Non ho visto le figure del PDF: confrontale con il paper prima di presentare.
- **Esempio 3 del paper**: il testo dice che T1 aggiunge `-y ≤ -2`, `-5x ≤ -9` e `x ≤ -3`. A mano trovo anche `y ≤ -4` (da `4x - 2y ≤ -4` e `-x + y ≤ -1`), che non è elencata. Non cambia la conclusione (si arriva comunque a `0 ≤ -24`), ma se lo racconti alla lavagna usa solo i tre risultati del paper e non dire che T1 è l'insieme completo dei risultanti.
- **Verifica**: non ho potuto renderizzare le slide (LibreOffice senza Impress in questo ambiente). Ho controllato con le metriche dei font che il testo entri nei riquadri, ma apri il file in PowerPoint e guarda ogni slide prima di usarlo.
