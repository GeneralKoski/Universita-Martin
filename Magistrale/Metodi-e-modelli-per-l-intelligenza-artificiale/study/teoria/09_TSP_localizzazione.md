# 09 - TSP e Localizzazione di Impianti

📂 Fonte: `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /Lezioni 15-16.pdf`

## Obiettivi
Saper formulare due problemi classici di OC.

## TSP - Commesso Viaggiatore
Su grafo orientato completo, trovare un **circuito hamiltoniano** di costo minimo.

**Variabili**: x_ij ∈ {0,1}, x_ij = 1 ⟺ (i,j) nel tour
**Vincoli base**:
- Σ_j x_ij = 1, ∀i (si esce una volta)
- Σ_i x_ij = 1, ∀j (si entra una volta)

**Eliminazione sotto-tour** (due formulazioni equivalenti):
- **Cut-set**: Σ_{i∈S, j∉S} x_ij ≥ 1, ∀S ⊂ V, S ≠ ∅, V
- **Subtour elimination**: Σ_{i,j∈S} x_ij ≤ |S|−1, ∀S, 2 ≤ |S| ≤ n−1

Numero esponenziale di vincoli → si aggiungono "lazy" quando violati.

## UFL - Localizzazione senza Capacità
Aprire impianti tra siti N per servire clienti M minimizzando costi totali.

**Variabili**:
- y_j ∈ {0,1}: 1 se apri j
- z_ij ≥ 0: quantità servita a i da j (oppure x_ij = z_ij/d_i frazione)

**Tre modelli** (diversi vincoli di link y-x):
1. **UFL1**: vincolo aggregato Σ z_ij ≤ K y_j (K grande)
2. **UFL2**: Σ x_ij ≤ m y_j
3. **UFL3**: x_ij ≤ y_j ∀i,j (**migliore** - formulazione più stretta)

**Domanda d'esame ricorrente**: "Quale formulazione è migliore?" → la 3, perché ha P_3 ⊆ P_2 (rilassamento lineare più stringente).

## CFL - Localizzazione con Capacità
Aggiunge: Σ_i z_ij ≤ u_j y_j (capacità u_j)

## Tempo stimato: 2 ore
