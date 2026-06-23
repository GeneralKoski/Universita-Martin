# Lezione 2 — Funzioni in più variabili

Continuazione dei fondamenti matematici. Si tratta di funzioni `f: ℝᴺ → ℝ` (e `F: ℝᴺ → ℝᴹ`), continuità, derivabilità, differenziabilità, gradiente, teorema di Schwartz.

---

## 1. Similarità del coseno (cosine similarity)

### Definizione
Per x, y ∈ ℝᴺ, x, y ≠ 0, si definisce:

```
cos θ = (x · y) / (‖x‖ · ‖y‖)
```

dove θ è l'angolo tra i vettori x e y. Valori in [-1, 1]:
- cos θ = 1 → vettori paralleli concordi
- cos θ = 0 → ortogonali (x ⊥ y)
- cos θ = -1 → paralleli discordi

### Giustificazione (legge del coseno, caso N=2)
Triangolo con lati `‖x‖`, `‖y‖`, `‖y - x‖` e angolo θ tra x e y:

```
‖y - x‖² = ‖x‖² + ‖y‖² - 2·‖x‖·‖y‖·cos θ
```

D'altra parte, sviluppando con il prodotto scalare:
`‖y - x‖² = ‖x‖² + ‖y‖² - 2(x·y)`.

Confrontando: `x·y = ‖x‖·‖y‖·cos θ` ⇒ formula del coseno.

---

## 2. Funzioni in più variabili — definizioni

- **Scalare**: `f: ℝᴺ → ℝ`, `(x₁,...,xₙ) ↦ y ∈ ℝ`. Per ogni vettore x ∈ ℝᴺ esiste un unico y ∈ ℝ.
- **Vettoriale**: `F: ℝᴺ → ℝᴹ`, `F = (f₁,...,fₘ)ᵀ`, ogni `fᵢ: ℝᴺ → ℝ`.

### Esempio (N=1, M=2): coordinate polari
Circonferenza di centro 0 e raggio ρ > 0:
`S(0, ρ) = { x ∈ ℝ² : ‖x‖ = ρ }`.
Parametrizzazione `F: [0, 2π] → S(0,ρ)`:
```
F(θ) = (ρ cos θ, ρ sin θ)
```

### Esempio (N=2, M=3): coordinate sferiche
Sfera di centro 0 e raggio ρ in ℝ³: `S(0, ρ) = { x ∈ ℝ³ : ‖x‖ = ρ }`.
`F: [0, 2π] × [0, π] → S(0, ρ)`:
```
F(θ, φ) = (ρ cos θ sin φ, ρ sin θ sin φ, ρ cos φ)
```

### Visualizzazione (lab)
- `linspace(a, b, n)` → punti X del dominio (1D).
- `meshgrid(X, Y)` → griglia di punti del dominio 2D, su cui calcolare `f(X, Y) = Z`.

---

## 3. Continuità (ε–δ)

### Definizione
`f: ℝᴺ → ℝ` si dice **continua** in ℝᴺ, scritto `f ∈ C⁰(ℝᴺ)`, se:

```
∀x ∈ ℝᴺ,  ∀ε > 0,  ∃δ > 0  :  ∀y ∈ ℝᴺ,  ‖x - y‖ < δ  ⇒  |f(x) - f(y)| < ε
```

cioè: `d(x,y) < δ ⇒ d(f(x), f(y)) < ε`.

- **Caso N=1**: la classica definizione di Cauchy con intorni di raggio δ in dominio e ε in codominio.
- **Caso N=2**: l'intorno del punto x = (x₁, y₁) è un *disco* di raggio δ; la differenza |f(x) - f(y)| deve stare in un intervallo di ampiezza 2ε.

### Continuità separata (per N=2)
`f: ℝ² → ℝ` si dice **continua separatamente in x** se, fissato y, la funzione `fᵧ(·) = f(·, y): ℝ → ℝ` è continua. Analogamente continua separatamente in y se, fissato x, `fₓ(·) = f(x, ·)` è continua.

### Osservazione fondamentale (controesempio classico)
**Continuità separata ⇏ continuità globale.**

Esempio:
```
f(x,y) = { xy / (x² + y²)   se (x,y) ≠ (0,0)
         { 0                 se (x,y) = (0,0)
```

- Lungo l'asse x (y=0): f(x,0) = 0 ⇒ continua in 0 nella variabile x.
- Lungo l'asse y (x=0): f(0,y) = 0 ⇒ continua in 0 nella variabile y.
- Lungo la retta y = x: `f(x,x) = x²/(2x²) = 1/2` per ogni x ≠ 0.

