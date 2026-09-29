# Spiegazione approfondita delle slide - da zero conoscenze

Questo file accompagna `SLIDES.pdf`. Spiega **ogni slida** partendo dal presupposto che chi legge non sappia nulla di compilatori, clang-tidy o LLM. Ogni acronimo è sciolto la prima volta che compare. Serve a te per padroneggiare i contenuti, e a chiunque voglia capire il seminario senza background.

> Legenda: 🟦 = concetto chiave · 💡 = perché conta · 🗣 = come dirlo a voce.

---

## Glossario lampo (i termini che tornano sempre)

| Termine | Significato in una riga |
|---|---|
| **Compilatore** | Programma che traduce il codice sorgente (testo che scrivi) in qualcosa che la macchina può eseguire. |
| **Clang** | Il compilatore C/C++/Objective-C del progetto LLVM. È anche una *libreria*: puoi usarne i pezzi nei tuoi programmi. |
| **LLVM** | Grande progetto open source di infrastrutture per compilatori. Clang è il suo front-end per il C++. |
| **Linter** | Strumento che analizza il codice e segnala problemi di stile, bug probabili o cattive pratiche, **senza eseguirlo**. |
| **clang-tidy** | Il linter "ufficiale" basato su Clang. Capisce il codice come lo capisce il compilatore. |
| **AST** | *Abstract Syntax Tree*, l'albero che rappresenta la struttura del programma. Vedi slide 4. |
| **Check** | Una singola regola di clang-tidy (es. "non usare printf"). Ne esistono centinaia; io ne scrivo una mia. |
| **Fix-it** | Correzione automatica che il check propone (e può applicare da solo). |
| **CI** | *Continuous Integration*, il sistema che ricompila e ricontrolla il codice a ogni modifica, in automatico. |
| **LLM** | *Large Language Model*, un modello di IA tipo ChatGPT o Claude, che genera testo/codice da un prompt. |
| **Deterministico** | Stesso input → sempre stesso output. clang-tidy lo è; un LLM no. |

---

## Slide 1 - Copertina

**Cosa c'è sulla slide:** titolo, sottotitolo, nome.

🟦 **Il messaggio:** sto per costruire da zero uno strumento che "capisce il codice, non solo il testo". Questa frase è il filo rosso di tutto il seminario.

🗣 *"Le mostro come si costruisce un check personalizzato di clang-tidy da zero, lo si testa e lo si confronta con un LLM."*

---

## Slide 2 - Il problema

**Cosa c'è sulla slide:** una citazione (il fastidio in code review) + 3 punti.

🟦 **Il punto di partenza:** in C++ moderno esiste un modo migliore di `printf` per stampare a schermo (`std::print`, type-safe). Ma nei progetti veri `printf` continua a comparire. Vorremmo che il controllo lo facesse la macchina, automaticamente.

**Perché non basta `grep`/regex?**
- **`grep`** = comando Unix che cerca una stringa di testo dentro i file.
- **Regex** (espressione regolare) = un modo per descrivere pattern di testo (es. "trova la parola printf").

Entrambi guardano **i caratteri**, non il **significato**. Esempi in cui sbagliano:
- `// printf(...)` → è un commento, non codice. grep lo segnala, ma è un **falso positivo**.
- `"contiene printf nella stringa"` → è testo dentro le virgolette, non una chiamata.
- `mylib::printf(...)` → è un'altra funzione con lo stesso nome, definita dall'utente. grep non sa distinguerla.

💡 **Conclusione:** serve uno strumento che ragioni su **tipi e scope** (cioè: di che tipo è questa cosa? a quale funzione si riferisce davvero?), esattamente come fa il compilatore.

> **Scope** = il "contesto di visibilità" di un nome. `printf` globale e `mylib::printf` hanno lo stesso nome breve ma vivono in scope diversi: sono due cose distinte.

---

## Slide 3 - Architettura di clang-tidy

**Cosa c'è sulla slide:** il diagramma a 6 box.

🟦 **L'idea forte:** Clang non è una scatola nera che "ingoia codice e sputa un eseguibile". È fatto di pezzi riusabili come una **libreria**. Possiamo agganciarci a metà strada.

Il flusso, box per box:
1. **codice.cpp** → il file sorgente che scrivo.
2. **clang frontend** → la prima parte del compilatore: legge il testo, controlla che sia C++ valido, capisce i tipi.
   - *Frontend* = la parte "davanti" del compilatore, quella che legge e capisce il sorgente (in contrapposizione al *backend*, che genera il codice macchina).
