# 03 - Esercizi: Equazioni di Bellman

## Esercizi disponibili
- 📂 `Elly/3_Cammini_Minimi_Equazioni_di_Bellman/ese_2_2026.pdf`
- 📂 `Elly/3_Cammini_Minimi_Equazioni_di_Bellman/ese_3_2026.pdf`
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` - esame 28 giugno 2005, esercizio 1 (con soluzione svolta)

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
