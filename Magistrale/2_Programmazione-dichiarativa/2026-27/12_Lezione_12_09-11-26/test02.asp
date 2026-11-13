numero(1..10).
possibile(X):- numero(X).

scelto(X) :- possibile(X), not non_scelto(X).
non_scelto(X) :- possibile(X), not scelto(X).

almeno_2 :- scelto(X),scelto(Y), X != Y.
almeno_3 :- scelto(X),scelto(Y),scelto(Z), X != Y, Y != Z, X != Z.

:- almeno_3.


almeno_1 :- scelto(X). 

:- not almeno_1.

#show scelto/1.
