# 7 - Programmazione Lineare & Ottimizzazione Combinatoria (Lezioni 13-14, 15-16)

## Contenuto cartella
- `Lezioni 13-14.pdf` - PI, PIB, PIM, problemi di OC, formulazioni
- `Lezioni 15-16.pdf` - TSP, modellizzazione binaria, UFL/CFL, formulazioni e prospettiva geometrica
- `ese_5_2026.pdf`, `ese_6_2026.pdf`, `ese_6_2026_sol.pdf` - esercizi
- `sol-ese-cop-seq-stsp.pdf` - soluzioni copertura/sequencing/STSP

## Lezioni 13-14: introduzione alla PI

### Tipologie di programmi
- **PL**: max c^T x, Ax ≤ b, x ≥ 0, x ∈ ℝⁿ (variabili continue)
- **PI**: come PL ma x ∈ ℤⁿ (variabili intere)
- **PIB** (Programma Intero Binario / 0-1): x ∈ {0,1}ⁿ
- **PIM** (Programma Intero Misto): alcune variabili intere, altre continue

### Perché la PI è difficile
- Molti problemi reali richiedono variabili intere o decisioni discrete
- I metodi della PL **non funzionano** direttamente
- Servono algoritmi specifici: branch & bound, piani di taglio, ecc.

### Problemi di Ottimizzazione Combinatoria (POC)
Dati N = {1,…,n}, c: N → ℝ, X ⊆ 𝒫(N) (insieme ammissibile di sottoinsiemi), funzione obiettivo z(S) = Σ_{j∈S} c_j. Si cerca max/min su X.

**Esempi**: MST, cammino minimo, **assegnazione**, copertura, ecc.

**Proprietà**: insieme ammissibile **finito** ⟹ esiste enumerazione totale, ma impraticabile (cfr. esempio Dantzig: 70 lavori → 70! ≈ 10¹⁰⁰, irrealizzabile).

### POC ↔ variabili binarie
Ogni S ⊆ N si rappresenta con x ∈ {0,1}ⁿ ponendo x_j = 1 se j ∈ S. Quindi ogni POC si formula come PIB.

### Esempi PIB classici
- **Zaino 0-1 (knapsack)**: max Σ c_j x_j, Σ a_j x_j ≤ b, x ∈ {0,1}ⁿ
- **Assegnazione**: min Σ c_ij x_ij, Σ_j x_ij = 1 (∀i), Σ_i x_ij = 1 (∀j), x_ij ∈ {0,1}
- **Set Covering** (copertura): min c^T x, Ax ≥ e, x ∈ {0,1}ⁿ - A matrice di incidenza
- **Set Packing** (impaccamento): max c^T x, Ax ≤ e, x ∈ {0,1}ⁿ
- **Set Partition** (partizione): max c^T x, Ax = e, x ∈ {0,1}ⁿ

## Lezioni 15-16: modellizzazione avanzata e formulazioni

### TSP - Problema del Commesso Viaggiatore
Dato G = (V, A) orientato completo, c_ij costo arco, trovare un **circuito hamiltoniano (tour)** di costo minimo. È un POC con |X| = (n−1)!.

**Variabili**: x_ij = 1 se (i,j) è nel tour.
**Vincoli base**:
- x_ij ∈ {0,1}
- Σ_j x_ij = 1 (∀i): si esce da i una sola volta
- Σ_i x_ij = 1 (∀j): si entra in j una sola volta

**Eliminazione dei sotto-tour** (due formulazioni equivalenti):
- **Cut-set**: Σ_{i∈S, j∉S} x_ij ≥ 1, ∀S ⊂ V, S ≠ ∅, V
- **Subtour elimination**: Σ_{i,j∈S} x_ij ≤ |S|−1, ∀S, 2 ≤ |S| ≤ n−1

### Modellizzazione con variabili binarie (pattern)
- **Scelta binaria**: x_j ∈ {0,1}
- **Relazioni**: nessuno o entrambi 5,6 ⟹ x_5 − x_6 = 0
- **Vincoli di selezione**: almeno k progetti ⟹ Σ x_j ≥ k
- **Vincoli disgiuntivi** (almeno uno di due vincoli): si introduce y ∈ {0,1} e M-grandi
- **Restrizione su valori discreti**: y ∈ {a_1,…,a_k} ⟹ y = Σ a_j x_j, Σ x_j = 1, x_j ∈ {0,1}

### UFL - Localizzazione di Impianti senza Capacità
Dati: clienti M, siti candidati N, domanda d_i, costo apertura f_j, costo unitario c_ij.

**Variabili**: y_j = 1 se si apre l'impianto j; z_ij = quantità servita a i da j (oppure x_ij = z_ij/d_i = frazione).

**Modello 1** (UFL1): vincolo aggregato Σ z_ij ≤ K y_j (K grande).
**Modello 2** (UFL2): vincolo aggregato Σ x_ij ≤ m y_j.
**Modello 3** (UFL3): vincoli disaggregati x_ij ≤ y_j (∀i,j) - **più stringente**, formulazione migliore.

### CFL - Localizzazione con Capacità
Vincolo aggiuntivo: Σ_i z_ij ≤ u_j y_j (capacità u_j dell'impianto j).

### Formulazioni - Prospettiva Geometrica
- **Poliedro** P ⊆ ℝⁿ⁺ᵖ: P = {x: Ax ≤ b}
- **Formulazione** per X ⊆ ℤⁿ × ℝᵖ: poliedro P tale che X = P ∩ (ℤⁿ × ℝᵖ)
- **Formulazione migliore**: P_1 ⊂ P_2 ⟹ P_1 è migliore (rilassamento lineare più stretto, stime migliori su z*)
- **Inviluppo convesso** Conv(X): se X è regione ammissibile di un PI/PIM, Conv(X) è un poliedro
- **Formulazione ideale** = Conv(X): risolvendo il rilassamento lineare di Conv(X) si ottiene direttamente la soluzione del PI

**Esempio**: per il problema Zaino 0-1, formulazioni con vincoli "spezzati" (Σ a_j x_j ≤ b sostituito da disuguaglianze valide più strette) sono migliori.
