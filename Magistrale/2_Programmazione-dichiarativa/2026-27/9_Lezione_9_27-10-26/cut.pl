p(1).
p(5).

a(motivo_1) :- p(X), X>2,writeln(X),!, fail.
a(motivo_2) :- p(X), X<2.
a(motivo_3) :- p(X), X=2,!.

b(X):-a(X).
b(X):-p(X).