# Lezione 4 — Apprendimento Supervisionato, Loss e Discesa del Gradiente

## 1. Apprendimento Supervisionato (Machine Learning)

### 1.1 Dataset
- **Dataset**: insieme di esempi $(\underline{x},\underline{y})$ con $\underline{x}\in\mathbb{R}^N$, $\underline{y}\in\mathbb{R}^M$, dove $\underline{y}=f^*(\underline{x})$ è l'output corretto.
- **Suddivisione in tre insiemi disgiunti**:
  $$D_{\text{train}}\cap D_{\text{val}}=\emptyset,\qquad D_{\text{train}}\cap D_{\text{test}}=\emptyset$$
  - **$D_{\text{train}}$**: usato dall'**algoritmo di addestramento** per modificare i parametri $\theta=(W,\underline{b})$.
  - **$D_{\text{val}}$**: usato durante il training per controllare la qualità del modello (tuning iperparametri).
  - **$D_{\text{test}}$**: usato a modello "pronto" per valutare le performance finali.
- **Inferenza**: applicazione del modello addestrato su input nuovi.

### 1.2 Strategia su SLP e MLP a 1 strato nascosto
L'apprendimento si basa sull'**ottimizzazione**:
1. **Definire una misura dell'errore** (costo / loss).
2. **Minimizzare il costo** rispetto ai parametri $\theta$.

### 1.3 Misura dell'errore
- Si misura la distanza fra $f^*(\underline{x})$ (target dal dataset) e $F_\theta(\underline{x})$ (output del modello) tramite una **norma** in $\mathbb{R}^M$:
  $$\|f^*(\underline{x})-F_\theta(\underline{x})\|=\|\underline{y}^*-\underline{y}\|$$
- **Problema di ottimizzazione**:
  $$\min_{\theta}\ \|\underline{y}^*-F_\theta(\underline{x})\|,\qquad \theta=(W,\underline{b})$$

---

## 2. Funzione di Costo (Loss)

**Def**: si dice **funzione di costo / di perdita / loss** una funzione definita su un dataset $D=\{(\underline{x},\underline{y}):\underline{x}\in\mathbb{R}^N,\ \underline{y}\in\mathbb{R}^M\}$:
$$\mathcal{L}:D\to\mathbb{R}$$

### 2.1 Loss $L_1$
Per $|D|=m$:
$$\boxed{\;\mathcal{L}_1(D):=\sum_{i=1}^m \big\|f^*(\underline{x}_i)-F_\theta(\underline{x}_i)\big\|=\sum_{i=1}^m\|\underline{y}_i^*-F_\theta(\underline{x}_i)\|\;}$$
- Interpretazione geometrica: per $|D|=2$ corrisponde alla **geometria del taxi** (somma delle distanze).

### 2.2 Loss $L_2$ — Errore Quadratico Medio (MSE)
Per $|D|=m$, $f^*:\mathbb{R}^N\to\mathbb{R}^M$, $F_\theta:\mathbb{R}^N\to\mathbb{R}^M$:
$$\boxed{\;\mathcal{L}_2(D)=\frac{1}{2m}\sum_{i=1}^m\big\|f^*(\underline{x}_i)-F_\theta(\underline{x}_i)\big\|^2=\frac{1}{2m}\sum_{i=1}^m\big\|\underline{y}_i^*-F_\theta(\underline{x}_i)\big\|^2\;}$$
- Vista come funzione dei parametri: $\mathcal{L}:\mathbb{R}^P\to\mathbb{R}$, $\theta\mapsto\mathcal{L}(\theta)$.

### 2.3 $\mathcal{L}_2$ specializzata per SLP
Con $F_\theta(\underline{x})=\sigma(W^T\underline{x}+\underline{b})$:
$$\mathcal{L}_2^{\text{SLP}}(D)=\frac{1}{2m}\sum_{i=1}^m\big\|\underline{y}_i^*-\sigma\big(W^T\underline{x}_i+\underline{b}\big)\big\|^2=\mathcal{L}_2^{\text{SLP}}(W,\underline{b})$$

### 2.4 $\mathcal{L}_2$ specializzata per MLP a 1 strato nascosto
$$\mathcal{L}_2^{\text{MLP}}(D)=\frac{1}{2m}\sum_{i=1}^m\Big\|\underline{y}_i^*-\sigma\Big({W^{(2)}}^T\sigma\big({W^{(1)}}^T\underline{x}_i+\underline{b}^{(1)}\big)+\underline{b}^{(2)}\Big)\Big\|^2$$
$$=\mathcal{L}_2^{\text{MLP}}\big(W^{(1)},W^{(2)},\underline{b}^{(1)},\underline{b}^{(2)}\big)$$

