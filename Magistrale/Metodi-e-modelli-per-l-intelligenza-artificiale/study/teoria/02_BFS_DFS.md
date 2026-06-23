# 02 — BFS e DFS

📂 Fonte: `Elly/2_Procedure_BFS_e_DFS/Lezioni 3-4.pdf`

## Obiettivi
Saper esplorare un grafo in due modi e capire **a cosa serve ciascuno**.

## Da sapere a memoria
- **BFS** (Breadth First Search): per **livelli** L_k. Privilegia larghezza.
  - L_k = nodi a distanza geometrica k da s
  - Calcola **cammini minimi in numero di archi** (non in lunghezza pesata!)
- **DFS** (Depth First Search): per profondità con back-tracking.
- Pseudocodice BFS (5 passi)
- Procedura del Labirinto (back-tracking sui livelli per trovare il cammino)

## Teorema/dimostrazione
**Lemma BFS**: w ∈ L_k ⟺ d(s, w) = k.
- Dimostrazione per induzione su k (sapere entrambe le direzioni: ⟹ e ⟸).
- Conseguenza: BFS calcola cammini minimi (in numero di archi).

## Quando usare cosa
- BFS → cammino minimo in archi, problema del labirinto, information retrieval
- DFS → controllo connessione, ricerca cicli, ordinamento topologico

## Tempo stimato: 1 ora
