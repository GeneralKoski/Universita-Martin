# Lezione 1 — Introduzione all'IA e Fondamenti Matematici

Corso: Fondamenti dell'Intelligenza Artificiale — Prof.ssa Eleonora Iotti — UniPR — A.A. 2025/2026.

---

## 1. Informazioni sul corso ed esame

### Modalità d'esame
- **Progetto individuale**: report di 1 pagina in LaTeX (template fornito) + presentazione finale di max 10 minuti. Fino a **3 punti**.
- **Prova scritta**: 3 domande aperte su tutto il programma. Fino a **30 punti**.
- Voto totale: scritto (max 30) + progetto (max 3) = max 33 (lode).

### Programma teorico
1. Funzioni in più variabili
2. Reti neurali (SLP, MLP)
3. Visione artificiale
4. Integrali in più variabili e convoluzione
5. Deep Learning (CNN, RNN)
6. Generazione (LM, GAN)
7. Equazioni differenziali ordinarie
8. Sistemi ad agenti

### Testi di riferimento
- Russell & Norvig, *Intelligenza artificiale: un approccio moderno* (Pearson)
- Nielsen, *Neural Networks and Deep Learning* (online)
- Zhang, Lipton, Li, Smola, *Dive into Deep Learning* (d2l.ai)
- Goodfellow, Bengio, Courville, *Deep Learning* (MIT Press)

---

## 2. Insiemi numerici

| Insieme | Descrizione | Costruzione |
|---|---|---|
| ℕ | Naturali | Assiomi di Peano |
| ℤ | Interi | Coppie (a,b)∈ℕ² con (a,b)R(c,d) ⇔ a+d = b+c |
| ℚ | Razionali | Coppie (a,b)∈ℤ² con (a,b)R(c,d) ⇔ a·d = b·c |
| ℝ | Reali | |ℕ| < |P(ℕ)| = |ℝ| (cardinalità del continuo) |
| ℂ | Complessi | i := √(-1) (unità immaginaria) |

### Assiomi di Peano (costruzione di ℕ)
1. 0 ∈ ℕ
2. Esiste una funzione successore S: ℕ → ℕ
3. ∀n ∈ ℕ: S(n) ≠ 0
4. S è iniettiva: S(n) = S(m) ⇒ n = m
5. **Principio di induzione**: se P(0) e P(n) ⇒ P(S(n)), allora P(n) ∀n ∈ ℕ.

### Cardinalità: |ℕ| < |ℝ|
- |ℕ| = ℵ₀ (numerabile).
- ℝ è in biiezione con P(ℕ); per il **teorema di Cantor** |X| < |P(X)|, quindi |ℕ| < |P(ℕ)| = |ℝ|.
- Conseguenza: ℝ è **non numerabile**.

---

## 3. Spazi metrici

### Definizione
Sia X un insieme. Una funzione `d: X² → ℝ` è una **metrica** (o distanza) se soddisfa i tre assiomi:
1. **Positività**: ∀x,y ∈ X, d(x,y) ≥ 0 e d(x,x) = 0 (separazione: d(x,y)=0 ⇔ x=y)
2. **Simmetria**: ∀x,y ∈ X, d(x,y) = d(y,x)
3. **Disuguaglianza triangolare**: ∀x,y,z ∈ X, d(x,y) ≤ d(x,z) + d(z,y)

La coppia (X, d) si dice **spazio metrico**.

### Esempio: distanza euclidea su ℝ
`d: ℝ² → ℝ`, `d(x,y) = |x-y|`. Verificare i 3 assiomi è esercizio standard.

### Palla aperta e chiusa in ℝ
Siano x₀ ∈ ℝ, r > 0:
- **Palla aperta** (intorno sferico): `B(x₀, r) = { x ∈ ℝ : |x - x₀| < r } = (x₀-r, x₀+r)`
- **Palla chiusa**: `B̄(x₀, r) = { x ∈ ℝ : |x - x₀| ≤ r } = [x₀-r, x₀+r]`

---

## 4. Lo spazio ℝᴺ

Sia N ∈ ℕ, N > 0. `ℝᴺ = ℝ × ℝ × ... × ℝ` (N volte). Elementi: `x = (x₁,...,xₙ)`, vettori colonna N×1.

### Vettori notevoli
- Vettore nullo: `0 = (0,0,...,0)`
- Vettore uno: `1 = (1,1,...,1)`

### Operazioni (struttura di spazio vettoriale su ℝ)
- Somma: `x + y = (x₁+y₁, ..., xₙ+yₙ)`
- Prodotto per scalare: `λ·x = (λx₁, ..., λxₙ)`, λ ∈ ℝ

### Assiomi spazio vettoriale
1. + e · associative e commutative
2. ∃ 0 ∈ ℝᴺ tale che x + 0 = x
3. 1·x = x; 0·x = 0
4. (λ+μ)·x = λ·x + μ·x; λ·(x+y) = λx + λy (linearità/distributività)
5. λ·(μ·x) = (λ·μ)·x

### Combinazione lineare
Dati x, y ∈ ℝᴺ, λ, μ ∈ ℝ: `z = λx + μy = (λxᵢ + μyᵢ)ᵢ₌₁..ₙ ∈ ℝᴺ`.

### Base canonica di ℝᴺ
- e₁ = (1,0,...,0)
- e₂ = (0,1,0,...,0)
- ...
- eₙ = (0,...,0,1)

