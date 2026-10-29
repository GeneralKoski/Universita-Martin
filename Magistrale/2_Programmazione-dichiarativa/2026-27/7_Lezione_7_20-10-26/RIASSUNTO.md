# Lezione 7 - 20/10/2026: termini composti, liste, alberi e cammini su grafi

Fonte: `struct.pl`, l'unico file caricato su Elly per la lezione (niente slide). La lezione 6 non ha materiale su Elly. Le risposte riportate sotto sono state **eseguite** con SWI-Prolog 10.0.2.

## Termini composti come strutture dati

```prolog
struct(abc,1234,qwer).
struct(abcd,12345,qwer).

struct(abcd1,f(1,2),qwer2).
struct(abcd2,f(2,2),qwer3).
struct(abcd3,f(1,3),qwer4).

struct(1,abcd1,f(1,2),qwer2).
struct(2,abcd2,f(2,2),qwer3).
struct(3,abcd3,f(1,3),qwer4).
```

- In Prolog non ci sono record o tipi: un fatto è già una **tabella**, e un termine composto come `f(1,2)` è un campo strutturato. Il commento `%struct(X,Y,Z).` del file ricorda lo "schema".
- `struct/3` e `struct/4` sono **predicati diversi**: in Prolog un predicato è identificato da nome **e** arità (`nome/arità`).
- Le interrogazioni sono **pattern matching** per unificazione, anche dentro i sottotermini:
  - `?- struct(X,Y,Z).` → le 5 righe di `struct/3`, nell'ordine del listato
  - `?- struct(N,A,f(1,B),C).` → `N = 1, A = abcd1, B = 2, C = qwer2 ; N = 3, A = abcd3, B = 3, C = qwer4` (solo le righe con `f` e primo argomento 1)
  - `?- struct(_, f(P,Q), _).` → le tre righe con un `f(_, _)` in seconda posizione: `struct(abc,1234,qwer)` non unifica, perché `1234` non è un termine `f(_,_)`
- Il primo argomento di `struct/4` fa da **chiave** (1, 2, 3), come un id in una tabella.

## Liste

### Codifica a mano e notazione nativa
```prolog
l(1,l(5,l(6,nil))).
p([1,2,3,4,5]).
```
- `l(Testa, Coda)` con `nil` per la lista vuota è la stessa idea della lezione 5: `l(1,l(5,l(6,nil)))` è la lista 1, 5, 6. `?- l(H, l(H2, T)).` → `H = 1, H2 = 5, T = l(6,nil)`.
- Con la sintassi nativa: `?- p(L), L = [Hd|Tl].` → `Hd = 1, Tl = [2,3,4,5]`.

