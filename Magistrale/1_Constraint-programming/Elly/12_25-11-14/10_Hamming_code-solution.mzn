%% Hamming Codes - By AD 2016

include "globals.mzn";

% 9,7,5 unsat (search with options)
% 34.2 s with mylex, 25.2 s with lex_less, LIMIT without

int: n=6; %11;
int: k=4; %16;
int: d=4; %5

array[1..k,1..n] of var 0..1: code;


%constraint forall(i in 1..k-1, j in i+1..k)(
constraint forall(i,j in 1..k where i <j)(
    sum(l in 1..n)(abs(code[i,l]-code[j,l])) >= d
);

%%% REDUNDANT CONSTRAINTS (Breaking Symmetries)

constraint forall(j in 1..n)(code[1,j] = 0);

%constraint forall(i in 1..k-1)(lex_less([code[i,l] | l in 1..n],[code[i+1,l]|l in 1..n]));

%%% MY LEXICOGRAPHIC <

constraint     forall(i in 1..k-1)( mylex([code[i,j] | j in 1..n],  [code[i+1,j] | j in 1..n])) ;


predicate mylex(array [1..n] of var 0..1: first,
                array [1..n] of var 0..1: second) =
    let { array [1..n] of var bool: temp} in
        (temp[n] = (first[n] <second[n]) /\
         temp[1] = true /\
         forall(j in 1..n-1)(
             temp[n-j] =  (first[n-j] < second[n-j]) \/
                                 ((first[n-j] = second[n-j]) /\ temp[n-j+1])
            ));

solve satisfy;
%solve :: int_search([code[i,j] | i in 1..k,j in 1..n], first_fail, indomain_min, complete) satisfy;

output[
  if j = 1 then "\n" else " " endif
  ++
  show(code[i,j])
  | i in 1..k, j in 1..n
] ;