vola(X) :- uccello(X), not anormale(X).
anormale(X) :- pinguino(X).
uccello(X) :- pinguino(X).
uccello(tweety).
pinguino(skippy).