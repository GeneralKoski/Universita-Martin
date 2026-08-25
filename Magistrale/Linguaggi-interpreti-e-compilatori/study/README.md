# Study - preparazione esame

> **ORALE: giovedì 10 settembre 2026.** Seminario svolto il 23 giugno 2026 (30% del voto, già in cassaforte): resta solo l'orale, che pesa il **70%**. Calendario in `../TODO.md`.

Punto d'ingresso unico per lo studio. I file sono numerati nell'ordine esatto in cui vanno affrontati, dal primo all'ultimo giorno.

> **Per sapere cosa studiare oggi: [`00_CALENDARIO.md`](00_CALENDARIO.md)** - piano giorno per giorno dal 25 agosto al 10 settembre (ripianificato il 25/08, lo studio parte da lì), con i file da aprire e le checkbox. Questo README resta la vista per blocchi tematici e il riferimento sul metodo.

Tutto il lavoro del seminario (check `misc-no-printf`, run reali, confronto LLM, slide, script verbale, demo) è chiuso e **consumato al seminario del 23 giugno**: i blocchi 5, 6 e 7 qui sotto sono storia, non lavoro residuo. Restano i blocchi **1-4** (studio orale) e **8** (ripasso). Vedi `../TODO.md` per lo stato dettagliato.

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
| 7 | ✅ Mail al prof - seminario **svolto 23 giu 2026** | - | [`07_mail_prof.md`](07_mail_prof.md) |
| 8 | Ripasso intensivo sera prima orale | 2h | [`08_ripasso_intensivo.md`](08_ripasso_intensivo.md) |
| | **Totale residuo** | **~35h** | |

---

## Logica dell'ordine

- **1-4** = orale (70% del voto): è tutto il lavoro che resta, richiede il blocco di tempo più grande e va sedimentato.
- **La pratica di laboratorio è stata ridotta a 1.5h** e spostata dentro il blocco 1, il giorno del parsing bottom-up (sabato 29 agosto): resta solo `calc-2` vs `calc-2-prec` con `calc.output` aperto, che è la parte che il prof può chiedere. Il lexer Flex modificato, i 4 binari di TinyP e l'LLVM playground (Step 2 di [`../study_method/STUDY_PLAN.md`](../study_method/STUDY_PLAN.md)) sono **opzionali**: si fanno solo se un blocco chiude in anticipo. Con 16 giorni invece di 30 non c'è più spazio per le 6h piene.
- **5-7** = seminario (30% del voto): ✅ chiuso il 23 giugno 2026, vale per tutti gli appelli dell'a.a. Tenuti qui come storico.
- **8** = ripasso: la sera prima dell'orale, **niente cose nuove**.

## Convenzioni

- I file `02_`, `03_`, `06_` sono symlink alle fonti canoniche (`notes/`, `Martin/`). Modifica solo l'originale.
- I file `04_`, `05_`, `07_`, `08_` sono guide operative scritte qui.
- Quando completi un blocco, spunta in `../TODO.md`.
