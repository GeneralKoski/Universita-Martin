# 5 — Cammini Minimi: Floyd–Warshall (Lezioni 9-10)

## Contenuto cartella
- `Lezioni 9-10.pdf` — algoritmo di Floyd–Warshall
- `ese_4_2026.pdf` — esercizio

## Problema
Calcolare cammini minimi **fra tutte le coppie di nodi** di G = (V, A) orientato, con ℓ_ij ∈ ℝ.

Applicazioni: tavole distanze città, problemi di localizzazione e distribuzione.

## Approccio
Diversamente da Bellman/Dijkstra (un nodo sorgente alla volta), Floyd–Warshall costruisce iterativamente, per h = 0, 1, …, n:
- $d^h_{ij}$ = lunghezza del cammino minimo da i a j che usa **solo nodi {1, …, h} come possibili nodi intermedi**
- $p^h_{ij}$ = predecessore di j in tale cammino

## Condizioni iniziali
$$d^0_{ij} = \begin{cases} \ell_{ij} & (i,j) \in A \\ 0 & i=j \\ \infty & \text{altrimenti} \end{cases} \qquad p^0_{ij} = \begin{cases} i & i \neq j \\ - & i=j \end{cases}$$

## Formula ricorsiva
Per h = 1, …, n:
$$d^h_{ij} = \min\{d^{h-1}_{ij},\; d^{h-1}_{ih} + d^{h-1}_{hj}\}, \quad \forall i \neq j$$

**Idea**: nel cammino min da i a j o non si usa h come intermedio (e d^h = d^{h-1}), oppure sì e per il principio di ottimalità il cammino si spezza in min(i→h) + min(h→j).

Aggiornamento predecessori:
$$p^h_{ij} = \begin{cases} p^{h-1}_{hj} & d^h_{ij} \neq d^{h-1}_{ij} \\ p^{h-1}_{ij} & d^h_{ij} = d^{h-1}_{ij} \end{cases}$$

## Output
- $d^n_{ij}$ = lunghezza cammino minimo da i a j (matrice finale D⁽ⁿ⁾).
- $p^n_{ij}$ permette di ricostruire ogni cammino con back-tracking.

## Circuiti negativi
Floyd–Warshall li **rileva**: se in qualche iterazione k compare $d^k_{ii} < 0$ sulla diagonale, allora c'è un circuito negativo passante per i. L'algoritmo si interrompe ma la matrice P⁽ᵏ⁾ permette comunque di ricostruire il circuito.

## Osservazioni
- Funziona anche su grafi non orientati/misti (sostituendo archi non orientati con due archi).
- Esempi risolti nel PDF: grafo 4-nodi con circuito negativo riconosciuto, grafo 5-nodi senza circuiti.
