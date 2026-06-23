# 06 - Minimum Spanning Tree (MST)

📂 Fonte: `Elly/6_Albero_Ricoprente_Minimo_(MST) /Lezioni 11-12.pdf`

## Obiettivi
Albero ricoprente di costo minimo in un grafo non orientato pesato.

## Da sapere a memoria
- Definizione: T=(V, A_T), |A_T| = n−1, T albero, A_T ⊆ A
- **Lemma fondamentale degli MST**: per ogni S ⊂ V, S ≠ ∅, l'arco (i*, j*) di lunghezza minima con i* ∈ S, j* ∉ S sta in **ogni** MST.
  - Sapere la **dimostrazione per assurdo** (rimpiazzare l'arco f del MST con e produrrebbe un albero più leggero)
- **Corollario**: arco minimo uscente da v ∈ V sta in qualche MST (caso S = {v})

## Algoritmo (Prim semplificato)
1. Inizia da un nodo arbitrario
2. Aggiungi l'arco più breve uscente
3. Ripeti: arco più breve fra connessi e non connessi
4. STOP quando tutti i nodi sono raggiunti

## Pareggi
In caso di archi di pari peso: scelta arbitraria, ma annota tutte le scelte multiple (l'esercizio può chiedere quante MST esistono).

## Applicazioni
- Reti di trasporto/collegamento di costo minimo
- **Rilassamento per STSP via 1-alberi** (vedi cap. 11)
- Clustering

## Tempo stimato: 1 ora
