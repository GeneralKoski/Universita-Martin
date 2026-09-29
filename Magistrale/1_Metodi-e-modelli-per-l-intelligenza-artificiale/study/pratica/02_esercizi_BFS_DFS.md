# 02 - Esercizi: BFS e DFS

## Esercizi disponibili

| Fonte | Contenuto |
|---|---|
| `Elly/2_Procedure_BFS_e_DFS/ese_1_2026.pdf` | foglio 1: (1) recipienti da 3 e 5 litri, raccogliere 4 litri nel più grande; (2) barcaiolo/lupo/capra/cavolo. Entrambi da ricondurre a esplorazione su un **grafo degli stati** |
| `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` p. 2 | **soluzione del foglio 1** (su Elly non c'è): per i recipienti lo stato è la coppia `(x,y)` dei contenuti e la sequenza minima si legge dai livelli BFS - 6 mosse; per il barcaiolo i 10 stati ammissibili sono disegnati come grafo bipartito sx/dx |
| `Appunti_colleghi/Zip_appunti/esercizi MMD.pdf` p. 3 | esempio di **DFS** con notazione a parentesi e albero di visita |
| `AAA METODI E MODELLI PER LE DECISIONI.pdf` | appunti dei gestionali, prime lezioni (approfondimento) |

Il punto dell'esercizio non è l'algoritmo ma la **modellazione**: capire che gli stati sono i nodi e le mosse ammissibili sono gli archi. Una volta costruito il grafo, la BFS è meccanica.

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
