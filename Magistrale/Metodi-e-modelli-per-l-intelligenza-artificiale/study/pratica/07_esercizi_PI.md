# 07 - Esercizi: Programmazione Intera

## Esercizi disponibili
- 📂 `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /ese_5_2026.pdf`
- 📂 `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria /ese_6_2026.pdf` (con soluzione `ese_6_2026_sol.pdf`)
- 📂 `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf`

## Tipologie di esercizio

### A) Formulare un problema reale come PI/PIB
Dato un testo (es. "Pronto Soccorso deve scegliere medici per coprire interventi"):
1. Identifica le variabili (binarie? intere? continue?)
2. Scrivi la funzione obiettivo (max/min)
3. Scrivi i vincoli (linkando a parole chiave del testo: "almeno", "esattamente", "al più")
4. Specifica il dominio delle variabili

**Pattern ricorrenti**:
- "scegli 1 fra n" → x_j ∈ {0,1}, Σ x_j = 1
- "almeno k fra n" → Σ x_j ≥ k
- "se y allora deve x" → x ≥ y oppure x − y ≥ 0
- "almeno uno dei due vincoli" → variabile y disgiuntiva + M-grandi

### B) Riconoscere il tipo di problema
"Questo è uno Zaino?" / "Questo è un Set Covering?" / ecc. - leggi attentamente il vincolo (≥ e per copertura, ≤ e per packing, = e per partition).

### C) Confrontare formulazioni
Date due formulazioni P_1 e P_2 dello stesso problema:
- P_1 ⊆ P_2? Se sì, P_1 è migliore
- Calcolare z*_PL1 e z*_PL2 e confrontare

## Tempo stimato: 3 ore
