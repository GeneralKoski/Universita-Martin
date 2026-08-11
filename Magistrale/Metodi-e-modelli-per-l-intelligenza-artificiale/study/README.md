# Piano di studio - Metodi e Modelli per l'IA

> ⚠️ **ESAME RINVIATO ALLA SESSIONE INVERNALE** (deciso l'11/08/2026). L'appello del 17 settembre 2026 non si sostiene: la priorità di agosto-settembre è l'orale di Linguaggi, Interpreti e Compilatori del 10 settembre. Il calendario qui sotto è quello vecchio, condiviso con LIC - va rifatto quando si conosce la data dell'appello invernale.
>
> Il materiale (teoria 01-14, pratica 01-12, anatomia esame) è completo e resta valido: cambia solo la pianificazione.

Percorso ottimale per preparare l'esame, suddiviso in **teoria** e **pratica**. I file sono numerati: seguili in ordine.

**Leggi prima di tutto [`pratica/00_ANATOMIA_ESAME.md`](pratica/00_ANATOMIA_ESAME.md):** censimento di 12 appelli risolti, dell'esonero 2022, dei quiz Elly e dei fogli di esercizi 2026, con la frequenza di ogni tipo di esercizio e l'ordine di priorità su cui fare pratica. In sintesi, il 60% di uno scritto tipo sta in tre esercizi: Floyd-Warshall da matrici parziali (6/12 appelli), duale lagrangiano (7/12), Dijkstra tabellare (4/12).

## Calendario verso il 17 settembre

Carico stimato: **~23h di teoria + ~23h di pratica + 6-8h di simulazioni**, cioè il doppio di LIC (orale il 10 settembre, ~21-26h). Per questo Metodi va caricato **prima**: i 7 giorni fra i due esami bastano solo per le simulazioni, non per teoria nuova.

```
27 lug - 2 ago   : Blocco A completo - teoria 01-06 + pratica 01-06 (grafi)
3 - 9 ago        : Blocco B parte 1 - teoria 07-10 + pratica 07-08 (PI, POC, TSP, formulazioni)
10 - 16 ago      : Blocco B parte 2 - teoria 11-14 + pratica 09, 11, 12 (rilassamenti, dualità, TU, trasporto)
17 - 30 ago      : LIC ha priorità (studio orale). Qui solo manutenzione: 1 sessione/sett di esercizi sui grafi per non perdere la mano
31 ago - 6 set   : 1ª simulazione scritta cronometrata (tracce da "esami nicolodi risolti.pdf")
7 - 9 set        : LIC ripasso intensivo. Metodi in pausa
10 set (gio)     : ORALE LIC
11 - 16 set      : full Metodi - 2ª e 3ª simulazione scritta + dimostrazioni a voce per l'orale
17 set (gio)     : SCRITTO METODI
```

**Vincoli:**
- Gli algoritmi sui grafi vanno **automatizzati a mano** (Dijkstra, Floyd-Warshall, Prim eseguiti su carta senza pensarci): è la parte dello scritto che si perde più in fretta, da qui la manutenzione settimanale ad agosto.
- Le dimostrazioni per l'orale si ripassano nell'ultima settimana, dopo l'orale di LIC.
- Da verificare su Esse3: iscrizione all'appello e se l'orale è in giornata o in data successiva.

---

## Strategia consigliata

1. Per ogni argomento: **teoria prima**, poi **pratica** dello stesso numero.
   - Es. leggi `teoria/01_*.md` → fai `pratica/01_*.md` → poi passa a `02`.
2. Argomenti raggruppati in 2 macro-blocchi (come da indicazioni dei colleghi):
   - **Blocco A - Algoritmi sui grafi** (file 01-06)
   - **Blocco B - Programmazione intera & ottimizzazione combinatoria** (file 07-14 teoria, 07-12 pratica)
3. Alla fine, **simulazione d'esame** completa con `esami nicolodi risolti.pdf` (vedi `pratica/13_simulazione_esame.md`).

## Programma 6 CFU (limite ufficiale)
Il programma per Scienze Informatiche **arriva fino a "Trasporto generalizzato e problemi facili" incluso** (Lezioni 21-22 su Elly = file 14 teoria, 12 pratica). Restano fuori **branch & bound, piani di taglio, programmazione dinamica**: le Lezioni 13-14 li citano come panoramica, ma non vanno saputi eseguire. Se in una traccia d'esame vecchia trovi un branch and bound, salta l'esercizio.

Corrispondenza fra i moduli Elly e i file di questa cartella:

| Elly | teoria | pratica |
|---|---|---|
| 1 Elementi di teoria dei grafi | 01 | 01 |
| 2 Procedure BFS e DFS | 02 | 02 |
| 3 Cammini minimi: Bellman | 03 | 03 |
| 4 Cammini minimi: Dijkstra | 04 | 04 |
| 5 Cammini minimi: Floyd-Warshall | 05 | 05 |
| 6 Albero ricoprente minimo | 06 | 06 |
| 7 PL & ottimizzazione combinatoria | 07, 08, 09, 10 | 07, 08 |
| 8 Rilassamenti e dualità | 11, 12 | 09 |
| 9 Matrici TU e teorema di interezza | 13 | 11 |
| 10 Trasporto generalizzato | 14 | 12 |

Nota: non esiste un `pratica/10_*`, la numerazione della pratica salta dal 09 all'11.

## Struttura

```
study/
├── teoria/    - concetti, definizioni, teoremi, dimostrazioni (per l'orale)
└── pratica/   - esercizi e algoritmi da eseguire a mano (per lo scritto)
```

## Che ruolo ha ciascuna fonte

| Cartella | A cosa serve |
|---|---|
| `Elly/` | **programma ufficiale 2025/26** (6 CFU): lezioni 1-22, `riassunto.md` per modulo, e i **7 fogli di esercizi assegnati quest'anno**. È il riferimento su *cosa* è in programma. |
| `Appunti_colleghi/Zip_appunti/` | **l'unica fonte di tracce d'esame vere**: 12 appelli risolti, l'esonero 2022, i quiz Elly. È il riferimento su *come* viene chiesto. |
| `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` | **svolgimenti a mano dei fogli 1-7**, gli stessi fogli che il prof assegna oggi. Copre anche i fogli 1 e 4, per cui su Elly la soluzione non c'è. |
| `Appunti_colleghi/Zip_appunti/LEZIONI 22-23/` | appunti dei gestionali (9 CFU): più estesi del necessario, solo approfondimento. |

Le due prime cartelle **non sono sostituibili l'una con l'altra**, ed è la cosa più importante da capire nell'organizzare lo studio:

- Il capitolo con più peso allo scritto (rilassamento e duale lagrangiano, 7 appelli su 12) ha su Elly solo teoria e dimostrazioni: il **calcolo numerico** si allena unicamente sulle 7 tracce svolte in `esami nicolodi risolti.pdf`.
- Viceversa il capitolo 14 (trasporto e flussi) su Elly c'è, ma negli esami risolti **non compare mai**: è materia da orale.

Bibliografia (per consultazione): Wolsey *Integer Programming*, Maffioli *Elementi di programmazione matematica*, Ghiani-Musmanno (logistica), Hillier-Lieberman (ricerca operativa).
