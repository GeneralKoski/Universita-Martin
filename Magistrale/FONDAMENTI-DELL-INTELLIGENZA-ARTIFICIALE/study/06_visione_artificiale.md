## Lezione 6 — Visione Artificiale (Computer Vision)

Obiettivo della Computer Vision: creare un modello del mondo reale a partire da immagini bidimensionali (image processing). Si possono trattare più immagini (ricostruzione 3D), immagini fuori dallo spettro visibile, immagini statiche o video.

---

## 1. Definizione formale di immagine

**Def. (immagine):** un'immagine è una funzione
$$f : \mathbb{R}^2 \to C,$$
dove $C$ è lo **spazio colorimetrico**, $C \subseteq \mathbb{R}^3$ oppure $C \subseteq \mathbb{R}^4$.

### 1.1 Pipeline di Computer Vision

- **Basso livello (1):** acquisizione (fotocamere, ottiche, illuminazione, calibrazione) $\to$ pre-processing $\to$ feature extraction (descrizione simbolica con etichette non semantiche, es. coordinate di estremi di segmenti) $\to$ segmentazione (partizionamento non semantico).
- **Alto livello (2):** recognition (caratteristiche generali $\to$ conoscenza, es. "oggetto circolare"), identification (istanziare la conoscenza, "è una pallina da tennis"), detection (bounding box, mask, "la pallina si sta muovendo"). Il sistema infine deve prendere una **decisione**.

---

## 2. Digitalizzazione: campionamento e quantizzazione

Da $f:\mathbb{R}^2 \to C$ si passa a un'immagine digitale tramite due processi.

### 2.1 Campionamento

- Decompone l'immagine in **pixel** creando una griglia di dimensione $H \times W$ = **risoluzione**.
- Si seleziona il valore di $f$ sui nodi della griglia.

### 2.2 Quantizzazione

Dipende da $C$. Spazi colorimetrici più comuni:

- **RGB** $\subseteq \mathbb{R}^3$: Rosso, Verde, Blu (colori primari additivi).
- **HSV** $\subseteq \mathbb{R}^3$: Hue (tonalità), Saturation (saturazione), Value (luminosità). Comodo per ragionamenti percettivi sulla tonalità.
- **CMYK** $\subseteq \mathbb{R}^4$: Cyan, Magenta, Yellow, blacK. Utilizzato in stampa (modello sottrattivo).

Due parametri:
- $N_B$ = numero di bit per pixel.
- $N_C$ = numero di colori da rappresentare.

Vincolo: $2^{N_B} \geq N_C \iff N_B \geq \log_2 N_C \iff N_B = \lceil \log_2 N_C \rceil$.

### 2.3 Esempio: codifica TrueColor (RGB 24 bit)

- 8 bit per Rosso (0–255), 8 bit per Verde (0–255), 8 bit per Blu (0–255).
- $N_B = 24 \Rightarrow 2^{24} \approx 16$ milioni di colori.
- Immagine digitalizzata = 3 matrici $R, G, B \in \mathbb{R}^{H \times W}$.
- Proiettando sulla diagonale del cubo RGB ($R=G=B$) si ottiene un'immagine $\tilde f : \mathbb{R}^2 \to \mathbb{R}$ in **scala di grigi**.

### 2.4 Tensori

**Def. (tensore):** applicazione multi-lineare a valori in $\mathbb{R}$:
$$T : \underbrace{V \times \cdots \times V}_{k\text{ volte}} \times \underbrace{V^* \times \cdots \times V^*}_{h\text{ volte}} \to \mathbb{R},$$
con $V$ spazio vettoriale e $V^* = \{ f : V \to \mathbb{R}\;\text{lineari}\}$ il duale.

- Esempio: matrice $M \in \mathbb{R}^{H \times W}$ è un tensore $M : V \times V \to \mathbb{R}$, $(i,j) \mapsto m_{ij}$, ossia $M \in V^* \times V^*$.
- Tensore $T : V \times (V^* \times V^*) \to \mathbb{R}$, $(i,j,k) \mapsto T^i_{jk}$: l'indice $i$ è il **canale**, $j,k$ le coordinate del pixel.

