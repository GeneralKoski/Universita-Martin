numero(1..10).
possibile(X):- numero(X).

scelto(X) :- possibile(X), not non_scelto(X).
non_scelto(X) :- possibile(X), not scelto(X).
p :- scelto(X),scelto(Y), X != Y.

:- not p.


#show scelto/1.