# Lezione 7 - Integrazione in $\mathbb{R}^N$ e Convoluzione

> Riferimento: `Lezione_7/Lezione 7.pdf` - Prof. Iotti, Fondamenti di IA, UniPR.
> Obiettivo: costruire l'integrale di Riemann in $\mathbb{R}^N$, dimostrarne le proprietà fondamentali, definire la convoluzione 1D/2D e dimostrare commutatività, linearità ed equivarianza alla traslazione tramite cambio di variabile (jacobiano). Casi notevoli: filtro media, filtro gaussiano.

---

## 1. Insiemi compatti e scatole in $\mathbb{R}^N$

### 1.1 Compatto

- **Def.** Un sottoinsieme $K \subseteq \mathbb{R}^N$ si dice **compatto** se è:
  - **chiuso**: il suo complementare $\mathbb{R}^N \setminus K$ è aperto;
  - **limitato**: $\exists\, \delta > 0$ tale che $\forall \underline{x},\underline{y} \in K$, $\|\underline{x}-\underline{y}\| < \delta$.
- Caratterizzazione equivalente in $\mathbb{R}^N$ (Heine–Borel): $K$ compatto $\iff$ chiuso e limitato.

### 1.2 Caso $N=1$: intervallo $[a,b]$

- $[a,b] \subseteq \mathbb{R}$ è compatto.
- Su $[a,b]$ vale il **teorema fondamentale del calcolo integrale**:
  $$\int_a^b f(x)\,dx = F(b) - F(a),$$
  con $F$ primitiva di $f$. L'integrale rappresenta l'area con segno tra grafico e asse $x$.

### 1.3 Scatola in $\mathbb{R}^N$

- **Def.** Si dice **scatola** $[\underline{a},\underline{b}] \subseteq \mathbb{R}^N$ l'insieme
  $$[\underline{a},\underline{b}] = \{\underline{x} \in \mathbb{R}^N : a_1 \le x_1 \le b_1 \,\wedge\, \dots \,\wedge\, a_N \le x_N \le b_N\} = [a_1,b_1] \times [a_2,b_2] \times \dots \times [a_N,b_N].$$
- Ogni scatola è compatta (prodotto di compatti).

### 1.4 Funzione caratteristica (indicatrice)

- **Def.** Per $A \subseteq \mathbb{R}^N$,
  $$\mathbf{1}_A(\underline{x}) = \begin{cases} 1 & \underline{x} \in A \\ 0 & \text{altrimenti}\end{cases}$$
- Caso $N=2$: il grafico di $\mathbf{1}_{[a_1,b_1]\times[a_2,b_2]}$ è un parallelepipedo di altezza 1 sopra la scatola.

---

## 2. Funzioni semplici e integrale

### 2.1 Funzione semplice

- **Def.** $\varphi : \mathbb{R}^N \to \mathbb{R}$ è **semplice (elementare)** se è combinazione lineare finita di indicatrici di scatole:
  $$\varphi(\underline{x}) = \sum_{i=1}^{m} \lambda_i \cdot \mathbf{1}_{[\underline{a}^i,\underline{b}^i]}(\underline{x}), \qquad \lambda_i \in \mathbb{R}.$$
- Si scrive $\varphi \in \mathcal{S}$.

### 2.2 Integrale di una funzione semplice

- **Def.** L'integrale di $\varphi \in \mathcal{S}$ su $\mathbb{R}^N$ è
  $$\int_{\mathbb{R}^N} \varphi(\underline{x})\, d\underline{x} = \sum_{i=1}^m \lambda_i \cdot (b_1^i - a_1^i)(b_2^i - a_2^i)\cdots (b_N^i - a_N^i),$$
  dove $\lambda_i$ è l'**altezza** e il prodotto delle differenze è la **misura della base** (volume $N$-dim).
- Forma equivalente con integrali iterati su scatole:
  $$\int_{\mathbb{R}^N} \varphi\, d\underline{x} = \sum_{i=1}^m \lambda_i \int_{a_1^i}^{b_1^i}\int_{a_2^i}^{b_2^i}\cdots\int_{a_N^i}^{b_N^i} 1\, dx_1\, dx_2\, \dots dx_N.$$

