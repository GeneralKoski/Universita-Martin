# Studio del seminario: TVL (Simon, King, Howe)

Guida per capire il paper a fondo, slide per slide, con le definizioni, un esempio e cosa saper dire. In fondo c'è la **checklist di domande** per capire quando sei pronto.

Tutto è ricavato dal testo del paper (`2026-27/1_Material/Topics for seminars.zip`, cartella `07 - TVL`). Gli esempi numerici marcati **(mio)** li ho aggiunti io e controllati a mano: non sono nel paper. Le figure del PDF non le ho viste.

## Come usarlo

1. Leggi la sezione di una slide, poi chiudi e prova a spiegarla a voce in 1 minuto.
2. Rifai a mano gli esempi (foglio e penna). È il modo più veloce per capire `result` e il join.
3. Alla fine rispondi alla checklist senza guardare. Se rispondi bene alle domande 1-6 sei a posto per l'essenziale.

## Simboli usati

| Simbolo | Significato |
|---|---|
| `T` | un sistema (insieme finito) di disuguaglianze `a·x + b·y ≤ c` |
| `[[T]]` | l'insieme di punti di R^n che soddisfano tutte le disuguaglianze di `T` (la semantica) |
| `T1 ⊨ T2` | entailment: `[[T1]] ⊆ [[T2]]`, cioè `T1` implica `T2` |
| `T1 ≡ T2` | equivalenti: si implicano a vicenda |
| `⊓`, `⊔` | meet e join del reticolo |
| `conv(S)` | inviluppo convesso di `S` |
| `cl(S)` | chiusura topologica di `S` (aggiunge i punti di bordo mancanti) |
| `var(t)` | le variabili con coefficiente diverso da zero in `t` |
| `π_Y(T)` | restrizione: le sole disuguaglianze di `T` le cui variabili stanno tutte in `Y` |
| `∃x` | proiezione: eliminare la variabile `x` |
| `θ(t)` | angolo che orienta il semipiano di `t`, serve per ordinare le disuguaglianze |
| `d` | numero di variabili (dimensione) |
| `k` | numero massimo di disuguaglianze in una proiezione |

## Promemoria di interpretazione astratta

Un dominio astratto rappresenta insiemi di stati del programma con elementi finiti. Servono: un ordine, un join (`⊔`) per unire i rami di un `if` e i cicli, una proiezione per le variabili che escono di scope, un test di entailment per capire quando il punto fisso è stato raggiunto, e un **widening** per far terminare i cicli quando il dominio ha catene ascendenti infinite. In genere si ha una coppia di Galois `(α, γ)`: `γ` dice cosa significa un elemento astratto, `α` dà la migliore astrazione di un insieme concreto. Questi concetti sono nelle slide 06-07 del corso. Domini numerici classici: intervalli (slide 12 del corso), Octagon, poliedri.

---

## Slide 1 - Titolo

**Di cosa parla il paper.** Propone un dominio astratto numerico fatto di disuguaglianze lineari con **al massimo due variabili** per disuguaglianza e **coefficienti qualsiasi** (reali). Mostra che tutte le operazioni necessarie a un'analisi (meet, join, proiezione, entailment, widening) si fanno in tempo polinomiale e in modo semplice.

**Il filo del discorso.** Tutto ruota intorno a un'idea sola, la *completion* (chiusura): rendere esplicite tutte le conseguenze di un sistema sulle coppie di variabili. Dopo, ogni operazione si fa coppia per coppia, e ogni coppia è un problema in due dimensioni, quindi facile.

**Saper dire.** In una frase: "un dominio tra gli Octagon e i poliedri, con coefficienti qualsiasi e costo polinomiale, grazie a un'operazione di completion".

---

## Slide 2 - Precisione contro trattabilità

**Il compromesso.** Più un dominio è espressivo (esprime più relazioni), più le operazioni costano.

| Dominio | Forma delle disuguaglianze | Relazionale? | Costo |
|---|---|---|---|
| Intervalli | `l ≤ x ≤ u` | no, una variabile per volta | molto basso |
| Octagon (Miné) | `±x ± y ≤ c`, coefficienti in {−1, 0, +1} | sì, ma limitato | chiusura O(d³) |
| **TVL** | `a·x + b·y ≤ c`, `a, b, c` reali | sì, due variabili | O(d³ (log d)²) con `k` costante |
| Poliedri | `Σ ai·xi ≤ c`, tutte le variabili | sì, completo | esponenziale nel caso peggiore |

**Domini relazionali.** Un dominio non relazionale (intervalli) tiene un vincolo per variabile e perde le relazioni: dopo `x = y` non sa più che `x` e `y` sono uguali. Un dominio relazionale ricorda relazioni come `x − y ≤ 3`.

