## Lezione 5 — Backpropagation e teorema di approssimazione universale

Obiettivo: calcolare in modo efficiente il gradiente $\nabla_\theta \mathcal{L}$ rispetto a tutti i parametri $\theta = (W^{(1)}, b^{(1)}, \ldots, W^{(L+1)}, b^{(L+1)})$ di una rete neurale, per poter applicare la discesa del gradiente.

---

## 1. Derivazione esplicita del gradiente per SLP (Single Layer Perceptron)

### 1.1 Setup

- Architettura: input $x \in \mathbb{R}^N$, output $y \in \mathbb{R}^M$, una sola matrice di pesi $W \in \mathbb{R}^{N \times M}$ e bias $b \in \mathbb{R}^M$.
- Pre-attivazione del neurone $j$: $s_j = \sum_{i=1}^{N} w_{ij} x_i + b_j$.
- Output del neurone $j$: $\sigma(s_j)$, con $\sigma$ funzione di attivazione (es. sigmoide, tanh).
- Loss $L_2$ su singolo esempio: $\mathcal{L} = \tfrac{1}{2}\,\| \sigma(s) - y \|^2$.
- Loss su dataset $D = \{(x^{(k)}, y^{*(k)})\}_{k=1}^{m}$, $|D|=m$:
$$\mathcal{L} = \frac{1}{2m}\sum_{k=1}^{m} \| \sigma(s^{(k)}) - y^{*(k)} \|^2.$$

### 1.2 Calcolo di $\partial \mathcal{L}/\partial w_{ij}$ per chain rule

Per un solo esempio (poi si media). Si parte dalla norma euclidea:
$$\frac{\partial}{\partial w_{ij}} \| \sigma(s) - y \| = \frac{\sigma(s_j) - y_j}{\| \sigma(s) - y \|} \cdot \sigma'(s_j) \cdot x_i.$$

Catena: $\| \sigma(s) - y \| \to \sigma(s_j) \to s_j \to w_{ij}$.
- $\partial \| \cdot \| / \partial \sigma(s_j) = (\sigma(s_j) - y_j)/\| \sigma(s) - y \|$.
- $\partial \sigma(s_j) / \partial s_j = \sigma'(s_j)$.
- $\partial s_j / \partial w_{ij} = x_i$ (gli altri termini $w_{kj}$, $k\neq i$, hanno derivata nulla).

Ultimo step: derivare il quadrato nella loss. Da $\partial\|\sigma(s)-y\|^2/\partial w_{ij} = 2\,\|\sigma(s)-y\| \cdot (\sigma(s_j)-y_j)/\|\sigma(s)-y\| \cdot \sigma'(s_j) \cdot x_i$. I fattori $\|\sigma(s)-y\|$ si semplificano e il $2$ cancella il $\tfrac{1}{2}$ della loss.

### 1.3 Equazioni finali SLP

