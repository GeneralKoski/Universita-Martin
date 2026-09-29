# 04 - Esercizi: Dijkstra

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/4_Cammini_Minimi_Dijkstra/ese_3.1_2026.pdf` | equazioni di Bellman sul grafo piccolo (ripreso dal foglio 2) + **Dijkstra da 1=A a tutti gli altri** su un grafo di 8 nodi A-H |
| `Elly/6_Albero_Ricoprente_Minimo_(MST)/sol-ese-dijkstra(ese3.1).pdf` | soluzione dell'esercizio sopra |
| `Elly/5_Cammini_Minimi_Floyd_Warshall/ese_4_2026.pdf` es. 1 | matrice costi `c_ij` = acquisto macchinari inizio anno i → fine anno j: interpretare come cammino minimo e risolvere **con Dijkstra** |
| `Elly/4_Cammini_Minimi_Dijkstra/Sol-piano-rinn-ott.pdf` | soluzione del piano di rinnovo (l'esercizio è nel foglio 3, capitolo Bellman) |
| `esami nicolodi risolti.pdf` | **4 tracce svolte**: 28 giugno 2005 es. 2, 6 settembre 2005 es. 1, 20 settembre 2006 es. 1, 19 febbraio 2007 es. 1 (quest'ultima con nodi A-H) |

Dijkstra esce in **4 appelli su 12**: è il secondo esercizio più frequente dopo Floyd-Warshall e il duale lagrangiano. Le 4 tracce svolte bastano per allenarlo fino all'automatismo.

## Schema operativo (tabella iterazioni)
1. Tabella con colonne = nodi, righe = (λ, p) per ogni iterazione
2. **Iter 0**: λ(s) = 0*, λ(altri) = ∞, p tutti 0; s diventa permanente
3. **Aggiornamento**: per ogni successore j di r (ultimo permanente):
   - se λ(j) > λ(r) + ℓ_rj → aggiorna λ e p
4. **Scelta**: trova il nodo con λ minimo tra i temporanei → diventa permanente (asterisco *)
5. Ripeti finché destinazione (o tutti) permanenti
6. **Back-tracking**: dal target risali coi predecessori

## Trucchi
- Usa colonne separate "λ" e "p" per ogni iterazione (più leggibile)
- Asterisca il valore che diventa permanente in quell'iterazione
- Il valore λ di un nodo, una volta permanente, **non cambia più**
- Se un arco è non orientato, trattarlo come due archi orientati di pari peso

## Errori da evitare
- Aggiornare λ di un nodo già permanente (non si fa)
- Dimenticare che ℓ_ij ≥ 0 è ipotesi: se ci sono pesi negativi, Dijkstra **non è valido**

## Tempo stimato: 2 ore
