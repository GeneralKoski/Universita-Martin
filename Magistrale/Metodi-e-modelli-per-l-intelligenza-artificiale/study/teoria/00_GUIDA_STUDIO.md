# 00 - Guida allo studio della teoria (passo passo)

Percorso ordinato per preparare la parte teorica (orale) di Metodi e Modelli.
Segui i passi **in ordine**: ogni argomento poggia sui precedenti.

Programma 6 CFU: si arriva fino al file **14 (Trasporto generalizzato)** incluso.

> **Prima di distribuire le ore, leggi [`../pratica/00_ANATOMIA_ESAME.md`](../pratica/00_ANATOMIA_ESAME.md).** Questa guida è ordinata in modo **didattico** (ogni capitolo poggia sul precedente) e assegna tempi uniformi, ma l'esame non pesa i capitoli in modo uniforme. Su 12 appelli censiti:
>
> - cap. 11-12 (rilassamenti e dualità) → **7 appelli su 12**
> - cap. 05 (Floyd-Warshall) → **6 su 12**
> - cap. 04 (Dijkstra) → 4 su 12
> - cap. 14 (trasporto/flussi) → **0 su 12** (solo orale: non esistono tracce d'esame su questo capitolo)
>
> Usa l'ordine di questa guida per **capire**, e i pesi dell'anatomia per decidere **quanto esercitarti** su ciascun capitolo.

> **Le dimostrazioni non servono solo all'orale.** Nel formato recente (esonero 2022, foglio 7 del 2026) alcune dimostrazioni sono esercizi **dello scritto**. Vedi la checklist in fondo, sezione "da saper scrivere".

**Abbinamento teoria → pratica.** Nel Blocco A è 1:1 (teoria 0X → `../pratica/0X_*`).
Nel Blocco B la pratica raggruppa più argomenti di teoria:
| Teoria | Pratica |
|---|---|
| 07 PI + 08 Ott. combinatoria | `07_esercizi_PI.md` |
| 09 TSP/Localizzazione + 10 Formulazioni | `08_esercizi_TSP_localizzazione.md` |
| 11 Rilassamenti + 12 Dualità | `09_esercizi_rilassamenti_dualita.md` |
| 13 TU/Interezza | `11_esercizi_TU.md` |
| 14 Trasporto/Flussi | `12_esercizi_flussi_trasporto.md` |

Tempo totale teoria: **~23 ore**. Con la pratica raddoppia circa.

---

## Come usare questa guida

1. Leggi il file di teoria del passo.
2. Fissa la **dimostrazione** indicata (all'orale contano quelle - vedi elenco in fondo).
3. Rispondi alla **domanda di autocontrollo** senza guardare gli appunti.
4. Fai gli esercizi di pratica abbinati (vedi tabella di abbinamento sopra).
5. Spunta la casella nel tracker.

---

## BLOCCO A - Algoritmi sui grafi (file 01-06)

### Passo 1 - `01_teoria_grafi.md` (1-2h)
Vocabolario di base: senza questo il resto non si capisce.
- **Dimostrazione chiave:** Teorema di Fulkerson (numerabilità progressiva ⟺ no circuiti).
- **Autocontrollo:** differenza fra ciclo euleriano e hamiltoniano? Perché in un albero |A| = |V|−1?

### Passo 2 - `02_BFS_DFS.md` (1h)
Esplorazione grafi; BFS = cammini minimi in numero di archi.
- **Dimostrazione chiave:** Lemma BFS (w ∈ L_k ⟺ d(s,w)=k) per induzione, entrambe le direzioni.
- **Autocontrollo:** quando uso BFS e quando DFS?

### Passo 3 - `03_bellman.md` (1.5h)
Cammini minimi su DAG, anche pesi negativi.
- **Dimostrazioni chiave:** Principio di ottimalità (per assurdo) + teorema di unicità.
- **Autocontrollo:** perché Bellman non regge coi circuiti negativi?

### Passo 4 - `04_dijkstra.md` (1.5h)
Cammini minimi con pesi ≥ 0, anche con circuiti.
- **Dimostrazione chiave:** lemma di correttezza; capire **dove** serve ℓ_ij ≥ 0.
- **Autocontrollo:** compila a memoria la tabella Bellman vs Dijkstra.

### Passo 5 - `05_floyd_warshall.md` (2h)
Cammini minimi fra tutte le coppie; rileva circuiti negativi.
- **Dimostrazione chiave:** giustificazione della formula ricorsiva via principio di ottimalità.
- **Autocontrollo:** come ti accorgi di un circuito negativo durante l'esecuzione?

### Passo 6 - `06_MST.md` (1h)
Albero ricoprente minimo (Prim).
- **Dimostrazione chiave:** Lemma fondamentale degli MST (per assurdo, scambio archi).
- **Autocontrollo:** enuncia il corollario per S = {v}.

> **Checkpoint Blocco A:** sai dire a voce, dato un grafo, quale algoritmo di cammino minimo scegliere e perché? (BFS / Bellman / Dijkstra / Floyd-Warshall)

---

## BLOCCO B - Programmazione intera & ottimizzazione combinatoria (file 07-14)

### Passo 7 - `07_programmazione_intera.md` (1h)
PL vs PI vs PIB vs PIM; perché la PI è difficile.
- **Autocontrollo:** perché non basta arrotondare la soluzione del rilassamento lineare?

### Passo 8 - `08_ottimizzazione_combinatoria.md` (2h)
Da POC a PIB; problemi classici (zaino, assegnazione, set covering/packing/partition).
- **Autocontrollo:** scrivi la formulazione dello zaino 0-1 e del set covering a memoria.

### Passo 9 - `09_TSP_localizzazione.md` (2h)
Formulazioni di TSP (eliminazione sotto-tour) e localizzazione impianti (UFL/CFL).
- **Domanda ricorrente:** quale formulazione UFL è migliore? → **UFL3** (P_3 ⊆ P_2).
- **Autocontrollo:** le due formulazioni di eliminazione sotto-tour (cut-set vs subtour).

### Passo 10 - `10_formulazioni.md` (1.5h)
Prospettiva geometrica: poliedri, Conv(X), "P_1 ⊆ P_2 ⟹ migliore".
- **Autocontrollo:** perché Conv(X) è la formulazione ideale ma non si usa in pratica?

### Passo 11 - `11_rilassamenti.md` (2h)
Rilassamento lineare, combinatori (1-alberi per STSP), lagrangiano.
- **Dimostrazione chiave:** le 3 proprietà del rilassamento; proposizione L*_u ≥ z*.
- **Autocontrollo:** cos'è un 1-albero e perché ogni tour è un 1-albero ma non viceversa?

### Passo 12 - `12_dualita.md` (2h)
Dualità debole/forte; costruzione del duale via rilassamento PL; matching vs copertura.
- **Autocontrollo:** perché matching/copertura non sono in dualità forte in generale (triangolo)?

### Passo 13 - `13_TU_interezza.md` (2h) - il più importante
Matrici TU e Teorema di Interezza: quando un PI è "facile".
- **Dimostrazione chiave:** Teorema di Interezza (le 3 equivalenze) e König su grafo bipartito.
- **Autocontrollo:** quando la matrice di incidenza nodi-archi è TU? (orientato / bipartito / generico)

### Passo 14 - `14_trasporto_flussi.md` (2h) - ultima del programma
Flusso di costo minimo e trasporto generalizzato; tutto si riduce a questo.
- **Autocontrollo:** riproduci a memoria la tabella "problema → riduzione a flusso".

> **Checkpoint Blocco B:** dato un problema, sai (1) formularlo come PI/PIB, (2) dire se è "facile" (matrice TU ⟹ basta il rilassamento lineare) oppure se serve una stima duale via rilassamento?

---

## Ripasso finale (prima dell'appello)

1. Ripassa **solo le dimostrazioni** (elenco sotto) - sono il cuore dell'orale.
2. Rivedi le **domande ricorrenti** qui sotto.
3. Fai la simulazione completa: `../pratica/13_simulazione_esame.md`.

### Dimostrazioni da saper SCRIVERE (escono allo scritto)

Fonti: `Elly/8_Rilassamenti_e_Dualità/ese_7_2026.pdf`, `Elly/9_Matrici_TU_e_Teorema_di_Interezza/sol_es_Lez_19_20.pdf`, esonero 2022.

- [ ] Dato un programma e una sua modifica, **provare che è un rilassamento** (verificare le due condizioni: `X ⊆ T` e `f(x) ≥ c(x)` su X) - esonero 2022 es. 3
- [ ] Se `P = Conv(X)` e `x*` è SBA ottima di (PL), allora `x*` è ottima per (PI) - foglio 7 es. 2
- [ ] Se `x* ∈ S` allora è ottima per (PI); se `c^T x* = c^T x̂` con `x̂ ∈ S` allora `x̂` è ottima - foglio 7 es. 3
- [ ] Condizione di ottimalità lagrangiana: `ū ≥ 0`, `x̄` ottima di `P(ū)`, ammissibile per (P) e `ū^T(Dx̄ − d) = 0` ⟹ `x̄` ottima per (P) - esonero 2022 es. 6 (facoltativo)
- [ ] `A` TU ⟹ i vertici di `P*(A,b)` sono interi, per ogni `b` intero (si passa a `Â = [A | Iₘ]`, anch'essa TU) - Lezioni 19-20

Sono cinque, tutte corte, tutte con soluzione disponibile. Vanno provate a penna almeno una volta ciascuna: saperle "a senso" non basta per scriverle.

### Dimostrazioni da saper esporre a voce (checklist)
- [ ] Teorema di Fulkerson (numerabilità progressiva)
- [ ] Lemma BFS (w ∈ L_k ⟺ d(s,w)=k)
- [ ] Principio di ottimalità di Bellman (per assurdo)
- [ ] Teorema di unicità delle equazioni di Bellman
- [ ] Correttezza di Dijkstra (ruolo di ℓ_ij ≥ 0)
- [ ] Formula ricorsiva di Floyd-Warshall
- [ ] Lemma fondamentale degli MST (per assurdo)
- [ ] 3 proprietà del rilassamento + proposizione lagrangiana L*_u ≥ z*
- [ ] Dualità debole matching/copertura (|M| ≤ |R|)
- [ ] Teorema di Interezza (3 equivalenze) + König sul bipartito

### Domande d'esame ricorrenti
- Quale algoritmo di cammino minimo scelgo e perché? (tabella comparativa)
- Quale formulazione UFL è migliore e perché? → UFL3
- Cosa vuol dire "una formulazione è migliore di un'altra"? → P_1 ⊆ P_2
- Quando un PI si risolve col solo rilassamento lineare? → matrice TU (Teorema di Interezza)
- Matching e copertura: dualità debole sempre, forte solo se grafo bipartito (König)

---

## Tracker

| Passo | Teoria | Pratica |
|---|---|---|
| 01 Grafi | [ ] | [ ] 01 |
| 02 BFS/DFS | [ ] | [ ] 02 |
| 03 Bellman | [ ] | [ ] 03 |
| 04 Dijkstra | [ ] | [ ] 04 |
| 05 Floyd-Warshall | [ ] | [ ] 05 |
| 06 MST | [ ] | [ ] 06 |
| 07 PI | [ ] | [ ] 07 |
| 08 Ott. combinatoria | [ ] | (in 07) |
| 09 TSP/Localizzazione | [ ] | [ ] 08 |
| 10 Formulazioni | [ ] | (in 08) |
| 11 Rilassamenti | [ ] | [ ] 09 |
| 12 Dualità | [ ] | (in 09) |
| 13 TU/Interezza | [ ] | [ ] 11 |
| 14 Trasporto/Flussi | [ ] | [ ] 12 |
| Simulazione finale | [ ] 13 | |
