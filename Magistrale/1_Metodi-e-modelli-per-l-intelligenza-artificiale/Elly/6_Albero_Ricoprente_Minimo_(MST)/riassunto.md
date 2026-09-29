# 6 - Albero Ricoprente Minimo / Minimum Spanning Tree (Lezioni 11-12)

## Contenuto cartella
- `Lezioni 11-12.pdf` - algoritmo MST
- `sol_esercizi_(3.4bisese_2).pdf` - soluzioni esercizio
- `sol-ese-dijkstra(ese3.1).pdf` - soluzione esercizio Dijkstra

## Problema
Dato G = (V, A) **non orientato**, con costi ℓ_ij ∈ ℝ sugli archi, trovare un albero ricoprente T = (V, A_T), |A_T| = n−1, di **costo totale minimo**.

## Applicazioni
- Progettazione di reti di trasporto/collegamento di costo minimo
- Problema del Commesso Viaggiatore (rilassamento via MST)
- Clustering

## Proprietà fondamentale degli MST
**Lemma**: sia T* un MST di G. Sia S ⊂ V, S ≠ ∅. Sia e = (i*, j*) ∈ A un arco di **lunghezza minima** con i* ∈ S e j* ∉ S. Allora e è un arco di T*.

**Dimostrazione**: per assurdo, se e ∉ T*, in T* esiste un cammino da i* a j*; sia f = (i,j) il primo arco di tale cammino con i ∈ S, j ∉ S. Per definizione ℓ_ij > ℓ_i*j*, quindi sostituendo f con e si ottiene un albero ricoprente di costo strettamente minore - contraddizione.

**Corollario**: l'arco di lunghezza minima uscente da un qualsiasi nodo è in un MST (S = {v}).

## Algoritmo MST (Prim semplificato)
1. Partire da un nodo arbitrario i. Aggiungere l'arco più breve uscente da i.
2. Se tutti i nodi sono collegati, STOP.
3. Trovare l'arco più breve fra i nodi connessi e i nodi isolati, aggiungerlo. Tornare al passo 2.

In caso di scelte multiple di pari costo, scegliere arbitrariamente.

## Esempio risolto
Grafo a 7 nodi {A,…,G}, partendo da A: archi scelti (A,G), (G,F), (F,E), (E,D), (A,C), (B,C). Costo totale 32.
