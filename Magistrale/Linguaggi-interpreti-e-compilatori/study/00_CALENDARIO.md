# 00 - Calendario giorno per giorno verso l'orale

> **ORALE: giovedì 10 settembre 2026.** Seminario svolto il 23 giugno 2026 (30% del voto, già in cassaforte): resta solo l'orale, che pesa il **70%**.
>
> Scritto l'11 agosto 2026, dopo il rinvio di Metodi e Modelli alla sessione invernale. I 30 giorni fino all'orale sono **tutti per LIC**.

Questo file è il piano operativo giorno per giorno. I blocchi tematici e il metodo stanno in [`README.md`](README.md); qui c'è solo *cosa apro oggi*.

Carico totale: **~32h su 30 giorni**, cioè 1.5-2h nei giorni lavorativi e 2-2.5h nei weekend. Non è un piano teso: c'è margine per sforare di un giorno senza compromettere niente.

---

## ⚠️ Prima di iniziare: materiale da scaricare da Elly

Due sezioni intere del corso non sono mai state scaricate. Non è materiale accessorio: è **l'analisi sintattica**, cioè la metà più interrogabile del front end.

- [ ] **Analisi sintattica** → entrambe le cartelle "Slide tratte dal libro di testo" (pptx e pdf). Sono le slide EaC **08-14**, quelle che nel repo mancano tra la `07-DFA_Minimization` e la `15-Context_sensitive_Analysis_I`. Salvare in `5b_Analisi_sintattica/`
- [ ] **Esercitazione su analisi sintattica** → `Bison.pdf` + "Esempi di semplici parser generati con flex & bison". Salvare in `5c_Esercitazione_su_analisi_sintattica/`
- [ ] Controllare nelle cartelle Elly di **IR** e **Middle end** se ci sono le slide EaC **19**, **21** e **28**: nel repo la sequenza salta quei tre numeri

Le cartelle `5b_` e `5c_` ordinano correttamente tra `5_` e `6_` e non rompono i link relativi esistenti in `notes/` e `study/`.

Fino al 15 agosto il parsing non serve, quindi il download non blocca l'inizio dello studio: va fatto entro **sabato 15**.

---

## Settimana 1 (11-17 agosto) - front end fino al parsing

### Martedì 11 - inquadramento (2h)
- [ ] `1_Introduzione_al_corso/RIASSUNTO.md` + `Intro.pdf`
- [ ] `2_Interpreti_e_compilatori/RIASSUNTO.md` + `Interpreti-Compilatori.pdf`
- [ ] `3_Struttura_del_compilatore/RIASSUNTO.md` + `Struttura-Compilatore.pdf`

**Obiettivo:** disegnare front-end / middle-end / back-end a memoria, e sapere quale formalismo abita ogni fase.

### Mercoledì 12 - lexer, teoria (1.5h)
- [ ] `4_Analisi_lessicale/RIASSUNTO.md` + `Analisi-Lessicale.pdf` + `DFA.pdf`
- [ ] EaC `05-Regular_Expressions_NFAs_DFAs.pptx`, `06-Building_Scanners.pptx`

**Obiettivo:** catena RE → NFA (Thompson) → DFA (subset construction), e la distinzione specifica/implementazione.

### Giovedì 13 - minimizzazione DFA (1.5h)
- [ ] `4_Analisi_lessicale/07-DFA_Minimization.pptx` + `note.txt`

⚠️ Il prof ha trattato **solo Hopcroft**, non Moore né Brzozowski. Punto in cui si inciampa: la definizione precisa di `δ⁻¹(s, c)` nella worklist.

### Venerdì 14 - Flex ed esercitazione lexer (1h)
- [ ] `4_Analisi_lessicale/Flex.pdf`
- [ ] `5_Esercitazione_su_analisi_lessicale/RIASSUNTO.md` + `note.txt`
- [ ] Leggere `lexer-cpp.ll` riga per riga

### Sabato 15 - Ferragosto
Riposo, o recupero se sei in ritardo. **Scadenza download del materiale di parsing da Elly.**

### Domenica 16 - parsing I (2h)
- [ ] `notes/08_parsing.md` §1-4: CFG e derivazioni, gerarchia dei parser, LL(1) con FIRST/FOLLOW, LR(1) con item e handle
- [ ] Slide EaC di parsing (parte top-down)

⚠️ Leggere `notes/08_parsing.md` **prima** delle slide EaC: è in italiano e sintetico, dà la struttura in cui incastrare le slide inglesi. Il contrario ti fa annegare nei dettagli delle tabelle.

