# Lezione 5 - 13/10/2026: primi programmi Prolog e macchina di Turing

Fonte: `test.pl` e `mdt.pl`, i due file caricati su Elly per la lezione (niente slide). Le lezioni 2-4 non hanno materiale su Elly. Le query e le risposte riportate sotto sono tracciate a mano sulla risoluzione SLD, non eseguite (sul fisso non c'è SWI-Prolog).

## `test.pl` - esempi di base

### Chiusura transitiva e ordine di selezione SLD
Fatti: `p(a,b).` e `p(b,c).` `q/2` è la **chiusura transitiva** di `p` (raggiungibilità), scritta in tre versioni di cui solo una è attiva nel file:

```prolog
%% versione 1
q(X,Y):- p(X,Y).
q(X,Y):- p(X,Z),q(Z,Y).

%% versione 2: stesse clausole, ordine invertito
% q(X,Y):- p(X,Z),q(Z,Y).
% q(X,Y):- p(X,Y).

%% versione 3: ricorsione a sinistra
% q(X,Y):- q(Z,Y),p(X,Z).
% q(X,Y):- p(X,Y).
```

- La **regola di selezione** di Prolog è fissa: fra le **clausole** si prova prima quella più in alto nel listato, nel **body** si risolve prima l'atomo più a sinistra. La semantica logica delle tre versioni è la stessa, il comportamento operazionale no.
- **Versione 1**, `?- q(a,Y).` → `Y = b ; Y = c ; false.` Prima il caso base, poi un passo di `p` e la ricorsione.
- **Versione 2**, stessa query: stesse risposte in ordine inverso, `Y = c ; Y = b`, perché si scende in ricorsione prima di provare il caso base. Termina comunque, perché `p(X,Z)` a sinistra consuma un arco a ogni passo.
- **Versione 3**: **va in loop**, come dice il commento del file. Il primo atomo del body è di nuovo `q(Z,Y)` con `Z` libera, quindi l'albero SLD ha un ramo infinito più a sinistra e Prolog non arriva mai alla seconda clausola né a `p`. Non dà nemmeno una risposta: finisce con lo stack esaurito. Morale: nel caso ricorsivo l'atomo che fa avanzare (qui `p`) va messo prima della chiamata ricorsiva.

### Numeri di Peano
```prolog
num(0).
num(s(X)) :- num(X).
```
- I naturali come termini: `0`, `s(0)`, `s(s(0))`, ... con `s` = successore.
- `?- num(X).` enumera all'infinito `X = 0 ; X = s(0) ; X = s(s(0)) ; ...`

### Liste
- Una lista si può codificare a mano con un funtore binario e una costante per la lista vuota: `l(a,vuoto)` è `[a]`, `l(a,l(b,vuoto))` è `[a,b]`.
- Prolog ha la sintassi nativa: `[]` è la lista vuota, `[Testa | Coda]` la cella. `[a,b]` è `[a | [b]]`, cioè `[a | [b | []]]`.
- Riconoscere una lista:

```prolog
lista([]).
lista([ _ |Y]) :- lista(Y).
```

### Somma e lunghezza con `is`
```prolog
% somma(Somma_in_output, Lista)
somma(0,[]).
somma(S,[X|Y]) :- somma(S1,Y), S is S1 + X.

len(0,[]).
len(S,[_|Y]) :- len(S1,Y), S is S1 + 1.
```
- `is` valuta l'**espressione aritmetica** a destra e la unifica con il termine a sinistra. Senza `is`, `S1 + X` resta il termine `+(S1,X)`, non un numero.
- L'output sta nel primo argomento, per convenzione del file.
- `?- somma(S,[1,2,3]).` → `S = 6`; `?- len(N,[a,b,c]).` → `N = 3`.
- L'ordine nel body conta anche qui: `is` vuole la destra già **istanziata**, quindi va dopo la chiamata ricorsiva che calcola `S1`. Messo prima, darebbe un errore di istanziazione. (Aggiunta mia, non nel file: nessuna delle due è ricorsiva in coda, e con la lista libera, `?- somma(S,L).`, la prima risposta è `S = 0, L = []` ma la seconda dà errore, perché `X` non è istanziata quando arriva `is`.)

## `mdt.pl` - macchina di Turing in Prolog

Un **simulatore di macchina di Turing**: il programma della macchina è un insieme di fatti, l'esecuzione è la ricerca SLD.

### Il programma della macchina
`delta/5` è la **funzione di transizione**: `delta(StatoCorrente, SimboloLetto, NuovoStato, NuovoSimbolo, Movimento)`, con movimento `l` (sinistra) o `r` (destra). `elementoVuoto` è il **blank**.

```prolog
delta(q0,0,q1,1,l).
delta(q2,1,q2,0,r).
delta(q0,elementoVuoto,q1,1,l).
delta(q1,elementoVuoto,q2,0,r).

statoFinale(q2).

stato(X):- delta(X,_,_,_,_).
```
- `stato/1` ricava gli stati da `delta`: lo sono tutti quelli che hanno almeno una transizione uscente (non è usato dal resto del programma).

### Il nastro
- `nastro(ListaL, Current, ListaR)`: `Current` è la cella sotto la testina, `ListaL` le celle a sinistra **a partire dalla più vicina**, `ListaR` quelle a destra, sempre dalla più vicina. Così spostarsi costa solo togliere o mettere una testa di lista.
- Il nastro è infinito ma rappresentato finito: quando una lista finisce, la cella nuova è `elementoVuoto`.

### Calcolo e passo
```prolog
calcolo(NastroFinale,StatoFinale,NastroFinale,StatoFinale):-
            statoFinale(StatoFinale).
calcolo(NastroFinale,StatoFinale,Nastro,Stato):-
            passo(Nastro,Stato,Nastro1,Stato1),
            % \+ statoFinale(Stato1),
            calcolo(NastroFinale,StatoFinale,Nastro1,Stato1).

passo(Nastro, Stato, NuovoNastro, NuovoStato):-
    Nastro = nastro(L,Current, R),
    delta(Stato,Current, NuovoStato, NuovoSimbolo, Spostamento),
    updateNastro(nastro(L,Current,R),NuovoNastro, NuovoSimbolo, Spostamento).
```
- `calcolo/4`: i primi due argomenti sono l'**output** (nastro e stato finali), gli ultimi due l'input. Caso base: se lo stato corrente è finale, il nastro corrente è il risultato. Altrimenti si fa un `passo` e si ricorre.
- `passo/4` legge il simbolo sotto la testina, cerca una transizione in `delta` e aggiorna il nastro.
- Il controllo `\+ statoFinale(Stato1)` è commentato, e la seconda clausola di `calcolo` non verifica che lo stato non sia finale. Quindi la macchina si ferma alla prima configurazione finale, ma **sul backtracking prosegue oltre** se da lì esiste una transizione: con questo `delta` succede, perché `q2` è finale e ha `delta(q2,1,q2,0,r)`. (Aggiunta mia: togliere il commento così com'è non funziona, perché vieterebbe proprio i passi che entrano in uno stato finale, e la macchina non accetterebbe mai. La guardia giusta è sullo stato corrente, `\+ statoFinale(Stato)` prima di `passo`.)
- Se non c'è transizione per lo stato e il simbolo correnti, e lo stato non è finale, `calcolo` fallisce: la macchina si blocca senza accettare.

### Aggiornamento del nastro
```prolog
% spostamento a sinistra, nessuna cella a sinistra: arriva un blank
updateNastro(nastro([],_,R),nastro(NL,NC,NR),Simbolo,l):-
      NL = [], NR = [Simbolo|R], NC = elementoVuoto.
% spostamento a sinistra
updateNastro(nastro([X|Y],_,R),nastro(NL,NC,NR),Simbolo,l):-
      NL = Y, NR = [Simbolo|R], NC = X.
% spostamento a destra, nessuna cella a destra: arriva un blank
updateNastro(nastro(L,_,[]),nastro(NL,NC,NR),Simbolo,r):-
      NL = [Simbolo|L], NR = [], NC = elementoVuoto.
% spostamento a destra
updateNastro(nastro(L,_,[X|Y]),nastro(NL,NC,NR),Simbolo,r):-
      NL = [Simbolo|L], NR = Y, NC = X.
```
- Il simbolo scritto finisce nella cella appena lasciata: va in testa a `R` se ci si sposta a sinistra, in testa a `L` se ci si sposta a destra. La nuova cella corrente è la testa della lista dal lato del movimento, oppure `elementoVuoto` se quella lista è vuota.
- Le uscite sono scritte con unificazioni esplicite nel body (`NL = ...`). Metterle direttamente nella testa sarebbe equivalente.
- (Nel file tutte e quattro le clausole hanno lo stesso commento a disegno, `... e d | C | b c ...` → `... e | d | Simbolo b c ...`, che descrive lo spostamento a sinistra con cella disponibile: va bene solo per la seconda. Qui i commenti sono stati sostituiti con quello che fa ciascuna clausola.)

### Esempio tracciato
Il file non contiene una query. Partendo da un nastro con il solo `0` in stato `q0`:

```prolog
?- calcolo(NF, SF, nastro([],0,[]), q0).
```

1. `q0` legge `0`: scrive `1`, va a sinistra, passa in `q1`. A sinistra non c'è niente: `nastro([], elementoVuoto, [1])`.
2. `q1` legge il blank: scrive `0`, va a destra, passa in `q2`: `nastro([0], 1, [])`.
3. `q2` è finale → prima risposta `NF = nastro([0],1,[]), SF = q2`.
4. Sul backtracking (`;`): `q2` legge `1`, scrive `0` e va a destra → `nastro([0,0], elementoVuoto, [])`, ancora `q2` finale → seconda risposta. Poi `q2` sul blank non ha transizioni → `false`.
