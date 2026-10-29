# 09 - Unconstrained variable oracles for faster numeric static analyses

Fonte: `09 - Unconstrained variable oracles for faster numeric static analyses.pdf`

Come il deck 08, non è una lezione ma la presentazione di un articolo di ricerca del gruppo di Parma: *Unconstrained Variable Oracles for Faster Numeric Static Analyses*, di **Vincenzo Arceri, Greta Dolcetti, Enea Zaffanella** (in copertina Dolcetti risulta University of Parma & Ca' Foscari University of Venice; nella prima pagina dell'articolo, riprodotta nella slide 26, tutti e tre sono a Parma). Le slide non dicono dove è stato pubblicato (**[aggiunta]**, da verificare: dovrebbe essere SAS 2023, Static Analysis Symposium). La slide 26 è uno screenshot del titolo e dell'abstract dell'articolo, senza numero; quella finale ("Thanks!") abbrevia il titolo togliendo "Numeric". Molte slide sono formule, CFG e tabelle: qui sono trascritte. Le integrazioni sono segnate come **[aggiunta]**. In fondo c'è la struttura dell'articolo letta come modello per il seminario.

## Contesto
- Il processo di abstract interpretation può introdurre **inefficienze**.
- **Soluzioni canoniche**:
  - scegliere un **dominio astratto** diverso (per esempio intervalli invece di poliedri, vedi il confronto fra domini nel deck 05);
  - scegliere **operatori astratti** diversi (lo split del deck 08 è un esempio di questa strada).

## Abstract compilation
- Le tecniche di **abstract compilation** consistono nel **riscrivere la rappresentazione intermedia** del programma usata dall'analizzatore.
- **Obiettivo**: ottimizzare l'**esecuzione astratta**.
- È un **trade-off fra accuratezza ed efficienza**.
- **[aggiunta]** È l'analogo di un passo di ottimizzazione di un compilatore, ma l'"esecuzione" da rendere più veloce è quella astratta, non quella concreta: il programma riscritto non deve calcolare gli stessi valori, deve solo avere una semantica che **sovra-approssima** quella originale.

## L'approccio
- L'efficienza della valutazione si migliora di solito **propagando informazione nota** (constant propagation e simili); si può migliorare anche **propagando informazione ignota**.

### Likely unconstrained variables
Figura: lo stato prima di `x = y + expr` contiene $expr \rightsquigarrow [1, 12]$ e $y \rightsquigarrow [-\infty, +\infty]$; dopo, oltre a questi, $x \rightsquigarrow [-\infty, +\infty]$.
- $y$ è **likely unconstrained** (LU), quindi anche $x$ è likely unconstrained.
- Se non si sa nulla di $y$, è probabile che si sappia poco o nulla dell'intera espressione.
- Non conviene quindi fare una valutazione astratta accurata (e magari costosa) dell'intera espressione.

### Propagazione dell'informazione LU
- L'idea è individuare le variabili (**Likely Unconstrained Variables**, LUV) per cui in un certo punto di programma probabilmente **non ci sarà informazione**, e **propagare questa mancanza di informazione**.
- **Obiettivo**: semplificare l'analisi e migliorarne l'efficienza.

## I passi della tecnica
1. **Dataflow analysis** (la "havoc analysis"), in due varianti: **relazionale** e **non relazionale**. Ha la forma
$$[\![\cdot]\!] : \mathsf{Stmt} \times \wp(\mathsf{Var}) \to \wp(\mathsf{Var})$$
   cioè trasforma l'insieme $lu$ delle variabili LU prima dello statement in quello dopo.
2. **Propagazione** sul CFG, in due varianti: **esistenziale** e **universale**.
3. **Trasformazione del programma**.

