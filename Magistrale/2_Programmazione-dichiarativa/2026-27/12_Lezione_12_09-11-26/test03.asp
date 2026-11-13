numero(1..100).
possibile(X):- numero(X).

p(X,Y):- possibile(X), possibile(Y).
p(X,Y,Z):- possibile(X), possibile(Y), possibile(Z).
p(X,Y,Z,W):- possibile(X), possibile(Y), possibile(Z), possibile(W).  