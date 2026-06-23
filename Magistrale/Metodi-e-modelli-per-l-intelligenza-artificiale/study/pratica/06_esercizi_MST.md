# 06 — Esercizi: MST

## Esercizi disponibili
- Esempio nelle Lezioni 11-12.pdf
- 📂 `Elly/6_Albero_Ricoprente_Minimo_(MST) /sol_esercizi_(3.4bisese_2).pdf`
- 📂 `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf`

## Schema operativo
1. Scegli un nodo iniziale arbitrario
2. Aggiungi l'arco più breve uscente
3. Lista i nodi connessi ↔ archi candidati (uscenti dal sottoalbero corrente verso nodi non connessi)
4. Aggiungi quello di costo minimo. In caso di pareggio: nota la scelta multipla.
5. Ripeti finché non sono tutti collegati (n−1 archi)
6. Calcola il costo totale

## Domande tipiche d'esame
- "Calcolare un MST sul grafo G."
- "Determinare quanti MST distinti esistono sul grafo G." (in caso di archi con stesso peso)
- "Calcolare un 1-albero minimo per il rilassamento del STSP" (vedi Cap. 11): 2 archi minimi su nodo 1 + MST sui nodi {2,…,n}

## Errori da evitare
- Aggiungere un arco che chiude un ciclo (l'algoritmo greedy non lo farebbe se segui le regole)
- Sbagliare a contare gli archi: |A_T| = n − 1
- Dimenticare che MST richiede grafo **non orientato**

## Tempo stimato: 1 ora
