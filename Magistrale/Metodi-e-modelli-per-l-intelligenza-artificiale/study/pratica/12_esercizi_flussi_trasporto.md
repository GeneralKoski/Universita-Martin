# 12 — Esercizi: flussi, trasporto e problemi riducibili

## Esercizi disponibili
- Esempi nelle Lezioni 21-22.pdf
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` — vari problemi di flusso/trasporto

## Tipologie di esercizio

### A) Formulare un problema come flusso di costo minimo
1. Identifica nodi e archi del grafo orientato G = (V, A)
2. Per ogni nodo assegna b_k: sorgente (>0), pozzo (<0), transito (=0)
3. Verifica bilanciamento: Σ b_k = 0 (se manca, aggiungi sorgenti/pozzi fittizi)
4. Capacità h_ij e costi c_ij sugli archi
5. Scrivi il PL: min c^T x, Ax = b, 0 ≤ x ≤ h

### B) Massimo flusso → flusso di costo minimo
1. Aggiungi un arco fittizio (t, s) con h_ts = ∞, c_ts = −1
2. Tutti gli altri archi: c_ij = 0
3. Tutti i nodi diventano nodi di transito (b_k = 0)
4. Risolvi min c^T x: massimizzare x_ts equivale a massimizzare il flusso da s a t

### C) Problema di assegnazione
- Grafo bipartito completo: n persone (V_1) ↔ n lavori (V_2)
- Variabili x_ij ∈ {0,1} (oppure ≥ 0 per il rilassamento, che è equivalente per TU)
- Vincoli: Σ_j x_ij = 1 ∀i, Σ_i x_ij = 1 ∀j
- Si risolve come PL grazie alla TU della matrice di incidenza bipartita

### D) Cammino minimo come flusso di costo minimo
- b_s = 1, b_t = −1, b_k = 0 per gli altri
- Costi c_ij = lunghezze
- Variabili x_ij ∈ [0,1] (rilassamento) hanno SBA ottime in {0,1} grazie alla TU

### E) Matching bipartito come flusso
1. Costruisci R(G): aggiungi sorgente s con archi verso V_1, pozzo t con archi da V_2
2. Capacità 1 su tutti gli archi
3. Calcola flusso massimo da s a t (es. Ford-Fulkerson) → cardinalità del matching

## Domande tipiche d'esame
- "Formulare il seguente problema come flusso di costo minimo"
- "Mostrare che la matrice dei vincoli è TU"
- "Risolvere il problema di assegnazione data la matrice dei costi"
- "Ridurre il seguente problema di matching bipartito a un problema di flusso massimo"

## Tempo stimato: 3 ore
