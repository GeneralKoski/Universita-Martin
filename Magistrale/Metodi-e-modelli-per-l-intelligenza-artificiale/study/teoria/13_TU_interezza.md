# 13 - Matrici TU e Teorema di Interezza

📂 Fonte: `Elly/9_Matrici_TU_e_Teorema_di_Interezza/Lezioni 19-20.pdf`

## Obiettivi
Capire quando un PI è "facile": si può risolvere col solo rilassamento lineare.

## Da sapere a memoria
- **Definizione di TU**: ogni sottomatrice quadrata ha det ∈ {−1, 0, 1}; quindi a_ij ∈ {0, ±1}
- **Condizione sufficiente operativa** per riconoscere TU (3 punti: coefficienti, max 2 non nulli per colonna, partizione delle righe)
- 8 equivalenze: A TU ⟺ Aᵀ TU ⟺ −A TU ⟺ [A,I] TU ⟺ ...

## Matrici di incidenza nodi-archi
| Grafo | TU? |
|---|---|
| Orientato | **Sempre TU** |
| Non orientato (generico) | Non TU in generale (es. triangolo: det = 2) |
| Non orientato **bipartito** | **TU** |

## Teorema di Interezza (forma canonica) - il più importante
Sia A intera. Sono **equivalenti**:
1. I vertici di P*(A,b) = {x : Ax ≤ b, x ≥ 0} sono interi ∀ b intero
2. max{c^T x : Ax ≤ b, x ≥ 0} ammette SBA ottima intera ∀ b intero
3. A è TU

**Conseguenza pratica**: se la matrice dei vincoli di un PI è TU, si risolve col simplesso sul rilassamento lineare e si ottiene direttamente la soluzione intera.

## Applicazione: dualità forte matching/copertura su grafo bipartito
Su G non orientato:
- Catena di disuguaglianze: z_PI ≤ z*_PI ≤ z*_PL = w*_PL ≤ w*_PI ≤ w_PI
- **Se G bipartito**: A è TU ⟹ tutte le disuguaglianze diventano uguaglianze ⟹ **dualità forte** ⟹ |M_max| = |R_min| (Teorema di König)
- Su grafi non bipartiti vale solo la dualità debole

## Tempo stimato: 2 ore
