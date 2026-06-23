# 3 — Cammini Minimi: Equazioni di Bellman (Lezioni 5-6)

## Contenuto cartella
- `Lezioni 5-6.pdf` — teoria delle equazioni di Bellman
- `ese_2_2026.pdf`, `ese_3_2026.pdf` — esercizi

## Problema
Dato G = (V, A) orientato, una funzione lunghezza ℓ: A → ℝ e un nodo s ∈ V. Determinare per ogni j ∈ V un cammino di lunghezza minima da s a j.

**Notazione**: u_j = lunghezza del cammino minimo da s a j.

**Ipotesi generali**:
1. ∀j ≠ s, esiste almeno un cammino s → j;
2. Non ci sono circuiti di lunghezza negativa.

## Principio di Ottimalità di Bellman
Sia P un cammino minimo da s a j, e k un nodo lungo P. Allora i sottocammini P(s,k) e P(k,j) sono entrambi minimi.

**Conseguenze** (sulle lunghezze u_j):
1. u_s = 0
2. (i,j) ∈ A ⟹ u_j ≤ u_i + ℓ_ij
3. ∃ k predecessore di j tale che u_j = u_k + ℓ_kj

## Equazioni di Bellman
$$\begin{cases} x_s = 0 \\ x_j = \min\{x_i + \ell_{ij} \mid (i,j) \in A\}, \quad \forall j \neq s \end{cases}$$

Le u_j sono soluzione, **ma in generale non l'unica** (esempio nel PDF: infinite soluzioni se ci sono circuiti di lunghezza zero).

## Teorema (unicità)
Se G non contiene circuiti di lunghezza ≤ 0, allora le equazioni di Bellman hanno **un'unica soluzione**, data da x_j = u_j.

## Soluzione su grafi senza circuiti
Se G è senza circuiti, si numerano progressivamente i nodi (algoritmo di Fulkerson, vedi Lez. 1-2). Allora:
$$u_1 = 0, \qquad u_j = \min_{i<j}\{u_i + \ell_{ij} \mid (i,j) \in A\}, \quad j = 2, \dots, n$$

Risolvibile **per sostituzione** in cascata: u_2 dipende solo da u_1, u_3 da u_1, u_2, ecc.

## Esempio risolto
Grafo a 8 nodi numerati progressivamente. Calcolando in tabella le u_j e i predecessori, si ottiene un cammino minimo 1 → 2 → 5 → 8 di lunghezza u_8 = 14.
