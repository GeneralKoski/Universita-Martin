# 8 - Rilassamenti e Dualità (Lezioni 17-18)

## Contenuto cartella
- `Lezioni 17-18.pdf` - rilassamenti, rilassamento lineare, lagrangiano, dualità
- `ese_7_2026.pdf` - esercizio (1-albero e STSP)
- `sol-ese-7.pdf` - soluzione esercizio 7

## Stime per il valore ottimo z*
Dato un problema di max z* = max{c(x): x ∈ X}:
- **Stime primali**: dal basso, fornite da soluzioni ammissibili (ogni x ∈ X dà c(x) ≤ z*).
- **Stime duali**: dall'alto, **più difficili**, ottenute via rilassamenti o problemi duali.

Se le due stime coincidono (z = z̄), la soluzione è ottima. Tolleranza ε: se z̄ − z ≤ ε, soluzione ε-ottima.

## Rilassamenti

### Definizione
(R) max{f(x): x ∈ T} è **rilassamento** di (P) max{c(x): x ∈ X} se:
- (i) X ⊆ T
- (ii) f(x) ≥ c(x), ∀x ∈ X

### Proprietà
1. **z* ≤ z*_R** (rilassamento dà sempre stima dall'alto)
2. Se (R) è inammissibile ⟹ (P) è inammissibile
3. Se l'ottimo x* di (R) appartiene a X **e** f(x*) = c(x*), allora x* è ottimo anche per (P)

## Rilassamento Lineare
Dato un PI: max{c^T x: x ∈ X = P ∩ ℤⁿ}, il **rilassamento lineare** è:
$$(PL): \max\{c^T x : x \in P\}$$

Si rilassa l'integralità. È un PL, risolvibile col simplesso.

**Proposizione**: se P_1 ⊆ P_2 sono due formulazioni di X, allora z*_PL1 ≤ z*_PL2 (formulazione più stretta = stima migliore).
Se P = Conv(X) (formulazione ideale), ogni vertice ottimo di P è soluzione del PI.

## Rilassamenti Combinatori
- **TSP** (asimmetrico): rilassato col problema di assegnazione → z*_TSP ≥ z*_ASS
- **STSP** (simmetrico, c_ij = c_ji): rilassato con i **1-alberi**
  - **1-albero**: 2 archi uscenti dal nodo 1 + un albero ricoprente sui nodi {2,…,n}
  - Ogni tour è un 1-albero, ma non viceversa
  - z*_STSP ≥ z*_1ALB
  - Per calcolare il 1-albero minimo: 2 archi minimi uscenti da 1 + MST sui nodi {2,…,n}

## Rilassamento Lagrangiano
PI con vincoli di disuguaglianza: max{c^T x: Dx ≤ d, x ∈ X}.

**Funzione lagrangiana**: per u ≥ 0 (moltiplicatori/variabili duali),
$$L_u(x) = c^T x + u^T(d - Dx)$$

**Rilassamento lagrangiano**:
$$(PI(u)): L*_u = \max\{L_u(x) : x \in X\}$$

È un rilassamento perché:
- (i) regione ammissibile più ampia (si rilassa Dx ≤ d)
- (ii) per x ammissibile, L_u(x) = c^T x + u^T(d − Dx) ≥ c^T x (perché u ≥ 0 e d − Dx ≥ 0)

⟹ **L*_u ≥ z* per ogni u ≥ 0**. La miglior stima si ottiene risolvendo min_{u≥0} L*_u.

## Dualità

### Dualità debole
Due problemi (P) max{c(x): x ∈ X} e (D) min{w = b(u): u ∈ U} formano **coppia in dualità debole** se:
$$c(x) \leq b(u), \quad \forall x \in X, \forall u \in U$$

**Vantaggio**: ogni soluzione duale dà una stima dall'alto su z* di (P).

### Dualità forte
Se z* = w*, si dice che (P) e (D) sono in **dualità forte**.

### Criterio di ottimalità
Se x̂ ∈ X, û ∈ U e c(x̂) = b(û), allora x̂ è ottima per (P) e û è ottima per (D).

### Costruzione del duale di un PI via rilassamento lineare
PI: z* = max{c^T x: Ax ≤ b, x ≥ 0, x ∈ ℤⁿ}.
Rilassamento lineare PL: max{c^T x: Ax ≤ b, x ≥ 0}.
Duale del PL (DPL): min{b^T y: A^T y ≥ c, y ≥ 0, y ∈ ℝᵐ}.

Per dualità forte della PL: z*_PL = w*_PL. E z*_PI ≤ z*_PL = w*_PL ≤ w_PL per ogni y ammissibile in DPL.
**(PI) e (DPL) sono in dualità debole.**

## Dualità combinatoria
Su grafo non orientato G = (V, A):
- **Accoppiamento (matching)**: M ⊆ A insieme di archi disgiunti (senza nodi in comune)
- **Copertura per nodi**: R ⊆ V tale che ogni arco di G ha almeno un estremo in R

**Proposizione**: max accoppiamento e min copertura sono in **dualità debole** (|M| ≤ |R|, dim. di König).

In generale **non sono in dualità forte** (esempio: triangolo, max matching = 1, min cover = 2).

### Formulazione PI
- Accoppiamento (impaccamento): max e^T x, Ax ≤ e, x ∈ {0,1}ⁿ
- Copertura: min e^T y, B^T y ≥ e, y ∈ {0,1}ⁿ
con A matrice di incidenza nodi-archi.