> **STEP 1**: definire il costo. ✓

---

## 3. Minimizzazione del Costo

### 3.1 Problema
$$\min_\theta\ \mathcal{L}_2^{\text{SLP}}(\theta);\qquad \min_\theta\ \mathcal{L}_2^{\text{MLP}}(\theta)$$

### 3.2 Osservazione: SLP è ben condizionato se $\sigma$ è differenziabile
- Heaviside era discontinua $\Rightarrow$ il problema era **mal-condizionato**.
- Se $\sigma$ è **differenziabile**, allora $F_\theta(\underline{x})=\sigma(W^T\underline{x}+\underline{b})$ è differenziabile.
- **Definizione di differenziale** ($F_\theta^{(j)}$ è la $j$-esima componente):
  $$dF_\theta^{(j)}(\underline{x}_0)=\sum_{i=1}^N\frac{\partial F_\theta^{(j)}}{\partial w_{ij}}\,dw_{ij}+\frac{\partial F_\theta^{(j)}}{\partial b_j}\,db_j=\sum_{i=1}^N \lambda\,dw_{ij}+\mu\,db_j$$
  con $\lambda,\mu\in\mathbb{R}$ valutati in $\underline{x}_0$. Conseguenza: piccole perturbazioni di $W,\underline{b}$ producono **piccole** variazioni di $F$ (problema **ben-condizionato**).

### 3.3 Algoritmo di Discesa del Gradiente per la Loss
$$\boxed{\;\begin{cases}\underline{\theta}_0=\underline{a}\quad\text{(scelti casualmente)}\\ \underline{\theta}_k=\underline{\theta}_{k-1}-\eta\,\nabla_\theta\mathcal{L}(\underline{\theta}_{k-1})\end{cases}\;}$$
- $\eta$ = **coefficiente di apprendimento** (learning rate), iperparametro.
- L'aggiornamento è sui **parametri** (pesi e bias).
- Il gradiente è calcolato rispetto a $\theta$ (parametri).
- **Epoca**: una iterazione completa dell'algoritmo. Si conclude dopo $N_e$ iterazioni/epoche.
- $\mathcal{L}^{\text{SLP}}(W,\underline{b})\ge 0$ e si vuole arrivare a $\mathcal{L}^{\text{SLP}}(W,\underline{b})\approx 0$, equivalente a $F_\theta(\underline{x})\approx \underline{y}^*\ \forall(\underline{x},\underline{y}^*)\in D$.

---

## 4. Dimostrazione: perché $\underline{v}=-\eta\nabla\mathcal{L}$

### 4.1 Obiettivo
Si vuole, ad ogni passo, $\mathcal{L}(\underline{\theta}_k)<\mathcal{L}(\underline{\theta}_{k-1})$, ossia:
$$\Delta\mathcal{L}=\mathcal{L}(\underline{\theta}_k)-\mathcal{L}(\underline{\theta}_{k-1})<0$$

### 4.2 Approssimazione differenziale
Se $\underline{\theta}_k-\underline{\theta}_{k-1}\approx 0$ ed $\mathcal{L}$ è differenziabile:
$$\Delta\mathcal{L}\approx d\mathcal{L}(\underline{v}),\qquad \underline{v}:=\underline{\theta}_k-\underline{\theta}_{k-1}$$
$$d\mathcal{L}(\underline{v})=\nabla_\theta\mathcal{L}\cdot\underline{v}$$
Vogliamo $\nabla_\theta\mathcal{L}\cdot\underline{v}<0$.

### 4.3 Scelta della direzione
**Idea**: $\underline{v}=-\eta\,\nabla_\theta\mathcal{L}$ con $\eta\in\mathbb{R}$, $\eta>0$.
$$d\mathcal{L}(\underline{v})=\nabla_\theta\mathcal{L}\cdot(-\eta\,\nabla_\theta\mathcal{L})=-\eta\,\|\nabla_\theta\mathcal{L}\|^2<0\qquad\checkmark$$
(in quanto $\eta>0$ e $\|\nabla_\theta\mathcal{L}\|^2>0$ se $\nabla\ne 0$).

### 4.4 Condizione su $\eta$
L'approssimazione $\Delta\mathcal{L}\approx d\mathcal{L}$ è buona solo se $\underline{\theta}_k\approx\underline{\theta}_{k-1}$, ma serve $\|\underline{\theta}_k-\underline{\theta}_{k-1}\|>0$ (altrimenti l'algoritmo è fermo). Quindi $\eta$ molto piccolo **ma non nullo**.
- Imponendo $\|\underline{v}\|=\varepsilon>0$:
  $$\varepsilon=\|\underline{v}\|=\|-\eta\,\nabla_\theta\mathcal{L}\|=\eta\,\|\nabla_\theta\mathcal{L}\|$$
