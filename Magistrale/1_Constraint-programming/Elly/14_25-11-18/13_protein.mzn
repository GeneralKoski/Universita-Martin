%% Simplified 2D HP protein folding

include "globals.mzn";

int: n = 16;
array [1..n] of int:
  prot =  [  1,0,0,1,0,0,1,0,0,1,
                 0,0,1,0,0,1         ];

% int: n = 20;
% array [1..n] of int:
%   prot =  [  1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1];

array[1..n] of var 0..2*n: x;
array[1..n] of var 0..2*n: y;

% int: range =  round(sqrt(n)/1.5);
% array[1..n] of var n-range..n+range: x;
% array[1..n] of var n-range..n+range: y;

array[1..n,1..n] of var 0..1: energy;
var 0..n*n: e;

% next
constraint forall(i in 1..n-1)(
    abs(x[i]-x[i+1]) + abs(y[i]-y[i+1]) = 1
);

% % no overlap
% constraint forall(i in 1..n-1, j in i+2..n)(
%     abs(x[i]-x[j]) + abs(y[i]-y[j]) >= 1
% );

% next + no overlap = saw

array [1..n] of var 0..4*n*n: pairs;
constraint forall(i in 1..n)(
   pairs[i] = n*(x[i]-1)+y[i]-1
);
constraint
   all_different(pairs)  :: domain;

% starting
% constraint
%    x[1]=n /\ x[2]=n+1 /\ y[3]>=n /\
%    y[1]=n /\ y[2]=n
%    ;

% ENERGY

constraint
forall(i in 1..n-2, j in i+2..n)
(
    ( (abs(x[i]-x[j]) + abs(y[i]-y[j]) = 1 /\
     prot[i]=1 /\ prot[j]=1) <->
     energy[i,j]=1 )
);

constraint forall(i in 1..n, j in 1..i)(
     energy[i,j]=0
)
/\
forall(i in 1..n-1)(
     energy[i,i+1]=0
);

constraint  e = sum(i,j in 1..n)(energy[i,j]);

solve maximize e;

% solve satisfy;


output
["Protein of length ", show(n), "\n",
show(prot), "\n",  show(x), "\n", show(y), "\n", show(energy), "\n", show(e),
"\n"]