3. **AST + semantica** → il risultato: l'albero della struttura del programma, **con il significato già calcolato** (tipi risolti, funzioni giuste collegate). Vedi slide 4.
   - *Semantica* = il significato del codice, non solo la sua forma. "Che tipo ha `x`? Quale funzione viene chiamata davvero?"
4. **AST matchers** 🔴 → *qui scrivo io*. Descrivo quali nodi dell'albero mi interessano. Vedi slide 5.
5. **check** 🔴 → *qui scrivo io*. La logica che reagisce: "ho trovato un printf → emetti un avviso".
6. **diagnostica + fix-it** → l'output: il messaggio di warning e la correzione automatica.

💡 **Perché conta:** dei 6 pezzi, **solo 2 sono nostri** (in rosso). Tutto il lavoro difficile - capire il C++, risolvere i tipi - è già fatto da Clang e ce lo regala. È questo che rende fattibile scrivere un check in <50 righe.

---

## Slide 4 - Cos'è l'AST, in 6 righe

**Cosa c'è sulla slide:** un comando + l'albero stampato.

🟦 **AST = Abstract Syntax Tree** (albero sintattico astratto). È il programma rappresentato come un **albero** invece che come testo. Ogni costrutto del linguaggio diventa un **nodo**.

Il comando della slide chiede a Clang di stampare l'AST di `int x = (int)3.14;`. Risultato:

```
TranslationUnitDecl                          ← l'intero file
└── VarDecl 'x' 'int'                         ← "dichiaro la variabile x, di tipo int"
    └── CStyleCastExpr 'int' <FloatingToIntegral>  ← "c'è un cast a int"
        └── FloatingLiteral 'double' 3.14     ← "il valore di partenza è 3.14, un double"
```

Termini:
- **TranslationUnitDecl** = la radice, rappresenta tutto il file compilato (una *translation unit* = un file sorgente con i suoi include).
- **VarDecl** = *Variable Declaration*, la dichiarazione di una variabile.
- **CStyleCastExpr** = l'espressione di cast in stile C, cioè `(int)qualcosa`. Nota: porta scritto il tipo di arrivo (`int`) e il tipo di partenza.
- **FloatingToIntegral** = "da numero con virgola a numero intero". È l'informazione semantica: Clang **sa** che qui un `3.14` diventerà `3`.
- **FloatingLiteral** = un valore numerico con la virgola scritto direttamente nel codice (`3.14`).

💡 **Il punto chiave:** il cast non è la stringa `"(int)"`. È un **nodo tipato** che porta con sé tutta l'informazione di significato. I check ragionano su *questo*, non sul testo. Per questo non si fanno fregare da commenti, stringhe e nomi simili.

---

## Slide 5 - Gli AST Matchers

**Cosa c'è sulla slide:** due esempi di matcher.

🟦 **DSL = Domain-Specific Language** (linguaggio specifico di dominio). È un mini-linguaggio fatto per un solo scopo. Qui lo scopo è: "descrivere quali nodi dell'AST voglio trovare".

Primo esempio, da leggere **dall'esterno all'interno**:
```cpp
callExpr(callee(functionDecl(hasName("::printf"))))
```
- `callExpr` = una *call expression*, cioè una chiamata di funzione (qualcosa come `f(...)`).
- `callee` = "il chiamato", cioè la funzione che viene invocata.
- `functionDecl` = *function declaration*, una dichiarazione di funzione.
- `hasName("::printf")` = "che si chiama `::printf`".

Tutto insieme: **"trova ogni chiamata a una funzione il cui nome è `::printf`"**.

> Il `::` davanti a `printf` significa "nel namespace globale", cioè la `printf` "vera" del C, non una con lo stesso nome definita da qualcun altro. Questo è ciò che permette di **non** confondere `printf` con `mylib::printf`.

Secondo esempio: `cxxMethodDecl(isVirtual(), unless(isOverride()))` = "ogni metodo virtuale che non è un override" (un altro tipo di regola, mostrato solo per far vedere che il DSL è generale).

💡 **Perché è bello:** è **dichiarativo** - dici *cosa* cercare, non *come* girare l'albero a mano. L'alternativa manuale si chiama `RecursiveASTVisitor` (un "visitatore" che scende nodo per nodo): funziona ma è molto più verboso.

---

## Slide 6 - Anatomia di un check

**Cosa c'è sulla slide:** la dichiarazione della classe `NoPrintfCheck`.

🟦 Ogni check è una **classe C++** che eredita da `ClangTidyCheck` (la classe base fornita da clang-tidy) e implementa **due funzioni** ("hook", cioè agganci):