---

## 3. Integrale di Riemann in $\mathbb{R}^N$

Sia $f : \mathbb{R}^N \to \mathbb{R}$ **limitata** ($|f(\underline{x})| < \delta$) e a **supporto compatto** ($\text{supp}(f) \subseteq K$ scatola).

### 3.1 Minoranti e maggioranti semplici

- $S_-(f) = \{\psi \in \mathcal{S} : \psi(\underline{x}) \le f(\underline{x})\ \forall \underline{x} \in \mathbb{R}^N\}$ - minoranti semplici.
- $S_+(f) = \{\varphi \in \mathcal{S} : \varphi(\underline{x}) \ge f(\underline{x})\ \forall \underline{x} \in \mathbb{R}^N\}$ - maggioranti semplici.
- Osservazione: $S_-(f) \neq \emptyset$ e $S_+(f) \neq \emptyset$ perché $f$ è limitata e a supporto compatto (basta prendere $\pm \delta \cdot \mathbf{1}_K$).

### 3.2 Definizione di integrale di Riemann

- **Def.** $f$ è integrabile secondo Riemann se
  $$\sup\!\left\{\int_{\mathbb{R}^N}\psi\, d\underline{x} : \psi \in S_-(f)\right\} = \inf\!\left\{\int_{\mathbb{R}^N}\varphi\, d\underline{x} : \varphi \in S_+(f)\right\}.$$
  In tal caso, il valore comune è
  $$\int_{\mathbb{R}^N} f(\underline{x})\, d\underline{x} = \int_{D_1}\int_{D_2}\cdots\int_{D_N} f(x_1,\dots,x_N)\, dx_1\, dx_2\, \dots dx_N,$$
  con $\text{supp}(f) = D_1 \times D_2 \times \dots \times D_N$.

### 3.3 Proprietà dell'integrale

1. **Linearità.** Se $f,g$ integrabili e $\lambda \in \mathbb{R}$:
   $$\int_{\mathbb{R}^N}(f+g)\,d\underline{x} = \int_{\mathbb{R}^N} f\,d\underline{x} + \int_{\mathbb{R}^N} g\,d\underline{x}, \qquad \int_{\mathbb{R}^N}\lambda f\,d\underline{x} = \lambda \int_{\mathbb{R}^N} f\,d\underline{x}.$$
2. **Monotonia.** Se $f \le g$ ovunque allora $\int f \le \int g$. In particolare $f \le |f|$ implica $\int f \le \int |f|$.
3. **Disuguaglianza triangolare integrale.**
   $$\left|\int_{\mathbb{R}^N} f(\underline{x})\,d\underline{x}\right| \le \int_{\mathbb{R}^N} |f(\underline{x})|\,d\underline{x}.$$

### 3.4 Esempio (HW): $N=2$

Sia $f(x,y) = x^2 + y e^x$ su $K = [0,1] \times [1,2]$.
- $\int_K f(x,y)\,dx\,dy = \int_0^1 \int_1^2 f(x,y)\,dy\,dx = \int_1^2 \int_0^1 f(x,y)\,dx\,dy$ (Fubini su scatola).

---

## 4. Cambio di variabile in $\mathbb{R}^N$

### 4.1 Matrice jacobiana

- Sia $g : A \to B$ con $A,B \subseteq \mathbb{R}^N$, $g$ differenziabile e biiettiva, $\underline{x} \mapsto \underline{y} = g(\underline{x})$.
- **Matrice jacobiana:**
  $$J_g = \begin{pmatrix} \dfrac{\partial g_1}{\partial x_1} & \dfrac{\partial g_1}{\partial x_2} & \cdots & \dfrac{\partial g_1}{\partial x_N}\\[4pt] \dfrac{\partial g_2}{\partial x_1} & \dfrac{\partial g_2}{\partial x_2} & \cdots & \dfrac{\partial g_2}{\partial x_N}\\[2pt] \vdots & & & \vdots \\[2pt] \dfrac{\partial g_N}{\partial x_1} & \cdots & & \dfrac{\partial g_N}{\partial x_N}\end{pmatrix}.$$

