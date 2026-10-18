% programma in input: delta/5 (stato corrente, simbolo corrente, nuovo stato, nuovo simbolo, movimento)
delta(q0,0,q1,1,l).
delta(q2,1,q2,0,r).
delta(q0,elementoVuoto,q1,1,l).
delta(q1,elementoVuoto,q2,0,r).

statoFinale(q2).


stato(X):- delta(X,_,_,_,_).


% nastro(ListaL,Current,ListaR)
% ListaL = [], [X], ...

% Passo di calcolo
% Input: nastro corrente , stato corrente, 
% output: nuovo nastro, nuovo stato

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

updateNastro(nastro([],_,R),nastro(NL,NC,NR),Simbolo,l):-
% ... $ $ $ e d | C | b c $ $ $ $ $ ...
% ... $ $ $ e | d | Simbolo b c $ $ $ $ $ ...
      NL = [],
      NR = [Simbolo|R],
      NC = elementoVuoto.
updateNastro(nastro([X|Y],_,R),nastro(NL,NC,NR),Simbolo,l):-
% ... $ $ $ e d | C | b c $ $ $ $ $ ...
% ... $ $ $ e | d | Simbolo b c $ $ $ $ $ ...
      NL = Y,
      NR = [Simbolo|R],
      NC = X.

updateNastro(nastro(L,_,[]),nastro(NL,NC,NR),Simbolo,r):-
% ... $ $ $ e d | C | b c $ $ $ $ $ ...
% ... $ $ $ e | d | Simbolo b c $ $ $ $ $ ...
      NL = [Simbolo|L],
      NR = [],
      NC = elementoVuoto.
updateNastro(nastro(L,_,[X|Y]),nastro(NL,NC,NR),Simbolo,r):-
% ... $ $ $ e d | C | b c $ $ $ $ $ ...
% ... $ $ $ e | d | Simbolo b c $ $ $ $ $ ...
      NL = [Simbolo|L],
      NR = Y,
      NC = X.
