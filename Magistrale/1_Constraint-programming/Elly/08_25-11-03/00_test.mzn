int: n=4;

array [1..n] of var 1..n: x;
%array [1..n] of var 1..n-1: x;

constraint
   forall(i,j in 1..n where i!=j) (x[i] !=  x[j]);

%constraint
%    (x[n]   <  x[1]);

solve satisfy;

output [ show(x)];