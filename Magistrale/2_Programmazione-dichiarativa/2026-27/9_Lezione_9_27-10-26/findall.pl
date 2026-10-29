p(1).
p(2).
p(a).
p(1).

p(X1) :- p(X), X=2, X1 is X+1.

go :- findall(X, p(X), L), 
      writeln_rec(L).

writeln_rec([]).
writeln_rec([H|T]) :- writeln(H), writeln_rec(T).