**Octagon, come funziona (serve per il confronto).** Per `d` variabili si usano `2d` variabili `x_i^+` e `x_i^-` e una matrice `2d × 2d` (DBM, difference-bound matrix). Ogni disuguaglianza `x_i − x_j ≤ c`, `x_i + x_j ≤ c` o `x_i ≤ c` diventa una differenza tra due variabili della matrice, e la **chiusura** (che rende tutti i vincoli il più stretti possibile) si calcola con Floyd-Warshall, cioè cammini minimi, in O(d³). Le operazioni dopo la chiusura sono semplici: per esempio il join di `x − y ≤ c1` e `x − y ≤ c2` è `x − y ≤ max(c1, c2)`.

**Poliedri.** Descrivono tutti i vincoli lineari insieme. Il join è un inviluppo convesso e si calcola con l'algoritmo di Chernikova passando da disuguaglianze a vertici e raggi, con costo esponenziale nel caso peggiore.

**Il punto del paper.** Dagli Octagon prende l'idea di *chiusura* (qui chiamata completion, per non confonderla con la chiusura topologica) e toglie il vincolo dei coefficienti unitari.

**Saper dire.** Perché TVL sta "in mezzo" e cosa guadagna rispetto agli Octagon (coefficienti qualsiasi).

---

## Slide 3 - Il dominio

### Definizioni

- `Lin_X`: tutte le disuguaglianze `a·xi + b·xj ≤ c` con `a, b, c` reali (quindi al più due variabili).
- `Two_X`: tutti i sottoinsiemi **finiti** di `Lin_X`. Un elemento del dominio è un sistema `T`.
- Semantica: `[[T]]` = intersezione dei semipiani, un poliedro in R^n.
- Ordine: `T1 ⊨ T2` se `[[T1]] ⊆ [[T2]]`. Si quozienta per equivalenza (`Two≡_X`).
- Il paper dimostra che `(Two≡_X, ⊨, ⊓, ⊔)` è un **reticolo, non un reticolo completo**:
  - `[T1] ⊓ [T2] = [T1 ∪ T2]`: il meet è l'unione dei sistemi (intersezione dei poliedri).
  - `[T1] ⊔ [T2] = [T]` con `[[T]] = cl(conv([[T1]] ∪ [[T2]]))`: il join è la **chiusura topologica dell'inviluppo convesso** dell'unione.

### Perché serve `cl` (Esempio 1 del paper)

`T1` descrive il solo punto `(0, 1)`. `T2` descrive la semiretta `{(x, y) | y = x, x ≥ 0}`. Un punto dell'inviluppo convesso è `λ·(0,1) + (1−λ)·(t,t)`. Calcolando **(mio)**: con `a` = ascissa e `b` = ordinata si ottiene `b − a = λ`. Quindi:

- per `a > 0`, `b − a` può valere qualsiasi valore in `[0, 1)`, ma **mai 1** (servirebbe `λ = 1`, che dà solo `(0,1)`);
- per `a = 0` si ha `0 ≤ b ≤ 1`, compreso il punto `(0,1)`.

L'inviluppo è quindi `{a ≥ 0, 0 ≤ b − a < 1} ∪ {(0,1)}`: contiene il punto `(0,1)` ma **non la semiretta `y = x + 1`**, quindi non è chiuso. Un sistema di disuguaglianze non strette (`≤`) descrive solo insiemi **chiusi**, quindi non può rappresentarlo. Si prende la chiusura, che aggiunge la semiretta mancante: il join è `{x ≥ 0, x ≤ y, y ≤ x + 1}` (mio).

### Niente α

Il paper nota che, con `γ(T) = [[T]]`, **non esiste α**: non c'è una migliore astrazione per l'insieme `{(x, y) | x² + y² ≤ 1}` (il cerchio). Qualsiasi poligono finito che lo contiene si può stringere aggiungendo un lato: non c'è un minimo. Negli Octagon invece ogni oggetto planare ha al più otto disuguaglianze (`±x`, `±y`, `±x ± y`) e una migliore approssimazione esiste. Per questo il dominio si usa con la sola `γ`.

### Perché "non completo"

Contiene solo sistemi **finiti**. Un'unione infinita di approssimazioni sempre più strette del cerchio non ha estremo superiore dentro il dominio. (Spiegazione intuitiva mia: il paper afferma solo che è un reticolo e non un reticolo completo.)

**Saper dire.** Cos'è un elemento, cosa sono meet e join, perché serve `cl` con l'esempio, perché non c'è α.

---

## Slide 4 - Forma completa

### Definizioni

