# 08 - Ottimizzazione Combinatoria (OC)

📂 Fonte: `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /Lezioni 13-14.pdf`

## Obiettivi
Riconoscere problemi combinatori e formularli come PIB.

## Da sapere a memoria
- POC: dati N = {1,…,n}, c: N → ℝ, X ⊆ 𝒫(N) finito, max/min Σ_{j∈S} c_j su S ∈ X
- Insieme ammissibile **finito** ⟹ esiste enumerazione totale, ma è impraticabile
- Ogni S ⊆ N ↔ vettore binario x ∈ {0,1}ⁿ con x_j = 1 ⟺ j ∈ S
- Ogni POC si formula come PIB

## Esempi classici (sapere formulazione)
- **Zaino 0-1**: max c^T x, a^T x ≤ b, x ∈ {0,1}ⁿ
- **Assegnazione**: min Σ c_ij x_ij, vincoli "uno a uno", x ∈ {0,1}^{n×n}
- **Set Covering** (copertura): min c^T x, Ax ≥ e
- **Set Packing** (impaccamento): max c^T x, Ax ≤ e
- **Set Partition** (partizione): max c^T x, Ax = e

## Trucchi di modellazione binaria
- Scelta: x_j ∈ {0,1}
- Almeno k progetti: Σ x_j ≥ k
- Disgiuntivo (almeno uno di due vincoli): variabile y ∈ {0,1} + M-grandi
- Valori discreti y ∈ {a_1,…,a_k}: y = Σ a_j x_j, Σ x_j = 1

## Tempo stimato: 2 ore