### 4.2 Formula del cambio di variabile

- **Teorema.** Se $f : \mathbb{R}^N \to \mathbb{R}$ è integrabile in $A$, allora
  $$\boxed{\ \int_A f(\underline{x})\,d\underline{x} \;=\; \int_B f(g(\underline{y}))\,|\det(J_g)|\,d\underline{y}\ }$$
  (con $g$ biiettiva $A \to B$; nelle convenzioni del corso si scrive equivalentemente $\int_A f(g(\underline{x}))|\det J_g|\,d\underline{x} = \int_B f(\underline{y})\,d\underline{y}$).
- Il fattore $|\det J_g|$ corregge la dilatazione/contrazione del volume infinitesimo: $d\underline{y} = |\det J_g|\,d\underline{x}$.

---

## 5. Convoluzione

### 5.1 Definizione (1D, $N=1$)

- $x : \mathbb{R} \to \mathbb{R}$ segnale in ingresso, $w : \mathbb{R} \to \mathbb{R}$ **nucleo (kernel)**.
- **Convoluzione 1D**: si "scontra" $w$ contro $x$:
  $$(x * w)(t) = \int_{\mathbb{R}} x(a)\, w(t-a)\, da \;=\; s(t) \quad \text{(feature map)}.$$
- Interpretazione "antialiasing": $x$ rumoroso, $w$ pesa una finestra attorno a $t$ producendo segnale "pulito".

### 5.2 Definizione (2D, $N=2$)

- $x : \mathbb{R}^2 \to \mathbb{R}$, $w : \mathbb{R}^2 \to \mathbb{R}$.
- **Convoluzione 2D**:
  $$(x * w)(u,v) = \iint_{\mathbb{R}^2} x(a,b)\, w(u-a,\, v-b)\, da\, db \;=\; s(u,v).$$

### 5.3 Condizione kernel = densità di probabilità

Per ottenere filtri di **smoothing** (media pesata, non amplifica) si richiede a $w$:
$$w \ge 0, \qquad \int_{\mathbb{R}} w(t)\, dt = 1 \quad (\text{o }\iint w = 1\text{ in 2D}).$$

---

## 6. Filtro media (1D)

- Kernel: $w(t) = \mathbf{1}_{[-k,k]}(t)\cdot \dfrac{1}{2k}$.
- Verifica densità: $w \ge 0$ e $\int w = \frac{1}{2k}\cdot 2k = 1$. ✓
- Calcolo esplicito di $(x*w)(t)$:
  $$(x*w)(t) = \int_{\mathbb{R}} x(a)\,\mathbf{1}_{[-k,k]}(t-a)\cdot\frac{1}{2k}\, da.$$
- Cambio di variabile $\bar t = t-a \Rightarrow a = t-\bar t,\ da = -d\bar t$. Per $a \in [t-k, t+k]$ si ha $\bar t \in [-k,k]$:
  $$(x*w)(t) = \int_{-k}^{k} x(t-\bar t)\cdot\frac{1}{2k}\, d\bar t = \frac{1}{2k}\int_{-k}^{k} x(t-\bar t)\, d\bar t.$$
- Interpretazione: media locale di $x$ in una finestra di ampiezza $2k$ centrata in $t$.

---

## 7. Proprietà della convoluzione (1D) - con dimostrazione

### 7.1 Commutatività: $(x*w)(t) = (w*x)(t)$

- **Dim.** Cambio di variabile $b = t-a \Rightarrow a = t-b,\ db = -da$. Quando $a$ va da $-\infty$ a $+\infty$, $b$ va da $+\infty$ a $-\infty$:
  $$(x*w)(t) = \int_{\mathbb{R}} x(a)\,w(t-a)\,da = \int_{+\infty}^{-\infty} x(t-b)\,w(b)\,(-db)$$
  $$= -\int_{+\infty}^{-\infty} x(t-b)w(b)\,db = \int_{-\infty}^{+\infty} w(b)\,x(t-b)\,db = (w*x)(t). \quad \blacksquare$$

