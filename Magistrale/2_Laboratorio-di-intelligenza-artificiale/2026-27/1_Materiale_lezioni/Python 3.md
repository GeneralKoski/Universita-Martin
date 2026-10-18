# Python 3

Fonte: `Python 3.pdf` (73 slide), più `Esempio Python 3 OOP.py` (il file `Student.py` citato nelle slide di OOP).

## Perché Python e come usarlo
- Linguaggio **easy to use**, con costrutti sia semplici sia sofisticati, **strutture dati native** efficienti e approccio **OOP**.
- **Interpretato** e portabile (ma può anche essere compilato), con interfacce interattive (**IPython**, **Jupyter**). È il linguaggio principale per il **machine learning**.
- Si usa **Python 3**, che **non è retrocompatibile** con Python 2 (es. `print something` contro `print(something)`).
- Modi d'uso:
  - script: `python3 myscript.py`
  - interprete interattivo: `python3`, oppure `ipython3` (più usabile; nella slide è scritto `iptyhon3`)
  - **notebook Jupyter**: celle di codice e markdown. **Pericolo**: l'ordine delle celle nel notebook può non coincidere con l'ordine in cui sono state eseguite (stato nascosto del kernel).

### Jupyter Lab
- Nel corso si usa **Jupyter Lab**; le indicazioni sono per Ubuntu su Windows (WSL, "bash on windows"). Documentazione: jupyter.org e jupyterlab.readthedocs.io.
- Installazione rapida:

```bash
sudo apt-get update
sudo apt install python3
sudo apt install python3-pip
sudo pip install jupyterlab
```

- Si lancia con `jupyter-lab` e si apre nel browser il link stampato nel terminale (figura: output del server con URL e token).
- (Aggiunta: sulle Ubuntu recenti `sudo pip install` è bloccato dal PEP 668 "externally-managed-environment"; si usa un ambiente virtuale, `python3 -m venv .venv` e poi `pip install jupyterlab`, oppure `pipx`/`uv`.)