- `var(t)` = variabili con coefficiente non nullo. Può essere vuoto (`0 ≤ −1`, contraddizione), una variabile (un limite, `x ≤ 5`) o due.
- **Restrizione** `π_Y(T) = {t ∈ T | var(t) ⊆ Y}`: le disuguaglianze di `T` che usano solo variabili di `Y`.
- **Completo** (Def. 5): `T` è completo se per ogni disuguaglianza `t` (con al più due variabili) vale `T ⊨ t ⇒ π_var(t)(T) ⊨ t`. Cioè: tutto ciò che `T` implica su `var(t)` è già implicato dalle sole disuguaglianze di `T` su `var(t)`.

### Esempio **(mio)**

`T = {y ≤ x, x ≤ z}`. Conseguenza: `y ≤ z`. Ma `π_{y,z}(T) = ∅` (nessuna disuguaglianza di `T` usa solo `y` e `z`), e `∅ ⊭ y ≤ z`. Quindi `T` **non è completo**. Aggiungendo `y ≤ z` diventa completo: ora la relazione tra `y` e `z` è scritta nella coppia `{y, z}`.

### Prop. 1 e Prop. 3

- **Prop. 1**: ogni `T` ha una forma completa equivalente `T'`: si aggiungono a `T` le proiezioni sulle coppie di variabili (`T_{x,y}` = proiezione di `T` sul piano `x, y`, eliminando tutte le altre variabili).
- **Prop. 3**: un sistema completo è insoddisfacibile se e solo se contiene una disuguaglianza contraddittoria su zero variabili (`0 ≤ −1`). Quindi si rileva l'insoddisfacibilità leggendo la forma completa.

### Ordinare per angolo

Per ordinare le disuguaglianze di una coppia si usa `θ(a·x + b·y ≤ c) = ψ` con `cos ψ = −b / √(a² + b²)` e `sin ψ = a / √(a² + b²)`. `θ` è l'angolo (antiorario) di cui bisogna ruotare il semipiano `y ≥ 0` per sovrapporlo al semipiano `a·x + b·y ≤ 0`. Intuizione: ogni disuguaglianza è un lato del poliedro planare, e ordinare per `θ` significa elencare i lati girando intorno al poliedro. Serve per `filter`, `extreme` ed `entails`.

### Entailment tra poche disuguaglianze (sezione 2.5)

`{t1, t2} ⊨ t` si riduce alla regola di Cramer: cerco `λ1, λ2 ≥ 0` tali che `λ1·t1 + λ2·t2` abbia gli stessi coefficienti di `t`. Con `d = a1·b2 − a2·b1`:

- `λ1 = (a·b2 − a2·b) / d`
- `λ2 = (a1·b − a·b1) / d`
- implicazione vera se `λ1 ≥ 0`, `λ2 ≥ 0` e `λ1·c1 + λ2·c2 ≤ c` (se `d = 0` le pendenze coincidono e basta confrontare le costanti).

Esempio **(mio)**: `t1: x + y ≤ 4`, `t2: x − y ≤ 2`. Qui `d = −2`. Per `t: x ≤ c` si ha `λ1 = λ2 = 1/2` e `λ1·4 + λ2·2 = 3`. Quindi `{t1, t2} ⊨ x ≤ 3` (sommando le due, `2x ≤ 6`). È costo costante.

**Saper dire.** Cos'è un sistema completo, con l'esempio `y ≤ x, x ≤ z`; che dopo la completion si ragiona coppia per coppia; cosa fa `π_Y`.

---

## Slide 5 - Come si calcola la completion

### Chi l'ha inventata

Nelson (1978): un algoritmo polinomiale per decidere la **soddisfacibilità** di sistemi con due variabili per disuguaglianza. Il paper osserva che quell'algoritmo calcola già la completion.

### Ingrediente 1: `result`

Date `t1 ≡ a·x + b·y ≤ c` con `a > 0` e `t2 ≡ d·x + e·z ≤ f` con `d < 0`, la **resultante** elimina `x`:

`a·e·z − d·b·y ≤ a·f − d·c`

È una combinazione lineare con pesi positivi (`−d` per la prima, `a` per la seconda) in cui `x` si annulla: è un passo di Fourier-Motzkin. `result(T)` raccoglie tutte le resultanti di coppie di disuguaglianze.

Esempio **(mio)** con coefficienti non unitari: `2x + y ≤ 4` e `−x + 3z ≤ 1`. Qui `a = 2, b = 1, c = 4, d = −1, e = 3, f = 1`. La formula dà `6z + y ≤ 2 + 4`, cioè `y + 6z ≤ 6`. Controllo: `(2x + y) + 2·(−x + 3z) = y + 6z ≤ 4 + 2·1 = 6`. ✓.

### Ingrediente 2: `filter`

