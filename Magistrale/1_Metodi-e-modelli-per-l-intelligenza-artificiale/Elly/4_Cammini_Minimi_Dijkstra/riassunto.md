# 4 - Cammini Minimi: Algoritmo di Dijkstra (Lezioni 7-8)

## Contenuto cartella
- `Lezioni 7-8.pdf` - algoritmo di Dijkstra (teoria + esempio)
- `ese_3.1_2026.pdf` - esercizio
- `Sol-piano-rinn-ott.pdf` - soluzione esercizio "piano di rinnovo ottimale"

## Ipotesi
- G = (V, A) orientato
- Possono esistere circuiti
- ℓ_ij ≥ 0 per ogni arco (esclude circuiti negativi)

A differenza di Bellman, **funziona anche con circuiti** purché non negativi.

## Idea
Ad ogni nodo i ∈ V sono associate due etichette:
- **λ(i)**: lunghezza del miglior cammino temporaneo da s a i (λ(i) ≥ u_i)
- **p(i)**: predecessore di i in tale cammino

Suddivisione dei nodi:
- 𝒫 = nodi **permanenti**: λ(i) = u_i (definitivo)
- 𝒯 = nodi **temporanei**: λ(i) ≥ u_i (ancora aggiornabile)

Inizialmente solo s ∈ 𝒫. Ad ogni passo un nodo temporaneo diventa permanente, in **ordine crescente** di distanza da s.

## Algoritmo
1. **Inizializzazione**: λ(1) = 0, λ(i) = ∞ ∀i ≠ 1; p(i) = 0 ∀i; r := 1; 𝒫 := {1}, 𝒯 := V\{1}.
2. **Aggiornamento etichette temporanee**: per ogni j ∈ 𝒯 con (r, j) ∈ A, se λ(j) > λ(r) + ℓ_rj, allora λ(j) := λ(r) + ℓ_rj e p(j) := r.
3. **Scelta del nodo permanente**: h ∈ 𝒯 con λ(h) = min{λ(j) : j ∈ 𝒯}; h diventa permanente, r := h.
   - Se h = t, STOP; ricostruire il cammino con back-tracking sui p(·).
   - Altrimenti, torna al passo 2.

## Correttezza (Lemma)
Se per ogni i ∈ 𝒫 si conosce u_i, e (v, h) realizza il minimo
$$u_v + \ell_{vh} = \min\{u_i + \ell_{ij} : (i,j) \in A, i \in \mathcal{P}, j \notin \mathcal{P}\},$$
allora **u_v + ℓ_vh è la lunghezza di un cammino minimo da 1 a h**. La dimostrazione usa l'ipotesi ℓ_ij ≥ 0 (qualsiasi cammino alternativo non può accorciare).

## Osservazioni
- Si può estendere a cammini minimi da s **a tutti i nodi** (basta non fermarsi finché 𝒯 ≠ ∅).
- Funziona anche su grafi non orientati o misti, sostituendo ogni arco non orientato con due archi orientati di pari lunghezza.

## Esempio risolto
Grafo a 6 nodi: u₁=0, u₂=3, u₃=7, u₄=18, u₅=13, u₆=22. Cammino minimo 1 → 2 → 3 → 5 → 4 → 6.
