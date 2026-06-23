# Lezione 3 - Discesa del Gradiente e Reti Neurali

## 1. Algoritmo di Discesa del Gradiente

### 1.1 Setup e problema
- Data $f:\mathbb{R}^N\to\mathbb{R}$, gradiente $\nabla f=\left(\dfrac{\partial f}{\partial x_1},\dots,\dfrac{\partial f}{\partial x_N}\right)$.
- **Problema**: trovare un **minimo** della funzione $f$ (idealmente globale, in pratica locale).
- **Idea geometrica**: $\nabla f$ punta nella direzione di **massima crescita** $\Rightarrow$ ci si muove in direzione **opposta**: $-\nabla f$.

### 1.2 Caso N = 1
- Funzione $f:\mathbb{R}\to\mathbb{R}$, esempio $f(x)=x^2$, minimo in $x=0$.
- Se $x_0>0$ allora $f'(x_0)=2x_0>0$ (la derivata "porta su"); per scendere si va in direzione $-f'$.
- **Iterazione**:
  $$x_0=a\in\mathbb{R},\qquad x_m=x_{m-1}-\eta\, f'(x_{m-1})$$
  con $\eta\in\mathbb{R}$ **iperparametro** (learning rate), $m\in\mathbb{N}$.

### 1.3 Caso N > 1
- Funzione $f:\mathbb{R}^N\to\mathbb{R}$.
- **Iterazione vettoriale**:
  $$\underline{x}_0=\underline{a}\in\mathbb{R}^N,\qquad \underline{x}_m=\underline{x}_{m-1}-\eta\,\nabla f(\underline{x}_{m-1})$$
- Esempio $N=2$: $f(x,y)=x^2+y^2$, $\nabla f=(2x,2y)$, minimo in $(0,0)$.

### 1.4 Strategie di terminazione
Dato un minimo $\underline{m}$ (quando noto) e una soglia $\varepsilon>0$, l'iterazione si arresta secondo una delle seguenti condizioni:

