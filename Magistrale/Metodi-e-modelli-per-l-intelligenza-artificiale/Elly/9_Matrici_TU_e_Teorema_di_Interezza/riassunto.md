# 9 — Matrici Totalmente Unimodulari e Teorema di Interezza (Lezioni 19-20)

## Contenuto cartella
- `Lezioni 19-20.pdf` — TU, teorema di interezza, applicazione dualità forte
- `sol_es_Lez_19_20.pdf` — soluzione esercizio

## Argomenti

### Quando un PI è "facile"
Due possibili definizioni:
1. **Inviluppo convesso esplicito**: conosciamo Conv(X) come poliedro descritto da disuguaglianze, e possiamo rimpiazzare il PI col rilassamento lineare.
2. **Dualità forte**: esiste un duale (D) di (PI) con w* = z*, che dà criteri di ottimalità facilmente verificabili.

### Quando basta il rilassamento lineare
Per (PI) max c^T x, Ax = b, x ≥ 0, x ∈ ℤⁿ:
- SBA del PL: x̂ = (B⁻¹b, 0)ᵀ, B matrice di base m×m
- Se **det B = ±1** ⟹ x̂ è intera (perché B⁻¹ = (1/det B)·cofattori, e b intero)
- Se **tutte** le matrici di base hanno det ±1 e b è intero ⟹ ogni SBA ottima è intera

### Matrici Totalmente Unimodulari (TU)
**Definizione**: A intera è TU se ogni sua sottomatrice quadrata ha det ∈ {−1, 0, +1}.
**Conseguenza**: a_ij ∈ {0, −1, 1}.

### Riconoscimento — condizioni necessarie e sufficienti (equivalenze)
A è TU ⟺ Aᵀ TU ⟺ −A TU ⟺ [A, A] TU ⟺ [A, I] TU ⟺ [A, −A] TU ⟺ [A; I] TU ⟺ [A; −I] TU.

Le operazioni elementari (scambio righe/colonne, cancellazione, moltiplicare per −1) **preservano** la TU.

### Riconoscimento — condizione sufficiente operativa
A è TU se:
1. a_ij ∈ {0, −1, 1}
2. Ogni colonna ha **al massimo 2 coefficienti non nulli**
3. Le righe si partizionano in M_1, M_2 tali che:
   - se una colonna ha due "+1" (o due "−1"), questi stanno in righe di **insiemi diversi**;
   - se una colonna ha un "+1" e un "−1", questi stanno in righe dello **stesso insieme**.

### Matrici di incidenza nodi-archi
- **Grafo orientato**: matrice di incidenza nodi-archi è **sempre TU** (colonne hanno esattamente un +1 e un −1; partizione banale M_1 = M, M_2 = ∅)
- **Grafo non orientato**: in generale **non** TU (es. triangolo K_3, det = 2)
- **Grafo bipartito non orientato**: matrice di incidenza nodi-archi **TU** (V = V_1 ∪ V_2 dà la partizione)

### Teorema di Interezza

**Forma standard** (Ax = b, x ≥ 0):
Sia A intera con rg A = m.
1. Se A è TU ⟹ vertici di P(A,b) sono interi per ogni b ∈ ℤᵐ con P(A,b) ≠ ∅
2. Se A è TU ⟹ max{c^T x : Ax = b, x ≥ 0} ammette SBA ottima intera (∀ b intero)
3. Se A è TU ⟹ il duale min{b^T y : Aᵀy ≥ c, y ∈ ℝᵐ} ammette SBA ottima intera

**Forma canonica** (Ax ≤ b, x ≥ 0): vale anche **viceversa**:
- Vertici di P*(A,b) interi ∀ b intero ⟺ A è TU [Hoffman-Kruskal 1956, Veinott-Dantzig 1967]

### Applicazione: dualità forte matching/copertura
Su grafo G non orientato:
- (PI1) max accoppiamento: max e^T x, Ax ≤ e, x ∈ {0,1}^m (A = matrice incidenza)
- (PI2) min copertura per nodi: min e^T y, Aᵀy ≥ e, y ∈ {0,1}^n

Catena: z_PI ≤ z*_PI ≤ z*_PL = w*_PL ≤ w*_PI ≤ w_PI (dualità debole).

**Se G è bipartito** ⟹ A è TU ⟹ z*_PI = z*_PL = w*_PL = w*_PI ⟹ **dualità forte** (Teorema di König).
