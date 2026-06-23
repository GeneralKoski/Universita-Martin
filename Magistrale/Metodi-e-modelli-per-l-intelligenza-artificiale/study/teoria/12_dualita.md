# 12 — Dualità

📂 Fonte: `Elly/8_Rilassamenti_e_Dualità/Lezioni 17-18.pdf`

## Obiettivi
Costruire un problema duale che dia stime sul primale; capire dualità debole vs forte.

## Da sapere a memoria
- **Dualità debole**: (P) max c(x) su X e (D) min b(u) su U sono in dualità debole se c(x) ≤ b(u), ∀x ∈ X, ∀u ∈ U
- **Dualità forte**: z* = w*
- **Criterio di ottimalità**: se c(x̂) = b(û), x̂ e û sono ottimi
- **Vantaggio**: ogni soluzione duale dà stima dall'alto su z*

## Costruzione del duale via rilassamento lineare
PI: max c^T x, Ax ≤ b, x ≥ 0, x ∈ ℤⁿ
Rilassamento PL: max c^T x, Ax ≤ b, x ≥ 0
Duale del PL (DPL): min b^T y, A^T y ≥ c, y ≥ 0

**Catena**: z*_PI ≤ z*_PL = w*_PL ≤ w_PL (dualità forte della PL ⟹ dualità debole tra PI e DPL).

## Dualità combinatoria (esempi)
Su grafo non orientato:
- **Accoppiamento (matching)**: archi disgiunti
- **Copertura per nodi**: nodi che coprono ogni arco

**Proposizione**: max accoppiamento e min copertura sono in **dualità debole** (|M| ≤ |R|, dimostrabile direttamente).

**Non sono in dualità forte in generale** (es. triangolo: max M = 1, min R = 2).

Formulazione PI:
- Matching: max e^T x, Ax ≤ e, x ∈ {0,1}ⁿ — è un **set packing**
- Copertura: min e^T y, A^T y ≥ e, y ∈ {0,1}ⁿ — è un **set covering**

I rilassamenti lineari delle due sono **uno il duale dell'altro** (in dualità forte di PL).

## Tempo stimato: 2 ore
