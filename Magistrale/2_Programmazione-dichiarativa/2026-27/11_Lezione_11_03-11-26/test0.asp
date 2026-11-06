%%% due modelli
%a :- not b.
%b :- not a.

% %%% tre modelli p1,p2,p3
% p1 :- not p2, not p3.
% p2 :- not p1, not p3.
% p3 :- not p1, not p2.

% %%% tre modelli {t1,t2}, {t1,t3}, {t2,t3}
% t1 :- p1.
% t2 :- p1.

% t1 :- p2.
% t3 :- p2.

% t2 :- p3.
% t3 :- p3.   

%%% tre modelli {a}, {b}, {a,b}
% a :- p1.
% b :- p2.
% a :- p3.
% b :- p3.   

% a :- not non_a.
% non_a :- not a.

% b :- not non_b.
% non_b :- not b.

% :- non_a, non_b.

a(vero) :- not a(falso).
a(falso) :- not a(vero).

b(vero) :- not b(falso).
b(falso) :- not b(vero).

:- a(falso), b(falso).