### Euristiche (slide 7)
Diagramma: **Oracle** {Relational, Non-Relational} $\times$ **Propagation** {Existential, Universal}, con frecce da ogni oracolo a ogni propagazione.
- **Quattro varianti** diverse.
- Sono **soluzioni euristiche**: hanno sia **falsi positivi** sia **falsi negativi**.
- L'analisi finale è comunque sempre **sound**.
- **[aggiunta]** Il perché: la trasformazione sostituisce un assegnamento $x \leftarrow expr$ con $x \leftarrow ?$ (assegnamento non deterministico, "havoc"). La semantica di $x \leftarrow ?$ contiene quella di qualunque assegnamento a $x$, quindi il programma trasformato ha più comportamenti dell'originale, e un invariante sound per il trasformato è sound anche per l'originale. L'oracolo può sbagliare quanto vuole: sbagliando si perde precisione o velocità, mai correttezza.

## Non-relational oracle (slide 8)
$$[\![ x \leftarrow ? ]\!](lu) = lu \cup \{x\}$$

$$[\![ x \leftarrow y \mathbin{op} z ]\!](lu) = \begin{cases} lu \setminus \{x\}, & \text{se } y \notin lu \text{ e } z \notin lu, \\ & \text{oppure se } op = \% \text{ e } z \notin lu, \\ & \text{oppure se } op = - \text{ e } y = z; \\ lu \cup \{x\}, & \text{altrimenti.} \end{cases}$$

$$[\![ x \leftarrow y \mathbin{op} k ]\!](lu) = \begin{cases} lu \setminus \{x\}, & \text{se } y \notin lu, \text{ oppure se } op = \%, \\ & \text{oppure se } op = * \text{ e } k = 0; \\ lu \cup \{x\}, & \text{altrimenti.} \end{cases}$$

$$[\![ (x \bowtie y) ]\!](lu) = \begin{cases} lu \setminus \{x\}, & \text{se } y \notin lu; \\ lu \setminus \{y\}, & \text{se } x \notin lu; \\ lu, & \text{altrimenti.} \end{cases}$$

- Un input non deterministico rende la variabile LU.
- Un'operazione binaria dà un risultato vincolato se entrambi gli operandi sono vincolati, oppure nei casi in cui il risultato è vincolato a prescindere: il **resto** $y \% z$ è limitato dal divisore ($|y \% z| < |z|$), $y - y = 0$, $y * 0 = 0$, e $y \% k$ è limitato da $k$.
- Una **guardia** $x \bowtie y$ (con $\bowtie$ un operatore di confronto) vincola una variabile LU se l'altra è vincolata.
- **[aggiunta]** "Vincolato" qui non vuol dire "limitato": l'oracolo è sintattico e non guarda i valori, ed è proprio questo a generare falsi positivi e negativi (sotto).

## Relational oracle (slide 9)
$$[\![ x \leftarrow ? ]\!](lu) = lu \cup \{x\}$$

$$[\![ x \leftarrow y \mathbin{op} z ]\!]^{\mathrm{rel}}(lu) = \begin{cases} lu \setminus \{x, y, z\}, & \text{se } op \in \{+, -\}; \\ [\![ x \leftarrow y \mathbin{op} z ]\!](lu), & \text{altrimenti.} \end{cases}$$

$$[\![ x \leftarrow y \mathbin{op} k ]\!]^{\mathrm{rel}}(lu) = \begin{cases} lu \setminus \{x\}, & \text{se } op = \%; \\ lu \setminus \{x, y\}, & \text{altrimenti.} \end{cases}$$

- (Refuso nella slide: nelle due definizioni relazionali manca il segno $=$ fra $(lu)$ e la parentesi graffa.)
- Un dominio relazionale (poliedri) conserva la **relazione** introdotta da un assegnamento lineare: dopo $x \leftarrow y + z$ vale $x - y - z = 0$ anche se nessuna delle tre è limitata. Per questo $x$, $y$ e $z$ escono tutte dall'insieme LU; per le altre operazioni si ricade sull'oracolo non relazionale.
- Con una costante, $x \leftarrow y \mathbin{op} k$ crea una relazione fra $x$ e $y$ (tolte entrambe), tranne per il resto, che non è lineare (tolta solo $x$, che è comunque limitata da $k$).
- La regola per le guardie nella variante relazionale non è riportata nella slide.

