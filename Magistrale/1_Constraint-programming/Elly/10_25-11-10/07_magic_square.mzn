%
% Magic square integer programming version in MiniZinc.
%
% In recreational mathematics, a magic square of order n is an
% arrangement of n^2 numbers, usually distinct integers, in a square,
% such that n numbers in all rows, all columns, and both diagonals sum
% to the same constant. A normal magic square contains the integers
% from 1 to n^2.
%
% (From Wikipedia, the free encyclopedia.)


include "globals.mzn";

% square order
int: n = 6;
int: m = n*n;

array[1..n, 1..n] of var 1..n*n: x;

var int: s;

s = (sum(i in 1..n*n)(i)) div n; % the magic sum



constraint
   s >= 0
   /\
   s <= n*n*n
   /\
%   /\ s=40
  alldifferent([ x[i, j] | i , j in 1..n])
  /\
  % the sum in each row must be the magic sum
  forall(i in 1..n) (
     sum(j in 1..n) (x[i,j]) = s
  )

  /\
  % the sum in each column must be the magic sum
  forall(j in 1..n) (
     sum(i in 1..n) (x[i,j]) = s
  )

  /\
  % the sum in each diagonal
     sum(i in 1..n) (x[i,i]) = s
  /\
     sum(i in 1..n) (x[i,n-i+1]) = s


%   /\ x[1,1] < x[1,n]

%    /\ x[1,1] < x[n,1]

%    /\ x[1,1] < x[n,n]

%   /\ x[1,n] < x[n,1]

 ;


solve satisfy;
%solve :: int_search([s], most_constrained, indomain_split, complete) satisfy;

output
[
  if j = 1 then "\n" else " " endif
  ++
  show(x[i,j])
  | i, j in 1..n
]  ++ ["\n s=" ++ show(s)];
