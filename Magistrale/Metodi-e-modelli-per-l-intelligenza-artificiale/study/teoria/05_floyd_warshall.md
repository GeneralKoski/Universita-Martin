# 05 - Floyd–Warshall

📂 Fonte: `Elly/5_Cammini_Minimi_Floyd_Warshall/Lezioni 9-10.pdf`

## Obiettivi
Cammini minimi **fra tutte le coppie** di nodi in una sola passata.

## Da sapere a memoria
- Significato di $d^h_{ij}$: lunghezza min cammino da i a j usando solo {1,…,h} come intermedi
- **Condizioni iniziali**: D⁽⁰⁾ con ℓ_ij sugli archi, 0 sulla diagonale, ∞ altrove; P⁽⁰⁾ con i (o "−" se i=j)
- **Formula ricorsiva** (sapere la **giustificazione** via principio di ottimalità):
  $$d^h_{ij} = \min\{d^{h-1}_{ij},\; d^{h-1}_{ih} + d^{h-1}_{hj}\}$$
- Aggiornamento di P⁽ʰ⁾: copia se d non cambia, altrimenti prende p^{h-1}_{hj}

## Punto chiave: rilevamento circuiti negativi
- Se in qualche passo $d^k_{ii} < 0$ sulla diagonale → c'è circuito negativo per i, STOP
- Si può comunque ricostruire il circuito con P⁽ᵏ⁾

## Quando usare cosa (riepilogo cammini minimi)
- **BFS** → cammino min in archi (peso unitario)
- **Bellman** → grafi senza circuiti, anche pesi negativi (per sostituzione)
- **Dijkstra** → pesi ≥ 0, anche con circuiti
- **Floyd–Warshall** → tutte le coppie, qualsiasi peso reale, **rileva circuiti negativi**

## Tempo stimato: 2 ore (l'esercizio è laborioso)