1. **Vicinanza al minimo**: $\|\underline{x}_m-\underline{m}\|<\varepsilon$.
2. **Vicinanza in valore**: $|f(\underline{x}_m)-f(\underline{m})|<\varepsilon$.
3. **Stagnazione dell'iterato**: $\|\underline{x}_m-\underline{x}_{m-1}\|<\varepsilon$.
4. **Gradiente piccolo**: $\|\nabla f(\underline{x}_m)\|<\varepsilon$.
   - Caso limite: $\nabla f(\underline{x}_m)=0\Rightarrow \underline{x}_{m+1}=\underline{x}_m-\eta\cdot 0=\underline{x}_m$ (l'algoritmo è fermo).
5. **Numero massimo di iterazioni**: $m>T$ con $T$ soglia.

> Nota: 1 e 2 richiedono di conoscere $\underline{m}$ (in pratica raramente disponibile); 3, 4, 5 sono le strategie effettivamente usabili.

---

## 2. Reti Neurali - Modello Base: Percettrone

### 2.1 Definizione
- Funzione $f_{\underline{w},b}:\mathbb{R}^N\to\mathbb{R}$ con parametri $\underline{w}\in\mathbb{R}^N$ (pesi) e $b\in\mathbb{R}$ (bias).
- **Formulazione classica con soglia $T$**:
  $$f(\underline{x})=\begin{cases}0 & \text{se }\sum_{i=1}^N x_i w_i\le T \\ 1 & \text{se }\sum_{i=1}^N x_i w_i> T\end{cases}$$
- Riscrittura con **bias** $b=-T$:
  $$f(\underline{x})=\begin{cases}0 & \underline{x}\cdot\underline{w}+b\le 0 \\ 1 & \underline{x}\cdot\underline{w}+b> 0\end{cases}$$
- **Output determinato** dal segno di $\underline{x}\cdot\underline{w}+b$:
  - $\le 0$: neurone **non attivo**;
  - $>0$: neurone **attivo**.

### 2.2 Funzione di attivazione (Heaviside)
- Definizione: $\sigma:\mathbb{R}\to\mathbb{R}$, $\sigma(x)=\begin{cases}0 & x\le 0\\ 1 & x>0\end{cases}$.
- Forma compatta del percettrone: $\boxed{\,f(\underline{x})=\sigma(\underline{x}\cdot\underline{w}+b)\,}$.

### 2.3 Problema di mal-condizionamento
- Heaviside è **discontinua**: piccole perturbazioni $\Delta\underline{w},\Delta b,\Delta\underline{x}$ possono causare un **salto totale** dell'output (da 0 a 1).
- Conseguenza: **non è differenziabile** $\Rightarrow$ non si può ottimizzare con discesa del gradiente.
- **Soluzione**: sostituire Heaviside con $\sigma$ **continua, derivabile, limitata**.

---

## 3. Funzioni di Attivazione (proprietà richieste)

Funzioni $\sigma:\mathbb{R}\to\mathbb{R}$ **non decrescenti** con proprietà utili:
1. **Continua**: $\sigma\in\mathcal{C}^0(\mathbb{R})$.
2. **Derivabile con derivata continua**: $\sigma\in\mathcal{C}^1(\mathbb{R})$ (o $\mathcal{C}^k$, fino a $\mathcal{C}^\infty$).
3. **Limitata**: $\exists L\ge 0$ tale che $\forall x\in\mathbb{R},\ |\sigma(x)|\le L$.

Un percettrone con $\sigma$ di attivazione almeno $\mathcal{C}^1$ si dice **neurone artificiale**.

### 3.1 Sigmoide logistica
- $\sigma_\beta:\mathbb{R}\to\mathbb{R}$, $\sigma_\beta\in\mathcal{C}^\infty$, monotona crescente, $|\sigma|\le 1$, parametro $\beta>0$.
- Formula:
  $$\sigma_\beta(x)=\frac{1}{1+e^{-\beta x}}$$
- **Derivata** (passaggio chiave: aggiungo e sottraggo 1 al numeratore $e^{-\beta x}=e^{-\beta x}+1-1$):
  $$\frac{d\sigma}{dx}(x)=\frac{\beta e^{-\beta x}}{(1+e^{-\beta x})^2}=\beta\cdot\frac{1}{1+e^{-\beta x}}\cdot\frac{e^{-\beta x}+1-1}{1+e^{-\beta x}}=\beta\,\sigma(x)\big(1-\sigma(x)\big)$$
- **Limite**: $\displaystyle\lim_{\beta\to+\infty}\sigma_\beta(x)=\begin{cases}1 & x\ge 0\\ 0 & x<0\end{cases}$ (recupera Heaviside).

### 3.2 Tangente iperbolica (tanh)
- $\sigma_\beta\in\mathcal{C}^\infty$, monotona crescente, $|\sigma|\le 1$, $\beta>0$.
- Formula:
  $$\sigma_\beta(x)=\tanh(\beta x)=\frac{e^{\beta x}-e^{-\beta x}}{e^{\beta x}+e^{-\beta x}}=\frac{e^{2\beta x}-1}{e^{2\beta x}+1}=\frac{1-e^{-2\beta x}}{1+e^{-2\beta x}}$$
- **Limite**: $\displaystyle\lim_{\beta\to+\infty}\tanh(\beta x)=\begin{cases}1 & x>0\\ 0 & x=0\\ -1 & x<0\end{cases}$.
- **Relazione con la sigmoide logistica**:
  $$\boxed{\,\sigma_{2\beta}^{\text{logistica}}(x)=\tfrac{1}{2}\big(\tanh_\beta(\beta x)+1\big)\,}$$

### 3.3 ReLU (Rectified Linear Unit)
- $\sigma\in\mathcal{C}^0(\mathbb{R})$ (non $\mathcal{C}^1$ in 0), monotona crescente, **non limitata**.
- Formula:
  $$\sigma(x)=\max\{0,x\}=\begin{cases}0 & x\le 0\\ x & x>0\end{cases}$$
- Derivata: $\sigma'(x)=0$ se $x\le 0$, $\sigma'(x)=1$ se $x>0$.

### 3.4 Softplus (Smooth ReLU)
- $\sigma_\beta\in\mathcal{C}^\infty(\mathbb{R})$, monotona crescente.
- Formula:
  $$\sigma_\beta(x)=\frac{1}{\beta}\log\big(1+e^{\beta x}\big)$$
- È un'approssimazione $\mathcal{C}^\infty$ di ReLU, recuperata per $\beta\to+\infty$.

---

## 4. Single-Layer Perceptron (SLP)

### 4.1 Definizione formale
**Def**: si dice **SLP** un grafo $G=\langle V,E\rangle$ con le proprietà:
- **Diretto** (archi orientati: $(a,b)\ne(b,a)$),
- **Bipartito**: $\exists\,A,B\subseteq V$ con $A\cap B=\emptyset$ e $A\cup B=V$ (strati di **input** e **output**),
- **Aciclico**,
- **Fully connected** (ogni nodo di $A$ collegato a ogni nodo di $B$),
- I vertici sono **neuroni artificiali**.

### 4.2 Formulazione vettoriale
- $f_\theta:\mathbb{R}^N\to\mathbb{R}^M$ con parametri $\theta=(W,\underline{b})$.
- $W\in\mathbb{R}^{N\times M}$ **matrice dei pesi**: la colonna $\underline{W}_j$ contiene i pesi del neurone $j$.
- $\underline{b}=(b_1,\dots,b_M)^T\in\mathbb{R}^M$ **vettore dei bias**.
- **Uscita componente per componente**:
  $$f_\theta(\underline{x})=\begin{pmatrix}\sigma(\underline{x}\cdot\underline{W}_1+b_1)\\ \sigma(\underline{x}\cdot\underline{W}_2+b_2)\\ \vdots\\ \sigma(\underline{x}\cdot\underline{W}_M+b_M)\end{pmatrix}=\Big(\sigma\Big(\textstyle\sum_{i=1}^N w_{i,j}x_i+b_j\Big)\Big)_{j=1}^M$$
- Forma compatta:
  $$\boxed{\,f_\theta(\underline{x})=\sigma\big(W^T\underline{x}+\underline{b}\big)\,}$$

---

## 5. Multi-Layer Perceptron (MLP)

### 5.1 Definizione formale
**Def**: si dice **MLP** un grafo $G=\langle V,E\rangle$ **diretto e aciclico** con:
- **$L$ strati nascosti** + 1 strato di **input** + 1 strato di **output**;
- gli strati $S_{\text{IN}},S_1,\dots,S_L,S_{\text{OUT}}$ sono **a due a due disgiunti** e $S_{\text{IN}}\cup S_1\cup\dots\cup S_L\cup S_{\text{OUT}}=V$;
- i sottografi $G_{i,j}=\langle S_i\cup S_j,E\rangle$ tra strati consecutivi sono **bipartiti** e **fully connected**.

Cardinalità: $m_{\text{IN}}=N$, $m_1,m_2,\dots,m_L$, $m_{\text{OUT}}=M$. Matrici di pesi $W^{(1)},W^{(2)},\dots,W^{(L+1)}$, bias $\underline{b}^{(1)},\dots,\underline{b}^{(L+1)}$.

### 5.2 Formulazione ricorsiva
$$F:\mathbb{R}^N\to\mathbb{R}^{m_1}\to\mathbb{R}^{m_2}\to\cdots\to\mathbb{R}^{m_L}\to\mathbb{R}^M$$
$$\boxed{\;\begin{cases}F_0(\underline{x})=\underline{x}\\ F_k(\underline{x})=\sigma\big({W^{(k)}}^T\,F_{k-1}(\underline{x})+\underline{b}^{(k)}\big)\end{cases}\;}$$

### 5.3 Esempio: MLP con 1 strato nascosto
$$F(\underline{x})=\sigma\Big({W^{(2)}}^T\cdot\underbrace{\sigma\big({W^{(1)}}^T\underline{x}+\underline{b}^{(1)}\big)}_{\text{attivazione del I strato}}+\underline{b}^{(2)}\Big)$$

### 5.4 Pre-attivazione vs attivazione
- **Pre-attivazione** del neurone: $\underline{w}\cdot\underline{x}+b$ (combinazione lineare, prima di $\sigma$).
- **Attivazione**: $\sigma(\underline{w}\cdot\underline{x}+b)$ (output non lineare del neurone).

---

## 6. Apprendimento Supervisionato (introduzione)

### 6.1 Problema generale
- Dato un **modello** $F_\theta$ (SLP o MLP) con parametri $\theta=(W,\underline{b})$, trovare $\theta^*$ tale che $F_{\theta^*}$ approssimi bene una **funzione obiettivo** $f^*:\mathbb{R}^N\to\mathbb{R}^M$, **non nota** in forma analitica.

### 6.2 Dataset
$$D=\big\{(\underline{x},f^*(\underline{x})):\underline{x}\in\mathbb{R}^N\big\}$$
- Insieme di esempi (input, output corretto) usati per ottimizzare $\theta$.
- **Interpolazione vs Fitting**: il modello deve **generalizzare**, non solo passare esattamente per i punti.

> Continua in Lezione 4: definizione della **loss** e minimizzazione tramite discesa del gradiente.
