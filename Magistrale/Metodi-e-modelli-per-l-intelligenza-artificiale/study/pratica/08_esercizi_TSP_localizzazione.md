# 08 - Esercizi: TSP, UFL, sequencing

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/sol-ese-cop-seq-stsp.pdf` | tre soluzioni: copertura (foglio 5, con matrice di incidenza 6×6 esplicita), **STSP con 1-albero su 6 nodi** (dalle Lezioni 17-18), sequenziamento (foglio 6 es. 5) |
| `Elly/7_Programmazione_Lineare_&_Ottimizzazione_Combinatoria/Lezioni 15-16.pdf` | formulazioni TSP (cut-set e subtour), UFL1/2/3, CFL, prospettiva geometrica |
| `Elly/8_Rilassamenti_e_Dualità/ese_7_2026.pdf` es. 1 | localizzazione supermercati → impaccamento |
| `esami nicolodi risolti.pdf` | 20 luglio 2006 es. 1 e 20 settembre 2006 es. 2: **1-albero di costo minimo** come limitazione inferiore per il PCVS, con la giustificazione `z*_PCVS ≥ z*_1-albero` |
| quiz Elly | TSP simmetrico 5 nodi, rilassamento lagrangiano sui **vincoli di grado** con `u` dato → valore ottimo numerico; UFL con `u` dato sui vincoli di domanda |

## TSP - esercizio tipico
"Dato il grafo G con costi c_ij, formulare il problema TSP come PIB. Scrivere variabili, obiettivo e vincoli (con eliminazione sotto-tour)."

**Variabili**: x_ij ∈ {0,1}
**Obiettivo**: min Σ c_ij x_ij
**Vincoli**:
- Σ_j x_ij = 1 ∀i, Σ_i x_ij = 1 ∀j
- Eliminazione subtour (cut-set o subtour elimination)

## UFL - esercizio tipico
"Formulare UFL e confrontare le formulazioni 1, 2, 3. Quale è migliore? Perché?"

→ La 3 (vincoli disaggregati x_ij ≤ y_j) è migliore perché P_3 ⊊ P_2.

Possibile follow-up: "Calcolare il valore ottimo del rilassamento lineare delle tre formulazioni" (mostra che PL_3 ≤ PL_2 ≤ PL_1).

## Sequenziamento (foglio 6, es. 5)
Attenzione: nel materiale 2026 il sequenziamento **non** è modellato come TSP. Il problema è: n lavori su macchina singola, `p_j` ore per il lavoro j, `t_j` istante di inizio, peso `w_j`; minimizzare `Σ w_j t_j`.

La formulazione è un **PIM con vincoli disgiuntivi**: per ogni coppia j ≠ k deve valere `t_j + p_j ≤ t_k` **oppure** `t_k + p_k ≤ t_j`. Si introducono binarie `y_jk` = 1 se j precede k, e si scrive

```
(1 − y_jk)·M + t_k − t_j ≥ p_j     ∀ j ≠ k
(1 − y_kj)·M + t_j − t_k ≥ p_k     ∀ j ≠ k
t_j ≥ 0,  y_jk ∈ {0,1}
```

con `M ≫ Σ p_j`. È l'esempio canonico di vincolo disgiuntivo con M-grande, quindi va saputo: soluzione completa in `sol-ese-cop-seq-stsp.pdf`.

## Tempo stimato: 2 ore