Per una coppia `Y = {x, y}`, `filter_Y(T)` toglie le disuguaglianze **ridondanti** (quelle implicate dalle altre), restituendo un sottoinsieme equivalente e minimo. Se il sistema è insoddisfacibile restituisce una sola disuguaglianza contraddittoria; toglie anche le tautologie (`0 ≤ 1`). Come funziona (Fig. 1): le disuguaglianze sono ordinate per `θ`; si scorre il giro in senso antiorario, e per ogni disuguaglianza `tc` si controlla se le sue due vicine (`tn` e `tl`) la implicano (entailment tra tre disuguaglianze, costo costante): se sì, `tc` è ridondante e si toglie. Ci si ferma dopo un giro completo senza ridondanze. Costo **lineare**.

### Ripetere quanto?

`complete(T0) = T_m` con `T_{i+1} = filter(T_i ∪ result(T_i))` e `m = ⌈log2(|var(T0)| − 1)⌉`.

**Lemma 1** (riformulazione di Nelson): se `T ⊨ t`, esiste un insieme `Y` di al più `⌊|var(T)|/2⌋ + 1` variabili tale che `π_Y(T ∪ result(T)) ⊨ t`. Cioè: un'iterazione di `result` **dimezza** (circa) il numero di variabili necessarie per derivare una conseguenza. Ripetendo, bastano circa `log2 d` iterazioni (Teorema 1: il risultato è equivalente a `T` ed è completo).

Intuizione **(mia)**: in una catena `x0 ≤ x1 ≤ ... ≤ x4`, `result` collega variabili a distanza 2, poi a distanza 4: la distanza **raddoppia** a ogni giro, e per coprire una catena lunga `m` servono `log2 m` giri.

### Esempio 2 del paper

`T0 = {x0 ≤ x1, x1 ≤ x2, x2 ≤ x3, x3 ≤ x4}` (5 variabili, quindi `⌈log2 4⌉ = 2` iterazioni).
- `result(T0) = {x0 ≤ x2, x1 ≤ x3, x2 ≤ x4}` (distanza 2).
- `result(T0 ∪ T1)` aggiunge `{x0 ≤ x3, x0 ≤ x4, x1 ≤ x4}` (distanza 3 e 4). Ora `T3 = T0 ∪ T1 ∪ T2` è un punto fisso.

### Esempio 3 del paper (insoddisfacibilità)

`T0 = {−x + y ≤ −1, −2x − 3y ≤ −6, 4x − 2y ≤ −4}`. È già completo, ma servono due passi in più: uno rende esplicite le disuguaglianze a una variabile, l'altro quelle a zero variabili. Il paper dice che `T1 = filter(T0 ∪ result(T0))` aggiunge `{−y ≤ −2, −5x ≤ −9, x ≤ −3}` e poi `0 ≤ −24 ∈ result(T1)`, quindi `filter` collassa tutto in `{0 ≤ −24}`. Controllo **(mio)**:
- `−5x ≤ −9`: `3·(−x + y ≤ −1) + (−2x − 3y ≤ −6)` ✓.
- `x ≤ −3`: `2·(−x + y ≤ −1) + (4x − 2y ≤ −4) = 2x ≤ −6` ✓.
- `−y ≤ −2`: `(4x − 2y ≤ −4) + 2·(−2x − 3y ≤ −6) = −8y ≤ −16` ✓.
- `0 ≤ −24`: `5·(x ≤ −3) + (−5x ≤ −9)` ✓.

**Attenzione (mio):** calcolando a mano anche `(4x − 2y ≤ −4) + 4·(−x + y ≤ −1) = 2y ≤ −8`, cioè `y ≤ −4`, che il paper non elenca in `T1`. Non cambia la conclusione. Alla lavagna usa solo i quattro risultati sopra.

### Costo

`k` = numero massimo di disuguaglianze in una proiezione, `d` = numero di variabili. Il costo è `O(k² d³ log d (log k + log d))`. Se `k` è limitato da una costante (widening per trattabilità), diventa `O(d³ (log d)²)`, appena sopra gli `O(d³)` degli Octagon.

**Saper dire.** Cosa fa `result`, con un esempio tuo; cosa fa `filter`; perché bastano log d iterazioni; come si rileva un sistema insoddisfacibile.

---

## Slide 6 - Proiezione ed entailment

### Proiezione (sezione 5)

`∃x(T)` = tutte le restrizioni `π_Y(T)` con `Y` coppia di variabili che **non contiene** `x`. In pratica: **si tolgono le disuguaglianze che contengono `x`**. Non serve Fourier-Motzkin, perché in un sistema completo le conseguenze che non dipendono da `x` sono già scritte esplicitamente. La Prop. 6 dimostra che è corretta (coincide con la proiezione geometrica) e che il risultato è ancora completo.

Esempio dal paper: sistema completo con `y ≤ x` e `x ≤ z` (e quindi anche `y ≤ z`). Proiettando `x` si toglie `y ≤ x` e `x ≤ z` ma resta `y ≤ z`, che la completion aveva già scritto.

### Entailment (sezione 6)

