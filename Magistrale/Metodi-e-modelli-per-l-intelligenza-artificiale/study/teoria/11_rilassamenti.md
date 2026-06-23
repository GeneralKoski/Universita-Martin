# 11 — Rilassamenti

📂 Fonte: `Elly/8_Rilassamenti_e_Dualità/Lezioni 17-18.pdf`

## Obiettivi
Ottenere stime **dall'alto** sul valore ottimo di un PI, indispensabili per branch & bound.

## Da sapere a memoria
- Stime **primali** (dal basso, da soluzioni ammissibili) vs **duali** (dall'alto, da rilassamenti/dualità)
- **Definizione di rilassamento** (R) di (P): X ⊆ T ∧ f(x) ≥ c(x) ∀x ∈ X
- 3 proprietà fondamentali:
  1. z* ≤ z*_R
  2. (R) inammissibile ⟹ (P) inammissibile
  3. Se ottimo di (R) cade in X **e** f(x*) = c(x*), allora x* è ottimo per (P)

## Tipi di rilassamento

### Rilassamento Lineare
Si rilassa l'integralità: PI → PL (max c^T x su P invece che P ∩ ℤⁿ).

**P_1 ⊆ P_2 ⟹ z*_PL1 ≤ z*_PL2** (formulazione migliore = stima migliore).

### Rilassamenti combinatori
- **TSP** rilassato con Assegnazione (z*_TSP ≥ z*_ASS — è un min!)
- **STSP** (simmetrico) rilassato con **1-alberi**:
  - 1-albero = 2 archi su nodo 1 + MST sui nodi {2,…,n}
  - Ogni tour è un 1-albero, non viceversa
  - z*_STSP ≥ z*_1ALB

### Rilassamento Lagrangiano
PI: max c^T x, Dx ≤ d, x ∈ X.

Funzione lagrangiana: L_u(x) = c^T x + u^T(d − Dx), u ≥ 0.
Rilassamento: PI(u): max{L_u(x) : x ∈ X}.

**Proposizione**: per ogni u ≥ 0, L*_u ≥ z*. Quindi min_{u≥0} L*_u è la migliore stima.

**Perché funziona**: si "incorporano" i vincoli Dx ≤ d nella funzione obiettivo (penalizzando le violazioni). I vincoli rilassati possono rendere il problema molto più facile.

## Tempo stimato: 2 ore
