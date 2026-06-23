%
% Cumulative Scheduling in Minizinc
%
%
% Example from the Sisctus documentation:
% http://www.sics.se/sicstus/docs/latest/html/sicstus/Cumulative-Scheduling.html#Cumulative%20Scheduling

% """
% Cumulative Scheduling

% This example is a very small scheduling problem. We consider seven
% tasks where each task has a fixed duration and a fixed amount of used
% resource:

% Task Duration Resource
%  t1    16       2
%  t2     6       9
%  t3    13       3
%  t4     7       7
%  t5     5      10
%  t6    18       1
%  t7     4      11

% The goal is to find a schedule that minimizes the completion time for
% the schedule while not exceeding the capacity 13 of the resource. The
% resource constraint is succinctly captured by a cumulative/4
% constraint. Branch-and-bound search is used to find the minimal
% completion time.

% This example was adapted from [Beldiceanu & Contejean 94].
% """
%
% Model created by Hakan Kjellerstrand, hakank@bonetmail.com
% See also my MiniZinc page: http://www.hakank.org/minizinc
%

include "globals.mzn";

array[1..7] of int: Ds = [16, 6,13, 7, 5,18, 4];   %%%% Duration times
array[1..7] of int: Rs = [ 2, 9, 3, 7,10, 1,11];   %%%% Resources used

var int: Capacity;
array[1..7] of var 1..69: Ss;   %%% Start times
var 1..80: End;

%%% Example: activity 3 starts after the end of activity 1
constraint
    Ss[3] >= Ss[1]+ Ds[1] /\
    Ss[7] >= Ss[5]+ Ds[5] /\
    Ss[5] >= Ss[1]+ Ds[1]
    ;

predicate after(array[int] of var int: S, array[int] of var int: D, var int: E) =
   forall(i in index_set(S)) (
      E >= S[i] + D[i]
   )
;

constraint
   Capacity >= 0 /\
   Capacity <= 20 /\
   after(Ss, Ds, End) /\
   cumulative(Ss, Ds, Rs, Capacity)
;


solve
%:: int_search(Ss ++ Ds,
%        first_fail, indomain_min, complete)
%minimize Capacity;
minimize End;



output [
"Capacity: " ++ show(Capacity) ++ "\n"++
"Ss: " ++ show(Ss) ++ "\n"++
"End: " ++ show(End) ++ "\n"
];