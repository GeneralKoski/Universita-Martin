# 14 — Trasporto Generalizzato e problemi "facili"

📂 Fonte: `Elly/10_Trasporto_generalizzato_(fine_materiale_ 6CFU)/Lezioni 21-22.pdf`

> **Ultima lezione del programma 6 CFU.**

## Obiettivi
Vedere come tanti problemi diversi si riducono tutti al **flusso di costo minimo** su rete, e come la TU della matrice di incidenza li renda risolvibili col solo simplesso.

## Da sapere a memoria

### Problema di flusso di costo minimo
- Capacità h_ij, costi c_ij, sorgente s, pozzo t, valore f del flusso
- Vincoli di **bilancio** sui nodi intermedi (uscente = entrante)
- 0 ≤ x_ij ≤ h_ij

### Trasporto generalizzato
- Ogni nodo k ha b_k ∈ ℝ: > 0 sorgente, < 0 pozzo, = 0 transito
- Σ b_k = 0 (rete bilanciata)
- Formulazione: min c^T x, Ax = b, 0 ≤ x ≤ h
- **A = matrice incidenza nodi-archi del digrafo ⟹ TU**

### Teorema di Interezza per il trasporto
Se h e b sono **interi**, ogni SBA ottima ha **componenti intere** ⟹ flussi interi sugli archi (conseguenza diretta del Teorema di Interezza in forma canonica applicato alla matrice [A; −A; I] che è TU).

## Problemi riconducibili a flusso di costo minimo

| Problema | Riduzione |
|---|---|
| **Massimo flusso** | aggiungere arco (t,s) con h_ts = ∞, c_ts = −1, tutti i nodi di transito |
| **Trasporto (Hitchcock)** | grafo bipartito completo (origini → destinazioni), no nodi di transito |
| **Assegnazione** | caso del trasporto con a_i = b_j = 1 |
| **Cammino minimo** | b_1 = 1, b_n = −1, gli altri 0, x_ij ∈ {0,1} |
| **Matching bipartito (cardinalità max)** | flusso massimo su R(G) con capacità 1 |
| **Matching bipartito pesato** | assegnazione con costi w_ij = −c_ij |

## Conseguenza importante per gli esami
- Per tutti questi problemi su grafi orientati (o bipartiti non orientati): **basta risolvere il rilassamento lineare** (PL) col simplesso e si ottiene una soluzione intera
- Su grafi non orientati non bipartiti: il matching **non è risolvibile col solo PL**, va costruita la rete di flusso o si usa Ford-Fulkerson

## Tempo stimato: 2 ore
