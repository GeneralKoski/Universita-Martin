# 03 - Equazioni di Bellman

📂 Fonte: `Elly/3_Cammini_Minimi_Equazioni_di_Bellman/Lezioni 5-6.pdf`

## Obiettivi
Cammini minimi su grafi orientati con pesi reali (anche negativi, no circuiti negativi).

## Da sapere a memoria
- **Principio di Ottimalità di Bellman**: sottocammini di cammini minimi sono minimi (sapere la **dimostrazione** per assurdo)
- **Equazioni di Bellman**:
  $$x_s = 0, \quad x_j = \min\{x_i + \ell_{ij} : (i,j) \in A\}$$
- Le u_j sono **una** soluzione, non sempre l'unica
- **Teorema di unicità**: se G non ha circuiti di lunghezza ≤ 0, le equazioni hanno soluzione unica = u_j (sapere la dimostrazione: si costruisce un cammino "all'indietro" e si arriva a una contraddizione)
- Su grafi senza circuiti: si usa **numerazione progressiva di Fulkerson** + **risoluzione per sostituzione**

## Quando usare Bellman
- Grafi senza circuiti (DAG)
- Pesi anche **negativi** purché non formino circuiti negativi
- Se ci sono circuiti negativi → Bellman non si applica, usare Floyd–Warshall (che li rileva)

## Tempo stimato: 1.5 ore
