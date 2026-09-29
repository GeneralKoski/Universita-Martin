# 07 - Esercizi: Programmazione Intera

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/ese_5_2026.pdf` | 6 città con distanze stradali, centro servizi installabile in ogni nodo, copertura entro 11 km → formulare il PI che minimizza le installazioni (**set covering**; prima vanno calcolati gli insiemi di copertura) |
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/ese_6_2026.pdf` | **5 esercizi di sola formulazione**: (1) vincoli logici su 7 investimenti con binarie, (2) attivazione corsi con min/max studenti, (3) scelta corsi minimizzando le ore del venerdì, (4) cutting-stock, (5) sequenziamento su macchina singola (PIM) |
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/ese_6_2026_sol.pdf` | soluzioni del foglio 6, complete di definizione delle variabili |
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/sol-ese-cop-seq-stsp.pdf` | soluzioni di copertura, sequenziamento e STSP |
| `Elly/8_Rilassamenti_e_Dualità/ese_7_2026.pdf` es. 1 | localizzazione supermercati siti × distretti → **impaccamento** (soluzione in `sol-ese-7.pdf`, con la matrice di incidenza scritta per esteso) |
| `esonero 2022` es. 5 | 6 clienti serviti da 4 rotte → set covering |

L'esercizio 1 del foglio 6 (i 6 vincoli logici con variabili binarie) è il più utile in assoluto: sono esattamente i pattern che servono per tradurre qualunque testo. Vale la pena saperli scrivere a memoria.

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
