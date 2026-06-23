
include "globals.mzn";

var 0..9: S;
var 0..9: E;
var 0..9: N;
var 0..9: D;
var 0..9: M;
var 0..9: O;
var 0..9: R;
var 0..9: Y;

var 0..1: C1;
var 0..1: C2;
var 0..1: C3;
var 0..1: C4;


%   4321 (Carry)
%    SEND
%  + MORE
%  ------
%   MONEY

% constraint
%      D + E = 10* C1 + Y
% ;

% constraint
%      C1 + N + R = 10* C2 + E
% ;

% constraint
%      C2 + E + O = 10* C3 + N
% ;
% constraint
%      C3 + S + M = 10* C4 + O
% ;

% constraint
%      C4 = M /\
%      S > 0 /\
%      M > 0
% ;

constraint
            1000*S + 100*E + 10*N + D  +
            1000*M + 100*O + 10*R + E  =
  10000*M + 1000*O + 100*N + 10*E + Y
 /\
 S > 0 /\
 M > 0
;





%%% THEY SHOULD BE ALL DIFFERENT:
% constraint
%  S != E /\ S!= N /\ S!= D /\ S!= M /\ S!= O /\ S!= R /\ S!= Y /\
%            E!= N /\ E!= D /\ E!= M /\ E!= O /\ E!= R /\ E!= Y /\
%                     N!= D /\ N!= M /\ N!= O /\ N!= R /\ N!= Y /\
%                              D!= M /\ D!= O /\ D!= R /\ D!= Y /\
%                                       M!= O /\ M!= R /\ M!= Y /\
%                                                O!= R /\ O!= Y /\
%                                                         R!= Y  ;

constraint all_different([S,Y,R,E,N,D,M,O]);

%solve satisfy;

solve :: int_search([S,Y,R,E,N,D,M,O],
 %input_order,
 first_fail,
% most_constrained,

 %indomain,
 %indomain_split,
 %indomain_min,
 %indomain_median,
 %indomain_random,
 indomain_split,

 complete) satisfy;


output [
%   show(fd), "\n",
   "S:", show(S), " E:", show(E), " N:", show(N), " D:", show(D),
   " M:", show(M), " O:", show(O), " R:", show(R), " Y:", show(Y),
   "\n\n",

   "    ", show(S), show(E), show(N), show(D),"\n",
   "+   ", show(M), show(O), show(R), show(E),"\n",
   " = ",  show(M), show(O), show(N), show(E), show(Y), "\n"

];