Quindi avvicinandosi a (0,0) lungo la diagonale il limite è 1/2 ≠ 0 = f(0,0): **f non è continua in (0,0)** pur essendo separatamente continua.

---

## 4. Direzioni e rette

### Direzione
Una **direzione** è un vettore `v ∈ ℝᴺ` con `‖v‖ = 1`. Ogni vettore non nullo x ∈ ℝᴺ individua la direzione `v = x / ‖x‖`.

I vettori della base canonica `eᵢ` sono direzioni.

### Retta passante per x₀ con direzione v
`R(x₀, v) = { x ∈ ℝᴺ : x = x₀ + t·v,  t ∈ ℝ }`.

---

## 5. Derivata direzionale

### Definizione
Sia `f: ℝᴺ → ℝ`, x₀ ∈ ℝᴺ, v direzione (‖v‖=1). f si dice **derivabile in x₀ lungo v** se esiste finito il limite del rapporto incrementale ristretto a R(x₀, v):

```
∂f/∂v (x₀) := lim_{t→0}  [f(x₀ + tv) - f(x₀)] / t
```

### Derivata parziale
Caso particolare con v = eᵢ (i-esimo vettore della base canonica):

```
∂f/∂xᵢ (x₀) := lim_{t→0}  [f(x₁,...,xᵢ+t,...,xₙ) - f(x₀)] / t
```

### Differenza fondamentale fra N=1 e N>1
- **N=1**: l'esistenza di f'(x₀) implica ⇒ continuità in x₀ ⇒ esistenza retta tangente al grafico in x₀.
- **N>1**: l'esistenza di tutte le `∂f/∂xᵢ(x₀)` da sola **NON garantisce**:
  - continuità in x₀,
  - esistenza del piano tangente al grafico (sottospazio di dim N-1+1 in ℝᴺ⁺¹).

### Esempio di calcolo (N=2)
`f(x,y) = x² + y·eˣ`.
- `∂f/∂x = lim_{t→0} [(x+t)² + y·e^(x+t) - x² - y·eˣ]/t = lim [t² + 2xt + y·eˣ(eᵗ-1)]/t = 2x + y·eˣ` (usando lim (eᵗ-1)/t = 1).
- `∂f/∂y = lim_{t→0} [x² + (y+t)eˣ - x² - y·eˣ]/t = lim t·eˣ/t = eˣ`.

Quindi `(∂f/∂x, ∂f/∂y) = (2x + y·eˣ, eˣ)`.