**Def. (immagine digitalizzata in TrueColor):** un tensore
$$\boxed{\; I : C \times (H^* \times W^*) \to \mathbb{R}, \qquad C = \{R,G,B\}\;}$$

### 2.5 Conversioni a scala di grigi

- **Immagine luminanza** (formula percettiva):
$$\boxed{\; L := 0{,}299 \cdot R + 0{,}587 \cdot G + 0{,}114 \cdot B\;}$$
- **Immagine media:** $M := (R + G + B)/3$.

---

## 3. Operatori puntuali (point operators)

Operano su un singolo pixel: $L_{ij} \mapsto $ nuovo valore. Implementazione efficiente con **lookup-table** (LUT, colormap): array indicizzato $0 \div N_\ell$ con valori $0 \div N_\ell$, costo $O(1)$.

Notazione: $L \in \mathbb{R}^{H \times W}$ immagine in scala di grigi a livelli $0 \div N_\ell$, $L_{ij}$ intensità del pixel in posizione $(i,j)$.

### 3.1 Inversione dei livelli di grigio

- Continuo: $i(t) = N_\ell - t$, applicato come $i(f(x)) = N_\ell - f(x)$.
- Discreto: $\boxed{\; I_{ij} = N_\ell - L_{ij} \;}$ per $i=1,\ldots,H,\;j=1,\ldots,W$.
- Effetto: produce il negativo.

### 3.2 Compressione logaritmica

- Espande i livelli bassi (scuri) e comprime i livelli alti (chiari).
- Continuo: $\ell(t) = \dfrac{1}{1+N_\ell} \log(1 + t)$.
- Discreto:
$$\boxed{\; y_{ij} = \frac{1}{1 + N_\ell} \log(1 + L_{ij})\;}$$

(Sulle slide compare anche la forma normalizzata $\log(1+L_{ij})/\log(1+N_\ell)$, equivalente a meno di costante.)

### 3.3 Correzione gamma (compressione di potenza)

Parametro $\gamma > 0$, $\gamma \in \mathbb{R}$.

- Continuo: $p(t) = N_\ell^{1-\gamma} \cdot t^\gamma$.
- Discreto:
$$\boxed{\; P_{ij} = N_\ell^{1-\gamma} \cdot L_{ij}^{\gamma}\;}$$

Discussione del parametro:
- $\gamma \in (0, 1)$: comportamento simile alla compressione logaritmica (espande gli scuri, comprime i chiari).
- $\gamma = 1$: identità ($P_{ij} = L_{ij}$).
- $\gamma > 1$: comprime gli scuri, espande i chiari.

### 3.4 Espansione/contrast stretching rispetto a soglia $T$

- Continuo:
$$y(t) = \begin{cases} 0 & \text{se } t < T \\ N_\ell \cdot \dfrac{t - T}{N_\ell - T} & \text{se } t \geq T \end{cases}$$
- Discreto:
$$\boxed{\; y_{ij} = \begin{cases} 0 & \text{se } L_{ij} < T \\ N_\ell \cdot \dfrac{L_{ij} - T}{N_\ell - T} & \text{se } L_{ij} \geq T \end{cases}\;}$$

Tutti i pixel sotto soglia diventano neri, quelli sopra vengono mappati linearmente sull'intero intervallo $[0, N_\ell]$.

### 3.5 Istogramma e equalizzazione

**Def. (istogramma dei livelli di grigio):** funzione
$$h : \{0, 1, \ldots, 2^{N_B} - 1\} \to \mathbb{N}, \qquad h(\ell) = \big| \{ L_{ij} = \ell, \; i=1,\ldots,H, \; j=1,\ldots,W\} \big|.$$

Conta il numero di pixel di luminanza $\ell$. Trasformando l'istogramma (es. equalizzazione) si ottiene $\hat h$ corrispondente alla nuova mappatura. Applicazione tipica: stima area di oggetti chiari con soglia $T$:
$$t(\ell) = |\{h(\ell) \geq T\}|, \quad \text{area} = \sum_{\ell=0}^{2^{N_B}-1} t(\ell).$$

---