$$\boxed{\;\frac{\partial \mathcal{L}}{\partial w_{ij}} = \frac{1}{m} \sum_{k=1}^{m} \underbrace{\big(\sigma(s_j^{(k)}) - y_j^{*(k)}\big) \cdot \sigma'(s_j^{(k)})}_{\text{errore sul neurone } j} \cdot x_i^{(k)}\;}$$

$$\boxed{\;\frac{\partial \mathcal{L}}{\partial b_j} = \frac{1}{m} \sum_{k=1}^{m} \big(\sigma(s_j^{(k)}) - y_j^{*(k)}\big) \cdot \sigma'(s_j^{(k)})\;}$$

Il termine $(\sigma(s_j) - y_j^*) \cdot \sigma'(s_j)$ si chiama errore sul neurone $j$ di output: confronta la predizione $\sigma(s_j)$ col target $y_j^*$ del dataset, modulato dalla pendenza $\sigma'$.

---

## 2. Gradiente per MLP a 1 strato nascosto (5 step)

### 2.1 Setup MLP a 2 layer

- Strato 1 (nascosto): $W^{(1)} \in \mathbb{R}^{N \times m_1}$, $b^{(1)} \in \mathbb{R}^{m_1}$, pre-attivazione $s_j^{(1)} = \sum_i w_{ij}^{(1)} x_i + b_j^{(1)}$.
- Strato 2 (output): $W^{(2)} \in \mathbb{R}^{m_1 \times M}$, $b^{(2)} \in \mathbb{R}^M$, pre-attivazione $s_k^{(2)} = \sum_{v=1}^{m_1} w_{vk}^{(2)} \cdot \sigma(s_v^{(1)}) + b_k^{(2)}$.
- Output: $y_k = \sigma(s_k^{(2)})$.

Per i pesi del secondo strato si applica direttamente il risultato SLP:
$$\frac{\partial \mathcal{L}}{\partial w_{ij}^{(2)}} = \frac{1}{m}\sum_{k=1}^{m} \big(\sigma(s_j^{(2)}) - y_j^{*(k)}\big)\cdot \sigma'(s_j^{(2)}) \cdot \sigma(s_i^{(1)}).$$

Per i pesi del primo strato $w_{ij}^{(1)}$ il calcolo richiede la chain rule completa.

### 2.2 I 5 step per $\partial \mathcal{L}/\partial w_{ij}^{(1)}$

**Step 1 — derivata di $s_j^{(1)}$ rispetto a $w_{ij}^{(1)}$:**
$$\frac{\partial s_j^{(1)}}{\partial w_{ij}^{(1)}} = x_i, \qquad \frac{\partial s_k^{(1)}}{\partial w_{ij}^{(1)}} = 0 \;\; (k \neq j).$$

**Step 2 — derivata di $\sigma(s_j^{(1)})$ via chain rule:**
$$\frac{d\sigma(s_j^{(1)})}{d w_{ij}^{(1)}} = \sigma'(s_j^{(1)}) \cdot x_i, \qquad \frac{d\sigma(s_k^{(1)})}{d w_{ij}^{(1)}} = 0 \;\; (k \neq j).$$

**Step 3 — derivata di $s_k^{(2)}$ rispetto a $w_{ij}^{(1)}$:** poiché $s_k^{(2)} = \sum_{v=1}^{m_1} w_{vk}^{(2)} \sigma(s_v^{(1)}) + b_k^{(2)}$,
$$\frac{\partial s_k^{(2)}}{\partial w_{ij}^{(1)}} = \sum_{v=1}^{m_1} w_{vk}^{(2)} \cdot \sigma'(s_v^{(1)}) \cdot \frac{\partial s_v^{(1)}}{\partial w_{ij}^{(1)}} = w_{jk}^{(2)} \cdot \sigma'(s_j^{(1)}) \cdot x_i,$$
poiché solo $v=j$ sopravvive.

**Step 4 — attivazione $\sigma(s_k^{(2)}) \rightsquigarrow y_k$:** chain rule $d\sigma/d w = (d\sigma/ds)\cdot(ds/dw)$:
$$\frac{d \sigma(s_k^{(2)})}{d w_{ij}^{(1)}} = \sigma'(s_k^{(2)}) \cdot w_{jk}^{(2)} \cdot \sigma'(s_j^{(1)}) \cdot x_i \qquad \forall k = 1,\ldots,M.$$

**Step 5 — derivata della norma $\|\sigma(s^{(2)}) - y\|$:** sommando su tutte le componenti $k$ dell'output,
$$\frac{\partial \|\sigma(s^{(2)}) - y\|}{\partial w_{ij}^{(1)}} = \sum_{k=1}^{M} \frac{\sigma(s_k^{(2)}) - y_k}{\|\sigma(s^{(2)}) - y\|} \cdot \sigma'(s_k^{(2)}) \cdot w_{jk}^{(2)} \cdot \sigma'(s_j^{(1)}) \cdot x_i.$$

### 2.3 Risultato finale (mediato sul dataset)

$$\boxed{\;\frac{\partial \mathcal{L}}{\partial w_{ij}^{(1)}} = \frac{1}{m}\sum_{k=1}^{m} \underbrace{\Bigg(\sum_{v=1}^{M} \underbrace{(\sigma(s_v^{(2)}) - y_v^{(k)})\,\sigma'(s_v^{(2)})}_{\text{errore neurone } v \text{ output}} \cdot w_{jv}^{(2)}\Bigg) \cdot \sigma'(s_j^{(1)})}_{\text{errore neurone interno } j\text{-esimo}} \cdot x_i^{(k)}\;}$$

L'errore sul neurone interno $j$ è la combinazione pesata (tramite $w_{jv}^{(2)}$) degli errori dei neuroni di output ai quali $j$ è connesso, modulata da $\sigma'(s_j^{(1)})$. Questo motiva la definizione ricorsiva degli errori.

---

## 3. Algoritmo di Backpropagation (forma generale)

### 3.1 Definizioni formali

**Errore sullo strato di output** $\delta^{(L+1)} \in \mathbb{R}^M$:
$$\boxed{\;\delta_k^{(L+1)} = \big(\underbrace{\sigma(s_k^{(L+1)})}_{\text{calcolato (forward)}} - \underbrace{y_k}_{\text{dataset}}\big) \cdot \sigma'(s_k^{(L+1)})\;}$$

**Errori sugli strati nascosti** $\delta^{(\ell)} \in \mathbb{R}^{m_\ell}$, ricorsione all'indietro:
$$\boxed{\;\delta_j^{(\ell)} = \sum_{k=1}^{m_{\ell+1}} \delta_k^{(\ell+1)} \cdot w_{jk}^{(\ell)} \cdot \sigma'(s_j^{(\ell)})\;}$$

(Da notare: $w_{jk}^{(\ell)}$ è il peso che collega il neurone $j$ dello strato $\ell$ al neurone $k$ dello strato $\ell+1$.)

### 3.2 Equazioni della backpropagation

$$\boxed{\;\frac{\partial \mathcal{L}}{\partial w_{ij}^{(\ell)}} = \frac{1}{m}\sum_{k=1}^{m} \delta_j^{(\ell)} \cdot \sigma\big(s_i^{(\ell-1)}\big)\;}$$

$$\boxed{\;\frac{\partial \mathcal{L}}{\partial b_j^{(\ell)}} = \frac{1}{m}\sum_{k=1}^{m} \delta_j^{(\ell)}\;}$$

Convenzione: se $\ell$ è il primo strato, $\sigma(s_i^{(0)}) := x_i$.

### 3.3 Sketch della dimostrazione (induttivo all'indietro)

- Caso base $\ell = L+1$: per la derivazione SLP, $\partial\mathcal{L}/\partial w_{ij}^{(L+1)} = \tfrac{1}{m}\sum (\sigma(s_j^{(L+1)})-y_j)\sigma'(s_j^{(L+1)}) \cdot \sigma(s_i^{(L)}) = \tfrac{1}{m}\sum \delta_j^{(L+1)} \sigma(s_i^{(L)})$.
- Passo induttivo: assunto che $\delta^{(\ell+1)}$ rappresenti correttamente l'errore propagato fino allo strato $\ell+1$, applicando chain rule attraverso $s_k^{(\ell+1)} = \sum_v w_{vk}^{(\ell)} \sigma(s_v^{(\ell)}) + b_k^{(\ell+1)}$ si ottiene esattamente la formula ricorsiva $\delta_j^{(\ell)} = \sum_k \delta_k^{(\ell+1)} w_{jk}^{(\ell)} \sigma'(s_j^{(\ell)})$, come visto al §2.

---

## 4. Algoritmo di addestramento di un MLP (pseudocodice)

### 4.1 Iperparametri
- $N_{\text{epoche}} \in \mathbb{N}$: numero di epoche.
- $\eta > 0$, $\eta \in \mathbb{R}$: learning rate (coefficiente di apprendimento).

### 4.2 Input
- Dataset $D_{\text{train}} = \{(x^{(1)}, y^{(1)}), \ldots, (x^{(m)}, y^{(m)})\}$ con $x^{(i)} \in \mathbb{R}^N$, $y^{(i)} \in \mathbb{R}^M$, $m = |D|$.
- Architettura: $L$ strati, dim. input $N$, dim. nascosti $m_1, \ldots, m_L$, dim. output $M$.

### 4.3 Pseudocodice

```
for ℓ = 1, 2, …, L+1:
    inizializza W^(ℓ), b^(ℓ) in modo casuale  (parametri θ_0)

for i = 1, …, N_epoche:
    for x^(k) ∈ D_train:

        # ---------- PASSO FORWARD ----------
        a_k^(0) = x^(k)                       # input activation
        for ℓ = 1, …, L+1:
            a_k^(ℓ) = σ( W^(ℓ)ᵀ · a_k^(ℓ-1) + b^(ℓ) )

        # ---------- PASSO BACKWARD ----------
        calcolare δ_k^(L+1)                    # errore output rispetto a y^(k)
        for ℓ = L, L-1, …, 1:
            calcolare δ_k^(ℓ)                  # ricorsione

    # ---------- AGGIORNAMENTO PARAMETRI θ_i ----------
    for ℓ = 1, …, L+1:
        W_i^(ℓ) = W_{i-1}^(ℓ) - η · (1/m) Σ_k a_k^(ℓ-1) · δ_k^(ℓ)
        b_i^(ℓ) = b_{i-1}^(ℓ) - η · (1/m) Σ_k δ_k^(ℓ)
```

Un'iterazione completa (forward + backward + update) è uno step di discesa del gradiente sul dataset intero.

---

## 5. Teorema di Approssimazione Universale

### 5.1 Enunciato

**Ipotesi:**
- $\sigma : \mathbb{R} \to \mathbb{R}$, $\sigma \in C^1(\mathbb{R})$, $\sigma$ monotona crescente (funzione di attivazione regolare, come la sigmoide).
- $f : K \subseteq \mathbb{R}^N \to \mathbb{R}^M$ con $K$ chiuso e limitato (compatto), $f \in C^0(K)$ (continua sul compatto).
- Fissato $\varepsilon > 0$.

**Tesi:** esistono
- $m_1 \in \mathbb{N}$ (numero di neuroni del primo strato),
- $W^{(1)} \in \mathbb{R}^{N \times m_1}$ e $W^{(2)} \in \mathbb{R}^{m_1 \times M}$ (matrici dei pesi),
- $b^{(1)} \in \mathbb{R}^{m_1}$ (vettore dei bias del primo strato),

tali che la funzione $F : \mathbb{R}^N \to \mathbb{R}^M$ realizzata da un MLP semplificato con un solo strato nascosto
$$\boxed{\;F(x) := W^{(2)\,T} \cdot \sigma\big(W^{(1)\,T} \cdot x + b^{(1)}\big)\;}$$
soddisfa
$$\boxed{\;\max_{x \in K} \|F(x) - f(x)\| < \varepsilon\;}$$

### 5.2 Interpretazione e nota cruciale

- Ogni funzione continua su un compatto può essere approssimata uniformemente, a meno di $\varepsilon$ piccolo a piacere, da un MLP a un solo strato nascosto sufficientemente "largo".
- Il teorema **NON è costruttivo**: garantisce l'esistenza dei parametri $(m_1, W^{(1)}, b^{(1)}, W^{(2)})$ ma non dice come trovarli né quanto grande deve essere $m_1$. La ricerca dei parametri è proprio il compito dell'addestramento (discesa del gradiente + backpropagation).
- Nella forma data manca il bias $b^{(2)}$ sull'output: la versione "semplificata" ne fa a meno, ma non cambia il risultato.
- L'aumento del numero di strati ($L > 1$) non aumenta la classe di funzioni rappresentabili (rimane sempre l'insieme delle continue su compatti), ma può ridurre drasticamente $m_1$ e migliorare la capacità di generalizzazione.

---

## 6. Riassunto operativo

- $\delta^{(L+1)}$ = errore puntuale predetto-target modulato da $\sigma'$.
- $\delta^{(\ell)}$ = combinazione lineare degli errori dello strato successivo, pesata per i pesi uscenti, modulata da $\sigma'$ del livello $\ell$.
- Le derivate dei pesi ($\partial\mathcal{L}/\partial w$) sono prodotti $\delta \cdot$ attivazione precedente; le derivate dei bias ($\partial\mathcal{L}/\partial b$) sono direttamente $\delta$.
- L'algoritmo di training si compone di tre fasi per ogni epoca: forward, backward (calcolo $\delta$), update con $\eta$.
- La giustificazione teorica (esistenza di una rete che approssima qualunque $f$ continua su compatto) è data dal teorema di approssimazione universale, ma non risolve il problema pratico della ricerca dei parametri.