### Falsi positivi (slide 10)
```
y ← 0
x ← y ∗ z
```
- Poiché $z$ è LU, anche $x$ risulta LU, ma l'analisi a intervalli calcolerebbe $x \in [0, 0]$ (perché $[0,0] \times [-\infty, +\infty] = [0, 0]$).
- Falso positivo = variabile segnata LU per cui l'analisi avrebbe trovato informazione: **si perde precisione**.

### Falsi negativi (slide 11)
```
y ≥ 0 and z ≤ 0
x ← y + z
```
- $x$ risulta vincolata (sia $y$ sia $z$ hanno un vincolo), ma l'analisi a intervalli calcola $x \in [-\infty, +\infty]$, perché $[0, +\infty] + [-\infty, 0] = [-\infty, +\infty]$.
- Falso negativo = variabile non segnata LU che di fatto non ha informazione: **si perde un'occasione di speed-up**, nessuna precisione.

## Propagazione esistenziale e universale (slide 12)
- **Esistenziale**: una variabile è nell'insieme LU all'inizio di un blocco se c'è **almeno un** arco entrante lungo cui è LU.
- **Universale**: una variabile è nell'insieme LU all'inizio di un blocco se è LU lungo **tutti** gli archi entranti.
- **[aggiunta]** Nei termini del deck 04 è un'analisi **forward**: l'esistenziale è una **may** analysis (join $= \cup$, più aggressiva), l'universale una **must** analysis (join $= \cap$, più conservativa).

## Trasformazione del programma (slide 13)
```
Algorithm 1: Program transformation
Input: ⟨N, E⟩ (input CFG), LU_post : N → ℘(Var) (LU variables map)
1 foreach bb ∈ N do
2   let lu = LU_post(bb)
3   foreach s = (x ← expr) ∈ bb do
4     if x ∈ lu then
5       replace s with s' = (x ← ?) in bb
6     end
7   end
8 end
```
- Per ogni blocco si prende l'insieme LU **all'uscita** del blocco, e ogni assegnamento a una variabile di quell'insieme diventa un havoc $x \leftarrow ?$. Le guardie non vengono toccate.
- **[aggiunta]** Perché fa guadagnare tempo: valutare un'espressione su un dominio relazionale costa (soprattutto se non è lineare e va linearizzata), mentre $x \leftarrow ?$ è una semplice **proiezione** che toglie vincoli: sui poliedri in rappresentazione a generatori basta aggiungere i due raggi opposti $\pm \vec{v}_x$ (Miné, §5.3.3). Inoltre meno vincoli rendono più piccoli tutti i passi successivi (join, inclusione, widening). Con i **factored polyhedra** (sotto) una variabile senza vincoli finisce in un fattore a sé, e i fattori restano più piccoli.

## Esempio completo (slide 14-16)
CFG di partenza:

```
              b0: x ← 0
             /          \
  b1: (y < 0)            b2: (y ≥ 0)
      x ← x + 1              x ← x − 1
      y ← y + 1              y ← z ∗ 2
             \          /
              b3: x ← x + y
```

Insiemi LU con l'oracolo **non relazionale**:
- $\mathrm{LU}_{\mathrm{post}}(b0) = \{y, z\}$ ($y$ e $z$ sono input sconosciuti, $x \leftarrow 0$ vincola $x$);
- $\mathrm{LU}_{\mathrm{post}}(b1) = \{z\}$ (la guardia $y < 0$ vincola $y$, e $x + 1$, $y + 1$ restano vincolate);
- $\mathrm{LU}_{\mathrm{post}}(b2) = \{y, z\}$ ($y \leftarrow z * 2$ con $z$ LU e $k = 2 \neq 0$ rende $y$ LU);
- **esistenziale**: $\mathrm{LU}_{\mathrm{pre}}(b3)^\exists = \mathrm{LU}_{\mathrm{post}}(b1) \cup \mathrm{LU}_{\mathrm{post}}(b2) = \{y, z\}$, quindi $x \leftarrow x + y$ rende $x$ LU e $\mathrm{LU}_{\mathrm{post}}(b3)^\exists = \{x, y, z\}$;
- **universale**: $\mathrm{LU}_{\mathrm{pre}}(b3)^\forall = \mathrm{LU}_{\mathrm{post}}(b1) \cap \mathrm{LU}_{\mathrm{post}}(b2) = \{z\}$, quindi $\mathrm{LU}_{\mathrm{post}}(b3)^\forall = \{z\}$.

