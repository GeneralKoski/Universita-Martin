# 03 - Esercizi: Equazioni di Bellman

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/3_Cammini_Minimi_Equazioni_di_Bellman/ese_2_2026.pdf` | (a) cammino minimo 1→13 su un DAG di 13 nodi; (b) risolvere le equazioni di Bellman su un grafo piccolo **con un circuito** (3→4→2→3): serve a capire quando la soluzione è unica |
| `Elly/3_Cammini_Minimi_Equazioni_di_Bellman/ese_3_2026.pdf` | **piano di rinnovo ottimale**: macchinario da 12.000 €, tabella manutenzione + ricavato per età, 5 anni → costruire il DAG e risolvere con Bellman |
| `Elly/4_Cammini_Minimi_Dijkstra/Sol-piano-rinn-ott.pdf` | soluzione dell'esercizio sopra (sta nella cartella Dijkstra, non in quella di Bellman) |
| `Elly/6_Albero_Ricoprente_Minimo_(MST)/sol_esercizi_(3.4bisese_2).pdf` | soluzione del foglio 2 |
| `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` pp. 3-4 | **il piano di rinnovo svolto per intero** da un collega: costruzione del DAG, calcolo di tutti i `c_ij`, equazioni di Bellman con predecessori, e i **tre** cammini minimi ottimi (costo 31.000) |
| `esami nicolodi risolti.pdf` | 28 giugno 2005 es. 1 e 17 gennaio 2006 es. 1, entrambi svolti |

## Lo schema "piano di rinnovo": la formula da ricordare

È lo schema più ricorrente di tutto il corso (foglio 3, foglio 4, esonero 2022 es. 4, quiz Elly "bicicletta"). Il grafo ha **nodi = istanti**: nodo i = inizio dell'anno i, ultimo nodo = fine del periodo. L'arco (i, j) con j > i significa "compro all'inizio dell'anno i e rivendo all'inizio dell'anno j", e il suo costo è

```
c_ij = costo di acquisto + Σ(k=1..j-i) m_k − r_(j-i)
```

dove `m_k` = manutenzione durante il k-esimo anno di possesso e `r_(j-i)` = ricavo dalla vendita dopo j−i anni di utilizzo. Sull'ultimo arco non c'è ricavo (non si rivende).

Costruito il grafo, è un DAG già numerato progressivamente: si risolve per sostituzione con Bellman. Vedi anche `00_ANATOMIA_ESAME.md` §3.

## Schema operativo
1. **Verifica**: il grafo è senza circuiti? (altrimenti Bellman non vale)
2. **Fulkerson**: numera progressivamente i nodi (entrata = 1, scendi)
3. **Tabella**: due colonne, lunghezza u_j e predecessore [k]
4. Riempi la tabella in ordine di numerazione:
   - u_1 = 0
   - u_j = min{u_i + ℓ_ij : (i,j) ∈ A, i < j}
   - Annota il predecessore che realizza il minimo
5. **Back-tracking** dal nodo target ai predecessori per ricostruire il cammino

## Errori da evitare
- Non controllare l'ipotesi "senza circuiti"
- Saltare la numerazione progressiva (poi ti perdi)
- Confondere "min" con "max" (Bellman cerca il minimo)
- Dimenticare di annotare i predecessori (necessari per il cammino)

## Tempo stimato: 1.5 ore
