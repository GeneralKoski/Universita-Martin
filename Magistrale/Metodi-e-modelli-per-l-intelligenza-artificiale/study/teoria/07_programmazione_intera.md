# 07 — Programmazione Intera (PI)

📂 Fonte: `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /Lezioni 13-14.pdf`

## Obiettivi
Capire **cos'è** un PI, perché è difficile, come si distingue dalla PL.

## Da sapere a memoria
- **PL**: max c^T x, Ax ≤ b, x ≥ 0, x ∈ ℝⁿ — variabili continue
- **PI**: come sopra ma x ∈ ℤⁿ — variabili intere
- **PIB**: x ∈ {0,1}ⁿ — binarie/0-1
- **PIM**: alcune intere, altre continue

## Perché la PI è difficile
- I metodi della PL **non funzionano** direttamente (la soluzione del rilassamento lineare in genere è frazionaria)
- Servono algoritmi specifici: **branch & bound**, **piani di taglio**, programmazione dinamica
- Spazio combinatorio enorme (Dantzig: 70 lavori → 70! soluzioni)

## Tempo stimato: 1 ora
