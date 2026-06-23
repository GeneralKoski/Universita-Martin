# 10 — Formulazioni e prospettiva geometrica

📂 Fonte: `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /Lezioni 15-16.pdf`

## Obiettivi
Capire perché non basta "scrivere" un PI: la qualità della formulazione conta.

## Da sapere a memoria
- **Poliedro**: P = {x : Ax ≤ b}
- **Formulazione** per X ⊆ ℤⁿ: poliedro P tale che X = P ∩ ℤⁿ
- Per uno stesso X esistono **infinite formulazioni** diverse
- **P_1 ⊆ P_2 ⟹ P_1 è migliore** (rilassamento lineare più stretto, stima più accurata di z*)

## Inviluppo convesso
- **Conv(X)** = inviluppo convesso di X = più piccolo insieme convesso che contiene X
- **Proprietà 1**: se X è regione ammissibile di un PI/PIM, Conv(X) è un poliedro
- **Proprietà 2**: i vertici di Conv(X) sono elementi di X
- **Conv(X) è la formulazione "ideale"**: risolvere il rilassamento lineare di Conv(X) dà direttamente la soluzione del PI

## Perché in pratica non si usa Conv(X)
Conv(X) può avere un numero esponenziale di vincoli (es. TSP). Si cercano formulazioni "buone" senza arrivare all'ideale.

## Esempi (importanti per orale)
- 3 formulazioni di X = {(0,0), (1,0), (0,1)} ⊂ ℝ²
- Formulazioni del problema dello Zaino 0-1
- Formulazioni 2 vs 3 di UFL (la 3 è strettamente più piccola)

## Tempo stimato: 1.5 ore