**Prop. 7**: se `T'` è completo, `T' ⊨ T` se e solo se `π_Y(T') ⊨ π_Y(T)` per ogni coppia `Y = {x, y}`. Quindi il confronto si fa piano per piano.

Su un piano, `T1 ⊨ T2` significa che ogni disuguaglianza `t` di `T2` è implicata da `T1`. Per ogni `t` bastano le due disuguaglianze di `T1` con angolo `θ` immediatamente prima e dopo quello di `t` (vicine in ordine angolare), e l'entailment `{t_i, t_{i+1}} ⊨ t` si controlla con Cramer in tempo costante. Con tutto ordinato per `θ` basta scorrere le due liste insieme (Fig. 4): costo **lineare**.

**Saper dire.** Perché la proiezione è "gratis" dopo la completion, e perché l'entailment si riduce a coppie di variabili.

---

## Slide 7 - Join

### Idea

Il join è l'inviluppo convesso (poi chiuso). Per i poliedri qualsiasi si usa Chernikova, passando da disuguaglianze a **vertici e raggi** e viceversa, con costo potenzialmente esponenziale. Qui, grazie alla completion, si calcola il join **proiezione per proiezione** (`⋎`, Def. 11): per ogni coppia `{x, y}` si fa l'inviluppo convesso (chiuso) dei due poliedri planari `π_{x,y}(T1)` e `π_{x,y}(T2)`.

- **Prop. 4**: se `T1` e `T2` sono completi, anche il risultato lo è.
- **Prop. 5**: il risultato coincide con `cl(conv([[T1]] ∪ [[T2]]))`, cioè con l'inviluppo nello spazio intero.

Ogni proiezione è un poliedro **planare**, e per quelli esiste un algoritmo semplice.

### I tre passi