### Lunedì 17 - parsing II (2h)
- [ ] `notes/08_parsing.md` §5-7: conflitti, LALR(1) e Bison, precedenza di operatori
- [ ] Slide EaC su LR + costruzione tabelle
- [ ] `Bison.pdf`

---

## Settimana 2 (18-24 agosto) - semantica statica, IR, ottimizzazioni

### Martedì 18 - parsing III, pratica (1.5h)
- [ ] Esempi di parser flex & bison scaricati da Elly
- [ ] `6_Analisi_dipendente_da_contesto/TinyP/parser.yy`: `%left`, `%prec`, azioni semantiche sul Bison vero
- [ ] Su carta: FIRST/FOLLOW e tabella LL(1) della grammatica della domanda 14 di `notes/04_domande_tipo.md`

### Mercoledì 19 - context-sensitive I (1.5h)
- [ ] `6_Analisi_dipendente_da_contesto/RIASSUNTO.md` + `L16ContextSensitive-1up.pdf` + EaC `15-...I.pptx`

**Obiettivo:** attribute grammar, attributi sintetizzati vs ereditati, non ciclicità, valutazione single-pass.

### Giovedì 20 - context-sensitive II e AST (1.5h)
- [ ] `L17AdHoc-1up.pdf`, `L18TypeAnalysis-1up.pdf`, EaC `16-...II.pptx`
- [ ] `TinyP/ast.hh` e `ast_visitor.hh`: il visitor pattern è l'esempio concreto da citare

La frase chiave del corso: le risposte dipendono da **valori**, non da parti del discorso, e richiedono **calcolo non locale**. Per questo in pratica vince l'ad-hoc SDT sul formalismo delle AG.

### Venerdì 21 - IR e LLVM (1.5h)
- [ ] `7_Rappresentazione_intermedia_(IR)/RIASSUNTO.md` + `LLVM-IR.pdf` + EaC `17-Intermediate_Representations.pptx`

**Obiettivo:** classificazione IR (strutturale/lineare/ibrida), 3-address code, forma SSA, `phi`, `getelementptr`.

### Sabato 22 - astrazione procedurale (2h)
- [ ] EaC `18-The_Procedure_Abstraction_I.pptx`, `20-Procedure_Abstraction_III.pptx`

**Obiettivo:** activation record, calling convention (pre-call, prologo, epilogo, post-call), catena degli access link, per valore vs per riferimento.

⚠️ Compile-time vs run-time: l'AR esiste a run-time, il codice che lo costruisce è emesso a compile-time.

### Domenica 23 - OOL e code shape (2.5h)
- [ ] EaC `22-Support_for_OOLs.pptx`, `23-Support_for_Inheritance_in_OOLs.pptx` → vtable, ereditarietà singola e multipla
- [ ] EaC `24-Code_Shape_I`, `25-Code Shape_II`, `26-Code Shape_III` → array e matrici, stringhe C vs Pascal, short-circuit, if-then-else e cicli, le 3 strategie del `case`

### Lunedì 24 - ottimizzazioni locali e dominatori (2h)
- [ ] `8_Il_middle_end_analisi_e_ottimizzazioni/RIASSUNTO.md`
- [ ] EaC `27-...local_value_numbering.pptx`, `29-...SVN_and_Loop_Unrolling.pptx`
- [ ] `08Dominators-1up.pdf` → dominatori, dominatore immediato, DVN

---

## Settimana 3 (25-31 agosto) - dataflow, astratta, laboratorio, cheatsheet

### Martedì 25 - dataflow (2h)
- [ ] EaC `30-Global_Optimization_Live_Analysis.pptx`
- [ ] `13DFA-1up.pdf`, `09GlobalOptimization-1up.pdf`, `14Proliferation-1up.pdf`, `19Clean-1up.pdf`
- [ ] `notes/06_dataflow.md`: le 4 analisi classiche (Live, Reaching, Available, Very Busy) nello stesso framework

### Mercoledì 26 - interpretazione astratta, intuizione (1.5h)
- [ ] `9_Cenni_su_interpretazione_astratta/RIASSUNTO.md` + `cousot-tutorial.pdf` + `note.txt` (link ai paper originali dei Cousot)

### Giovedì 27 - interpretazione astratta, formale (1.5h)
- [ ] `mine-tutorial.pdf`
- [ ] Knaster-Tarski e Kleene, Galois connection, domini (segni, intervalli, congruenze), widening

⚠️ Non basta dire "esiste un punto fisso": va giustificato. Ed è qui che si chiude il cerchio col dataflow del giorno 25.

### Venerdì 28 - laboratorio front end (1.5h)
```bash
cd 5_Esercitazione_su_analisi_lessicale && make
echo 'int main() { return 0; }' | ./lexer-cpp
```
- [ ] Modificare una regola, ricompilare, osservare il cambiamento
- [ ] Buildare ed eseguire i parser flex & bison dell'esercitazione di analisi sintattica

