# Lezione 8 — CNN, Pooling, Backpropagation, RNN

> Riferimenti: `Lezione_8/Lezione 8.pdf`, `l8a.pdf`, `l8b.pdf` — Prof. Iotti, Fondamenti di IA, UniPR.
> Obiettivo: passare dalla convoluzione all'architettura CNN, definirne formalmente il blocco convoluzionale e il pooling, derivare la backpropagation (cross-correlation con kernel flippato; indicatrice del massimo per max-pool), introdurre regolarizzazione (dropout) e dati sequenziali (RNN). Cenni su modelli generativi.

---

## 1. Cross-correlation (correlazione incrociata)

### 1.1 Definizione

- Sia $x : \mathbb{R} \to \mathbb{R}$ segnale in input e $w : \mathbb{R} \to \mathbb{R}$ kernel.
- **Cross-correlation 1D**:
  $$(x \star w)(t) = \int_{\mathbb{R}} x(a)\, w(t+a)\, da.$$
- Relazione con la convoluzione (kernel **flippato** $w^-(t) := w(-t)$):
  $$(x \star w)(t) = (x * w^-)(-t).$$
- **Differenza cruciale dalla convoluzione**: nella cross-correlation **non** si "ribalta" il kernel; la convoluzione invece flippa $w$ (argomento $t-a$). Nelle CNN moderne la "convoluzione" implementata in libreria è in realtà una cross-correlation.

---

## 2. Architettura di una CNN

### 2.1 Idea