## 4. Operatori locali e differenziazione spaziale

Gli operatori locali agiscono su un pixel + il suo **vicinato** (sotto-matrice quadrata di dimensione $m$ dispari, tipicamente $3 \times 3$). Tipologie:
- **Sharpening**: estrazione contorni (edges), nitidezza.
- **Smoothing**: sfocatura, riduzione rumore.

Concetto chiave (sharpening): un edge è un cambio brusco di intensità. La derivata prima ha **rampe** ai bordi, la derivata seconda ha "attacco" delle rampe (zero-crossing). Il problema è: cosa significa $\nabla I$ se $I$ è digitale? Soluzione: **approssimazione tramite polinomi di Taylor**.

### 4.1 Sviluppo di Taylor a una variabile (richiamo)

Se $f \in C^k(\mathbb{R})$, $x_0 \in \mathbb{R}$, $x \in B(x_0, r)$:
$$f(x) = \sum_{i=0}^{k} \frac{f^{(i)}(x_0)}{i!}\,(x - x_0)^i + R_k(x)\,(x - x_0)^k, \qquad \lim_{x \to x_0} R_k(x) = 0.$$

### 4.2 Sviluppo di Taylor multi-indice

**Def. (multi-indice):** $\alpha = (\alpha_1, \alpha_2, \ldots, \alpha_N) \in \mathbb{N}^N$.
- $|\alpha| = \alpha_1 + \alpha_2 + \cdots + \alpha_N$ (lunghezza).
- $\alpha! = \alpha_1! \cdot \alpha_2! \cdots \alpha_N!$ (fattoriale).
- $(x - x_0)^\alpha = (x_1 - x_{0,1})^{\alpha_1} \cdots (x_N - x_{0,N})^{\alpha_N}$.
- Derivata di ordine $\alpha$:
$$\partial^\alpha f = \frac{\partial^{|\alpha|} f}{\partial x_1^{\alpha_1} \partial x_2^{\alpha_2} \cdots \partial x_N^{\alpha_N}}.$$

**Teorema di Taylor multivariato:** se $f : \mathbb{R}^N \to \mathbb{R}$, $f \in C^k(A)$ con $A$ aperto, $x_0 \in A$, $x \in B(x_0, r)$, allora
$$\boxed{\; f(x) = \sum_{|\alpha| \leq k} \frac{\partial^\alpha f(x_0)}{\alpha!} \cdot (x - x_0)^\alpha + \sum_{|\alpha| = k} R_\alpha(x)\,(x-x_0)^\alpha,\;}$$
con $\lim_{x \to x_0} R_\alpha(x) = 0$.

### 4.3 Esempio: $f(x,y) = x^2 + y e^x$, $x_0 = (0,0)$, $k = 2$

Derivate parziali nei multi-indici $\alpha \in \{(0,0),(1,0),(0,1),(1,1),(2,0),(0,2)\}$:
- $\partial f/\partial x = 2x + ye^x \Rightarrow (1,0)$ in $(0,0)$: $0$.
- $\partial f/\partial y = e^x \Rightarrow (0,1)$ in $(0,0)$: $1$.
- $\partial^2 f/\partial x^2 = 2 + ye^x \Rightarrow (2,0)$ in $(0,0)$: $2$.
- $\partial^2 f/\partial y^2 = 0 \Rightarrow (0,2)$: $0$.
- $\partial^2 f/(\partial x\,\partial y) = e^x \Rightarrow (1,1)$ in $(0,0)$: $1$.

$$f(x,y) \cong 0 + 0 \cdot x + 1 \cdot y + \frac{2}{2!\,0!}\,x^2 + \frac{0}{0!\,2!}\,y^2 + 2 \cdot \frac{1}{1!\,1!}\, xy = y + 2xy + x^2$$

(intorno a $(0,0)$, $k=2$).

---

## 5. Filtro di Sobel (operatore I ordine, sharpening)

Maschera $M \in \mathbb{R}^{3 \times 3}$, dimensione dispari $m=3$.

### 5.1 Setup di Taylor I ordine sull'immagine