- `registerMatchers(...)` → **QUALI** nodi cerco (vedi slide 7).
- `check(...)` → **COSA** faccio quando ne trovo uno (vedi slide 8).

Termini:
- **Classe / ereditare** = concetto di programmazione a oggetti: `NoPrintfCheck` "è un" `ClangTidyCheck` e ne riusa il comportamento, aggiungendo il proprio.
- **override** = "ridefinisco una funzione che la classe base aveva già previsto". Qui riempio i due hook che il framework si aspetta.
- **StringRef, ClangTidyContext** = tipi di Clang passati al costruttore; non serve capirli in dettaglio, sono "il contesto" in cui gira il check.

💡 **Perché è corta:** tutta la fatica (leggere il file, controllare i tipi, capire gli scope) la fa il **driver** di clang-tidy. Io riempio solo i due buchi con la mia regola.

---

## Slide 7 - Il nostro check: `misc-no-printf`

**Cosa c'è sulla slide:** "cosa fa" + "perché didatticamente".

🟦 **Il nome `misc-no-printf`:** in clang-tidy i check sono raggruppati per categoria. `misc` = *miscellaneous* (varie), la categoria dei check generici. `no-printf` = cosa fa.

Cosa fa, in concreto:
- segnala `::printf` di **libc** (la libreria standard del C, dove vive la `printf` originale);
- **non** segnala `mylib::printf` → è una funzione diversa, in un altro scope, definita dall'utente;
- propone un **fix-it** che sostituisce il nome con `std::print`.
  - **`std::print`** = la funzione di stampa introdotta in **C++23** (lo standard del 2023). È *type-safe*: controlla i tipi degli argomenti a tempo di compilazione, cosa che `printf` non fa (con `printf` puoi sbagliare i formati e avere bug silenziosi).

💡 **Perché è un buon esempio per il seminario:** è abbastanza semplice da spiegare in 15 minuti, ma tocca i 3 casi che fanno fallire un'analisi testuale: **scope** (namespace), **macro**, **template**. Quindi dimostra il valore vero dell'AST.

---

## Slide 8 - `registerMatchers`

**Cosa c'è sulla slide:** il codice del matcher (8 righe).

🟦 Qui dichiaro il pattern da cercare. È la stessa frase della slide 5, con due aggiunte:

```cpp
callExpr(
  callee(functionDecl(hasName("::printf"))),   // chiamate a ::printf
  unless(isExpansionInSystemHeader())          // ma non dentro header di sistema
).bind("printfCall")                            // dai un'etichetta al match
```

- `hasName("::printf")` → come detto, aggancia il nome **globale e qualificato**. Niente collisioni con `printf` dell'utente. È **il** dettaglio che rende il check intelligente.
- `unless(...)` → "a meno che". `unless(isExpansionInSystemHeader())` = "escludi i match che provengono dall'espansione di un header di sistema".
  - **Header di sistema** = i file di libreria come `<cstdio>`, `<iostream>`. Senza questa esclusione, ogni volta che includi `<cstdio>` (che *contiene* la dichiarazione di printf) avresti rumore non tuo.
  - **Espansione** = quando il preprocessore "incolla" il contenuto degli header dentro il tuo file.
- `.bind("printfCall")` → mette un'**etichetta** sul nodo trovato, così nella funzione `check` possiamo ripescarlo per nome.

💡 **Take-away:** tutta l'intelligenza "di scope" è in `hasName("::printf")`; tutta la pulizia dell'output è in `unless(...)`.

---

## Slide 9 - `check` + diagnostica + fix-it

**Cosa c'è sulla slide:** il codice della funzione `check`.

🟦 Questa funzione viene chiamata **una volta per ogni match**. Fa 3 cose:

```cpp
const auto *Call = R.Nodes.getNodeAs<CallExpr>("printfCall");  // 1. ripesco il nodo
const Expr *Callee = Call->getCallee()->IgnoreImpCasts();      // 2. trovo il "printf"
diag(Callee->getBeginLoc(), "uso di 'printf' ... usare 'std::print'")  // 3a. avviso
  << FixItHint::CreateReplacement(                              // 3b. correzione
       SourceRange(Callee->getBeginLoc(), Callee->getEndLoc()),
       "std::print");
```

