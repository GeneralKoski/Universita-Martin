# 04 — Esercizi: Dijkstra

## Esercizi disponibili
- 📂 `Elly/4_Cammini_Minimi_Dijkstra/ese_3.1_2026.pdf`
- 📂 `Elly/4_Cammini_Minimi_Dijkstra/Sol-piano-rinn-ott.pdf` — problema "piano di rinnovo ottimale" (applicazione)
- 📂 `Elly/6_Albero_Ricoprente_Minimo_(MST) /sol-ese-dijkstra(ese3.1).pdf`
- 📂 `Appunti_colleghi/Zip_appunti/esami nicolodi risolti.pdf` — esame 28 giugno 2005, esercizio 2

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