Pixel centrale $z_0 = (x,y)$, intorno $z = (x+h, y+k)$ con $h,k \in \{-1, 0, 1\}$. Sviluppo I ordine di $f : \mathbb{R}^2 \to C$:
$$f(x+h, y+k) \cong f(x,y) + \frac{\partial f}{\partial x}(x,y) \cdot h + \frac{\partial f}{\partial y}(x,y) \cdot k.$$

### 5.2 Combinazioni di $h, k$ per stimare le derivate

Caso $h=0$ (direzione orizzontale, derivata rispetto a $y$):
- $k=-1$: $f(x, y-1) \cong f(x,y) - \partial f/\partial y$.
- $k=+1$: $f(x, y+1) \cong f(x,y) + \partial f/\partial y$.
- Sottraendo: $\dfrac{\partial f}{\partial y}(x,y) \cong \dfrac{f(x, y+1) - f(x, y-1)}{2}$.

Caso $k=0$ (direzione verticale, derivata rispetto a $x$):
- $h=-1$: $f(x-1, y) \cong f(x,y) - \partial f/\partial x$.
- $h=+1$: $f(x+1, y) \cong f(x,y) + \partial f/\partial x$.
- Sottraendo: $\dfrac{\partial f}{\partial x}(x,y) \cong \dfrac{f(x+1, y) - f(x-1, y)}{2}$.

Diagonali (combinazioni $h=\pm 1, k=\pm 1$):
- $h=k=1$: $f(x+1, y+1) \cong f(x,y) + \partial f/\partial x + \partial f/\partial y$.
- $h=k=-1$: $f(x-1, y-1) \cong f(x,y) - \partial f/\partial x - \partial f/\partial y$.
- Sottrazione (1): $\partial f/\partial x + \partial f/\partial y \cong \big(f(x+1, y+1) - f(x-1, y-1)\big)/2$.
- $h=+1, k=-1$ e $h=-1, k=+1$: per simmetria sottrazione (2): $\partial f/\partial x - \partial f/\partial y \cong \big(f(x+1, y-1) - f(x-1, y+1)\big)/2$.

Sommando (1) + (2) e dividendo per 4:
$$\frac{\partial f}{\partial x}(x,y) \cong \frac{f(x+1, y+1) + f(x+1, y-1) - f(x-1, y-1) - f(x-1, y+1)}{4}.$$

### 5.3 Maschera della derivata orizzontale e verticale

Combinando il contributo "verticale" (peso 2 sui pixel $(x\pm 1, y)$) e i contributi diagonali (peso 1 sui $(x\pm 1, y\pm 1)$), dividendo per 4 si ottiene la **maschera di Sobel** $M_x$ per la derivata $\partial f/\partial x$:
$$\boxed{\; M_x = \begin{pmatrix} -1 & -2 & -1 \\ 0 & 0 & 0 \\ 1 & 2 & 1 \end{pmatrix} \;}$$

Analogamente, per simmetria, la maschera per $\partial f/\partial y$:
$$\boxed{\; M_y = \begin{pmatrix} -1 & 0 & 1 \\ -2 & 0 & 2 \\ -1 & 0 & 1 \end{pmatrix} = M_x^{\,T}.\;}$$

### 5.4 Convoluzione e filtro gradiente

Sia $L \in \mathbb{R}^{H \times W}$ l'immagine luminanza:
- $L_x = L * M_x$ approssima $\partial L/\partial x$.
- $L_y = L * M_y$ approssima $\partial L/\partial y$.

Gradiente: $\nabla L = (\partial L/\partial x, \partial L/\partial y) \cong (L_x, L_y)$.

Modi per ottenere un'immagine "edge" da $\nabla L$:
- Norma euclidea: $\|\nabla L\| = \sqrt{(\partial L/\partial x)^2 + (\partial L/\partial y)^2}$.
- **Filtro gradiente di Sobel** (più economico):
$$\boxed{\; G_L = |L_x| + |L_y|\;}$$

### 5.5 Problema del bordo