Programmi trasformati (in rosso nelle slide gli statement cambiati):
- **esistenziale**: in b2 `y ← z ∗ 2` diventa `y ← ?`, in b3 `x ← x + y` diventa `x ← ?`;
- **universale**: cambia solo `y ← ?` in b2, b3 resta `x ← x + y`.

**[aggiunta]** Cosa si perde. Con gli **intervalli** nulla: dopo il join $x \in [-1, 1]$ e $y$ è $\top$, quindi $x + y$ è comunque $\top$. Con i **poliedri** sì: l'originale tiene $y = 2z$ all'uscita di b2 e, in b3, la relazione $-1 \le x - y \le 1$ (il nuovo $x$ è il vecchio $x \in [-1,1]$ più $y$); la versione esistenziale perde entrambe, l'universale solo $y = 2z$. Sono esattamente le relazioni che l'oracolo relazionale avrebbe protetto ($y \leftarrow z * 2$ è lineare). È un piccolo modello dei risultati sperimentali: ~99% dei vincoli conservati con gli intervalli, ~90% con i poliedri.

## Experimental evaluation
### Setup
- Due suite di benchmark:
  - **WCET analysis** (PAGAI, 34 file), con i dettagli nell'articolo;
  - **Linux drivers** (SVCOMP, 10 file).
- Due domini:
  - **Intervals**;
  - **Factored Polyhedra** (PPLite).
