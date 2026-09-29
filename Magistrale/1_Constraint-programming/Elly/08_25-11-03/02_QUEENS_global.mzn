int: n=8;                                 % The number of queens.

array [1..n] of var 1..n: q;

include "globals.mzn";


constraint all_different(q)::domain; %% the annotation "domain" tells the solver to use domain propagation (gecode default is bounds consistency!);
constraint all_different(i in 1..n)(q[i] + i)::domain;

constraint all_different(i in 1..n)(q[i] - i)::domain;

%solve satisfy;
solve :: int_search(q,
input_order,
% first_fail,
 %most_constrained,
 indomain_min,
 complete) satisfy;
output [ show(q)];