1. **`getNodeAs<CallExpr>("printfCall")`** → recupera il nodo che avevamo etichettato con `.bind`.
2. **`getCallee()->IgnoreImpCasts()`** → prende la parte "chiamata" (il token `printf`). `IgnoreImpCasts` salta eventuali conversioni implicite che Clang ha inserito, così puntiamo esattamente al nome.
3. **`diag(...)`** → emette la **diagnostica** (il messaggio di warning), ancorata alla posizione del `printf`.
   - **`FixItHint::CreateReplacement(range, "std::print")`** → la **correzione automatica**: "sostituisci l'intervallo di testo che copre `printf` con `std::print`".
   - **`SourceRange(begin, end)`** = l'intervallo di sorgente da `begin` a `end`, cioè esattamente il token `printf`.

💡 **Perché è importante "solo il token":** non riscriviamo l'intera riga, solo il nome. Così il fix è **chirurgico, sicuro e idempotente** (applicarlo due volte non rompe nulla) e clang-tidy può applicarlo in automatico su migliaia di file a ogni PR (*Pull Request* = una proposta di modifica al codice).

---

## Slide 10 - Divider "Demo"

Slide di transizione, solo titolo. 🗣 *"Basta codice, vediamolo all'opera."*

---

## Slide 11 - Demo 1: esempi mirati + confronto LLM

**Cosa c'è sulla slide:** due comandi + la tabella di confronto.

**Parte demo (i comandi):**
- snippet 02 (collisione di namespace) → **1 solo hit**: il check segnala `::printf` ma ignora `mylib::printf`. Prova che capisce lo scope.
- snippet 06 (il caso tosto): c'è un `using logging::printf;` che cambia quale funzione viene scelta. La **overload resolution** (vedi sotto) fa sì che `::printf("...", 1)` con un argomento `int` venga in realtà risolta al template `logging::printf`, **non** alla printf di libc. Il check lo sa e segnala solo l'unica chiamata davvero a libc.
  - **Overload resolution** = il meccanismo con cui C++ sceglie *quale* funzione chiamare quando ne esistono più con lo stesso nome ma argomenti diversi. È un calcolo che fa il compilatore, non si vede nel testo.
  - **Template** = una funzione "stampo" parametrica sul tipo, da cui il compilatore genera versioni concrete.

**Parte confronto (la tabella):** ho dato gli stessi 6 snippet a due LLM - **Claude Opus 4.7** e **ChatGPT 5.5** - facendo **24 run** in totale (6 snippet × 2 modelli × 2 chat ripetute, per testare anche la coerenza).

Cosa dicono le righe:
- **Determinismo:** clang-tidy dà sempre lo stesso risultato (100%). Gli LLM no.
- **Fix primario `std::print`:** Claude lo propone in 4 casi su 6; ChatGPT **mai** come prima scelta (preferisce `std::cout`/`std::printf`).
- **Snippet 06:** clang-tidy → sempre 1 hit corretto. Gli LLM → nelle due chat ripetute danno risposte **opposte**.
- **Bug fuori scope (`2.5→2`):** in un altro snippet c'è `static_cast<int>(2.5)` che tronca silenziosamente 2.5 a 2 (perdita di precisione). Il check **non** lo vede (non è il suo compito), ma **entrambi gli LLM sì**.

💡 **Il risultato più significativo:** sullo snippet 06, lo **stesso modello**, interrogato **due volte con lo stesso prompt**, dà due interpretazioni tecniche opposte dello stesso codice. Questo è il cuore del confronto: l'LLM non è deterministico nemmeno con se stesso.

---

## Slide 12 - Demo 2: progetti veri

**Cosa c'è sulla slide:** due casi reali con i comandi.

**Caso A - `bear_demo` (build con Make):**
- **Make** = un vecchio e diffuso sistema per compilare progetti, guidato da un `Makefile`.
- **Bear** = *Build EAR*, uno strumento che "ascolta" la tua build e registra come ogni file viene compilato, producendo un `compile_commands.json`.
  - **`compile_commands.json`** = il "database di compilazione": elenca, per ogni file, il comando esatto con cui va compilato (flag, include, ecc.). clang-tidy ne ha bisogno per analizzare un file esattamente come lo vede il compilatore.
- Risultato: **5/5 hit, 0 falsi positivi**.
- 🗣 *Pattern realistico:* erediti un progetto con un suo sistema di build e ci attacchi un linter **senza riscrivere nulla**.