1. **`extreme`** (Fig. 2): le disuguaglianze di un poliedro planare, ordinate per `θ`, definiscono **vertici** (intersezione di due lati consecutivi) e **raggi** (se l'angolo tra due lati consecutivi è `≥ π`, il poliedro è illimitato in quella direzione). Casi particolari: un solo semipiano genera un raggio in più. Al massimo **4 raggi** per poliedro (due semipiani opposti).
2. **Graham scan** (Fig. 3): si mettono insieme i vertici di `T1` e `T2`. Per gestire i raggi, si calcola un quadrato centrato nell'origine che contiene tutti i vertici; ogni vertice viene **traslato lungo ogni raggio** (di `2√2·m`, così finisce fuori dal quadrato) e i punti traslati si aggiungono all'insieme. Si applica l'algoritmo di Graham (inviluppo convesso di punti nel piano), modificato per tenere i punti sul bordo.
3. **`connect`**: ogni coppia di vertici adiacenti sull'inviluppo genera la disuguaglianza della retta che li unisce, `(y2 − y1)x + (x1 − x2)y ≤ (y2 − y1)x1 + (x1 − x2)y1`. Si scartano i lati che stanno interamente fuori dal quadrato e quelli con la stessa pendenza dell'ultimo (collineari). Ci sono casi speciali per punti allineati.

**Costo**: dominato da Graham, `O(n log n)` con `n = |V|·|R|` (e `|R| ≤ 8`), cioè `O((|T1| + |T2|) log(|T1| + |T2|))`. Gli autori scrivono che, per quanto ne sanno, questo algoritmo per poliedri planari è nuovo.

### Esempio **(mio)** con coefficienti non unitari

`T1`: quadrato `[0,1] × [0,1]`. `T2`: il punto `(3, 3)`. L'inviluppo ha vertici `(0,0), (1,0), (3,3), (0,1)` e i lati:
- `−x ≤ 0`, `−y ≤ 0` (lati sugli assi);
- `3x − 2y ≤ 3` (lato da `(1,0)` a `(3,3)`);
- `−2x + 3y ≤ 3` (lato da `(0,1)` a `(3,3)`).

Controllo: `(1,0)`: `3 ≤ 3` ✓, `(3,3)`: `9 − 6 = 3` ✓ e `−6 + 9 = 3` ✓, `(0,1)`: `3 ≤ 3` ✓, e `(1,1)` è dentro. I coefficienti `3` e `2` **non sono unitari**: un Octagon non può rappresentare questo join esattamente. Il punto `(3, 5/2)`, per esempio, soddisfa tutti i vincoli di Octagon che contengono il poligono (`x−y ≤ 1`, `x+y ≤ 6`, `x ≤ 3`, ...), ma viola `3x − 2y ≤ 3` (`9 − 5 = 4 > 3`).

**Saper dire.** Perché il join si calcola coppia per coppia, i tre passi (extreme, Graham, connect), perché i raggi vengono spinti fuori da un quadrato, il costo.

---

## Slide 8 - Widening

### A cosa serve

Il dominio ha catene ascendenti infinite (si possono aggiungere disuguaglianze all'infinito), quindi per far terminare i cicli serve un widening. Può servire anche per tenere sotto controllo tempo e spazio.

### Per la terminazione

**Qualsiasi widening dei poliedri si può applicare a un poliedro planare**, e poi estendere al sistema (proiezione per proiezione). Esempio generale **(mio)**: il widening standard di Cousot-Halbwachs tiene solo le disuguaglianze del vecchio poliedro che sono ancora vere nel nuovo; per un intervallo, `[0,1] ∇ [0,2] = [0, +∞)`. Per ritardarlo e perdere meno precisione conviene applicarlo **solo quando il numero e la dimensione delle proiezioni si sono stabilizzati**.

**Sottigliezza**: applicare la completion **dopo** il widening può **reintrodurre** le disuguaglianze appena eliminate, perché sono conseguenze di altre. Questo può impedire la terminazione.

### Per la trattabilità

Limitare a una costante `k` il numero di disuguaglianze in ogni proiezione. Come scegliere quale togliere: **quella che contribuisce al lato più corto** del poliedro (la meno importante per la forma). Risultato:
- rappresentazione `O(d²)`, come le DBM degli Octagon, ma **densa**: si occupa spazio solo per le disuguaglianze presenti, e senza i coefficienti unitari;
- completion `O(d³ (log d)²)`, contro `O(d³)` degli Octagon.

**Saper dire.** I due usi del widening, la sottigliezza con la completion, il compromesso costo/precisione.

---

## Slide 9 - Evidenza empirica

### Cosa hanno fatto

Hanno implementato una completion **ingenua** e misurato la crescita del numero di proiezioni e di disuguaglianze su **poliedri planari casuali**: ogni poliedro è l'inviluppo convesso di punti casuali in un quadrato, su coppie di variabili diverse. Tre scenari:

- **varying**: poliedri con 3-13 disuguaglianze ciascuno, fino a 147 in totale; dimensione 10.
- **constant**: 10 disuguaglianze per ogni coppia di variabili; dimensione 10.
- **sparse**: pochi poliedri che condividono variabili (vincoli debolmente accoppiati); dimensione 100.

### Risultati (Fig. 6)

| | varying | constant | sparse |
|---|---|---|---|
| dimensione (variabili) | 10 | 10 | 100 |
| disuguaglianze generate | 147 | 143 | 139 |
| per poliedro, dopo redundancy removal | 3-13 | 10 | 10 |
| disuguaglianze non ridondanti su cui si applica la completion | 100 | 100 | 100 |
| media per poliedro dopo la completion | 5,3 | 7,0 | 7,1 |
| resultanti aggiunte (media) | 210 | 189 | 106 |
| aumento del numero di proiezioni | **56%** | **123%** | **9%** |
| proiezioni con più di 30 disuguaglianze | 0,22% | 0,18% | 0,00% |

L'aumento è maggiore in `constant` perché all'inizio ci sono poche proiezioni non vuote (circa 143/10), quindi la completion ne crea molte. In `sparse` è minimo, perché le disuguaglianze condividono poche variabili.

### Perché le disuguaglianze restano poche

Il numero di disuguaglianze non cresce con il numero di punti `n`: l'inviluppo convesso di `n` punti casuali in un **quadrato** ha in media `O(log n)` punti estremi; per punti in un **cerchio** sono `O(n^(1/3))`. Meno dell'1% delle proiezioni ha più di 30 disuguaglianze. Da qui l'idea di limitare `k` a una costante con poca perdita di precisione.

### Limite onesto

I dati sono **casuali**, non vengono da programmi reali, e non c'è un confronto di tempi con gli Octagon. Gli autori notano che i dati casuali non favoriscono l'algoritmo, quindi la completion dovrebbe restare trattabile, ma è un'indicazione, non una prova. Il caso peggiore (crescita quadratica del numero di proiezioni) esiste.

**Saper dire.** Cosa è stato misurato, i tre numeri (56%, 123%, 9%), perché `k` resta piccolo, i limiti.

---

## Slide 10 - Confronto e limiti

| | Octagon | TVL |
|---|---|---|
| Disuguaglianze | `±x ± y ≤ c` | `a·x + b·y ≤ c` |
| Coefficienti | −1, 0, +1 | reali qualsiasi |
| Rappresentazione | matrice DBM `2d × 2d` | densa, solo le presenti |
| Chiusura / completion | `O(d³)`, Floyd-Warshall | `O(d³ (log d)²)` con `k` costante |
| Oggetto planare | al più 8 disuguaglianze, α esiste | numero non limitato, niente α |

**Limiti.**
- Niente α: lavora solo con γ.
- Il dominio è definito sui **reali**: gli interi non sono trattati (il paper nomina l'estensione agli interi come linea di ricerca).
- Prove su dati casuali, senza integrazione in un tool di analisi.
- Widening con la sottigliezza della completion.

**Applicazioni citate nell'introduzione.** Verifica di programmi, model checking di automi temporizzati, parallelizzazione, vulnerabilità di sicurezza (buffer overrun), memory leak, terminazione di programmi logici.

**Related work (una riga a testa, solo se te lo chiedono).** Miné: Octagon e DBM (cammini minimi, Pratt). Su e Wagner: intervalli di interi per sistemi a due variabili. Jaffar et al., Harvey e Stuckey: vincoli con due variabili nei solver CLP. Hochbaum e Naor: algoritmo per la soddisfacibilità, `O(|T| |var(T)|² log |T|)`.

**Future work del paper.** Partizionare il sistema con union-find in sottosistemi a variabili disgiunte, e usare iterazione semi-naive per non rifare lavoro nella completion.

---

## Slide 11 - Conclusioni

Il messaggio da ricordare, in tre punti:
1. **Una sola operazione**, la completion, rende polinomiali meet, join, proiezione ed entailment.
2. Le operazioni sono **semplici** da implementare, quindi meno soggette a errori.
3. Rispetto agli Octagon si tolgono i **coefficienti unitari** senza perdere la trattabilità.

---

# Checklist di domande

Rispondi a voce, senza guardare. Le risposte sono nella sezione sotto. Segna quelle che sai.

**Essenziali (1-6)**

- [ ] 1. Cos'è un elemento del dominio TVL, e cosa distingue questo dominio dagli Octagon e dai poliedri?
- [ ] 2. Perché il join richiede la chiusura topologica `cl`? Fai l'esempio.
- [ ] 3. Cos'è un sistema completo? Perché dopo la completion si ragiona coppia per coppia?
- [ ] 4. Cosa fa `result`? Fammi un esempio con coefficienti non unitari.
- [ ] 5. Perché bastano circa `log2 d` iterazioni per la completion?
- [ ] 6. Come si calcola il join, e perché costa `O(n log n)`?

**Da sapere bene (7-10)**

- [ ] 7. Cosa fa `filter` e come usa l'angolo `θ`?
- [ ] 8. Perché proiettare una variabile in un sistema completo è "gratis"?
- [ ] 9. Perché non esiste α? Cosa cambia rispetto agli Octagon?
- [ ] 10. Cosa dice la Prop. 7 sull'entailment e come si controlla il caso con tre disuguaglianze?

**Domande a trabocchetto (11-14)**

- [ ] 11. Perché il widening è delicato in questo dominio?
- [ ] 12. Che cosa dimostrano gli esperimenti e che cosa no?
- [ ] 13. Quanto costa la completion e da cosa dipende? Come si arriva a `O(d³ (log d)²)`?
- [ ] 14. Il TVL è esatto rispetto ai poliedri?

**Ripasso del corso (per l'orale, 15-17)**

- [ ] 15. Cos'è una coppia di Galois e cosa sono α e γ?
- [ ] 16. Cos'è un widening e perché serve? Dai un esempio sugli intervalli.
- [ ] 17. Che differenza c'è tra un dominio relazionale e uno non relazionale?

## Risposte

**1.** Un elemento è un insieme finito di disuguaglianze `a·x + b·y ≤ c` con al più due variabili e coefficienti reali qualsiasi. Rispetto agli Octagon (coefficienti solo −1, 0, +1) è più espressivo; rispetto ai poliedri (tutte le variabili in una disuguaglianza) è più semplice e ha operazioni polinomiali.

**2.** Perché l'inviluppo convesso di due insiemi chiusi può non essere chiuso, e un sistema di disuguaglianze non strette descrive solo insiemi chiusi. Esempio 1: `T1` = punto `(0,1)`, `T2` = semiretta `y = x, x ≥ 0`. L'inviluppo contiene `(0,1)` ma non la semiretta `y = x + 1`, `x ≥ 0`. Il join è la chiusura: `{x ≥ 0, x ≤ y, y ≤ x + 1}`.

**3.** `T` è completo se ogni sua conseguenza `t` è già implicata dalle sole disuguaglianze di `T` su `var(t)`, cioè su una o due variabili. Prop. 1: ogni sistema ha una forma completa equivalente. Dopo la completion le relazioni tra le coppie di variabili sono tutte scritte, quindi le operazioni si fanno coppia per coppia (poliedri planari).

**4.** Date `a·x + b·y ≤ c` con `a > 0` e `d·x + e·z ≤ f` con `d < 0`, elimina `x`: `a·e·z − d·b·y ≤ a·f − d·c`. Esempio: `2x + y ≤ 4` e `−x + 3z ≤ 1` danno `y + 6z ≤ 6` (sommo la prima al doppio della seconda).

**5.** Lemma 1 (da Nelson): un'iterazione di `result` dimezza (circa) il numero di variabili necessarie a derivare una conseguenza. Ripetendo, ne bastano `⌈log2(|var| − 1)⌉`. Intuizione: in una catena di dipendenze la distanza coperta raddoppia a ogni giro.

**6.** Si fa l'inviluppo convesso su ogni proiezione planare (Prop. 4 e 5: il risultato è completo e coincide con l'inviluppo nello spazio intero). Tre passi: `extreme` (disuguaglianze → vertici e raggi, al più 4 raggi), Graham scan (i raggi si trattano traslando i vertici fuori da un quadrato), `connect` (lati dell'inviluppo → disuguaglianze). Costa `O(n log n)` perché è dominato da Graham.

**7.** Per una coppia di variabili ordina le disuguaglianze per angolo `θ` (che dice come è orientato il semipiano) e scorre il giro: se le due vicine implicano la disuguaglianza corrente, la toglie. Ogni controllo è un entailment tra tre disuguaglianze (costante), quindi costa tempo lineare dopo l'ordinamento.

**8.** Perché in un sistema completo le conseguenze che non dipendono da `x` sono già scritte esplicitamente: basta togliere le disuguaglianze che contengono `x` (niente Fourier-Motzkin). Prop. 6: il risultato è corretto e ancora completo.

**9.** Non c'è una migliore astrazione per, per esempio, un cerchio: qualsiasi poligono finito che lo contiene si può stringere con un lato in più. Negli Octagon ogni oggetto planare ha al più otto disuguaglianze e quindi una migliore approssimazione esiste. Per questo il TVL lavora solo con `γ`.

**10.** Prop. 7: se `T'` è completo, `T' ⊨ T` se e solo se `π_Y(T') ⊨ π_Y(T)` per ogni coppia `Y`. Su un piano, `{t1, t2} ⊨ t` si controlla con Cramer: si cercano `λ1, λ2 ≥ 0` con `λ1·t1 + λ2·t2` stesso coefficiente di `t`, poi si confrontano le costanti. Esempio: `x + y ≤ 4` e `x − y ≤ 2` danno `x ≤ 3` con `λ1 = λ2 = 1/2`.

**11.** Applicare la completion dopo il widening può reintrodurre le disuguaglianze appena tolte (sono conseguenze di altre), rompendo la terminazione. Per questo il widening si applica solo quando numero e dimensione delle proiezioni si sono stabilizzati.

**12.** Mostrano che, su poliedri planari casuali, il numero di proiezioni cresce del 56%, 123%, 9% e meno dello 0,3% ha più di 30 disuguaglianze, quindi limitare `k` costa poca precisione. **Non** dimostrano niente su programmi reali: dati casuali, nessun confronto di tempi con gli Octagon, completion ingenua.

**13.** `O(k² d³ log d (log k + log d))`, dove `d` è il numero di variabili e `k` il massimo di disuguaglianze per proiezione. Con `k` limitato da una costante (widening per trattabilità) diventa `O(d³ (log d)²)`, contro `O(d³)` degli Octagon.

**14.** No: è un'astrazione dei poliedri. Tiene solo le relazioni a due variabili alla volta, quindi una relazione tra tre variabili si perde (salvo ciò che è deducibile dalle proiezioni).

**15.** Una coppia di funzioni `α: concreto → astratto` (migliore astrazione) e `γ: astratto → concreto` (significato) con `α(c) ≤ a ⟺ c ⊆ γ(a)`. Garantisce che l'astrazione sia corretta. (Dalle slide 06-07 del corso, riguardale.)

**16.** Un operatore `∇` che sovrastima il join e forza la stabilizzazione in un numero finito di passi, per far terminare i cicli sui domini con catene ascendenti infinite. Sugli intervalli: `[0,1] ∇ [0,2] = [0, +∞)` (il limite instabile va all'infinito).

**17.** Non relazionale: un vincolo indipendente per ogni variabile (intervalli), perde le relazioni tra variabili. Relazionale: ricorda relazioni tra variabili (come `x − y ≤ 3`), a costo maggiore.

---

## Cose da NON fare all'esame

- Non dire che il TVL ha un'α o che è esatto sui poliedri.
- Non dire che gli esperimenti usano programmi reali o che confrontano i tempi con gli Octagon.
- Non affermare che il paper tratta gli interi o che esiste un tool: sono solo cenni.
- Non dire "completion = chiusura topologica": sono due cose diverse (la completion è l'analogo della chiusura degli Octagon, la chiusura topologica `cl` serve per il join).
- Non entrare nelle dimostrazioni: se ti chiedono "come si dimostra?" di' l'idea in una riga (per esempio "per induzione sulle iterazioni, usando il Lemma 1") e passa oltre.