Ogni `x = (x₁,...,xₙ) = Σᵢ xᵢ·eᵢ`.

---

## 5. Norma, distanza e prodotto scalare in ℝᴺ

### Norma euclidea
`‖x‖ = √(Σᵢ₌₁ᴺ xᵢ²)`

### Distanza euclidea
`d(x,y) = ‖x - y‖ = √(Σᵢ (xᵢ - yᵢ)²)`

⇒ (ℝᴺ, d) è uno spazio metrico.

### Palla in ℝᴺ
`B(x₀, r) = { x ∈ ℝᴺ : ‖x - x₀‖ < r }` (aperta, < ; chiusa, ≤).

### Prodotto scalare (dot product / prodotto interno)
Dati x, y ∈ ℝᴺ:
`x·y = ⟨x,y⟩ = Σᵢ₌₁ᴺ xᵢ·yᵢ ∈ ℝ`

### Proprietà fondamentali
- `x·x = Σᵢ xᵢ² = ‖x‖²`
- **Ortogonalità**: `x·y = 0 ⇔ x ⊥ y`
- **Identità del quadrato della somma**:
  `‖x+y‖² = ‖x‖² + ‖y‖² + 2(x·y)`

  *Dimostrazione*: ‖x+y‖² = (x+y)·(x+y) = x·x + 2(x·y) + y·y.
- **Identità del parallelogramma**:
  `‖x+y‖² + ‖x-y‖² = 2(‖x‖² + ‖y‖²)`

  *Dimostrazione*: sviluppare ambedue i termini con la formula precedente; i termini misti 2(x·y) e -2(x·y) si cancellano.
- **Disuguaglianza di Cauchy-Schwarz**: `|x·y| ≤ ‖x‖·‖y‖`, con uguaglianza ⇔ x, y linearmente dipendenti.

---

## 6. Funzioni in più variabili (introduzione)

### Funzione vettoriale
`F: ℝᴺ → ℝᴹ`, con N, M > 0. Si scrive come vettore di M componenti scalari:
```
F(x) = (f₁(x), f₂(x), ..., fₘ(x))ᵀ,    fᵢ: ℝᴺ → ℝ
```
Le M `fᵢ` sono dette **componenti** di F (funzioni più semplici, scalari di N variabili).

### Funzioni reali di N variabili
`f: ℝᴺ → ℝ`, `f(x₁,...,xₙ) ∈ ℝ`.
- N=1: `f(x)` (una variabile)
- N=2: `f(x,y)` (grafico in ℝ³)
- N=3: `f(x,y,z)`

(Queste funzioni saranno il cuore della Lezione 2.)

---

## 7. Storia ed evoluzione dell'IA

### Definizione (Russell & Norvig, *AI: a modern approach*)
L'IA si articola lungo due assi:

|             | Come una persona | In modo razionale |
|-------------|------------------|-------------------|
| **Pensare** | Pensare come una persona | Pensare razionalmente |
| **Agire**   | Agire come una persona   | Agire razionalmente   |

### Tappe storiche fondamentali

- **1950** — Alan Turing, *Computing Machinery and Intelligence* (rivista *Mind*). Pone la domanda "Can machines think?" e propone l'**Imitation Game** (Test di Turing): un computer è intelligente se è in grado di imitare una persona in una conversazione.
- **Anni '70** — Reti neurali artificiali: simulare il cervello a livello cellulare (neuroni, assoni, soma). Apprendimento tramite training set / test set.
- **1980** — *Neocognitron* di Kunihiko Fukushima: prima rete neurale per riconoscimento di testo manoscritto.
- **1989** — **LeNet** (Yann LeCun): applica l'algoritmo di **backpropagation** al Neocognitron.
- **1997** — Deep Blue (IBM) sconfigge Kasparov a scacchi (branching factor > 40, ~50 mosse).
- **2012** — **AlexNet** (Alex Krizhevsky) vince ImageNet → boom del Deep Learning.
- **2013** — Variational Autoencoders (Kingma, Welling).
- **2014** — **GAN** (Generative Adversarial Networks, Ian Goodfellow). VGG16/VGG19 (Simonyan, Zisserman).
- **2015** — Inception (Google). Diffusion models. AlphaGo (DeepMind) sconfigge Fan Hui (branching factor > 250, ~350 mosse).
- **2018** — StyleGAN (NVIDIA): generazione di volti fake in alta definizione.
- **2019** — **Premio Turing** a LeCun, Bengio, Hinton per il Deep Learning.
- **2022** — DALL-E (OpenAI), Midjourney, StableDiffusion. ChatGPT.

### IA forte vs IA debole
- **IA forte**: un computer correttamente programmato può avere intelligenza non distinguibile da quella umana (Hobbes: "ragionare non è altro che calcolare").
- **IA debole**: un computer non potrà mai eguagliare la mente umana, può solo *simulare* alcuni processi cognitivi.

### Aree dell'IA (oltre il Deep Learning)
- **Sistemi esperti**: logica, regole di deduzione (∧I, ∨E, →E, ∀E, ∃I, ...).
- **Programmazione a vincoli** (CSP): Sudoku, instradamento.
- **Agenti intelligenti**: bot, daemon, BDI (Belief-Desires-Intentions, es. Dragon Age Origins), sistemi multi-agente.
- **Computer Vision, Robotica, Translation, Autonomous Driving, Digital Twins**.
