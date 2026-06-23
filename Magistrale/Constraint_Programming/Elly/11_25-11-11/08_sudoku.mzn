 % Sudoku solver.

 include "globals.mzn";

 array [1..9, 1..9] of var 1..9: sq;
%  array [1..9, 1..9] of var 0..1: b;

predicate row_diff(int: r) =
  alldifferent([ sq[r, j] | j in 1..9]);

% row constraint
constraint forall(i in 1..9)
         (row_diff(i)) ;

% column constraint
constraint forall(i in 1..9)
  (alldifferent([ sq[j, i] | j in 1..9])) ;

% block constraint
predicate block_diff(int: r, int: c) =
        alldifferent([ sq[r + j, c + k] | j,k in 0..2]);

constraint forall(i,j in 0..2)
   ( block_diff(3*i+1,3*j+1)) ;


% constraint forall(i in 1..8)
%    (sq[1,i]<sq[1,i+1]) ;


%%% 111 222 333
%%% 111 222 333
%%% 111 222 333
%%% 444 555 666
%%% 444 555 666
%%% 444 555 666
%%% 777 888 999
%%% 777 888 999
%%% 777 888 999

  sq =
%    [| _, _, _, _, 1, _, _, _, _
%     | _, _, _, 2, _, _3, _, _, _
%     | _, _, 4, _, _, _, _5, _, _
%     | _, 6, _, _, _, _, _, _7, _
%     | 8, _, _, _, 5, _, _, _, _9
%     | _, 1, _, _, _, _, _, 3, _
%     | _, _, 5, _, _, _, 4, _, _
%     | _, _, _, 7, _, 1, _, _, _
%     | _, _, _, _, 9, _, _, _, _
%     |];
%
 [| _, _, 1, 6, _, _, _, _, _
  | _, _, _, _, 3, 2, 6, _, _
  | 3, 8, _, _, _, _, _, 2, _
  | 5, 3, _, _, _, 7, _, _, 8
  | _, _, _, _, _, _, _, _, _
  | 6, _, _, 9, _, _, _, 4, 5
  | _, 1, _, _, _, _, _, 3, 9
  | _, _, 9, 4, 5, _, _, _, _
  | _, _, _, _, _, 8, 7, _, _
  |];
%  [| _, _, _, _, _, _, _, _, _
%   | _, 6, 8, 4, _, 1, _, 7, _
%   | _, _, _, _, 8, 5, _, 3, _
%   | _, 2, 6, 8, _, 9, _, 4, _
%   | _, _, 7, _, _, _, 9, _, _
%   | _, 5, _, 1, _, 6, 3, 2, _
%   | _, 4, _, 6, 1, _, _, _, _
%   | _, 3, _, 2, _, 7, 6, 9, _
%   | _, _, _, _, _, _, _, _, _
%   |];

 % [| _, _, 1, _, _, _, _, _, _
 %  | _, _, 2, _, 3, 1, _, _, 4
 % | _, _, _, 5, _, _, 6, _, 7
 %  | 5, _, _, 1, 4, _, _, _, _
 %  | _, 7, _, _, _, _, _, 2, _
 %  | _, _, _, _, 7, 8, _, _, 9
 %  | 8, _, 7, _, _, 9, _, _, _
 %  | 4, _, _, _, 6, _, 3, _, _
 %  | _, _, _, _, _, _, 5, _, _
 % |];
%   [| _, _, 6, _, _, _, _, 9, _
%    | _, _, _, 5, _, 1, 7, _, _
%    | 2, _, _, 9, _, _, 3, _, _
%    | _, 7, _, _, 3, _, _, 5, _
%    | _, 2, _, _, 9, _, _, 6, _
%    | _, 4, _, _, 8, _, _, 2, _
%    | _, _, 1, _, _, 3, _, _, 4
%    | _, _, 5, 2, _, 7, _, _, _
%    | _, 3, _, _, _, _, 8, _, _
%    |];

%solve satisfy;
solve :: int_search([sq[i,j] | i,j in 1..9], most_constrained, outdomain_max, complete) satisfy;

output[
  if j = 1 then "\n" else " " endif
  ++
  show(sq[i,j])
  | i, j in 1..9
] ;







% predicate row_diff(int: r) =
%      all_different (c in 1..9) (sq[r, c])  :: domain; %% the annotation "domain" tells the solver to use domain propagation if available

% constraint forall (r in 1..9)(row_diff(r));

% predicate col_diff(int: c) =
%      all_different (r in 1..9) (sq[r, c])  :: domain; %% the annotation "domain" tells the solver to use domain propagation if available

% constraint forall (c in 1..9)(col_diff(c));

% predicate block_diff(int: i, int: j) = % i block index for rows, j block index for columns (i, j 0..2)
%      all_different (r , c in 1..3) (sq[3*i+r, 3*j+c])  :: domain; %% the annotation "domain" tells the solver to use domain propagation if available

% constraint forall (i,j in 0..2)(block_diff(i,j));