# 11 — Esercizi: Matrici TU e Teorema di Interezza

## Esercizi disponibili
- 📂 `Elly/9_Matrici_TU_e_Teorema_di_Interezza/sol_es_Lez_19_20.pdf` — esercizio con soluzione

## Tipologie di esercizio

### A) Riconoscere se una matrice è TU
1. **Check coefficienti**: tutti in {0, ±1}? Se no → non TU.
2. **Check colonne**: ognuna ha al massimo 2 non nulli? Se no, **non si può concludere** con la condizione sufficiente (ma potrebbe essere TU lo stesso — vedi i controesempi al teorema necessario).
3. **Check partizione delle righe** in M_1, M_2 secondo le regole:
   - colonne con 2 "+1" o 2 "−1" → righe in **insiemi diversi**
   - colonne con "+1" e "−1" → righe nello **stesso insieme**

Se trovi una partizione che funziona ⟹ TU. Se non riesci, prova anche su Aᵀ.

### B) Dimostrare che una matrice di incidenza è TU
Se è grafo orientato: applica direttamente la regola "ogni colonna ha esattamente un +1 e un −1, partizione banale M_1 = tutto".
Se è grafo bipartito non orientato: V = V_1 ∪ V_2 dà la partizione (M_1 = righe di V_1, M_2 = righe di V_2).

### C) Applicare il Teorema di Interezza
Dato un PI, riconoscere che la matrice dei vincoli è TU (es. è una matrice di incidenza di grafo orientato/bipartito) ⟹ concludere che basta risolvere il rilassamento lineare.

### D) Calcolo SBA del rilassamento lineare
Quando il problema è "facile" (TU + b intero), si può calcolare una SBA ottima:
- Identifica una base B (sottomatrice quadrata invertibile)
- Calcola x_B = B⁻¹ b
- Verifica che det B = ±1 (così la soluzione è intera)

## Tempo stimato: 2-3 ore
