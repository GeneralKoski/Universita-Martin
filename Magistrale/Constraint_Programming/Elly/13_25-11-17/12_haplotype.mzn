%% Haplotype by pure parsimony

include "globals.mzn";

int: n = 4; %%% number of SNP (genotype's length)
int: m = 5; %%% number of genotypes strings
array [1..m,1..n] of int:
%   geno =  [| 1,2,0,1,
%            | 2,0,0,1,
%            | 0,1,0,2 |];

  geno = [| 1,2,0,1,
          | 2,0,0,1,
          | 0,1,0,2,
          | 1,0,2,0,
          | 2,2,1,0 |];

%%%% model: each genotype i is explained by two consecutive haplo in position 2*i-1 and 2*i (indexes start from 1)
%%%% the matrix haplo contains duplicates (the more, the better!)
var 0..m*m: haplo_size;
array [1..2*m,1..n] of var 0..1: haplo;

%%% TODO: implement a version where the haplo matrix contains NO duplicates
%%% array [1..k,1..n] of var 0..1: haplo;
%%% with k increasing from m .... 2m


% explain
constraint forall(i in 1..m,j in 1..n)(
    (geno[i,j] = 1 -> haplo[2*i-1,j]=1 /\ haplo[2*i,j] = 1) /\
    (geno[i,j] = 0 -> haplo[2*i-1,j]=0 /\ haplo[2*i,j] = 0) /\
    (geno[i,j] = 2 -> haplo[2*i-1,j] != haplo[2*i,j])
);

%breaking symmetries

% constraint forall(i in 1..m)(
%    lex_less([haplo[2*i-1,l] | l in 1..n],[haplo[2*i,l]|l in 1..n])
% );

% count for duplicates (quadratic!)
array [1..2*m,1..2*m] of var 0..1: equal;
array [1..2*m] of var 0..1: representative;

constraint forall(i in 1..2*m-1, j in i+1..2*m)(
    sum(l in 1..n)(abs(haplo[i,l]-haplo[j,l])) > 0
   <-> %%% REIFICATION
   equal[i,j] = 0
);

% Lower part of the matrix set to 0
constraint forall(i in 1..2*m, j in 1..i)(
   equal[i,j]=0
);

% identify representative (is off diagonal has no equal strings --> representative)
constraint forall(i in 1..2*m)(
   sum(j in i+1..2*m)(equal[i,j]) = 0 <-> representative[i]=1
);

constraint  haplo_size = sum(i in 1..2*m)(representative[i]);


solve
%   :: int_search(haplo,
%%++ [energy[i,j] | i,j in 1..n],
%       first_fail, indomain_min, complete) satisfy;
minimize haplo_size;

output
[show(haplo_size), " haplotypes used"] ++
[if j == 1 then "\n" else " " endif ++
    show(geno[i,j])
 | i in 1..m, j in 1..n]
++ ["\n---------"] ++
[if j == 1 then "\n" else " " endif ++
    show(haplo[i,j])
 | i in 1..2*m, j in 1..n]
++ ["\n--------- equal"] ++
[if j == 1 then "\n" else " " endif ++
    show(equal[i,j])
 | i in 1..2*m, j in 1..2*m]
++ ["\n", show(representative)]
