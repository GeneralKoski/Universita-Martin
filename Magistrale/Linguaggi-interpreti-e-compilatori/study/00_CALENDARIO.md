# 00 - Calendario giorno per giorno verso l'orale

> **ORALE: giovedì 10 settembre 2026.** Seminario svolto il 23 giugno 2026 (30% del voto, già in cassaforte): resta solo l'orale, che pesa il **70%**.
>
> **Ripianificato il 25 agosto 2026.** La versione precedente partiva dall'11 agosto e nessuno dei suoi blocchi è stato svolto: le due settimane 11-24 agosto (front end, parsing, IR, middle end locale, ~19h) sono state perse. Questo calendario riparte da zero su **16 giorni**, dal 25 agosto al 9 settembre.

Questo file è il piano operativo giorno per giorno. I blocchi tematici e il metodo stanno in [`README.md`](README.md); qui c'è solo *cosa apro oggi*.

---

## Il vincolo nuovo: 16 giorni, ~35h, zero margine

| | |
|---|---|
| Carico residuo | **~35h** (19h studio + 1.5h laboratorio + 3.5h cheatsheet + 4h domande + 2.5h incrocio + 4.5h ripasso) |
| Giorni disponibili | 16 (25 ago - 9 set) |
| Capienza pianificata | 12 giorni lavorativi × 2h + 4 giorni di weekend × 4h = **40h** |
| Margine | ~5h, cioè **due mezze giornate di recupero in tutto** |

Il piano precedente aveva 30 giorni per 32h: si poteva sforare senza conseguenze. Adesso no. **Un giorno saltato va recuperato nel weekend immediatamente successivo**, non rimandato.

### Cosa è stato tagliato per far entrare tutto

- **Laboratorio: da 4h a 1.5h.** Sopravvive solo la parte interrogabile all'orale, cioè `calc-2` vs `calc-2-prec` con `calc.output` sotto gli occhi (sabato 29). I 4 binari di TinyP, il `diff` LLVM `-O0`/`-O2` e la modifica al lexer Flex diventano **opzionali**: si fanno solo se un blocco chiude in anticipo.
- **Domande tipo: un passaggio completo + uno selettivo**, non due completi (domenica 6 e lunedì 7).
- **Domande incrocio: 2h invece di 3**, compresse su lunedì 7 e martedì 8 insieme alla simulazione.