### Sabato 29 - laboratorio TinyP e LLVM (2.5h)
```bash
cd 6_Analisi_dipendente_da_contesto/TinyP && make all
```
- [ ] Provare tutti e 4 i binari (`tinyP-pp`, `tinyP-astdump`, `tinyP-run`, `tinyP-concrete`) sul programmino in `study_method/STUDY_PLAN.md`. `collecting.cc` è il ponte concettuale verso l'interpretazione astratta
```bash
clang -O0 -S -emit-llvm sq.c -o sq.ll
clang -O2 -S -emit-llvm sq.c -o sq.opt.ll
diff sq.ll sq.opt.ll
```
- [ ] Rileggere `Martin/1_clang-tidy_custom_check/RESULTS.md`: il tuo check è un esempio concreto di front end di Clang + AST matcher da tirare fuori all'orale

### Domenica 30 - cheatsheet parte 1, a memoria (2h)
- [ ] `notes/02_cheatsheet.md`: le 4 equazioni dataflow con tabella direzione/meet/init/fixpoint, Hopcroft, LVN, FIRST/FOLLOW

### Lunedì 31 - cheatsheet parte 2 (1.5h)
- [ ] Formula GEP, Galois connection, Knaster-Tarski/Kleene, calling convention, activation record, vtable
- [ ] Prima lettura di `notes/03_glossario.md`

---

## Settimana 4 (1-6 settembre) - domande a voce

Le 57 domande stanno in `notes/04_domande_tipo.md`. Rispondere **a voce**, cronometrando 2-3 minuti ognuna. Le domande aggiunte nell'audit del 05/05 hanno la traccia di risposta: rispondi prima, confronta dopo.

### Martedì 1 (1.5h)
- [ ] Domande **1-19**: introduzione e struttura, front end, analisi sintattica

### Mercoledì 2 (1.5h)
- [ ] Domande **20-41**: IR e back end, middle end

### Giovedì 3 (1.5h)
- [ ] Domande **42-57**: interpretazione astratta, strumenti, domande trick

### Venerdì 4 (1.5h)
- [ ] Secondo passaggio **solo** sulle domande in cui hai esitato, a un giorno di distanza dal primo

### Sabato 5 - domande incrocio (2h)
- [ ] `04_domande_incrocio.md`: D1 pipeline completa di un C++ con virtual methods, D2 constant propagation con loop (dataflow vs astratta), D3 middle end di Clang vs interpretazione astratta

### Domenica 6 - simulazione (2h)
- [ ] Simulazione orale completa a voce, 30-40 minuti di fila
- [ ] I disegni: RE → NFA → DFA → DFA minimo, Live Variables su un CFG di 4 nodi

---

## Finale (7-10 settembre)

### Lunedì 7 (1.5h)
- [ ] Solo le sezioni "Punti chiave per l'orale" dei 9 `RIASSUNTO.md`
- [ ] `notes/05_pipeline_compilatore.md` per il quadro d'insieme

### Martedì 8 (1h)
- [ ] `notes/02_cheatsheet.md` + `notes/03_glossario.md`
- [ ] Riscrivere a memoria su carta le 4 equazioni dataflow

### Mercoledì 9 (2h)
- [ ] [`08_ripasso_intensivo.md`](08_ripasso_intensivo.md) e nient'altro

**Niente cose nuove.** Se non l'hai studiato finora, non lo studi adesso. A letto entro le 23.

### Giovedì 10 - ORALE

---

## Regole del piano

- **Il ripasso 7-9 settembre è intoccabile.** Se una settimana sfonda, si sacrifica prima il laboratorio (28-29 ago), poi le domande incrocio (5 set). Mai il ripasso
- **Ogni argomento si chiude a voce**, sulla sezione "Punti chiave per l'orale" del riassunto. Se lo leggi e ti sembra chiaro ma non riesci a dirlo, non lo sai
- **Le domande su cui esiti si annotano** e finiscono nel secondo passaggio del 4 settembre
- LIC è da **9 CFU**: pesa il 50% in più di un esame da 6. Sui numeri attuali (media 28,00 su 5 esami votati) un **30** porta il voto di partenza da 102,66 a ~104,4; un **28** lo lascia invariato; un **26** lo fa scendere a ~101,0
- I file `02_cheatsheet.md`, `03_domande_tipo.md` e `06_pratica_script.md` di questa cartella sono symlink che su Windows si aprono come file di testo contenenti il path. Usare direttamente `notes/02_cheatsheet.md` e `notes/04_domande_tipo.md`