I pixel sul bordo non hanno tutti i 9 vicini necessari per la maschera $3 \times 3$. Possibili soluzioni:
- **Zero-padding**: riempire il bordo con zeri.
- **Shrink**: ridurre l'immagine output da $H \times W$ a $(H-2) \times (W-2)$ (per maschera $3\times 3$).
- **Extend**: estendere l'intensità dei pixel del bordo (replica).

Per raffinare la ricerca degli edge oltre Sobel: **Canny Edge Detector** (vedi materiale di approfondimento).

---

## 6. Filtro Laplaciano (operatore II ordine, sharpening)

### 6.1 Definizione

**Def. (Laplaciano)** di $f : \mathbb{R}^2 \to \mathbb{R}$, $f \in C^2(\mathbb{R}^2)$:
$$\boxed{\; \nabla^2 f := \frac{\partial^2 f}{\partial x^2} + \frac{\partial^2 f}{\partial y^2}\;}$$

**Attenzione:** $\nabla^2 f \neq (\nabla f)^2$. Il primo è la somma delle derivate seconde pure (uno scalare), il secondo sarebbe la norma quadra del gradiente.

### 6.2 Approssimazione di II ordine via Taylor

Sviluppo II ordine in $z_0 = (x,y)$, $z = (x+h, y+k)$:
$$f(x+h, y+k) \cong f(x,y) + \frac{\partial f}{\partial x}h + \frac{\partial f}{\partial y}k + \frac{1}{2}\frac{\partial^2 f}{\partial x^2}h^2 + \frac{1}{2}\frac{\partial^2 f}{\partial y^2}k^2 + \frac{\partial^2 f}{\partial x\,\partial y}\,h\,k.$$

Con $h \in \{-1, 0, 1\}$, $k \in \{-1, 0, 1\}$:
- $(h=1, k=0)$: $f(x+1, y) \cong f + \partial_x f + \tfrac{1}{2}\partial_x^2 f$.
- $(h=-1, k=0)$: $f(x-1, y) \cong f - \partial_x f + \tfrac{1}{2}\partial_x^2 f$.
- Sommando: $f(x+1, y) + f(x-1, y) \cong 2 f(x,y) + \partial_x^2 f$.

$$\boxed{\; \frac{\partial^2 f}{\partial x^2}(x,y) \cong f(x-1, y) - 2 f(x,y) + f(x+1, y)\;}$$

Analogamente:
- $(h=0, k=\pm 1)$ e somma: $f(x, y-1) + f(x, y+1) \cong 2 f(x,y) + \partial_y^2 f$.

$$\boxed{\; \frac{\partial^2 f}{\partial y^2}(x,y) \cong f(x, y-1) - 2 f(x,y) + f(x, y+1)\;}$$

### 6.3 Maschere

$$M_{xx} = \begin{pmatrix} 0 & 1 & 0 \\ 0 & -2 & 0 \\ 0 & 1 & 0 \end{pmatrix}, \qquad M_{yy} = \begin{pmatrix} 0 & 0 & 0 \\ 1 & -2 & 1 \\ 0 & 0 & 0 \end{pmatrix}.$$

Sommando (linearità della convoluzione):
$$\boxed{\; M_{\nabla^2} = M_{xx} + M_{yy} = \begin{pmatrix} 0 & 1 & 0 \\ 1 & -4 & 1 \\ 0 & 1 & 0 \end{pmatrix}\;}$$

E si calcola $\nabla^2 L = L * (M_{xx} + M_{yy}) = L * M_{\nabla^2}$.

---

## 7. Filtri di smoothing (riduzione rumore)

Considerano una sezione 1D dei pixel $(\ldots, i-2, i-1, i, i+1, i+2, \ldots)$ con un picco di rumore in $i,j$. Tipologie:
1. Filtro media (lineare).
2. Filtro massimo (non lineare).
3. Filtro minimo (non lineare).
4. Filtro mediano (non lineare).

### 7.1 Filtro media

Dimensione $m$ dispari, $m \in \mathbb{N}$:
$$M_a = \begin{pmatrix} 1/m^2 & 1/m^2 & \cdots \\ \vdots & & \\ & & 1/m^2 \end{pmatrix} \in \mathbb{R}^{m \times m}.$$

