# 09 — Esercizi: rilassamenti e dualità

## Esercizi disponibili
- 📂 `Elly/8_Rilassamenti_e_Dualità/ese_7_2026.pdf`
- 📂 `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /sol-ese-cop-seq-stsp.pdf` (sezione STSP / 1-albero)
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` (più tracce)

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
"Scrivi il duale del seguente PL" — applicazione meccanica delle regole:
- max ↔ min
- Variabili → vincoli (e viceversa)
- ≤ → variabile ≥ 0, ≥ → variabile ≤ 0, = → variabile libera

### D) Rilassamento lagrangiano
"Scrivi il rilassamento lagrangiano relativo ai vincoli Dx ≤ d con moltiplicatori u":
- L_u(x) = c^T x + u^T(d − Dx)
- max{L_u(x) : x ∈ X} con X = vincoli rimasti

## Tempo stimato: 2-3 ore