**Caso B - `tinyxml2` (libreria reale, build CMake):**
- **CMake** = un generatore di build moderno, molto usato. Con `-DCMAKE_EXPORT_COMPILE_COMMANDS=ON` produce direttamente il `compile_commands.json` (senza bisogno di Bear).
- `--extra-arg=-isysroot $(xcrun --show-sdk-path)` = su macOS bisogna dire al check dove sono gli header di sistema (l'**SDK**, *Software Development Kit*); altrimenti non li trova.
- Risultato: **28 hit in 0.2 secondi**.

💡 **Il numero da ricordare:** su tinyxml2, `grep printf` trova **42** corrispondenze, clang-tidy ne segnala **28**. I **14 di differenza** sono commenti, stringhe, e funzioni con nome simile ma diverse (`vfprintf`, `snprintf`) o macro. Quei 14 sono **esattamente i falsi positivi** che un linter testuale produrrebbe. *Questo* è il valore misurabile dell'analisi AST.

---

## Slide 13 - Test, documentazione, integrazione

**Cosa c'è sulla slide:** 4 punti.

Un check "serio" non è solo codice; deve essere testato, documentato e integrabile:

- **Test in stile lit:** **lit** = *LLVM Integrated Tester*, il framework con cui LLVM testa tutto. Un test lit è un file con commenti speciali `// RUN: ...` e `// CHECK: ...` che descrivono *cosa lanciare* e *cosa aspettarsi*. Il nostro test gira dentro la **build farm** ufficiale di LLVM (l'insieme di macchine che compilano e testano il progetto) e verifica sia il messaggio sia il fix applicato.
- **Documentazione in `.rst`:** **reStructuredText**, il formato di documentazione usato da LLVM. Ogni check ufficiale ha la sua pagina; ho scritto la mia nello stesso formato.
- **Integrazione CI:** **CI** = *Continuous Integration*. `clang-tidy --warnings-as-errors='*'` trasforma ogni warning in **errore** → se il check trova un `printf`, la pipeline fallisce e la modifica **non viene accettata** (merge bloccato).
- **Distribuzione:** il check si compila come parte di **`clang-tools-extra`** (il pacchetto di tool extra di Clang, dove vivono tutti i check di clang-tidy) → potrebbe essere proposto **upstream**, cioè contribuito al progetto ufficiale.

💡 **Messaggio:** non è un giocattolo. Segue esattamente il percorso di un check vero di LLVM.

---

## Slide 14 - Take-away

**Cosa c'è sulla slide:** quando sì / quando no + complementarità.

🟦 **Quando conviene scrivere un check custom:**
- c'è un **pattern interno ricorrente** (una cosa che nel tuo team capita spesso);
- la regola è **deterministica** (o è giusto o è sbagliato, senza sfumature);
- esiste un **fix riapplicabile** automaticamente.

**Quando NON conviene:**
- la regola è **sfumata** ("questo codice è poco leggibile") → meglio una review umana o un LLM;
- è uno **stile generico** → probabilmente esiste già un check ufficiale, non reinventarlo.

🟦 **La tesi finale - complementarità, non competizione:**
- **clang-tidy** è imbattibile dove la risposta è **deterministica**: scope, tipi, overload resolution. Veloce, gratuito, ripetibile su milioni di righe.
- **gli LLM** trovano bug **fuori dal mandato** del check (come il troncamento `2.5 → 2`), ma sulla precisione "di compilatore" **fluttuano**: stesso codice, risposte diverse.

🗣 **La chiusura:** *"La domanda non è 'meglio clang-tidy o LLM', ma 'che tipo di domanda stai facendo al codice'. Se ha una risposta deterministica, vince clang-tidy. Se richiede comprensione del contesto, vince l'LLM."*

---

## Appendice - risposte rapide a domande "da zero"

**Perché `printf` è considerato cattivo in C++?**
Non è "cattivo", è *vecchio*. Non controlla i tipi: se scrivi `printf("%d", "ciao")` (formato intero, ma passi una stringa) il compilatore spesso non se ne accorge e ottieni comportamento indefinito. `std::print` controlla tutto a compile time.

**Che differenza c'è tra un linter e un compilatore?**
Il compilatore deve produrre l'eseguibile e segnala solo errori che impediscono la compilazione. Il linter è più "opinionato": segnala cose che *compilano benissimo* ma sono cattive idee (come `printf` in C++ moderno).

**Perché non usare semplicemente un LLM per tutto?**
Tre motivi: **costo** (ogni run costa token), **velocità** (un LLM su 100.000 file è impraticabile; clang-tidy ci mette millisecondi a file), **determinismo** (in CI vuoi che la stessa modifica dia sempre lo stesso esito - un LLM non lo garantisce).

**Cosa significa "scrivere un check da zero" in pratica?**
Buildare LLVM da sorgente (~30 min la prima volta), aggiungere una classe C++ con due funzioni, registrarla, scrivere un test lit, documentarla in `.rst`. Il codice della regola è <50 righe; il resto è infrastruttura e verifica.
