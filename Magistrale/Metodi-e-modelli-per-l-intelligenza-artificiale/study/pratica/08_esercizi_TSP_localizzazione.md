# 08 - Esercizi: TSP, UFL, sequencing

## Esercizi disponibili
- 📂 `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /sol-ese-cop-seq-stsp.pdf` - **soluzioni** copertura, sequencing, STSP
- Esempi nelle Lezioni 15-16.pdf

## TSP - esercizio tipico
"Dato il grafo G con costi c_ij, formulare il problema TSP come PIB. Scrivere variabili, obiettivo e vincoli (con eliminazione sotto-tour)."

**Variabili**: x_ij ∈ {0,1}
**Obiettivo**: min Σ c_ij x_ij
**Vincoli**:
- Σ_j x_ij = 1 ∀i, Σ_i x_ij = 1 ∀j
- Eliminazione subtour (cut-set o subtour elimination)

## UFL - esercizio tipico
"Formulare UFL e confrontare le formulazioni 1, 2, 3. Quale è migliore? Perché?"

→ La 3 (vincoli disaggregati x_ij ≤ y_j) è migliore perché P_3 ⊊ P_2.

Possibile follow-up: "Calcolare il valore ottimo del rilassamento lineare delle tre formulazioni" (mostra che PL_3 ≤ PL_2 ≤ PL_1).

## Sequencing
Schedulazione di lavori su macchina con tempi di setup. Si modella come TSP su grafo dei lavori (i nodi sono i job, gli archi i tempi di transizione).

## Tempo stimato: 2 ore
