# Lezione 8 - 26/10/2026: generate and test e le N regine

Fonte: `generate.pl`, l'unico file caricato su Elly per la lezione (niente slide). Le risposte riportate sotto sono state **eseguite** con SWI-Prolog 10.0.2.

## Lo schema generate and test

```prolog
num(1).
num(2).
num(3).

genera(X1,X2,X3,X4):- num(X2), X2=X3, num(X1), num(X4).

test(X1,X2,X3,X4):- X2 = X3.

soluzione(X1,X2,X3,X4):- genera(X1,X2,X3,X4), test(X1,X2,X3,X4).
```

- **Generate and test**: un predicato **genera** le soluzioni candidate (con il backtracking), un altro le **verifica**. Prolog le prova una alla volta: se il test fallisce si torna indietro e si genera il candidato successivo. È la forma più semplice di ricerca in uno spazio di soluzioni.
- Qui il problema giocattolo è: assegnare valori in {1,2,3} a quattro variabili con il vincolo `X2 = X3`.
- Il generatore puro avrebbe 3⁴ = **81** candidati. Questo `genera/4` invece **anticipa il vincolo**: fissa `X2`, impone subito `X2 = X3` e solo dopo enumera `X1` e `X4`. I candidati sono 3 · 3 · 3 = **27** (verificato), tutti già corretti, e il `test` non scarta mai niente.
- Morale: spostare i vincoli **dentro** la generazione, il prima possibile, taglia lo spazio di ricerca. È l'idea che porta alla programmazione a vincoli (CLP) e ad ASP.
- `?- soluzione(A,B,C,D).` → prima risposta `A = 1, B = 1, C = 1, D = 1`, 27 in tutto.
- `genera/4` e `genera/2` (sotto) sono predicati diversi: stesso nome, arità diversa.

## Generatore generico di assegnamenti

```prolog
genera(N,Allocazione) :- length(Allocazione,N),
                valori_ammessi(N,ListaValori),
                writeln(ListaValori),
                funzione(Allocazione,ListaValori).

valori_ammessi(N,[N|R]) :-
            N>0,
            M is N-1,
            valori_ammessi(M,R).
valori_ammessi(0,[]).

funzione([A|R],Cod) :-  member(A,Cod),
                        funzione(R,Cod).
funzione([],Cod).
```

- `length(Allocazione, N)` con `Allocazione` libera crea una lista di **N variabili fresche**: la "struttura" della soluzione.
- `valori_ammessi(N, L)` costruisce il dominio `[N, N-1, ..., 1]`: `?- valori_ammessi(3,V).` → `V = [3,2,1]`. L'ordine delle clausole non crea problemi: con `N = 0` la prima fallisce su `N > 0` e risponde la seconda.
- `funzione(Lista, Dominio)` assegna a ogni variabile un valore del dominio con `member`: è una **funzione** da {1..N} (le posizioni) a {1..N} (i valori). Le soluzioni sono tutte le N^N funzioni: `?- genera(3,A).` → prima risposta `A = [3,3,3]` (il dominio parte da N), 27 in tutto (verificato).
- `writeln(ListaValori)` è solo una stampa di debug: esce `[3,2,1]` a ogni chiamata.
- In `funzione([],Cod)` la variabile `Cod` è un singleton (warning di SWI): andrebbe `_`.

## Le N regine

```prolog
safe([]).
safe([Q|Qs]) :- safe(Qs),
nonattacca(Q,Qs).
nonattacca(X,Xs) :- natt(X,1,Xs).
natt(_X,_,[]).
natt(X,Offset,[Y|R]) :- X =\= Y+Offset, X =\= Y, X =\= Y-Offset,
                        N1 is Offset+1, natt(X,N1,R).
```

- Problema: mettere N regine su una scacchiera N×N senza che due si attacchino (stessa riga, stessa colonna o stessa diagonale).
- **Rappresentazione**: una lista di N numeri, l'elemento i-esimo è la **riga** della regina nella **colonna** i. Una regina per colonna è garantito dalla codifica stessa, quindi restano da controllare righe e diagonali.
- `safe(L)`: la lista è sicura se lo è la coda e la testa `Q` non attacca nessuna delle regine successive.
- `natt(X, Offset, Ys)`: `Offset` è la distanza in colonne fra `X` e la regina `Y` che si sta confrontando (parte da 1 e cresce). Tre vincoli:
  - `X =\= Y` - righe diverse
  - `X =\= Y + Offset` e `X =\= Y - Offset` - non sulla stessa diagonale (righe che differiscono quanto le colonne)
- `=\=` è la **disuguaglianza aritmetica**: valuta entrambi i lati, quindi vuole valori già istanziati. Per questo `safe` si può chiamare solo **dopo** la generazione.
- `?- safe([2,4,1,3]).` → `true`; `?- safe([1,2,3,4]).` → `false` (tutte sulla stessa diagonale).
- Il file non ha il predicato che mette insieme le due parti. (Aggiunta: va scritto `regine(N, Q) :- genera(N, Q), safe(Q).`, cioè generate and test.)
- Risultati (verificati), con `genera(N,Q), safe(Q)`:
  - N = 4: `[3,1,4,2]` e `[2,4,1,3]`, le 2 soluzioni
  - N = 6: 4 soluzioni
  - N = 8: le classiche **92 soluzioni**, ma in circa **47 secondi**: il generatore produce tutte le 8⁸ ≈ 16,8 milioni di funzioni e il test le scarta quasi tutte.
- (Aggiunta) È esattamente il limite del generate and test puro, e la lezione dello schema precedente: già generare **permutazioni** invece di funzioni (righe tutte diverse, 8! = 40.320 candidati) o controllare `nonattacca` mentre si piazza ogni regina (test anticipato) riduce lo spazio di ordini di grandezza. In CLP(FD) il vincolo si posta prima della ricerca e propaga.

## Da ricordare per l'orale
- Generate and test: generatore con backtracking + test; semplice ma esponenziale
- Anticipare i vincoli nella generazione riduce lo spazio (81 → 27 nel primo esempio)
- `length(L, N)` con `L` libera crea N variabili fresche
- N regine: codifica "una regina per colonna", vincoli su righe e diagonali con l'offset di colonna
- Gli operatori aritmetici di confronto (`=\=`, `<`, `>`) vogliono argomenti istanziati: il test si fa dopo la generazione
