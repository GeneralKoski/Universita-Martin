# 11 - Abstract interpretation in LiSA

Fonte: `11 - Abstract interpretation in LiSA.pdf`

Nella slide di copertina la lezione è numerata "Lecture 9". Molte pagine sono build successive della stessa slide (overview di LiSA, program-wide fixpoint, interprocedural analysis, GoLiSA, EVMLiSA): qui sono riassunte una volta sola, nella versione completa. La slide "Example: sign analysis" (pagina 94) contiene solo l'icona di un monitor: l'esempio è stato fatto dal vivo e nel PDF non c'è. Il deck non contiene codice Java vero, solo pseudocodice e diagrammi di classi: nessun output è stato verificato eseguendo LiSA (Java non è installato su questa macchina). Le brevi integrazioni sono segnate come **[aggiunta]**.

## LiSA, a Library for Static Analysis
- **Core team (2020 - oggi)**: Luca Negrini (UNIVE), Vincenzo Arceri (UNIPR), Luca Olivieri (UNIVE), Pietro Ferrara (UNIVE).
- È una **libreria per costruire analizzatori statici basati su abstract interpretation**:
  - per **più linguaggi** di programmazione;
  - per **domini** (astratti) di tipo diverso.
- Scopi:
  - sperimentare **implementazioni modulari**;
  - essere **facile da imparare** (semplice, vicina alla formalizzazione);
  - **prototipazione rapida** di analizzatori e domini.
