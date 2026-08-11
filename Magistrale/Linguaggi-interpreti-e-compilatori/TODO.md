# TODO - esame Linguaggi, Interpreti e Compilatori

Stato: 2026-08-11.

> **ORALE FISSATO: giovedì 10 settembre 2026.** Seminario già svolto il 23 giugno 2026 (30% del voto, valido per tutti gli appelli dell'a.a.): resta solo l'orale (70%).
>
> **Metodi e Modelli rinviato alla sessione invernale** (deciso l'11/08/2026): i 30 giorni fino all'orale sono tutti per LIC. Vedi la sezione "Pianificazione verso il 10 settembre" in fondo.

> **Per studiare:** entry point unico in [`study/`](study/README.md). 8 blocchi numerati nell'ordine in cui vanno affrontati.

Per il dettaglio del lavoro tecnico già fatto vedi `Martin/1_clang-tidy_custom_check/{PLAN,TODO,RESULTS}.md`.

---

## ✅ Già chiuso

- Argomento del seminario confermato dal prof: **clang-tidy custom check** (`misc-no-printf`)
- Build LLVM da sorgente, check scritto+installato, lit test ufficiale PASS
- Run reali: `fmt` (0/0), `tinyxml2` (28/0 falsi positivi)
- Bear demo Make funzionante (5/5)
- Documentazione `.rst` ufficiale del check + entry in `list.rst`
- **Confronto LLM reale completato (2026-05-05)**: 6 snippet × 2 modelli × 2 chat fresche = 24 run. Wow moment confermato sullo snippet 06 (overload resolution): clang-tidy 100% deterministico, LLM 50/50 sul finding chiave. Vedi `Martin/1_clang-tidy_custom_check/comparison/COMPARISON.md`.
- **Slide v1 (2026-05-05)**: `SLIDES.md` riscritto con frontmatter Marp + tema custom, esportato in `SLIDES.pdf` 13 pagine. Diagramma architettura inline a 7 box colorati. Resta solo un pass di review a freddo.
- **Script verbale (2026-05-05)**: `Martin/1_clang-tidy_custom_check/SCRIPT.md` con frasi pivot tecnico-fluide per ogni slide, apertura/chiusura forte (~15s ognuna), transizioni esplicite, Q&A con 6 domande probabili + risposte preparate, note operative.
- **Recupero materiale mancante (2026-08-11)**: confronto con l'inventario completo di Elly via API. Due sezioni del corso non erano mai state scaricate → nuove cartelle `5b_Analisi_sintattica/` (slide EaC 08-14) e `5c_Esercitazione_su_analisi_sintattica/` (`Bison.pdf` + 6 parser compilabili), entrambe con `RIASSUNTO.md`. Aggiunto al cheatsheet il blocco parsing che mancava del tutto (FIRST/FOLLOW, tabella LL(1), item LR(1), conflitti, precedenza Bison), 5 domande nuove (57 → 62), 12 voci di glossario. Nient'altro manca: le slide EaC 13, 19, 21 e 28 su Elly non esistono.
- **Materiali studio orale (2026-05-05)**: audit completo dei 9 RIASSUNTO + `notes/`. Chiuse lacune bloccanti per orale 70% (era assente l'analisi sintattica → nuovo `notes/08_parsing.md` ~670 righe; corretti errori in Live equation, Galois connection, dominator init; aggiunte sezioni in IR (GEP, invoke, conversioni, refcount, access link), Middle End (Available Expr+GCSE, Very Busy+hoisting, IV+strength reduction, mem2reg/SROA/instcombine/LICM), Interpretazione Astratta (Knaster-Tarski, Kleene, soundness con dim, esempio Intervals)). Glossario esteso, 13 nuove domande (44 → 57).

---

## 🎯 Da fare - in ordine di priorità

### ~~1. Confronto LLM reale~~ ✅ FATTO 2026-05-05
6 snippet (estesi da 4: aggiunti 05_method_collision e 06_using_template_alias) × 2 modelli × 2 chat fresche = 24 run completati. Risultati integrali in `Martin/1_clang-tidy_custom_check/comparison/`.

**Wow moment vero**: snippet 06 (overload resolution dopo `using logging::printf;`). clang-tidy = 1 hit deterministico sempre nello stesso punto; LLM = 2/4 run sbagliano il finding chiave, lo stesso modello dà risposte opposte tra chat fresche.

**Pattern stabili**: ChatGPT non propone mai `std::print`/`std::println` come fix primario (0/6, solo come alternativa C++23 condizionale); Claude lo fa quando appropriato (4/6); determinismo Claude > ChatGPT.

**Bonus**: LLM trova bug fuori scope (troncamento `2.5→2`, `nullptr` UB) → conferma complementarità.

### ~~2. Mail al prof + seminario~~ ✅ FATTO
Seminario **svolto martedì 23 giugno 2026** (30% del voto). Vale per **tutti gli appelli dell'a.a. 2025/26**: non va rifatto anche se ti ripresenti a un appello successivo.
Orale LIC: **10 settembre 2026** (era in ballo anche il 26 agosto, scartato).

### ~~3. Slide vere~~ ✅ v1 FATTA 2026-05-05
`SLIDES.md` con frontmatter Marp + tema custom (palette blu/rosso/verde, JetBrains Mono, gradient cover); diagramma architettura inline (HTML+CSS, 7 box colorati); export `SLIDES.pdf` 13 pagine. Resta solo un pass di review a freddo prima di mandarle al prof.

### ~~4. Demo cronometrata + pratica script~~ ✅ CONSUMATO nel seminario del 23/06
Materiale del seminario (demo, slide, script verbale). Non serve più per l'orale del 10 settembre, ma il progetto `misc-no-printf` resta un **esempio concreto da citare all'orale** (front end di clang, AST matcher, diagnostica).

### ~~5. Script verbale~~ ✅ FATTO 2026-05-05
`Martin/1_clang-tidy_custom_check/SCRIPT.md`: frasi pivot tecnico-fluide per ogni slide, apertura/chiusura forte, transizioni esplicite, Q&A con 6 domande probabili + risposte preparate, note operative. Usato al seminario.

### 6. Studio orale degli 11 capitoli (~17-19h)
Seguire `study/00_CALENDARIO.md` (o `study_method/STUDY_PLAN.md` per il metodo):
- Lez 1-3 (Intro, Interpreti vs Compilatori, Struttura): 1.5h
- Lez 4-5 (Analisi lessicale, Flex): 2h
- **Parsing (analisi sintattica): 4h.** Ordine: prima `notes/08_parsing.md` (sintesi italiana, dà la struttura), poi `5b_Analisi_sintattica/` (slide EaC 08-14, recuperate da Elly l'11/08/2026)
- **Esercitazione Bison - `5c_Esercitazione_su_analisi_sintattica/`: 1.5h.** `Bison.pdf` + i sei parser `calc-*`; il confronto `calc-2` vs `calc-2-prec` è la domanda d'orale su Bison
- Lez 6 (Analisi dipendente da contesto, TinyP): 2h
- Lez 7 (IR, LLVM, GEP, code shape, invoke, conversioni, access link): 2-3h
- Lez 8 (Middle end, dataflow, Available/Very Busy, induction var, LLVM passes): 2-3h
- Lez 9 (Interpretazione astratta, Knaster-Tarski, Kleene, soundness, widening): 1.5h

Per ogni lezione: leggi `RIASSUNTO.md` → apri PDF docente → "Punti chiave per l'orale" → rispondi a voce alle domande.

### 7. Memorizzazione cheatsheet (~3.5h)
`notes/02_cheatsheet.md`:
- Equazioni delle 4 DFA classiche (Live, Reaching, Available, Very Busy) + tabella riepilogo direzione/meet/init/fixpoint
- Algoritmo LVN
- Algoritmo Hopcroft (worklist) con definizione precisa di `δ⁻¹(s, c)`
- **Blocco parsing** (aggiunto l'11/08/2026, prima mancava del tutto): algoritmo FIRST/FOLLOW, regola di riempimento della tabella LL(1) e condizione di LL(1)-ità, item LR(1) con `closure`/`goto`, tabella dei due conflitti, direttive di precedenza Bison e confronto grammatica stratificata vs piatta
- Tabella domini astratti
- Formula GEP, Galois connection, Knaster-Tarski/Kleene
- Calling convention, activation record, vtable

### 8. 62 domande tipo (~4h)
`notes/04_domande_tipo.md` (44 iniziali, +13 dopo l'audit del 2026-05-05, +5 sull'esercitazione Bison l'11/08/2026):
- Sezioni: Introduzione, Front end, Analisi sintattica, IR e back end, Middle end, Interpretazione astratta, Strumenti, Trick, **Esercitazione Bison** (nuova)
- Risposta a voce, cronometrando 2-3 min ognuna
- Le 13 domande nuove hanno traccia di risposta - usala come autovalutazione (rispondi prima, poi confronta)
- Per quelle su cui esiti: torna al RIASSUNTO o al PDF
- Riprova il giorno dopo

### 9. Domande "incrocio" (~2-3h)
- Pipeline completa di compilazione di un C++ con virtual methods
- Constant propagation con loop (dataflow + astratta)
- Middle end Clang vs interpretazione astratta

### 10. Ripasso intensivo (~2h, sera prima dell'orale)
- Solo "Punti chiave per l'orale" degli 11 RIASSUNTO
- Glossario `notes/03_glossario.md`
- **Niente cose nuove**

---

## ⏱ Bilancio ore residue (post-2026-05-05)

| Blocco | Stato | Ore residue |
|---|---|---|
| Confronto LLM | ✅ fatto | - |
| Slide v1 (PDF) | ✅ fatto | - |
| Script verbale | ✅ fatto | - |
| Audit materiali studio | ✅ fatto | - |
| Demo cronometrata + slide + script | ✅ consumato al seminario | - |
| Seminario (30% del voto) | ✅ svolto 23/06/2026 | - |
| Recupero materiale mancante da Elly | ✅ fatto 11/08/2026 | - |
| Studio orale 11 capitoli (parsing e Bison inclusi) | ⏳ | 17-19h |
| Laboratorio (lexer, Bison, TinyP, LLVM) | ⏳ | 4h |
| Cheatsheet + 62 domande + incrocio + simulazione | ⏳ | 11.5h |
| Ripasso intensivo | ⏳ | 4.5h |
| **Totale residuo (solo orale)** | | **~32h** |

## 📅 Pianificazione verso il 10 settembre

Aggiornato al **2026-08-11** (martedì). **Metodi e Modelli è stato rinviato alla sessione invernale**: l'appello del 17 settembre non si sostiene, quindi i 30 giorni da qui all'orale sono **tutti per LIC**. Il calendario non è più condiviso.

Il lavoro residuo era stimato in ~21-26h e su 30 giorni il tempo non è più il vincolo. Il margine **non va diluito**: è stato investito in due cose che nelle versioni precedenti del piano erano le prime a cadere - la pratica di laboratorio (Step 2 di `study_method/STUDY_PLAN.md`) e il parsing, che era l'argomento coperto peggio e che dall'11/08 ha finalmente il materiale del corso. Totale rivisto: **~32h**.

> **Piano giorno per giorno: [`study/00_CALENDARIO.md`](study/00_CALENDARIO.md).** È la fonte unica per "cosa apro oggi", con le checkbox da spuntare. Qui sotto solo la vista settimanale.

```
11 - 17 ago  : intro + struttura + lexer + Flex, poi parsing I-II    ~8h
18 - 24 ago  : parsing III, context-sensitive, IR, procedure abstraction, OOL, code shape, LVN/dominatori  ~11h
25 - 31 ago  : dataflow, interpretazione astratta, laboratorio, cheatsheet a memoria   ~11h
1 - 6 set    : 62 domande a voce (due passaggi) + domande incrocio + simulazione   ~10h
7 - 9 set    : ripasso intensivo (solo "Punti chiave" + glossario, niente cose nuove)   ~4.5h
10 set (gio) : ORALE LIC
```

✅ **Materiale allineato con Elly l'11/08/2026.** Le due sezioni **Analisi sintattica** ed **Esercitazione su analisi sintattica**, mai scaricate, sono state recuperate via API in `5b_Analisi_sintattica/` (slide EaC 08-14, 6 pptx + 5 pdf `-1up`) e `5c_Esercitazione_su_analisi_sintattica/` (`Bison.pdf` + 6 parser compilabili), entrambe con `RIASSUNTO.md`. Confronto con l'inventario completo di Elly: **nient'altro manca**; le slide EaC 13, 19, 21 e 28 su Elly non esistono. Integrità verificata su tutti i 50 PDF/slide: nessun file corrotto o troncato.

**Vincoli da tenere a mente:**
- Il seminario è già in cassaforte e pesa il 30%: l'orale sposta il restante 70%, quindi non c'è nulla da recuperare, solo da difendere.
- LIC è da **9 CFU**: pesa il 50% in più di un esame da 6. Sulla media ponderata (28,00 su 5 esami votati) un **30** qui porta il voto di partenza da 102,66 a ~104,4, un **28** lo lascia invariato, un **26** lo fa scendere a ~101,0. È l'esame in cui conviene spingere.
- Buffer: se una settimana sfonda, la prima da sacrificare è la pratica di laboratorio (25-31 ago), poi le domande incrocio. **Mai** il ripasso 7-9 set.

**Esse3: tutto a posto.** Appello LIC del 10 settembre **prenotato l'11/08/2026**; Fondamenti dell'IA verbalizzato; Metodi del 17 settembre mai prenotato, quindi non serve disiscriversi.

---

## 📎 Riferimenti rapidi

- Stato dettagliato Fase 1: `Martin/1_clang-tidy_custom_check/RESULTS.md`
- Piano lavoro Fase 1-2-3: `Martin/1_clang-tidy_custom_check/PLAN.md`
- Coda Fase 1: `Martin/1_clang-tidy_custom_check/TODO.md`
- **Slide finale (PDF):** `Martin/1_clang-tidy_custom_check/SLIDES.pdf` (sorgente: `SLIDES.md`)
- **Script verbale del seminario:** `Martin/1_clang-tidy_custom_check/SCRIPT.md`
- **Confronto LLM completo:** `Martin/1_clang-tidy_custom_check/comparison/COMPARISON.md` + `comparison/llm_responses/`
- Programma corso e modalità d'esame: vedi cartelle `1_*` ... `9_*`
- Metodo di studio: `study_method/STUDY_PLAN.md`
- **Cheatsheet, glossario, parsing, dataflow, 62 domande:** `notes/` (indice in `notes/00_INDEX.md`)
- **Slide e esercitazione sull'analisi sintattica:** `5b_Analisi_sintattica/` e `5c_Esercitazione_su_analisi_sintattica/` (recuperate da Elly l'11/08/2026)

---

**Quando torno qui in futuro**, partiamo da questo file: spunto cosa è stato fatto e proseguiamo dal punto successivo.
