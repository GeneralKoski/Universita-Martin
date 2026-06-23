# 05 — Esercizi: Floyd–Warshall

## Esercizi disponibili
- 📂 `Elly/5_Cammini_Minimi_Floyd_Warshall/ese_4_2026.pdf`
- Esempi nelle Lezioni 9-10.pdf
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` (vari esami)

## Schema operativo
1. Costruisci D⁽⁰⁾: ℓ_ij sugli archi, 0 sulla diagonale, ∞ altrove
2. Costruisci P⁽⁰⁾: i (predecessore di j da i = i stesso), "−" sulla diagonale
3. Per h = 1, 2, …, n:
   - Per ogni cella (i, j) con i ≠ j:
     - $d^h_{ij} = \min(d^{h-1}_{ij},\; d^{h-1}_{ih} + d^{h-1}_{hj})$
     - se cambia, aggiorna anche $p^h_{ij} = p^{h-1}_{hj}$, altrimenti copia
   - **Controllo circuiti negativi**: se $d^h_{ii} < 0$ → STOP
4. Output: D⁽ⁿ⁾ con tutte le distanze, P⁽ⁿ⁾ per ricostruire i cammini

## Suggerimento pratico
- Marca con * le celle che cambiano (rende controllabile la procedura)
- Se l'esercizio chiede solo d_ij per una coppia specifica, calcola tutta la matrice comunque (errori si propagano)
- Al passo h: la riga h e la colonna h **non cambiano** rispetto al passo h-1

## Esercizio classico tipico d'esame
"Implementare Floyd–Warshall sul grafo G. Verificare se ci sono circuiti negativi. Calcolare un cammino minimo dal nodo X al nodo Y."

## Tempo stimato: 2-3 ore (è laborioso ma meccanico)
