# 2 - Procedure BFS e DFS (Lezioni 3-4)

## Contenuto cartella
- `Lezioni 3-4.pdf` - teoria BFS e DFS
- `Lezioni 3-4bis.pdf` - esempi e figure
- `ese_1_2026.pdf` - esercizio

## BFS - Breadth First Search (esplorazione a ventaglio)
Privilegia la **larghezza**. Partendo da un nodo iniziale s:
- si elencano tra parentesi tutti i nodi adiacenti, poi si passa al primo della parentesi e si elencano i suoi adiacenti non ancora visitati, e così via.
- Si etichettano i nodi con interi crescenti 0, 1, 2, … = distanza geometrica (numero minimo di archi) da s.
- I nodi vengono raggruppati in **livelli L_k** = nodi a distanza k da s.

### Lemma fondamentale
> w ∈ L_k ⟺ d(s, w) = k

Dimostrazione per induzione su k. Conseguenza: BFS calcola **cammini minimi in numero di archi** dal nodo s a tutti gli altri.

### Problema del Labirinto
Trovare un cammino tra due nodi i, j: si esegue BFS da i, poi back-tracking dai livelli (dal nodo finale, si risale ai livelli inferiori scegliendo nodi adiacenti).

### Pseudocodice BFS
1. l(1) := 0, i := 0
2. U := {nodi non etichettati adiacenti a un nodo etichettato i}
3. Se U ≠ ∅, etichetta gli elementi di U con i+1
4. i := i+1
5. Torna al passo 2

**Applicazioni**: information retrieval (database relazionali), problemi di intelligenza artificiale (puzzle, ricerca su grafi di stato).

## DFS - Depth First Search (esplorazione a scandaglio)
Privilegia la **profondità**: dal nodo iniziale si scende su un adiacente, poi su un adiacente di questo, ecc., fino a non poter più procedere; si fa **back-tracking** al nodo precedente per cercare altri rami non visitati. I nodi sono etichettati nell'ordine di visita.

Esempio nel PDF: V'={a,b,c,d,e,f,g}, etichette finali a=1, b=2, c=3, e=4, f=5, g=6, d=7.