- **Dati a griglia**: immagini $\mathbb{R}^{H\times W \times c}$, segnali, video. La CNN sfrutta località e equivarianza alla traslazione (vedi Lezione 7).
- **Tensori (volumi)**: ogni layer è un tensore $h \times w \times d$ (altezza × larghezza × profondità $d$ = #canali).

### 2.2 Pipeline standard

$$\underbrace{x}_{\text{input}} \;\to\; \underbrace{\text{Conv} + \text{Pool}}_{\text{blocco}} \;\to\; \underbrace{\text{Conv} + \text{Pool}}_{\text{blocco}} \;\to\; \cdots \;\to\; \underbrace{\text{MLP}}_{\text{testa}} \;\to\; y$$

- Flusso dei tensori:
  $$I \in \mathbb{R}^{H\times W \times c} \;\xrightarrow{W^{(1)}, b^{(1)}}\; C \in \mathbb{R}^{h_1 \times w_1 \times \#\text{filtri}} \;\xrightarrow{W^{(2)}, b^{(2)}}\; P \in \mathbb{R}^{h_2 \times w_2 \times \#\text{filtri}} \;\to\; \cdots$$
- Le ultime feature map vengono "appiattite" e date in pasto a un MLP che produce l'output.

---

## 3. Blocco convoluzionale

### 3.1 Iperparametri

- **Depth** $d$: numero di filtri (= profondità dell'output).
- **Stride** $s$: passo con cui si sposta il filtro sull'input.
- **Zero-padding** $p$: spessore del bordo di zeri attorno all'input.
- **Kernel size** $m$: dimensione del filtro $m \times m$, con $m$ dispari.

### 3.2 Formula della dimensione di output

Per un blocco convoluzionale che riceve un input $H \times W$:

$$\boxed{\ h_1 \times w_1 \;=\; \frac{H \times W - m + 2p}{s} \;+\; 1\ }$$

(formula da applicare separatamente alle due dimensioni: $h_1 = (H - m + 2p)/s + 1$, $w_1 = (W - m + 2p)/s + 1$).

### 3.3 Slice e fibra

- **Slice $k$**: la sotto-matrice $h_1 \times w_1$ del tensore output ottenuta fissando la coordinata di profondità $k$ (è la $k$-esima feature map).
- **Fibra**: il vettore lungo la dimensione di profondità ottenuto fissando la posizione spaziale $(i,j)$.

### 3.4 Output del blocco convoluzionale

Per la slice $k$, posizione $(i,j)$:

$$C_{ij}^{k} \;=\; \sigma\!\left(W_k^{(1)} * \underline{x} \;+\; b^{(1)}\right) \;=\; \sigma\!\left(\sum_{c}\sum_{\ell}\sum_{m} w_{\ell m}^{(1,c,k)}\, x_{(i-\ell,\, j-m)}^{(c)} \;+\; b^{(1)}\right)$$

dove:
- $c$ scorre sui canali di input,
- $\ell, m$ scorrono sulle posizioni del filtro $m \times m$,
- $\sigma$ è una funzione di attivazione non lineare (ReLU, sigmoide, ...).

### 3.5 Pesi condivisi

- **Idea chiave**: lo stesso filtro $W_k^{(1)}$ è usato su **tutte le posizioni $(i,j)$** della slice $k$.
- Numero di parametri per filtro $m \times m$ (singolo canale): $m^2$. Esempio $m=3 \Rightarrow$ **9 parametri** + 1 bias.
- Confronto con MLP fully-connected su un'immagine $1000 \times 1000$:
  - MLP: ogni neurone del primo layer ha $10^6$ pesi $\Rightarrow$ milioni/miliardi di parametri.
  - CNN con $K$ filtri $3\times 3$: $9K$ parametri (+ bias) totali, indipendentemente dalle dimensioni dell'immagine.
- Consente **equivarianza alla traslazione** (l'attivazione si sposta con l'input — vedi Lezione 7) e drastica riduzione del numero di parametri.

---

## 4. Backpropagation nel blocco convoluzionale

### 4.1 Setup

- Loss $L_2$ (MSE): $\mathcal{L}$.
- Per un layer $(\ell)$ totalmente connesso si ha $\dfrac{\partial \mathcal{L}}{\partial w_{ij}^{(\ell)}} = \delta_j^{(\ell)} \cdot x_i$, con
  $$\delta_j^{(\ell)} \;=\; \sum_{v=1}^{m_\ell} \delta_v^{(\ell+1)}\, w_{jv}^{(\ell+1)} \cdot \frac{d\sigma}{d s_j^{(\ell)}}\!\left(s_j^{(\ell)}\right).$$

### 4.2 Cosa cambia nel layer convoluzionale

- Pre-attivazione nella posizione $(h,k)$:
  $$s_{j}^{(\ell)}\Big|_{h,k} \;=\; \big(W^{(\ell)} * \underline{x} + b^{(\ell)}\big)_{h,k}.$$
- Quindi
  $$\frac{d\sigma}{d s_{h,k}^{(\ell)}}\!\left(s_{h,k}^{(\ell)}\right) \;=\; \sum_{h}\sum_{k} \frac{d\sigma}{d s}\!\big(W^{(\ell)} * \underline{x} + b^{(\ell)}\big)_{h,k}\, \cdot\, x_{(i-h,\, j-k)}^{(c)}\;=\;\frac{d\sigma}{ds}\!\big(W^{(\ell)} * \underline{x} + b^{(\ell)}\big) \;\star\; \underline{x}.$$
- **Cross-correlation con il kernel "flippato"**: la derivata rispetto ai pesi convoluzionali è una cross-correlation tra la derivata locale dell'attivazione e l'input.

### 4.3 Formula finale (gradiente sui pesi)

$$\boxed{\ \frac{\partial \mathcal{L}}{\partial w_{ij}^{(\ell)}} \;=\; \sum_{v=1}^{m_\ell} \delta_v^{(\ell+1)}\, w_{jv}^{(\ell+1)} \cdot \left(\frac{d\sigma}{ds} \,\star\, \underline{x}\right)_{i}\ }$$

- È **implementata** come una cross-correlation: ecco perché in pratica la "convoluzione" delle CNN è realmente una correlazione incrociata (o equivalentemente una convoluzione con kernel pre-flippato).

---

## 5. Layer di pooling

### 5.1 Concetto

- Filtro **non lineare** che riduce le dimensioni spaziali aggregando regioni.
- **Iperparametri**: dimensione kernel $m \times m$ (con $m$ dispari) e stride $s$.

### 5.2 Max-pooling

- Definizione:
  $$x_{ij} \;\longmapsto\; \max\!\big(x_{i+m,\, j+m}\big) \;=\; p_{ij}^{k}.$$
- È robusto a piccole traslazioni: due input lievemente diversi possono produrre lo stesso output (es. `1,10,3,1,2 → 10,10,3` e `3,1,10,3,1 → 10,10,10`).

### 5.3 Average pooling

- Stessa idea ma con la media:
  $$p_{ij}^{k} \;=\; \frac{1}{m^2}\sum_{(h,k')\in\text{finestra}} x_{h,k'}.$$
- È **lineare**, differenziabile ovunque (non ha la patologia del max).

### 5.4 Backpropagation in max-pooling

- **Problema**: la funzione $\max$ **non è differenziabile** ovunque.
- Convenzione: gli input **non massimi** non contribuiscono al gradiente ($\nabla \mathcal{L} = 0$), il valore massimo $p_{ij}^{k}$ viene "riportato com'è" tramite $f(x) = x \Rightarrow f'(x) = 1$.
- Formalmente, nel calcolo di $\delta_j^{(\ell)}$ la derivata $\dfrac{d\sigma}{ds_j}(s_j)$ è sostituita dall'**indicatrice del massimo**:
  $$\delta_j^{(\ell)} \;=\; \sum_{v=1}^{m_\ell} \delta_v^{(\ell+1)}\, w_{jv}^{(\ell+1)} \cdot \mathbf{1}_{\{s_j = p_{ij}^k\}}.$$
- Cioè $=1$ solo se $s_j$ è il massimo della finestra, $=0$ altrimenti. Solo il neurone "vincitore" propaga il segnale di errore.

---

## 6. Dropout (regolarizzazione)

- **Idea**: durante il training, ogni neurone viene "spento" con probabilità $p$ (output forzato a 0), in modo indipendente per ogni mini-batch.
- **Motivazione**: impedisce che la rete si affidi a specifici neuroni (co-adaptation), forzando la ridondanza delle feature → previene overfitting.
- A inferenza: tutti i neuroni sono attivi; gli output vengono riscalati di un fattore $(1-p)$ per compensare.

---

## 7. Reti Neurali Ricorrenti (RNN)

### 7.1 Motivazione

- MLP: input $\underline{x} \in \mathbb{R}^N$ con $N$ **fissato**.
- CNN: input $I \in \mathbb{R}^{H\times W \times c}$ con $H,W,c$ **fissati**.
- **Dati sequenziali** (musica, video, testo, serie temporali): la dimensione $t$ è **variabile**. Servono cicli nel grafo di calcolo.

### 7.2 Tipi di task

- **Speech synthesis**: input/output sequenziali.
- **Image captioning**: output sequenziale.
- **Generazione di testo**: input/output sequenziali (e.g. LM).

### 7.3 Cella ricorrente (formula)

Per ogni passo $t$ (con stato iniziale $\underline{y}(-1) = \underline{0}$):

$$\boxed{\ \underline{y}(t) \;=\; \sigma\!\big(W \cdot \underline{x}(t) \;+\; \widehat{W}\cdot \underline{y}(t-1) \;+\; \underline{b}\big)\ }$$

dove:
- $W$: pesi sull'input corrente,
- $\widehat{W}$: pesi sullo stato precedente,
- $\underline{b}$: bias.

### 7.4 Unrolling temporale

$$\underline{0} \to f \xrightarrow{\underline{x}(0)} \underline{y}(0) \to f \xrightarrow{\underline{x}(1)} \underline{y}(1) \to f \xrightarrow{\underline{x}(2)} \cdots \to f \xrightarrow{\underline{x}(m)} \underline{y}(m).$$

- A ogni $t$ fissato, $\underline{x}(t), \underline{y}(t) \in \mathbb{R}^N$ con dimensione finita; la sequenza è di lunghezza arbitraria.
- Backprop = **Backpropagation Through Time (BPTT)**: si srotola la rete e si applica backprop come a una rete profonda.

### 7.5 Problema del long-range

- Su sequenze lunghe i gradienti tendono a **svanire** (vanishing) o **esplodere** (exploding) attraversando molti passi temporali.
- Conseguenza: la RNN "vanilla" fatica a catturare dipendenze a lungo termine.
- Soluzioni (cenni): LSTM, GRU, attention/Transformer.

---

## 8. Cenni: variabili latenti, generative, NLP

### 8.1 Modelli probabilistici e likelihood

- Sia $p_\theta(\underline{x})$ un modello con parametri $\theta$. Dato un dataset $\{x^{(i)}\}_{i=1}^n$, si massimizza la **likelihood**
  $$\mathcal{L}(\theta) = \prod_i p_\theta(x^{(i)}) \quad \Longleftrightarrow \quad \max_\theta \sum_i \log p_\theta(x^{(i)}) \quad (\text{log-likelihood}).$$
- **Variabili latenti** $z$: introducono una sorgente di variabilità non osservata, $p_\theta(x) = \int p_\theta(x|z)\,p(z)\,dz$ (VAE, modelli generativi).

### 8.2 NLP / Language Modeling

- Un LM stima $p(w_t \mid w_{1:t-1})$. Implementabile con RNN, LSTM, Transformer.
- **Softmax** sull'ultimo livello per ottenere una distribuzione su un vocabolario di taglia $V$:
  $$\text{softmax}(\underline{z})_i \;=\; \frac{e^{z_i}}{\sum_{j=1}^V e^{z_j}}.$$
- **Cross-entropy** loss per classificazione/LM:
  $$\mathcal{L}_{CE} = -\sum_i y_i \log \hat y_i,$$
  dove $\underline{y}$ è la label one-hot e $\hat{\underline{y}}$ la distribuzione predetta.

### 8.3 GAN (cenni)

- Due reti: **generatore** $G$ (mappa rumore $z \sim p_z$ in dati sintetici) e **discriminatore** $D$ (distingue reale da finto). Gioco minimax:
  $$\min_G \max_D \; \mathbb{E}_{x\sim p_{\text{data}}}[\log D(x)] + \mathbb{E}_{z\sim p_z}[\log(1 - D(G(z)))].$$
- All'equilibrio $G$ produce campioni indistinguibili dal training set.

---

## 9. Sintesi — checklist d'esame

- [ ] Definizione di cross-correlation e relazione $(x \star w)(t) = (x * w^-)(-t)$.
- [ ] Architettura tipo CNN: Conv + Pool $\times k$ + MLP.
- [ ] Iperparametri: $d, s, p, m$ e formula $h_1 = (H - m + 2p)/s + 1$.
- [ ] Definizione di slice e fibra di un tensore.
- [ ] Formula esplicita $C_{ij}^k = \sigma\big(\sum_c \sum_\ell \sum_m w_{\ell m}\, x_{i-\ell, j-m}^{(c)} + b\big)$.
- [ ] Argomento dei **pesi condivisi**: $m^2$ parametri/filtro indipendenti dalle dimensioni dell'immagine, vs. milioni/miliardi in MLP fully-connected.
- [ ] Backprop nel blocco conv: $\partial \mathcal{L}/\partial w_{ij}^{(\ell)} = \sum_v \delta_v^{(\ell+1)} w_{jv}^{(\ell+1)} \cdot (d\sigma/ds \star \underline{x})_i$ — implementata come **cross-correlation** col kernel flippato.
- [ ] Max-pooling: definizione, **non differenziabile**; backprop tramite indicatrice $\mathbf{1}_{\{s_j = p_{ij}^k\}}$ (solo il "vincitore" riceve gradiente).
- [ ] Average pooling come alternativa lineare e differenziabile.
- [ ] Dropout: cosa fa e perché regolarizza.
- [ ] RNN: formula $\underline{y}(t) = \sigma(W\underline{x}(t) + \widehat{W}\underline{y}(t-1) + \underline{b})$, unrolling temporale con stato iniziale $\underline{0}$, problema del long-range (vanishing/exploding).
- [ ] Cenni su variabili latenti, log-likelihood, softmax, cross-entropy, GAN.