### 7.2 Linearità (nell'input)

- Per $x,y$ segnali e $\lambda,\mu \in \mathbb{R}$:
  $$\big((\lambda x + \mu y) * w\big)(t) = \lambda\,(x*w)(t) + \mu\,(y*w)(t).$$
- Discende direttamente dalla **linearità dell'integrale**.

### 7.3 Equivarianza alla traslazione (NON invarianza!)

- Sia $\tilde x(t) = x(t-\tau)$ (segnale ritardato di $\tau$). Allora
  $$(\tilde x * w)(t) = (x*w)(t-\tau) = s(t-\tau).$$
- **Dim.** Calcolo:
  $$(\tilde x * w)(t) = \int_{\mathbb{R}} \tilde x(a)\,w(t-a)\,da = \int_{\mathbb{R}} x(a-\tau)\,w(t-a)\,da.$$
  Cambio di variabile $b = a - \tau \Rightarrow a = b+\tau,\ db = da$ (jacobiano = 1):
  $$= \int_{\mathbb{R}} x(b)\, w(t-b-\tau)\,db = \int_{\mathbb{R}} x(b)\, w\big((t-\tau)-b\big)\,db = (x*w)(t-\tau).\quad \blacksquare$$
- **Lettura**: traslando l'input di $\tau$ l'output trasla anch'esso di $\tau$. Non è invarianza (l'output non resta identico), è **equivarianza**.

---

## 8. Proprietà della convoluzione (2D)

### 8.1 Commutatività in 2D

- **Dim.** Cambio di variabile $\alpha = u-a,\ \beta = v-b$, ovvero $g(a,b) = (u-a, v-b)$:
  $$J_g = \begin{pmatrix} \partial_a g_1 & \partial_b g_1 \\ \partial_a g_2 & \partial_b g_2 \end{pmatrix} = \begin{pmatrix} -1 & 0 \\ 0 & -1\end{pmatrix}, \quad |\det J_g| = 1.$$
  Quindi
  $$(x*w)(u,v) = \iint x(a,b)\,w(u-a,v-b)\,da\,db = \iint x(u-\alpha, v-\beta)\,w(\alpha,\beta)\cdot 1\, d\alpha\,d\beta = (w*x)(u,v).\quad \blacksquare$$

### 8.2 Linearità in 2D

- $\big((\lambda x + \mu y)*w\big)(u,v) = \lambda(x*w)(u,v) + \mu(y*w)(u,v)$. (linearità integrale).

### 8.3 Equivarianza alla posizione (2D)

- Sia $\tilde x(u,v) = x(u-u_0, v-v_0)$. Allora $(\tilde x * w)(u,v) = (x*w)(u-u_0, v-v_0)$.
- **Dim.**
  $$(\tilde x * w)(u,v) = \iint x(a-u_0, b-v_0)\,w(u-a,v-b)\,da\,db.$$
  Cambio di variabile $\alpha = a - u_0,\ \beta = b - v_0$:
  $$J_g = \begin{pmatrix} 1 & 0 \\ 0 & 1\end{pmatrix}, \quad |\det J_g| = 1,$$
  $$= \iint x(\alpha,\beta)\,w\big((u-u_0)-\alpha,\,(v-v_0)-\beta\big)\,d\alpha\,d\beta = (x*w)(u-u_0, v-v_0).\quad \blacksquare$$
- Conseguenza fondamentale per le CNN: rilevatori di feature **traslano con l'input**, non sono ancorati a una posizione assoluta.

---

## 9. Filtro gaussiano 2D

### 9.1 Definizione

- Parametri: $\mu = 0$, $\sigma > 0$ (gaussiana isotropa $\mathcal{N}(\underline{0}, \sigma^2 I)$):
  $$w(u,v) = \frac{1}{2\pi\sigma^2}\, e^{-\frac{u^2+v^2}{2\sigma^2}}.$$
