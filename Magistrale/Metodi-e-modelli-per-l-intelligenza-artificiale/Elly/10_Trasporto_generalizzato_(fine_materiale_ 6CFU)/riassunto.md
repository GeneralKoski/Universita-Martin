# 10 — Trasporto generalizzato e problemi "facili" (Lezioni 21-22)

> **Fine del programma 6 CFU** (per Scienze Informatiche).

## Contenuto cartella
- `Lezioni 21-22.pdf` — flussi di costo minimo, problema del trasporto, assegnazione, cammino minimo, abbinamento

## Argomenti

### Problema di flusso di costo minimo
Dato G = (V, A) orientato con:
- **capacità** h_ij ≥ 0 su ogni arco
- **costo unitario** c_ij su ogni arco
- nodo **sorgente** s, nodo **pozzo** t, **valore del flusso** f assegnato

**Flusso**: x_ij ∈ [0, h_ij] con vincolo di **bilancio** ai nodi intermedi (uscente = entrante).

**Modello PL** (semplificato):
```
min Σ c_ij x_ij
Σ x_si − Σ x_js = f          (uscente da s)
Σ x_ki − Σ x_jk = 0  ∀k≠s,t  (bilancio intermedi)
Σ x_ti − Σ x_jt = -f         (entrante in t)
0 ≤ x_ij ≤ h_ij
```

### Problema di Trasporto Generalizzato
Generalizza: ogni nodo k può avere bilancio b_k assegnato:
- b_k > 0: **sorgente** (offerta)
- b_k < 0: **pozzo** (domanda)
- b_k = 0: **nodo di transito**

Si assume rete **bilanciata** (Σ b_k = 0).

**Formulazione**:
```
min c^T x
A x = b      (equazioni di bilancio, A = matrice incidenza nodi-archi)
0 ≤ x ≤ h
x ≥ 0
```

In forma canonica:
$$\min c^T x \quad \text{s.t.}\quad \begin{bmatrix} A \\ -A \\ I_m \end{bmatrix} x \leq \begin{bmatrix} b \\ -b \\ h \end{bmatrix},\quad x \geq 0$$

### Teorema 1.2 — Interezza delle SBA
Se capacità h e domande/offerte b sono **intere**, allora ogni SBA (e in particolare ogni SBA ottima) del problema di trasporto generalizzato ha **componenti intere** ⟹ flussi interi sugli archi.

**Idea**: la matrice di incidenza nodi-archi di un grafo orientato è TU ⟹ applicabile il Teorema di Interezza in forma canonica.

## Problemi riconducibili a flusso di costo minimo

Tutti gerarchicamente "facili" perché risolvibili via rilassamento lineare + TU.

### 1. Massimo Flusso
Si aggiunge un arco fittizio (t, s) con h_ts = ∞ e c_ts = −1, costi 0 sugli altri archi, tutti nodi di transito. Risolvendo il flusso di costo minimo si ottiene il flusso massimo.

### 2. Problema del Trasporto (modello di Hitchcock)
m origini, n destinazioni, offerte a_i e domande b_j (Σ a_i = Σ b_j), costo c_ij:
```
min Σ c_ij x_ij
Σ_j x_ij = a_i  ∀i
Σ_i x_ij = b_j  ∀j
x_ij ≥ 0
```
Caso speciale di flusso di costo minimo su grafo **bipartito completo** (origini → destinazioni), senza nodi di transito, capacità illimitate.

### 3. Problema di Assegnazione
n persone, n lavori, costo c_ij, x_ij ∈ {0,1}:
```
min Σ c_ij x_ij
Σ_j x_ij = 1 ∀i
Σ_i x_ij = 1 ∀j
```
Caso speciale del trasporto con a_i = b_j = 1. **Grazie alla TU**, il rilassamento lineare (x_ij ≥ 0) ha SBA ottime binarie ⟹ si risolve col simplesso.

### 4. Cammino Minimo
Da s = 1 a t = n, con x_ij ∈ {0,1} se l'arco fa parte del cammino:
```
min Σ c_ij x_ij
bilancio: b_1 = 1, b_n = −1, b_k = 0 ∀k ≠ 1,n
```
Anche qui: rilassamento lineare ha SBA ottime intere (TU).

### 5. Abbinamento (matching) bipartito di cardinalità massima
Su G non orientato bipartito:
```
max Σ x_ij
Σ_{j: (i,j)∈A} x_ij ≤ 1  ∀i ∈ V
x_ij ∈ {0,1}
```
Su grafo **bipartito** la matrice di incidenza è TU ⟹ il rilassamento lineare ha SBA ottime binarie.
Su grafo non bipartito **non è TU in generale** ⟹ il Teorema di Interezza non si applica direttamente.

**Riduzione a flusso massimo** (Lemma 2.3): si costruisce R(G) aggiungendo sorgente s con archi verso V_1 e pozzo t da V_2, capacità 1 su tutti gli archi. La cardinalità max del matching = valore max del flusso s→t.

### 6. Abbinamento bipartito di peso massimo
Con pesi w_ij > 0:
```
max Σ w_ij x_ij
Σ_{j: (i,j)∈A} x_ij ≤ 1  ∀i
x_ij ∈ {0,1}
```
Su grafo bipartito, TU ⟹ rilassamento ha SBA ottime binarie.
**Equivalente all'assegnazione** (con w_ij = −c_ij): assegnare n persone a n lavori = abbinamento bipartito pesato sul grafo bipartito completo.