Non è stato toccato: il parsing (4h piene + 1.5h di Bison, è l'argomento coperto peggio) e il ripasso finale del 7-9 settembre.

Per il laboratorio di sabato 29 serve **bison**, che sulla macchina Windows non è installato (flex e g++ sì).

---

## ✅ Materiale: completo e allineato con Elly (11/08/2026)

Le due sezioni sull'analisi sintattica, mai scaricate, sono state recuperate via API:

- `5b_Analisi_sintattica/` - slide EaC **08-14** in doppio formato: 6 pptx + 5 pdf `-1up`
- `5c_Esercitazione_su_analisi_sintattica/` - `Bison.pdf` del docente + **6 parser compilabili** (`calc-1`, `calc-2`, `calc-2-prec`, `calc-3`, `calc-3-rpn`, `Wait`)

Entrambe hanno il loro `RIASSUNTO.md`. Nient'altro manca: le slide EaC 13, 19, 21 e 28 su Elly non esistono. Integrità verificata su tutti i 50 PDF/slide.

---

## Settimana 1 (25-30 agosto) - tutto il front end

### Martedì 25 - inquadramento + avvio lexer (2h)
- [ ] `1_Introduzione_al_corso/RIASSUNTO.md` + `Intro.pdf`
- [ ] `2_Interpreti_e_compilatori/RIASSUNTO.md` + `Interpreti-Compilatori.pdf`
- [ ] `3_Struttura_del_compilatore/RIASSUNTO.md` + `Struttura-Compilatore.pdf`
- [ ] `4_Analisi_lessicale/RIASSUNTO.md` + inizio `Analisi-Lessicale.pdf`

**Obiettivo:** disegnare front-end / middle-end / back-end a memoria, e sapere quale formalismo abita ogni fase. Le prime tre lezioni sono corte: non dilatarle, servono da telaio per tutto il resto.

### Mercoledì 26 - analisi lessicale completa (2h)
- [ ] `4_Analisi_lessicale/DFA.pdf` + EaC `05-Regular_Expressions_NFAs_DFAs.pptx`, `06-Building_Scanners.pptx`
- [ ] `07-DFA_Minimization.pptx` + `note.txt`
- [ ] `Flex.pdf` + `5_Esercitazione_su_analisi_lessicale/RIASSUNTO.md`, `lexer-cpp.ll` letto riga per riga

**Obiettivo:** catena RE → NFA (Thompson) → DFA (subset construction) → DFA minimo, e la distinzione specifica/implementazione.

⚠️ Il prof ha trattato **solo Hopcroft**, non Moore né Brzozowski. Punto in cui si inciampa: la definizione precisa di `δ⁻¹(s, c)` nella worklist.

### Giovedì 27 - parsing I, top-down (2h)
- [ ] `notes/08_parsing.md` §1-3: CFG e derivazioni, gerarchia dei parser, LL(1) con FIRST/FOLLOW
- [ ] `5b_Analisi_sintattica/RIASSUNTO.md` per orientarti nella cartella
- [ ] `L10ParseIntro-1up.pdf` (26 pag), `L11TopDown-1up.pdf` (28 pag)

⚠️ Leggere `notes/08_parsing.md` **prima** delle slide EaC: è in italiano e sintetico, dà la struttura in cui incastrare le slide inglesi. Il contrario ti fa annegare nei dettagli delle tabelle.

### Venerdì 28 - parsing II, tabella LL(1) sulle mani (2h)
- [ ] `L12TopDownII-1up.pdf` (27 pag): discesa recursiva e parser LL(1)
- [ ] Su carta: FIRST/FOLLOW e tabella LL(1) della grammatica della domanda 14 di `notes/04_domande_tipo.md`

Questo è il primo punto in cui si scrive invece di leggere. Se la tabella non viene, il problema è FIRST/FOLLOW: torna su `notes/08_parsing.md` §3 prima di passare al bottom-up.

### Sabato 29 - parsing III bottom-up + Bison (4h)

**Blocco A, teoria LR (2.5h)**
- [ ] `notes/08_parsing.md` §4-7: LR(1) con item e handle, conflitti, LALR(1) e Bison, precedenza di operatori
- [ ] `L13Transition-1up.pdf` (29 pag), `L14LRParsers-1up.pdf` (55 pag - il più corposo della serie)
- [ ] `14-Parsing_Wrap_up.pptx` (esiste solo in pptx): il confronto finale LL vs LR

Se ti perdi sull'esecuzione shift-reduce, apri i pptx: lì l'animazione passo-passo **è** il contenuto.

**Blocco B, Bison e laboratorio (1.5h)**
- [ ] `5c_Esercitazione_su_analisi_sintattica/RIASSUNTO.md` + `Bison.pdf`
- [ ] La progressione dei `calc.yy`: `calc-1` (riconoscitore) → `calc-2` (interprete, precedenza **strutturale** in expr/term/factor) → `calc-2-prec` (grammatica piatta ambigua + `%left`/`%right`/`%prec UMINUS`) → `calc-3` (compilatore verso RPN) → `calc-3-rpn` (interprete di RPN)

```bash
cd 5c_Esercitazione_su_analisi_sintattica/calc-2 && make && echo "2+3*4" | ./calc
```

- [ ] **Aprire `calc.output`** (il Makefile passa `--report=all`): stati LR, item, tabelle e conflitti. È la teoria del Blocco A resa visibile
- [ ] `cd ../Wait && make`: verificare se Bison segnala conflitti e di che tipo

Il confronto `calc-2` vs `calc-2-prec` è una domanda d'orale quasi obbligata: stesso linguaggio, precedenza ottenuta in due modi opposti, con costi opposti. ⚠️ Serve **bison** installato (`winget`/MSYS2), oppure fai il blocco B sul Mac.

### Domenica 30 - analisi dipendente da contesto + IR (4h)

**Blocco A, context-sensitive (2h)**
- [ ] `6_Analisi_dipendente_da_contesto/RIASSUNTO.md` + `L16ContextSensitive-1up.pdf` + EaC `15-...I.pptx`
- [ ] `L17AdHoc-1up.pdf`, `L18TypeAnalysis-1up.pdf`, EaC `16-...II.pptx`
- [ ] `TinyP/ast.hh` e `ast_visitor.hh`: il visitor pattern è l'esempio concreto da citare

**Obiettivo:** attribute grammar, attributi sintetizzati vs ereditati, non ciclicità, valutazione single-pass. La frase chiave del corso: le risposte dipendono da **valori**, non da parti del discorso, e richiedono **calcolo non locale**. Per questo in pratica vince l'ad-hoc SDT sul formalismo delle AG.

**Blocco B, IR (2h)**
- [ ] `7_Rappresentazione_intermedia_(IR)/RIASSUNTO.md` + `LLVM-IR.pdf` + EaC `17-Intermediate_Representations.pptx`

**Obiettivo:** classificazione IR (strutturale/lineare/ibrida), 3-address code, forma SSA, `phi`, `getelementptr`.

---

## Settimana 2 (31 agosto - 6 settembre) - back end, middle end, memorizzazione

### Lunedì 31 - astrazione procedurale (2h)
- [ ] EaC `18-The_Procedure_Abstraction_I.pptx`, `20-Procedure_Abstraction_III.pptx`

**Obiettivo:** activation record, calling convention (pre-call, prologo, epilogo, post-call), catena degli access link, per valore vs per riferimento.

⚠️ Compile-time vs run-time: l'AR esiste a run-time, il codice che lo costruisce è emesso a compile-time.

### Martedì 1 - OOL e code shape (2h)
- [ ] EaC `22-Support_for_OOLs.pptx`, `23-Support_for_Inheritance_in_OOLs.pptx` → vtable, ereditarietà singola e multipla
- [ ] EaC `24-Code_Shape_I`, `25-Code Shape_II`, `26-Code Shape_III` → array e matrici, stringhe C vs Pascal, short-circuit, if-then-else e cicli, le 3 strategie del `case`

Sono 5 slide set in 2h: vanno sfogliate con l'occhio sui punti chiave del `RIASSUNTO.md`, non lette pagina per pagina.

### Mercoledì 2 - ottimizzazioni locali e dominatori (2h)
- [ ] `8_Il_middle_end_analisi_e_ottimizzazioni/RIASSUNTO.md`
- [ ] EaC `27-...local_value_numbering.pptx`, `29-...SVN_and_Loop_Unrolling.pptx`
- [ ] `08Dominators-1up.pdf` → dominatori, dominatore immediato, DVN

### Giovedì 3 - dataflow globale (2h)
- [ ] EaC `30-Global_Optimization_Live_Analysis.pptx`
- [ ] `13DFA-1up.pdf`, `09GlobalOptimization-1up.pdf`, `14Proliferation-1up.pdf`, `19Clean-1up.pdf`
- [ ] `notes/06_dataflow.md`: le 4 analisi classiche (Live, Reaching, Available, Very Busy) nello stesso framework

È il giorno da cui dipendono più domande d'orale di qualsiasi altro. Se qualcosa deve sforare, che sfori qui.

### Venerdì 4 - interpretazione astratta (2h)
- [ ] `9_Cenni_su_interpretazione_astratta/RIASSUNTO.md` + `cousot-tutorial.pdf` + `note.txt`
- [ ] `mine-tutorial.pdf`: Knaster-Tarski e Kleene, Galois connection, domini (segni, intervalli, congruenze, octagons, **polyhedra**), widening

⚠️ Non basta dire "esiste un punto fisso": va giustificato. Ed è qui che si chiude il cerchio col dataflow di ieri.

⚠️ **Zaffanella è co-autore della Parma Polyhedra Library.** I poliedri sono il suo campo di ricerca, quindi questo capitolo pesa più di quanto suggerisca il titolo "Cenni su". Non liquidare polyhedra come "troppo costoso, in pratica non si usa": parlane come trade-off precisione/costo, con octagons come compromesso. Se ti chiede un approfondimento sul widening, probabilmente vuole arrivare al widening sui poliedri.

### Sabato 5 - cheatsheet a memoria (4h)
- [ ] `notes/02_cheatsheet.md`, parte 1: le 4 equazioni dataflow con tabella direzione/meet/init/fixpoint, Hopcroft, LVN
- [ ] Blocco parsing: algoritmo FIRST/FOLLOW, regola di riempimento della tabella LL(1) e condizione di LL(1)-ità, item LR(1) con `closure`/`goto`, tabella dei due conflitti, direttive di precedenza Bison
- [ ] Parte 2: formula GEP, Galois connection, Knaster-Tarski/Kleene, calling convention, activation record, vtable
- [ ] Prima lettura di `notes/03_glossario.md`

Memorizzare significa **riscrivere su carta a libro chiuso**, non rileggere. Le 4 equazioni si riscrivono da zero almeno due volte.

### Domenica 6 - 62 domande a voce, passaggio completo (4h)
Rispondere **a voce**, cronometrando 2-3 minuti ognuna. Le domande con traccia di risposta (quelle dell'audit del 05/05 e le 58-62 su Bison) sono autovalutazione: rispondi prima, confronta dopo.
- [ ] Domande **1-19**: introduzione e struttura, front end, analisi sintattica
- [ ] Domande **20-41**: IR e back end, middle end
- [ ] Domande **42-62**: interpretazione astratta, strumenti, domande trick, esercitazione Bison
- [ ] Annotare la lista delle domande in cui hai esitato → è il programma di domani

---

## Finale (7-10 settembre)

### Lunedì 7 - recupero esitazioni + incrocio (2h)
- [ ] Secondo passaggio **solo** sulle domande annotate ieri
- [ ] `04_domande_incrocio.md` D1: pipeline completa di compilazione di un C++ con virtual methods

### Martedì 8 - incrocio + simulazione (2h)
- [ ] `04_domande_incrocio.md` D2 (constant propagation con loop: dataflow vs astratta) e D3 (middle end di Clang vs interpretazione astratta)
- [ ] Simulazione orale a voce, 30-40 minuti di fila, senza fermarsi
- [ ] I disegni: RE → NFA → DFA → DFA minimo, Live Variables su un CFG di 4 nodi
- [ ] Riscrivere a memoria su carta le 4 equazioni dataflow

### Mercoledì 9 - ripasso intensivo (2h)
- [ ] Solo le sezioni "Punti chiave per l'orale" degli 11 `RIASSUNTO.md`
- [ ] `notes/05_pipeline_compilatore.md` per il quadro d'insieme, `notes/03_glossario.md`
- [ ] [`08_ripasso_intensivo.md`](08_ripasso_intensivo.md) e nient'altro

**Niente cose nuove.** Se non l'hai studiato finora, non lo studi adesso. A letto entro le 23.

### Giovedì 10 - ORALE

---

## Regole del piano

- **Il ripasso 7-9 settembre è intoccabile.** Se qualcosa sfora, si sacrificano nell'ordine: il laboratorio opzionale (TinyP, `diff` LLVM), poi le domande incrocio D2/D3, poi il secondo passaggio sulle domande. Mai il ripasso, mai il parsing
- **Il recupero è nel weekend, non "domani".** Con 5h di margine su 16 giorni, un giorno rimandato che scivola in avanti si porta dietro tutti gli altri
- **Ogni argomento si chiude a voce**, sulla sezione "Punti chiave per l'orale" del riassunto. Se lo leggi e ti sembra chiaro ma non riesci a dirlo, non lo sai
- Il progetto `misc-no-printf` del seminario resta un **esempio concreto da citare all'orale** (front end di Clang, AST matcher, diagnostica): `Martin/1_clang-tidy_custom_check/RESULTS.md`
- LIC è da **9 CFU**: pesa il 50% in più di un esame da 6. Sui numeri attuali (media 28,00 su 5 esami votati) un **30** porta il voto di partenza da 102,66 a ~104,4; un **28** lo lascia invariato; un **26** lo fa scendere a ~101,0
- I file `02_cheatsheet.md`, `03_domande_tipo.md` e `06_pratica_script.md` di questa cartella sono symlink che su Windows si aprono come file di testo contenenti il path. Usare direttamente `notes/02_cheatsheet.md` e `notes/04_domande_tipo.md`
