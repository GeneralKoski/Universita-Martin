# Seminario - scaletta della presentazione (15 minuti)

**Paper (topic 07 dell'elenco di Arceri, scelta da comunicare con la mail):** Simon, King, Howe - *Two Variables per Linear Inequality as an Abstract Domain* (19 pagine, `2026-27/1_Material/Topics for seminars.zip`, cartella `07 - TVL`).

**Esame:** presentazione di max 15 minuti, poi orale di 10 minuti sugli argomenti del corso. Il topic va comunicato ad Arceri entro il 27/11/2026 alle 9:00 per presentare entro dicembre (mail con oggetto `[Static analysis and software verification] 7 Mat. <MATRICOLA>`).

## In una frase

Un dominio numerico relazionale di disuguaglianze `a·x + b·y ≤ c` con **al massimo due variabili** e coefficienti **qualsiasi** (reali): più espressivo degli Octagon (che ammettono solo coefficienti -1, 0, +1) e molto più trattabile dei poliedri. Tutte le operazioni diventano **polinomiali** perché si lavora sulle **proiezioni sui piani a due variabili**, dopo aver reso esplicite tutte le conseguenze con un'operazione detta *completion*.

## Scaletta (11 slide, circa 14 minuti, un po' di margine)

| # | Slide | Min | Cosa dire |
|---|---|---|---|
| 1 | Titolo e contesto | 0:45 | Autori, tema: domini numerici relazionali. Aggancio al corso: i domini numerici delle slide sugli intervalli e sull'interpretazione astratta |
| 2 | Il compromesso precisione / trattabilità | 1:15 | Intervalli (non relazionali, veloci) - Octagon di Miné (`±x ± y ≤ c`, matrice DBM 2d×2d, chiusura O(d³) con Floyd-Warshall) - poliedri (relazionali, costo esponenziale nel caso peggiore, Chernikova). Il TVL sta in mezzo: limite degli Octagon = coefficienti unitari. Aggancio: stesso tema delle slide 08 (split operator) e 09 (unconstrained variable oracles), cioè rendere veloci le analisi numeriche |
| 3 | Il dominio | 1:30 | `Two_X` = insiemi finiti di disuguaglianze con al massimo due variabili, ordinati per entailment. È un **reticolo, non completo**: meet = unione, join = chiusura topologica dell'inviluppo convesso. **Esempio 1** del paper (T1 = punto (0,1), T2 = semiretta x=y, x≥0): l'inviluppo convesso non è chiuso, per questo serve `cl`. Nota da dire a voce: **non esiste α** (non c'è la migliore approssimazione di un cerchio con un numero finito di disuguaglianze), si lavora solo con γ |
| 4 | Idea chiave: forma completa | 1:30 | Restrizione `π_Y(T)` alle disuguaglianze sulle sole variabili in `Y`. Un sistema è **completo** se ogni conseguenza `t` è già implicata dalle sue disuguaglianze su `var(t)`, cioè su una o due variabili. Prop. 1: ogni sistema ha una forma completa equivalente (aggiungere tutte le proiezioni sulle coppie). Messaggio: dopo la completion, **ragionare sul sistema intero = ragionare coppia per coppia**. È l'analogo della chiusura negli Octagon |
| 5 | Come si calcola la completion | 2:00 | Algoritmo di Nelson (1978, test di soddisfacibilità). Due ingredienti: **`result`** (data `a·x+b·y≤c` con a>0 e `d·x+e·z≤f` con d<0 elimina `x` e ottiene `a·e·z - d·b·y ≤ a·f - d·c`) e **`filter`** (toglie le ridondanti ordinando per angolo θ, tempo lineare). **Lemma 1**: un'iterazione dimezza le variabili necessarie, quindi bastano circa log₂(\|var\|) iterazioni. **Esempio 2** (catena x0≤x1≤x2≤x3≤x4) e **Esempio 3** (rilevamento dell'insoddisfacibilità: si arriva a `0 ≤ -24`) da disegnare alla lavagna o in slide. Complessità O(k²d³ log d (log k + log d)), con k = disuguaglianze per proiezione |
| 6 | Le operazioni "facili" | 1:00 | **Proiezione** `∃x`: basta togliere tutte le disuguaglianze che contengono `x`, senza Fourier-Motzkin (esempio del paper: da `y≤x` e `x≤z` resta `y≤z` perché la completion l'aveva già esplicitata). **Entailment**: si controlla coppia per coppia (Prop. 7), con proiezioni ordinate per angolo, tempo lineare; il caso base di tre disuguaglianze è in tempo costante con la regola di Cramer |
| 7 | Join: inviluppo convesso planare | 2:00 | Il pezzo originale del paper. Si fa l'inviluppo convesso **su ogni proiezione 2D** (Prop. 4 e 5: il risultato è completo e coincide con l'inviluppo dello spazio intero). Passi: `extreme` (da disuguaglianze a vertici e raggi, al massimo 4 raggi per poliedro) - Graham scan sul quadrato che contiene i vertici, con i punti lungo i raggi spinti fuori dal quadrato - ritorno alle disuguaglianze con `connect`. Costo O(n log n) invece di Chernikova. Dire che gli autori affermano che questo algoritmo, per quanto ne sanno, è unico |
| 8 | Widening | 1:30 | **Per terminazione**: va bene un qualunque widening dei poliedri, applicato sulle proiezioni, meglio quando il numero e la dimensione delle proiezioni si sono stabilizzati. **Sottigliezza** da dire: applicare la completion dopo il widening può reintrodurre le disuguaglianze appena tolte e rompere la terminazione. **Per trattabilità**: limitare a una costante il numero di disuguaglianze per proiezione (si scarta quella che contribuisce al lato più corto), così il costo scende a O(d³ (log d)²), contro O(d³) degli Octagon |
| 9 | Evidenza empirica | 1:15 | Poliedri planari casuali, tre scenari (*varying*, *constant*, *sparse*). Tabella del paper: la completion fa crescere le proiezioni del 56%, 123%, 9%; meno dello 0,3% delle proiezioni ha più di 30 disuguaglianze. Spiegazione: l'inviluppo di n punti casuali ha O(log n) punti estremi. **Dire onestamente il limite**: i dati sono casuali, non programmi reali, e non c'è confronto di tempi con gli Octagon |
| 10 | Confronto, limiti, applicazioni | 1:00 | Rispetto agli Octagon: toglie il vincolo sui coefficienti, costo poco superiore, rappresentazione densa (spazio solo per le disuguaglianze presenti). Limiti: niente α, lavora sui reali (gli interi non sono trattati), prove solo su dati casuali, con una sola implementazione naive della completion per gli esperimenti (nessun tool di analisi). Applicazioni citate nell'introduzione: verifica di programmi, automi temporizzati, parallelizzazione, vulnerabilità di sicurezza, memory leak, terminazione di programmi logici |
| 11 | Conclusioni | 0:30 | Un'operazione (completion) sistema tutto: meet, join, proiezione, entailment diventano polinomiali e semplici da implementare (e quindi meno soggette a errori). Un passo avanti sugli Octagon senza perdere trattabilità |

Totale circa 14 minuti e 15 secondi. Se scivoli sui tempi, taglia dalla slide 9 e dalla 10, non dalla 5 e dalla 7.

## Cosa lasciare fuori

- Le dimostrazioni delle Prop. 4, 5, 6 e del Teorema 1 (basta enunciarle).
- Il codice completo di `filter`, `extreme`, `join`, `entails` (Fig. 1-4): mostra a voce l'idea, non il listato.
- La sezione *Related work* (Su-Wagner, Jaffar et al., Hochbaum-Naor): una riga al massimo.
- Le Future Work (union-find per partizionare il sistema).

## Domande probabili (risposte dal paper o dedotte da esso)

- **Perché serve la completion?** Perché proiezione, join ed entailment, fatte coppia per coppia, sono corrette solo se ogni conseguenza è già visibile su una coppia di variabili. Senza completion si perderebbe precisione (analogo della chiusura degli Octagon).
- **Perché il join richiede `cl`?** Perché l'inviluppo convesso di insiemi chiusi può non essere chiuso (Esempio 1) e un sistema di disuguaglianze non strette descrive solo insiemi chiusi.
- **Perché non c'è α?** Un insieme come un cerchio non ha una migliore approssimazione con un numero finito di disuguaglianze, a differenza degli Octagon dove ogni oggetto planare ha al massimo otto disuguaglianze.
- **Perché il widening è delicato?** Perché la completion dopo il widening può reintrodurre disuguaglianze scartate e impedire la terminazione.
- **Cosa guadagna rispetto agli Octagon e cosa paga?** Coefficienti qualsiasi invece di ±1, al prezzo di O(d³ (log d)²) invece di O(d³) e di dover limitare k.
- **Il TVL è esatto rispetto ai poliedri?** No: è un'astrazione dei poliedri che tiene solo le relazioni a due variabili alla volta.

## Da controllare prima dell'esame

- Provare a mano l'Esempio 3 (insoddisfacibilità) e l'Esempio 1 (inviluppo non chiuso), da raccontare con carta e penna.
- Capire bene `result` con un esempio proprio, scegliendo coefficienti diversi da 1.
- Rivedere le slide 04 (dataflow), 06-07 (Galois, semantica astratta) e 12 (intervalli) del corso, perché i 10 minuti di orale sono su tutto il programma.

Questa scaletta è basata sul testo del paper estratto dal PDF. Le figure (poliedri disegnati, istogramma della Fig. 5) non le ho viste: vanno guardate nel PDF.
