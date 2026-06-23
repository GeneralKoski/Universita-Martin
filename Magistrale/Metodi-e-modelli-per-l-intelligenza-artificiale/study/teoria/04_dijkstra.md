# 04 — Algoritmo di Dijkstra

📂 Fonte: `Elly/4_Cammini_Minimi_Dijkstra/Lezioni 7-8.pdf`

## Obiettivi
Cammino minimo da un nodo a tutti gli altri quando i **pesi sono ≥ 0**, anche con circuiti.

## Da sapere a memoria
- **Ipotesi**: G orientato (anche con circuiti), ℓ_ij ≥ 0
- Etichette λ(i) (lunghezza temporanea) e p(i) (predecessore)
- Insiemi 𝒫 (permanenti) e 𝒯 (temporanei)
- I 3 passi dell'algoritmo: inizializzazione → aggiornamento → scelta del minimo permanente
- Estensione a grafi non orientati: sostituire ogni arco con due archi orientati di pari lunghezza

## Teorema/dimostrazione
**Correttezza (lemma)**: se note u_i per i ∈ 𝒫, e (v,h) realizza il minimo
$$u_v + \ell_{vh} = \min\{u_i + \ell_{ij} : i \in \mathcal{P}, j \notin \mathcal{P}\}$$
allora u_v + ℓ_vh = u_h. **Sapere la dimostrazione**: si scompone qualsiasi cammino alternativo come P_1 ∪ {(i,j)} ∪ P_2, si usa ℓ_ij ≥ 0 per L(P_2) ≥ 0 e si confronta. **Senza ℓ_ij ≥ 0 il lemma cade** (Dijkstra non funziona con pesi negativi).

## Bellman vs Dijkstra
| | Bellman | Dijkstra |
|---|---|---|
| Pesi negativi | OK (no circuiti neg.) | NO |
| Circuiti | NO | SI |
| Output | da s a tutti | da s a tutti (o a un t specifico) |

## Tempo stimato: 1.5 ore