- **[aggiunta]** Nel deck 08 gli stessi benchmark erano 39 file PAGAI e 7 driver: le due selezioni non coincidono. Tutte le tabelle e i grafici delle slide riguardano i **10 driver Linux** (il totale delle righe torna con la riga "all tests").
- **[aggiunta]** I *factored polyhedra* dividono le variabili in blocchi indipendenti e tengono un poliedro per blocco (un'idea simile al *variable packing* di Miné, §6.2.5, ma con blocchi calcolati dinamicamente).

### Clam/Crab (Gurfinkel, Navas; VSTTE 2021)
- Moduli del framework **SeaHorn**.
- **Crab**: libreria C++ di analisi statica, domini astratti e motore di punto fisso, **CrabIR**.
- **Clam**: front-end di Crab, $\texttt{C} \to \texttt{LLVM} \to \texttt{CrabIR}$.
- **Clam-diff**: confronta gli invarianti di due analisi.
- Figura: il CFG CrabIR di un `main` con un ciclo `for`:

```
entry:     havoc(call) /* nd_int(...) */
           i.0 = 0
for.cond:
  __@bb_5: assume(-call+i.0 <= -1)   -> for.inc: inc = i.0+1; i.0 = inc  -> for.cond
  __@bb_6: assume(call-i.0 <= 0)     -> for.end: @V_1 = 0
```

- L'input non deterministico (`nd_int()`) è già un `havoc`, cioè proprio l'$x \leftarrow ?$ dell'oracolo; le guardie sono `assume` lineari ($i < n$ e $i \ge n$), come nel deck 08.

### Pipeline completa (slide 19)
```
C source code → LLVM bitcode → original CrabIR ───────────────────────────────→ original target-analysis invariants
                                                                                          ↕ Clam-diff
C source code → LLVM bitcode → original CrabIR → havoc-analysis invariants → havocked CrabIR → havocked target-analysis invariants
```
- Strumenti: **Clang/LLVM + clam-pp** (da C a bitcode), **Clam** (da bitcode a CrabIR), **Havoc analysis** (l'oracolo, produce gli insiemi LU), **Havoc propagation** (la trasformazione, produce il CrabIR "havocked"), **Target Analysis** (l'analisi vera, con intervalli o poliedri), **Clam-diff** (confronta gli invarianti delle due pipeline).

### Statement trasformati (slide 20)
"stmts havocked": quanti statement vengono trasformati in havoc con le quattro varianti. La colonna *time* non ha unità e i valori non corrispondono ai tempi del grafico finale: misura probabilmente un'altra cosa (forse la sola havoc analysis), va verificato nell'articolo.

| test | stmts | LU∃ | time | LU∀ | time | LU∃rel | time | LU∀rel | time |
|---|---|---|---|---|---|---|---|---|---|
| all tests | 353544 | 119509 | 7014 | 104509 | 12653 | 14591 | 6771 | 14411 | 12533 |
| wl12xx | 109101 | 89543 | 332 | 75667 | 578 | 942 | 453 | 915 | 726 |
| rtlwifi | 53456 | 5873 | 1481 | 5873 | 3391 | 5813 | 1418 | 5813 | 3049 |
| w83781d | 52909 | 5452 | 2933 | 5450 | 4366 | 2605 | 2645 | 2605 | 4706 |
| brocade | 37587 | 4703 | 308 | 4495 | 666 | 2098 | 309 | 2039 | 614 |
| libfc | 31272 | 3108 | 1285 | 2811 | 2472 | 66 | 1263 | 65 | 2227 |
| vmxnet3 | 19598 | 3983 | 175 | 3849 | 311 | 496 | 184 | 495 | 327 |
| mdc | 17104 | 2333 | 154 | 2168 | 314 | 1017 | 149 | 981 | 322 |
| firewire | 13196 | 1902 | 185 | 1701 | 284 | 800 | 185 | 747 | 282 |
| solos | 12465 | 2302 | 122 | 2301 | 199 | 732 | 131 | 730 | 210 |
| abituguru | 6856 | 310 | 39 | 194 | 72 | 22 | 34 | 21 | 70 |

(LU∃ e LU∀ = oracolo non relazionale, LU∃rel e LU∀rel = relazionale.)

Riquadro della slide, che confronta gli estremi (non relazionale esistenziale, il più aggressivo, e relazionale universale, il più conservativo):
- $\mathrm{LU}^\exists = [4.5\%;\ 82.1\%]$ (da abituguru a wl12xx);
- $\mathrm{LU}^\forall_{\mathrm{rel}} = [0.2\%;\ 10.9\%]$ (da libfc a rtlwifi);
- $\mathrm{LU}^\exists$ avg $= 33.8\%$;
- $\mathrm{LU}^\forall_{\mathrm{rel}}$ avg $= 4.1\%$.
- (Precisazione: le due "avg" sono il rapporto fra i totali, $119509 / 353544$ e $14411 / 353544$, quindi pesate per dimensione e dominate da wl12xx. La media semplice delle percentuali dei 10 test è circa $19.7\%$ per $\mathrm{LU}^\exists$ e $4.2\%$ per $\mathrm{LU}^\forall_{\mathrm{rel}}$. Ho ricontrollato tutti i totali e gli estremi: tornano.)
- **[aggiunta]** In ogni riga la propagazione universale ha un tempo maggiore di quella esistenziale (in totale $12653$ contro $7014$).

Conclusioni della slide 21:
- gli oracoli **relazionali** sono **troppo conservativi**;
- quelli **non relazionali** sono **piuttosto aggressivi** e possono portare a miglioramenti di efficienza significativi;
- la scelta fra **relazionale e non relazionale** pesa molto più di quella fra **esistenziale e universale**.

### Precisione: intervalli (slide 22)
"Domain: Intervals, ~99% original constraints". Gli invarianti dell'analisi trasformata sono confrontati con quelli originali: **EQ** = invariante identico, **GT** = invariante strettamente più grande, cioè meno preciso.

| | totale | LU∃ EQ | LU∃ GT | LU∀ EQ | LU∀ GT |
|---|---|---|---|---|---|
| # INVS | 3102 | 2981 | 121 | 3005 | 97 |
| % INVS | 100.00 | 96.10 | 3.90 | 96.87 | 3.13 |
| vmxnet3 | 513 | 416 | 97 | 416 | 97 |
| mdc | 112 | 88 | 24 | 112 | 0 |

- Gli invarianti meno precisi stanno tutti in vmxnet3 e mdc ($97 + 24 = 121$); su mdc la propagazione universale non perde niente.
- **[aggiunta]** Il "~99%" è la percentuale di **vincoli** conservati, mentre la tabella conta gli **invarianti** identici (96-97%): un invariante GT può aver perso un solo vincolo su tanti.

### Precisione: poliedri (slide 23)
"Domain: Polyhedra, ~90% original constraints".

| | totale | LU∃ EQ | LU∃ GT | LU∀ EQ | LU∀ GT |
|---|---|---|---|---|---|
| # INVS | 3102 | 1389 | 1713 | 1485 | 1617 |
| % INVS | 100.00 | 44.78 | 55.22 | 47.87 | 52.13 |
| vmxnet3 | 513 | 190 | 323 | 190 | 323 |
| brocade | 511 | 154 | 357 | 154 | 357 |
| firewire | 499 | 319 | 180 | 319 | 180 |
| w83781d | 356 | 95 | 261 | 95 | 261 |
| solos | 303 | 104 | 199 | 104 | 199 |
| libfc | 295 | 295 | 0 | 295 | 0 |
| rtlwifi | 208 | 5 | 203 | 5 | 203 |
| abituguru | 169 | 91 | 78 | 168 | 1 |
| wl12xx | 136 | 92 | 44 | 92 | 44 |
| mdc | 112 | 44 | 68 | 63 | 49 |

- (Errore nella slide: per LU∀ le percentuali sono scritte $47.83$ e $53.17$, che sommano a $101$. Quelle giuste sono $1485 / 3102 = 47.87\%$ e $1617 / 3102 = 52.13\%$; in tabella ho messo i valori corretti. Gli altri numeri tornano.)
- libfc (evidenziato in verde) non perde nessun invariante; abituguru e mdc (in grassetto) sono gli unici in cui esistenziale e universale differiscono, e l'universale è più preciso.
- Con i poliedri più della metà degli invarianti è meno preciso, ma i vincoli conservati sono ancora circa il 90%.

### Tempo, poliedri (slide 24)
Istogramma "Overall Analysis Time", **Original** (azzurro) contro **Our approach** (arancio), unità non indicata. Valori letti a occhio:

| test | original | our approach |
|---|---|---|
| wl12xx | ~181 | ~22 |
| libfc | ~167 | ~104 |
| brocade | ~141 | ~106 |
| vmxnet3 | ~134 | ~37 |
| w83781d | ~110 | ~110 |
| mdc | ~107 | ~25 |
| abituguru | ~94 | ~55 |
| rtlwifi | ~80 | ~69 |
| solos | ~80 | ~10 |
| firewire | ~65 | ~21 |

- Etichette sul grafico: **1.60** su libfc (in verde: speed-up senza alcuna perdita di precisione, vedi tabella sopra) e **8.23** su solos (in azzurro: lo speed-up massimo).
- **Avg. speedup 2.61**.
- w83781d non accelera, rtlwifi e brocade poco.
- **[aggiunta]** Dalle barre lette a occhio la media aritmetica degli speed-up sarebbe circa 3.4 e il rapporto fra i tempi totali circa 2.1, mentre la media geometrica viene circa 2.6: il 2.61 è con ogni probabilità una media geometrica. La slide non dice nemmeno quale delle quattro varianti è "our approach" (presumibilmente una non relazionale, visto quanto poco trasformano le relazionali).

## Conclusion
- **Risultati**:
  - **speed-up significativi**, fino a **8.23**, in media **2.61**;
  - **perdita di precisione limitata**: circa il **90% dei vincoli originali** (poliedri).
- **Lavori futuri**:
  - ulteriori **semplificazioni del CFG** dopo la havoc-processing;
  - **euristiche migliori**.

### Abstract dell'articolo (slide 26)
Nell'ambito dell'analisi statica basata su abstract interpretation si propone un **passo di pre-analisi leggero** che suggerisce, in ogni punto di programma, quali variabili sono probabilmente non vincolate per una certa classe di proprietà numeriche astratte. Usando l'esito come **oracolo**, si semplificano gli statement del programma propagando questa mancanza di informazione, per regolare il **trade-off precisione/efficienza**. Una valutazione sperimentale preliminare mostra che l'idea funziona (lo screenshot si interrompe qui).

## Struttura dell'articolo (modello per il seminario)
- **Problema**: i domini relazionali (poliedri) sono precisi ma costosi, e spesso l'analisi spende tempo a calcolare con precisione valori di cui alla fine non saprà nulla.
- **Idea**: invece di cambiare dominio o operatori (le soluzioni canoniche), riscrivere il programma (**abstract compilation**): una pre-analisi economica indica le variabili *probabilmente* non vincolate e i loro assegnamenti diventano havoc.
- **Formalizzazione**: una dataflow analysis $[\![\cdot]\!] : \mathsf{Stmt} \times \wp(\mathsf{Var}) \to \wp(\mathsf{Var})$ in due varianti (non relazionale e relazionale), due propagazioni ai punti di join ($\cup$ esistenziale, $\cap$ universale), un algoritmo di trasformazione. La soundness non dipende dall'oracolo, perché l'havoc sovra-approssima ogni assegnamento.
- **Implementazione**: pipeline su Clam/Crab con havoc analysis, havoc propagation e Clam-diff per confrontare gli invarianti.
- **Valutazione**: driver Linux di SVCOMP (e PAGAI nell'articolo), intervalli e factored polyhedra; misure di quanti statement si trasformano, precisione (EQ/GT e vincoli conservati) e tempo. Speed-up medio 2.61, massimo 8.23; ~99% dei vincoli con gli intervalli, ~90% con i poliedri.
- **Limiti** (alcuni dichiarati, altri **[aggiunta]**): l'oracolo è euristico, con falsi positivi (precisione persa) e falsi negativi (speed-up mancati); le varianti relazionali trasformano troppo poco, le non relazionali molto ma perdono più precisione; con i poliedri più della metà degli invarianti peggiora; i risultati mostrati riguardano 10 driver; l'articolo stesso parla di valutazione **preliminare**.

## Da ricordare
- **Abstract compilation**: riscrivere la IR per rendere più veloce l'esecuzione astratta, accettando un trade-off con la precisione.
- **Likely unconstrained variable**: variabile su cui probabilmente l'analisi non saprà nulla; se un operando è LU, il risultato è LU, salvo i casi in cui è vincolato a prescindere ($y \% z$, $y - y$, $y * 0$).
- Oracolo **non relazionale** (aggressivo) contro **relazionale** (conservativo: un assegnamento lineare crea una relazione, quindi toglie tutte le variabili coinvolte dall'insieme LU).
- Propagazione **esistenziale** (LU su almeno un arco entrante, $\cup$, may) contro **universale** (LU su tutti, $\cap$, must).
- Trasformazione: se $x \in \mathrm{LU}_{\mathrm{post}}(bb)$, ogni $x \leftarrow expr$ in $bb$ diventa $x \leftarrow ?$. Sempre **sound**, qualunque cosa dica l'oracolo.
- Falso positivo: `y ← 0; x ← y ∗ z` (si perde $x \in [0,0]$). Falso negativo: `y ≥ 0, z ≤ 0; x ← y + z` (intervallo comunque $\top$).
- Numeri: statement trasformati dal 4.5% all'82.1% (non relazionale esistenziale), dallo 0.2% al 10.9% (relazionale universale); precisione ~99% dei vincoli con gli intervalli, ~90% con i poliedri; speed-up sui poliedri in media **2.61**, massimo **8.23** (solos), **1.60** su libfc senza perdita di precisione.