## Variabili e tipi
- Il tipo di una variabile è **forzato** dall'utente (dichiarazione o **casting** esplicito) oppure **inferito dal contesto**: non serve dichiarare le variabili.
- Il valore nullo è **`None`**.
- Tipi built-in (funzioni di costruzione/cast):
  - `int(a [,base])`: interi, es. `10`, `0xFFF`, `0b110101`
  - `float(a)`: virgola mobile, es. `1.123`, `1.82e308`
  - `chr(a)`: singolo carattere `'a'` (non corrispondono agli interi). (Precisazione: in Python non esiste un tipo carattere; `chr(97)` prende un intero, il code point, e restituisce una `str` di lunghezza 1; l'inversa è `ord('a')`.)
  - `str(a)`: stringhe con `'...'`, `"..."` o multilinea con `"""..."""`
  - `bool(a)`: `True` / `False`
  - `complex(a [,imag])`: numeri complessi

## Funzioni primitive
- `print(a1, a2, ..., sep=..., end=...)`: `sep` separa gli argomenti, `end` chiude la stampa. (La firma nella slide mostra `sep='\t'`: i default reali sono `sep=' '` ed `end='\n'`.)

```python
a = 1
print(a, 2, sep='-', end='|')   # 1-2|
a = input('please input the value of a')   # legge una stringa da console
a = eval(input('please input the value of a'))  # "5 + 5" -> 10
eval('5+5')   # 10
```

- `input` restituisce sempre una **stringa**; `eval` valuta un'espressione Python (aggiunta: pericoloso su input non fidato, per convertire numeri si usa `int(...)`/`float(...)`).

## Operatori
- **Numerici**: `+ - * /` (`/` dà sempre float), `%` modulo (resto), `//` quoziente intero, `**` potenza (`2**4 = 16`).
- **Bitwise**: `&`, `|`, `^` (AND, OR, XOR), `~` complemento a 1, shift. (Errore nella slide: gli shift sono `<<` e `>>`, non `<<<`/`>>>`; `0b1 << 2` vale `0b100`, cioè 4.)
- **Assegnamento**: `=, +=, -=, *=, /=, **=, &=, ...`. **Non esistono** `++` e `--`.
- **Confronto**: `==`, `!=`, `<, >, <=, >=`. La slide avverte che "a volte `==` confronta puntatori e non valori". (Precisazione: `==` chiama `__eq__` e confronta valori; confronta le identità solo per classi che non ridefiniscono `__eq__`, perché l'implementazione di default è l'identità. Per confrontare i riferimenti si usa `is`.)
- **Logici**: `and`, `or`, `not`.

```python
a, b, c = True, True, False   # assegnamento multiplo
print((a and b) or not c)     # True
```

- **Identità**: `is`, `is not` confrontano le locazioni di memoria (i riferimenti) tramite `id(x)`, che restituisce un intero unico per ogni oggetto vivo.
- La slide dice che "i tipi primitivi sono passati per copia, gli altri per riferimento, come in Java". (Precisazione: in Python tutto è un oggetto e si passa sempre il riferimento, "call by sharing"; int, float, str e tuple sembrano passati per copia solo perché sono **immutabili**.)

## Stringhe
- Le stringhe sono **immutabili**.
- Concatenazione `+`, ripetizione `*`, lunghezza `len`:

```python
'hello' + 'world'   # 'helloworld' (la slide riporta 'hello world', con uno spazio che + non aggiunge)
'AG' * 3            # 'AGAGAG'
len('AGAGAG')       # 6
```

### Slicing
- `s[i]` singola posizione, `s[start:end]` sottostringa (`end` escluso), `s[start:end:step]` sottosequenza con passo.
- Indici **negativi** contano dalla fine.

```python
s = 'my string'
s[0]          # 'm'
s[0:5]        # 'my st'
s = '0123456789'
s[0:len(s):3] # '0369'
s[-1]         # '9'  (equivale a s[-1:] o s[len(s)-1:len(s)])
s[:-1]        # '012345678'
s[::-1]       # '9876543210' (la slide riporta '98765433210', con un 3 di troppo)
```

### Metodi delle stringhe
- `str.find(sub[, start, end])`: posizione più piccola dove occorre `sub` (aggiunta: `-1` se assente; `end` è escluso).
- `str.index(sub[, start, end])`: come `find` ma, se `sub` non c'è, lancia `ValueError` (nella slide `ValuerError`).
- `str.replace(old, new[, count])`: copia della stringa con le occorrenze di `old` sostituite da `new`. (Errore nella slide: dice che di default sostituisce solo la prima occorrenza; in realtà di default le sostituisce **tutte**, `count` limita il numero.)
- `str.count(sub[, start, end])`: numero di occorrenze.
- **Attenzione**: ricerca e sostituzione **non considerano sovrapposizioni**:

```python
s = 'TTTATATATTT'
s.replace('ATA', 'N')   # 'TTTNTATTT'
s.count('ATA')          # 1 (le occorrenze sovrapposte sono 2)
```

- `upper()`, `lower()`; test `isupper()`, `islower()`, `isalpha()`, `isdigit()`, `isprintable()`, ...
- `strip([chars])`: toglie i caratteri `chars` (default: spazi bianchi, `\t`, `\n`) a inizio e fine.
- `startswith(sub)`, `endswith(sub)`: `True` se la stringa inizia/finisce con `sub` (nella slide "con la sottostringa start (end)", refuso per `sub`).

## Controllo del flusso
- I blocchi non hanno parentesi: il corpo è identificato dall'**indentazione**. Corpo vuoto con **`pass`**.

```python
if a > b:
    print(a)
elif a < b:
    pass
else:
    print(b)
    b += 1
```

- **`while ... else`**: il ramo `else` viene eseguito quando la condizione diventa `False`, **non** se si esce con `break`.

```python
a, i = 3, 0
while i < a:
    print(i, ' ', sep='', end='')
    i += 1
else:
    print('finish')      # 0 1 2 finish
```

- **`for ... in ... else`** (stessa semantica dell'`else`).
- `range([start=0,] stop [, step=1])` genera i numeri "al volo": `range(1000)` non costruisce una lista di 1000 elementi ma un oggetto **lazy** su cui si itera. (L'output di `for i in range(3): print(i, sep='', end='')` nella slide è `0 1 2`, ma con `end=''` si ottiene `012`.)

## Strutture dati built-in
- Le principali: **`list`, `tuple`, `set`, `frozenset`, `dict`**, disponibili senza import.
- `list` e `tuple`: sequenze **ordinate** di oggetti **eterogenei**, indicizzate da interi (non esistono array built-in). `list` è **mutabile**, `tuple` **immutabile**.
- `set`: insieme **non ordinato** di oggetti eterogenei, senza duplicati. `frozenset`: insieme **immutabile**, che secondo la slide "permette prestazioni migliori di set". (Precisazione: il vantaggio vero del frozenset è che è **hashable**, quindi può essere chiave di un dict o elemento di un altro set; le prestazioni di ricerca sono le stesse.)
- `dict`: mappa **mutabile** chiave-valore.

### Liste
- Sequenza ordinata e mutabile, anche eterogenea: `my_list = ['mygene', 6.16e-10, 0.0006, 3, True]`. La variabile è un **riferimento** alla lista (figura: `my_list` punta a un blocco di 5 celle indicizzate 0-4).
- Lo slicing funziona come per le stringhe (la slide dice "per le liste", intende "per le stringhe") ma si può usare anche per **modificare**:

```python
my_list[0]       # 'mygene'
my_list[-1]      # True
my_list[0:2]     # ['mygene', 6.16e-10]  (nella slide my_mylist, refuso)
my_list[4] = False
my_list_2 = my_list[:]   # lo slicing non di assegnamento crea una NUOVA copia
```

- Operazioni:
  - `len(lst)`; concatenazione `lst1 + lst2` (la slide scrive `[lst1] + [lst2]`, che invece crea una lista di due liste); ripetizione `[1,2]*3` → `[1,2,1,2,1,2]`
  - `append(x)` in coda; `extend(lst2)` appende tutti gli elementi di `lst2`; `insert(pos, x)`; `clear()`; `count(x)`
  - `reverse()`: la slide dice che "restituisce una copia invertita" (errore: inverte **sul posto** e restituisce `None`; per una copia si usa `lst[::-1]` o `list(reversed(lst))`)
  - `remove(x)`: rimuove la prima occorrenza, errore (`ValueError`) se `x` non c'è
  - `pop([pos])`: rimuove e restituisce l'elemento in `pos` (default: l'ultimo)
- **`del`** elimina una variabile, un elemento o una porzione: `del lst[3]` equivale nel risultato a `lst = lst[0:3] + lst[4:]`, ma quest'ultima crea due copie e le concatena, mentre `del` lavora sul posto senza copie.

### Tuple
- Sequenza ordinata **immutabile**: valgono gli stessi operatori delle liste tranne quelli di modifica.

```python
my_tuple = ('mygene', 6.16e-10, 0.0006, 3, False)
my_tuple[0:2]      # ('mygene', 6.16e-10)
(1, 2) + (3, 4)    # (1, 2, 3, 4)
```

### Strutture innestate, shallow e deep copy
- La slide afferma che le tuple "sono gestite sempre per copia e mai per riferimento", le liste sempre per riferimento. (Precisazione: anche le tuple sono riferimenti; non si vede la differenza solo perché non si possono modificare. Una tupla che contiene una lista mostra le modifiche della lista.)
- Non esistono matrici built-in: si usano **liste di liste** (o di tuple). Attenzione ai riferimenti condivisi:

```python
my_sub_list = [1, 2]
my_list_1 = [my_sub_list, 3, 4]
my_list_2 = [my_sub_list, 5, 6]
my_sub_list[0] = 0
print(my_list_1)   # [[0, 2], 3, 4]
print(my_list_2)   # [[0, 2], 5, 6]  entrambe puntano alla stessa sottolista
```

- Figura: `my_list_1` e `my_list_2` hanno il primo elemento che punta allo stesso blocco `[1, 2]`, che diventa `[0, 2]`.
- La slide dice che "l'assegnamento delle liste usa l'operatore copy ed è una shallow copy". (Errore: `my_list_2 = my_list_1` **non copia nulla**, crea un alias allo stesso oggetto, come mostra l'esempio stesso. La **shallow copy** è `lst.copy()`, `lst[:]` o `copy.copy(lst)`: nuova lista esterna, ma gli elementi interni sono gli stessi oggetti.)
- **Deep copy**: copia ricorsiva di tutto il contenuto. Si importa dal modulo **`copy`** (la slide dice "dalla libreria deepcopy", ma `deepcopy` è la funzione):

```python
from copy import deepcopy
my_list_1 = [[1, 2], 3, 4]
my_list_2 = deepcopy(my_list_1)
my_list_1[0][0] = 0
print(my_list_1)   # [[0, 2], 3, 4]
print(my_list_2)   # [[1, 2], 3, 4]
```

### Insiemi
- Collezione **non ordinata** di elementi eterogenei, **senza duplicati**. Creazione con `{...}` o `set()` (attenzione: `{}` è un dict vuoto).

```python
my_set = {'DNA repair', 2, 0.003}
my_set = set()
my_set.add('DNA repair')
my_set.remove(0.003)     # KeyError se assente (discard non dà errore)
A = {1, 2, 3}; B = {1, 4, 5}
A | B    # unione {1, 2, 3, 4, 5}
A & B    # intersezione {1}
A - B    # differenza {2, 3}
A ^ B    # differenza simmetrica (XOR) {2, 3, 4, 5}
```

- La slide dice che questi operatori creano copie "così come `&=, |=, -=, ^=`". (Errore: gli operatori composti modificano l'insieme **sul posto**, non creano un nuovo oggetto; verificato: con `b = a; a |= {2}` anche `b` cambia.)
- Confronti: `A <= B` (A sottoinsieme di B), `A >= B` (A contiene B), `x in A`, `x not in A`.

### Dizionari
- Insieme **mutabile** di coppie chiave-valore; chiavi e valori di qualsiasi tipo (aggiunta: le chiavi devono essere hashable, quindi immutabili). Chiavi **univoche**, valori anche duplicati.

```python
my_dict = {1: 'one', 'two': 2}
my_dict = dict()
my_dict[1] = 'one'      # accesso/inserimento tramite chiave
my_dict['two'] = 2
```

## Iteratori
- Le strutture dati sono **collezioni iterabili**. Se la struttura è ordinata l'iterazione ne segue l'ordine, altrimenti (set) l'ordine non è garantito.

```python
for x in my_list: ...
for x in my_dict.values(): ...
for k, v in my_dict.items(): print(k, v)   # items() dà coppie (chiave, valore)
```

- (Nella slide l'output di `my_dict.items()` per `{1:'one', 'two':2}` è `(1,'one')(2,'two')`, ma la seconda coppia è `('two', 2)`. Anche gli output con `end=''` sono stampati con spazi che non ci sarebbero.)

## Numeri casuali: modulo `random`
- `import random`; documentazione docs.python.org/3/library/random.html.
- **Seme**: `random.seed(seed)`. Fissarlo serve alla **riproducibilità** dei risultati: con un seme automatico ogni esecuzione dà risultati diversi e invalida quelli precedenti. Da ricordare per il progetto.
- Generatore **Mersenne Twister** (equidistribuito in 623 dimensioni), distribuzione **uniforme**.
- Funzioni:
  - `random.randint(a, b)`: intero in `[a, b]`, **entrambi inclusi**
  - `random.shuffle(lst)`: mescola la lista sul posto
  - `random.choice(lst)`: un elemento a caso
  - `random.sample(population, k)`: `k` elementi a caso. La slide dice "possibilmente con ripetizione" (errore: `sample` estrae **senza** ripetizione; con ripetizione si usa `random.choices(population, k=k)`, che accetta anche `weights=` per distribuzioni non uniformi, utile per l'esercizio 1.3).

## Caso d'uso: bag of words per sequenze di DNA
- Una metodologia **bag of words** scompone un oggetto $X$ nella collezione $\mathbb{X} = \{x_1, \dots, x_n\}$ delle parti che lo compongono e usa $\mathbb{X}$ per analizzare $X$.
- Sequenza di DNA = stringa sull'**alfabeto nucleotidico** $\Gamma = \{A, C, G, T\}$. $\Gamma^k$ = parole di lunghezza $k$, i **k-meri**. Un **dizionario** su $\Gamma$ è una collezione di parole in $\Gamma^*$.
- $s[i]$ = $i$-esimo carattere, $s[i, j]$ = sottostringa da $i$ a $j$ inclusi ($1 \le i \le j \le |s|$; la slide scrive "di lunghezza $|w|$" per $s$, refuso).
- **Dizionario k-esimo** di $w = a_1 \dots a_n$:

$$D_k(w) = \{ s \in \Gamma^k : \exists i,\ 1 \le i \le n - k + 1 \mid w[i, i+k-1] = s \}$$

(la slide scrive $1 \le i \le n$; perché il k-mero stia dentro $w$ serve $i \le n-k+1$.)

- Dizionario di tutti i fattori: $D(w) = \bigcup_{1 \le k \le |w|} D_k(w)$.
- **Posizioni** e **molteplicità** di un fattore $s$:

$$pos(w, s) = \{ 1 \le i \le |w| : w[i, i+|s|-1] = s \} \qquad mult(w, s) = |pos(w, s)|$$

(la slide scrive $w[i, i+|s|]$, che con estremi inclusi è lungo $|s|+1$.)

- Esercizi:
  - 1.1-1.3: generare DNA casuale con distribuzione **uniforme** e verificarla; poi **non uniforme** (A e T 30%, C e G 20%) e verificarla.
  - 1.4: verificare che un fattore $s$ sia contenuto in $w$.
  - 1.5: contare le occorrenze di $s$ in $w$ **con sovrapposizioni** (es. `count('AGAGA', 'AGA') = 2`) e confrontare con `str.count`, che dà 1.
  - 1.6-1.8: estrarre $D_2(w)$, poi $D_k(w)$ per $k$ qualsiasi, poi $D_k(w)$ con la **molteplicità** di ogni k-mero (un dict k-mero → conteggio).
  - 1.9: **indice di Jaccard** fra i dizionari di due sequenze:

$$J(A, B) = \frac{|A \cap B|}{|A \cup B|}$$

  - 1.10: **Jaccard generalizzato** su multi-insiemi ($m_A(x)$ = molteplicità di $x$ in $A$), da verificare sempre in $[0, 1]$:

$$GJ(A, B) = \frac{\sum_{x \in A \cup B} \min(m_A(x), m_B(x))}{\sum_{x \in A \cup B} \max(m_A(x), m_B(x))}$$

## Ordinamento
- `sorted(iterable, key=None, reverse=False)`: restituisce **sempre una lista** ordinata, da qualsiasi iterabile (anche un set).
- `lst.sort(key=None, reverse=False)`: ordina la lista **sul posto**, senza copia.
- Si possono ordinare le coppie di un dict con `sorted(my_dict.items())`, ma solo se le chiavi sono confrontabili: `{1:'one', 'two':2}` dà errore (`TypeError`) perché non c'è un ordine fra `1` e `'two'`. (Nella slide il codice ha `For` maiuscolo e `x = sorted(my_set):` con i due punti finali, entrambi errori di sintassi.)
- Esercizio 1.11: esaminare il valore di ritorno di `my_dict.items()` (aggiunta: è una vista `dict_items` di tuple chiave-valore).
- **Ordinare tuple per colonne** con `operator.itemgetter` (come ordinare un foglio di calcolo con una preferenza fra colonne). Record nel formato `(nome, gruppo sanguigno, età)`:

```python
from operator import itemgetter
my_tuples = {('john', 'A', 10), ('dave', 'B', 15), ('jane', 'A', 15)}
sorted(my_tuples)                          # per colonne da sinistra a destra
sorted(my_tuples, key=itemgetter(2))       # per età
sorted(my_tuples, key=itemgetter(2, 0, 1)) # per età, poi nome, poi gruppo
# [('john','A',10), ('dave','B',15), ('jane','A',15)]
```

- (Nota: con `key=itemgetter(2)` jane e dave hanno la stessa età; l'ordinamento è stabile, quindi il loro ordine dipende da quello di partenza, che per un set non è garantito.)

## Comprensione (list/set/dict comprehension)
- Costrutto di programmazione funzionale: `[ <valori generati> <uno o più for> <filtri> ]`.

```python
[True for i in range(3)]                    # [True, True, True]
[i for i in range(10) if i % 2 == 0]        # [0, 2, 4, 6, 8]
[(i, j) for i in range(3) for j in range(3) if i != j]   # pattern combinatori
[[j * i for j in range(3)] for i in range(3)]            # [[0,0,0],[0,1,2],[0,2,4]]
{i for i in range(3)}                       # set {0, 1, 2}
{i: i*2 for i in range(3)}                  # dict {0:0, 1:2, 2:4}
```

- Esercizi 1.12-1.14: tabelline dal 2 al 9 come lista di liste e come dict; tutte le combinazioni degli elementi di un insieme con e senza ripetizioni.

## Combinatoria: `zip` e `itertools`
- `zip` aggrega due o più liste elemento per elemento; serve per esempio a costruire un dict da chiavi e valori (`dict(zip(a, b))`).

```python
a, b = ['a', 'b', 'c'], [0, 1, 2]
for i in zip(a, b): print(i, end=' ')   # ('a', 0) ('b', 1) ('c', 2)
```

- **`itertools`**: iteratori efficienti per prodotti cartesiani (`product`), permutazioni (`permutations`), combinazioni (`combinations`, `combinations_with_replacement`), ecc.

```python
from itertools import *
for i in permutations('ABCD', 2): print(''.join(i), end=' ')   # AB AC AD BA ...
for i in permutations(range(3)): print(''.join(i), end=' ')
```

- (Errore nella seconda riga: `''.join` accetta solo stringhe, sugli interi di `range(3)` dà `TypeError`; serve `''.join(map(str, i))`.)
- Esercizi: 1.15 generare $\Gamma^k$ (aggiunta: `product('ACGT', repeat=k)`); 1.16 **nullomeri** = parole di $\Gamma^k$ assenti in una stringa $s$; 1.17 k-meri assenti in tutte le stringhe di una collezione. (La 1.17 definisce l'**elongazione** di un k-mero $w$, cioè $w \cdot x$ con $x \in \Gamma$, ma poi la consegna non la usa.)

## Funzioni
- Dichiarazione con `def nome(parametri):`, docstring opzionale come prima riga, corpo indentato, `return` opzionale.
- Valore di ritorno: opzionale, tipo non dichiarato, si possono restituire **più valori** (internamente una tupla, poi scomposta nell'assegnamento).
- Parametri: tipo non dichiarato; passaggio "per copia o riferimento come in Java" (vedi la precisazione sopra); **parametri opzionali** con valore di default; parametri passabili **per nome** in qualsiasi ordine.
- Versione corretta degli esempi delle slide:

```python
def count_AT(dna, lower_case=True):
    """this function returns the number of occurrences of
    A and T within a DNA sequence"""
    count_a = dna.count('A')
    count_t = dna.count('T')
    if lower_case:
        count_a += dna.count('a')
        count_t += dna.count('t')
    return count_a, count_t

my_sequence = 'ACcccGTtGAaCGggcTTaatGAC'
count_A, count_T = count_AT(my_sequence)
count_AT(my_sequence, lower_case=True)
count_AT(lower_case=False, dna=my_sequence)   # per nome, ordine libero
```

- (Errori negli esempi delle slide: mancano i `:` dopo `def count_A(dna)` e `def count_AT(...)`; si calcolano `count_a`/`count_t` ma si restituiscono `count_A`/`count_T`, cioè `NameError`; nella versione con `lower_case` le minuscole sono già contate nella prima riga e poi aggiunte di nuovo, quindi sono contate due volte; in `count_CG(s)` il corpo usa `dna` invece di `s`.)
- La slide dice che "i parametri senza default devono sempre essere i primi nella chiamata e seguire l'ordine dichiarato", ma l'esempio subito dopo passa `lower_case` prima di `dna`. (Precisazione: la regola vale per gli argomenti **posizionali**, che vanno prima di quelli per nome; nella **definizione** i parametri senza default precedono quelli con default. Con argomenti tutti per nome l'ordine è libero.)
- **Docstring**: va scritta bene (descrizione, `Parameters`, `Returns`). Si visualizza con `help(count_CG)` (la slide scrive `help(count_CG(s))`, che invece chiama la funzione e mostra l'help del valore restituito) oppure, in IPython/Jupyter, con `?count_CG` (o `count_CG?`), che mostra anche firma, file e tipo.
- **Visibilità**: le variabili definite dentro la funzione non sono visibili fuori (`NameError`); quelle definite fuori sono **visibili (in lettura) dentro**. (Aggiunta: per riassegnare una variabile globale dentro una funzione serve `global`.)

```python
b = 2
def foo():
    a = 10
    print(a, b)
foo()          # 10 2
print(a, b)    # NameError: name 'a' is not defined
```

## File I/O
- `open(filename, mode)` restituisce un **descrittore di file**:
  - `'r'` sola lettura (default), `'rb'` binario (default: testuale)
  - `'w'` scrittura, sovrascrive il file esistente
  - `'a'` append in coda
- Metodi:
  - `f.read()` tutto il file come unica stringa; `f.read(N)` i primi N byte (aggiunta: in modo testo sono N caratteri)
  - `f.readline()` la riga successiva; `f.readlines()` lista di tutte le righe
  - `f.write(str)` scrive una stringa. La slide dice che `f.write(str_list)` scrive una lista di stringhe come righe consecutive (errore: `write` accetta solo una stringa; per una lista c'è `f.writelines(lst)`, che non aggiunge i `\n`)
  - `f.close()` chiude il file, sia in lettura sia in scrittura
- La slide insiste su `f.flush()` per i file in scrittura. (Precisazione: `close()` fa già il flush, e `with` chiude da solo; `flush()` serve se il file resta aperto e i dati devono arrivare su disco subito.)

```python
f_in = open('my_file_in', 'r')
f_out = open('my_file_out', 'w')
for line in f_in.readlines():
    f_out.write(line)
f_out.flush()
f_out.close()
f_in.close()
```

- Il descrittore è **iterabile** sulle righe: `for line in open('my_file', 'r'): print(line)` (manca il `:` nella slide; `print` aggiunge un secondo a capo, si usa `end=''` o `line.rstrip()`). La slide dice che in questo caso il file si chiude automaticamente (precisazione: non è garantito dal linguaggio; in CPython si chiude quando l'oggetto viene raccolto dal garbage collector).
- Il costrutto **`with`** (context manager) chiude il file automaticamente anche in caso di eccezioni: è il modo consigliato.

```python
with open('my_file_out', 'w') as f_out:
    for line in open('my_file_in', 'r'):
        f_out.write(line)
```

## Eccezioni
```python
try:
    ...                      # codice che può lanciare un'eccezione
except <tipo> [as err]:      # ripetibile; cattura il tipo e le sue sottoclassi
    ...
else:
    ...                      # se non ci sono state eccezioni
finally:
    ...                      # sempre
```

- Se nessun `except` cattura il tipo lanciato, l'errore si propaga. La slide dice che si catturano tutti gli errori con `except Error:` (errore: in Python non esiste una classe `Error` built-in; si usa `except Exception:`, che copre tutte le eccezioni normali).
- Esempio delle slide: `try` esterno per apertura/chiusura (`except OSError as err`), `try` interno per la scrittura (`except IOError`, con `else` e `finally: f.close()`). (Aggiunta: in Python 3 `IOError` è un alias di `OSError`.)
- **`raise`** lancia un'eccezione: `raise ValueError("Date provided can't be in the past")`. Lista delle eccezioni built-in: docs.python.org/3/library/exceptions.html.
- **`assert`** per verificare condizioni:

```python
import sys
assert sys.version_info >= (3, 7), "Versione minima supportata 3.7."
```

(nella slide c'è una virgola doppia `, ,`, errore di sintassi.)

- Esercizio 1.18: scrivere un lettore di file **FASTA** (una o più sequenze, ognuna preceduta da una riga di descrizione che inizia con `>`, sequenza spezzata a capo ogni 80 caratteri; nell'esempio Pax-6 le righe sono di 60) che gestisca tutti i casi.

## Programmazione a oggetti (OOP)
La slide rimanda al file `Student.py` (qui `Esempio Python 3 OOP.py`), che mostra: dichiarazione di classe, `self`, variabili pubbliche e private, metodi d'istanza e statici (la slide scrive "funzioni di distanza", refuso per "di istanza"), override delle funzioni built-in, overloading degli operatori, ordinamento di oggetti custom.

### La classe `Student` dell'esempio
- **Attributi**: `distinctive_features` pubblico; `__age` **privato** perché inizia con `__`. (Precisazione: non è un vero privato, è **name mangling**: dall'esterno `s.__age` dà `AttributeError`, ma `s._Student__age` funziona.) Definiti a livello di classe sono attributi di classe; quelli assegnati in `__init__` con `self.x = ...` sono d'istanza.
- **Costruttore** `__init__(self, ...)`: ogni metodo d'istanza ha `self` come primo parametro.
- **Getter/modificatori** per il privato: `get_age()`, `getting_old()` (incrementa l'età).
- **Metodo "statico"** `scream()` senza `self`: si chiama come `Student.scream()`; `s.scream()` dà `TypeError` perché Python passa l'istanza come primo argomento. (Aggiunta: il modo standard è il decoratore `@staticmethod`, con cui il metodo si può chiamare anche da un'istanza.)
- **`__repr__`**: rappresentazione testuale dell'oggetto (analogo di `toString()` di Java), es. `|S,23,M|`.
- **`__hash__`**: valore hash, utile per usare l'oggetto in set e come chiave di dict; qui è l'hash di `__repr__`.
- **`__cmp`** privato (manca il `__` finale, quindi non è un metodo speciale del linguaggio): confronta per età e, a parità, per nome; restituisce negativo/0/positivo.
- **Overloading dei confronti** `__lt__, __gt__, __eq__, __le__, __ge__, __ne__`, tutti basati su `__cmp`: così `==`, `<` ecc. funzionano e **`sorted()`** può ordinare liste di `Student`.
- **`__add__`** ridefinisce `+`: restituisce un **nuovo** `Student` con la somma delle età. Il commento spiega perché non modificare `self`: gli operatori aritmetici di solito producono un nuovo oggetto.

```python
class Student:
    def __init__(self, name, age, sex, d_features):
        self.name = name
        self.__age = age
        self.sex = sex
        self.distinctive_features = d_features
    def get_age(self): return self.__age
    def getting_old(self): self.__age += 1
    def __repr__(self):
        return '|' + str(self.name) + ',' + str(self.__age) + ',' + str(self.sex) + '|'
    def __cmp(self, other):
        assert isinstance(other, Student)
        if self.__age == other.__age:
            if self.name == other.name: return 0
            return -1 if self.name < other.name else 1
        return self.__age - other.__age
    def __lt__(self, other): return self.__cmp(other) < 0
    def __eq__(self, other): return self.__cmp(other) == 0
    def __add__(self, other):
        return Student(self.name, self.__age + other.__age, self.sex, self.distinctive_features)
```

- Output dell'esecuzione (verificato): `S`, `22`, `23`, `Arrrrrgh!!!`, `s == s2` → `False`, `s1 == s2` → `False` (stessa età, nome diverso), `s1 < s` → `True`, `sorted([s, s1, s2])` → `[|S1,21,M|, |S2,21,M|, |S,23,M|]`, `s + s1` → `|S,44,M|`.
- (Difetti dell'esempio, non bloccanti: `__eq__` usa età e nome mentre `__hash__` usa anche il sesso, quindi due oggetti "uguali" possono avere hash diversi, contro la regola "uguali implica stesso hash"; l'hash cambia se l'oggetto cambia età, e un oggetto mutabile dentro un set si "perde"; l'`assert isinstance` fa sollevare `AssertionError` confrontando con un non-`Student`, mentre la convenzione è restituire `NotImplemented`.)

### Classi iterabili
- Per rendere una classe **iterabile** si ridefinisce `__iter__(self)`, che restituisce un oggetto **iteratore**; l'iteratore ridefinisce `__next__`, che lancia **`StopIteration`** alla fine. Classe principale e iteratore possono coincidere.

```python
class irange:
    def __init__(self, end, start=0):
        self.c = start
        self.end = end
    def __iter__(self):
        return irange(self.end, self.c)
    def __next__(self):
        self.c += 1
        if self.c >= self.end:
            raise StopIteration
        else:
            return self.c

for i in irange(10): print(i)
```

- (Errore: `__next__` incrementa **prima** di restituire, quindi `irange(10)` produce 1..9 e salta lo 0, verificato; per imitare `range` va restituito il valore corrente e poi incrementato.)
- Esercizi 1.19-1.20: classi per iterare i **k-meri** e i **k-nullomeri** di una stringa, indipendentemente dall'alfabeto.

## Da ricordare per il progetto
- Usare **Python 3**, notebook Jupyter Lab, ma attenzione all'**ordine di esecuzione** delle celle (prima della consegna: riavviare il kernel ed eseguire tutto).
- Fissare il **seme** (`random.seed`) per la **riproducibilità**.
- Mutabili (`list`, `dict`, `set`) contro immutabili (`str`, `tuple`, `frozenset`); assegnamento = alias, `copy` = shallow, `deepcopy` = copia completa.
- `str.count`/`replace` non contano le sovrapposizioni; `replace` di default sostituisce tutto.
- `sorted` restituisce una lista nuova, `sort`/`reverse`/`shuffle` lavorano sul posto e restituiscono `None`.
- `random.sample` senza ripetizione, `random.choices` con ripetizione (e pesi).
- Comprehension per costruire liste, set e dict; `itertools` per prodotti, permutazioni e combinazioni (es. $\Gamma^k$).
- File con `with open(...)`; eccezioni con `try/except/else/finally`, `raise`, `assert`.
- OOP: `__init__`, `self`, privati con `__`, `__repr__`, `__eq__`/`__lt__` per confronto e ordinamento, `__hash__` coerente con `__eq__`, `__iter__`/`__next__` per gli iterabili.
- Bag of words su DNA: $D_k(w)$, molteplicità, Jaccard e Jaccard generalizzato.