- Condizione operativa:
  $$\boxed{\;\eta\approx\frac{\varepsilon}{\|\nabla_\theta\mathcal{L}\|}\;}$$
- $\eta$ né troppo grande (rompe l'approssimazione) né nullo (non avanza).

### 4.5 Aggiornamento finale
$$\underline{\theta}_k=\underline{\theta}_{k-1}+\underline{v}=\underline{\theta}_{k-1}-\eta\,\nabla_\theta\mathcal{L}(\underline{\theta}_{k-1})$$

---

## 5. Chain-Rule (Derivata della Funzione Composta)

### 5.1 Caso $N=1$: $f,g:\mathbb{R}\to\mathbb{R}$
$f\circ g:\mathbb{R}\to\mathbb{R}\to\mathbb{R}$, $x\mapsto g(x)\mapsto f(g(x))$.
$$\frac{d f}{dx}\big(g(x_0)\big)=\frac{df}{dg}\big(g(x_0)\big)\cdot\frac{dg}{dx}(x_0)$$
**Esempio**: $(2x+3)^2\Rightarrow$ derivata $=2(2x+3)\cdot 2$.

### 5.2 Caso 1: $f:\mathbb{R}^N\to\mathbb{R}$, $g:\mathbb{R}\to\mathbb{R}^N$
$f\circ g:\mathbb{R}\to\mathbb{R}^N\to\mathbb{R}$, $g=(g_1,\dots,g_N)$.
$$\frac{d(f\circ g)}{dx}(x_0)=\sum_{i=1}^N\frac{\partial f}{\partial g_i}\big(g(x_0)\big)\cdot\Big(\frac{dg_i}{dx}(x_0)\Big)=\nabla_g f(g(x_0))\cdot\Big(\frac{dg}{dx}\Big)_{i=1}^N$$
(prodotto scalare).

### 5.3 Caso 2: $f:\mathbb{R}^N\to\mathbb{R}$, $g:\mathbb{R}^M\to\mathbb{R}^N$
$f\circ g:\mathbb{R}^M\to\mathbb{R}^N\to\mathbb{R}$.
$$\frac{\partial (f\circ g)}{\partial x_k}=\sum_{i=1}^N\frac{\partial f}{\partial g_i}\big(g(\underline{x}_0)\big)\cdot\frac{\partial g_i}{\partial x_k}(\underline{x}_0)$$
$$\nabla(f\circ g)=\Big(\frac{\partial(f\circ g)}{\partial x_1},\dots,\frac{\partial(f\circ g)}{\partial x_M}\Big)$$

### 5.4 Caso 3: $f:\mathbb{R}^N\to\mathbb{R}^K$, $g:\mathbb{R}^M\to\mathbb{R}^N$
$f\circ g:\mathbb{R}^M\to\mathbb{R}^N\to\mathbb{R}^K$ (Jacobiani composti — caso più generale).

---

## 6. Calcolo di $\nabla\mathcal{L}_2^{\text{SLP}}$ via Chain-Rule

### 6.1 Decomposizione
$$\mathcal{L}_2^{\text{SLP}}(W,\underline{b})=\frac{1}{2m}\sum_{i=1}^m\big\|\sigma(W^T\underline{x}^{(i)}+\underline{b})-\underline{y}^{(i)}\big\|^2$$
Quattro funzioni in cascata:
1. **Pre-attivazione**: $\underline{s}(W,\underline{b})=W^T\underline{x}+\underline{b}\in\mathbb{R}^M$.
2. **Attivazione**: $\sigma(\underline{s}(W,\underline{b}))$.
3. **Norma**: $\|\sigma(\underline{s})-\underline{y}\|$.
4. **Quadrato** (e media): $x\mapsto x^2$.

### 6.2 Chain-rule applicata
$$\nabla_\theta\mathcal{L}=\underbrace{\frac{\partial x^2}{\partial\|\cdot\|}}_{4}\cdot\underbrace{\frac{\partial\|\cdot\|}{\partial\sigma}}_{3}\cdot\underbrace{\frac{\partial\sigma}{\partial\underline{s}}}_{2}\cdot\underbrace{\frac{\partial\underline{s}}{\partial\theta}}_{1}$$
Si calcolano $\nabla_W\mathcal{L}$ e $\nabla_{\underline{b}}\mathcal{L}$ separatamente.

### 6.3 (1) Derivata della pre-attivazione $\underline{s}=W^T\underline{x}+\underline{b}$
La componente $j$-esima (neurone $j$):
$$s_j=w_{1j}x_1+w_{2j}x_2+\dots+w_{ij}x_i+\dots+w_{Nj}x_N+b_j$$
$$\boxed{\;\frac{\partial s_j}{\partial w_{ij}}=x_i\quad(k=j),\qquad \frac{\partial s_k}{\partial w_{ij}}=0\quad(k\ne j)\;}$$
$$\frac{\partial s_j}{\partial b_j}=1,\qquad \frac{\partial s_k}{\partial b_j}=0\ (k\ne j)$$

### 6.4 (2) Derivata dell'attivazione $\sigma(\underline{s})$
$\sigma:\mathbb{R}^M\to\mathbb{R}^M$ applicata componente per componente. $\sigma$ deve essere **derivabile**.
$$\frac{d\sigma}{d w_{ij}}(s_k)=0\quad (k\ne j)$$
$$\frac{d\sigma}{d w_{ij}}(s_j)=\frac{d\sigma}{d s_j}\cdot\frac{\partial s_j}{\partial w_{ij}}=\sigma'(s_j)\cdot x_i$$

### 6.5 (3) Derivata della norma $\|\cdot\|$
$f:\mathbb{R}^M\to\mathbb{R}$, $\underline{x}\mapsto\|\underline{x}\|=\sqrt{x_1^2+\dots+x_M^2}$:
$$\boxed{\;\frac{\partial \|\underline{x}\|}{\partial x_i}=\frac{x_i}{\|\underline{x}\|}\;}$$

### 6.6 Composizione finale (chain-rule, caso 2)
Per $\|\sigma(\underline{s})-\underline{y}\|:\mathbb{R}^{N\cdot M+M}\to\mathbb{R}^M\to\mathbb{R}^M\to\mathbb{R}$:
$$\frac{\partial f}{\partial w_{ij}}\big(\sigma(\underline{s})-\underline{y}\big)=\sum_{k=1}^M\frac{\partial f}{\partial \sigma(s_k)}\cdot\frac{\partial\sigma(s_k)}{\partial w_{ij}}$$
- Per $k\ne j$: $\dfrac{\partial\sigma(s_k)}{\partial w_{ij}}=0\Rightarrow$ termine nullo.
- Per $k=j$:
$$\frac{\partial f}{\partial w_{ij}}=\frac{\partial f(\sigma(\underline{s})-\underline{y})}{\partial \sigma}\cdot\sigma'(s_j)\cdot x_i=\frac{\sigma(s_j)-y_j}{\|\sigma(\underline{s})-\underline{y}\|}\cdot\sigma'(s_j)\cdot x_i$$

### 6.7 Risultato finale
$$\boxed{\;\frac{\partial\,\|\sigma(\underline{s})-\underline{y}\|}{\partial w_{ij}}=\frac{\sigma(s_j)-y_j}{\|\sigma(\underline{s})-\underline{y}\|}\cdot\sigma'(s_j)\cdot x_i\;}$$
(analogo per $b_j$, con $x_i\to 1$).

---

## 7. Sintesi Concettuale (utile a esame)

- **Apprendimento supervisionato** = **ottimizzazione** della loss sui parametri.
- **Loss** = misura aggregata dell'errore sul dataset (norma $L_1$ o quadrato della norma $L_2$).
- **Discesa del gradiente** sui parametri: $\theta_k=\theta_{k-1}-\eta\,\nabla_\theta\mathcal{L}$.
- **Giustificazione formale**: la direzione $-\nabla_\theta\mathcal{L}$ è l'unica scelta lineare in $\nabla\mathcal{L}$ che garantisce $d\mathcal{L}<0$, perché $d\mathcal{L}(-\eta\nabla\mathcal{L})=-\eta\|\nabla\mathcal{L}\|^2<0$.
- **Condizione su $\eta$**: piccolo per validità di $\Delta\mathcal{L}\approx d\mathcal{L}$, ma non nullo per progredire ($\eta\approx\varepsilon/\|\nabla\mathcal{L}\|$).
- **$\sigma$ differenziabile** rende il problema **ben condizionato**: piccole perturbazioni dei parametri producono piccole variazioni della loss $\Rightarrow$ il gradiente è informativo.
- **Chain-rule** permette il calcolo esplicito di $\nabla_\theta\mathcal{L}$ decomponendo la rete in pre-attivazione, attivazione, norma, quadrato.
- **Risultato chiave** per SLP: $\dfrac{\partial\mathcal{L}}{\partial w_{ij}}\propto(\sigma(s_j)-y_j)\cdot\sigma'(s_j)\cdot x_i$, base della **back-propagation** (Lezione 5).
