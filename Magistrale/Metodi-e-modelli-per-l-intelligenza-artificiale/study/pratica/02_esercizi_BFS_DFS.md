# 02 — Esercizi: BFS e DFS

## Esercizi disponibili
- 📂 `Elly/2_Procedure_BFS_e_DFS/ese_1_2026.pdf` — esercizio ufficiale 2026
- Esercizi sugli appunti scritti dei colleghi (`AAA METODI E MODELLI...pdf`, prime lezioni)

## Schema operativo BFS
1. Disegna il grafo
2. Scegli un nodo iniziale s
3. Apri parentesi: elenca tutti i nodi adiacenti a s, sottolinea s
4. Per ogni nodo della parentesi corrente, apri una nuova parentesi con i suoi adiacenti **non ancora elencati**
5. Etichetta i livelli L_0, L_1, L_2, …
6. Per il problema del labirinto: parti dal nodo target, risali ai livelli inferiori scegliendo un adiacente del livello L_{k-1}

## Schema operativo DFS
1. Scegli s, etichetta con 1
2. Vai a un adiacente non visitato, etichetta con 2
3. Continua in profondità finché possibile
4. Quando bloccato, risali fino a trovare un adiacente non etichettato
5. Continua finché tutti sono etichettati

## Esercizio classico tipico d'esame
"Dato il grafo G, applicare la procedura BFS partendo dal nodo X. Indicare i livelli e trovare un cammino dal nodo X al nodo Y."

## Tempo stimato: 1.5 ore
