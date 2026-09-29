# TODO - esame Linguaggi, Interpreti e Compilatori

Stato: 2026-09-07.

> 🛑 **ORALE DEL 10 SETTEMBRE 2026: NON SI SOSTIENE.** Deciso il 07/09/2026 per preparazione insufficiente. Anche il calendario del 25/08 non è mai partito: dei ~35h di lavoro residuo non è stata fatta nessuna ora, quindi presentarsi all'orale (70% del voto, domande aperte su tutto il programma) avrebbe significato buttare l'appello su un esame da 9 CFU.
>
> **Nuovo bersaglio: appello della sessione invernale (gennaio-febbraio 2027)**, data da verificare su Esse3 quando esce il calendario. Metodi e Modelli è nella stessa sessione (rinviato l'11/08/2026): il calendario invernale andrà condiviso fra i due esami.
>
> ⚠️ **Due cose da chiudere subito, non appena possibile:**
> 1. **Mail al prof Zaffanella** per comunicare l'assenza all'appello del 10 settembre: l'iscrizione su Esse3 è stata fatta l'11/08/2026 e ormai la finestra per disiscriversi è chiusa, quindi risulti prenotato. Motivazione comunicata: **motivi familiari**, con alcune settimane di assenza. La bozza sta in `study/07_mail_prof.md`, che non e' piu' tracciata da git: le bozze di mail restano in locale.
> 2. **Chiedere nella stessa mail se il seminario resta valido.** Il seminario del 23 giugno 2026 vale "per tutti gli appelli dell'**a.a. 2025/26**" e l'appello di settembre 2026 è con ogni probabilità l'ultimo di quell'anno accademico. Se la sessione invernale 2027 conta come a.a. 2026/27, il 30% del voto va **rifatto** (nuovo argomento da concordare almeno 30 giorni prima, nuove slide, nuovo Q&A). È il vero costo del rinvio e va accertato prima di pianificare lo studio, non dopo.

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

### 2. Mail al prof - ⏳ RIAPERTO (seminario ✅, nuova mail da mandare)
Seminario **svolto martedì 23 giugno 2026** (30% del voto). Vale per **tutti gli appelli dell'a.a. 2025/26**: non va rifatto se ti ripresenti a un appello *di quell'anno accademico*.
⚠️ Con il rinvio alla sessione invernale 2027 questo diventa il punto aperto: se quell'appello appartiene all'a.a. 2026/27, il seminario va rifatto. Da chiedere al prof - vedi `study/07_mail_prof.md`.
Orale LIC: era **10 settembre 2026** (il 26 agosto era l'altra opzione), **non sostenuto**. Prossimo bersaglio: appello invernale, data da verificare.

### ~~3. Slide vere~~ ✅ v1 FATTA 2026-05-05
`SLIDES.md` con frontmatter Marp + tema custom (palette blu/rosso/verde, JetBrains Mono, gradient cover); diagramma architettura inline (HTML+CSS, 7 box colorati); export `SLIDES.pdf` 13 pagine. Resta solo un pass di review a freddo prima di mandarle al prof.

### ~~4. Demo cronometrata + pratica script~~ ✅ CONSUMATO nel seminario del 23/06
Materiale del seminario (demo, slide, script verbale). Il progetto `misc-no-printf` resta un **esempio concreto da citare all'orale** (front end di clang, AST matcher, diagnostica) - e se il seminario va rifatto per l'a.a. 2026/27, slide, script e confronto LLM sono già in cassaforte: si riparte da lì, non da zero.

### ~~5. Script verbale~~ ✅ FATTO 2026-05-05
`Martin/1_clang-tidy_custom_check/SCRIPT.md`: frasi pivot tecnico-fluide per ogni slide, apertura/chiusura forte, transizioni esplicite, Q&A con 6 domande probabili + risposte preparate, note operative. Usato al seminario.

### 6. Studio orale degli 11 capitoli (~17-19h)
L'ordine dei blocchi resta valido ed è la parte riusabile del piano fallito - le date del calendario no. Vedi `study/00_CALENDARIO.md` per la sequenza (le date del 25 ago - 10 set sono da ignorare) o `study_method/STUDY_PLAN.md` per il metodo:
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
| Studio orale 11 capitoli (parsing e Bison inclusi) | ⏳ | 19h |
| Laboratorio (Bison + `calc.output`; TinyP e LLVM opzionali) | ⏳ | 1.5h |
| Cheatsheet + 62 domande + incrocio + simulazione | ⏳ | 10h |
| Ripasso intensivo | ⏳ | 4.5h |
| **Totale residuo (solo orale)** | | **~35h** |

## 📅 Pianificazione - rinvio alla sessione invernale

Aggiornato al **2026-09-07** (domenica). **L'orale del 10 settembre non si sostiene.** Il carico residuo è rimasto **~35h**, identico a quello stimato il 25 agosto: non è stata studiata nessuna ora, quindi il bilancio qui sopra vale ancora tutto.

### Cosa ha fatto fallire i due piani precedenti

Sono stati scritti due calendari giorno per giorno - uno l'11 agosto (30 giorni, 32h), uno il 25 agosto (16 giorni, 35h) - e **nessuno dei due è mai partito**. Il collo di bottiglia non è la pianificazione: pianificare è la parte che è stata fatta due volte. Per la sessione invernale, quindi, **niente terzo calendario dettagliato scritto in anticipo**: prima si accumulano ore di studio reali, poi si ancora un calendario alla data dell'appello quando esce.

Il vincolo strutturale da tenere presente: 2h nei giorni lavorativi sono un'ipotesi che non ha mai retto. Il piano invernale deve reggere su ore che sono già state messe, non su ore promesse.

### Assenza di alcune settimane (da settembre)

Lutto in famiglia: alcune settimane fuori, a partire da settembre 2026. È un'assenza da mettere nel conto quando si pianifica la sessione invernale - il tempo di studio riparte al rientro, non ora, e i corsi del secondo anno partono a ottobre. Prima di partire va mandata la mail al prof.

### Da chiudere subito (settembre)

- [ ] **Mail al prof Zaffanella** - comunicare l'assenza all'appello del 10 settembre (risulti prenotato dall'11/08 e la finestra per disiscriversi è chiusa). Bozza in [`study/07_mail_prof.md`](study/07_mail_prof.md)
- [ ] **Nella stessa mail: chiedere se il seminario del 23 giugno resta valido** per l'appello invernale. Vale "per tutti gli appelli dell'a.a. 2025/26" e settembre 2026 è probabilmente l'ultimo appello di quell'a.a.
- [ ] **Verificare su Esse3** la data dell'appello invernale di LIC appena esce il calendario (e quella di Metodi e Modelli, che è nella stessa sessione)

### Se il seminario va rifatto

Costo aggiuntivo non banale, ma non si riparte da zero: argomento + materiale vanno riconcordati col docente **almeno 30 giorni prima**, quindi la mail va mandata con largo margine sull'appello invernale. Slide (`SLIDES.pdf`, 13 pagine), script verbale, check `misc-no-printf` e confronto LLM sono tutti pronti in `Martin/1_clang-tidy_custom_check/`: nel caso peggiore si ripresenta lo stesso lavoro con un pass di aggiornamento.

### Vincoli da tenere a mente

- **La sessione invernale non ospita solo questi due esami.** LIC (~35h residue) e Metodi e Modelli (~23h teoria + ~23h pratica + 6-8h simulazioni, stimate ad agosto) ci finiscono entrambi, ma da ottobre 2026 partono anche i **corsi del secondo anno** (Algoritmi per l'IA, Analisi Statica, Laboratorio di IA, Programmazione Dichiarativa): a gennaio arrivano i loro primi appelli, con il materiale fresco e le lezioni appena seguite.
- **Priorità invernale: aperta.** Non è affatto detto che LIC e Metodi vengano prima. Dare la precedenza ai nuovi esami del secondo anno è un'opzione concreta e in molti casi la più efficiente (il materiale è fresco, il corso appena finito), col rischio opposto che LIC e Metodi slittino ancora. Da decidere a corsi avviati, viste le date su Esse3 e il carico reale del semestre - non ora.
- Il seminario pesa il **30%** e - se resta valido - è già in cassaforte: l'orale sposta il restante 70%.
- LIC è da **9 CFU**: pesa il 50% in più di un esame da 6. Sulla media ponderata (28,00 su 5 esami votati) un **30** qui porta il voto di partenza da 102,66 a ~104,4, un **28** lo lascia invariato, un **26** lo fa scendere a ~101,0. È l'esame in cui conviene spingere - ed è anche il motivo per cui non valeva la pena presentarsi impreparato il 10 settembre.
- L'appello invernale ricade nel **secondo anno**: essere ancora *in corso* (bonus +3 sul voto di laurea) non è a rischio, ma i due esami del primo anno rinviati si sommano ai quattro del secondo.

✅ **Materiale allineato con Elly l'11/08/2026.** Le due sezioni **Analisi sintattica** ed **Esercitazione su analisi sintattica**, mai scaricate, sono state recuperate via API in `5b_Analisi_sintattica/` (slide EaC 08-14, 6 pptx + 5 pdf `-1up`) e `5c_Esercitazione_su_analisi_sintattica/` (`Bison.pdf` + 6 parser compilabili), entrambe con `RIASSUNTO.md`. Confronto con l'inventario completo di Elly: **nient'altro manca**; le slide EaC 13, 19, 21 e 28 su Elly non esistono. Integrità verificata su tutti i 50 PDF/slide: nessun file corrotto o troncato. Da riverificare solo se il docente carica materiale nuovo per l'a.a. 2026/27.

**Esse3:** appello LIC del 10 settembre **prenotato l'11/08/2026 e non annullabile** - ci si presenta come assenti, con la mail al prof a spiegare. Fondamenti dell'IA verbalizzato. Metodi del 17 settembre mai prenotato, quindi non serve disiscriversi.

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