- Libreria Java **open source**, creata e mantenuta da UNIPR e UNIVE (Ca' Foscari). Codice su https://github.com/lisa-analyzer (pagina 95).

## Cos'è LiSA (e cosa non è)
Diagramma costruito in più passi (pagine 4-9):
- Il cuore è un **motore di analisi generico** con **componenti già sviluppati** (pre-developed components).
- Dall'alto entrano i **parametri di configurazione**: scelta dei componenti e **plug-in di componenti nuovi**.
- A destra escono **warning e output** dell'analisi.
- **"Not a Full Analyzer"**: l'icona del codice sorgente in ingresso è barrata. LiSA **non legge direttamente il codice sorgente**.
- **"a Library"**: un **Full Analyzer** è il riquadro che contiene un passo di traduzione (icona dell'ingranaggio) dal codice sorgente agli **inputs** (un diagramma di flusso, cioè i CFG) più LiSA. Il front-end per il linguaggio specifico lo scrive chi costruisce l'analizzatore; LiSA fa il resto.

## LiSA Overview
Lo schema generale (pagine 10-19, ripreso più volte nel deck evidenziando di volta in volta un blocco):

```
 P^i (programma nel linguaggio L^i)
   |
 L^i Frontend   --> compilazione in un programma LiSA,
   |                definizione del modello di esecuzione del linguaggio,
   |                definizione della semantica delle istruzioni
 CFGs           --> control flow embedded, fixpoint standard
   |
   v           configuration, components
 +--------------------- LiSA ------------------------------+
 |  Interprocedural Analysis --> CFG fixpoint               |
 |    [Call Graph]                   |                      |
 |          ^                  Statement semantics          |
 |          +-------------------/    |                      |
 |                                   v                      |
 |                    Abstract State [Heap Domain]          |
 |                                   [Value Domain]         |
 |                                   |                      |
 |                                Checks --> analysis dump, |
 |                                           warnings       |
 +----------------------------------------------------------+
```

- In blu i blocchi **language dependent** (frontend, CFG, statement semantics), in verde quelli **configurable** (interprocedural analysis, call graph, abstract state con heap e value domain, checks).
- Il **CFG fixpoint** e il collegamento fra i blocchi sono il motore fisso di LiSA.
- Gli **Checks** ricevono sia i risultati dell'interprocedural analysis sia gli abstract state, e producono warning e dump dell'analisi.

## CFG in LiSA
Esempio:

```c
1 int i = 2;
2 int max = 10;
3 while (i < max)
4   i = i + 1;
5 return i;
```

CFG disegnato da LiSA:

```
   [ i = 2 ]          (entrypoint: bordo nero singolo)
       |
   [ max = 10 ]
       |
   [ <(i, max) ] <------+
     |      :           |
false:      :true       |
     v      v           |
 [[ return i ]]  [ i = +(i, 2) ] -+
 (exitpoint: bordo doppio)
```

- Legenda: nodo normale con bordo grigio singolo, **entrypoint** nero singolo, **exitpoint** nero doppio; arco **sequenziale** nero continuo, arco **true** blu tratteggiato, arco **false** rosso tratteggiato.
- Le espressioni sono in forma prefissa: `<(i, max)` per `i < max`, `+(i, 2)` per una somma.
- (Errore nella slide, pagine 13-16: il nodo del corpo del ciclo è `i = +(i, 2)`, ma il codice a fianco dice `i = i + 1`. Il CFG corrisponde a `i = i + 2`; con il codice mostrato il nodo dovrebbe essere `i = +(i, 1)`.)
- **I nodi sono istanze di `Statement`**, **gli archi sono istanze di `Edge`**.
- **LiSA non fissa una semantica** per nessuno `Statement`/`Edge`: lascia che sia l'utente (cioè il frontend) a definirla.

## Computing fixpoints on CFGs
Algoritmo del punto fisso intraprocedurale:

```
 1: forall n ∈ N do
 2:     out_n ← ⊥                         // ⊥ = non ancora processato / irraggiungibile
 3: in_n0 ← ⊤                             // ⊤ = nessuna informazione
 4: out_n0 ← semantics_n0(in_n0)          // usa Statement.semantics()
 5: ws ← succ(n0)
 6: while ws ≠ ∅ do
 7:     n ← pop(ws)
 8:     in_n ← ⊔{ traverse_{m→n}(out_m) :   // ⊔ per sovra-approssimare l'entry state; usa Edge.traverse()
 9:                m ∈ preds(n) }
10:     tmp_n ← semantics_n(in_n)
11:     if tmp_n ⋢ out_n then             // ⊑ per tenere il risultato "più alto"
12:         out_n ← out_n ⊕ tmp_n         // ⊔ per salire / ∇ per la convergenza
13:         ws ← ws ∪ succ(n)
14: return out
```

- `ws` è la **worklist**, come in quella delle dataflow analyses (lezione 04), ma qui parametrica sul dominio astratto.
- Lo stato iniziale del nodo di ingresso è $\top$: dell'input non si sa nulla. Tutti gli altri partono da $\bot$.
- L'entry state di un nodo è il **lub** degli stati di uscita dei predecessori, ciascuno passato attraverso l'arco con `Edge.traverse()`: è così che un arco true/false può filtrare lo stato (assume della guardia o della sua negazione).
- $\oplus$ è un parametro: il **lub** $\sqcup$ (iterazione di Kleene) oppure il **widening** $\nabla$ quando il dominio ha catene ascendenti infinite.
- **[aggiunta]** Il test della riga 11 fa da criterio di arresto: se il nuovo risultato è già contenuto nel vecchio, il nodo è stabile e i successori non vengono rimessi in lista.

## The program-wide fixpoint
Diagramma di flusso (pagine 20-27):

```
 select the CFGs to start the analysis from
              |
              v
 +--> run a fixpoint over them <- - - - - - - - - - - +
 |            |                                       :
 |     < are calls in the CFG? > --yes--> access another CFG's result
 |            | no                                    :
 |            v                                       v
 +--- find other CFGs to analyze          access the result from a
                                          previous fixpoint
```

- Si scelgono i CFG da cui partire, si fa il punto fisso su di essi, poi si cercano altri CFG da analizzare e si ripete.
- Quando nel CFG c'è una chiamata, serve il **risultato di un altro CFG**, preso da un **punto fisso precedente** (frecce tratteggiate verdi).
- Avvertenza in rosso: **"This happens inside the CFG fixpoint! We do not want this logic to flow over there"**. Il controllo "ci sono chiamate?" avviene dentro il punto fisso del singolo CFG, e non si vuole che la logica interprocedurale contamini il fixpoint intraprocedurale. Da qui la separazione del componente successivo.

## The interprocedural analysis
Diagramma completo (pagine 28-34):

Frecce del diagramma:

| Da | A | Etichetta |
|---|---|---|
| Interprocedural Analysis | CFG Fixpoint | fixpoint logic |
| CFG Fixpoint | Non-calling statement | `semantics()` |
| Non-calling statement | CFG Fixpoint | abstract result |
| CFG Fixpoint | Calling statement | `semantics()` |
| Calling statement | Interprocedural Analysis | `ia.getResult(this)` |
| Interprocedural Analysis | Call Graph | `cg.resolve(call)` |
| Call Graph | Interprocedural Analysis | call targets |
| Interprocedural Analysis | Calling statement | abstract result |
| Calling statement | CFG Fixpoint | abstract result |

- L'**Interprocedural Analysis** (configurabile) decide la **fixpoint logic** e la passa al CFG Fixpoint. La logica può essere:
  - considerare i CFG **in isolamento**;
  - **partire dal `main` e seguire le chiamate**;
  - altro.
- Il CFG Fixpoint chiama `semantics()` sugli statement:
  - uno **statement non chiamante** restituisce direttamente il suo abstract result;
  - uno **statement chiamante** chiede il risultato all'analisi interprocedurale con `ia.getResult(this)`.
- L'analisi interprocedurale risolve la chiamata con `cg.resolve(call)` sul **Call Graph** (configurabile), che restituisce i **call target**. Il call graph può usare:
  - i **tipi a runtime del receiver**;
  - i **tipi compatibili con la signature**;
  - altro.
- Poi restituisce l'abstract result allo statement chiamante, che lo passa al CFG Fixpoint.
- Messaggi chiave (in rosso):
  - **la semantica degli statement non sa cosa fa il fixpoint**;
  - **tutto il processo è indipendente dall'analisi** (dal dominio scelto);
  - **il resto di LiSA ignora le chiamate**.

## Syntax vs semantics
- La semantica degli statement va specificata in modo **generico**:
  - deve valere **per tutte le analisi**;
  - **le analisi non devono dare significato alla sintassi**. Esempio: in Java `a + b` può essere una **somma** o una **concatenazione** di stringhe.
- Una soluzione: **riscrivere in una IR** (rappresentazione intermedia).
- Ma così si perde la possibilità di **sfruttare informazione semantica** (es. il tipo calcolato dall'analisi per decidere cosa significa `+`).

## Symbolic expressions
- Soluzione di LiSA: **spezzare gli `Statement` in `SymbolicExpression`** ($expr_1, expr_2, \dots, expr_n$), che sono ciò che arriva ai domini.
- La riscrittura avviene **dinamicamente**, durante l'analisi, e può sfruttarne i risultati: **tipi, valori possibili**, ecc.
- Le `SymbolicExpression` sono **estendibili**: LiSA ne fornisce alcune, l'utente può definirne altre.
- **Le analisi devono modellare solo queste espressioni**, ignorando la sintassi che c'è dietro.

### Esempi (pseudocodice)
`+` che diventa somma o concatenazione a seconda dei tipi:

```
1 Plus.semantics():  // left + right
2   if type(left) is string or type(right) is string:
3     return domain.eval(new BinaryExpression("cat", left, right))
4   else:
5     return domain.eval(new BinaryExpression("+", left, right))
```

Operatore condizionale `condition ? ifTrue : ifFalse`:

```
1 Conditional.semantics():  // condition ? ifTrue : ifFalse
2   sat = domain.isSatisfied(condition)
3   tt = ifTrue.semantics()
4   ff = ifFalse.semantics()
5   return sat.isTrue() ? tt : (sat.isFalse() ? ff : tt ⊔ ff)
```

- Se il dominio sa che la condizione è sempre vera (o sempre falsa) si tiene solo un ramo, altrimenti il lub dei due.
- (Nota: qui il metodo si chiama `isSatisfied`, mentre nell'interfaccia `SemanticDomain` più avanti è `satisfies`; è pseudocodice, si intende lo stesso metodo.)
- **[aggiunta]** Nello pseudocodice i due rami sono valutati sullo stesso stato; per avere più precisione, `ifTrue` andrebbe valutato dopo `assume(condition)` e `ifFalse` dopo `assume(!condition)`.

Pre-incremento `++var`:

```
1 PreIncrement.semantics():  // ++var
2   add = new BinaryExpression("+", var, new Const(1))
3   d1 = domain.store(var, add)
4   return d1.eval(var)
```

- Lo statement diventa un assegnamento `var = var + 1` seguito dalla valutazione di `var` (il valore di `++var` è quello già incrementato). Anche qui `store` è il nome usato nello pseudocodice; nell'interfaccia il metodo è `assign`.

## The abstract state
Riferimento [Fer16] (nella bibliografia finale non compare per esteso; **[aggiunta]** è il lavoro di Ferrara del 2016 sul framework generico che combina analisi dello heap e dei valori).

- L'**Abstract State** (configurabile) riceve una symbolic expression e contiene:
  - un **Heap Domain**, che traccia la **struttura della memoria dinamica**: nuove allocazioni, pointer aliasing, ecc.;
  - un **Value Domain**.
- L'Heap Domain **riscrive le espressioni che riguardano la memoria** nelle loro variabili simboliche.
- Il Value Domain **"vede" solo espressioni con variabili e costanti**.

### Esempio
1. `x.f = 5`: l'Heap Domain associa `x → L1` (L1 è la locazione astratta, il sito di allocazione), e riscrive l'assegnamento in `L1 = 5`. Value Domain: `L1 → {5}`.
2. `x.g = 7`: l'Heap Domain riscrive in `L1 = 7`. Value Domain: `L1 → {5, 7}`.
   - Serve un **weak update** perché `x.f` e `x.g` sono astratti nello **stesso sito di allocazione** (analisi **field-insensitive**): non si può sovrascrivere 5 con 7, si fa il join.
3. Con un'analisi dello heap **field-sensitive**: Value Domain `L1.f → {5}`, `L1.g → {7}`, nessuna perdita di precisione.
   - (Nella slide l'analisi field-sensitive è detta "call site based", mentre la pagina precedente parla di "allocation site": nel contesto si intende un'analisi basata sui siti di allocazione.)
- **[aggiunta]** Strong update: si sovrascrive il valore, possibile solo se la locazione astratta rappresenta un'unica locazione concreta. Weak update: si fa il lub fra vecchio e nuovo valore.

## Abstract domains in LiSA
Gli stati astratti devono essere **costruiti, uniti e confrontati** durante il punto fisso. Due interfacce:

| `Lattice : L` | `SemanticDomain : D` |
|---|---|
| `lessOrEqual(other: L): boolean` | `assign(id: ID, expression: SymbExpr): D` |
| `lub(other: L): L` | `smallStepSemantics(expression: SymbExpr): D` |
| `widening(other: L): L` | `satisfies(expression: SymbExpr): Satisfiability` |
| `top(): L` | `assume(expression: SymbExpr): D` |
| `bottom(): L` | |

- **Abstract State, Value Domain e Heap Domain implementano entrambe.**
- Ogni istanza è un **elemento del reticolo**: il suo stato porta l'informazione astratta, gli operatori del reticolo la confrontano e combinano.
- Ogni istanza può fare da **pre-state**: gli operatori di `SemanticDomain` la trasformano in un **post-state**.
- **[aggiunta]** Corrispondenza con la teoria: `lessOrEqual` è $\sqsubseteq$, `lub` è $\sqcup$, `widening` è $\nabla$, `top`/`bottom` sono $\top$/$\bot$; `assign` e `smallStepSemantics` sono le funzioni di trasferimento astratte $[\![\cdot]\!]^\sharp$, `assume` è il filtro delle guardie e `satisfies` dice se un'espressione booleana è sempre vera, sempre falsa o ignota (`Satisfiability`), come serve a `Conditional` sopra.

### Main classes for value analyses
Gerarchia delle classi (pagina 63):

```
        Lattice : L                         SemanticDomain : D, E, I
          ^     ^ (dashed)                        ^
          |     |                                 |
 NonRelationalElement : T, F     FunctionalLattice : F, K, V     ValueDomain : D
  + satisfies(expr, env: F): Satisfiability  + getState(key: K): F      ^ (dashed)
  + assume(expr, env: F): F                  + putState(key: K, value: V): F
          ^                                       ^                     |
 NonRelationalDomain : T, F                 Environment : M, E, T, V ---+
  + eval(expr, env: F): T                    + eval(expr: SymbExpr): T
          ^                                       ^
 NonRelationalValueDomain : T               ValueEnvironment : T
```

- Ramo sinistro: il **valore astratto di una singola variabile** (es. un segno, un intervallo). `NonRelationalDomain` aggiunge `eval`, che valuta un'espressione dato un ambiente `env`.
- Ramo centrale: `FunctionalLattice` è un reticolo di funzioni (chiave → valore) con `getState`/`putState`; `Environment` lo specializza come mappa variabili → valori e implementa `ValueDomain`; `ValueEnvironment` è la classe concreta.
- Nel PDF ci sono anche delle etichette rosse che nella pagina renderizzata non si vedono (sono nel livello di testo ma coperte): vicino al ramo sinistro "values of variables", "lattice structure", "eval logic"; vicino a `ValueEnvironment` "variable mapping", "one instance per state", "NRVD for eval logic". **[aggiunta]** Lettura: chi scrive un dominio non relazionale implementa un `NonRelationalValueDomain` (valori delle variabili, struttura di reticolo, logica di valutazione); `ValueEnvironment` fa la mappa variabili → valori, ne esiste un'istanza per ogni stato astratto e delega la valutazione al NRVD.

## LiSA frontends
- **Linguaggi**: Go, Michelson, EVM bytecode, Python, LLVM, Java. Loghi dei frontend: **JLiSA**, **PyLiSA**, **GoLiSA**, **EVMLiSA**.
- **Temi di ricerca**: blockchain, stringhe, linguaggi dinamici, numeric trends, data science, interazioni modulari.
- **Didattica**: SCSR a UNIVE (usato da 4 anni), SASV a UNIPR, cioè questo corso (usato da 2 anni).

## GoLiSA
- **Goal**: rilevare il **non-determinismo negli smart contract scritti in Go**.
- **Why**: il non-determinismo nel software blockchain impedisce ai nodi di raggiungere uno **stato consensuale comune**, con conseguenti fork, blocchi, servizi negati.
- **How**: **analisi di non-interferenza**, cioè si traccia se valori non deterministici **fluiscono** in statement che possono modificare lo **stato globale della blockchain**.
- (Refusi nella slide: "non-determinism ... do not allow" va letto "does not allow"; "non-det values flows" va letto "flow".)

Esempio:

```go
func foo(id string) {
    var obj MyObject
    obj.ID = id
    obj.Date = time.Now()
    value, _ := json.Marshal(obj)
    store.Set(id, value)
}
```

- `time.Now()` è la **sorgente** non deterministica (evidenziata), `store.Set(id, value)` è il **sink** che scrive nello stato della blockchain (evidenziato). Le frecce rosse mostrano il flusso `time.Now()` → `obj` → `value` → `store.Set`: **Warning!**

Confronto sperimentale (tabella della slide):

| Tool | #Warnings | #TP | #FP | #FN |
|---|---|---|---|---|
| GoLiSA | 195 | 124 | 71 | 0 |
| ChainCode | 203 | 68 | 135 | 53 |
| Revive^CC | 351 | 79 | 272 | 1 |

- In ogni riga #TP + #FP = #Warnings. GoLiSA è l'unico **senza falsi negativi** e con meno falsi positivi.
- **[aggiunta]** Precisione di GoLiSA $124/195 \approx 64\%$. Nota: #TP + #FN non è uguale per i tre tool (124, 121, 80), quindi non sono misurati sullo stesso insieme di problemi reali; probabilmente ogni tool è valutato solo sulle categorie di non-determinismo che sa riconoscere (nella slide non è spiegato).

## EVMLiSA
- L'**EVM bytecode** è un linguaggio a basso livello basato su stack, eseguito dalla **Ethereum Virtual Machine**, il motore di esecuzione degli smart contract Ethereum. (Nella slide manca il sostantivo: "a stack-based low-level running on...", va letto "low-level language".)
- Il flusso di esecuzione si cambia con l'istruzione `JUMP`...
- ...ma la destinazione dei `JUMP` **non è scritta nel codice, è calcolata dinamicamente**. Esempio:

```
PUSH1 0x0A PUSH1 0x0C ADD JUMP
```

- **[aggiunta]** Si mettono sullo stack 0x0A e 0x0C, `ADD` li somma (0x16 = 22) e `JUMP` salta a quell'indirizzo, preso dalla cima dello stack: per sapere dove va l'arco del CFG bisogna conoscere il contenuto dello stack.
- **Goal**: costruire **CFG sound** per l'EVM bytecode.
- **How**: un dominio astratto **parametrico**, insiemi di (al più) $\ell$ stack astratti di altezza $h$ ("$\ell$-sized abstract $h$-sized stack set domain");
  - poi si usano gli stack inferiti per **aggiungere archi** al CFG...
  - ...finché non si scoprono più archi nuovi (nella slide "untile", refuso per "until").
- **[aggiunta]** È di nuovo un punto fisso: la costruzione del CFG e l'analisi si alternano, perché ogni arco nuovo può rendere raggiungibile codice che produce altri salti.
- **Checker di EVMLiSA**: reentrancy, timestamp dependency, `tx.origin`.

Confronto sperimentale:

| Tool | Precision (%) | Recall (%) | F-measure (%) |
|---|---|---|---|
| EVMLiSA | 93.75 | 100.00 | 96.77 |
| EtherSolve | 85.71 | 60.00 | 70.59 |
| Vandal | 41.67 | 100.00 | 58.82 |
| Mythril | 21.01 | 96.67 | 34.52 |

- **[aggiunta]** Le F-measure sono coerenti con precision e recall ($F = 2PR/(P+R)$, ricontrollate tutte e quattro). EVMLiSA ha recall 100% con la precisione più alta.

## LiSA latest news
Due ritagli di giornale (pagina 93):
- Articolo **"Analisi software: l'Università di Parma fra le prime nel mondo"** (Ricerca, premiata con Ca' Foscari): **JLiSA**, analizzatore sviluppato da UniPR e Ca' Foscari, ha preso la **medaglia di bronzo nella track Java di SV-COMP**, la principale competizione di verifica del software (nata nel 2012 per iniziativa di Dirk Beyer, LMU Monaco; risultati presentati a TACAS, che quell'anno si teneva a Torino ad aprile). Terzo posto alla prima partecipazione, unica tecnologia "100% made in Italy" in gara. Team: Vincenzo Arceri e lo studente magistrale Filippo Bianchi per UniPR; per Ca' Foscari il gruppo SSV di Agostino Cortesi e Pietro Ferrara, con Luca Negrini, Luca Olivieri e i dottorandi Giacomo Zanatta e Teodors Lisovenko. JLiSA è basato su LiSA.
- **ParmaToday, 23 dicembre 2025**: "La National Security Agency Usa sceglie un sistema di verifica software targato Università di Parma e Ca' Foscari". L'NSA ha deciso di usare LiSA per alcune attività. LiSA è iniziato a Ca' Foscari nel 2020 ed è sviluppato principalmente da Negrini, Arceri e Olivieri.

## Example: sign analysis
- Pagina 94: solo il titolo e l'icona di un monitor. L'esempio (un'analisi dei segni scritta in LiSA) è stato mostrato dal vivo e nel PDF non c'è.
- **[aggiunta]** In base alle classi viste sopra, un dominio dei segni è un dominio non relazionale: si implementa il valore di una variabile ($\bot$, $-$, $0$, $+$, $\top$) con le operazioni di reticolo (`lessOrEqual`, `lub`, `top`, `bottom`; il widening può coincidere con il lub perché il reticolo è finito) e la logica di `eval` per costanti ed espressioni binarie (le tabelle $+^\sharp$, $*^\sharp$ della lezione 07); la mappa variabili → segni la dà `ValueEnvironment`. I nomi esatti dei metodi da implementare dipendono dalla versione di LiSA e non sono nelle slide.

## Riferimenti (pagine 96-98)
- **LiSA**: Ferrara, Negrini, Arceri, Cortesi, *Static analysis for dummies: experiencing LiSA*, SOAP@PLDI 2021; Negrini, Ferrara, Arceri, Cortesi, *LiSA: A Generic Framework for Multilanguage Static Analysis*, Challenges of Software Verification 2023; Negrini, Arceri, Olivieri, Cortesi, Ferrara, *Teaching Through Practice: Advanced Static Analysis with LiSA*, FMTea 2024.
- **EVMLiSA**: Arceri, Merenda, Dolcetti, Negrini, Olivieri, Zaffanella, *Towards a Sound Construction of EVM Bytecode Control-Flow Graphs*, FTfJP@ECOOP 2024; Arceri, Merenda, Negrini, Olivieri, Zaffanella, *EVMLiSA: Sound Static Control-Flow Graph Construction for EVM Bytecode*, Blockchain: Research and Applications, 2025.
- **GoLiSA**: Olivieri et al., *Ensuring determinism in blockchain software with GoLiSA: an industrial experience report*, SOAP@PLDI 2022; *Information Flow Analysis for Detecting Non-Determinism in Blockchain*, ECOOP 2023; *Detection of Phantom Reads in Hyperledger Fabric*, IEEE Access 2024; *Static Detection of Untrusted Cross-Contract Invocations in Go Smart Contracts*, SAC 2025; *Detection of Read-Write Issues in Hyperledger Fabric Smart Contracts*, SAC 2025.
- **Stringhe e codice dinamico** (Arceri, Mastroeni): *Analyzing Dynamic Code: A Sound Abstract Interpreter for Evil Eval*, ACM TOPS 2021; *A sound abstract interpreter for dynamic code*, SAC 2020; con S. Xu, *Static Analysis for ECMAScript String Manipulation Programs*, Applied Science 2020; *Static Program Analysis for String Manipulation Languages*, VPT@Programming 2019.
- Ultima pagina: **Zulip workspace sull'abstract interpretation**, absint.zulipchat.com.

## Da ricordare
- LiSA è una **libreria** Java open source (UNIPR + UNIVE) per costruire analizzatori basati su abstract interpretation, multi-linguaggio e multi-dominio. **Non è un analizzatore completo**: il frontend che traduce il sorgente in CFG lo scrive l'utente.
- Pipeline: programma $P^i$ → **frontend** $L^i$ (language dependent) → **CFG** → LiSA (interprocedural analysis + call graph, CFG fixpoint, statement semantics, abstract state con heap e value domain, checks) → warning e dump.
- CFG: nodi = `Statement`, archi = `Edge`; LiSA **non fissa la semantica** di nessuno dei due.
- Fixpoint sul CFG: worklist, $out_n = \bot$ all'inizio, $in_{n_0} = \top$, entry = $\sqcup$ dei `traverse` dei predecessori, si aggiorna con $\oplus$ ($\sqcup$ o $\nabla$) solo se $tmp_n \not\sqsubseteq out_n$.
- Le chiamate le gestisce solo l'**interprocedural analysis** (configurabile) con il **call graph** (`cg.resolve(call)`): gli statement chiamanti chiedono `ia.getResult(this)`, la semantica degli statement non sa cosa fa il fixpoint, il resto di LiSA ignora le chiamate.
- Gli statement si scompongono in **`SymbolicExpression`**, riscritte dinamicamente sfruttando l'analisi (es. `+` come somma o `cat` secondo i tipi): i domini modellano solo quelle, non la sintassi.
- **Abstract state** = heap domain (riscrive gli accessi in memoria in variabili simboliche, es. `x.f` → `L1`) + value domain (vede solo variabili e costanti). Field-insensitive → **weak update** (`L1 → {5, 7}`), field-sensitive → `L1.f → {5}`, `L1.g → {7}`.
- Ogni dominio implementa **`Lattice`** (`lessOrEqual`, `lub`, `widening`, `top`, `bottom`) e **`SemanticDomain`** (`assign`, `smallStepSemantics`, `satisfies`, `assume`). Per i domini non relazionali si scrive un `NonRelationalValueDomain`, messo in un `ValueEnvironment`.
- Applicazioni: **GoLiSA** (non-determinismo negli smart contract Go via non-interferenza, 0 falsi negativi) ed **EVMLiSA** (CFG sound per EVM bytecode con jump calcolati, dominio di insiemi di stack astratti, F-measure 96.77%).
