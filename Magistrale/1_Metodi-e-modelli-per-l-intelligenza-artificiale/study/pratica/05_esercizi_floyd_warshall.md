# 05 - Esercizi: Floyd–Warshall

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/5_Cammini_Minimi_Floyd_Warshall/ese_4_2026.pdf` | es. 1 costi macchinari → cammino minimo con Dijkstra; **es. 2 completare F-W da `D^(0)`/`P^(0)`** su 4 nodi con pesi negativi |
| `Elly/5_Cammini_Minimi_Floyd_Warshall/Lezioni 9-10.pdf` | due esempi svolti: grafo 4 nodi con circuito negativo riconosciuto, grafo 5 nodi senza circuiti |
| `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` | svolgimento del foglio 4 (su Elly la soluzione non c'è) |
| `esami nicolodi risolti.pdf` | **6 tracce svolte**: 13 lug 2005, 20 set 2005, 9 feb 2006, 26 giu 2006, 22 gen 2007, 20 giu 2007 |
| `parziale/WhatsApp Image 2024-03-28*` | esercizio 1 dell'esonero 2022, stessa forma |

**Questo è l'esercizio più frequente dell'esame: 6 appelli su 12, più l'esonero.** Nella forma tipica non parti da zero, ma da `D^(k)` e `P^(k)` già calcolate ("la terza iterazione ha prodotto le seguenti matrici: completare l'algoritmo"). Sei tracce svolte sono abbondanti: usane 3 per imparare e 3 come verifica a freddo.

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
