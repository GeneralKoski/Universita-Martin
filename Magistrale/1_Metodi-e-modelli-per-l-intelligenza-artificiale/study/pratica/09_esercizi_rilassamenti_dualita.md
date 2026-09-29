# 09 - Esercizi: rilassamenti e dualità

> ⚠️ **Capitolo più importante per lo scritto.** Il rilassamento/duale lagrangiano esce in **7 appelli su 12** (vedi `00_ANATOMIA_ESAME.md` §1): è l'esercizio singolo più frequente dell'esame. Le due procedure meccaniche da automatizzare sono in `00_ANATOMIA_ESAME.md` §2.

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/8_Rilassamenti_e_Dualità/ese_7_2026.pdf` | es. 1 impaccamento (localizzazione supermercati); **es. 2 e 3 sono dimostrazioni**: `P = Conv(X)` + SBA ottima di (PL) ⟹ ottima per (PI); e `x* ∈ S` ⟹ ottima, `c^T x* = c^T x̂` ⟹ `x̂` ottima |
| `Elly/8_Rilassamenti_e_Dualità/sol-ese-7.pdf` | soluzioni del foglio 7 |
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/sol-ese-cop-seq-stsp.pdf` | 1-albero minimo su 6 nodi, svolto |
| `esami nicolodi risolti.pdf` | **7 tracce di duale lagrangiano svolte**: 28 giu 2005 es. 4, 13 lug 2005 es. 4, 20 set 2005 es. 2, 17 gen 2006 es. 3, 9 feb 2006 es. 2, 20 lug 2006 es. 2, 19 feb 2007 es. 2 |
| quiz Elly (`NICOLODI REVISIONI 1.pdf`) | rilassamento lagrangiano con `u` **dato** (TSP sui vincoli di grado, UFL sui vincoli di domanda) → valore ottimo numerico; `w*_DL` e `z*_PL` dello zaino |
| esonero 2022 es. 3 e 6 | dimostrazioni: "(2) è un rilassamento di (1)"; condizione di ottimalità `ū^T(Dx̄ − d) = 0` |

Nota: il foglio 7 del 2026 copre **teoria e formulazioni**, non il calcolo numerico del duale lagrangiano. Per allenare quel calcolo le uniche fonti sono le 7 tracce d'esame svolte.

## Esercizi tipici

### A) Calcolo 1-albero per STSP
Dato un grafo G non orientato pesato (matrice delle distanze):
1. Trovare i **2 archi minimi** uscenti dal nodo 1
2. Calcolare il **MST** sui nodi {2, …, n}
3. Sommare: il costo del 1-albero = somma dei costi dei due archi + costo MST
4. Verificare se è anche un **tour**: ogni nodo ha grado 2? Allora è un tour ottimo per STSP.

Esempio: Lezioni 17-18.pdf, esercizio con matrice 6×6.

### B) Rilassamento lineare
Dato un PI:
1. Eliminare i vincoli di integralità
2. Risolvere il PL risultante (graficamente se 2 variabili, altrimenti col simplesso)
3. La soluzione del PL è una **stima dall'alto** (per max) sul valore ottimo del PI

### C) Dualità
"Scrivi il duale del seguente PL" - applicazione meccanica delle regole:
- max ↔ min
- Variabili → vincoli (e viceversa)
- ≤ → variabile ≥ 0, ≥ → variabile ≤ 0, = → variabile libera

### D) Rilassamento lagrangiano - scrittura
"Scrivi il rilassamento lagrangiano relativo ai vincoli Dx ≤ d con moltiplicatori u":
- `L_u(x) = c^T x + u^T(d − Dx)`
- `max{L_u(x) : x ∈ X}` con X = vincoli rimasti (integralità compresa)

### E) Duale lagrangiano - calcolo del valore ottimo (l'esercizio da 7/12 appelli)

Due varianti, procedure complete in `00_ANATOMIA_ESAME.md` §2. In sintesi:

**Variante zaino** (n variabili, un vincolo di budget): raccogli ogni `x_j` in `L(μ) = Σ x_j(c_j − μ a_j) + μ b` → tabella dei segni dei coefficienti, che si annullano nei rapporti `c_j/a_j` (gli stessi del rilassamento lineare) → per ogni intervallo di μ poni `x_j = 1` dove il coefficiente è positivo → `L*(μ)` lineare a tratti → grafico → il minimo cade in un punto di rottura.

**Variante 2 variabili** (rilassi un vincolo, risolvi graficamente): disegna la regione e i **punti interi** → traccia la retta parallela alla funzione obiettivo passante per i punti interi ottimi → intersecala col vincolo rilassato preso come uguaglianza → il sistema 2×2 dà il punto, valutato in z dà `w*_DL`.

**L'errore da non fare**: nella variante 2 la retta passa per i punti **interi**, non per i vertici del poliedro.

### F) Conclusione sulla dualità
Quasi tutte le tracce chiudono con "che relazione sussiste fra `z*_PL` e `w*_DL`?". La risposta tipica: sono **uguali**, quindi c'è dualità forte, perché le due regioni ammissibili coincidono. Va detto il perché, non solo constatata l'uguaglianza numerica.

## Tempo stimato: 2-3 ore
