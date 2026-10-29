
num(1).
num(2).
num(3).

genera(X1,X2,X3,X4):- num(X2), X2=X3, num(X1), num(X4).

test(X1,X2,X3,X4):- X2 = X3.

soluzione(X1,X2,X3,X4):- genera(X1,X2,X3,X4), test(X1,X2,X3,X4).

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

safe([]).
safe([Q|Qs]) :- safe(Qs),
nonattacca(Q,Qs).
nonattacca(X,Xs) :- natt(X,1,Xs).
natt(_X,_,[]).
natt(X,Offset,[Y|R]) :- X =\= Y+Offset, X =\= Y, X =\= Y-Offset,
                        N1 is Offset+1, natt(X,N1,R).