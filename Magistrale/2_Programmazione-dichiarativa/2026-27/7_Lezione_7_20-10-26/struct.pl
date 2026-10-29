%%% struttura dati "struct"

%struct(X,Y,Z).

struct(abc,1234,qwer).
struct(abcd,12345,qwer).

struct(abcd1,f(1,2),qwer2).
struct(abcd2,f(2,2),qwer3).
struct(abcd3,f(1,3),qwer4).

struct(1,abcd1,f(1,2),qwer2).
struct(2,abcd2,f(2,2),qwer3).
struct(3,abcd3,f(1,3),qwer4).

l(1,l(5,l(6,nil))).

p([1,2,3,4,5]).

member(X, [X | _Resto]).
member(X, [A | Resto]) :- member(X, Resto).

prefix([], _ ).
prefix([A | R], [A | S]) :- prefix(R, S).

len([], 0).
len([_ | R], N) :- len(R, M), N is M + 1.

len2([], X, X).
len2([_ | R], N, Result) :- M is N + 1, len2(R, M, Result).


membertree(X, tree(X,_ ,_ )).
membertree(X, tree(_ ,L,R)) :- membertree(X,L).
membertree(X, tree(_ ,L,R)) :- membertree(X,R).


%edge(a ,a).
edge(a ,b).
edge(b ,a).
edge(b ,d).
edge(a ,c).
edge(c ,e).
edge(d ,f).
edge(e ,f).

connesso(X,Y,Path,Path) :- edge(X,Y).
connesso(X,Y,Path, Result ) :- edge(X,Z), non_member([Z,X],Path),connesso(Z,Y, [X|Path],Result).