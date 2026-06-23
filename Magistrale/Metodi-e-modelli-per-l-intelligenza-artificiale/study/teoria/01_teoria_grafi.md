# 01 — Teoria dei grafi (basi)

📂 Fonte: `Elly/1_Elementi_di_Teoria_dei_Grafi/Lezioni 1-2.pdf`

## Obiettivi
Acquisire il vocabolario di base per tutto il corso. Senza questo, il resto non si capisce.

## Da sapere a memoria
- Definizione di grafo G = (V, A): nodi e archi
- Differenze: orientato vs non orientato, semplice, completo, bipartito, misto
- Anelli, archi paralleli, grado (uscente/entrante)
- Sottografo indotto vs grafo parziale
- Cammino, ciclo, connessione
- Cicli **euleriano** e **hamiltoniano**

## Teoremi da conoscere (per l'orale)
1. **Teorema di Eulero (1736)**: G ha ciclo euleriano ⟺ G connesso ∧ ogni nodo ha grado pari
2. **Caratterizzazione albero**: 5 affermazioni equivalenti
3. **Teorema di Fulkerson**: G orientato è numerabile progressivamente ⟺ è senza circuiti — sapere la **dimostrazione** (algoritmo costruttivo)

## Trappole tipiche
- Confondere ciclo euleriano (passa per ogni *arco*) con hamiltoniano (passa per ogni *nodo*)
- Dimenticare che in un albero |A| = |V| − 1
- In un grafo orientato, distinguere "circuito" (orientato) da "ciclo" (non orientato)

## Tempo stimato: 1-2 ore