- **Separabilità**: si fattorizza come prodotto di gaussiane 1D:
  $$w(u,v) = \underbrace{\frac{1}{\sqrt{2\pi}\sigma}\, e^{-\frac{u^2}{2\sigma^2}}}_{=\,g(u)}\;\cdot\;\underbrace{\frac{1}{\sqrt{2\pi}\sigma}\, e^{-\frac{v^2}{2\sigma^2}}}_{=\,g(v)}.$$
- Vantaggio computazionale: convoluzione 2D = due convoluzioni 1D in cascata (riga + colonna).

### 9.2 Convoluzione (uso della commutativa)

$$(x*w)(u,v) = \iint x(a,b)\, w(u-a,v-b)\,da\,db \overset{\text{commut.}}{=} \iint x(u-a, v-b)\cdot \frac{1}{2\pi\sigma^2} e^{-\frac{a^2+b^2}{2\sigma^2}}\,da\,db.$$

### 9.3 Coordinate polari

Cambio di variabile $g : (\rho,\theta) \mapsto (a,b)$ con
$$a = \rho\cos\theta, \qquad b = \rho\sin\theta, \qquad \rho = \sqrt{a^2+b^2}\ge 0,\quad \theta \in [0, 2\pi).$$
- Jacobiano:
  $$J_g = \begin{pmatrix} \cos\theta & -\rho\sin\theta \\ \sin\theta & \rho\cos\theta\end{pmatrix}, \quad \det J_g = \rho\cos^2\theta + \rho\sin^2\theta = \rho.$$
- Quindi $da\,db = \rho\, d\rho\, d\theta$ e
  $$(x*w)(u,v) = \int_0^{+\infty}\!\!\int_0^{2\pi} x(u-\rho\cos\theta,\, v-\rho\sin\theta)\cdot \frac{1}{2\pi\sigma^2} e^{-\frac{\rho^2}{2\sigma^2}}\,\rho\, d\rho\, d\theta.$$

### 9.4 Troncamento e discretizzazione

- La gaussiana decresce rapidamente: $\exists\, M > 0$ (tipicamente $M \approx 3\sigma$) tale che $\rho > M \Rightarrow |w(u,v)| < \varepsilon$ piccolo a piacere.
- Approssimazione su scatola finita:
  $$\int_{\mathbb{R}^2} \cdots \approx \int_{-M}^{M}\!\!\int_{-M}^{M} \cdots \;=\; \int_0^{M}\!\!\int_0^{2\pi} \cdots \,d\rho\, d\theta.$$
- Nel **discreto** (immagini): si scelgono $M$ e $\sigma$ come iperparametri; il kernel diventa una matrice $(2M+1)\times(2M+1)$ di campioni di $w$, eventualmente rinormalizzata affinché la somma faccia 1.

---

## 10. Sintesi - checklist d'esame

- [ ] Sapere definire compatto, scatola, indicatrice, funzione semplice.
- [ ] Saper scrivere $\int_{\mathbb{R}^N}\varphi$ per $\varphi$ semplice (altezza × prodotto basi).
- [ ] Saper definire integrabilità di Riemann via $\sup S_-$ = $\inf S_+$.
- [ ] Linearità, monotonia, disuguaglianza triangolare integrale.
- [ ] Formula cambio di variabile con $|\det J_g|$.
- [ ] Definizione convoluzione 1D e 2D, ruolo del kernel come densità ($w\ge 0,\ \int w=1$).
- [ ] Filtro media: kernel + calcolo esplicito.
- [ ] Dimostrare commutatività (1D e 2D), linearità, equivarianza alla traslazione/posizione (1D e 2D) - sempre via cambio di variabile con jacobiano.
- [ ] Filtro gaussiano: forma, separabilità, passaggio in polari ($|\det J_g|=\rho$), troncamento $\sim 3\sigma$, discretizzazione.
- [ ] Distinguere **equivarianza** da **invarianza**: la convoluzione è equivariante alle traslazioni.