### `member/2`
```prolog
member(X, [X | _Resto]).
member(X, [A | Resto]) :- member(X, Resto).
```
- Caso base: `X` è la testa. Caso ricorsivo: `X` sta nella coda.
- Si usa **in entrambe le direzioni**: `?- member(b,[a,b,c]).` → `true` (verifica); `?- member(M,[a,b,c]).` → `M = a ; M = b ; M = c` (generazione).
- La variabile `A` nella seconda clausola è un **singleton**, e SWI dà un warning al caricamento: andrebbe scritta `_` o `_A`. Stesso warning per `R` e `L` in `membertree`.
- `member/2` esiste già nella libreria `lists` di SWI: ridefinirlo nel proprio file funziona (la definizione utente ha la precedenza sull'autoload), ma in un progetto vero meglio un nome diverso.

### `prefix/2`
```prolog
prefix([], _ ).
prefix([A | R], [A | S]) :- prefix(R, S).
```
- La lista vuota è prefisso di tutto; altrimenti le teste devono coincidere e si prosegue sulle code.
- `?- prefix(P,[1,2,3]).` → `P = [] ; P = [1] ; P = [1,2] ; P = [1,2,3]` (dal più corto, perché il caso base è la prima clausola). `?- prefix([2],[1,2,3]).` → `false`.

### Lunghezza: ricorsione semplice e con accumulatore
```prolog
len([], 0).
len([_ | R], N) :- len(R, M), N is M + 1.

len2([], X, X).
len2([_ | R], N, Result) :- M is N + 1, len2(R, M, Result).
```
- `len` calcola la lunghezza della coda e **poi** aggiunge 1: il lavoro si fa al ritorno dalla ricorsione, quindi lo stack cresce con la lista.
- `len2` usa un **accumulatore**: `N` è il conteggio parziale, si incrementa **prima** della chiamata ricorsiva, e alla lista vuota l'accumulatore viene copiato nel risultato (`len2([], X, X)`). È **ricorsiva in coda** (*tail recursive*): la chiamata ricorsiva è l'ultimo goal, e Prolog può riusare il frame (ottimizzazione dell'ultima chiamata). Si chiama con l'accumulatore a 0.
- `?- len([a,b,c],N).` → `N = 3`; `?- len2([a,b,c],0,N).` → `N = 3`.
- Al contrario, con la lista libera: `?- len(L,2).` e `?- len2(L,0,2).` danno come prima risposta `L = [_,_]`, ma **chiedendo altre risposte non terminano**: la ricorsione continua a generare liste sempre più lunghe, nessuna delle quali ha lunghezza 2. (Verificato: entrambe esauriscono il limite di tempo dopo la prima risposta.)

## Alberi binari
```prolog
membertree(X, tree(X,_ ,_ )).
membertree(X, tree(_ ,L,R)) :- membertree(X,L).
membertree(X, tree(_ ,L,R)) :- membertree(X,R).
```
- Un albero binario è un termine `tree(Valore, Sinistro, Destro)`; la foglia vuota non ha una clausola (il file non la nomina, sotto si usa `nil`).
- `membertree` è il `member` sugli alberi: il valore è nella radice, oppure nel sottoalbero sinistro, oppure nel destro. È una **visita in profondità in pre-ordine**.
- `?- membertree(E, tree(1, tree(2,nil,nil), tree(3,nil,nil))).` → `E = 1 ; E = 2 ; E = 3`. Su `nil` nessuna clausola unifica, quindi `false`.

## Cammini su un grafo
```prolog
%edge(a ,a).
edge(a ,b).
edge(b ,a).
edge(b ,d).
edge(a ,c).
edge(c ,e).
edge(d ,f).
edge(e ,f).

connesso(X,Y,Path,Path) :- edge(X,Y).
connesso(X,Y,Path, Result ) :- edge(X,Z), non_member([Z,X],Path),connesso(Z,Y, [X|Path],Result).
```
- Grafo orientato con un **ciclo** `a → b → a` (e un cappio `a → a` commentato). La raggiungibilità ingenua `conn(X,Y) :- edge(X,Z), conn(Z,Y)` qui andrebbe in loop sul ciclo: per questo si porta dietro il **cammino percorso** (`Path`, i nodi già visitati) e si scartano i nodi già visti.
- `Result` restituisce il cammino; `Path` parte da `[]`.
- **Il file così com'è non funziona** (verificato):
  - `non_member/2` **non è definito**: `?- connesso(a,f,[],R).` dà `Unknown procedure: non_member/2`. Anche `?- connesso(a,b,[],R).` dà come prima risposta `R = []` (arco diretto) ma l'errore appena si chiede la successiva.
  - Anche definendolo come `non_member(X,L) :- \+ member(X,L).`, il controllo è sulla **coppia** `[Z,X]`, mentre `Path` contiene **nodi**: la coppia non c'è mai, il controllo passa sempre e il ciclo `a → b → a` torna a fare loop (verificato: la query non termina).
  - Il caso base restituisce `Path` senza aggiungere `X` e `Y`, quindi il cammino risultante è incompleto.
- (Aggiunta, non nel file) Versione corretta e verificata, con il controllo sul nodo e il cammino completo (in ordine inverso):

```prolog
non_member(X, L) :- \+ member(X, L).

connesso(X, Y, Path, [Y,X|Path]) :- edge(X, Y).
connesso(X, Y, Path, Result) :-
    edge(X, Z), non_member(Z, [X|Path]),
    connesso(Z, Y, [X|Path], Result).
```

  `?- connesso(a,f,[],R).` → `R = [f,d,b,a] ; R = [f,e,c,a]`, i due cammini semplici da `a` a `f`. `\+` è la **negazione per fallimento**: `\+ G` riesce se `G` fallisce (vedi lezione 9, `!, fail`).

## Da ricordare per l'orale
- Predicato = nome/arità: `struct/3` e `struct/4` sono distinti
- L'unificazione fa pattern matching anche dentro i termini composti
- I predicati su liste funzionano in più direzioni (verifica e generazione), ma non sempre terminano con argomenti liberi (`len(L,2)`)
- Accumulatore e ricorsione in coda: `len2` contro `len`
- Visita di un grafo con ciclo: serve la lista dei visitati, altrimenti la ricerca SLD non termina