Es. $M_3 = \dfrac{1}{9}\begin{pmatrix}1&1&1\\1&1&1\\1&1&1\end{pmatrix}$. È un filtro **lineare**: convoluzione standard.

### 7.2 Filtri non lineari

Il pixel $(i,j)$ viene sostituito con:
- **Max**: il massimo dei pixel del vicinato.
- **Min**: il minimo dei pixel del vicinato.
- **Mediano**: il valore mediano del vicinato (ottimo per rumore impulsivo "salt & pepper").

Non si esprimono come convoluzione perché non sono lineari.

### 7.3 Filtro gaussiano (lineare, smoothing)

Funzione gaussiana 2D con $\mu = 0$, $\sigma = 1$:
$$f(x, y) = \frac{1}{2\pi\sigma^2}\,e^{-(x^2 + y^2)/(2\sigma^2)}.$$

Discretizzata, con $\sigma = 1$:
$$\boxed{\; M_{ij} = \frac{1}{2\pi}\,e^{-(i^2 + j^2)/2}\;}$$

dove $M \in \mathbb{R}^{m \times m}$ con $m$ dispari, $i,j$ centrati nel pixel centrale. Il filtro pesa di più i pixel vicini al centro e meno quelli lontani; è lineare (convoluzione).

---

## 8. Convoluzione discreta

Sia $L \in \mathbb{R}^{H \times W}$ immagine, $M \in \mathbb{R}^{m \times m}$ maschera con $m$ dispari, $r = (m-1)/2$. Si considera il vicinato del pixel $(i,j)$:
$$V_{(i,j)} = \begin{pmatrix} L_{i-1,j-1} & L_{i,j-1} & L_{i+1,j-1} \\ L_{i-1,j} & L_{i,j} & L_{i+1,j} \\ L_{i-1,j+1} & L_{i,j+1} & L_{i+1,j+1} \end{pmatrix}.$$

Il nuovo valore in $(i,j)$ del risultato $L * M$:
$$\boxed{\; (L * M)_{ij} = \sum_{a=-r}^{r}\sum_{b=-r}^{r} L_{i+a, j+b} \cdot M_{a,b}\;}$$

Esempio esplicito con $m=3$:
$$(L*M)_{i,j} = L_{i-1, j-1} m_{1,1} + L_{i-1,j}\,m_{1,2} + L_{i-1,j+1}\,m_{1,3} + L_{i,j-1}\,m_{2,1} + L_{i,j}\,m_{2,2} + L_{i,j+1}\,m_{2,3} + L_{i+1,j-1}\,m_{3,1} + L_{i+1,j}\,m_{3,2} + L_{i+1,j+1}\,m_{3,3}.$$

Notazione: $L*M_x = L_x$, $L*M_y = L_y$, $L*M_{\nabla^2} = \nabla^2 L$.

---

## 9. Riassunto operativo

- Immagine = funzione $f:\mathbb{R}^2 \to C$, digitalizzata via campionamento ($H\times W$) e quantizzazione ($N_B \geq \log_2 N_C$).
- TrueColor = tensore $I : C \times (H^* \times W^*) \to \mathbb{R}$ con 3 canali RGB a 8 bit.
- Spazi colore: RGB (additivo), HSV (percettivo), CMYK (sottrattivo, stampa).
- Scala di grigi: luminanza $L = 0.299R + 0.587G + 0.114B$, oppure media $(R+G+B)/3$.
- Operatori puntuali (LUT, $O(1)$): inversione, log, gamma, contrast stretching con soglia $T$, equalizzazione istogramma.
- Operatori locali da Taylor:
  - I ordine $\to$ Sobel (sharpening): $M_x, M_y$, gradiente $G_L = |L_x|+|L_y|$ o $\|\nabla L\|$.
  - II ordine $\to$ Laplaciano: $M_{\nabla^2}$, attenzione $\nabla^2 f \neq (\nabla f)^2$.
- Smoothing: media (lineare), gaussiano (lineare), max/min/mediano (non lineari).
- Convoluzione: $L*M$ è la base di tutti i filtri lineari. Gestione del bordo: zero-padding, shrink, extend.
- Per edge detection raffinato $\to$ Canny Edge Detector.
