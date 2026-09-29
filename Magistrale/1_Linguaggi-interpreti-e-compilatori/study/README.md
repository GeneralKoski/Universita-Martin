# Study - preparazione esame

> 🛑 **ORALE RINVIATO ALLA SESSIONE INVERNALE** (deciso il 07/09/2026). L'appello del 10 settembre 2026 non si sostiene: preparazione insufficiente, il calendario del 25/08 non è mai partito. Nuovo bersaglio: appello di gennaio-febbraio 2027, data da verificare su Esse3. Contesto e azioni aperte in [`../TODO.md`](../TODO.md).
>
> Il seminario è stato svolto il 23 giugno 2026 (30% del voto) e resta solo l'orale, che pesa il **70%**. ⚠️ Ma vale "per tutti gli appelli dell'**a.a. 2025/26**": se l'appello invernale conta come a.a. 2026/27 il seminario va **rifatto**, con argomento da riconcordare almeno 30 giorni prima. Da chiedere al prof - bozza di mail in [`07_mail_prof.md`](07_mail_prof.md).

Punto d'ingresso unico per lo studio. I file sono numerati nell'ordine esatto in cui vanno affrontati, dal primo all'ultimo giorno.

> **Per sapere in che ordine studiare: [`00_CALENDARIO.md`](00_CALENDARIO.md)** - 17 blocchi con i file da aprire e le checkbox. Le date (25 agosto - 10 settembre) sono scadute e vanno ignorate: la sequenza no. Questo README resta la vista per blocchi tematici e il riferimento sul metodo.

Tutto il lavoro del seminario (check `misc-no-printf`, run reali, confronto LLM, slide, script verbale, demo) è stato **consumato al seminario del 23 giugno**: i blocchi 5 e 6 qui sotto sono storia. Il blocco **7 è tornato attivo** (mail al prof: assenza all'appello del 10/09 + validità del seminario per l'appello invernale). Restano poi i blocchi **1-4** (studio orale) e **8** (ripasso), tutti interi: ~35h. Vedi `../TODO.md` per lo stato dettagliato.

---

## Ordine di studio

| # | Blocco | Ore | File |
|---|---|---|---|
| 1 | Studio orale 11 capitoli (parsing e Bison inclusi) | 19h | [`01_studio_orale/`](01_studio_orale/README.md) |
| 2 | Cheatsheet a memoria | 3.5h | [`02_cheatsheet.md`](02_cheatsheet.md) |
| 3 | 62 domande tipo a voce (2-3 min ognuna) | 4h | [`03_domande_tipo.md`](03_domande_tipo.md) |
| 4 | Domande incrocio | 2-3h | [`04_domande_incrocio.md`](04_domande_incrocio.md) |
| 5 | ✅ Demo cronometrata + video backup | - | [`05_demo_cronometrata.md`](05_demo_cronometrata.md) |
| 6 | ✅ Pratica voce alta script | - | [`06_pratica_script.md`](06_pratica_script.md) |
| 7 | ⏳ Mail al prof - assenza al 10/09 + validità seminario | - | [`07_mail_prof.md`](07_mail_prof.md) |
| 8 | Ripasso intensivo sera prima orale | 2h | [`08_ripasso_intensivo.md`](08_ripasso_intensivo.md) |
| | **Totale residuo** | **~35h** | |

---

## Logica dell'ordine

- **1-4** = orale (70% del voto): è tutto il lavoro che resta, richiede il blocco di tempo più grande e va sedimentato.
- **La pratica di laboratorio era stata ridotta a 1.5h** e spostata dentro il blocco 1, insieme al parsing bottom-up: resta solo `calc-2` vs `calc-2-prec` con `calc.output` aperto, che è la parte che il prof può chiedere. Il lexer Flex modificato, i 4 binari di TinyP e l'LLVM playground (Step 2 di [`../study_method/STUDY_PLAN.md`](../study_method/STUDY_PLAN.md)) erano diventati **opzionali** per stare in 16 giorni. Con la sessione invernale il taglio si può annullare: le 6h piene tornano a starci, ed è il primo posto in cui rimettere ore.
- **5-7** = seminario (30% del voto): ✅ chiuso il 23 giugno 2026, vale per tutti gli appelli dell'a.a. **2025/26**. Tenuti qui come storico - e come base di partenza se per l'appello invernale va rifatto.
- **8** = ripasso: la sera prima dell'orale, **niente cose nuove**.

## Convenzioni

- I file `02_`, `03_`, `06_` sono symlink alle fonti canoniche (`notes/`, `Martin/`). Modifica solo l'originale.
- I file `04_`, `05_`, `07_`, `08_` sono guide operative scritte qui.
- Quando completi un blocco, spunta in `../TODO.md`.