### Derivata direzionale generica via parziali (caso differenziabile)
Per direzione v = (v₁, v₂)/‖(v₁,v₂)‖ in ℝ²:
```
∂f/∂v (x,y) = v₁ · ∂f/∂x + v₂ · ∂f/∂y
```
(verificato sia per v=(1,2)/√5 che per v=(3,4)/5 nell'esempio).

---

## 6. Gradiente e differenziabilità

### Gradiente
Se f ammette tutte le derivate parziali in x₀, si definisce il **gradiente** di f in x₀ come il vettore:

```
∇f(x₀) = ( ∂f/∂x₁(x₀), ∂f/∂x₂(x₀), ..., ∂f/∂xₙ(x₀) ) ∈ ℝᴺ
```

Si nota: `∇f(x₀) · v = Σᵢ vᵢ · ∂f/∂xᵢ(x₀)`.

### Differenziabilità
`f: ℝᴺ → ℝ` si dice **differenziabile in x₀** se esiste l'applicazione lineare `df_{x₀}: ℝᴺ → ℝ` tale che:

```
∀v ∈ ℝᴺ:   df_{x₀}(v) = Σᵢ vᵢ · ∂f/∂xᵢ(x₀) = v · ∇f(x₀) = ∂f/∂v (x₀)
```

cioè la derivata direzionale lungo *ogni* v si ottiene come prodotto scalare con il gradiente.

**Notazione**: `df_{x₀} = Σᵢ ∂f/∂xᵢ(x₀) · dxᵢ`.

### Proprietà
- f differenziabile in x₀ ⇒ f **continua** in x₀.
- f differenziabile in x₀ ⇒ esiste il **piano tangente** al grafico di f in x₀:
  ```
  φ(x) = f(x₀) + df_{x₀}(x - x₀) = f(x₀) + ∇f(x₀)·(x - x₀)
  ```
- Se `∇f(x₀) · v = 0` per qualche v, allora `∇f(x₀) ⊥ v` e `df_{x₀}(v) = 0` (v giace nel piano tangente).

### Direzione di massima crescita
Se f è differenziabile in x₀, allora `∇f(x₀)` indica la **direzione di massima crescita** di f in x₀. (Conseguenza di `∂f/∂v = ∇f·v = ‖∇f‖·‖v‖·cos θ`, massimizzata per v parallelo a ∇f.)

### Condizione necessaria di estremo (punti stazionari)
**Teorema**: Se f è differenziabile in x₀ e x₀ è un punto di **massimo** o **minimo** locale per f, allora `df_{x₀} = 0` in tutte le direzioni, ossia:

```
∇f(x₀) = 0
```

I punti che annullano il gradiente si dicono **punti stazionari** (o critici). È condizione *necessaria* ma non sufficiente (esempio: punti di sella).

### Teorema (sufficiente per la differenziabilità)
Sia `f: ℝᴺ → ℝ` con derivate parziali esistenti in B(x₀, r), r > 0. Se tali derivate parziali sono **continue** in x₀, allora f è **differenziabile** in x₀. (Si dice f ∈ C¹.)

---

## 7. Derivate seconde e Teorema di Schwartz

### Derivate seconde
Per `f: ℝ² → ℝ` ci sono 4 derivate seconde:
- `∂²f/∂x²` (xx)
- `∂²f/∂x∂y` (yx, prima rispetto a y, poi rispetto a x — *mista*)
- `∂²f/∂y∂x` (xy, prima rispetto a x, poi rispetto a y — *mista*)
- `∂²f/∂y²` (yy)

### Esempio
`f(x,y) = x² + y·eˣ`, `∂f/∂x = 2x + y·eˣ`, `∂f/∂y = eˣ`.
- `∂²f/∂x² = 2 + y·eˣ`
- `∂²f/∂y² = 0`
- `∂²f/∂x∂y = ∂(eˣ)/∂x = eˣ`
- `∂²f/∂y∂x = ∂(2x + y·eˣ)/∂y = eˣ`

Le miste coincidono: `∂²f/∂x∂y = ∂²f/∂y∂x = eˣ`. Non è coincidenza.

### Teorema di Schwartz
Sia `f: A ⊆ ℝ² → ℝ` con A aperto, `(x₀, y₀) ∈ A`. Se le **derivate miste** `∂²f/∂x∂y` e `∂²f/∂y∂x` esistono in `B((x₀,y₀), r)` e sono **continue** in (x₀, y₀), allora:

```
∂²f/∂x∂y (x₀, y₀)  =  ∂²f/∂y∂x (x₀, y₀)
```

### Sketch di dimostrazione
Si considera la funzione ausiliaria:
```
Δ(h, k) = f(x₀+h, y₀+k) - f(x₀+h, y₀) - f(x₀, y₀+k) + f(x₀, y₀)
```
Definendo `g(x) = f(x, y₀+k) - f(x, y₀)`, si ha Δ = g(x₀+h) - g(x₀). Per il teorema di Lagrange (in x), Δ = h·g'(ξ) per qualche ξ ∈ (x₀, x₀+h), e applicando di nuovo Lagrange (in y) a g'(ξ) = ∂f/∂x(ξ, y₀+k) - ∂f/∂x(ξ, y₀), si ottiene Δ = h·k·∂²f/∂y∂x(ξ, η). Procedendo simmetricamente (definendo prima h(y) = f(x₀+h, y) - f(x₀, y)) si ricava Δ = h·k·∂²f/∂x∂y(ξ', η'). Dividendo per h·k e mandando h, k → 0, la **continuità** delle derivate miste fa convergere ambedue le espressioni allo stesso valore in (x₀, y₀). □

### Generalizzazione
Se f ∈ Cᵏ(A) (tutte le derivate fino all'ordine k continue), allora le derivate miste di ordine ≤ k non dipendono dall'ordine di derivazione. Per k=2 questo è il classico teorema di Schwartz.

---

## 8. Schema sintetico dei legami

```
∂f/∂xᵢ esistono tutte  ⇏  f continua  (controesempio xy/(x²+y²))
∂f/∂xᵢ esistono e sono continue  ⇒  f differenziabile  ⇒  f continua, ∃ piano tg
f differenziabile  ⇒  ∂f/∂v = ∇f · v  per ogni direzione v
x₀ massimo/minimo locale + f differenziabile  ⇒  ∇f(x₀) = 0
derivate miste continue  ⇒  Schwartz: ∂²f/∂x∂y = ∂²f/∂y∂x
```
