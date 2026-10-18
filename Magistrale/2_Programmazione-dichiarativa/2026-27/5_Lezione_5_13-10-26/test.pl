p(a,b).
p(b,c).

%% versione 1
q(X,Y):- p(X,Y).
q(X,Y):- p(X,Z),q(Z,Y).

%% versione 2
% q(X,Y):- p(X,Z),q(Z,Y).
% q(X,Y):- p(X,Y).

%% versione 3 --> va in loop a causa dell'ordine di selezione SLD di 
%%                regola (prima nel listato) e atomo nel body (piu' a sinistra)
% q(X,Y):- q(Z,Y),p(X,Z).
% q(X,Y):- p(X,Y).


num(0).
num(s(X)) :- num(X).

% [a]
l(a,vuoto).
% [a,b]
l(a,l(b,vuoto)).
% [a | restodella lista]
% [a | [b]]

lista([]).
lista([ _ |Y]) :- lista(Y).

% somma(Somma_in_output, Lista)
somma(0,[]).
somma(S,[X|Y]) :- somma(S1,Y), S is S1 + X.

% somma(Somma_in_output, Lista)
len(0,[]).
len(S,[_|Y]) :- len(S1,Y), S is S1 + 1.