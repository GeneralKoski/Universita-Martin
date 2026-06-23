# 1 — Elementi di Teoria dei Grafi (Lezioni 1-2)

## Contenuto cartella
- `Lezioni 1-2.pdf` — teoria
- `Lezioni 1-2bis.pdf` — figure di esempio (grafi orientati/non orientati, cammini, cicli, alberi, alberi ricoprenti)

## Argomenti

### Definizioni base
- **Grafo** G = (V, A): V insieme finito non vuoto di nodi, A insieme di archi.
- **Anello/cappio**: arco con estremi coincidenti. **Archi paralleli**: stessi estremi. **Grafo semplice**: senza anelli né paralleli.
- **Grafo orientato (digrafo)**: archi come coppie ordinate (u,v); u predecessore, v successore. **Misto**: archi orientati + non orientati. **Completo**: tutte le coppie possibili. **Bipartito**: V = S∪T con archi solo tra S e T.
- **Grado** di un nodo = nº archi incidenti. In digrafo: grado **uscente** ed **entrante**.
- Nodi **adiacenti** se connessi da un arco. Nodo **isolato** se grado 0.

### Sottografi
- **Grafo parziale** G[B] = (V, B), B ⊆ A: si rimuovono archi.
- **Sottografo indotto** da R ⊆ V: si rimuovono nodi V\R e gli archi incidenti.

### Cammini e cicli
- **Cammino**: sequenza di archi consecutivi; due nodi (estremi) hanno grado 1, gli altri grado 2 se semplice.
- **Ciclo**: cammino con estremi coincidenti.
- **Grafo connesso**: per ogni coppia di nodi esiste un cammino tra essi.
- In digrafi: distinzione tra cammini/cicli **orientati** (archi nello stesso verso, circuiti) e **non orientati**.
- **Ciclo euleriano**: passa una sola volta per ogni arco.
  - **Teorema di Eulero (1736)**: G ha ciclo euleriano ⟺ G connesso e ogni nodo di grado pari.
- **Ciclo hamiltoniano**: passa una sola volta per ogni nodo.

### Alberi
Un grafo connesso e senza cicli. **Foglie** = nodi di grado 1.
**Caratterizzazioni equivalenti** di un albero G = (V,A):
1. G è albero;
2. G connesso e |A| = |V|−1;
3. G privo di cicli e |A| = |V|−1;
4. ogni coppia di nodi è connessa da un unico cammino;
5. G privo di cicli e aggiungendo un arco fra due non adiacenti si forma esattamente un ciclo.

**Albero ricoprente** T = (V, A_T) con A_T ⊆ A: albero che copre tutti i nodi di G.

### Grafi orientati senza circuiti
- **Numerabile progressivamente**: i nodi possono essere numerati in modo che (i,j)∈A ⟹ i<j.
- **Teorema**: G orientato è numerabile progressivamente ⟺ è senza circuiti.
- **Algoritmo di Fulkerson**: trovare un nodo entrata (grado entrante 0) → numerarlo 1 → cancellare archi uscenti → ripetere. Applicazioni: equazioni di Bellman, PERT, CPM.
